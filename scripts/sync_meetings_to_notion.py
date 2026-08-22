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

    python scripts/sync_meetings_to_notion.py            # 全件転記（既存スキップ）
    python scripts/sync_meetings_to_notion.py --dry-run  # 書き込まずに確認
    python scripts/sync_meetings_to_notion.py --limit 1  # 最新1件だけ転記

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


def rt(content: str) -> list[dict]:
    """Notion rich_text ブロック用のヘルパー（plain text のみ）。"""
    return [{"type": "text", "text": {"content": content}}]


def h2(text: str) -> dict:
    """Notion heading_2 ブロック。"""
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": rt(text)}}


def divider() -> dict:
    """Notion divider ブロック。"""
    return {"object": "block", "type": "divider", "divider": {}}


def paragraph(text: str) -> dict:
    """Notion paragraph ブロック。"""
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rt(text)}}


def bullet(text: str) -> dict:
    """Notion bulleted_list_item ブロック。"""
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rt(text)},
    }


def todo(text: str, checked: bool = False) -> dict:
    """Notion to_do ブロック。"""
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {"rich_text": rt(text), "checked": checked},
    }


def table_row(cells: list[str]) -> dict:
    """Notion table_row ブロック（各セルは plain text）。"""
    return {
        "type": "table_row",
        "table_row": {"cells": [[{"type": "text", "text": {"content": c}}] for c in cells]},
    }


def info_table(date_str: str, title: str, members_str: str) -> dict:
    """## 基本情報 テーブルブロックを作成する。"""
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": 2,
            "has_column_header": False,
            "has_row_header": True,
            "children": [
                table_row(["日時", date_str]),
                table_row(["タイトル", title]),
                table_row(["参加者", members_str]),
                table_row(["MEMO", "喫緊の問題など"]),
            ],
        },
    }


# ─── ページ本文ビルダー ───────────────────────────────────────────────────────


def build_page_body(
    title: str,
    date_str: str,
    members_str: str,
    summary: Optional[dict],
) -> list[dict]:
    """
    確定した転記フローのページ本文テンプレートを Notion ブロックとして組み立てる。

    ## 基本情報  (テーブル)
    ---
    ## サマリー  (TLDR + 箇条書き)
    ---
    ## 決定事項  (bullets から抽出、または placeholder)
    ---
    ## タスク    (このミーティングで作成されたタスク)
    ---
    ## To Do
    ---
    ## メール提案
    """
    tldr: str = ""
    bullets: list[str] = []
    if summary:
        tldr = summary.get("tldr") or ""
        bullets = summary.get("bullets") or []

    blocks: list[dict] = []

    # ── 基本情報 ──────────────────────────────────────────────────────
    blocks.append(h2("基本情報"))
    blocks.append(info_table(date_str, title, members_str))
    blocks.append(divider())

    # ── サマリー ──────────────────────────────────────────────────────
    blocks.append(h2("サマリー"))
    if tldr:
        blocks.append(paragraph(tldr))
    for b in bullets:
        blocks.append(bullet(b))
    if not tldr and not bullets:
        blocks.append(paragraph("（サマリーなし）"))
    blocks.append(divider())

    # ── 決定事項 ──────────────────────────────────────────────────────
    blocks.append(h2("決定事項"))
    if bullets:
        # bullets の最初の1〜3件を決定事項として仮配置（人間が後で整理）
        for b in bullets[:3]:
            blocks.append(bullet(b))
    else:
        blocks.append(bullet("（確認・整理してください）"))
    blocks.append(divider())

    # ── タスク ────────────────────────────────────────────────────────
    blocks.append(h2("タスク（このミーティングで作成されたタスク）"))
    blocks.append(bullet("このミーティングではタスクは作成されませんでした"))
    blocks.append(divider())

    # ── To Do ─────────────────────────────────────────────────────────
    blocks.append(h2("To Do"))
    blocks.append(todo("次回までにしなければならないことを記入してください"))
    blocks.append(divider())

    # ── メール提案 ────────────────────────────────────────────────────
    blocks.append(h2("メール提案"))
    # 件名
    blocks.append(paragraph(f"件名: {title}のお礼とご確認"))
    blocks.append(paragraph("---"))

    decision_text = bullets[0] if bullets else "（決定内容を記入してください）"
    email_body = (
        "【相手の名前】様\n\n"
        "本日はお忙しい中、お時間をいただきありがとうございました。\n"
        "改めて、本日ご確認いただいた内容を共有させていただきます。\n\n"
        "■ 決定事項\n\n"
        f"- {decision_text}\n\n"
        "■ To Do\n\n"
        "- 【【相手の名前】様】（相手のTo Doを記入）\n"
        "- 【弊社 【担当者】】（こちらのTo Doを記入）\n\n"
        "引き続きよろしくお願いいたします。"
    )
    blocks.append(paragraph(email_body))

    return blocks


# ─── ページペイロードビルダー ─────────────────────────────────────────────────


def build_notion_page(meeting: dict, detail: Optional[dict] = None) -> dict:
    """
    Notion ページ作成用のペイロードを組み立てる。

    Notion DB プロパティ:
        Title  : 会議タイトル (title 型)
        Date   : 会議日・ISO 形式 (date 型)
        Member : 参加者・カンマ区切り (rich_text 型)
        MEMO   : 必要に応じてメモを追記 (rich_text 型、通常空欄)
    """
    title = meeting.get("title") or "（タイトルなし）"
    date_str = format_date(meeting.get("created_at", datetime.now(timezone.utc).isoformat()))
    summary = meeting.get("summary") or (detail.get("summary") if detail else None)

    # 参加者（カンマ区切り）
    members_str = ""
    if detail:
        participants = detail.get("participants", [])
        names = [p.get("name", "") for p in participants if p.get("name")]
        members_str = ", ".join(names)

    # ページ本文
    children = build_page_body(title, date_str, members_str, summary)

    payload: dict[str, Any] = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Title": {
                "title": [{"type": "text", "text": {"content": title}}]
            },
            "Date": {"date": {"start": date_str}},
            "MEMO": {
                "rich_text": []  # ユーザーが後から記入
            },
        },
        "children": children,
    }

    if members_str:
        payload["properties"]["Member"] = {
            "rich_text": [{"type": "text", "text": {"content": members_str[:2000]}}]
        }

    return payload


def create_notion_page(payload: dict, dry_run: bool = False) -> Optional[str]:
    """Notion にページを作成する。dry_run=True の場合は作成しない。"""
    title = payload["properties"]["Title"]["title"][0]["text"]["content"]
    date = payload["properties"]["Date"]["date"]["start"]

    if dry_run:
        print(f"  [DRY-RUN] {date} / {title}")
        return "dry-run"

    url = f"{NOTION_API_BASE}/pages"
    resp = requests.post(url, headers=notion_headers(), json=payload, timeout=30)
    if resp.status_code == 200:
        page_id = resp.json().get("id", "")
        print(f"  [OK] {date} / {title}  (id: {page_id})")
        return page_id
    else:
        print(f"  [ERROR] {date} / {title}: {resp.status_code} {resp.text[:300]}")
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
        "--limit",
        type=int,
        default=0,
        metavar="N",
        help="先頭 N 件だけ転記する（0 = 全件）",
    )
    parser.add_argument(
        "--no-skip-existing",
        action="store_true",
        help="既存チェックをせず全件作成する",
    )
    parser.add_argument(
        "--dump-payload",
        action="store_true",
        help="1 件目のペイロードを JSON で標準出力に表示する（デバッグ用）",
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
    meetings.sort(key=lambda m: m.get("created_at", ""), reverse=True)
    print(f"  → {len(meetings)} 件のミーティングを取得\n")

    if args.limit > 0:
        meetings = meetings[: args.limit]
        print(f"[--limit {args.limit}] 最新 {args.limit} 件のみ処理します\n")

    # 既存 Notion ページのタイトル一覧を取得（スキップ判定用）
    existing_titles: set[str] = set()
    if not args.no_skip_existing and not args.dry_run:
        print("Notion の既存ページを確認中...")
        existing_titles = get_existing_notion_titles()
        print(f"  → {len(existing_titles)} 件の既存ページを確認\n")

    # 転記処理
    created = 0
    skipped = 0
    failed = 0
    first_payload_dumped = False

    print("転記を開始します...")
    for meeting in meetings:
        title = meeting.get("title") or "（タイトルなし）"
        date_str = format_date(meeting.get("created_at", ""))

        if not args.no_skip_existing and title in existing_titles:
            print(f"  [SKIP] {date_str} / {title}（既存）")
            skipped += 1
            continue

        # 詳細情報を取得（参加者リスト取得のため常に呼ぶ）
        detail = None
        try:
            detail = get_cogno_meeting(meeting["meeting_id"])
        except Exception as e:
            print(f"  [WARN] 詳細取得失敗: {title}: {e}")

        payload = build_notion_page(meeting, detail)

        # --dump-payload: 1件目のペイロードを JSON 出力
        if args.dump_payload and not first_payload_dumped:
            print("\n=== ペイロード (JSON) ===")
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            print("=========================\n")
            first_payload_dumped = True

        page_id = create_notion_page(payload, dry_run=args.dry_run)

        if page_id:
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
