# Cogno Worker 実行指示書

このファイルは Claude Code がセッション開始時に読み込む、Cogno Worker 向けの
リポジトリ指示です。Cogno から渡される Work Item 指示がある場合は、そちらを
優先してください。

## 1. ワークスペースの目的

Cogno Worker が共通の GitHub リポジトリからタスクを実行するための
ワークスペースです。複数の Worker が同時に、独立したブランチと worktree で
作業できます。

主な作業は、Equinox Partners のプロジェクト管理と資料作成の支援です。
会議要約、提案書の初稿、進行管理表の作成などを扱います。

## 2. 指示の優先順位

矛盾がある場合は、次の順に優先します。

1. Cogno Work Item に含まれるシステム指示・納品指示
2. 認証情報、個人情報、原本保護に関する禁止事項
3. Cogno Task の本文に書かれた成果物、保存先、完了条件
4. この `CLAUDE.md`
5. `source/` 内の参照資料

## 3. Claude Code と Cogno の接続

- Claude Code と Cogno Worker の接続、ローカル hook、MCP、Unix socket 連携を
  妨げないでください。
- `.claude/settings.local.json` などに Cogno が追加した hook は削除・無効化しないで
  ください。
- Cogno Work Item が GitHub への commit、push、PR 作成、Cogno MCP での納品を
  明示している場合、その指示に従ってください。
- main ブランチへ直接 push しないでください。変更は task 用ブランチから PR にします。

## 4. 作業開始時の確認

1. Cogno Work Item の本文を読み、成果物、保存先、完了条件を確認します。
2. 作業対象がリポジトリ変更の場合は、指定された隔離 worktree で作業します。
3. Task で指定された `source/` 内の参照ファイルを確認します。
4. 成果物の品質、安全性、保存先に影響する不明点は、作業結果に質問として明記します。
5. 影響が小さい不明点は、合理的な仮定を明記して作業を進めます。

## 5. ディレクトリ構成

```text
cogno-workspace/
├── CLAUDE.md
├── .cogno/
│   ├── .gitignore
│   ├── app-context.md
│   └── repo.json
├── source/
│   ├── meeting-notes/
│   ├── client-briefs/
│   └── reference/
├── drafts/
└── publish/
    └── [案件名]/
        ├── 01_レビュー待ち/
        └── 02_確定版/
```

## 6. 禁止事項

- `source/` 配下のファイルを編集・削除・移動しないでください。
- `publish/[案件名]/02_確定版/` を編集しないでください。
- 認証情報、API キー、個人情報を成果物に含めないでください。
- Task で指定されていないフォルダに成果物を作らないでください。
- メール、Slack、Web フォーム、外部 API への送信は、Task が明示しない限り行わないで
  ください。

## 7. 成果物のルール

完成物は原則として `publish/[案件名]/01_レビュー待ち/` に置きます。
`02_確定版/` への移動は人間が行います。

ファイル名は、Task で別指定がない限り次の形式にします。

```text
YYYY-MM-DD_[案件名]_[内容]_[版].[拡張子]
```

成果物では次を区別してください。

- 確認済み事実: 根拠となるファイル名または会議日時を添える
- 推測・仮説: 推測であることを明示する
- 未確認事項: 成果物の末尾にまとめる

## 8. 並行作業

複数の Worker が同時に動く場合、それぞれ別ブランチ、別 worktree で独立して
作業します。既存の未コミット変更を見つけた場合は、勝手に破棄しないでください。

<!--
このファイルは Claude Code のリポジトリメモリとして読み込まれます。
参考: https://code.claude.com/docs/en/memory
-->
