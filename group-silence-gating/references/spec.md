# group-silence-gating — Spec

## 目的
在群組聊天中提供「預設靜默」的 deterministic 閘門：
- 沒有硬觸發 → 一律不回覆
- 有硬觸發 → 才允許回覆（且回覆受限）

## 觸發條件（Hard Triggers）
- 文字包含 `/小蝦` 或 `@小蝦`
- 禁止語意推測

## Channel 規則
- LINE 群組：永遠靜默（即使觸發也不回）
- Telegram 群組：只有觸發才回

## 回覆約束（Triggered Reply Constraints）
- 只回觸發的那一則訊息
- 一句詳細回答（不要追問，不要延伸）
- 固定尾註兩行：
  ---
  🦐 要找我請 @小蝦 或 /小蝦 🦐

## 可靠性建議（非常重要）

### A) 最佳做法：LLM 前置 gating
把 gating 放在「進 LLM 之前」：router/provider middleware/hook。
好處：
- 最省 token
- 最不會失手（因為 LLM 根本沒看到不該回的訊息）

### B) 去重（dedupe）/ 可重入（idempotency）
群組訊息可能因為：重啟、平台 retry、網路抖動，而被重送。
因此任何「允許回覆」的路徑，建議做去重：
- key：message_id（或 message_sid）
- TTL：例如 60–300 秒
- 策略：TTL 內同 key 只允許回覆一次

> `scripts/gate.py` 只做 deterministic 判斷、不落地狀態；去重應在上游做。

## Changelog
- 2026-03-23：
  - 封包升級：新增 scripts/ references/ tests/ state/
  - 尾註統一為：🦐 要找我請 @小蝦 或 /小蝦 🦐
