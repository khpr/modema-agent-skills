# Red-team review: Group Silence Gating

Goal: prevent “accidental speech” in group chats.

## Threat model / failure modes

1) **LLM sees messages it shouldn’t**
- Symptom: model replies even when it “should be silent”.
- Root cause: relying only on prompt rules.
- Mitigation: pre-filter at ingress (router/n8n/middleware) and drop non-trigger messages.

2) **Trigger spoofing / ambiguity**
- Symptom: someone types “@小蝦” as plain text but not an actual mention; or includes it in a quote.
- Mitigation: prefer platform-native mention entities when available; otherwise accept text trigger but be explicit about the tradeoff.

3) **Over-triggering by partial matches**
- Symptom: item name contains the trigger string, or message contains “/小蝦” in code/log.
- Mitigation: regex anchor rules:
  - `/小蝦` should be at start-of-message or token boundary.
  - `@小蝦` should match a mention entity or token boundary.

4) **Under-triggering (missed mentions)**
- Symptom: user mentions via UI but display name differs (“小蝦 ” variants).
- Mitigation: match by userId/username where platform supports it; keep a configurable list of aliases.

5) **Footer leaks into contexts that shouldn’t have it**
- Symptom: footer added in DM/private chats.
- Mitigation: apply footer only in group-chat replies.

6) **Multi-message replies (breaks the ‘one message’ rule)**
- Symptom: assistant splits into multiple messages.
- Mitigation: enforce a single output message; if length is too long, compress to one sentence.

7) **Channel confusion**
- Symptom: LINE group receives replies.
- Mitigation: hard block LINE group replies in router before model; add regression test “LINE group => no output”.

## Abuse cases to test

- Normal group chatter: no reply.
- Message contains “/小蝦” in the middle of a sentence: should it trigger? (decide; recommended: no, unless token boundary)
- Quoted message contains “@小蝦” but user didn’t mention: should not trigger if mention-entity is required.
- Triggered message asking multiple questions: still reply only one sentence (pick the main ask).
