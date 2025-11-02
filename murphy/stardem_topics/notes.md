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

i tried to troubleshoot a bit, but that didn't really get me anywhere, so i rewrote my copilot prompt:

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

copilot gave me what is now `classify_topics_1.py` and i eventually i got to what is in `starmdem_topics_classified.json`. it worked fairly well, honestly. but the funny thing is ... i can't replicate that. not with that script anyway. i've rerun it and it will not produce the same results — it classifies the first three and then fails.

note that getting this — even if i could only get it once — required telling it to ignore every field except title and content. this has a downstream effect that i did not consider, which was that it didn't know what *section* the article was published in. see, i tried to get it to classify based on all metadata, but it freaked out every single time and gave me "other" for every single article.

it was ok — better than i expected, to be honest — but it was far from perfect. it categorized "EDITORIAL: 10-cent paper bag fee should be optional" as "Environment," for example. now, is that *wrong*? i suppose not. but it's also not what i would want it classified as given that it's an editorial. again, i didn't consider the downstream effect of not including "section." but there were some other just flat-out wrong or weird ones: "SPRING TRAINING GLANCE 3-10-24" was classified as "Sports." all the "Today in History" ones were classified as "Columns & Editorials," which ... no. i appreciate that it tried and probably got maybe 40-50% right?

i screwed with the script some more (check the chat log, i went back and forth with it) and added some new topics/changed some definitions. i changed the model, too, to groq-kimi-k2, and ran the script in `classify_topics_2.py`. 

i will say, this script was really good at getting it to classify public safety stories. pretty terrible at the random non-news stuff, like tv listings and today in history.

## copilot chat log 
