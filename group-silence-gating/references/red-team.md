# Red-team checklist — group-silence-gating

目標：確保「不該回的時候絕對不回」。

## 必過案例

### 1) 沒觸發
- 任意群組訊息（無 `/小蝦`、無 `@小蝦`）→ 必須 mute

### 2) 假觸發（相似字）
- `/小`、`小蝦`、`@小` → 不能當觸發（必須完整包含 `/小蝦` 或 `@小蝦`）

### 3) LINE 群組永遠靜默
- LINE + group + text 含 `/小蝦` → 仍然 mute

### 4) Telegram 群組觸發可回
- Telegram + group + text 含 `/小蝦` → reply，且必須帶 footer

### 5) 重送去重（上游）
- 同一 message_id 重送 N 次 → 上游 TTL 去重後只能回一次

## 常見失誤
- LLM 看到沒有觸發的訊息仍然回（未做前置 gating）
- 觸發後回覆太多句、或加追問
- 尾註忘記加 / 格式不一致
