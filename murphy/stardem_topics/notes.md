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


