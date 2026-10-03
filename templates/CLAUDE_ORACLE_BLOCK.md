## HARD RULE: RE-READ THE CORPUS ON EVERY COMPACT
After ANY context compaction (automatic or manual), BEFORE resuming work, run `/oracle-loop:reread-corpus` in the main session, file by file with the Read tool. Do it automatically. Compaction paraphrases rules and paraphrase drifts; the verbatim corpus is authoritative.

## HARD RULE: THE LESSONS LEDGER + PRE-PUSH SWEEP
`docs/LESSONS_LEARNED.md` records every failure with the law that now prevents it. Its PRE-PUSH SWEEP runs before every push or delivery. When something new goes wrong, add a row the same day (`/oracle-loop:lesson`).

## STANDING RULE: bank the major beats to the Oracle store as they happen
Major beats only (deliverables, builds, verdicts, the user's rulings verbatim, corrections, durable learnings), in the same turn, via `/oracle-loop:bank`. Live state in `docs/RESUME_<task>.md`, overwritten at every milestone and before any compact (`/oracle-loop:resume-note`). Worked commands go into `docs/EXAMPLE_LOG.md`.
