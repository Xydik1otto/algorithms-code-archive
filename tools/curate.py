#!/usr/bin/env python3
"""Curation pass over data/repos.json: remove off-topic repos, fix misplacements.
REMOVE/MOVE lists are maintained by the maintainer after each collection run.
"""
import json

REMOVE = set()

MOVE = {}  # full_name -> (from_cat, to_cat)

def main():
    with open("data/repos.json", encoding="utf-8") as f:
        data = json.load(f)
    removed, moved = [], []
    for cat in list(data):
        kept = []
        for r in data[cat]:
            fn = r["full_name"]
            if fn in REMOVE:
                removed.append(fn)
                continue
            if fn in MOVE and MOVE[fn][0] == cat:
                moved.append((fn, cat, MOVE[fn][1]))
                data[MOVE[fn][1]].append(r)
                continue
            kept.append(r)
        data[cat] = kept
    for cat in data:
        seen, uniq = set(), []
        for r in data[cat]:
            if r["full_name"] in seen:
                continue
            seen.add(r["full_name"])
            uniq.append(r)
        uniq.sort(key=lambda r: -r["stars"])
        data[cat] = uniq[:30]
    with open("data/repos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"removed {len(removed)}: {removed}")
    print(f"moved {len(moved)}: {[m[0] for m in moved]}")
    print(f"totals: { {k: len(v) for k, v in data.items()} }, sum={sum(len(v) for v in data.values())}")

if __name__ == "__main__":
    main()
