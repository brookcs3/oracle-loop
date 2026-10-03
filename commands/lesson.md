---
description: Add a row to the lessons ledger the same day something goes wrong, and turn a repeat failure into a guard.
argument-hint: "<what went wrong>"
allowed-tools:
  - Bash
  - Read
  - Edit
---

Add a row to `docs/LESSONS_LEARNED.md` for: $ARGUMENTS

1. Number it after the highest existing row (L<n>). Fields: **What happened**, **Cost**, **Root cause**, **How it was caught**, **Law now**, **Where recorded**. Facts only; quote the evidence.
2. Search the ledger and the store for the same law. If it already exists, this is a RECURRENCE: write it as "L<k> RECURRENCE (<date>)", add it to the reread watchlist, and propose an executable guard (a script check, a checklist line, a hook) instead of more prose.
3. If the law is a check to run before shipping, add it to the PRE-PUSH SWEEP at the bottom of the ledger as the next numbered item.
4. If it corrects an earlier rule, grep the old wording across CLAUDE.md, the example log, `.oracle/knowledge/*.json`, the session files and the ledger, and update or mark SUPERSEDED every echo in the same step.
5. Bank it: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" add gotcha|correction ...` with the row number in the content.
