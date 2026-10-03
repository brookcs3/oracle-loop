#!/usr/bin/env python3
"""Hook entry points for oracle-loop. Whatever this prints on stdout is added to Claude's context.

after-compact   SessionStart(compact): the reread comes first, before any tool call on the task; names the live-state files.
session-start   SessionStart(startup|resume): one line of store status and the live-state files, so a fresh session resumes.
pre-compact     PreCompact: reminds the session to have written the live state before the context is summarised.
A project without .oracle/ gets nothing (the hooks stay silent), so the plugin is safe to enable globally."""
import glob, json, os, sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
ORACLE = os.path.join(ROOT, ".oracle")


def live_files():
    pats = ["docs/RESUME*.md", "RESUME*.md", ".oracle/LIVE*.md"]
    found = []
    for p in pats:
        found += glob.glob(os.path.join(ROOT, p))
    found = [f for f in found if "TEMPLATE" not in os.path.basename(f).upper()]
    found.sort(key=os.path.getmtime, reverse=True)
    return [os.path.relpath(f, ROOT) for f in found[:5]]


def counts():
    try:
        idx = json.load(open(os.path.join(ORACLE, "index.json")))
        return f"{idx.get('total_entries', '?')} entries, {len(idx.get('sessions', []))} sessions"
    except Exception:
        return "index unreadable (run the oracle check)"


def main():
    if not os.path.isdir(ORACLE):
        return
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    live = live_files()
    live_txt = ", ".join(live) if live else "none found (write docs/RESUME_<task>.md)"
    if mode == "after-compact":
        print("ORACLE LOOP: the context was just compacted. Before ANY tool call on the task, run /oracle-loop:reread-corpus "
              "(the reread protocol): read the tiers in .oracle/READ_ORDER.md file by file with the Read tool, restore the live "
              f"state from: {live_txt}, run the skepticism sweep, then write the carry-forward in chat. The summary above is a "
              "paraphrase; the files are authoritative. Do this even if the summary says to resume directly.")
    elif mode == "session-start":
        print(f"ORACLE LOOP: project memory at .oracle/ ({counts()}). Live state: {live_txt}. Read the newest live-state file "
              "before working on the task; bank major beats as they happen (/oracle-loop:bank).")
    elif mode == "pre-compact":
        print("ORACLE LOOP: compaction is about to run. If the live-state file is not current (head, checks, running jobs, "
              "held changes, budget, Cameron's standing rulings verbatim, the next decision), it should have been written "
              "before this point; after the compact, /oracle-loop:reread-corpus restores from it.")


if __name__ == "__main__":
    main()
