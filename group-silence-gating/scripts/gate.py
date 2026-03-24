#!/usr/bin/env python3
"""Group Silence Gating — deterministic gate.

Input: channel/chat_type/text
Output: JSON decision (mute/reply) + constraints.

Notes:
- This script is intentionally deterministic and side-effect free.
- Dedup / TTL should be implemented at the router/provider layer; see references/spec.md.
"""

import argparse
import json
import re
import sys

FOOTER = "---\n🦐 找我請 @小蝦"


def contains_trigger(text: str) -> bool:
    return ("/小蝦" in text) or ("@小蝦" in text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", required=True, help="line|telegram|...")
    ap.add_argument("--chat-type", required=True, help="direct|group")
    ap.add_argument("--text", required=True)
    args = ap.parse_args()

    channel = args.channel.strip().lower()
    chat_type = args.chat_type.strip().lower()
    text = args.text

    decision = {
        "channel": channel,
        "chat_type": chat_type,
        "triggered": contains_trigger(text),
        "action": "mute",
        "reason": "default_mute",
        "reply_constraints": None,
    }

    # Channel rule: LINE groups are always mute.
    if channel == "line" and chat_type == "group":
        decision["action"] = "mute"
        decision["reason"] = "line_group_always_mute"
    elif decision["triggered"]:
        decision["action"] = "reply"
        decision["reason"] = "hard_trigger"
        decision["reply_constraints"] = {
            "one_sentence": True,
            "no_followup_questions": True,
            "reply_to_triggering_message_only": True,
            "footer": FOOTER,
        }

    sys.stdout.write(json.dumps(decision, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
