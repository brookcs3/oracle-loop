# READ_ORDER: what /oracle-loop:reread-corpus reads in this project

List files as backticked globs under a TIER heading; `oracle.py size` measures each tier. Keep TIER A to what the next action needs. Edit this for the project.

## TIER A (every reread)
- `CLAUDE.md`
- `docs/00_nav_structure.md`
- `docs/guide/*.md`
- `docs/RESUME_*.md`
- `.oracle/knowledge/*.json`
- `.oracle/index.json`
- `.oracle/timeline/project_timeline.md`
- `.oracle/sessions/*.md`

## TIER B (on demand; LESSONS in full before any ship/push step)
- `docs/LESSONS_LEARNED.md`
- `docs/EXAMPLE_LOG.md`

## TIER C (never on a routine reread; read the index, grep on demand)
- `docs/reference/**/*`
