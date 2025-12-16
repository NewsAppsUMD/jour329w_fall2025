# star dem different — cat murphy, dec. 6

ok, so, my main goal was to get even more data involved. yeah, i know,.

this involved *a lot* of scraping. i finally got through all of the enrollment data, and then ran a smaller scraper to get the attendance rates and student populations (students with disabilities, free and reduced meals, etc.). this took, like, forever. while those scrapers were running, 

i did a few other things:

## i asked claude to build me a browser-based beatbook

this turned out really well ... at first. originally, i didn't really give it very much to go on, to be honest. like, i kind of just fed it some data, waited for it to output something, gave it more stuff with some more specific directions, and so on.

and for a while, that was great. the early versions had the following tabs: data dashboard, five key issues, sources. there were also six tabs above them, one for each county and one for all counties.

the data dashboard mainly included the suspension data and some of the mcap data, along with a few visualizations, which was nice.

but then i tried to keep adding to it, and that's where it got tricky. last time i did this, i created a summary book of the county budgets for the local government beat, then tweaked them to focus on education. this time, i wanted to analyze both the county budgets and the school budgets — except claude couldn't handle the files.

and so ...

## i asked chatgpt to create a data book based on the FY26 budgets for each county and its public school system

in an effort to compress the 10 massive budget documents into a single file, i had chatgpt generate a comprehensive but succinct data book. i was actually pretty impressed with its output. i tried using gemini to compare the results, but chatgpt's was far and away better in terms of quality, structure, consistency and relevance. it took some back and forth, but the final product had a section for each county, subsectioned to include a core fiscal table, enrollment & per-pupil spending, blueprint drivers, capital outlook, emerging fiscal/policy issues and narrative sumamry. the book also included an additional two chapters at the end: cross-county comparison tables and regional takeaways. honestly, that was one of the better summary books i've created.

## i asked copilot to grab all relevant quotes from the article, put them in their own file and then generate profiles of the relevant actors

another thing that i ran into while fact-checking my original education beatbook was that the quotes were GARBAGE. i mean, everything from badly paraphrased to utterly nonsensical to pure hallucination. the data it used, however, was completely in line with the data files i provided it, so that tells me it's probably better if the llm has the relevant data already separated out and organized. so, in an effort to address that, i had copilot write me a script to pull just the quotes out of the stories. i then wanted it to generate profiles of the most prominent actors.

this too required somewhat of a back and forth effort. it repeatedly hallucinated quotes while generating these profiles, so it took some finagling to get it to pull only relevant quotes and then use only those quotes and relevant story content to compile a short bio. eventually, however, it did give me i think 26 profiles — one for every key player quoted at least five times in the star dem's coverage (i think in the last 7-8 months?). great, cool, wonderful. but then i got distracted and went back to ...

## i went back to claude to try to get this website working

mind you, i have collected so much freaking data that getting any llm to process any of this was nearly impossible. i continued to switch between models, using claude in-browser for the actual web interface, claude via copilot to use groq with the story content, and chatgpt for summarizing documents to feed back to claude.

and after those early app interfaces that claude built me with very little to go on, all of the webpages started to SUCK. they were barely functional, you couldn't click between tabs, they weren't loading any of the data. claude literally stopped working (repeatedly) because the files it was building were too large. add to that the fact that chatgpt and claude via copilot were incapable of fixing the html. so, that got really frustrating really fast.

so when i got bored of that ...

## i switched gears again and decided to make another narrative beat book

here was my thought process: if i have it make a narrative beat book with only some data elements, then i can have claude focus on formatting the data and pass it the narratives to add in afterward. for some inexplicable reason, the narrative beat books i was getting today were FIRE. the ones from the random groq model it was using at first were, like, pretty good — honestly, better than some other beat books i've spent hours trying to get right. but then i switched to gpt-oss-120b and it was INSANE. i don't know what changed. i have a feeling it was at least in part because of the budget data, but the dramatic improvement in quality floored me — and also kind of pissed me off, because, like, really? now you work? great.

but by the time i was done with this, i had to go back to ...

## i went back to claude and begged for forgiveness

i mean, the h2 says it all, right?

i had very little hope at this point that i was going to be able to pull off the website i wanted. VERY. LITTLE.

it just — nothing up to this point had worked in the way that i had wanted, and everything was simply too large for claude to manage.

but on a whim i tried one last time ... and it worked.

it required a fair amount of tweaking, but i got it to give me a narrative analysis of the five key issues on the education beat on the eastern shore, with a "critical findings" subhead to sum up the main point, plus two paragraphs and a table. on another table i got it to give me a narrative breakdown of count-level issues, alongside key statistics relevant to each county, like enrollment, budget, state funding, etc.

after many back and forths, i got claude to give me a schools dashboard. all 47 schools that i scraped from msde's website. an interactive interface that lets you click through each county and view all of the schools with their enrollment and the largest demographic, and you can click on each one of those to get a line-by-line of enrollment, male/female, race and student groups (swd, farms, multilingual, economically disadvantaged). i tried to get it to include mcap data, and it says it does, but the script was already 4000+ lines long, i wasnt going to push my luck.

and, finally, i had it give me a searchable sources table. ultimately, i ended up with 58 source cards, including the 26 key figures my copilot script pulled out earlier, plus some other district officials i scraped a couple weeks ago. it includes their titles, orgs, the topics they're quoted on and the number of times they've been quoted (when applicable).

ok, but like, BOOYAH. i'm genuinely so happy with how it came out. i have a lot more that i want to add — oh, and jesus, i need to get rid of the heinous inline css and js. but that's a next week problem.