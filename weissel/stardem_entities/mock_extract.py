import json, re, os, sys

input_path = sys.argv[1] if len(sys.argv) > 1 else 'stardem_sample_1.json'
out_path = 'stories_with_entities_mock.json'

if not os.path.exists(input_path):
    # try parent directory
    alt = os.path.join(os.path.dirname(__file__), input_path)
    if os.path.exists(alt):
        input_path = alt
    else:
        print('Input file not found:', input_path)
        sys.exit(1)

with open(input_path, 'r') as f:
    stories = json.load(f)

# Heuristic regexes
name_title_rx = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Mayor|Senator|Representative|Councilman|Councilwoman|Rev|Capt|Judge)\.?.{0,1}\s+[A-Z][a-z]+(?:\s[A-Z][a-z]+){0,2}\b")
proper_name_rx = re.compile(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2}\b")
place_comma_state_rx = re.compile(r"\b[A-Z][\w'\-]+(?:\s+[A-Za-z][\w'\-]+)*,\s*(?:MD|Md|Maryland)\b")
county_rx = re.compile(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\s+County\b")
org_rx = re.compile(r"\b(?:Star Democrat|County Commissioners|County Commission|School District|School Board|Board of Education|Police Department|Fire Department|City Council|Town Council|County Council|Board|Commission|Association|Committee|Department)\b", re.I)
org_keywords = set(['County','Commissioners','Commission','Board','School','District','Company','Inc','Corporation','Department','Hospital','Center','Academy','University','Bank','Police','Fire','Church','Club','Committee','Association','Council','Authority'])

enhanced = []
for s in stories[:5]:
    text = ' '.join(filter(None, [s.get('title',''), s.get('content',''), s.get('summary','')]))
    people = []
    places = []
    orgs = []

    # Titles like 'Mayor Jane Doe' or 'Dr. John Smith'
    for m in name_title_rx.findall(text):
        people.append(m.strip())

    # Generic proper names (2-3 capitalized words) but filter org-like and places
    for m in proper_name_rx.findall(text):
        parts = m.split()
        if any(p in org_keywords for p in parts):
            orgs.append(m)
            continue
        if ',' in m:
            continue
        if len(parts) >= 2 and len(parts) <= 3:
            people.append(m)

    # Places
    for m in place_comma_state_rx.findall(text):
        places.append(m.strip())
    for m in county_rx.findall(text):
        places.append(m.strip())

    # Organizations
    for m in org_rx.findall(text):
        orgs.append(m.strip())
    if re.search(r"\bStar Democrat\b", text, re.I):
        orgs.append('Star Democrat')

    # Dedupe preserving order
        # Dedupe preserving order and apply prioritization / limits
        def dedupe(seq):
            seen = set(); out = []
            for x in seq:
                k = x.strip()
                if not k: continue
                if k not in seen:
                    seen.add(k); out.append(k)
            return out

        # Remove author/byline from people and prioritize important people
        author = s.get('author') or s.get('byline') or ''
        def normalize(n):
            return n.strip()

        people_dedup = []
        seen = set()
        for p in people:
            np = normalize(p)
            if not np: continue
            if author and np.lower() == author.strip().lower():
                continue
            if np not in seen:
                seen.add(np); people_dedup.append(np)

        role_words = ('Mayor', 'Senator', 'Representative', 'Judge', 'Dr', 'Mr', 'Mrs', 'Ms', 'Chief', 'Sheriff', 'Officer', 'Coach', 'President', 'Principal')
        story_text = ' '.join(filter(None, [s.get('title',''), s.get('content',''), s.get('summary','')]))

        def score_person(name, idx):
            score = 0
            lname = name.lower()
            st = story_text.lower()
            # role/title presence is a strong signal
            for rw in role_words:
                if rw.lower() in name.lower():
                    score += 4
            # frequency of mentions is important
            freq = st.count(lname)
            score += min(freq, 5) * 1.5
            # earlier appearance is better
            pos = st.find(lname)
            if pos != -1:
                score += max(0, 3 - (pos / 200.0))
            # shorter names slightly preferred
            score += max(0, 1 - (len(name.split()) - 2) * 0.1)
            return (-score, idx)

        scored = sorted([(score_person(p, i), p) for i, p in enumerate(people_dedup)], key=lambda x: x[0])
        prioritized = [p for _, p in scored]

        # Filter to probable human first+last names
        def is_human_name(n):
            m = re.match(r"^[A-Z][A-Za-z'\-]+\s+[A-Z][A-Za-z'\-]+$", n)
            if not m:
                return False
            org_tokens = ('County','School','District','Commission','Commissioners','Board','Department','Inc','Company','Association','Committee','Publishing','Press','Times','Record','Observer','News','Document')
            for t in org_tokens:
                if t in n:
                    return False
            block_words = ('High','School','Conference','Athletic','Saints','Royals','Bucs','Sabres','Kings','Lady','Saint','Team','Delmarva','Star','Democrat','Christian','Eastern','Shore','Independent','Publishing','Press','Times','Record','Observer','News','Document')
            for part in n.split():
                if part in block_words:
                    return False
            return True

        human_only = [p for p in prioritized if is_human_name(p)]
        # Strictly keep only human-looking first+last names; allow empty list if none found
        people = human_only[:4]

        # Places: dedupe and limit to top 3
        places = dedupe(places)[:3]

        # Orgs: dedupe and keep up to 10
        orgs = dedupe(orgs)[:10]

    es = s.copy()
    es['entities_people'] = people
    es['entities_places'] = places
    es['entities_organizations'] = orgs
    enhanced.append(es)

with open(out_path, 'w') as f:
    json.dump(enhanced, f, indent=2)

print('Wrote', out_path)
print('First story extracted entities:')
if enhanced:
    print(json.dumps({'entities_people': enhanced[0]['entities_people'], 'entities_places': enhanced[0]['entities_places'], 'entities_organizations': enhanced[0]['entities_organizations']}, indent=2))
else:
    print('No stories processed')
