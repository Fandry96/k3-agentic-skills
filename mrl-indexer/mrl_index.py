"""
k3-agentic-skills — MRL Skill Indexer
EmbeddingGemma-300M Edition

Builds mrl_index.pkl from all SKILL.md files (and any knowledge/ subdirs)
in this repo's skills/ directory.

Zero API costs. Zero data leaves the machine. Sub-15ms/embedding.
Model: google/embeddinggemma-300M (768-dim, MRL-native)

Usage:
    pip install sentence-transformers numpy
    python mrl-indexer/mrl_index.py

Output: mrl-indexer/mrl_index.pkl
Search: python mrl-indexer/mrl_search.py "your query here"
"""
import os
import hashlib
import pickle
import time
import re
import numpy as np
from pathlib import Path

# ============================================================
# CONFIG — paths are relative to repo root, auto-detected
# ============================================================
REPO_ROOT   = Path(__file__).parent.parent.resolve()
SKILLS_DIR  = REPO_ROOT / "skills"
OUT_FILE    = Path(__file__).parent / "mrl_index.pkl"

MODEL_NAME       = "google/embeddinggemma-300M"
TARGET_DIMENSION = 768   # MRL-native; truncate to 256/128 for faster search
BATCH_SIZE       = 64
SAVE_INTERVAL    = 200


# ============================================================
# HELPERS
# ============================================================

def sanitize(text: str) -> str:
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)   # strip image tags
    text = re.sub(r"\s+", " ", text).strip()
    return text


def md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def smart_chunk(text: str, limit: int = 2000):
    """Split text into chunks under `limit` chars (~500 tokens).
    EmbeddingGemma supports up to 8192 tokens — generous limit is fine."""
    if len(text) <= limit:
        return [(text, "::main")]
    chunks, current, current_len, idx = [], [], 0, 0
    for line in text.split("\n"):
        ll = len(line) + 1
        if current_len + ll > limit and current:
            chunks.append(("\n".join(current), f"::chunk[{idx}]"))
            idx += 1
            current, current_len = [], 0
        current.append(line)
        current_len += ll
    if current:
        chunks.append(("\n".join(current), f"::chunk[{idx}]"))
    return chunks


def collect_skill_docs() -> list[dict]:
    """Collect SKILL.md files + any knowledge/ markdown files within each skill dir."""
    docs = []
    skill_count = 0
    knowledge_count = 0

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue

        # Primary SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            try:
                text = skill_md.read_text(encoding="utf-8", errors="ignore")
                docs.append({
                    "id":   f"skill:{skill_dir.name}",
                    "text": f"Skill: {skill_dir.name}\n\n{text}",
                    "type": "skill"
                })
                skill_count += 1
            except Exception as e:
                print(f"  [WARN] SKILL.md read error for {skill_dir.name}: {e}")

        # knowledge/ subdirectory (e.g. hestiacp-devops/knowledge/*.md)
        knowledge_dir = skill_dir / "knowledge"
        if knowledge_dir.exists():
            for kf in sorted(knowledge_dir.glob("*.md")):
                try:
                    text = kf.read_text(encoding="utf-8", errors="ignore")
                    docs.append({
                        "id":   f"skill:{skill_dir.name}/knowledge/{kf.name}",
                        "text": f"Skill Knowledge [{skill_dir.name}]: {kf.name}\n\n{text}",
                        "type": "skill-knowledge"
                    })
                    knowledge_count += 1
                except Exception as e:
                    print(f"  [WARN] knowledge read error {kf}: {e}")

        # prompts/ subdirectory (e.g. hestiacp-devops/prompts/*.md)
        prompts_dir = skill_dir / "prompts"
        if prompts_dir.exists():
            for pf in sorted(prompts_dir.glob("*.md")):
                try:
                    text = pf.read_text(encoding="utf-8", errors="ignore")
                    docs.append({
                        "id":   f"skill:{skill_dir.name}/prompts/{pf.name}",
                        "text": f"Skill Prompt [{skill_dir.name}]: {pf.name}\n\n{text}",
                        "type": "skill-prompt"
                    })
                    knowledge_count += 1
                except Exception as e:
                    print(f"  [WARN] prompts read error {pf}: {e}")

    print(f"[SOURCES] {skill_count} SKILL.md files")
    if knowledge_count:
        print(f"[SOURCES] {knowledge_count} knowledge/prompt files")
    return docs


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("k3-agentic-skills — MRL Skill Indexer")
    print("EmbeddingGemma-300M Edition")
    print("=" * 60)
    print(f"[CONFIG] Repo:      {REPO_ROOT}")
    print(f"[CONFIG] Skills:    {SKILLS_DIR}")
    print(f"[CONFIG] Output:    {OUT_FILE}")
    print(f"[CONFIG] Model:     {MODEL_NAME}")
    print(f"[CONFIG] Dimension: {TARGET_DIMENSION} (MRL-native)")
    print()

    # Force PyTorch backend — prevents Keras 3 conflict in mixed TF/torch envs
    import os
    os.environ.setdefault("USE_TF", "0")
    os.environ.setdefault("TRANSFORMERS_NO_TF", "1")

    # Load model
    print("[LOADING] EmbeddingGemma-300M via sentence-transformers...")
    print("          First run downloads ~200MB. Subsequent runs are instant.")
    t0 = time.time()
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME)
        print(f"[MODEL OK] Loaded in {time.time()-t0:.1f}s (<200MB RAM)")
    except ImportError:
        print("[FATAL] sentence-transformers not installed.")
        print("        Run: pip install sentence-transformers numpy")
        return
    except Exception as e:
        print(f"[FATAL] Model load failed: {e}")
        return

    # Connectivity test
    test_vec = model.encode(
        "connectivity test",
        prompt_name="Retrieval-document",
        truncate_dim=TARGET_DIMENSION,
        normalize_embeddings=True
    )
    print(f"[TEST OK] Shape: {test_vec.shape}, norm: {np.linalg.norm(test_vec):.4f}")

    # Load existing index (incremental rebuild — only re-embeds changed files)
    if OUT_FILE.exists():
        with open(OUT_FILE, "rb") as f:
            index = pickle.load(f)
        print(f"[LOADED]  Existing index: {len(index)} entries")
    else:
        index = {}
        print("[FRESH]   No existing index — building from scratch")

    # Collect documents
    print()
    documents = collect_skill_docs()
    print(f"[TOTAL]   {len(documents)} source files to process")
    print()

    # Chunk and diff against existing index
    pending_paths, pending_texts, pending_hashes = [], [], []
    for doc in documents:
        for chunk_text, suffix in smart_chunk(doc["text"]):
            clean = sanitize(chunk_text)
            if not clean or len(clean) < 20:
                continue
            full_path = f"{doc['id']}{suffix}"
            new_hash  = md5(clean)
            if full_path in index and index[full_path].get("hash") == new_hash:
                continue
            pending_paths.append(full_path)
            pending_texts.append(clean)
            pending_hashes.append(new_hash)

    print(f"[CHUNKS]  {len(pending_texts)} need embedding ({len(index)} cached)")

    if not pending_texts:
        print("[DONE]    Index is up to date!")
        _print_summary(index)
        return

    # Batch embed
    print(f"[EMBED]   Processing in batches of {BATCH_SIZE}...")
    start_time = time.time()
    total, unsaved = 0, 0

    for bi in range(0, len(pending_texts), BATCH_SIZE):
        batch_texts  = pending_texts[bi:bi + BATCH_SIZE]
        batch_paths  = pending_paths[bi:bi + BATCH_SIZE]
        batch_hashes = pending_hashes[bi:bi + BATCH_SIZE]
        batch_num    = bi // BATCH_SIZE + 1
        n_batches    = (len(pending_texts) + BATCH_SIZE - 1) // BATCH_SIZE

        vectors = model.encode(
            batch_texts,
            prompt_name="Retrieval-document",
            truncate_dim=TARGET_DIMENSION,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        for path, h, vec, text in zip(batch_paths, batch_hashes, vectors, batch_texts):
            index[path] = {
                "vector":  vec.astype(np.float32),
                "hash":    h,
                "snippet": text[:200]
            }
            total   += 1
            unsaved += 1

        elapsed   = time.time() - start_time
        rate      = total / elapsed if elapsed > 0 else 0
        remaining = (len(pending_texts) - bi - len(batch_texts)) / rate if rate > 0 else 0
        print(f"  [{batch_num}/{n_batches}] +{len(batch_texts)} "
              f"({total} done, {rate:.1f}/s, ~{remaining:.0f}s left)")

        if unsaved >= SAVE_INTERVAL:
            _save(index)
            unsaved = 0

    _save(index)
    elapsed = time.time() - start_time
    print(f"\n[COMPLETE] {total} new entries in {elapsed:.1f}s ({total/elapsed:.1f}/s)")
    _print_summary(index)


def _save(index: dict):
    tmp = str(OUT_FILE) + ".tmp"
    with open(tmp, "wb") as f:
        pickle.dump(index, f, protocol=pickle.HIGHEST_PROTOCOL)
    if OUT_FILE.exists():
        os.remove(OUT_FILE)
    os.rename(tmp, str(OUT_FILE))
    print(f"  [SAVED]  {len(index)} entries -> {OUT_FILE.name}")


def _print_summary(index: dict):
    types: dict[str, int] = {}
    for k in index:
        if k.startswith("skill:") and "/knowledge/" in k:
            t = "skill-knowledge"
        elif k.startswith("skill:") and "/prompts/" in k:
            t = "skill-prompt"
        elif k.startswith("skill:"):
            t = "skill"
        else:
            t = "other"
        types[t] = types.get(t, 0) + 1
    print(f"\n  Total entries: {len(index)}")
    for t, c in sorted(types.items()):
        print(f"    {t}: {c} chunks")
    print(f"\n  Index path: {OUT_FILE}")
    print(f"  Search:     python mrl-indexer/mrl_search.py \"your query\"")


if __name__ == "__main__":
    main()
