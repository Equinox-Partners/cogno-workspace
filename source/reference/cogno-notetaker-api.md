# Cogno Notetaker API リファレンス

> 確認日: 2026-08-21

Cogno タスク内から `list_meetings` / `get_meeting` の 2 つの MCP ツールで
ミーティング情報（要約・書き起こし・参加者・チャット）を取得できる。

---

## 利用可能なツール

| ツール | 返却内容 |
|---|---|
| `list_meetings` | 最新 N 件の一覧（タイトル・日時・TLDR・箇条書き要約） |
| `get_meeting` | 特定ミーティングの詳細（要約全文・書き起こし・参加者・チャット） |

---

## 使い方

### 1. 一覧取得

```
list_meetings(limit=10)
```

返却例（要約あり）:

```json
{
  "meeting_id": "71c4dfc8-...",
  "title": "cogno 定例MTG",
  "created_at": "2026-08-14T01:32:23Z",
  "summary": {
    "tldr": "...",
    "bullets": ["..."]
  }
}
```

要約が生成されていない場合は `"summary": null`。

### 2. 詳細取得（要約のみ・高速）

```
get_meeting(meeting_id="...", include_transcript=false)
```

### 3. 詳細取得（書き起こし含む）

```
get_meeting(meeting_id="...", include_transcript=true)
```

書き起こしは話者ごとの発言形式で返却される:

```
Shun Ishihara: なるほど
Yuichi Matsuoka: 一番 初め に 今 渡す って いう 機構 が あり まし て...
```

書き起こしが長い場合はページネーションが必要:

```python
# transcript_truncated == true のとき続きを取得
get_meeting(meeting_id="...", transcript_offset=<transcript_next_offset>)
```

---

## 制限・注意事項

- 録音者がワークスペースに**共有していない**ミーティングは `list_meetings` に表示されない
- 要約が生成されていないミーティングは `summary: null`（書き起こしは取得可能）
- Notion への**書き込み**は別途確認が必要（Cogno タスク内からの共有 WS への書き込みは
  制限がある可能性あり ← 2026-08-14 cogno 定例MTG で松岡が調査担当）

---

## Notion 自動転記フローへの応用

`cogno 定例MTG`（2026-08-14）で確認された未解決点は以下の 2 点だった:

1. **Meeting アプリからの情報取得** → ✅ 解決（このタスクで確認）
2. **Notion 共有 WS への書き込み** → 要確認（松岡調査中）

書き込みが解消されれば、以下の完全自動化フローが実現可能:

```
list_meetings → get_meeting → Notion ページ作成/更新
```
