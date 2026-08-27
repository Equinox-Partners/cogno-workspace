# 現在の Cogno worker 環境

確認日時: 2026-08-28 08:55 JST

## 実行環境

| 項目 | 値 |
|---|---|
| OS | macOS 26.5.1 |
| Darwin | 25.5.0 |
| アーキテクチャ | arm64 / Apple Silicon |
| ホスト名 | Trapworks-2.local |
| タイムゾーン | Asia/Tokyo (JST, +0900) |
| shell | zsh 5.9 |

## 主要 CLI

| ツール | バージョン |
|---|---|
| Git | 2.50.1 (Apple Git-155) |
| GitHub CLI | 2.62.0 |
| ripgrep | 14.1.1 |
| Node.js | v22.11.0 |
| npm | 11.13.0 |
| Python | 3.14.7 |

## Git / worktree

| 項目 | 値 |
|---|---|
| 登録チェックアウト | `/Users/Shun/Desktop/nightwoker` |
| タスク worktree | `/Users/Shun/Desktop/nightwoker/.cogno/agents/task-6429` |
| 作業ブランチ | `cogno/cogno-worker-519` |
| 確認時 HEAD | `bd8c0fd11d27ded3cb97d976ecbd6ec09869530c` |
| リモート | `https://github.com/Equinox-Partners/cogno-workspace.git` |
| アクティブな worktree 数 | 38（登録チェックアウト1 + エージェント worktree 37） |

## リポジトリ構成

| パス | 用途 |
|---|---|
| `CLAUDE.md` | Worker 向け指示 |
| `.cogno/repo.json` | Cogno リポジトリ設定 |
| `.cogno/app-context.md` | ワークスペースと環境情報 |
| `.github/workflows/ci.yml` | CI workflow |
| `.github/workflows/cd.yml` | CD workflow |
| `source/` | 読み取り専用の参照資料 |
| `drafts/` | 作業中の下書き |
| `publish/` | レビュー用・確定版の成果物 |

## Cogno 設定の要点

- Workspace ID: `cogno-workspace-001`
- Workspace name: `Cogno Worker Execution Environment`
- 並行実行: 有効
- ブランチ命名規則: `task-{taskId}` または `cogno/<task-name>-{taskId}`
- task worktree 規約: `.cogno/agents/task-{taskId}`
- 最大同時タスク数: 10
- タスクタイムアウト: 3600秒
- PR レビュー必須: false
- 自動マージ: false
- ブランチ削除（マージ後）: true

## CI/CD

| workflow | トリガー | 現在の内容 |
|---|---|---|
| `.github/workflows/ci.yml` | push（main/develop/task-*/cogno/**）+ PR（main/develop）+ workflow_dispatch | ブランチ名バリデーション + `echo "CI workflow is working"` |
| `.github/workflows/cd.yml` | push to `main` | `echo "CD workflow is working"` |

## 連携・統合状況

| 統合サービス | 状態 |
|---|---|
| GitHub Actions (CI/CD) | 有効 |
| Cogno API | 設定済み（`COGNO_API_TOKEN` Secret 必要） |
| Slack 通知 | 無効（`slackNotifications: false`） |
| Notion | MCP 経由で連携済み |
| Slack | MCP 経由で連携済み |
| Gmail | MCP 経由で連携済み |
| Google Calendar | MCP 経由で連携済み |
| Google Drive | MCP 経由で連携済み |
| Canva | MCP 経由で連携済み |
| Sentry | cogno MCP 経由で参照可能 |

## cogno MCP が提供するツール（主要なもの）

- `list_projects` / `list_skills` / `get_skill` / `load_skill` — プロジェクト・スキル管理
- `get_task` / `update_task` / `create_task` / `search_tasks` — タスク CRUD
- `submit_task_description` / `get_current_description` — タスク成果物の提出
- `report_repo_changes` — worktree・PR の登録
- `get_meeting` / `list_meetings` — ミーティングノート参照
- `get_notion_page` / `get_sentry_issue` / `get_slack_thread` — 外部サービス参照
- `upload_capture` — スクリーンショット等のファイルアップロード
- `schedule_attention` / `record_attention_outcome` — 定期チェック管理

## フィーチャーフラグ（repo.json）

| フラグ | 値 |
|---|---|
| `parallelExecution` | true |
| `rollbackOnFailure` | true |
| `healthCheck` | true |
| `slackNotifications` | false |
| `detailedLogging` | true |

## 注意事項

- 環境変数やトークン値は確認・記載していない。
- GitHub Secrets として `COGNO_API_TOKEN`, `COGNO_API_ENDPOINT`, `COGNO_WORKSPACE_ID` が必要。
- `source/` 配下と `publish/*/02_確定版/` は運用ルール上、AI が編集しない領域。
- 2026-08-23 版との差分：Node.js が v24.17.0 → v22.11.0、gh が 2.95.0 → 2.62.0、ripgrep が 15.2.0 → 14.1.1 に変化（環境バージョンが揺れている）。
