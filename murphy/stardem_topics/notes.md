# star-dem topic exploration — cat murphy, nov. 1

as you're well aware from having to deal with me, the embeddings map wouldn't render, so i didn't actually have a chance to explore that.

## option 2

i chose to start with option 2 because, given the disastrous organization of the star-dem articles, i quite frankly don't trust that the llm will be able to classify the articles without explicit instruction.

here's what i gave copilot:

```python
I need to build a python script called `classify_topics.py`.

Here are the script requirements:
- Use the `llm` command-line tool with the model `groq/meta-llama/llama-4-scout-17b-16e-instruct`
- Use subprocess to call the `llm` command using `stardem_topics.md` as a reference
- Have the LLM process each story from `stardem_sample.json`
- Have the LLM assign each story the single best-fitting topic from the topic list provided in `topics.csv`
- Have the LLM save the updated stories to `stardem_topics_classified.json`
- Print progress as it processes stories
```

for context, i did what we did with the cns_tag_browser assignment and created a .csv file with not only topic names but descriptions of those topics. so, for example:

```
Topic, Description
"Local Government","News articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss the members and actions of a local government, including mayors and mayoral candidates, town boards, and town or county councils."
```

again, i did this because i wanted to be as explicit as possible as far as how it should classify the stories. except, my last topic classification was "other," which i defined as "obituaries, legal notices, calendars, columns, editorials and any articles that do not otherwise fall under a defined topic."

... and that meant that the first time i ran the script, it classified all 200 stories as "other." lol.

i tried to troubleshoot a bit, but that didn't really get me anywhere, so i rewrote my copilot prompt.

```python
topic_list = [
    {
        "topic": "Local Government",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss the members and actions of a local government, including mayors and mayoral candidates, town boards, and town or county councils."
    },
    {
        "topic": "Economy & Budget",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss the finances and economy of a municipality."
    },
    {
        "topic": "Planning & Development",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss planning, zoning or municipal development."
    },
    {
        "topic": "Housing",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss housing, including affordable housing, homelessness and new housing developments."
    },
    {
        "topic": "Transportation, Infrastructure & Public Works",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss transportation, infrastructure or public works at the municipal level, including public transportation, roads and bridges, and public sewer, electricity and water services."
    },
    {
        "topic": "Public Safety & Crime",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss public safety, municipal crime, local police or legal cases."
    },
    {
        "topic": "Arts & Society",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local community and culture, including restaurants, performances, art, music, fairs and other public events."
    },
    {
        "topic": "Education",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss primary or secondary education at the local level, including municipal school systems, curricula and funding."
    },
    {
        "topic": "Environment",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss environmental topics, including pollution, ecosystems, conservation and the Chesapeake Bay."
    },
    {
        "topic": "Community Outreach",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss municipal social programs, including food drives, vaccination drives, free mental health screenings and other public benefit initiatives."
    },
    {
        "topic": "Elections",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local elections, including mayoral elections, town or county council elections and town or county board elections."
    },
    {
        "topic": "Agriculture",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local agriculture and aquaculture, including fishing, crabbing and farming."
    },
    {
        "topic": "Sports",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local sports, including youth sports, high school sports and athletic infrastructure."
    },
    {
        "topic": "Calendars",
        "definition": "Calendars."
    },
    {
        "topic": "Obituaries",
        "definition": "Obituaries."
    },
    {
        "topic": "Legal Notices",
        "definition": "Legal notices."
    },
    {
        "topic": "Columns & Editorials",
        "definition": "Columns and editorials."
    },
    {
        "topic": "Other",
        "definition": "Other non-news articles that do not fall under another clearly defined topic."
    }
]

I need to build a python script called `classify_topics.py`.

Here are the script requirements: 
- Use subprocess to call the `llm` command-line tool with the model `groq/meta-llama/llama-4-scout-17b-16e-instruct` 
- Have the LLM process each story from `stardem_sample.json`
- Have the LLM assign each story the single best-fitting topic from `topic_list`
- Have the LLM save the updated stories to `stardem_topics_classified.json`
- Print progress as it processes stories
```





## copilot chat log 

cat-murphy: I need to build a python script called `classify_topics.py`.

Here are the script requirements:
- Use the `llm` command-line tool with the model `groq/meta-llama/llama-4-scout-17b-16e-instruct`
- Use subprocess to call the `llm` command using `stardem_topics.md` as a reference
- Have the LLM process each story from `stardem_sample.json`
- Have the LLM assign each story the single best-fitting topic from the topic list provided in `topics.csv`
- Have the LLM save the updated stories to `stardem_topics_classified.json`
- Print progress as it processes stories

GitHub Copilot: ````python
import json
import csv
import subprocess
from pathlib import Path

# File paths
SAMPLE_JSON = "stardem_sample.json"
TOPICS_CSV = "topics.csv"
REFERENCE_MD = "../assignments/stardem_topics.md"
OUTPUT_JSON = "stardem_topics_classified.json"

# Load stories
with open(SAMPLE_JSON, "r") as f:
    stories = json.load(f)

# Load topic list from CSV
topic_list = []
with open(TOPICS_CSV, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        topic = row[0].strip().strip('"')
        topic_list.append(topic)

# Prepare reference file path (absolute)
reference_path = str(Path(REFERENCE_MD).resolve())

# Classify each story
for idx, story in enumerate(stories, 1):
    prompt = f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {story.get('title', '')}
Content: {story.get('content', '')}

Return only the topic name from the list above.
"""
    # Call llm via subprocess
    try:
        result = subprocess.run(
            [
                "llm",
                "-m", "groq/meta-llama/llama-4-scout-17b-16e-instruct",
                "--system", f"Refer to the file {reference_path} for context.",
                "--context-file", reference_path,
                "--no-stream"
            ],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True
        )
        topic = result.stdout.decode("utf-8").strip().splitlines()[0]
    except Exception as e:
        topic = "Other"
        print(f"Error classifying story {idx}: {e}")

    story["topic"] = topic
    print(f"[{idx}/{len(stories)}] Classified: {story.get('title', '')} -> {topic}")

# Save results
with open(OUTPUT_JSON, "w") as f:
    json.dump(stories, f, indent=2)
print(f"\nSaved classified stories to {OUTPUT_JSON}")
````

cat-murphy: It's classifying everything as other

GitHub Copilot: This is likely because many entries in your `stardem_sample.json` are not real stories—they just have a `"day"` field and no `"title"` or `"content"`. The LLM can't classify these, so it defaults to "Other".

**How to fix:**  
Skip any story that doesn't have both a `"title"` and `"content"` field. Only send real stories to the LLM.

Here’s how you can update your script:

````python
# ...existing code...

classified_stories = []

for idx, story in enumerate(stories, 1):
    title = story.get('title', '').strip()
    content = story.get('content', '').strip()
    if not title or not content:
        # Skip non-story entries, but still add with topic "Other"
        story["topic"] = "Other"
        classified_stories.append(story)
        print(f"[{idx}/{len(stories)}] Skipped non-story entry (no title/content) -> Other")
        continue

    prompt = f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {title}
Content: {content}

Return only the topic name from the list above.
"""
    try:
        result = subprocess.run(
            [
                "llm",
                "-m", "groq/meta-llama/llama-4-scout-17b-16e-instruct",
                "--system", f"Refer to the file {reference_path} for context.",
                "--context-file", reference_path,
                "--no-stream"
            ],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True
        )
        topic = result.stdout.decode("utf-8").strip().splitlines()[0]
    except Exception as e:
        topic = "Other"
        print(f"Error classifying story {idx}: {e}")

    story["topic"] = topic
    classified_stories.append(story)
    print(f"[{idx}/{len(stories)}] Classified: {title} -> {topic}")

# Save results
with open(OUTPUT_JSON, "w") as f:
    json.dump(classified_stories, f, indent=2)
print(f"\nSaved classified stories to {OUTPUT_JSON}")
# ...existing code...
````

This will only classify real stories and mark the rest as "Other".

cat-murphy: Rewrite the script so that it only looks at the content and title keys when it reads the sample json

GitHub Copilot: ````python
import json
import csv
import subprocess
from pathlib import Path

# File paths
SAMPLE_JSON = "stardem_sample.json"
TOPICS_CSV = "topics.csv"
REFERENCE_MD = "../assignments/stardem_topics.md"
OUTPUT_JSON = "stardem_topics_classified.json"

# Load stories
with open(SAMPLE_JSON, "r") as f:
    stories = json.load(f)

# Load topic list from CSV
topic_list = []
with open(TOPICS_CSV, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        topic = row[0].strip().strip('"')
        topic_list.append(topic)

# Prepare reference file path (absolute)
reference_path = str(Path(REFERENCE_MD).resolve())

classified_stories = []

for idx, story in enumerate(stories, 1):
    title = story.get('title', '').strip()
    content = story.get('content', '').strip()
    if not title and not content:
        # Skip entries with neither title nor content
        continue

    prompt = f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {title}
Content: {content}

Return only the topic name from the list above.
"""
    try:
        result = subprocess.run(
            [
                "llm",
                "-m", "groq/meta-llama/llama-4-scout-17b-16e-instruct",
                "--system", f"Refer to the file {reference_path} for context.",
                "--context-file", reference_path,
                "--no-stream"
            ],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True
        )
        topic = result.stdout.decode("utf-8").strip().splitlines()[0]
    except Exception as e:
        topic = "Other"
        print(f"Error classifying story {idx}: {e}")

    classified_stories.append({
        "title": title,
        "content": content,
        "topic": topic
    })
    print(f"[{idx}/{len(stories)}] Classified: {title} -> {topic}")

# Save results
with open(OUTPUT_JSON, "w") as f:
    json.dump(classified_stories, f, indent=2)
print(f"\nSaved classified stories to {OUTPUT_JSON}")
````

cat-murphy: Do it with this one

GitHub Copilot: ````python
import json
import csv
import subprocess
from pathlib import Path

# File paths
SAMPLE_JSON = "stardem_sample.json"
TOPICS_CSV = "topics.csv"
REFERENCE_MD = "../assignments/stardem_topics.md"
OUTPUT_JSON = "stardem_topics_classified.json"

# Load stories, keeping only title and content keys
with open(SAMPLE_JSON, "r") as f:
    raw_stories = json.load(f)
    stories = []
    for s in raw_stories:
        story = {}
        if "title" in s:
            story["title"] = s["title"]
        if "content" in s:
            story["content"] = s["content"]
        if story:  # Only add if at least one key exists
            stories.append(story)

# Load topic list from CSV (first column only)
topic_list = []
with open(TOPICS_CSV, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        topic = row[0].strip().strip('"')
        topic_list.append(topic)

# Prepare reference file path (absolute)
reference_path = str(Path(REFERENCE_MD).resolve())

classified_stories = []

for idx, story in enumerate(stories, 1):
    title = story.get('title', '').strip()
    content = story.get('content', '').strip()
    if not title and not content:
        continue

    prompt = f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {title}
Content: {content}

Return only the topic name from the list above.
"""
    try:
        result = subprocess.run(
            [
                "llm",
                "-m", "groq/meta-llama/llama-4-scout-17b-16e-instruct",
                "--system", f"Refer to the file {reference_path} for context.",
                "--context-file", reference_path,
                "--no-stream"
            ],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True
        )
        topic = result.stdout.decode("utf-8").strip().splitlines()[0]
    except Exception as e:
        topic = "Other"
        print(f"Error classifying story {idx}: {e}")

    classified_stories.append({
        "title": title,
        "content": content,
        "topic": topic
    })
    print(f"[{idx}/{len(stories)}] Classified: {title} -> {topic}")

# Save results
with open(OUTPUT_JSON, "w") as f:
    json.dump(classified_stories, f, indent=2)
print(f"\nSaved classified stories to {OUTPUT_JSON}")
````

cat-murphy: topic_list = [
    {
        "topic": "Local Government",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss the members and actions of a local government, including mayors and mayoral candidates, town boards, and town or county councils."
    },
    {
        "topic": "Economy & Budget",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss the finances and economy of a municipality."
    },
    {
        "topic": "Planning & Development",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss planning, zoning or municipal development."
    },
    {
        "topic": "Housing",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss housing, including affordable housing, homelessness and new housing developments."
    },
    {
        "topic": "Transportation, Infrastructure & Public Works",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss transportation, infrastructure or public works at the municipal level, including public transportation, roads and bridges, and public sewer, electricity and water services."
    },
    {
        "topic": "Public Safety & Crime",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss public safety, municipal crime, local police or legal cases."
    },
    {
        "topic": "Arts & Society",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local community and culture, including restaurants, performances, art, music, fairs and other public events."
    },
    {
        "topic": "Education",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss primary or secondary education at the local level, including municipal school systems, curricula and funding."
    },
    {
        "topic": "Environment",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss environmental topics, including pollution, ecosystems, conservation and the Chesapeake Bay."
    },
    {
        "topic": "Community Outreach",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss municipal social programs, including food drives, vaccination drives, free mental health screenings and other public benefit initiatives."
    },
    {
        "topic": "Elections",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local elections, including mayoral elections, town or county council elections and town or county board elections."
    },
    {
        "topic": "Agriculture",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local agriculture and aquaculture, including fishing, crabbing and farming."
    },
    {
        "topic": "Sports",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local sports, including youth sports, high school sports and athletic infrastructure."
    }
]

I need to build a python script called `classify_topics.py`.

Here are the script requirements: 
- Use subprocess to call the `llm` command-line tool with the model `groq/meta-llama/llama-4-scout-17b-16e-instruct` 
- Have the LLM process each story from `stardem_sample.json`
- Have the LLM assign each story the single best-fitting topic from `topic_list`
- Have the LLM save the updated stories to `stardem_topics_classified.json`
- Print progress as it processes stories

GitHub Copilot: ````python
import json
import subprocess

SAMPLE_JSON = "stardem_sample.json"
OUTPUT_JSON = "stardem_topics_classified.json"

# Define the topic list with definitions
topic_list = [
    {
        "topic": "Local Government",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss the members and actions of a local government, including mayors and mayoral candidates, town boards, and town or county councils."
    },
    {
        "topic": "Economy & Budget",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss the finances and economy of a municipality."
    },
    {
        "topic": "Planning & Development",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss planning, zoning or municipal development."
    },
    {
        "topic": "Housing",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss housing, including affordable housing, homelessness and new housing developments."
    },
    {
        "topic": "Transportation, Infrastructure & Public Works",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss transportation, infrastructure or public works at the municipal level, including public transportation, roads and bridges, and public sewer, electricity and water services."
    },
    {
        "topic": "Public Safety & Crime",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss public safety, municipal crime, local police or legal cases."
    },
    {
        "topic": "Arts & Society",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local community and culture, including restaurants, performances, art, music, fairs and other public events."
    },
    {
        "topic": "Education",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss primary or secondary education at the local level, including municipal school systems, curricula and funding."
    },
    {
        "topic": "Environment",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss environmental topics, including pollution, ecosystems, conservation and the Chesapeake Bay."
    },
    {
        "topic": "Community Outreach",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss municipal social programs, including food drives, vaccination drives, free mental health screenings and other public benefit initiatives."
    },
    {
        "topic": "Elections",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local elections, including mayoral elections, town or county council elections and town or county board elections."
    },
    {
        "topic": "Agriculture",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local agriculture and aquaculture, including fishing, crabbing and farming."
    },
    {
        "topic": "Sports",
        "definition": "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss local sports, including youth sports, high school sports and athletic infrastructure."
    }
]

# Load stories, keeping only title and content keys
with open(SAMPLE_JSON, "r") as f:
    raw_stories = json.load(f)
    stories = []
    for s in raw_stories:
        story = {}
        if "title" in s:
            story["title"] = s["title"]
        if "content" in s:
            story["content"] = s["content"]
        if story:  # Only add if at least one key exists
            stories.append(story)

classified_stories = []

for idx, story in enumerate(stories, 1):
    title = story.get('title', '').strip()
    content = story.get('content', '').strip()
    if not title and not content:
        continue

    # Build topic list string for prompt
    topic_prompt = "\n".join(
        [f'- {t["topic"]}: {t["definition"]}' for t in topic_list]
    )

    prompt = f"""
Assign this news story to exactly ONE topic from the following list, using the definitions provided:

{topic_prompt}

Choose the topic that best represents what this story is primarily about.

Title: {title}
Content: {content}

Return only the topic name from the list above.
"""

    try:
        result = subprocess.run(
            [
                "llm",
                "-m", "groq/meta-llama/llama-4-scout-17b-16e-instruct",
                "--no-stream"
            ],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True
        )
        topic = result.stdout.decode("utf-8").strip().splitlines()[0]
    except Exception as e:
        topic = "Other"
        print(f"Error classifying story {idx}: {e}")

    classified_stories.append({
        "title": title,
        "content": content,
        "topic": topic
    })
    print(f"[{idx}/{len(stories)}] Classified: {title} -> {topic}")

# Save results
with open(OUTPUT_JSON, "w") as f:
    json.dump(classified_stories, f, indent=2)
print(f"\nSaved classified stories to {OUTPUT_JSON}")
````
