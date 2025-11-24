#!/usr/bin/env python3
import argparse
import json
from datetime import datetime


def infer_year(item):
    # prefer explicit 'year' key
    if isinstance(item, dict):
        y = item.get('year')
        if isinstance(y, int):
            return y
        # fallback: try to parse 'date' field
        d = item.get('date') or item.get('pub_date') or item.get('Date')
        if isinstance(d, str):
            # try common formats
            for fmt in ('%Y-%m-%d','%B %d, %Y','%b %d, %Y','%Y','%m/%d/%Y'):
                try:
                    return datetime.strptime(d.strip(), fmt).year
                except Exception:
                    pass
            # try to extract 4-digit year
            import re
            m = re.search(r"(20\d{2})", d)
            if m:
                return int(m.group(1))
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', '-s', default='weissel/stardem_topic_entities/Sports.json')
    p.add_argument('--out', '-o', default='weissel/stardem_topic_entities/sports2024.json')
    p.add_argument('--preview', action='store_true', help='print a small preview of included titles')
    args = p.parse_args()

    with open(args.source, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise SystemExit('source JSON does not contain a top-level list of stories')

    keep = []
    for item in data:
        year = infer_year(item)
        if year == 2024:
            keep.append(item)

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(keep, f, ensure_ascii=False, indent=2)

    print(f'Wrote {len(keep)} stories to {args.out}')
    if args.preview:
        print('\nSample included titles:')
        for i, it in enumerate(keep[:10], 1):
            t = it.get('title') or it.get('headline') or '<no title>'
            print(f'{i:2d}. {t}')

if __name__ == '__main__':
    main()
