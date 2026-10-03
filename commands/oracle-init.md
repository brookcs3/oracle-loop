---
description: Set up the Oracle Loop in this project (.oracle/ store, READ_ORDER tiers, lessons ledger, live-state and example-log templates). Never overwrites.
allowed-tools:
  - Bash
  - Read
  - Edit
---

Set this project up for the Oracle Loop.

1. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" init` from the project root and show its output. It creates `.oracle/` (knowledge/, sessions/, timeline/, index.json, READ_ORDER.md) and copies the templates that are missing: `docs/LESSONS_LEARNED.md`, `docs/EXAMPLE_LOG.md`, `docs/RESUME_TEMPLATE.md`, `docs/00_nav_structure.md`, `docs/guide/README.md`, `CLAUDE_ORACLE_BLOCK.md`. Nothing that exists is overwritten.
2. Open `.oracle/READ_ORDER.md` and fill in its tiers for THIS project with the user: which files are the verbatim rules (the corpus, captured word for word from wherever the work's rules live, numbered in the source's own order in docs/guide/), which file holds the live state, which records of passed work get copied, what is history. Keep TIER A to what the next action needs; measure with `oracle.py size`.
3. Merge `CLAUDE_ORACLE_BLOCK.md` into the project's CLAUDE.md (show the user the text first), then delete the block file. It carries the three hard rules: reread after every compact, the lessons ledger with its pre-push sweep, and banking major beats as they happen.
4. Bank the first beat: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" beat "Oracle Loop set up" --session <YYYY-MM-DD>_<slug>`.
5. Run `oracle.py check` and report its VERDICT.
