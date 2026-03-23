#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PY_SCRIPT="$ROOT_DIR/scripts/gate.py"
FIXTURES="$ROOT_DIR/tests/fixtures.json"

ROOT_DIR="$ROOT_DIR" PY_SCRIPT="$PY_SCRIPT" FIXTURES="$FIXTURES" python3 - <<'PY'
import json, os, subprocess, sys

py = os.environ['PY_SCRIPT']
fix = os.environ['FIXTURES']

cases = json.loads(open(fix, 'r', encoding='utf-8').read())

ok = 0
for c in cases:
    out = subprocess.check_output([
        'python3', py,
        '--channel', c['channel'],
        '--chat-type', c['chat_type'],
        '--text', c['text'],
    ], text=True)
    j = json.loads(out)
    if j.get('action') != c['expect_action']:
        print('FAIL', c['name'], 'expected', c['expect_action'], 'got', j.get('action'))
        sys.exit(1)
    ok += 1

print('OK', ok)
PY
