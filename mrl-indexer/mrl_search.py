"""
MRL Semantic Search — EmbeddingGemma-300M Edition
Searches the mrl_index.pkl using cosine similarity.

Usage:
    python mrl_search.py "your query here"
    python mrl_search.py "your query" --top 20
    python mrl_search.py "your query" --type skill
"""
import pickle
import numpy as np
import argparse
import time

# Lazy-load model to avoid import cost on repeated runs
_model = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("google/embeddinggemma-300M")
    return _model


def load_index(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def search(query, index, top_k=10, filter_type=None, dim=768):
    """Semantic search over the MRL index.
    
    Args:
        query: Natural language search query
        index: Dict of {path: {vector, hash, snippet}}
        top_k: Number of results to return
        filter_type: Optional filter (skill, ki, brain, deep-research, night2, night3)
        dim: MRL truncation dimension (768, 512, 256, or 128)
    """
    model = get_model()
    
    # Embed query with Retrieval-query prompt
    q_vec = model.encode(
        query,
        prompt_name="Retrieval-query",
        truncate_dim=dim,
        normalize_embeddings=True
    ).astype(np.float32)
    
    # Score all entries
    results = []
    for path, entry in index.items():
        # Apply type filter
        if filter_type:
            if filter_type == "skill" and not path.startswith("skill:"):
                continue
            elif filter_type == "ki" and not path.startswith("KI:"):
                continue
            elif filter_type == "brain" and not path.startswith("brain:"):
                continue
            elif filter_type == "deep-research" and not path.startswith("deep-research:"):
                continue
            elif filter_type == "night3" and not path.startswith("night3:"):
                continue
            elif filter_type == "night2" and not any(path.startswith(p) for p in ["skill:", "KI:", "brain:", "deep-research:", "night3:"]):
                if filter_type != "night2":
                    continue
        
        vec = entry["vector"]
        # MRL truncation for search (must match index dim)
        if len(vec) > dim:
            vec = vec[:dim]
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
        
        score = float(np.dot(q_vec, vec))
        results.append((path, score, entry.get("snippet", "")))
    
    # Sort by score descending
    results.sort(key=lambda x: -x[1])
    return results[:top_k]


def format_results(results, query):
    """Pretty-print search results."""
    print(f"\n{'='*60}")
    print(f"  Query: \"{query}\"")
    print(f"  Results: {len(results)}")
    print(f"{'='*60}\n")
    
    for i, (path, score, snippet) in enumerate(results, 1):
        # Determine type
        if path.startswith("skill:"):
            tag = "[SKILL]"
            name = path.split("::")[0].replace("skill:", "")
        elif path.startswith("KI:"):
            tag = "[KI]"
            name = path.split("::")[0]
        elif path.startswith("deep-research:"):
            tag = "[RESEARCH]"
            name = path.split("::")[0].replace("deep-research:", "")
        elif path.startswith("brain:"):
            tag = "[BRAIN]"
            name = path.split("::")[0].replace("brain:", "")
        elif path.startswith("night3:"):
            tag = "[NIGHT-3]"
            name = path.split("::")[0].replace("night3:", "")
        else:
            tag = "[DOC]"
            name = path.split("::")[0]
        
        bar = "#" * int(score * 20)
        print(f"  {i:2d}. [{score:.4f}] {bar}")
        print(f"      {tag}: {name}")
        print(f"      {snippet[:120]}...")
        print()


def main():
    parser = argparse.ArgumentParser(description="MRL Semantic Search")
    parser.add_argument("query", help="Natural language search query")
    parser.add_argument("--top", type=int, default=10, help="Number of results (default: 10)")
    parser.add_argument("--type", choices=["skill", "ki", "brain", "deep-research", "night2", "night3"],
                       help="Filter by source type")
    parser.add_argument("--dim", type=int, default=768, choices=[768, 512, 256, 128],
                       help="MRL truncation dimension (default: 768)")
    parser.add_argument("--index", default=None, help="Path to mrl_index.pkl")
    args = parser.parse_args()
    
    # Find index
    idx_path = args.index
    if not idx_path:
        candidates = [
            r"C:\K3_Firehose\k3-mcp-toolbox-public\k3-mcp-toolbox\src\mrl_index.pkl",
            "mrl_index.pkl",
        ]
        for c in candidates:
            if __import__("os").path.exists(c):
                idx_path = c
                break
    
    if not idx_path:
        print("[ERROR] mrl_index.pkl not found. Specify with --index")
        return
    
    print(f"[INDEX] Loading {idx_path}...")
    t0 = time.time()
    index = load_index(idx_path)
    print(f"[INDEX] {len(index)} entries loaded in {time.time()-t0:.1f}s")
    
    print(f"[MODEL] Loading EmbeddingGemma-300M...")
    t0 = time.time()
    results = search(args.query, index, top_k=args.top, filter_type=args.type, dim=args.dim)
    elapsed = time.time() - t0
    
    format_results(results, args.query)
    print(f"  Search completed in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
