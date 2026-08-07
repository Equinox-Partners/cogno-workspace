# README.md

## プロジェクト概要
Cogno Workerがローカル環境からタスクを実行するためのワークスペース。
2人以上のWorkerが同時に作業できる。

---

## ⚠️ GitHub リモート未設定について（重要）

このワークスペースには **GitHub リモートリポジトリが設定されていません**。

そのため、以下の問題が発生しています：
- Cogno AIワーカーが `cogno/task-*` ブランチを作成しても、push できない
- `gh pr create` が失敗する（GitHub CLI 連携不可）
- ブランチ上の成果物が main にマージされず、ローカルに蓄積され続ける

### 現在未マージのブランチ（手動でマージ or 確認が必要）

| ブランチ名 | 内容 |
|---|---|
| `cogno/task-4344` | ミーティング議事録のNotion自動保存ルールをREADMEに追加 |
| `cogno/task-4524` | Enoshima SVGイラスト追加 |
| `cogno/task-4816-airbnb-sheets-automation` | AirBnB→Google Sheets 自動化スクリプト群 |
| `cogno/task-4839` | 議事録Notion保存をフォルダ分類からフラットテーブル形式に変更 |

確認方法：`git log --all --oneline --decorate`

### GitHub リモートを接続する場合

```bash
# cogno-workspace-main（プライベート・空のリポジトリ）を使う場合
git remote add origin https://github.com/Equinox-Partners/cogno-workspace-main.git
git push -u origin main
git push origin --all  # 全ブランチをpush
```

接続後は、各ブランチを GitHub 上でPRとしてレビュー・マージできるようになります。

---

## 環境について

このワークスペースはローカル上に存在します。

### 人間のWorkerが作業する場合
- **git worktree・ブランチは使わない**
- ローカルファイルを直接編集する
- 生成ファイルは Google Drive の保存先に配置する（後述）
- Workerに共有するコンテキストは本ファイル（README.md）のみ

### Cogno AIワーカーが作業する場合（自動）
- AIワーカーは内部的に `.cogno/agents/task-<ID>/` に git worktree を作成して作業を分離する
- 成果コードは `cogno/task-<ID>` ブランチにコミットされる
- **ただしリモート未設定のため push・PR 作成は行えない**
- 成果ファイル（ドキュメント等）は Google Drive の保存先にも保存すること
- タスク説明は `submit_task_description` で納品する

---

## タスク命名ルール

タスクは以下の形式で命名する：

```
YYYY-MM-DD_<タスク内容がわかる名称>
```

例：
- `2026-08-03_見積書作成`
- `2026-08-03_議事録要約`

同日に複数タスクがある場合は、末尾に連番を付けて区別する（例：`2026-08-03_見積書作成_2`）。

---

## **重要: ファイル保存場所の厳密なルール**

**すべてのタスクで生成されたファイルは、必ず以下の場所に保存してください：**

```
/Users/Shun/マイドライブ（s.ishihara@equinox-partners.jp）/cogno storage
```

### ❌ 許可されない保存場所
- システムテンポラリ: `/tmp/file.txt`
- ホームディレクトリ直下: `~/file.txt`
- 上記パス以外の場所

タスクごとにサブフォルダ（`<タスク名>/`）を作成し、その中にファイルを保存することを推奨する。

> **AIワーカーへの補足**: git ブランチへのコミットはあくまで作業の分離・記録用です。
> レビュー・参照可能な成果物は Google Drive にも保存してください。

---

## ディレクトリ構成

```
cogno woker/                 # ローカル上のルートディレクトリ
├── README.md                # このファイル（Worker向け指示）
├── .cogno/
│   ├── agents/              # AIワーカーの git worktree（自動生成、.gitignore 対象）
│   ├── inputs/              # タスクの入力ファイル（Cognoから配置）
│   └── visual/              # ビジュアルキャプチャ用ガイド（Cognoから配置）
└── [その他プロジェクトファイル]
```

---

## 並行作業について

複数のWorkerが同時に動く場合、それぞれ別のタスクフォルダ内で独立して作業する。
同一ファイルへの同時編集を避けるため、作業対象のファイル・フォルダが他タスクと重複しないよう注意する。

---

## 作業手順（人間のWorker向け）

1. `list_skills` でスキルを確認
2. `get_current_description` でタスク説明を確認
3. タスク名（`YYYY-MM-DD_<内容>`）を決定し、対応するフォルダを作成
4. 上記の保存先パス配下でファイルを編集・生成する
5. `submit_task_description` でタスクをデリバリー
