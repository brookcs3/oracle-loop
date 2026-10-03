---
description: Write or overwrite the live-state file so the next session (or the session after a compact) resumes exactly where this one is.
argument-hint: "[task or file name]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

Write the live-state file for: $ARGUMENTS (default: the current task's `docs/RESUME_<task>.md`; start from `docs/RESUME_TEMPLATE.md` if there is none).

It must let a session with no memory resume in one read. Overwrite the "where we are" part; keep the dated history below it. Include, with facts checked from the real sources (git, the PR, the job logs), not from memory:
- the goal, and every standing ruling or condition the user gave, VERBATIM;
- the phase, the repo/branch/head commit, the PR or job and each named check with its status and verdict;
- running jobs and watchers with their IDs, what each decides, and how to stop them;
- held changes (uncommitted work, side branches, patches) and what releases them;
- any budget or count ledger, read from its source;
- the next steps in order and who makes each decision.
Stamp it with the time from the shell. Then bank the beat (`oracle.py beat ...`) and say the file's path.
