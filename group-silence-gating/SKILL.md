---
name: group-silence-gating
description: Enforce strict group-chat silence by default and only respond when explicitly triggered (e.g., Telegram/LINE group ops). Use when you must avoid accidental bot replies in busy group chats and need deterministic “speak only on /trigger or @mention” behavior, with one-message/one-sentence replies and a fixed footer reminder.
---

# Group Silence Gating

Implement a **"default mute"** policy in group chats: drop everything unless a **hard trigger** is present.

## Policy (deterministic)

1) **Default = mute**
- If the message is not explicitly triggered → **do not respond** (ideally: do not even forward to the LLM).

2) **Hard triggers only**
- Trigger if (any):
  - Text contains `/小蝦` (command)
  - Text contains `@小蝦` (mention)
- No semantic guessing.

3) **Reply constraint (when triggered)**
- Reply to **only the triggering message**.
- Produce **one detailed sentence** (no follow-up questions; no extra context).
- End with a fixed footer line:
  - `---`
  - `⚠️ 下次要我回覆請 @小蝦 或 /小蝦 ⚠️`

4) **Channel rule**
- **LINE: always mute** (never reply in groups).
- **Telegram: allow replies only via triggers** above.

## Implementation notes (recommended)

- Best reliability: enforce gating **before** calling the model (router/n8n/provider middleware).
- If you can’t pre-filter: still apply this policy in the agent, but treat it as weaker than pre-filtering.

## Red-team & QA

- Read and follow:
  - `references/red-team.md`
  - `references/skill-checklist.md`
