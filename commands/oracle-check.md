---
description: Cross-check the Oracle store for drift (counts, sessions, timeline vs git) and print the read proof.
allowed-tools:
  - Bash
---

Run from the project root and report both VERDICT lines; for every DRIFT line, fix it (bank the missing beats, index or fill the session file) and run the check again:
- `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" check`
- `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" proof`
