---
name: group-silence-gating
description: Enforce strict group-chat silence by default and only respond when explicitly triggered (e.g., Telegram/LINE group ops). Use when you must avoid accidental bot replies in busy group chats and need deterministic “speak only on /trigger or @mention” behavior, with one-message/one-sentence replies and a fixed footer reminder.
---

# Group Silence Gating

目的：在群組裡實作 **「預設靜默」**，只有在 **硬觸發** 出現時才允許回覆，避免 bot 失控刷屏。

## Use when
- 你需要「確定不會自己插話」的群組機器人策略
- 你想把「群組回覆規則」做成 deterministic、可驗收、可重跑的能力

## Don’t use when
- 你希望 bot 能主動參與聊天、或用語意推測「好像在叫我」

## 行為規格（deterministic）

1) **Default = mute**
- 沒有硬觸發 → 不回覆（理想狀態：甚至不要把訊息送進 LLM）

2) **Hard triggers only**
- 觸發條件（任一成立）：
  - 文字包含 `/小蝦`
  - 文字包含 `@小蝦`
- 禁止語意猜測。

3) **Reply constraint（被觸發才適用）**
- 只回「那一則觸發訊息」。
- 只輸出「一句詳細回答」，不追問、不延伸。
- 尾註固定兩行：
  - `---`
  - `🦐 要找我請 @小蝦 或 /小蝦 🦐`

4) **Channel rule**
- **LINE 群組：永遠靜默**（就算觸發也不回）
- **Telegram 群組：只有觸發才回**

## 入口（可重跑/可測）

- 規則判斷（輸入 channel/chat_type/text → 輸出 JSON 決策）：
  - `python3 scripts/gate.py --channel telegram --chat-type group --text "..."`

## 需要細節時

- 讀 `references/spec.md`（完整規格 + 變更紀錄 + 去重/可重入策略）
- 讀 `references/red-team.md`（攻防測試）
- 跑 `tests/smoke.sh`
