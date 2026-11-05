#!/usr/bin/env python3
"""Curation pass over data/repos.json: remove off-topic repos, fix misplacements.
REMOVE/MOVE lists are maintained by the maintainer after each collection run.
"""
import json

REMOVE = {
    # --- compression: not classic data-compression algorithms ---
    "headroomlabs-ai/headroom", "deepspeedai/DeepSpeed", "gchq/CyberChef",
    "leandromoreira/digital_video_introduction", "PaddlePaddle/PaddleNLP",
    "IridiumIO/CompactGUI", "peazip/PeaZip", "quantumaikr/quant.cpp",
    "mrphrazer/msynth", "harvardnlp/NeuralSteganography", "mcleish7/arithmetic",
    "zipnn/zipnn", "mightydeveloper/Deep-Compression-PyTorch",
    "chrisneagu/FTC-Skystone-Dark-Angels-Romania-2020", "0xHossam/HuffLoader",
    "borgbackup/borg",
    # --- hashing-crypto: products/platforms, not crypto algorithms ---
    "bitcoin/bitcoin", "anoma/anoma", "bee-san/Ciphey", "amark/gun",
    "cryptomator/cryptomator", "javascript-obfuscator/javascript-obfuscator",
    "apache/shiro", "kjur/jsrsasign", "rust-in-blockchain/awesome-blockchain-rust",
    "OpenAS2/OpenAs2App",
    # --- math-numerics: search engines, wrappers, tutorials ---
    "blevesearch/bleve", "guoguibing/librec", "pycontribs/jira",
    "mrcodetastic/ESP32-HUB75-MatrixPanel-DMA", "higham/what-is",
    "tirthajyoti/Stats-Maths-with-Python", "DiffEqML/torchdyn",
    "hosseinmoein/DataFrame",
    # --- image-vision: apps, paper lists, courses ---
    "roboflow/supervision", "ocrmypdf/OCRmyPDF", "JaidedAI/EasyOCR",
    "danielgatis/rembg", "amusi/CVPR2026-Papers-with-Code", "lukas-blecher/LaTeX-OCR",
    "GraphiteEditor/Graphite", "cshum/imagor", "h2non/bimg",
    "abusufyanvu/6S191_MIT_DeepLearning",
    "JayabharathP/The-Python-Mega-Course-Build-10-Real-World-Applications-",
    "CommissarMa/Crowd_counting_from_scratch",
    "himanshub1007/Alzhimers-Disease-Prediction-Using-Deep-learning",
    "luxonis/datadreamer", "mctrinh/neural-networks-from-scratch",
    "hemansnation/Machine-Learning-MLOps-GenerativeAI-NLP-CV-MLSystem-Design",
    # --- audio-dsp ---
    "AhmadHassan-BTed/NaSuno-SongHumanizer", "AhmadHassan-BTed/AhSilence",
    "Aureliengmz/clearwater", "maltman23/ArduTouch",
    "gionanide/Speech_Signal_Processing_and_Classification", "BatchDrake/SigDigger",
    # --- bioinformatics: courses, agent skills, dashboards ---
    "Developer-Y/cs-video-courses", "K-Dense-AI/scientific-agent-skills", "plotly/dash",
    "synthetic-sciences/openscience", "ai4s-research/awesome-ai-for-science",
    "nextflow-io/nextflow", "ClawBio/ClawBio", "LeonChaoX/qinyan-academic-skills",
    # --- nlp: LLM books/courses, apps ---
    "huggingface/transformers", "rasbt/LLMs-from-scratch", "d2l-ai/d2l-zh",
    "d2l-ai/d2l-en", "GokuMohandas/Made-With-ML", "eugeneyan/applied-ml",
    "srbhr/Resume-Matcher", "explosion/spacy-models", "diasks2/ruby-nlp",
    "taishi-i/awesome-japanese-nlp-resources", "totalgood/nlpia",
    "abhishek305/PyBot-A-ChatBot-For-Answering-Python-Queries-Using-NLP",
    # --- data-structures: interview prep, apps, clients ---
    "jwasham/coding-interview-university", "labuladong/fucking-algorithm",
    "azl397985856/leetcode", "pandas-dev/pandas", "huihut/interview",
    "halfrost/LeetCode-Go", "redisson/redisson", "MemoriLabs/Memori",
    "assimp/assimp", "MontFerret/ferret", "javascriptdata/danfojs",
    "evrencoskun/TableView", "nutsdb/nutsdb",
    # --- collections: interview prep / books / solution dumps ---
    "kdn251/interviews", "doocs/leetcode", "donnemartin/interactive-coding-challenges",
    "forthespada/CS-Books", "crossoverJie/JCSprout", "kunal-kushwaha/DSA-Bootcamp-Java",
    "QuantConnect/Lean", "InterviewMap/CS-Interview-Knowledge-Map",
    "ashishps1/awesome-leetcode-resources", "halfrost/Halfrost-Field",
    "iamshuaidi/CS-Book", "Blankj/awesome-java-leetcode", "krahets/LeetCode-Book",
    "wisdompeak/LeetCode", "WooVictory/Ready-For-Tech-Interview",
    # --- simulation: game engines, one-off apps, AI-agent noise ---
    "BoomingTech/Piccolo", "melonjs/melonJS", "galacean/engine",
    "mob-sakai/ParticleEffectForUGUI", "miickel/flutter_particle_clock",
    "stackql/stackql", "AhmadHassan-BTed/RoseWish", "csml-rpi/Foam-Agent",
    "ryoungj/ToolEmu", "sublayerapp/sublayer", "civai-technologies/cursor-agent",
    "USTCPCS/CVPR2018_attention", "sketchpunk/FunWithWebGL2",
}

MOVE = {  # full_name -> (from_cat, to_cat)
    "symbolica-dev/symbolica": ("compression", "math-numerics"),
    "gcherchi/FastAndRobustMeshArrangements": ("compression", "geometry"),
    "cgzirim/seek-tune": ("collections", "audio-dsp"),
    "krzyzanowskim/CryptoSwift": ("collections", "hashing-crypto"),
}

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
