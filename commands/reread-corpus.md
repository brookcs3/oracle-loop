---
description: The post-compact reread protocol. Reload the corpus, restore the live state, read with skepticism, then write a carry-forward before touching the task.
argument-hint: "[optional: tier to read, e.g. A]"
---

You are running the standing POST-COMPACT protocol of the Oracle Loop. Run it exactly, in the MAIN SESSION (never subagents or workflows, because reading through a delegate brings back a summary, which is the thing this protocol exists to replace), then get straight back to the goal.

## Why this exists
The corpus is the constitution, the Oracle store is the case law, the example log is the cookbook, the live-state file is where things stand right now. Compaction turns all of it into a paraphrase, and paraphrase drifts: rules get softened, mechanisms get invented, numbers get rounded into new numbers. Verbatim beats summary every time a rule question comes up. This command reloads the real files so the session resumes with working knowledge and no drift, and the store grows each session, so the workflow learns as it goes.

READING IS NOT LEARNING. A reread that reads everything and still cannot resume has failed. The protocol therefore has three parts: it restores the LIVE STATE, it reads with SKEPTICISM, and it writes a CARRY-FORWARD that maps the ledger and the store onto the next action before any tool call on the task.

THIS RUNS FIRST, EVERY TIME. After any compaction the reread comes before any tool call on the task, even when the compaction summary says "resume directly" or "do not recap". The oracle-loop SessionStart hook reminds you of this; the reminder is not optional.

## 0. Setup
- If `.oracle/` does not exist, say so and offer `/oracle-loop:oracle-init`; stop here.
- Confirm the model in the environment header and say if it differs from what the user set for this project (CLAUDE.md says).
- Measure before reading: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" size` prints each tier's token estimate from `.oracle/READ_ORDER.md`. Report it in the carry-forward. A single big file is fine; read it in consecutive chunks to the end, never just the tail.

## 1. The reread (Read tool, file by file; never cat or dump these through the shell)
Read every file `.oracle/READ_ORDER.md` lists for this reread, in its order:
- TIER A every time: the project's instruction files (CLAUDE.md), the verbatim corpus (rules the project works under), the live-state file(s), the playbook for the current phase, the WHOLE Oracle store (every `.oracle/knowledge/*.json` in full: patterns and solutions included, superseded entries too, because they show what not to do), the memory files, `.oracle/index.json`, the timeline and the newest session file, and any record of passed work the project copies from.
- TIER B on demand, named in the carry-forward when pulled: the lessons ledger in full before any push/ship step or when a law is questioned (otherwise its pre-push sweep plus the rows the carry-forward cites), the example log, digests and indexes.
- TIER C never on a routine reread: closed history, raw transcripts and books (read their index, grep on demand).
Reading a memory index line is not reading the memory file. Every file a tier names that does not exist is reported as missing, not chased.

## 2. The live state
Read the live-state file(s) (`docs/RESUME_<task>.md` or what READ_ORDER names). It holds: the phase; the head commit and any PR or job; each named check with its status and verdict; verdicts landed since the last change; running jobs and watchers with their IDs and what each decides; held changes and what releases them; any budget ledger; every standing ruling the user gave, verbatim; the next decision and whose it is.
Staleness check, run from the main session: compare the file's head and date with `git log -1 --format='%h %cI'` and, where there is one, the PR's checks and latest comment. Older than any of them, or missing, is DRIFT: rebuild it from those sources before the carry-forward.

## 3. The skepticism sweep (during the read)
- Be skeptical of new entries in the store, the ledger and memory: check timestamps (anything dated ahead of the real date, or stamped in a session that reads confused, is suspect) and verify suspicious claims with the real instruments before letting them affect a decision.
- CONTRADICTION SWEEP: list every critical or high entry that a later ledger row or dated correction contradicts but which is not marked SUPERSEDED; annotate it in the same step (`oracle.py annotate <id> "SUPERSEDED <date>: ... see <row>"`).
- Treat every "why it failed" reading in the store as a hypothesis unless an investigation result is cited.
- Store cross-check: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" check` (counts against index, sessions indexed and non-empty, the timeline's last beat no older than the last commit). Any DRIFT line means bank the missing beats before the carry-forward.
- Read proof: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/oracle.py" proof`, and say how many ledger rows and sweep items were read.

## 4. The carry-forward (write it in chat before any tool call on the task; keep it short)
1. **Live state, restated** from the checked file: phase, head, every named check, the last verdict, running jobs, held changes, budget, the user's standing conditions verbatim, the next decision and whose it is. The user should be able to correct it in one line.
2. **Phase** of each live piece of work.
3. **Governing laws for the next action**: every ledger row, sweep item and critical store entry that applies, each with the concrete action it implies on THIS work. Name a row only when you have written its action.
4. **Recurring-law watchlist**: the laws broken more than once, with the check that now guards each, plus any broken since the last reread.
5. **Open corrections and questions**: contradiction-sweep hits, unconfirmed (PLAUSIBLE) rows, rulings awaited from the user.
6. **Drift found and fixed**: live state, store cross-check, read proof, stale figures in the instruction files.
7. **Status and scoreboard** as the project keeps it.

## 5. Then resume the goal, critical path first
Go first to whatever pending result decides the next step or the next user decision. Report side work in one line. Do not idle and do not ask whether to continue: read, carry forward, work. Bank each major beat in the same turn it happens (`/oracle-loop:bank`), overwrite the live-state file at every milestone and before any compact (`/oracle-loop:resume-note`), and when a question to the user blocks one branch, start the read-only groundwork most branches need.

WHEN SOMETHING GOES WRONG AFTER THE REREAD: add a row to the lessons ledger the same day (`/oracle-loop:lesson`: what happened, cost, root cause, how it was caught, the law now, where recorded). A pre-ship check goes into the PRE-PUSH SWEEP. A correction to an earlier rule is propagated to every echo (grep the old wording across the instruction files, this protocol's project notes, the example log, the store, the session files and the ledger; update or mark SUPERSEDED in the same step). A law broken twice becomes an executable guard (a script check, a checklist line, a hook) rather than more prose. A worked command that produced a result goes into the example log. That is how a failure stops recurring.
