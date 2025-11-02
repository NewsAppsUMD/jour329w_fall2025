import json
import subprocess

SAMPLE_JSON = "stardem_sample.json"
OUTPUT_JSON = "stardem_topics_classified_2.json"

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
        "topic": "Columns, Editorials & Letters to the Editor",
        "definition": "Columns, editorials and letters to the editor."
    },
    {
        "topic": "Other",
        "definition": "Last-resort classification of other content that doesn't fall under another category."
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
                "-m", "groq-kimi-k2",
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