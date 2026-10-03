---
description: Bank a major beat to the Oracle store as it happens (a knowledge entry and/or a timeline line), with the right category and priority.
argument-hint: "<what happened>"
allowed-tools:
  - Bash
  - Read
---

Bank this beat: $ARGUMENTS

Rules (the Oracle Loop's standing banking rule):
- Bank MAJOR beats only, in the same turn they happen: real pipeline work (a deliverable written, a build, a submission, a verdict), new information or a ruling from the user, a correction, a key decision, a durable learning (a law, a tool gotcha, a reviewer pattern). Skip routine Q&A.
- Pick the category: `pattern` (how this kind of work is done), `preference` (the user's rulings and ways of working, quoted verbatim where possible), `gotcha` (a trap and how to avoid it), `solution` (what worked, with the evidence), `correction` (what was wrong and what is right). Priority: critical, high, medium, low.
- Before adding, query for a near-duplicate (`oracle.py query <key words>`); prefer `oracle.py annotate <id> "<dated addition>"` over a new entry. A disproved earlier reading is annotated "SUPERSEDED <date>: ... see <new entry>" in the same step.
- A "why it failed" reading is banked as a HYPOTHESIS until an investigation confirms it.
- Every timestamp comes from the shell (`date`), never typed from memory.

Commands (from the project root):
- `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" add <category> --priority <p> --title "<title>" --content "<what, why, evidence>" --context "<when it applies>" --tag <tag> --session <YYYY-MM-DD>_<slug>`
- `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" beat "<one dated paragraph for the timeline>" --session <YYYY-MM-DD>_<slug>`
- A worked command that produced a result also goes into `docs/EXAMPLE_LOG.md`.
Report the VERDICT lines.
