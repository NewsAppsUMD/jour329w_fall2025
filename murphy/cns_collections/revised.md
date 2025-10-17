# cns collections, part ii — cat murphy, oct. 16

## questions from yesterday (i got it to work w/ sports, finally) 

**what topic i chose:** sports

**how many stories:** 265

**key players**: 

well, i'm a little confused. there's one facet that has the array, and one that doesn't. if you just look at the non-array one, "[]" is the most common tag with 119 rows, and nothing else has more than two rows because it's all like this: ["Kal Miller", "Ethen Miller", "Alex Clemsen"]. but the array shows that john wall, the former washington wizards player, was the most frequently tagged actual person, with *eight* stories, then two cns students who did a podcast together, then patrick mahomes. quite a collection of people you got there, i must say. i just don't understand why they're both there. i don't remember that happening with any of the other stuff we did in datasette.

**geographic patterns:** 

again, it depends which one you look at. according to the non-array fact, other than "[]" (40), the top locations were maryland (22), washington (14) and then ... africa (17). (i had a feeling this might happen, because while watching the stories process, i noticed that there seemed to be a lot of stories about basketball in africa. so, yeah.) but the geography array facet shows maryland having 88 stories, washington having 50, baltimore having 38 and annapolis having 19 ... and africa having 17. again, i just dont understand why it's duplicated.

**institutional network**: 

based on the array facet, the most frequent key institution was "maryland" ... ok lol. next was umd, the capitals and the nfl.

**what the structured metadata reveal about this beat:**

well, i can tell you it reveals a lot about claude's ability to pull metadata. the thing is, i don't know if i can tell you what this does or doesn't reveal about the sports beat because i don't know that these metadata say anything even remotely helpful. it's so inconsistent to the point of uselessness. i really don't understand why it included separate columns for the array vs. the original .json. it's just weird. and there are some random tags that, even in the parsed arrays, still say "[]". it's also just very clear that the schema wasn't specific enough. the thing i noticed this with, in particular, was

i will say, though, that it did really well at tagging sports. it kept it to 32 categories, which was kind of impressive, considering that many of the other metadata facets had at least 100. also, i'm kind of proud of myself for the schema i wrote for "subcategory." i just wanted to see how it would do with giving stories, like, a topic within sports — "sports" is just so broad, and while it probably wouldn't be helpful for cns readers, it might be helpful on the back end to see what coverage areas within sports we tend to focus on. this one wasn't perfect, but it kept it to 90 subcategories, which i thought wasn't terrible. and a lot of them are the same thing — "NIL" vs. "NIL (Name, Image, Likeness)" vs. "Name, Image, and Likeness (NIL)" vs. "Name, Image and Likeness (NIL)" — or are too narrow and would need to be combined, but that i think would just need some cleaning up schema-wise. i saw similar things with the locations. like, rwanda and senegal could probably be slotted under "africa" given that it's a md-based publication, but again, it would obviously need additional instruction.

## today's questions

**does your prototype.md result seem useful? what does it do well and what does it not do well?**

the main thing i did was ask it to pick out 10 major coverage areas from the last five years and summarise how cns has covered those topics, then give a few ideas for follow-up reporting. i gave it background info, a response framework, guidelines and an exmaple. i used the anthrophic article you gave us as a guide for structure, which seemed to work pretty well. 

the topics it picked were fine, and the sumamries were fine — nothing all that special, but definitely passable. the biggest thing was the questions it came up with. the first time i ran it, they were garbage. after a couple tries, though, they weren't as bad. of course, some of them along the way, like "What role can basketball play in youth community development?" were contrived and dumb. but by the end i was getting summaries like this:

```
Our coverage primarily focuses on Maryland and nearby states, exploring the emerging landscape of high school athletes earning money through endorsements. We've examined the social, economic, and ethical implications of NIL for young athletes, highlighting stories from schools like DeMatha Catholic, Bishop McNamara, and others.

Our recent coverage is missing reporting on:
1. Long-term psychological impacts of NIL on youth athletes
2. Comparative analysis of NIL implementation across different states
3. Interviews with parents and coaches about their perspectives

Potential follow-up stories:
1. Mental health support for young athletes navigating NIL
2. How NIL might change recruitment strategies for colleges
3. Economic disparities in NIL opportunities across different communities
```

honestly, not bad.

the thing it sometimes sucked at — but i can't really blame it — was picking out what cns' "major" sports coverage areas. i mean, cns' sports coverage is all over the place, right? the .json makes it look like african basketball academies is a daily beat, so i can't really fault it for picking some out-there topics. overall, it did pretty well, but i also know some of the things it focused on were outlandish compared to what a human would write.

**did you change your prompt, and if so, how? did that work better?**

well, the first time i ran my prompt, it was 2,500 tokens too long — which makes no sense. and i didn't understand why this was happening at first, but every time i shortened it, it told me it was longer. then i realized my .json file was just enormous. so i shortened it down to like ~3,000 lines. then it actually ran my prompt lol. but here's the thing: while trying to figure out the token count thing, i shortened my prompt and didn't save the original version, which i spent lowkey a while working on. by the time claude actually ran my prompt, it was so much less detailed than my original one. so i did rewrite it, only to add back in some of the detail and clarity i had thought to include before. 

and it did help!! my latest prototype was (for this specific exercise) a good length, had the right amount of detail and provided a fair amount of food for thought as far as follow-ups go.

**what would you do differently with more time or data?**

still, i think it could do so much more. but, i mean, it took me a while to think of how i wanted to phrase this prompt — i know i could have used an llm to help, but i was in da zone. ideally, we would have far more data and more time to write a more specific prompt. for example, to get it to move away from the foreign reporting classes' work, i thought about adding a message like "hey, we're a maryland-based publication, so focus on stories that take place in maryland." but then that would exclude too many stories. in the context of an actual beat book, i would probably want more of a brief than a bulleted summary — there just wasn't enough here to warrant that, i don't think. so with more data and time, i would want to get it do more analysis rather than summarizing. like, i want it to be able to use a tool to go look at the article. i would want to use embeddings to sort articles by similarity. i would want to give it more specific instructions on what good follow-up reporting ideas look like. 
