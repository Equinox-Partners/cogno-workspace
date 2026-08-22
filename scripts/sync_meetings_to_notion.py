#!/usr/bin/env python3
"""
Cogno ミーティング → Notion 自動転記スクリプト
=============================================

Cogno に記録されたミーティングを Notion の会議録データベースへ自動転記する。

使い方:
    export COGNO_API_TOKEN="Bearer <token>"
    export COGNO_API_ENDPOINT="https://api.cogno.ai"
    export COGNO_WORKSPACE_ID="<workspace_id>"
    export NOTION_API_TOKEN="secret_<token>"
    export NOTION_DATABASE_ID="d1f19bb4-5186-4b35-a534-076bdd37a4e1"

    python scripts/sync_meetings_to_notion.py
    python scripts/sync_meetings_to_notion.py --dry-run   # 実際には書き込まない

必要パッケージ:
    pip install requests python-dateutil
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional

import requests
from dateutil import parser as dateutil_parser


# ─── 設定 ─────────────────────────────────────────────────────────────────────

COGNO_API_TOKEN = os.environ.get("COGNO_API_TOKEN", "")
COGNO_API_ENDPOINT = os.environ.get("COGNO_API_ENDPOINT", "https://api.cogno.ai")
COGNO_WORKSPACE_ID = os.environ.get("COGNO_WORKSPACE_ID", "")
NOTION_API_TOKEN = os.environ.get("NOTION_API_TOKEN", "")
NOTION_DATABASE_ID = os.environ.get(
    "NOTION_DATABASE_ID", "d1f19bb4-5186-4b35-a534-076bdd37a4e1"
)

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


# ─── Cogno API ────────────────────────────────────────────────────────────────


def cogno_headers() -> dict:
    return {
        "Authorization": COGNO_API_TOKEN,
        "Content-Type": "application/json",
    }


def list_cogno_meetings() -> list[dict]:
    """Cogno から全ミーティングを取得する。"""
    url = f"{COGNO_API_ENDPOINT}/workspaces/{COGNO_WORKSPACE_ID}/meetings"
    resp = requests.get(url, headers=cogno_headers(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # API レスポンス形式に応じて調整する（meetings キーまたはリスト直接）
    if isinstance(data, list):
        return data
    return data.get("meetings", [])


def get_cogno_meeting(meeting_id: str) -> dict:
    """1件のミーティング詳細（参加者・transcript 含む）を取得する。"""
    url = f"{COGNO_API_ENDPOINT}/workspaces/{COGNO_WORKSPACE_ID}/meetings/{meeting_id}"
    resp = requests.get(url, headers=cogno_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


# ─── Notion API ───────────────────────────────────────────────────────────────


def notion_headers() -> dict:
    return {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def get_existing_notion_titles() -> set[str]:
    """データベース内の既存ページタイトル一覧を取得する（重複作成防止）。"""
    titles: set[str] = set()
    url = f"{NOTION_API_BASE}/databases/{NOTION_DATABASE_ID}/query"
    cursor: Optional[str] = None

    while True:
        body: dict = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        resp = requests.post(url, headers=notion_headers(), json=body, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        for page in data.get("results", []):
            props = page.get("properties", {})
            title_prop = props.get("Title") or props.get("名前") or props.get("title")
            if not title_prop:
                continue
            rich = title_prop.get("title", [])
            if rich:
                titles.add(rich[0].get("plain_text", ""))

        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")

    return titles


def format_date(created_at: str) -> str:
    """ISO 8601 文字列を YYYY-MM-DD に変換する。"""
    dt = dateutil_parser.parse(created_at)
    return dt.date().isoformat()


def build_notion_page(meeting: dict, detail: Optional[dict] = None) -> dict:
    """
    Notion ページ作成用のペイロードを組み立てる。

    Notion DB フィールド:
        Title  : ミーティング名 (title 型)
        Date   : 開催日 (date 型)
        Member : 参加者リスト (rich_text 型)
        MEMO   : 要約/TLDR (rich_text 型)
    """
    title = meeting.get("title") or "（タイトルなし）"
    date_str = format_date(meeting.get("created_at", datetime.now(timezone.utc).isoformat()))
    summary = meeting.get("summary") or {}
    tldr = summary.get("tldr", "") if summary else ""
    bullets: list[str] = summary.get("bullets", []) if summary else []

    # 参加者リスト（detail が取得できた場合のみ）
    members: list[str] = []
    if detail:
        participants = detail.get("participants", [])
        members = [p.get("name", "") for p in participants if p.get("name")]

    # ページ本文ブロック（要約箇条書き）
    children: list[dict] = []
    if tldr:
        children.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": tldr}}]
                },
            }
        )
    if bullets:
        children.append(
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "議事内容"}}]
                },
            }
        )
        for b in bullets:
            children.append(
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": b}}]
                    },
                }
            )

    payload: dict[str, Any] = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Title": {
                "title": [{"type": "text", "text": {"content": title}}]
            },
            "Date": {"date": {"start": date_str}},
            "MEMO": {
                "rich_text": [
                    {"type": "text", "text": {"content": tldr[:2000] if tldr else ""}}
                ]
            },
        },
    }

    if members:
        payload["properties"]["Member"] = {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "、".join(members)[:2000]},
                }
            ]
        }

    if children:
        payload["children"] = children

    return payload


def create_notion_page(payload: dict, dry_run: bool = False) -> Optional[str]:
    """Notion にページを作成する。dry_run=True の場合は作成しない。"""
    title = payload["properties"]["Title"]["title"][0]["text"]["content"]
    date = payload["properties"]["Date"]["date"]["start"]

    if dry_run:
        print(f"  [DRY-RUN] {date} / {title}")
        return None

    url = f"{NOTION_API_BASE}/pages"
    resp = requests.post(url, headers=notion_headers(), json=payload, timeout=30)
    if resp.status_code == 200:
        page_id = resp.json().get("id", "")
        print(f"  [OK] {date} / {title}  (id: {page_id})")
        return page_id
    else:
        print(f"  [ERROR] {date} / {title}: {resp.status_code} {resp.text[:200]}")
        return None


# ─── メイン処理 ───────────────────────────────────────────────────────────────


def validate_env() -> list[str]:
    """必須環境変数の確認。不足があればリストで返す。"""
    missing = []
    if not COGNO_API_TOKEN:
        missing.append("COGNO_API_TOKEN")
    if not COGNO_WORKSPACE_ID:
        missing.append("COGNO_WORKSPACE_ID")
    if not NOTION_API_TOKEN:
        missing.append("NOTION_API_TOKEN")
    return missing


def main() -> None:
    parser = argparse.ArgumentParser(description="Cogno ミーティング → Notion 自動転記")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Notion への書き込みを行わず、転記対象のみ表示する",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        default=True,
        help="Notion に同名タイトルが存在する場合はスキップする（デフォルト: True）",
    )
    parser.add_argument(
        "--no-skip-existing",
        dest="skip_existing",
        action="store_false",
        help="既存チェックをせず全件作成する",
    )
    parser.add_argument(
        "--fetch-detail",
        action="store_true",
        default=False,
        help="参加者情報を取得するため各ミーティングの詳細 API を呼ぶ（低速・API 消費大）",
    )
    args = parser.parse_args()

    # 環境変数チェック
    missing = validate_env()
    if missing:
        print(f"[ERROR] 以下の環境変数が設定されていません: {', '.join(missing)}")
        print("  export COGNO_API_TOKEN='Bearer <token>'")
        print("  export COGNO_WORKSPACE_ID='<workspace_id>'")
        print("  export NOTION_API_TOKEN='secret_<token>'")
        sys.exit(1)

    print("=== Cogno → Notion ミーティング転記ツール ===")
    if args.dry_run:
        print("[DRY-RUN モード] Notion への書き込みは行いません\n")

    # Cogno からミーティング一覧を取得
    print("Cogno からミーティング一覧を取得中...")
    meetings = list_cogno_meetings()
    # 新しい順に並び替え
    meetings.sort(key=lambda m: m.get("created_at", ""), reverse=True)
    print(f"  → {len(meetings)} 件のミーティングを取得\n")

    # 既存 Notion ページのタイトル一覧を取得（スキップ判定用）
    existing_titles: set[str] = set()
    if args.skip_existing and not args.dry_run:
        print("Notion の既存ページを確認中...")
        existing_titles = get_existing_notion_titles()
        print(f"  → {len(existing_titles)} 件の既存ページを確認\n")

    # 転記処理
    created = 0
    skipped = 0
    failed = 0

    print("転記を開始します...")
    for meeting in meetings:
        title = meeting.get("title") or "（タイトルなし）"
        date_str = format_date(meeting.get("created_at", ""))

        if args.skip_existing and title in existing_titles:
            print(f"  [SKIP] {date_str} / {title}（既存）")
            skipped += 1
            continue

        # 詳細情報の取得（オプション）
        detail = None
        if args.fetch_detail:
            try:
                detail = get_cogno_meeting(meeting["meeting_id"])
            except Exception as e:
                print(f"  [WARN] 詳細取得失敗: {title}: {e}")

        payload = build_notion_page(meeting, detail)
        page_id = create_notion_page(payload, dry_run=args.dry_run)

        if args.dry_run or page_id:
            created += 1
        else:
            failed += 1

    # 結果サマリ
    print(f"\n=== 完了 ===")
    print(f"  作成: {created} 件")
    print(f"  スキップ（既存）: {skipped} 件")
    if failed:
        print(f"  失敗: {failed} 件")


if __name__ == "__main__":
    main()
