import json
import subprocess

SAMPLE_JSON = "stardem_sample_2.json"
OUTPUT_JSON = "stardem_topics_classified_5.json"

content_type_list = [
    {
        "content_type": "News",
        "definition": "Full articles, excluding calendars, obituaries, legal notices and opinion pieces, meant to inform, not persuade, readers on news topics such as politics, elections, government, agriculture, education, housing, economy and budget, transportation, infrastructure, public works, public safety, crime, environment, arts, society, community and sports."
    },
    {
        "content_type": "Calendars",
        "definition": "Calendars."
    },
    {
        "content_type": "Obituaries",
        "definition": "Obituaries."
    },
    {
        "content_type": "Legal Notices",
        "definition": "Legal notices."
    },
    {
        "content_type": "Opinion",
        "definition": "Columns, editorials, letters to the editor and any other opinion-based pieces for which the primary purpose is to persuade, not necessarily inform, readers."
    },
    {
        "content_type": "Miscellaneous",
        "definition": "TV listings, Today in History articles and other non-news and non-opinion content."
    }
]

topic_list = [
    {
        "topic": "Local Government",
        "definition": "Articles that center around and primarily discuss the members and actions of a local government, including mayors and mayoral candidates, town boards, and town or county councils."
    },
    {
        "topic": "Economy & Budget",
        "definition": "Articles that center around and primarily discuss the finances and economy of a municipality."
    },
    {
        "topic": "Planning & Development",
        "definition": "Articles that center around and primarily discuss planning, zoning or municipal development."
    },
    {
        "topic": "Housing",
        "definition": "Articles that center around and primarily discuss housing, including affordable housing, homelessness and new housing developments."
    },
    {
        "topic": "Transportation, Infrastructure & Public Works",
        "definition": "Articles that center around and primarily discuss transportation, infrastructure or public works at the municipal level, including public transportation, roads and bridges, and public sewer, electricity and water services."
    },
    {
        "topic": "Public Safety & Crime",
        "definition": "Articles that center around and primarily discuss public safety, municipal crime, local police or legal cases."
    },
    {
        "topic": "Arts & Culture",
        "definition": "Articles that center around and primarily discuss local community and culture. This includes features on local businesses, restaurants, food trucks, performances, art, music, fairs and other public events, as well as news articles about municipal social programs, such as community food drives, free mental health screenings and other public benefit initiatives."
    },
    {
        "topic": "Education",
        "definition": "Articles that center around and primarily discuss primary or secondary education, including municipal school systems, local colleges and universities, curricula and funding."
    },
    {
        "topic": "Environment",
        "definition": "Articles that center around and primarily discuss environmental topics, including pollution, ecosystems, conservation and the Chesapeake Bay."
    },
    {
        "topic": "Elections & Politics",
        "definition": "Articles that center around and primarily discuss politics and elections, including political disputes and elections for mayor, town or county council and town or county boards."
    },
    {
        "topic": "Agriculture",
        "definition": "Articles that center around and primarily discuss local agriculture and aquaculture, including fishing, crabbing and farming."
    },
    {
        "topic": "Sports",
        "definition": "Articles that center around and primarily discuss local sports, including youth sports, high school sports and athletic infrastructure."
    }, 
    {
        "topic": "Other",
        "definition": "Last-resort classification for content that does not fall under another clearly defined topic."
    }
]

def build_prompt(title, content):
    content_type_prompt = "\n".join(
        [f'- {t["content_type"]}: {t["definition"]}' for t in content_type_list]
    )
    topic_prompt = "\n".join(
        [f'- {t["topic"]}: {t["definition"]}' for t in topic_list]
    )
    return f"""
You are a local news classification assistant.

Given the following news story, do the following:
1. Assign a single content_type from this list (with definitions):
{content_type_prompt}

2. Assign a single primary_topic from this list (with definitions):
{topic_prompt}

3. If the content_type is "News" and the story is also very relevant to, but not primarily about, one additional topic from the topic list, assign a secondary_topic (maximum one, or "None" if not applicable). Otherwise, secondary_topic should be "None".

You must assign a content_type and a primary_topic, even if you are unsure. Do not leave any field blank. For the secondary_topic field, only assign a topic if the story is very relevant to it; disregard if the connection is tangential.

Return your answer as a valid JSON object with these keys: content_type, primary_topic, secondary_topic.

Examples:
- "Robbins YMCA opening reading hub to tackle childhood illiteracy" would be classified as "News", "Education", "Arts & Culture".
- "TV LISTINGS 7-19-24" would be classified as "Miscellaneous", "Other", "None"
- "Don't compare Trump to Hitler" would be classified as "Opinion", "Elections & Politics", "None"
- "BAAM Celebrates new Soccer Field and 20 Years" would be classified as "News", "Sports", "Arts & Culture"

Story:
Title: {title}
Content: {content}
"""

# Load stories, keeping only those with title or content
with open(SAMPLE_JSON, "r") as f:
    raw_stories = json.load(f)
    stories = []
    for s in raw_stories:
        title = s.get("title", "").strip() if "title" in s else ""
        content = s.get("content", "").strip() if "content" in s else ""
        if title or content:
            stories.append({"title": title, "content": content})

classified_stories = []

for idx, story in enumerate(stories, 1):
    title = story.get('title', '')
    content = story.get('content', '')

    prompt = build_prompt(title, content)

    try:
        result = subprocess.run(
            [
                "llm",
                "-m", "groq/meta-llama/llama-4-maverick-17b-128e-instruct",
                "--no-stream"
            ],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True
        )
        llm_output = result.stdout.decode("utf-8")
        # Try to extract the JSON object from the LLM output
        start = llm_output.find("{")
        end = llm_output.rfind("}")
        if start != -1 and end != -1:
            llm_json = json.loads(llm_output[start:end+1])
        else:
            raise ValueError("No JSON found in LLM output")
    except Exception as e:
        print(f"Error classifying story {idx}: {e}")
        llm_json = {
            "content_type": "",
            "primary_topic": "",
            "secondary_topic": "None"
        }

    classified_stories.append({
        "title": title,
        "content": content,
        "content_type": llm_json.get("content_type", ""),
        "primary_topic": llm_json.get("primary_topic", ""),
        "secondary_topic": llm_json.get("secondary_topic", "None")
    })
    print(f"[{idx}/{len(stories)}] Classified: {title} -> {llm_json.get('content_type','')}, {llm_json.get('primary_topic','')}, {llm_json.get('secondary_topic','None')}")

# Save results
with open(OUTPUT_JSON, "w") as f:
    json.dump(classified_stories, f, indent=2)
print(f"\nSaved classified stories to {OUTPUT_JSON}")