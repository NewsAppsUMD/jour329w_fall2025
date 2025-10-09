# cns more datasette — cat murphy, oct. 8

## keywords

### Do the results make sense?

make logical sense? usually. make practical sense? not really. like, for a story about a cargo ship stuck in the chesapeake, "Cargo Salvage" definitely makes *sense*; for a story about oyster population restoratiion, i guess "Bay Filtration" makes *sense*. but those aren't *useful*. but that in and of itself makes sense. the prompt was incredibly vague. the last time we did this, i had to tell it this:

```
list five umbrella categories that describe the main focus of the story, using one word for each if possible and a maximum of two words if necessary. use only terms that could be used as tags to categorize stories on a website, remembering that news consumers search primarily for broad categories like news, politics or sports, and typically not for specific or niche terms. only include topics that are nationally relevant or relevant to marylanders. each output should be simple enough that an average tenth-grader might research it for a school project, and broad enough that a general news publication in maryland would publish at least 10 stories annually that would fall under that category.
```

and even that was by no means perfect, but the outputs were far less variable. so i think this speaks more to the necessity of good prompts that clearly iterate the request. i guess what i'm saying is that i don't necessarily *blame* the llm for generating logically sensical but practically useless keywords. i did notice, though, that when the tags were accurate and useful, they still weren't necessarily the *most* useful. like, for a story about how the shutdown is impacting the chesapeake, "funding freeze" was listed ... but not congress or trump or shutdown. 

### Any surprising patterns?

i honestly thought the formatting thing was super weird. no formatting, bullets, dashes, numbers, back to no formatting, back to numbers. it's bizarre. and i know that we talked about how each row hits the api separately, meaning the outputs are independent of one another. but still. i guess it shouldn't be surprising to me at this point that ai is inconsistent, but the lack of a standarized response format with the same prompt on the same set of data — i mean, it's weird.

### Anything you don't like about this?

well, i hate that it doesn’t listen. like, it’d be one thing if it did something that i didn’t want BUT that i never specified in the prompt. but like, i told it to give me “up to five.” that is so clear. so the inability to trust it to follow simple, clear instructions makes me cautious, even skeptical. and i know that this is, you know, a known issue — it definitely doesn’t surprise me or anything. but this was a short prompt. a vague one, sure. but the fact that we have to be so careful about being so clear about how many outputs to list, the fact that we have to specify that it should use one word unless absolutely necessary — it’s just irritating and makes me worry i’ll miss something if i’m not manually checking every output.


## semantic search 

### What words or phrases did you try?

1. `transit`

2. `corruption`

3. `homes`

4. `cars`

### Do the results make sense?

at first, i was pretty impressed. the top three stories for `transit` were about high speed rail (24%), a pipeline (21%) — it mentioned "transcanada," though, so i get it — and sailing (20%). pretty good! 

the next one, `corruption`, was a little less impressive. the *most similar* story was about wes moore's "unique perspective," with a 17% similarity rating. the next two weren't better — one was about literacy (16.9%) and the other was about craft brewery regulations (16.7%). so ... yeah. 

then i did `homes`. this one was just like ????? the first result, with a *33%* similarity rating was MERRILL COLLEGE CAPSTONE CLASS DESCRIPTIONS (https://cnsmaryland.org/2025/02/25/81648/). at first, i was like, ok, well one of the tags is "state house," which i guess would ... kind of explain part of it? but now that i'm thinking about it, i'm realizing that maybe it has something to do with it being a *home page*? maybe? idrk. and `cars` went equally as strangely — the first result was about a stunt artist (23%). 

so i don't know. because most of the results had relatively low similarity ratings (except the `homes` one, lol, that was weird). my general opinion is that the results make sense *given that it didn't have much to go on*. and again, it's not like it claimed a governor-elect's "unique perspective" was equivalent to "corruption." i just think this would probably be far more helpful with more data — both in terms of volume and completeness. 

### Anything you don't like about this?

ok, well, i think my biggest thing is that i don't know how good of a representation this particular usage of semantic search is. like, it was pretty impressive for some things, but it was perplexed by others. and i think this mostly has to do with the volume of data it's pulling from, right? like, if we were analyzing the easton articles, there would be a lot more embeddings to perform a semantic search against. here, it kind of felt like none of the articles were all that similar to begin with, so performing a semantic search was pushing it. that being said, i do nevertheless think this has the potential to be exceptionally helpful, if only in some circumstances. and of course, i recognize that this isn't a perfect system in any situation — it's a tool. so while i was kind of disappointed, i also don't know that i necessarily consider this experience illustrative. tl;dr: i want to use it on a larger dataset before i give you a better answer about what i do or don't like. 