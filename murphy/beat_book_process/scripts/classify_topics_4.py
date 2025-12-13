import json
import subprocess

INPUT_FILE = "stardem_sample.json"
OUTPUT_FILE = "stardem_topics_classified_4.json"
MODEL = "groq/meta-llama/llama-4-maverick-17b-128e-instruct"

def build_prompt(title, content, used_topics):
    # If any topics have been used, tell the LLM to use the same name if it fits
    topic_hint = ""
    if used_topics:
        topic_hint = (
            f"\nIf you have already used a topic name for a similar story, use the same topic name for consistency. "
            f"Topics used so far: {', '.join(sorted(used_topics))}."
        )
    prompt = f"""
You are a news classifier.

Given the following story, assign a primary_topic field: a 1 or 2-word broad topic that best describes the primary focus of the article, based only on its title and content.

- Be consistent: if you have already used a topic name for a similar story, use the same topic name.
- Return only the topic name as a single string, no extra text.

Title: {title}
Content: {content}
{topic_hint}
"""
    return prompt

def classify_primary_topic(story, used_topics):
    prompt = build_prompt(story.get("title", ""), story.get("content", ""), used_topics)
    try:
        result = subprocess.run(
            [
                "llm",
                "-m", "groq/meta-llama/llama-4-maverick-17b-128e-instruct",
                "--no-cache",
                "--no-stream"
            ],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        topic = result.stdout.decode("utf-8").strip().splitlines()[0]
        # Clean up any extra quotes or whitespace
        topic = topic.strip().strip('"').strip("'")
        if topic:
            used_topics.add(topic)
        return topic
    except Exception as e:
        print(f"Error classifying story: {story.get('title','')[:60]}: {e}")
        return "Other"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        stories = json.load(f)

    used_topics = set()
    updated_stories = []
    for idx, story in enumerate(stories):
        print(f"[{idx+1}/{len(stories)}] Processing: {story.get('title','')[:60]}")
        topic = classify_primary_topic(story, used_topics)
        story["primary_topic"] = topic
        updated_stories.append(story)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_stories, f, ensure_ascii=False, indent=2)

    print(f"Classification complete. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()