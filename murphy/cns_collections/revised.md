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

**did you change your prompt, and if so, how? did that work better? what would you do differently with more time or data?**

well, the first time i ran my prompt, it was 2,500 tokens too long. i don't completely understand what happened next, but every time i shortened it, it told me it was longer.


cat prompt.txt enhanced_beat_stories.json | uv run llm -m claude-3.5-haiku > prototype.md