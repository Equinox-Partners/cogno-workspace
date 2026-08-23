# 現在の Cogno worker 環境

確認日時: 2026-08-23 22:28 JST

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
| GitHub CLI | 2.95.0 |
| ripgrep | 15.2.0 |
| Node.js | v24.17.0 |
| npm | 11.13.0 |
| Python | 3.14.7 |

## Git / worktree

| 項目 | 値 |
|---|---|
| 登録チェックアウト | `/Users/Shun/Desktop/nightwoker` |
| タスク worktree | `/Users/Shun/Desktop/nightwoker/.cogno/agents/task-6429` |
| 作業ブランチ | `cogno/cogno-worker-519` |
| 確認時 HEAD | `b2fc242717c3479ef8ffad13531b408a3592d97f` |
| リモート | `https://github.com/Equinox-Partners/cogno-workspace.git` |

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
- task worktree 規約: `.cogno/agents/task-{taskId}`
- 最大同時タスク数: 10
- PR レビュー必須: false
- 自動マージ: false

## CI/CD

| workflow | トリガー | 現在の内容 |
|---|---|---|
| `.github/workflows/ci.yml` | push / PR to `main`, `develop` | `echo "CI workflow is working"` |
| `.github/workflows/cd.yml` | push to `main` | `echo "CD workflow is working"` |

## 注意事項

- 環境変数やトークン値は確認・記載していない。
- GitHub Secrets として `COGNO_API_TOKEN`, `COGNO_API_ENDPOINT`, `COGNO_WORKSPACE_ID` が必要。
- `source/` 配下と `publish/*/02_確定版/` は運用ルール上、AI が編集しない領域。
