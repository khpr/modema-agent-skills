# Skill checklist: Group Silence Gating

Use this to verify the skill is “shippable”.

## Trigger quality
- [ ] Description includes clear “when to use” and trigger phrases.
- [ ] Trigger phrases are explicit: `/小蝦`, `@小蝦`.
- [ ] No semantic/LLM-only triggers.

## Behavior correctness
- [ ] Default = mute.
- [ ] Triggered = respond to only the triggering message.
- [ ] Output is one detailed sentence.
- [ ] Footer included (group replies only):
  - [ ] `---`
  - [ ] `⚠️ 下次要我回覆請 @小蝦 或 /小蝦 ⚠️`
- [ ] LINE group messages never cause replies.

## Safety / privacy
- [ ] No tool/exec logs or hidden reasoning persisted into memory.
- [ ] No leakage of private context into group replies.

## Robustness
- [ ] Mention matching strategy documented (entity vs plain text) with tradeoffs.
- [ ] Token-boundary or anchored matching considered to avoid false positives.

## Packaging
- [ ] SKILL.md frontmatter contains only `name` and `description`.
- [ ] No unnecessary extra docs (README/CHANGELOG/etc.).
- [ ] No symlinks.
- [ ] `package_skill.py` validation passes.
