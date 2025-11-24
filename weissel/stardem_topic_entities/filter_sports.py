#!/usr/bin/env python3
import json
from pathlib import Path

INPUT = Path(__file__).parent / "Sports.json"
OUTPUT = Path(__file__).parent / "Sports.filtered.json"

# Keywords that strongly indicate a national/pro league story
LEAGUE_KEYWORDS = [
    "nfl", "mlb", "nba", "nhl", "mls", "major league", "world series", "super bowl",
    "all-star", "national", "us open", "u.s. open", "grand slam", "nhl", "stanley cup",
    "champions league", "uefa", "college football", "ncaa", "pac-12", "big ten", "big ten",
    "national championship", "world championship", "premier league", "fifa", "olympic"
]

# Local place tokens commonly found in local/regional stories in this dataset
LOCAL_KEYWORDS = [
    "easton", "cambridge", "dent", "tilghman", "talbot", "caroline", "dorchester",
    "kent island", "queen anne", "salisbury", "anne arundel", "annapolis", "stevensville",
    "ridgely", "centreville", "middleshore", "millsboro", "chesapeake", "choptank", "county",
]


def score_of(entry):
    # Try nested llm_classification.score, or top-level 'score'
    sc = 0.0
    if isinstance(entry, dict):
        llm = entry.get("llm_classification") or entry.get("llm_classification_meta")
        if llm and isinstance(llm, dict) and "score" in llm:
            try:
                sc = float(llm.get("score", 0) or 0)
            except Exception:
                sc = 0.0
        else:
            # Some files might have top-level 'score'
            if "score" in entry:
                try:
                    sc = float(entry.get("score", 0) or 0)
                except Exception:
                    sc = 0.0
    return sc


def text_contains_any(text, keywords):
    if not text:
        return False
    t = text.lower()
    for k in keywords:
        if k in t:
            return True
    return False


def is_national_only(entry):
    # Heuristic: mentions national/league keywords AND does not mention local keywords
    title = entry.get("title", "")
    content = entry.get("content", "")
    combined = (title + "\n" + (content or "")).lower()

    has_league = text_contains_any(combined, LEAGUE_KEYWORDS)
    has_local = text_contains_any(combined, LOCAL_KEYWORDS)

    # Another signal: the llm candidates include National News with a fairly high score
    llm = entry.get("llm_classification")
    national_candidate = False
    if isinstance(llm, dict):
        candidates = llm.get("candidates") or []
        if isinstance(candidates, list):
            for c in candidates:
                if isinstance(c, dict):
                    topic = (c.get("topic") or "").lower()
                    try:
                        cand_score = float(c.get("score") or 0)
                    except Exception:
                        cand_score = 0
                    if "national" in topic and cand_score >= 0.5:
                        national_candidate = True

    return (has_league and not has_local) or (national_candidate and not has_local)


def main(min_score=0.9):
    data = json.loads(INPUT.read_text())
    kept = []
    removed = []

    for entry in data:
        sc = score_of(entry)
        if sc < min_score:
            removed.append((entry, "low_score", sc))
            continue
        if is_national_only(entry):
            removed.append((entry, "national_only", sc))
            continue
        kept.append(entry)

    OUTPUT.write_text(json.dumps(kept, ensure_ascii=False, indent=2))

    # Print a short summary
    print(json.dumps({
        "input_count": len(data),
        "kept_count": len(kept),
        "removed_count": len(removed),
        "removed_examples": [
            {"title": (e.get('title') if isinstance(e, dict) else None), "reason": r, "score": s}
            for (e, r, s) in removed[:10]
        ]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
