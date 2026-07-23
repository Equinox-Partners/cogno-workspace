# CLAUDE.md

## プロジェクト概要

Cogno Workerが共通のGitHub環境からタスクを実行するためのワークスペース。
2人以上のWorkerが同時に独立したブランチで作業できる。

## ルール

- ブランチ名は `task-<タスクID>` 形式にする
- mainブランチへの直接pushは禁止（PRを通す）
- worktreeは `.cogno/agents/task-<ID>/` に作成する

## ディレクトリ構成

```
cogno-workspace/
├── CLAUDE.md          # このファイル（Worker向け指示）
├── .cogno/
│   ├── .gitignore     # agents/, visual/ を除外
│   ├── app-context.md # アプリ情報・認証情報
│   └── repo.json      # Cognoのリポジトリ設定
└── [プロジェクトファイル]
```

## 並行作業について

複数のWorkerが同時に動く場合、それぞれ別ブランチ・別worktreeで独立して作業する。
mainブランチへのmergeはPRレビュー後に行う。
