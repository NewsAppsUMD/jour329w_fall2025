Brendan Weissel 9/22/25

I chose to look at stories with the "Donald Trump" Tag. This tag has a totoal of 333 appearances on the CNS webpage. 

I chose the story titled "Pardoned Maryland Jan. 6 participants find support after convictions" that was published on May 9, 2025. 
Link: https://cnsmaryland.org/2025/05/09/pardoned-maryland-jan-6-participants-find-support-after-convictions/


1. I started out by using the given prompt to see what I would get.
uv run python -m newspaper --url=https://cnsmaryland.org/2025/05/09/pardoned-maryland-jan-6-participants-find-support-after-convictions/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "You are an expert at categorizing topics for news stories. Read the text and provide no more than 5 topics."

Answer: 

1. Jan. 6 pardons & post-pardon normalization  
2. Maryland GOP intra-party shift (Hogan → MAGA)  
3. Suburban “demographic anxiety” as radicalizing force  
4. Community reception: rural red pockets vs. urban blue counties  
5. Political violence & democratic-backsliding concerns

Not great for what we are looking for as we want 2 word tags. I did not ask for that specifically so let me try that.

2. uv run python -m newspaper --url=https://cnsmaryland.org/2025/05/09/pardoned-maryland-jan-6-participants-find-support-after-convictions/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "You are an expert at categorizing topics for news stories. Read the text and give me tags to describe the story that are two words are less. "

Answer: 
Jan 6  
- Trump pardons  
- Maryland extremists  
- Political violence  
- GOP radicalization  
- Suburban rage  
- Capitol attack  
- Polarized politics

I intensionally did not ask for a specific number like "5" tags becasue I wanted to see how long the answer would eb with out them. 

3. uv run python -m newspaper --url=https://cnsmaryland.org/2025/05/09/pardoned-maryland-jan-6-participants-find-support-after-convictions/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "You are an expert at categorizing topics for news stories. Read the text and give me tags to describe the story that are two words are less. Make the tags that are broad enough to relate to other stories with the same."

Answer: 
Jan6  
Pardons  
Extremism  
Polarization  
Maryland
 
 Not sure why it changed how Jan6 was categorized but this is what I got. I think this is better but now a bit too specific with only word word. I don't hate these answers but I don't really want to tag a story with something like "Extremsim"

 4. uv run python -m newspaper --url=https://cnsmaryland.org/2025/05/09/pardoned-maryland-jan-6-participants-find-support-after-convictions/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 " You are an expert at categorizing news stories for a newsroom publishing system located at the University of Maryland. Read the following story text and provide 3–5 concise tags, each 1–2 words long. The tags should represent the main topics of the story, be useful for browsing/search, and follow the style of Capital News Service tags. Do not include full sentences, explanations, or duplicates."

 I asked ChatGPT for advice on how to frame this and gave the reponse it gave me with a tweak to add that it is about UMD. 

 Asnwer: 
 Jan-6-pardons  
Maryland-extremism  
Republican-shift  
Capitol-attackers  
Political-polarization

Can't lie, I loved this promt but the answers absoluetly stink. Too specific 

5. uv run python -m newspaper --url=https://cnsmaryland.org/2025/05/09/pardoned-maryland-jan-6-participants-find-support-after-convictions/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 " You are an expert at categorizing news stories for a newsroom publishing system. Read the following story text and provide 3–5 concise tags, each 1–2 words long. The tags should represent the main topics of the story, be useful for browsing/search, and follow the style of Capital News Service tags. Do not include full sentences, explanations, or duplicates.

Think about what other stories on the Capital News Service website may be categorized under. You want to select tags that are fairly broad and relevant to multiple CNS stories, not just this one. For example, if a story involves Donald Trump, ‘Donald Trump’ would be a good tag because it connects this piece to many other CNS stories about him. Consider what keywords readers might search for or click on as tags to browse related coverage. Choose words that would help group this story with other CNS articles and make it easier for readers to find through tags,"

I kept the begining part the same and then wrote up some text to help it be more specific for the CNS audience and what I desired. I gave it the Donald Trump example and info on CNS. 

Answer: 
Jan. 6  
Trump pardons  
Maryland politics  
Domestic extremism  
Polarization

I think this is only slightly better. Needs to be more broad as no one would search for Domestic extremism  on CNS (lol).

6.  uv run python -m newspaper --url=https://cnsmaryland.org/2025/05/09/pardoned-maryland-jan-6-participants-find-support-after-convictions/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "You are an expert at categorizing news stories for a newsroom publishing system. Read the following story text and provide 3–5 concise tags, each 1–2 words long. The tags should represent the main topics of the story, be useful for browsing/search, and follow the style of Capital News Service tags. Do not include full sentences, explanations, or duplicates.

Think about what other stories on the Capital News Service website may be categorized under. You want to select tags that are fairly broad and relevant to multiple CNS stories, not just this one. For example, if a story involves Donald Trump, ‘Donald Trump’ would be a good tag because it connects this piece to many other CNS stories about him. Consider what keywords readers might search for or click on as tags to browse related coverage. Choose words that would help group this story with other CNS articles and make it easier for readers to find through tags.

Favor generic, reusable tags that appear often on the Capital News Service site, such as ‘Republicans,’ ‘Democrats,’ or ‘Donald Trump.’ Only include 1–2 more specific tags when they represent a major theme (e.g., ‘Jan. 6’). Avoid one-off or overly narrow phrases like ‘Domestic extremism ’ or ‘polarization."

I told chatgpt my issues with the last prompts and had it help me out again and above is what I got. 

Answer: 
Jan. 6  
Donald Trump  
Republicans  
Maryland

I will go with this! These are 4 solid tags that could be used on CNS. 

Thoughts: 

I loved this assignment. I find the task of prompting to be super enjoyable as small tweaks can get very different results. I was suprised how granular and specific I had to be with the LLM to get what I wanted. To be honest I had to spoon feed the LLM what I wanted. I think you could set up a LLM to read every story and then categroize it and then as it knew the categories that had been used it would be more useful. The issue it ran into in the first requests is that it did not know anything about CNS, as I got more specific about my request and CNS the response got better. Oddly the first request when I used ChatGPT to help me gave a poor answer with odd words. It took time in my prompting to explain to the LLM I need generic words, in my head that was obvious. My biggest gripe is not being able to just have a back and forth chat with the LLM. If I could easily talk back and forth then I could have solved my problem and explain what I wanted in a much quicker way without needing the terminal each time. Using the terminal means you need to get your prompt right the first time becasue you need to start a new chat to get what you want. 