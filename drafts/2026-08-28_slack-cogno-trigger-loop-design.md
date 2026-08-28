# SlackトリガーによるCognoクラウドコード自動実行ループ 設計書

> 作成日: 2026-08-28  
> Task: #7573

---

## 概要

Slackの特定チャンネルで発生するイベントをトリガーとして、Cogno Workerが自動的にクラウドコードを実行し、関係者へDMで通知する仕組み。「ミーティング終了」「コード変更」「リリース準備」などの業務イベントを、人間が手動で連絡しなくても自動的に通知できるようにする。

---

## アーキテクチャ全体像

```
[イベント発生源]                   [トリガー層]              [実行層]               [通知層]
Cogno ミーティング終了    ─→  schedule_attention     ─→  Cogno Worker      ─→  Slack DM
GitHub PR / commit        ─→  Cogno attention rail  ─→  クラウドコード実行  ─→  関係者へ通知
Slack チャンネル発言      ─→  Slack Event Webhook   ─→  Worker run 起動   ─→  DM テンプレート送信
Cogno タスク状態変化      ─→  attention pipeline    ─→  条件分岐・処理      ─→
```

---

## トリガー条件・チャンネル設定・通知先一覧

| # | イベント名 | 監視対象 | トリガー条件 | 通知先 | DM内容 |
|---|---|---|---|---|---|
| T1 | **ミーティング終了** | Cogno `list_meetings` | 新規ミーティングが summary 生成済み状態で登録される | 参加者全員 | TLDR要約・決定事項・Todoリスト |
| T2 | **コード変更** | GitHub main branch | PR が merge されたとき | 開発チームメンバー | PR タイトル・変更ファイル数・レビュアー |
| T3 | **リリース準備** | GitHub tags / Slack `#releases` | `v*.*.*` タグが作成された / `[RELEASE]` キーワード発言 | PO・QA・開発リード | リリースバージョン・含まれる変更・チェックリスト |
| T4 | **タスク状態変化** | Cogno タスク一覧 | タスクが `ready` または `in_review` に変化 | タスク担当者・関連メンバー | タスクタイトル・現状・次のアクション |
| T5 | **Slack メンション** | `#cogno-bot` チャンネル | `@cogno` メンションを含む発言 | 発言者（即時応答） | 問い合わせへの回答・関連タスクリンク |

---

## チャンネル設定

| Slack チャンネル | 役割 | 購読するイベント |
|---|---|---|
| `#cogno-updates` | Cogno Worker からの自動通知（読み取り専用） | なし（出力のみ） |
| `#cogno-bot` | ユーザーが `@cogno` でコマンドを送るチャンネル | `app_mention` |
| `#dev-updates` | コード変更・PR通知 | `message.channels`（GitHub integration） |
| `#releases` | リリース関連の発言 | `message.channels`（`[RELEASE]` キーワード） |
| `#meeting-updates` | ミーティング終了通知（自動投稿） | なし（出力のみ） |

---

## ループ設計詳細

### ループ1：ミーティング終了トリガー（T1）

```
[schedule_attention] PT15M間隔でポーリング
  ↓
list_meetings(limit=20) で新規ミーティングを確認
  ↓
前回チェック以降に summary が生成されたミーティングを抽出
  ↓
get_meeting(meeting_id, include_transcript=false) で詳細取得
  ↓
参加者リストを取得 → Slack user ID に変換
  ↓
各参加者に DM 送信（テンプレートT1使用）
  ↓
Notion に転記（既存フロー）
  ↓
schedule_attention(subject="meeting-check", wake_in="PT15M") で再スケジュール
```

**DM テンプレート（T1）：**
```
📋 ミーティング終了: {title}

🕐 日時: {date} ({duration}分)
👥 参加者: {members}

📌 TLDR
{tldr}

✅ 決定事項
{bullets}

📝 あなたのTodo
{todos_for_this_person}

🔗 詳細: {notion_link}
```

---

### ループ2：コード変更トリガー（T2）

```
GitHub Webhook → Slack `#dev-updates` に自動投稿（既存）
  ↓
Cogno Worker が #dev-updates を監視（schedule_attention PT30M間隔）
  ↓
search_slack_messages(channel="#dev-updates", since=last_check) で新規PR確認
  ↓
マージされたPRを抽出
  ↓
開発チームメンバーリストを参照 → Slack DM送信
  ↓
Cogno タスク（コード変更）に関連タスクがあれば自動リンク
```

**DM テンプレート（T2）：**
```
🔀 PRがマージされました

#{pr_number} {pr_title}
👤 作成者: {author} / レビュアー: {reviewers}
📁 変更ファイル: {changed_files}件
🔗 {pr_url}
```

---

### ループ3：リリース準備トリガー（T3）

```
GitHub tag 作成（v*.*.*）または #releases での [RELEASE] 発言
  ↓
Cogno Worker が検知（schedule_attention または Slack Webhook）
  ↓
リリースバージョン・変更内容を収集
  ↓
PO・QA・開発リードに DM 送信
  ↓
リリースチェックリストをDMに添付
  ↓
Cogno タスク「リリース確認」を自動作成
```

**DM テンプレート（T3）：**
```
🚀 リリース準備開始: {version}

📋 含まれる変更（{pr_count}件のPR）
{pr_list}

✅ チェックリスト
- [ ] QAテスト完了確認
- [ ] ステージング環境での動作確認  
- [ ] リリースノート作成
- [ ] デプロイ承認

🔗 リリースページ: {release_url}
```

---

### ループ4：タスク状態変化トリガー（T4）

```
schedule_attention(subject="task-status-check", wake_in="PT1H") で定期実行
  ↓
search_tasks(status_changed_since=last_check) で変化したタスクを確認
  ↓
ready / in_review に変化したタスクを抽出
  ↓
タスク担当者・関連メンバーに Slack DM 送信
  ↓
次のアクションを提示
```

---

## 実装ステップ

### Phase 1：基盤整備（今すぐ実施可能）

1. **Cogno attention スケジュール設定**
   - `schedule_attention` でT1（ミーティング終了）を最初に設定
   - ポーリング間隔: 15分

2. **通知先メンバーリスト作成**（`source/reference/notification-targets.md`）
   - 開発チーム: [Slack user ID リスト]
   - PO: [Slack user ID]
   - QA: [Slack user ID]
   - 開発リード: [Slack user ID]

3. **DM テンプレートファイル整備**（`source/reference/dm-templates.md`）

### Phase 2：Slack Webhook 連携（要Slack App設定）

4. **Slack App 作成・設定**
   - Event Subscriptions: `app_mention`, `message.channels`
   - Bot Token Scopes: `chat:write`, `im:write`, `channels:history`
   - Webhook URL: Cogno Remote Trigger エンドポイント

5. **#cogno-bot チャンネルでのメンション対応**（T5）

### Phase 3：GitHub 連携（要GitHub App設定）

6. **GitHub Webhook 設定**
   - PR merge イベント → Cogno trigger
   - Tag 作成イベント → Cogno trigger

---

## 通知先メンバーリスト（要確認）

> ⚠️ 以下は仮定義です。実際のSlack user ID・メンバー構成を確認して更新してください。

| 役割 | 名前 | Slack User ID |
|---|---|---|
| 開発リード | （未定） | `U_______` |
| PO | （未定） | `U_______` |
| QA | （未定） | `U_______` |
| 開発チーム全員 | — | チャンネル `#dev-updates` で代替 |

---

## 次のアクション

- [ ] 通知先メンバーリストの実際のSlack IDを確認・記入
- [ ] Phase 1 の `schedule_attention` 設定を実際に走らせる
- [ ] Slack App の Bot Token を Cogno 環境変数に登録
- [ ] ミーティング終了ループ（T1）から先行実装・検証

