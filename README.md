# Oracle Loop

A Claude Code plugin for long projects that must not forget: a compounding project memory, a reread protocol that runs after every context compaction, a lessons ledger with a pre-push sweep, and hooks that make the loop happen without being asked.

It is the system built and run on Project Insight (eight Terminal-Bench-style audio tasks, three paid at Ready-to-Deliver, several survived compactions mid-pipeline) and earlier on Project Seal and Project Parchment, generalised so a new project gets it with one install instead of copying it out of an old repo.

## The loop

```
work -> bank major beats as they happen -> context fills -> compact
     -> SessionStart(compact) hook: "reread before anything"
     -> /oracle-loop:reread-corpus: verbatim corpus, live state, whole store, skepticism sweep, carry-forward
     -> resume on the critical path, with every earlier lesson applied
```

Why it exists: compaction turns rules into a paraphrase, and paraphrase drifts (rules soften, mechanisms get invented, numbers get rounded into new numbers). The verbatim files are reloaded instead. And reading is not learning: the reread ends with a written carry-forward that maps the ledger onto the next action, which is what stops a failure from recurring.

## What is in it

| Piece | What it does |
|---|---|
| `/oracle-loop:oracle-init` | Sets a project up: `.oracle/` (five knowledge files, sessions, timeline, index, `READ_ORDER.md`) plus the lessons ledger, example log, live-state template, corpus map and the CLAUDE.md block. Never overwrites. |
| `/oracle-loop:reread-corpus` | The post-compact protocol: measure the tiers, read them file by file, restore and staleness-check the live state, run the skepticism and contradiction sweep, cross-check the store, print the read proof, write the carry-forward, then resume critical path first. |
| `/oracle-loop:bank` | Banks a major beat: a categorised entry (pattern, preference, gotcha, solution, correction) and a timeline line, preferring an annotation over a near-duplicate. |
| `/oracle-loop:resume-note` | Overwrites the live-state file (head, checks, running jobs with IDs, held changes, budgets, the user's rulings verbatim, the next decision) so a session with no memory resumes in one read. |
| `/oracle-loop:lesson` | Adds a lessons-ledger row the same day something goes wrong; a repeat becomes an executable guard; a correction is propagated to every echo. |
| `/oracle-loop:oracle-check` | Drift cross-check (counts, sessions, timeline against git) and the read proof. |
| `oracle` skill | Lets Claude recall from the store before acting and bank without being told. |
| Hooks | `SessionStart(compact)`: the reread comes first. `SessionStart(startup/resume)`: store status and the live-state files. `PreCompact`: write the live state now. Silent in any project without `.oracle/`, so it is safe to enable everywhere. |
| `scripts/oracle.py` | The instrument (standard library only): `init`, `add`, `annotate`, `query`, `beat`, `check`, `proof`, `size`. Every gate prints a VERDICT line. |

## Install

The repo is its own marketplace:

```
/plugin marketplace add brookcs3/oracle-loop
/plugin install oracle-loop@oracle-loop
```

(A private repo needs `gh auth login` or an SSH key on the machine.) For development, `claude --plugin-dir /path/to/oracle-loop`, and `claude plugin validate /path/to/oracle-loop`.

Then in a project: `/oracle-loop:oracle-init`, fill in `.oracle/READ_ORDER.md` (what the reread reads, in tiers), capture the project's rules verbatim into `docs/guide/`, and merge the CLAUDE.md block.

Requires Python 3.11 or later on the PATH as `python3`.

## The store

```
.oracle/
  knowledge/patterns.json      how this kind of work is done
  knowledge/preferences.json   the user's rulings and ways of working, verbatim
  knowledge/gotchas.json       traps and how to avoid them
  knowledge/solutions.json     what worked, with the evidence
  knowledge/corrections.json   what was wrong and what is right
  sessions/<date>_<slug>.md    beat-by-beat session logs
  timeline/project_timeline.md the running history
  index.json                   counts and sessions, kept in sync by oracle.py
  READ_ORDER.md                the reread's tiers
```

Entry fields: `id, category, priority, title, content, context, examples, learned_from, created, last_used, use_count, tags`. The format matches an existing `.oracle/` from the claudeshack oracle plugin, so an existing store keeps working (`oracle.py check` and `proof` read it as is).

## Laws the protocol encodes (each one learned the hard way)

- The reread runs first after every compact, even when the summary says to resume directly.
- A reread that cannot resume without the user re-pasting the state has failed: the live-state file is written at every milestone and before any compact, and staleness-checked against git and the PR.
- The store's cross-check compares content, not just counts: the timeline's last beat must not be older than the last commit.
- Reread tiers are measured; closed history is read on demand, not every time.
- An interpretation of why something failed is banked as a hypothesis until it is investigated; disproved entries are marked SUPERSEDED with a pointer, in the same step.
- A law broken twice becomes an executable check, not more prose.
- Every correction is propagated to every echo of the old rule.
- A delegated verdict (a subagent's, a simulator's) is triage, never a gate.

## Layout

```
.claude-plugin/plugin.json      manifest
.claude-plugin/marketplace.json the repo as its own marketplace
commands/                       the six slash commands
skills/oracle/SKILL.md          the model-invoked skill
hooks/hooks.json, oracle_hooks.py
scripts/oracle.py               the instrument
templates/                      what oracle-init copies into a project
```
