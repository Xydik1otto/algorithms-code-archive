#!/usr/bin/env python3
"""Collect top GitHub repos implementing algorithms, grouped by algorithm task/domain.
Uses `gh api search/repositories` (official free GitHub API). Writes data/repos.json.
"""
import json, subprocess, time, os

CATEGORIES = {
    "sorting-searching": [
        ("sorting+algorithm", "Sorting"), ("sorting+visualization", "Sorting"),
        ("topic:sorting-algorithms", "Sorting"), ("binary+search+tree+library", "Searching"),
        ("binary+search+algorithm", "Searching"),
    ],
    "data-structures": [
        ("data+structures+library", "Data structures"), ("topic:data-structures", "Data structures"),
        ("persistent+data+structure", "Persistent"), ("bloom+filter", "Probabilistic"),
        ("linked+list+tree+graph+library", "Data structures"),
    ],
    "graphs-networks": [
        ("graph+algorithms+library", "Graphs"), ("topic:graph-algorithms", "Graphs"),
        ("pathfinding+algorithm", "Pathfinding"), ("shortest+path+algorithm", "Pathfinding"),
        ("minimum+spanning+tree", "Graphs"), ("maximum+flow+algorithm", "Graphs"),
        ("topic:graph-theory", "Graph theory"),
    ],
    "strings-text": [
        ("string+matching+algorithm", "String matching"), ("suffix+automaton+suffix+tree", "Suffix"),
        ("levenshtein+distance+library", "Edit distance"), ("regex+engine+implementation", "Regex"),
        ("aho+corasick", "String matching"), ("topic:string-algorithms", "Strings"),
    ],
    "compression": [
        ("compression+algorithm+implementation", "Compression"), ("topic:compression", "Compression"),
        ("lossless+compression+library", "Compression"), ("huffman+coding", "Compression"),
        ("arithmetic+coding", "Compression"),
    ],
    "hashing-crypto": [
        ("cryptographic+library", "Crypto"), ("hash+function+implementation", "Hashing"),
        ("password+hashing+library", "Hashing"), ("topic:cryptography", "Crypto"),
        ("encryption+algorithm+implementation", "Crypto"),
    ],
    "math-numerics": [
        ("numerical+library", "Numerics"), ("linear+algebra+library", "Linear algebra"),
        ("arbitrary+precision+arithmetic", "Big numbers"), ("prime+numbers+algorithm", "Number theory"),
        ("topic:numerical-analysis", "Numerics"), ("matrix+library", "Linear algebra"),
    ],
    "geometry": [
        ("computational+geometry+library", "Geometry"), ("topic:computational-geometry", "Geometry"),
        ("convex+hull+algorithm", "Geometry"), ("delaunay+triangulation", "Geometry"),
        ("polygon+clipping", "Geometry"),
    ],
    "machine-learning-classic": [
        ("machine+learning+from+scratch", "ML from scratch"), ("topic:ml-from-scratch", "ML from scratch"),
        ("neural+network+from+scratch", "NN from scratch"), ("decision+tree+algorithm+implementation", "ML"),
        ("clustering+algorithm+implementation", "Clustering"), ("gradient+boosting+library", "Ensembles"),
        ("reinforcement+learning+algorithm+implementation", "RL"),
    ],
    "optimization-metaheuristics": [
        ("genetic+algorithm+library", "Evolutionary"), ("simulated+annealing+algorithm", "Metaheuristics"),
        ("traveling+salesman+problem+solver", "Combinatorial"), ("topic:metaheuristics", "Metaheuristics"),
        ("constraint+solver", "CSP"), ("linear+programming+solver", "OR"),
        ("evolutionary+computation+framework", "Evolutionary"),
    ],
    "image-vision": [
        ("image+processing+library", "Image processing"), ("topic:image-processing", "Image processing"),
        ("edge+detection+algorithm", "Vision"), ("feature+detection+computer+vision", "Vision"),
        ("computer+vision+from+scratch", "Vision"),
    ],
    "audio-dsp": [
        ("dsp+library", "DSP"), ("fft+library", "DSP"), ("topic:dsp", "DSP"),
        ("audio+signal+processing+library", "Audio"),
    ],
    "distributed-consensus": [
        ("raft+consensus+implementation", "Consensus"), ("paxos+implementation", "Consensus"),
        ("topic:consensus", "Consensus"), ("distributed+hash+table", "DHT"),
        ("blockchain+implementation+from+scratch", "Blockchain"),
    ],
    "nlp-text-mining": [
        ("natural+language+processing+library", "NLP"), ("topic:natural-language-processing", "NLP"),
        ("text+mining+library", "Text mining"), ("stemming+lemmatization+library", "NLP"),
    ],
    "bioinformatics": [
        ("bioinformatics+library", "Bioinformatics"), ("sequence+alignment+algorithm", "Bioinformatics"),
        ("topic:bioinformatics", "Bioinformatics"),
    ],
    "game-ai": [
        ("minimax+alpha+beta+algorithm", "Game AI"), ("monte+carlo+tree+search", "MCTS"),
        ("game+ai+library", "Game AI"), ("behavior+tree+library", "Game AI"),
        ("topic:game-ai", "Game AI"),
    ],
    "simulation-physics": [
        ("physics+engine", "Physics"), ("cellular+automata+implementation", "Cellular automata"),
        ("agent+based+modeling+framework", "ABM"), ("topic:particle-system", "Simulation"),
    ],
    "collections": [
        ("algorithms+python", "Multi"), ("algorithms+javascript", "Multi"),
        ("algorithms+java", "Multi"), ("algorithms+rust", "Multi"),
        ("algorithms+golang", "Multi"), ("algorithms+c%2B%2B", "Multi"),
        ("algorithms+c%23", "Multi"), ("algorithms+swift", "Multi"),
        ("algorithms+kotlin", "Multi"), ("data+structures+algorithms+collection", "Multi"),
        ("awesome+algorithms", "Meta"), ("algorithm+visualizer", "Meta"),
    ],
}

def gh_search(query, per_page=10):
    out = subprocess.run(
        ["gh", "api", f"search/repositories?q={query}&sort=stars&order=desc&per_page={per_page}"],
        capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        print(f"  !! failed: {query}: {out.stderr.strip()[:150]}", flush=True)
        return []
    try:
        items = json.loads(out.stdout).get("items", [])
    except json.JSONDecodeError:
        print(f"  !! bad json: {query}", flush=True)
        return []
    res = []
    for it in items:
        res.append({
            "full_name": it["full_name"], "url": it["html_url"],
            "desc": (it.get("description") or "")[:220],
            "stars": it["stargazers_count"], "lang": it.get("language"),
            "topics": (it.get("topics") or [])[:6],
            "pushed": (it.get("pushed_at") or "")[:10],
            "archived": it.get("archived", False),
        })
    return res

def main():
    data = {}
    seen = {}
    total = 0
    for cat, queries in CATEGORIES.items():
        data[cat] = []
        print(f"== {cat}", flush=True)
        for q, task in queries:
            repos = gh_search(q)
            time.sleep(7)  # search API: 10 req/min
            for r in repos:
                if r["archived"] or r["stars"] < 40:
                    continue
                if r["full_name"] in seen:
                    continue
                seen[r["full_name"]] = cat
                r["task"] = task
                data[cat].append(r)
                total += 1
        data[cat].sort(key=lambda r: -r["stars"])
        data[cat] = data[cat][:30]
        print(f"  -> {len(data[cat])} kept", flush=True)
    os.makedirs("data", exist_ok=True)
    with open("data/repos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"TOTAL unique repos: {total}; saved to data/repos.json")

if __name__ == "__main__":
    main()
