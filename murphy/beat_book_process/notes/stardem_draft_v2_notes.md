# beatbook v2 — cat murphy, nov. 22

ok, so i honestly really liked my second beatbook draft from last time (the gpt-oss-120b one, not the qwen one). the first one was definitely fine, but the gpt one was better in terms of formatting, organization, writing, etc.

and while i had gotten general census data, my biggest takeaway was that i needed to go get more topic-specific data based on the issues it focused on. so, for example, student discipline appeared a lot in the beatbooks. now that i know that this is a prominent issue, i can go grab more data to contextualize it. and i knew that blueprint was a major topic, but again, i figured it could be stronger with more context.

ok and then while my friend copilot was writing scraping scripts for that i looked for other data that i might want to scrape and add to my beatbook. the two main things i managed to find were teacher data and some random school improvement data that ultimately wasn't that relevant. but for the teacher data, i got it to at least scrape the number of teachers in each county, the % increase/decrease from the prior year, the number of new teachers, and the % of all teachers who are new. i wanted school-by-school data, but the stupid microsoft bi interface wouldn't scrape so i ended up just screenshotting and ocring it. i also went and got the statewide mcap data to show how eastern shore schools perform compartively. getting these scrapers to work was very trial and error, and i had to manually check the outputs to ensure it wasn't spitting out duplicates or misinterpreting things or dumb stuff like that. i think (?) i caught at least most of the errors.

getting the school discipline data was a huge fucking hassle, but well worth it. i got numbers by county, school, type, race, gender, disability and offense. the best thing i could get on blueprint was actually from the local news network — just summaries for each county, really, but that works. getting the actual budgets is somewhat unsurprisingly difficult, and when you CAN get them, it's such a disaster that it's not even worth it lol.

since i liked the output of my original prompt, i didn't overhaul it (at least, i haven't yet, as of when i wrote this).

what i did first was update my county summary file (with all my county- and school-level data on board members, school officials, mcap scores, etc.) and, because i have so much scraped data, create a separate summary book for school-level data (namely individual mcap scores and suspension data). this took ... a while. i didn't really expect it to take THIS long, but things kept getting left out or somehow messed up along the way, and it required a lot of finagling to get what i wanted (though, notably, i'm neurotic).

i fear copilot was losing its mind at this point, so i opened a new chat window lol.

the rest of what i did was mainly tweak my script, to be honest. i ran my original script with my new data, and it was very similar to my old beatbook — fine, sure, but it got a little repetitive at times, it included irrelevant sections barely targential to the topic, the dates weren't super clear, wes moore kept coming up, etc. so i had copilot adjust it to:

```
exclude candidates from district leadership source lists, and exclude star dem writers. get rid of regional education partners and media sections. use footnotes, not title references. make SURE you are referencing the correct dates for the data — the discipline data is from 23-24, census data and scores from 2024. why did you randomly exclude science from the mcap proficiency data? include state-level figures in a separate list, not in each county. do not include the governor other than to say what he has signed. if it's a delegate or state senator, explain their connection to education. do not include "Neighboring District Superintendents." do not include "Community & Service Organizations". "Education Policy & Advocacy Groups" should not include public school employees or statewide advocacy groups — cut it. no "Law Enforcement & Public Safety". no "State Education Agency". no "Community & Service Organizations". put stuff like maryland reads and maryland rural development coop and Giving the Edge Foundation in a state orgs category, not individually. do not repeat names. do not include leaders of other county public schools in other counties. use consistent source format and spellings. get rid of the (PDF), (web portal), etc. in the documents section. 
```

the result was definitely better, but it now included stuff like this:

```
School Principals
Specific principal names were not provided in the source data; please refer to the Kent County Public Schools website for the most current listings (as of 2025).
```

the formatting also lowkey was worse ??? instead of listing things in, you know, a list, it just kind of put them together separated by semicolons.

point being, i switched models to use `groq/meta-llama/llama-4-maverick-17b-128e-instruct`instead of gpt so i could compare the results. because while i think my beatbook draft is fine, i'm kind of disappointed it didn't necessarily come out the way i wanted. the meta-llama one was good – see v3_enhanced. it semed to turn out slightly better in terms of organization and citations, and the length seemed slightly more reasonable.

either way, though, it made it very clear that i am still missing some key contextual data — namely school enrollment broken down by race and special populations, particularly given that it provides a comparison point for suspension rates. i tried to get it, but it was proving very difficult to scrape, so i moved on to other, easier to capture data (for now). 
