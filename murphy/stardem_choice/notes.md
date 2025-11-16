# stardem choice — cat murphy, nov. 12

### choice

well, to be clear, i kind of did ... both? i liked my enhanced stories, but i wanted slightly cleaner metadata, and i wanted more of it. 

so, first, i merged all education-related stories from the other topic .json files — mostly because education appeared quite frequently as a secondary topic in the other files, and some of them were definitely relevant (mainly local government stories about budgets, but also a fair number of health and public safety stories). i also defined a confidence score cutoff for education stories — it must be < 0.8 for stories where the primary topic was education and < 0.65 for stories where the secondary topic was education). then i reran my script on all 779 entries, getting rate limited so many times over the course of three days that i now have six groq accounts. a few failed, usually for syntax reasons/the content was too long, and a bunch got duplicated, so i ended up with 754 unique entries.

but i only did this because i wanted to have as much data as possible for a beatbook. 

ok, and while i ran that, i wrote two scripts: the first was to process my enhanced .json with entities and parse out stories that would be irrelevant to a beat book (which i defined as non-news stories, stories not relevant to the five covered counties and stories not relevant to boards of education, public officials, funding, etc.). i had it batch run and base its decisions only on the titles and extracted metadata, and for the most part the script did pretty well. it eliminated like 2/3 of the entries — which is about what i expected. there were some false positives and false negatives, but the selected data seemed pretty good.

i also used that time to write v1 of my beatbook generation script. i gave chatgpt a list of my metadata fields (no stardem content) and a couple general pointers on about what the beatbook was for and asked it to generate a beatbook script based on your example (chat log: https://chatgpt.com/share/6918d97e-5d48-800c-890b-bdc2e50300de).

### experimental design

#### what input combinations did you test (entities only, entities + summaries, etc.)?

my first script said to use the entity metadata only as context and to primarily base its output on the story content. i was a little nervous, considering just how much metadata i have for each story, that this was going to fail. even with only 278 stories, it did hit the token limit for `meta-llama/llama-4-maverick-17b-128e-instruct`. HOWEVER, it didn't fail with `openai/gpt-oss-120b`, so i ran it with that.

given the length of my first draft, i asked copilot to do the following to build a second script that:
- Simplifies and shortens the output. Maximum of three paragraphs per issue. No "why this matters" sections for sources. Create a consolidated list of data/documents instead of by county.
- Uses groq/qwen/qwen3-32b BUT strips out the content in the <think></think> tags
- Only uses titles and metadata

i was 100% expecting this to bomb, because i really didn't think that would be enough info.

it actually did better than i thought, but i added summaries to my data in order to rerun the script a third time and see if there was a happy medium.

#### how did you structure your prompts?

"i" (chatgpt) structured my first prompt to be incredibly specific — to the point that i kind of worried it had too many rules and would max out the llm's abilities lol. i asked it to generate a beatbook with three main things, broken down by county: the top three education-related issues, a list of key sources and a list of key documents. for the issues section, the prompt asked for 1–3 paragraphs of narrative prose per issue based primarily on the full story content, and it clarified that it could not use bullets and it had to make the writing "feel like a newsroom beat memo for a reporter." chatgpt also defined a pretty specific formatting structure and gave it some examples of who/what to include as key sources and documents. notably, it wasn't super specific about what the issue summary should look like, which i didn't love, so i actually changed it to 3-4 paragraphs of narrative prose "that lay out and contextualizes what an education reporter needs know."

my other prompts (edited as explained above) remained largely the same structurally.

### generation quality assessment

#### which types of content generated well? which didn't?

for my first one, the data/documents/records section was honestly pretty good. i mean, it included 8-11 CATEGORIES of records per county — the issue with that, of course, is that it definitely contributed to why the beat book was so long. and it occasionally repeated itself. lowkey, though, i didn't even know some of these datasets and records existed, and/or i wouldn't have thought to check them. the thing that irritated me was not the lists themselves but the inclusion of a "why it matters" statement under *every single one*.

the key source section was less impressive. to be fair, it wasn't all bad — i got outputs like this: 

```md
- **Richard Barton – Board President**  
  *Sets board agenda, presides over meetings, and champions fiscal stewardship.*  
  *Reporter hook:* Comments on board approvals (e.g., textbook adoption, calendar changes) and community reactions.

- **Amy Towers – Supervisor of Instruction**  
  *Directs curriculum decisions, teacher professional development, and AP program expansion.*  
  *Reporter hook:* Explains instructional policy shifts, textbook selections, and AP enrollment strategies.

- **Mark Jones – Vice President, Board of Education**  
  *Assists the President and often serves as spokesperson for board initiatives.*  
  *Reporter hook:* Provides quick responses on board votes, policy updates, and public‑meeting logistics.
```

and when it looked like this, i kind of liked the little blurbs about their positions. not sure how i feel about the "reporter hook." it was mostly just kind of repetitive.

the main issue was that i also got some of this:

```md
- **Easton Elementary School – Principal (on‑site contact)** – Front‑line voice on first‑day experiences, enrollment spikes, and parent‑community engagement. Ideal for human‑interest pieces and day‑to‑day operations.  
- **Easton High School – Principal** – Oversees secondary‑level implementation of Blueprint initiatives, AP course expansion, and career‑technical pathways. Source for high‑school achievement data and graduation‑rate discussions.  
- **Chapel District Elementary School – Principal** – Currently navigating a major renovation; can discuss design plans, state review process, and construction timelines.  
```

```md
- **Principal, Kent County High School**  
  – Oversees secondary curriculum, CTE programs, and facility needs (e.g., new middle‑school planning).  
  – Source for student‑performance data, program enrollment, and capital‑project impacts.

- **Principal, Lockerman Middle School** – Insight on middle‑grade challenges, especially science‑instruction gaps highlighted in MCAP results.
```

like, yeah, thanks. would have loved their ... you know, names? also, wes moore was in there a lot. lol. 

for my second one, the output was more succinct (*only* 16 pages this time), but for the most part it focused on the exact same issues and people. it was also more repetitive because it wasn't using the article content. for example, the pandemic was a central issue for basically every county, but the lack of specific information meant that the summaries all looked relatively similar. that being said, it was considerably better than i had expected it would be given that it didn't have nearly as much information. the key documents section here was better in the sense that it consolidated the list, but it left out some of the more interesting ones i saw in the first version, which was a little disappointing.

ALSO, the reduction in available information meant that it narrowed in on some really specific sources that definitely are not that important. for example, for queen anne's, it said these were key sources:

```md
- **Queen Anne’s County Board of Education** – Approves food service contracts (e.g., Sysco), curriculum changes (e.g., social-emotional learning grants), and school infrastructure projects.  
- **Julie Hickey** – Coordinator of Food Services, Queen Anne’s County Public Schools, manages school lunch/milk pricing and nutrition programs.  
```

like, uhhhh? 



#### how accurate was the generated content compared to the source stories? did the LLM hallucinate information not in the stories?

from what i can tell, it actually did a relatively ok job. by "relatively ok job," i mean that it was 42 pages long and i can only read so much of it. most of the figures and statements i was able to check were accurate, and what i appreciated was that the information was actually broken down by county, even when the overarching topic was the same. this is somewhat minor, but my first draft spelled talbot county as "talton" county and "talark" county a couple times, lol.

however, there are instances where the information is *misleading* or ... at least, it's kind of confusingly worded:

kent county:
```md
Kent County’s academic outcomes are increasingly a cause for concern, as reflected in the latest Maryland Comprehensive Assessment Program (MCAP) data. While statewide English proficiency has rebounded past pre‑pandemic levels, Kent remains one of the few counties where math scores have slipped further, registering a decline from 2022 to 2023. More alarming is the steep drop in eighth‑grade science proficiency, which fell to a five‑year low of 26 percent, mirroring a broader regional trend but disproportionately affecting Kent. The state attributes the science dip to disrupted middle‑school instruction during the pandemic, yet the local impact is evident in classrooms where teachers are still grappling with gaps in foundational concepts.
```

the part about the county's eight-grade science proficiency is (kind of) misleading — the statewide proficiency rate is 26%, which is the lowest in five years. kent's isn't specifically mentioned, though it is noted that the county's proficiency rate in 2023 was over 30% lower than in 2022. like, it's not wrong, it's maybe just a little confusing as to what is statewide and what is kent-specific.

the second draft seemed to avoid doing this, but i would put that more on the fact that it was going only off titles and metadata.

as far as hallucinations, my first draft hallucinated a handful of links — tcps.org, uppershorewib.org, kent.k12.md.us — but managed to get some correct, mainly the major state websites, like mgaleg.maryland.gov. and to be honest, i *thought* the first one was hallucinating some of the names because i kept seeing things like "mark jones" and "sarah jones" — but no, i checked, those really are their names lol. the second one also didn't seem to hallucinate (at least, not in any major way that i could tell)

the main issue i did see was not necessarily with the "accuracy" of the content, so to speak, but more with the dating. it didn't seem to have any comprehension of time or chronology, which meant things were out of order and at times just completely wrong. i tried to address this with my third prompt, but then qwen couldn't distinguish between the counties and started giving completely unhelpful summaries. when i fed that prompt to open ai's `gpt-oss-120b` model, though, it did pretty well.

### input effectiveness

#### did providing just entities work, or did you need story content too? how much context did the LLM need to generate useful content? what was the optimal amount of input to provide?

providing just entities and titles "worked" in the sense that it wasn't the worst thing i've ever read and it wasn't completely useless. like, i wouldn't say it was ideal by any means, but it wasn't, like, inaccurate or entirely unhelpful or anything. that being said, it generated detailed county-level information in a way it couldn't before when it had the story content available.

trying to split the difference, i added summaries to all my data and gave it back to qwen. the output was 21 pages — so, an in-between compared to the 16-page no-content and 42-page full-content versions.  

it seemed like this was the happy medium, though i would maybe try to expand the summaries to, like, 75 or 100 words, maybe.

#### did entity lists help focus the generation?

absolutely. there's no way the model could have written a beatbook using only the titles. i will note that having *good* extracted metadata helped immensely. one example of this was when people were mentioned in the titles by their last names only, the entity lists allowed the llm to identify their full names. having those lists also helped it weed out *unimportant* figures and organizations that it should not focus on while generating the beat book.

### model comparison

#### did you try multiple models? how did they differ?

well, the token limit on `meta-llama/llama-4-maverick-17b-128e-instruct` was too low to process my full .json of selected stories.

`openai/gpt-oss-120b` was able to process the entire file, and it gave me a 42-page beat book on the first try. uh, so yeah. the content was mostly ok, but it unsurprisingly got a little lost in the sauce at times.

`qwen/qwen3-32b` did a really great job the first time, especially considering that it was only using the titles and metadata because its token limit was too low to process the full file. actually, it did well enough that i created a new script to add 50-word summaries to `selected_processed_stories.json` so that i could feed it more info without hitting its token limit (hopefully). and while i didn't hit the token limit, i was not very pleased with the results. it was all over the place — it couldn't really distinguish the counties very well, even with really good metadata, and gave me stuff like this: 

```
The 2024–25 MCAP test results, released in August 2025, exposed stark academic disparities across Queen Anne’s County. Dorchester County schools saw a 3-point proficiency rise in math, while Caroline County plummeted 2 points, and Kent County flatlined. 
```

and no, it did not ever go back to QA, lol. it usually seemed like its summaries were dominated by coverage of larger counties — as in, when it didn't know what to say for a smaller county, it was pull from the others. i liked the random inclusion of "规划建设" — "planning and construction" — though.

so, i went back to my bestie, `openai/gpt-oss-120b`, to see how it did with less detailed data and a more succinct, more specific prompt. i got a little worried after running my third prompt with qwen that open ai's model wasn't going to work either, but it actually did really well, spitting out a 19-pager that was substantive without being surface-level too dense.

#### which model produced the most useful beat book content? ere certain models better for specific types of sections?

`openai/gpt-oss-120b`, hands down, across the board. i mean, let's give it credit for being able to handle the entire selected stories file and generate 42 pages of content in one go. that alone was kind of crazy, particularly because i LIKED that draft. it wasn't perfect, of course, but it was also my first attempt.

qwen's `qwen3-32b` model did well enough with just the entities and titles, but it really got lost in the sauce when i added summaries. `gpt-oss-120b` didn't do me dirty like that. nineteen pages of relevant issue descriptions, source lists and documents/data to get.

compared to qwen across every prompt, the issue summaries were better, the source lists were better and the document lists were better.

### beat book utility

#### what sections worked best for a beat book?

i really liked having issue sections as well as source and record information. i don't know that the issue narratives alone provide enough structure to visualize who's who and where to get stuff in the same way lists do, but i also don't think issues should be broken down into bullets — hence both. the main thing as far as sectioning goes is actually that it needs to be broken down by county. notably, though, the records section should *not* be broken down by county ... as i found out. 

#### what would need human editing or verification?

- cited figures
- links
- mentions of dates (last october, next march, etc.)
- currency (election results, vacancies, lawsuits, unpassed legislation, etc.)
- spellings (talark county public schools)

#### what's missing?

as i'm thinking about it, i'm realizing that one thing i'm missing is citations. it would be impossible to fact check these without a way to track where the information is from. i mean, it should be easy enough to have it cite row #s.

i also think, at least for the education beat, it's probably important to have a section dedicated to statewide issues. i say this only because post-pandemic academic recovery was a key issue in every county, and the sections were immensely repetitive. same for the blueprint program rollout. it's probably worth it to have a section dedicated to issues affecting the entire state, with stats by county, and then hyper-specific issues can go into the county-level issue sections.

### lessons learned

#### what surprised you about LLM-generated beat book content?

honestly, the quality floored me. i didn't really have any expectations going in because, well, i wasn't exactly sure how this was going to turn out. i mean, i didn't think they were going to be terrible, but i was expecting my first draft to be overly broad and short, not overly specific and 42 pages long. granted, my only point of reference was the first time we tried to do this, when everyone got three pages of bullet points. admittedly, i'm a little more clued in on a) what we're looking for and b) how to design a good prompt. but still, i was impressed.

#### what's the best use case for automated beat book generation?



#### where does human judgment remain essential?


#### how would you improve your approach?

less neurotic.
