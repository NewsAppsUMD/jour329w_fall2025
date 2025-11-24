Star-Democrat Choice Assignment 11/14/25

From my last attempt I modified the data so that I have 240 stories (20 from each month) created by CoPilot with even weight to each month depending on how many stories are from that month. I suspect this will give me a better sense of the yearround coverage from the Stardemocrat. 

I also simplified my schema to incldue the title of those included in the stories, I removed the venue metadata due to the incosistency.

Prompt: uv run python add_entities.py --model groq/meta-llama/llama-4-maverick-17b-128e-instruct --input Sports.highschool.2024.240.json

Name of file: stories_with_entities5.json

For some reason the LLM did a bad job filitering the 240 stories and included way too many professional sports stories, I will fix that for my next attempt. The LLM also removed the metadata piece that wrote a blurb about who the target audience was for each story. 

I wonder if there are not 240 stories only on high school so it added in professional ones to hit the 240 mark...I doubt it but it could be. Probably bad filtering by CoPilot

Specifically looking at the high school stories llama did a great job completing all aspects of the requested metadata. 

Next steps: remake the data section and run again. 

Attempt 2: I requested that CoPilot assist me in making a .json file of all the high school stories from 2024 that remove and roundup articles that only have results and also remove the college and professional stories. 

My hope is to get a comprehnsive review of a year in coverage from the stardemocrat to see how they format their sports coverage over a year and what sports they focus most on. 

I also added back the "who is this story targeted to" metadata. Llama worked well for me and my classmates so I used it again.

What I asked CoPilot: here are steps you need to do 
1. Take sports.json and remove every story not from 2024
2. remove everystory that is not specificaly about high school sprots coverage 
3. remove every story that is simply a roundup story with no reporting
4. tell me how many stories are in the .json

Propmt: uv run python add_entities.py --model groq/meta-llama/llama-4-maverick-17b-128e-instruct --input sports2024highschool.json

Other than the fact that this took about 2 hours to run I was very pleased with the results. 

Here are my takeaways/findings:

Looking specifically at the high school stories (172) from 2024 here are some important numbers:

Football: 38
Basketball: 33
Lacrosse: 18
Wrestling: 16
Soccer: 14
Field Hockey: 11
Softball: 10 
Baseball: 8 

I think I am missing some high school stories but this gives a general sense of what the focus of the stardem coverage is on an full year basis. 

By month:
October: 36
Feb: 26
Nov: 20
Mar: 16

October may be the time of the year the reporter needs the most help or needs to write shorter stories whereas in the summer the writer can do more profile stories. 

Type of stories: 
game recap: 138
preview: 21
feature: 11
results: 2 (just score compilation)

The "who the intended audience" section is great and will be super helpful for future reportrs. 

Here is an example: "Local high-school sports fans and families; readers interested in Cambridge-South Dorchester High athletics."

The "how important was this game" section was a fail. 

8: 88 
7: 39
6: 33

I would have liked more of a range from this. Cool if it worked not super important. 

For people quoted not every person quoted was given a title which I would like to clean up in the future. 

Attempt 3: 

I was happy with these results metadata wise but wanted to clean it up a bit by removing all the TV Listings from the data and the few remaining professional sports stories.

It took some time working with CoPilot to do this as it removed too many stories first but i got it to finally work. I was unable to get the llama LLM to run with the limited stories despite many attempts the LLM kept failing. 

I instead decided to use a different LLM to compare the results from my previous attmept. For show reason it said all 247 stories ran but only 41 appeared in the datasette.

As can be seen I created many different .json with data and metadata. Unfortunately most did not work but I am happy with the output I did get from attempt 2. 

Prompt: uv run python add_entities.py --model groq/ope
nai/gpt-oss-120b --input sports2024highschool.json




Overall analysis:

Best output: stories_with_entities6 is the best set of metadata. 

I am not sure what made the LLM fail but it happened on most attempts. Working with CoPilot to generate json with a but frustarting but with enough asks I got close to what I wanted. I just don't think it is that good at analyzing stoires that do or do not have to do with high school sports. 


#### Final Recommendations
That set of metadata I very close to being usable. Cleaning up the data is not that important becasue I can just facet by High School. I am going to run all 1000 + stories after this so I can have all of them but it won't finish in time for me to complete this assignment. If I clean up the title before the person quoted I am happy with this set of metadata. 



