import json
from typing import List, Dict, Union
import os
from pathlib import Path

# Resolve schemes file relative to the repository root (two levels up from this file)
DEFAULT_SCHEMES = {
    "mr": Path(__file__).resolve().parents[2] / "schemes_mr.json",
    "te": Path(__file__).resolve().parents[2] / "schemes_te.json",
}

SCHEMES_PATH = DEFAULT_SCHEMES.get(os.getenv("APP_LANG", "mr"), DEFAULT_SCHEMES["mr"])

def load_schemes(path: Union[str, Path] = SCHEMES_PATH) -> List[Dict]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Schemes file not found at {p}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def find_schemes_by_keywords(keywords: List[str], schemes=None):
    if schemes is None:
        schemes = load_schemes()
    import re

    def normalize(text: str) -> str:
        # Lowercase and remove common punctuation characters
        t = text.lower()
        # remove ASCII punctuation and common unicode punctuation
        t = re.sub(r"[\u0021-\u002f\u003a-\u0040\u005b-\u0060\u007b-\u007e\u0964\u0965,。]", " ", t)
        # collapse whitespace
        t = re.sub(r"\s+", " ", t).strip()
        return t

    def tokens(text: str) -> List[str]:
        return [tok for tok in normalize(text).split(" ") if tok]

    matched = []
    # precompute normalized haystacks
    scheme_hay = []
    for s in schemes:
        hay = f"{s.get('name', '')} {s.get('description', '')}"
        scheme_hay.append((s, normalize(hay), tokens(hay)))

    for k in keywords:
        nk = normalize(k)
        for s, hay_norm, hay_tokens in scheme_hay:
            # direct substring
            if nk and nk in hay_norm:
                if s not in matched:
                    matched.append(s)
                continue
            # token-based fuzzy: any token overlap (substring)
            for tok in tokens(nk):
                for h in hay_tokens:
                    if tok in h or h in tok:
                        if s not in matched:
                            matched.append(s)
                        break
                else:
                    continue
                break

    return matched
