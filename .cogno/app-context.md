# アプリケーションコンテキスト

## ワークスペース概要

このリポジトリは **Cogno Worker** が共通の GitHub 環境からタスクを実行するための
ワークスペースです。複数の Worker が同時に独立したブランチ・worktree で作業できます。

## 環境情報（2026-08-18 確認済み）

| 項目              | 値                            |
| --------------- | ---------------------------- |
| OS              | macOS 26.5.1 (Darwin 25.5.0) |
| アーキテクチャ         | ARM64 (Apple Silicon)        |
| Node.js         | v22.11.0                     |
| npm             | 11.13.0                      |
| Python          | 3.14.6                       |
| Git             | 2.50.1 (Apple Git-155)       |
| GitHub CLI (gh) | 2.62.0                       |

## 認証・シークレット

以下の GitHub Secrets が必要です（`.cogno/repo.json` の `validation.requiredGitHubSecrets` 参照）。

- `COGNO_API_TOKEN` — Cogno API 認証トークン（Bearer 形式）
- `COGNO_API_ENDPOINT` — Cogno API ベース URL
- `COGNO_WORKSPACE_ID` — Cogno ワークスペース識別子（例: `cogno-workspace-001`）

設定方法：GitHub リポジトリ → Settings → Secrets and variables → Actions

## CI/CD ワークフロー

| ワークフロー                    | トリガー                   | 用途          |
| ------------------------- | ---------------------- | ----------- |
| `.github/workflows/ci.yml` | PR・push (main/develop) | 検証・テスト      |
| `.github/workflows/cd.yml` | push (main のみ)        | ビルド・デプロイ通知 |

## ブランチ・worktree 規約

- ブランチ名: `task-<タスクID>` または `cogno/<名前>-<ID>`
- worktree パス: `.cogno/agents/task-<タスクID>/`
- main への直接 push 禁止（PR 必須）

## 注意事項

- 認証情報・API キーをコードやファイルに直接記述しない
- `source/` 配下のファイルは読み取り専用（編集・削除禁止）
- `publish/[案件名]/02_確定版/` は人間のみが変更可能
