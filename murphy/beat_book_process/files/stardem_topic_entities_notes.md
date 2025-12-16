# star-dem topic entities — cat murphy, nov. 10

ok, well, the first thing i was drawn to was local government ... it's usually the first thing i'm drawn to because i love covering local government, and i'd argue that it's probably the single most important coverage area for the star-dem. and, after scanning a few entries, i also suspect that the coverage is going to be all over the place. i mean, if there were any topic in need of subtopics, it's local government, right? that can encompass anything and everything from development and budget to public works and environment. and, evidently, you didn't separate out elections, so that too, i guess? then add in the editorials and letters to the editor ... i mean, it's a sprawling category with a lot going on.

so, with that said, i decided to go with education. honestly, it's a part of government, is it not? a lot of the coverage is going to be about education funding, staffing, legislation, etc. — all of which involves the government/politics side of things. (i do then question how much overlap there is, and if there are any relevant education stories that were put with local government.) case in point, local government is a secondary topic in nearly 400 of the education stories ... so, you know, most of them. and education is a secondary topic in 113 of the 1324 local government stories. now, the education stories are definitely still a little all over the place — i mean, there are 24 stories where the confidence score is below 0.7 because they have titles like "Decline in social capital has reached new lows" and "Local seniors inducted into hall of fame." but the topic is more manageable size-wise, without being too small, hence why i went with it.

#### updates

i'll note that it took so long to classify these that i had to use two different models (`groq/moonshotai/kimi-k2-instruct-0905` and then `groq/openai/gpt-oss-120b`), and i only got thru ~half of the entries.

kimi-k2-instruct-0905 was so slow, and i got rate-limited twice. gpt-oss-120b was fast...er. but it still took forever. i never got to a complete script modification because it just took too long, and i am too neurotic to let it finish when i see flaws, so i repeatedly stopped and edited as i went.

the main prompting things i did were for consistency and concision purposes — i had copilot edit the script to direct the llm to standardize names/titles and to stop pulling unrelated entities and unrelated events or flat-out non-events. this had downstream consequences because it excluded things, but there was too much irrelevant metadata before, and i think it will be easier to do the equivalent of select() instead of -select() — does that make sense?

#### accuracy

i'm actually pretty impressed with the accuracy of my updated prompt — it was, from what i looked at, pretty good at extracting the entities without extracting extranneous data. it didn't start like this — at first my prompt was only vaguely referencing "important" people, but because there's only one topic i was able to be very specific about the types of people i was looking for. superintendents, board presidents, etc. 

there were more false negatives than false positives, at least that i noticed. the downside of my uber-specific prompt was some things weren't extracted, like the name of the mayor, because they weren't explicitly "education-related". there were a couple people that got excluded otherwise, as well, like in one case the vice president of the education board — i'm almost positive it's because the title used in the article was "Board Vice President," meaning the education part was inferred but not explicit. in another case, someone was referred to as just a "board member," so it didn't classify him, despite having classified him in other stories. i looked at some of the more prevalent names, and it seems like this was a not-insignificant issue that would need to be addressed in my next script. generally speaking, though, the entities it did pull were spot on. there were just some syntax things that, because of the rigidity of my prompt, created some false positives.

#### quality

i had a version of a script (when i was pulling ~10 at a time to test it) that was inconsistent in its spelling/phrasing of things. the main one was the difference between "Kent County" and "Kent," things like that. but i had copilot address it in the script so that it had more specific directives on standardization. this worked ... most of the time. the most common ones were the people for whom it pulled the correct name and title, but sometimes did "Sharon Pepukayi (Superintendent of Talbot County Public Schools)," while other times doing "Sharon Pepukayi (Superintendent, Talbot County Public Schools)." again, a syntax mismatch but an infuriating one. i think i needed to be more specific as to how to format the titles — in retrospect, i'm realizing i did not give it an output format because the test runs were giving good results. 

as for places, the structure of my prompt made it so that my county and municipality fields were entirely consistent. from what i could see, every "Easton" was the same, every "Talbot County" was the same, etc. and it seemed to get at least the majority of maryland municipalities mentioned in each story, which was cool. again, i credit my uber-long county list. it was almost always spot-on. i will say that i added a "regions" field to find stories that talk about other states, because some of them are about maryland AND other things, and this ... was hit or miss. a lot of the examples were, like, a teacher gets an award and she served on some board in Delaware in the past, so Delaware was extracted as a region. i specifically told it to exclude those kinds of locations, and it was relatively good at that when it came to organizations, bodies, institutions, etc., but the regions field was more iffy. it wasn't a top priority, so idk if i would even fix it. the locations field was also meh. the idea worked more with stories that weren't specific to one topic, and i think it was generally more applicable to non-education stories. so it was a lot of relatively niche information, or just places that were already in another field.

i found organizations, like places, to be far too broad a category, so i also split it up. i asked for key events, key intiatives, key establishments, key organizations and key bodies. my thinking was that "events" and "initaitives" are *things* i want to know about, "establishments" are *places* i want to know about, and "organizations" and "bodies" are non-government and government institutions, respectively, that i want to know about. this worked ... most of the time. the issue i ran into with some of them was that school districts would be classified as "establishments" and bodies would be classified as "organizations." that being said, it seemed to get all of the important entities, they were sometimes just in the wrong field within my organization data. so, otherwise, i mostly liked how this turned out. for example, for one story i got "Blueprint for Maryland's Future" as a key initiative, "Empowerment Academy" and "Rising Sun Academy" as key establishments, "Maryland Association of Secondary School Principals" and "Maryland Education Coalition" as key organizations and a slew of government agencies and school boards — "Blueprint Accountability and Implementation Board," "Maryland General Assembly," "Maryland State Department of Legislative Services," "Dorchester County Public Schools," etc. — for bodies. that's what i was going for, and it seemed to work out most of the time.

#### patterns

the most frequently mentioned people in my data (though this only accounted for roughly half of the stories overall) were:
- Sharon Pepukayi, superintendent of Talbot County Public Schools (7)
- Emily Jackson, president of Talbot County Board of Education (7)
- Dr. Derek Simmons, superintendent of Caroline County Public Schools (6)

organizations:
- Maryland Association of Secondary School Principals (5),
- Chesapeake Forum (5)
- MISCLASSIFIED: Maryland State Department of Education (4)
- MISCLASSIFIED (though this is more understandable): Maryland Association of Boards of Education (4)
- Moms for Liberty (3)

bodies: 
- Talbot County Board of Education (21)
- Caroline County Board of Education (21)
- Maryland General Assembly (19)
- Dorchester County Board of Education (16)
- Talbot County Public Schools (11)

municipalities:
- Easton (98)
- Denton (34)
- Cambridge (27)
- St. Michaels, Chestertown and Centreville (16)

counties:
- Talbot County (111)
- Caroline County (54)
- Dorchester County (41)
- Queen Anne's County (39)
- Kent County (33)

these patterns definitely make sense — talbot and caroline county and their related entities dominate the lists. the consistency of those results is actually reassuring, because it says to me that it accurately and consistently extracted the entities across the board. the organizations one is kind of bleh, but that's not really all that shocking.

#### improvements

well, i'm pretty happy with mine overall. the main changes i would make would be to cut the organization field and combine it with bodies. the split made sense with the larger dataset, but it doesn't really execute the way i want it to here, and it's just a lot of duplicates, to be honest. i'd also probably ditch the location field for the same reason. it just didn't work with this subset of data because the locations were the establishments: schools. so, yeah. i would think about maybe trying to classify stories based on legislation, board meetings, etc — idk, it seems like it might be helpful to know which stories were specifically relevant to initiatives or meetings or events, etc. the most major change would be with the people field, i think, because it excluded people when their relationship to boards and schools were implied. so i would want to clarify 1) that it needs to look for public officials generally, 2) that if a person gets classified in one story, any other mention of them should be classified, 3) that there should be a standard format for titles and 4) that people's names must be standardized