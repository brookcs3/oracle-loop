---
name: oracle
description: Use in any project with a .oracle/ directory. Recall what the project already learned before acting (query the store), bank major beats as they happen, keep the live-state file current, and follow the reread protocol after a compaction. Use when starting work, before a risky step, when the user corrects you or gives a ruling, and when something goes wrong.
---

# The Oracle Loop

The project memory is `.oracle/`: five knowledge files (patterns, preferences, gotchas, solutions, corrections), session logs, a running timeline, an index, and `READ_ORDER.md` (what the reread reads). Around it sit a verbatim corpus of the project's rules (`docs/guide/`, mapped by `docs/00_nav_structure.md`), a lessons ledger with a pre-push sweep (`docs/LESSONS_LEARNED.md`), a worked-command cookbook (`docs/EXAMPLE_LOG.md`) and a live-state file per piece of work (`docs/RESUME_<task>.md`).

THE LOOP: context fills -> compact -> `/oracle-loop:reread-corpus` -> resume with working knowledge. The store grows each session, so the workflow learns as it goes. Documentation only pays if something forces it back into context; the reread is that force.

## When to recall
- Before starting a task or a risky step: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" query <key words>` and `--priority critical`. Apply what comes back; say which entry you are applying.
- A rule question: the verbatim corpus (`docs/guide/`) outranks any paraphrase, including the store and this skill. Grep it and cite `file:line`; a page not yet captured is said to be pending, never guessed.

## When to bank (same turn, major beats only)
A deliverable, a build, a submission, a verdict; a ruling or new information from the user (quote it verbatim); a correction; a key decision; a durable learning. Use `/oracle-loop:bank`. Prefer annotating a near-duplicate over adding one. A "why it failed" reading is a hypothesis until investigated; a disproved entry gets "SUPERSEDED <date>" and a pointer in the same step. Timestamps come from the shell.

## Live state
Overwrite `docs/RESUME_<task>.md` at every milestone and before any compact (`/oracle-loop:resume-note`): head, checks and verdicts, running jobs with IDs, held changes, budgets read from their source, the user's standing rulings verbatim, the next decision and whose it is. A reread that cannot resume without the user re-pasting where things were is a failure of this file.

## When something goes wrong
Same day, `/oracle-loop:lesson`: a ledger row with cost, root cause, how it was caught, and the law now. A law broken twice becomes an executable guard, not more prose. Every correction is propagated to every echo of the old rule.

## Standing habits this loop was built on
- Verify with the real instruments before stating a result; never fabricate a test result, a run outcome or a review verdict.
- A delegated verdict (a subagent's, a simulator's) is triage, never a gate; the real pipeline or instrument decides.
- Work, scratch and backups go in the project's work/ folder, never /tmp.
- Every bound, figure and claim written into a deliverable traces to a saved measurement from the current code.
