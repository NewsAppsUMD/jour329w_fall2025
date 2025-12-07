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

here was my thought process: if i have it make a narrative beat book with only some data elements, then i can have claude focus on formatting the data and 

