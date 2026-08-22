# ミーティング自動転記ガイド

Cogno notetaker が記録したミーティングを Notion の会議録データベースへ
自動的に転記する仕組みの設定・運用方法を説明する。

## 構成ファイル

```
scripts/sync_meetings_to_notion.py   ← 転記スクリプト本体
templates/meeting-minutes-template.md ← 転記フォーマット仕様
.github/workflows/sync-meetings.yml   ← GitHub Actions（毎日自動実行）
```

---

## 初期セットアップ

### 1. GitHub Secrets の登録

GitHub リポジトリの **Settings → Secrets and variables → Actions** で
以下の5つを登録する。

| Secret 名 | 説明 | 取得場所 |
|---|---|---|
| `COGNO_API_TOKEN` | Cogno API 認証トークン（`Bearer xxx` 形式） | Cogno 管理者に確認 |
| `COGNO_API_ENDPOINT` | Cogno API のベース URL | Cogno 管理者に確認 |
| `COGNO_WORKSPACE_ID` | Cogno ワークスペース ID | `.cogno/repo.json` |
| `NOTION_API_TOKEN` | Notion インテグレーション トークン（`secret_xxx`） | Notion → 設定 → インテグレーション |
| `NOTION_DATABASE_ID` | 転記先データベース ID | `d1f19bb4-5186-4b35-a534-076bdd37a4e1` |

### 2. Notion インテグレーションの権限設定

Notion のデータベースページで：
1. 右上「…」→「接続を追加」
2. 作成したインテグレーションを選択して追加

### 3. 動作確認（Dry-run）

GitHub Actions の **Actions** タブ → **Cogno ミーティング自動転記** →
**Run workflow** → **dry_run: true** で実行して、転記対象一覧が表示されることを確認する。

---

## 定期実行スケジュール

`.github/workflows/sync-meetings.yml` の設定で **毎日 JST 9:00** に自動実行される。

```yaml
schedule:
  - cron: "0 0 * * *"   # UTC 0:00 = JST 9:00
```

スケジュールを変更する場合は `cron` 式を編集する（[crontab.guru](https://crontab.guru) で確認可能）。

---

## スクリプトの動作仕様

1. Cogno API から全ミーティングを取得（新しい順にソート）
2. Notion データベースの既存ページタイトルを取得
3. 未転記のミーティングだけを Notion に作成（既存はスキップ）
4. 各ページに以下を設定:
   - **Title**: ミーティング名
   - **Date**: 開催日（`YYYY-MM-DD`）
   - **Member**: 参加者リスト（`--fetch-detail` 指定時のみ）
   - **MEMO**: 要約（TLDR）
   - **本文**: 詳細な箇条書き

### 重複防止ロジック

Notion 上の既存ページのタイトルと一致する場合はスキップする。
同名タイトルのミーティングが複数ある場合（例：「Arcbricks 定例会」が週次で存在）は
最初の1件のみ転記される。

> **回避策**: 同名ミーティングを区別する場合は Cogno 上でタイトルに日付を含める
> （例: `Arcbricks定例会 2026-08-13`）。

---

## ローカル実行

```bash
# 依存パッケージのインストール
pip install requests python-dateutil

# 環境変数を設定してスクリプトを実行
export COGNO_API_TOKEN="Bearer <token>"
export COGNO_API_ENDPOINT="https://api.cogno.ai"
export COGNO_WORKSPACE_ID="<workspace_id>"
export NOTION_API_TOKEN="secret_<token>"
export NOTION_DATABASE_ID="d1f19bb4-5186-4b35-a534-076bdd37a4e1"

# テスト実行（書き込みなし）
python scripts/sync_meetings_to_notion.py --dry-run

# 本番実行（既存スキップ・参加者なし）
python scripts/sync_meetings_to_notion.py

# 参加者情報も取得する（API 呼び出し増加・処理遅延あり）
python scripts/sync_meetings_to_notion.py --fetch-detail
```

---

## トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| `COGNO_API_TOKEN` エラー | 環境変数が未設定 | GitHub Secrets を確認 |
| Notion 401 エラー | トークン期限切れまたは権限不足 | Notion インテグレーション設定を再確認 |
| 既存ミーティングが重複作成される | 同名タイトルが異なる | `--no-skip-existing` を外す |
| 参加者が空欄 | `--fetch-detail` 未指定 | フラグを追加して実行 |
| 文字数制限エラー | MEMO が 2000 文字超 | スクリプトが自動切り捨て（正常動作） |
