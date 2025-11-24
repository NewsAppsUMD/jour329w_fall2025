#!/usr/bin/env python3
"""classify_topics.py

Read a JSON file of stories and assign a single, consistent topic to each
story using the `llm` CLI tool. Saves results to a new JSON file.

Usage:
  uv run python assignments/classify_topics.py --model <model> --input stardem_sample_1.json

The script:
 - loads the input JSON (array of objects)
 - for each story, calls the LLM with a short prompt (title + summary)
 - expects the model to return a single topic name (one or two words)
 - normalizes topic names to a consistent Title Case form
 - writes the enhanced array to `stardem_topics_classified.json`
"""

import json
import subprocess
import argparse
import sys
import time
import re
import os
from pathlib import Path
import shutil


def clean_model_output(text: str) -> str:
    """Strip markdown/code fences and extract the first non-empty line."""
    if not text:
        return ""
    text = text.strip()
    # remove triple-backtick code blocks if present
    if text.startswith('```'):
        parts = text.split('\n')
        # drop the first line (```...) and the last line if it's ```
        if parts[-1].strip().endswith('```'):
            parts = parts[1:-1]
        else:
            parts = parts[1:]
        text = '\n'.join(parts).strip()

    # take first non-empty line
    for line in text.splitlines():
        line = line.strip()
        if line:
            # remove surrounding quotes if present
            line = line.strip('"')
            return line
    return ""


def normalize_topic(topic: str) -> str:
    """Normalize topic strings to consistent Title Case, remove punctuation.

    This is intentionally simple: it lowercases, replaces underscores/hyphens,
    collapses whitespace, then title-cases the result. It helps avoid
    duplicate columns like 'Level' vs 'level' vs 'Level '.
    """
    if not topic:
        return "Other"
    s = topic.strip()
    # remove common leading labels like "Topic:"
    s = re.sub(r'^[Tt]opic:\s*', '', s)
    # replace separators with spaces
    s = s.replace('_', ' ').replace('-', ' ')
    # remove punctuation except ampersand
    s = re.sub(r"[^\w\s&]", '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    if not s:
        return "Other"
    return s.title()


def call_llm(model: str, prompt: str, timeout: int = 60) -> str:
    """Call the `llm` CLI and return stdout (text) or an error string prefixed with '__ERROR__:'.

    This implementation sends the prompt on stdin which is compatible with the `llm` CLI used
    elsewhere in this repository (you can also pipe a prompt into `uv run llm -m <model>`).
    """
    try:
        # send the prompt via stdin to be compatible with `llm -m <model>` usage
        result = subprocess.run(["llm", "-m", model], input=prompt, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            return f"__ERROR__:{result.stderr.strip() or result.stdout.strip()}"
        return result.stdout.strip()
    except FileNotFoundError:
        return "__ERROR__:llm CLI not found. Install it (uv run llm --help) or use --mock for testing."
    except Exception as e:
        return f"__ERROR__:{str(e)}"


def main():
    parser = argparse.ArgumentParser(description='Classify topics for Star-Democrat stories')
    # model may be provided via --model or LLM_MODEL env var; default to a sensible value
    parser.add_argument('--model', required=False, default=os.environ.get('LLM_MODEL', 'groq/meta-llama/llama-4-scout-17b-16e-instruct'),
                        help='Model to use with llm (e.g. groq/meta-llama/...). Can also be set via LLM_MODEL env var')
    parser.add_argument('--input', default='stardem_sample.json', help='Input JSON file (array of stories)')
    parser.add_argument('--mock', action='store_true', help='Use a lightweight local heuristic instead of calling the `llm` CLI (for testing)')
    parser.add_argument('--topics-file', default='', help='Optional JSON file containing a list of allowed one-word topics')
    parser.add_argument('--output', default='stardem_topics_classified.json', help='Output JSON file')
    parser.add_argument('--sleep', type=float, default=0.8, help='Seconds to sleep between LLM calls')
    args = parser.parse_args()

    inp = Path(args.input)
    # if the chosen default filename doesn't exist, fall back to stardem_sample_1.json (legacy name)
    if not inp.exists():
        alt = Path('stardem_sample_1.json')
        if alt.exists():
            inp = alt
        else:
            print(f"Input file not found: {inp} (tried fallback stardem_sample_1.json and it was missing)")
            sys.exit(1)

    with inp.open() as f:
        stories = json.load(f)

    # Load canonical topics: either from --topics-file or use built-in 15-topic list
    BUILT_IN_TOPICS = [
        "government", "planning", "development", "housing", "agriculture",
        "fisheries", "environment", "education", "sports", "business",
        "health", "safety", "events", "arts", "obituary",
    ]

    if args.topics_file:
        tf = Path(args.topics_file)
        if tf.exists():
            try:
                with tf.open() as fh:
                    topics = json.load(fh)
                    if not isinstance(topics, list):
                        print(f"topics-file {tf} does not contain a JSON list — using built-in topics")
                        topics = BUILT_IN_TOPICS
            except Exception:
                print(f"Failed to read topics-file {tf} — using built-in topics")
                topics = BUILT_IN_TOPICS
        else:
            print(f"topics-file {tf} not found — using built-in topics")
            topics = BUILT_IN_TOPICS
    else:
        topics = BUILT_IN_TOPICS

    # normalize topics to exact tokens (lowercase single words preferred)
    topics = [str(t).strip() for t in topics if t]

    enhanced = []
    seen_topics = {}

    total = len(stories)
    # If llm CLI is not available and --mock not specified, automatically fall back to mock mode
    if not args.mock:
        if shutil.which('llm') is None:
            print("Warning: 'llm' CLI not found in PATH — falling back to --mock mode for local testing")
            args.mock = True

    print(f"Classifying {total} stories using model {args.model} (mock={args.mock})")

    # helper: simple mock classifier using keyword matching
    def classify_mock(title: str, content: str, topics_list):
        txt = (title + '\n' + content).lower()
        # keyword map (topic -> list of keywords)
        keyword_map = {
            'sports': ['score', 'game', 'win', 'season', 'tournament', 'championship', 'basketball', 'football', 'wrestl', 'softball', 'lacrosse'],
            'education': ['school', 'board', 'student', 'teacher', 'high school', 'college', 'university'],
            'agriculture': ['farm', 'farmer', 'agricultur', 'crop', 'livestock', 'marbidco', 'blue catfish'],
            'fisheries': ['fish', 'seafood', 'bay', 'harbor', 'boat', 'boat show', 'choptank'],
            'business': ['business', 'opened', 'ribbon', 'store', 'company', 'entrepreneur'],
            'health': ['health', 'hospital', 'clinic', 'covid', 'mental health', 'va medical'],
            'government': ['county', 'commission', 'council', 'governor', 'senator', 'mayor', 'board'],
            'planning': ['zoning', 'planning', 'master plan', 'development', 'infill', 'sewer', 'water', 'infrastructure'],
            'housing': ['housing', 'affordable', 'townhomes', 'residential', 'subdivision'],
            'environment': ['environment', 'conservation', 'wetland', 'marsh', 'wildlife', 'solar'],
            'safety': ['fire', 'shoot', 'arrest', 'murder', 'accident', 'ems', 'police', 'firefighters'],
            'arts': ['art', 'gallery', 'festival', 'concert', 'theatre', 'museum'],
            'events': ['event', 'calendar', 'fair', 'festival', 'parade', 'meet', 'ribbon cutting'],
            'obituary': ['died', 'dies', 'obituary', 'celebrate', 'birthday', 'passed away'],
        }
        # score topics
        scores = {t: 0 for t in topics_list}
        for top, kws in keyword_map.items():
            for kw in kws:
                if kw in txt:
                    # if top is in allowed topics
                    if top in scores:
                        scores[top] += 1
        # pick best
        best = max(scores.items(), key=lambda kv: kv[1])
        if best[1] == 0:
            return 'other'
        return best[0]

    for i, story in enumerate(stories, start=1):
        title = story.get('title') or ''
        # prefer 'content', fall back to 'summary' or other fields
        content = story.get('content') or story.get('summary') or ''

        # Build prompt that lists allowed tokens exactly (one-word tokens recommended)
        canonical_list = ', '.join(topics)
        prompt = f"""
        Analyze this news story and assign it a single topic token.
        Choose exactly ONE token (return only the token string) from the following list (use exact spelling):
        {canonical_list}

        Title: {title}
        Content: {content}
        """

        if args.mock:
            out_token = classify_mock(title, content, topics)
            raw = out_token
        else:
            raw = call_llm(args.model, prompt)
        out = clean_model_output(raw)
        # normalize to token form
        topic = normalize_topic(out).lower()

        # maintain a stable canonical mapping (first seen wins)
        # map normalized output to allowed topics (best-effort); first-seen canonical wins
        if topic in [t.lower() for t in topics]:
            key = topic
            canonical = seen_topics.get(key, topic)
            if key not in seen_topics:
                seen_topics[key] = topic
        else:
            # attempt simple substring match
            mapped = None
            for t in topics:
                if t.lower() in topic or topic in t.lower():
                    mapped = t
                    break
            if mapped:
                canonical = seen_topics.get(mapped, mapped)
                seen_topics[mapped] = canonical
            else:
                canonical = 'other'
                seen_topics['other'] = 'other'

        enhanced_story = dict(story)
        enhanced_story['topic'] = canonical
        enhanced.append(enhanced_story)

        print(f"[{i}/{total}] -> {canonical}")
        time.sleep(args.sleep)

    # write output
    outp = Path(args.output)
    with outp.open('w') as f:
        json.dump(enhanced, f, indent=2)

    print(f"Wrote {len(enhanced)} classified stories to {outp}")


if __name__ == '__main__':
    main()
