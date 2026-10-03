#!/usr/bin/env python3
"""oracle.py: the project memory instrument behind the oracle-loop plugin. Standard library only.

The store lives in <project>/.oracle/:
  knowledge/{patterns,preferences,gotchas,solutions,corrections}.json   one JSON list per category
  sessions/<YYYY-MM-DD>_<slug>.md                                      what happened in a working session, beat by beat
  timeline/project_timeline.md                                         the running history, one dated paragraph per major beat
  index.json                                                           counts and the session list (kept in sync by this script)
  READ_ORDER.md                                                        the project's reread tiers (what /reread-corpus reads)

Subcommands (run from the project root, or pass --root):
  init                      create the store and copy the doc templates that are missing (never overwrites)
  add CATEGORY              add one entry: --priority --title --content [--context --example ... --tag ... --session]
  annotate ID TEXT          append a dated note to an entry's content (use "SUPERSEDED <date>: ..." for corrections)
  query [WORDS]             search titles, content and tags; --category, --priority, --limit
  beat TEXT                 append a dated paragraph to the timeline and a line to the session file (--session)
  check                     cross-check counts, sessions and drift against git; prints a VERDICT line
  proof                     print "entries read: n of N" per file, for the reread's read proof
  size                      estimate the token cost of each READ_ORDER tier
Every gate-style command ends with a VERDICT line; a failed check never falls through to a clear."""
import argparse, datetime, glob, json, os, re, shutil, subprocess, sys, uuid

CATEGORIES = ["patterns", "preferences", "gotchas", "solutions", "corrections"]
SINGULAR = {"patterns": "pattern", "preferences": "preference", "gotchas": "gotcha", "solutions": "solution", "corrections": "correction"}
PRIORITIES = ["critical", "high", "medium", "low"]
HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(os.path.dirname(HERE), "templates")


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def store(root):
    return os.path.join(root, ".oracle")


def load(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def save(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def knowledge(root):
    return {c: load(os.path.join(store(root), "knowledge", c + ".json"), []) for c in CATEGORIES}


def reindex(root):
    idx_path = os.path.join(store(root), "index.json")
    idx = load(idx_path, {})
    k = knowledge(root)
    counts = {c: len(v) for c, v in k.items()}
    sessions = sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(store(root), "sessions", "*.md")))
    idx.update({"created": idx.get("created", now()), "last_updated": now(), "total_entries": sum(counts.values()),
                "categories": counts, "sessions": sessions, "version": "oracle-loop-1"})
    save(idx_path, idx)
    return idx


def cmd_init(a):
    root = a.root
    made = []
    for sub in ("knowledge", "sessions", "timeline", "scripts"):
        os.makedirs(os.path.join(store(root), sub), exist_ok=True)
    for c in CATEGORIES:
        p = os.path.join(store(root), "knowledge", c + ".json")
        if not os.path.exists(p):
            save(p, []); made.append(os.path.relpath(p, root))
    tl = os.path.join(store(root), "timeline", "project_timeline.md")
    if not os.path.exists(tl):
        with open(tl, "w") as f:
            f.write("# Project Timeline\n\nOne dated paragraph per major beat, newest last. Append only.\n")
        made.append(os.path.relpath(tl, root))
    sources = [os.path.join(d, f) for d, _, fs in os.walk(TEMPLATES) for f in fs]   # os.walk sees dot-folders; glob ** does not
    for src in sorted(sources):
        rel = os.path.relpath(src, TEMPLATES)
        if rel.startswith(".oracle/knowledge") or rel.endswith(".gitkeep"):
            continue
        dst = os.path.join(root, rel)
        if os.path.exists(dst):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst); made.append(rel)
    idx = reindex(root)
    for m in made:
        print("created", m)
    print(f"VERDICT: INIT OK, {idx['total_entries']} entries, {len(made)} files created, nothing overwritten")


def cmd_add(a):
    cat = a.category if a.category in CATEGORIES else a.category + "s"
    if cat not in CATEGORIES:
        sys.exit(f"VERDICT: FAIL unknown category {a.category!r}; one of {CATEGORIES}")
    if a.priority not in PRIORITIES:
        sys.exit(f"VERDICT: FAIL unknown priority {a.priority!r}; one of {PRIORITIES}")
    path = os.path.join(store(a.root), "knowledge", cat + ".json")
    entries = load(path, [])
    words = set(re.findall(r"[a-z0-9]+", a.title.lower()))
    for e in entries:
        other = set(re.findall(r"[a-z0-9]+", e.get("title", "").lower()))
        if words and len(words & other) / max(len(words | other), 1) > 0.7:
            print(f"note: near-duplicate of {e['id']} '{e['title'][:70]}'; prefer `annotate` on it")
    e = {"id": str(uuid.uuid4()), "category": SINGULAR[cat], "priority": a.priority, "title": a.title, "content": a.content,
         "context": a.context or "", "examples": a.example or [], "learned_from": a.session or "", "created": now(),
         "last_used": now(), "use_count": 0, "tags": a.tag or []}
    entries.append(e)
    save(path, entries)
    idx = reindex(a.root)
    print(f"VERDICT: ADDED {e['id']} to {cat} ({len(entries)} there, {idx['total_entries']} total)")


def find(root, eid):
    for c, entries in knowledge(root).items():
        for i, e in enumerate(entries):
            if e["id"].startswith(eid):
                return c, entries, i
    return None, None, None


def cmd_annotate(a):
    c, entries, i = find(a.root, a.id)
    if c is None:
        sys.exit(f"VERDICT: FAIL no entry {a.id}")
    entries[i]["content"] += f" | {a.text}"
    entries[i]["last_used"] = now()
    if a.text.upper().startswith("SUPERSEDED") and not entries[i]["title"].startswith("SUPERSEDED"):
        entries[i]["title"] = "SUPERSEDED " + datetime.date.today().isoformat() + ": " + entries[i]["title"]
    save(os.path.join(store(a.root), "knowledge", c + ".json"), entries)
    print(f"VERDICT: ANNOTATED {entries[i]['id']} in {c}")


def cmd_query(a):
    terms = [t.lower() for t in a.words]
    hits = []
    for c, entries in knowledge(a.root).items():
        if a.category and c not in (a.category, a.category + "s"):
            continue
        for e in entries:
            if a.priority and e.get("priority") != a.priority:
                continue
            blob = " ".join([e.get("title", ""), e.get("content", ""), " ".join(e.get("tags", []))]).lower()
            if all(t in blob for t in terms):
                hits.append((PRIORITIES.index(e.get("priority", "low")) if e.get("priority") in PRIORITIES else 9, c, e))
    hits.sort(key=lambda h: (h[0], h[2].get("created", "")))
    for _, c, e in hits[: a.limit]:
        print(f"[{e.get('priority')}] {c}: {e['title']}\n  {e['content'][:a.width]}\n  id {e['id'][:8]}  {e.get('created', '')}\n")
    print(f"VERDICT: {len(hits)} match(es), {min(len(hits), a.limit)} shown")


def cmd_beat(a):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tl = os.path.join(store(a.root), "timeline", "project_timeline.md")
    with open(tl, "a") as f:
        f.write(f"\n## {stamp} - {a.text}\n" + (f"\n**Session**: `{a.session}`\n" if a.session else ""))
    if a.session:
        sp = os.path.join(store(a.root), "sessions", a.session + ".md")
        new = not os.path.exists(sp)
        with open(sp, "a") as f:
            if new:
                f.write(f"# Session: {a.session}\n")
            f.write(f"- {stamp}: {a.text}\n")
    reindex(a.root)
    print(f"VERDICT: BEAT BANKED at {stamp}" + (f" (session {a.session})" if a.session else ""))


def git_last(root):
    try:
        out = subprocess.run(["git", "-C", root, "log", "-1", "--format=%cI %h"], capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or None
    except Exception:
        return None


def cmd_check(a):
    root, problems = a.root, []
    idx = load(os.path.join(store(root), "index.json"), None)
    if idx is None:
        sys.exit("VERDICT: FAIL no .oracle/index.json (run init)")
    k = knowledge(root)
    for c, entries in k.items():
        if idx.get("categories", {}).get(c) != len(entries):
            problems.append(f"index says {idx.get('categories', {}).get(c)} {c}, disk has {len(entries)}")
        ids = [e.get("id") for e in entries]
        if len(ids) != len(set(ids)):
            problems.append(f"duplicate ids in {c}")
    on_disk = {os.path.splitext(os.path.basename(p))[0]: os.path.getsize(p) for p in glob.glob(os.path.join(store(root), "sessions", "*.md"))}
    for s in idx.get("sessions", []):
        if s not in on_disk:
            problems.append(f"index names session {s}, no file")
    for s, size in on_disk.items():
        if size == 0:
            problems.append(f"session {s} is zero bytes")
        if s not in idx.get("sessions", []):
            problems.append(f"session {s} not in index")
    tl = os.path.join(store(root), "timeline", "project_timeline.md")
    last_beat = None
    if os.path.exists(tl):
        stamps = re.findall(r"^## (\d{4}-\d{2}-\d{2})", open(tl).read(), re.M)
        last_beat = stamps[-1] if stamps else None
    g = git_last(root)
    if g and last_beat and g[:10] > last_beat:
        problems.append(f"timeline's last beat {last_beat} is older than the last commit {g}: bank the missing beats")
    for p in problems:
        print("DRIFT:", p)
    print(f"store: {sum(len(v) for v in k.values())} entries, {len(on_disk)} sessions, last beat {last_beat}, last commit {g}")
    print("VERDICT: " + ("CLEAN" if not problems else f"DRIFT ({len(problems)} problem(s))"))


def cmd_proof(a):
    total = 0
    for c, entries in knowledge(a.root).items():
        print(f"Oracle entries read: {len(entries)} of {len(entries)} ({c}.json)")
        total += len(entries)
    idx = load(os.path.join(store(a.root), "index.json"), {})
    ok = idx.get("total_entries") == total
    print(f"VERDICT: {'MATCH' if ok else 'MISMATCH'} {total} on disk, index says {idx.get('total_entries')}")


def cmd_size(a):
    ro = os.path.join(store(a.root), "READ_ORDER.md")
    if not os.path.exists(ro):
        sys.exit("VERDICT: FAIL no .oracle/READ_ORDER.md")
    tier, sizes = None, {}
    for line in open(ro):
        m = re.match(r"^##\s+(TIER\s+\w+)", line)
        if m:
            tier = m.group(1); sizes.setdefault(tier, 0); continue
        m = re.match(r"^\s*-\s+`([^`]+)`", line)
        if tier and m:
            for p in glob.glob(os.path.join(a.root, m.group(1)), recursive=True, include_hidden=True):
                if os.path.isfile(p):
                    sizes[tier] += os.path.getsize(p)
    for t, b in sizes.items():
        print(f"{t}: {b:,} bytes, about {b // 4:,} tokens")
    print(f"VERDICT: SIZED {sum(sizes.values()) // 4:,} tokens across {len(sizes)} tier(s)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=os.getcwd())
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("init")
    p = sp.add_parser("add"); p.add_argument("category")
    p.add_argument("--priority", default="medium"); p.add_argument("--title", required=True); p.add_argument("--content", required=True)
    p.add_argument("--context"); p.add_argument("--example", action="append"); p.add_argument("--tag", action="append"); p.add_argument("--session")
    p = sp.add_parser("annotate"); p.add_argument("id"); p.add_argument("text")
    p = sp.add_parser("query"); p.add_argument("words", nargs="*"); p.add_argument("--category"); p.add_argument("--priority")
    p.add_argument("--limit", type=int, default=20); p.add_argument("--width", type=int, default=400)
    p = sp.add_parser("beat"); p.add_argument("text"); p.add_argument("--session")
    sp.add_parser("check"); sp.add_parser("proof"); sp.add_parser("size")
    a = ap.parse_args()
    a.root = os.path.abspath(a.root)
    {"init": cmd_init, "add": cmd_add, "annotate": cmd_annotate, "query": cmd_query, "beat": cmd_beat,
     "check": cmd_check, "proof": cmd_proof, "size": cmd_size}[a.cmd](a)


if __name__ == "__main__":
    main()
