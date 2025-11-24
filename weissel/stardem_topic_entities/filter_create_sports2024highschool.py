#!/usr/bin/env python3
"""
Filter 2024 high-school sports stories from a source JSON array.
Usage:
  python filter_create_sports2024highschool.py \
    --source weissel/stardem_topic_entities/Sports.highschool.2024.240.json \
    --out weissel/stardem_topic_entities/sports2024highschool.json

The script uses heuristics to detect high-school coverage (e.g. "High School", "Easton High's", "freshman", "varsity", conference/region/state words)
and filters out obvious pro/college/transactions items.

It prints counts and a short sample of titles that were included/excluded.
"""

import json
import re
import argparse
from pathlib import Path

INCLUDE_KEYWORDS = [
    r"\bhigh school\b",
    r"\bHigh's\b",
    r"\bHigh\b",
    r"\bCounty High\b",
    r"\bHigh School's\b",
]
SCHOOL_NAME_REGEX = re.compile(r"[A-Z][\w'’\-]*(?:\s+[A-Z][\w'’\-]*)*\s+High\b")
GRADE_KEYWORDS = [
    "freshman",
    "sophomore",
    "junior",
    "senior",
    "varsity",
    "junior varsity",
    "JV",
    "senior night",
    "senior's",
]
CONTEXT_KEYWORDS = [
    "conference",
    "region",
    "state",
    "class",
    "Bayside",
    "county",
]
PROFESSIONAL_NEGATIVE = [
    "major league",
    "mlb",
    "nba",
    "nfl",
    "nhl",
    "nwsL",
    "college",
    "ncaa",
    "signed",
    "traded",
    "transactions",
    "spring training",
    "super bowl",
    "world series",
    "all-pro",
    "major",
]


def score_story(story):
    """Return (include_bool, score_details)"""
    content = (story.get("content") or "").replace("\u2019", "'")
    text = content + "\n" + (story.get("title") or "")
    text_l = text.lower()

    year = story.get("year")
    year_ok = (year == 2024) or ("2024" in (story.get("date_parsed") or "") )

    if not year_ok:
        return False, {"reason": "not_2024", "year": year}

    score = 0
    details = {}

    # strong high-school indicators
    if re.search(r"\bhigh school\b", text_l):
        score += 3
        details['high_school_phrase'] = True

    # look for "Easton High" style patterns
    if SCHOOL_NAME_REGEX.search(text):
        score += 2
        details['school_name_pattern'] = True

    # grade/team indicators
    for kw in GRADE_KEYWORDS:
        if kw in text_l:
            score += 1
            details.setdefault('grade_hits', []).append(kw)

    for kw in CONTEXT_KEYWORDS:
        if kw.lower() in text_l:
            score += 1
            details.setdefault('context_hits', []).append(kw)

    # negative signals for professional/transactional pieces
    neg = 0
    for nk in PROFESSIONAL_NEGATIVE:
        if nk.lower() in text_l:
            neg += 1
            details.setdefault('neg_hits', []).append(nk)

    details['score'] = score
    details['neg'] = neg

    # final decision heuristics (conservative): require score >=2 and neg <3
    include = (score >= 2) and (neg < 3)

    # Special-case: if title/content looks like a "TRANSACTIONS" or "TRANSACTIONS 1-" heading, exclude.
    title = (story.get('title') or '').lower()
    if title.startswith('transactions') or 'transactions' in title:
        include = False
        details['reason_override'] = 'transactions_title'

    # Also exclude pieces that look like roundups/transaction-heavy short items
    if len((story.get('content') or '').split()) < 60 and neg > 0 and score < 3:
        include = False
        details['reason_override'] = 'short_and_negative'

    return include, details


def main():
    parser = argparse.ArgumentParser(description='Filter 2024 high-school sports stories')
    parser.add_argument('--source', '-s', default='weissel/stardem_topic_entities/Sports.highschool.2024.240.json')
    parser.add_argument('--out', '-o', default='weissel/stardem_topic_entities/sports2024highschool.json')
    parser.add_argument('--sample', action='store_true', help='print sample titles')
    args = parser.parse_args()

    src = Path(args.source)
    out = Path(args.out)

    if not src.exists():
        print(f"Source file not found: {src}")
        return

    with src.open('r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("Expected top-level JSON array in source file")
        return

    included = []
    excluded = []

    for story in data:
        inc, det = score_story(story)
        if inc:
            included.append(story)
        else:
            excluded.append((story, det))

    # write output
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as f:
        json.dump(included, f, ensure_ascii=False, indent=2)

    print(f"Source: {src} — total stories: {len(data)}")
    print(f"Included (filtered) stories: {len(included)}")
    print(f"Excluded stories: {len(excluded)}")

    if args.sample:
        print('\nSample included titles:')
        for s in included[:10]:
            print(' -', s.get('title'))

        print('\nSample excluded titles:')
        for s, det in excluded[:10]:
            print(' -', s.get('title'), '->', det)

    print('\nWrote:', out)
    print('\nIf you want stricter or looser filtering, tweak GRADE_KEYWORDS, CONTEXT_KEYWORDS, and PROFESSIONAL_NEGATIVE in the script.')


if __name__ == '__main__':
    main()
