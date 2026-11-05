#!/usr/bin/env python3
"""Generate README.md from data/repos.json (algorithm implementations indexed by task)."""
import json, datetime, html, os

CAT_TITLES = {
    "collections": ("All-in-One Algorithm Collections", "Загальні збірки алгоритмів"),
    "data-structures": ("Data Structures", "Структури даних"),
    "sorting-searching": ("Sorting & Searching", "Сортування та пошук"),
    "graphs-networks": ("Graphs & Networks", "Графи та мережі"),
    "strings-text": ("Strings & Text Algorithms", "Рядкові алгоритми"),
    "compression": ("Compression", "Стиснення даних"),
    "hashing-crypto": ("Hashing & Cryptography", "Хешування та криптографія"),
    "math-numerics": ("Math & Numerics", "Математика та чисельні методи"),
    "geometry": ("Computational Geometry", "Обчислювальна геометрія"),
    "machine-learning-classic": ("Machine Learning (Classic)", "Класичне машинне навчання"),
    "optimization-metaheuristics": ("Optimization & Metaheuristics", "Оптимізація та метаевристики"),
    "image-vision": ("Image Processing & Vision", "Обробка зображень"),
    "audio-dsp": ("Audio & DSP", "Аудіо та цифрова обробка сигналів"),
    "distributed-consensus": ("Distributed Systems & Consensus", "Розподілені системи та консенсус"),
    "nlp-text-mining": ("NLP & Text Mining", "Обробка природної мови"),
    "bioinformatics": ("Bioinformatics", "Біоінформатика"),
    "game-ai": ("Game AI (Minimax, MCTS, BT)", "Ігровий ШІ"),
    "simulation-physics": ("Simulation & Physics", "Симуляція та фізика"),
}

CAT_ORDER = list(CAT_TITLES.keys())

def fmt_num(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)

def main():
    with open("data/repos.json", encoding="utf-8") as f:
        data = json.load(f)

    total = sum(len(v) for v in data.values())
    today = datetime.date.today().isoformat()

    lines = []
    a = lines.append
    a("# 🧮 Algorithms Code Archive / Карта реалізацій алгоритмів")
    a("")
    a(f"**A task-first map of algorithm & data-structure implementations across programming languages.** Need a max-flow solver, an FFT, a convex hull, a Raft implementation? Look up the *task*, get the best repos in any language. ({total} repos, last refreshed {today})")
    a("")
    a("> **Українською:** індекс реалізацій алгоритмів і структур даних, організований **за задачею**, а не за мовою. Кожен пункт — посилання на оригінальний репозиторій GitHub. Індекс оновлюється автоматично через офіційний GitHub Search API (див. [`tools/collect.py`](tools/collect.py)).")
    a("")
    a("> ⚠️ All links point to the **original repositories** — nothing is copied; each repo keeps its own license. / Усі посилання ведуть на оригінальні репозиторії — нічого не копіюється, ліцензії зберігаються у авторів.")
    a("")
    a("---")
    a("")
    a("## 📑 Table of Contents")
    a("")
    for cat in CAT_ORDER:
        repos = data.get(cat, [])
        if not repos:
            continue
        en, _ = CAT_TITLES[cat]
        a(f'- [`{en}`](#cat-{cat}) — {len(repos)} repos')
    a("")
    a("---")
    a("")

    for cat in CAT_ORDER:
        repos = data.get(cat, [])
        if not repos:
            continue
        en, uk = CAT_TITLES[cat]
        a(f'<a id="cat-{cat}"></a>')
        a(f"## {en}")
        a(f"**{uk}**")
        a("")
        a("| Repository | ⭐ | Lang | Task | Description |")
        a("|---|---|---|---|---|")
        for r in repos:
            desc = html.escape((r["desc"] or "").replace("|", "/")) or "—"
            lang = r["lang"] or "—"
            task = r.get("task", "")
            a(f'| [{r["full_name"]}]({r["url"]}) | {fmt_num(r["stars"])} | {lang} | {task} | {desc} |')
        a("")

    a("---")
    a("")
    a("## 🤝 Contributing")
    a("")
    a("Found a great implementation that's missing? Open an issue or PR with: repo URL, target category, and one-line description. Quality bar: active (non-archived), ≥40 stars, real code (not just docs or slides).")
    a("")
    a("## 🔁 How the index is built")
    a("")
    a("- Collected automatically via the official **GitHub Search API** (`tools/collect.py`), curated (`tools/curate.py`), rendered by `tools/gen_readme.py` (data in `data/repos.json`).")
    a(f"- Filters: stars ≥ 40, not archived, deduplicated across categories. Snapshot: **{today}**.")
    a("- Browsed **by task** (compression, graphs, hashing, geometry, DSP...), so you search by what you want to build — the Lang column tells you which language each implementation uses.")
    a("")
    a("## 📄 License")
    a("")
    a("This index: MIT. The linked projects keep their own licenses — check each repo before reuse.")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"README.md written: {total} repos across {sum(1 for v in data.values() if v)} categories")

if __name__ == "__main__":
    main()
