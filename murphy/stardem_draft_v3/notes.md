# star dem draft v3 — cat murphy, nov. 29

ok my notes file isn't going to be great because i've been working on this all week and i feel like i have so little to show for it. i spent so long processing the local government stories and adding metadata, then pruning it down to relevant stories (748) before whittling it down to only the *most* relevant, *most* timely stories (~170).

i went out and got so much external data — budget analysis, census data, county and municipal officials, election data, recent council meeting minutes. the thing i spent the longest on was getting claude to generate ENORMOUS summary documents analyzing each county's budget and recent meeting minutes/transcripts – all of which i had to go donwload by hand. i also spent a lot of time manually feeding it the names and titles of government officials when the town had a cloudflare system that blocked my scrapers.

but it actually became, like, too monumental of a task with that much data. i didn't really know what to do with it all after a certain point, and neither did the llm. and then each draft i generated just ... sucked. some were worse than others, but i never actually *liked* any of them. and that's a shift from last time, when i was pretty happy with what i ended up with. 

but here, it just became an overwhelming amount of information. organizing it into folders helped, but trying to get a prompt to take into consideration so many files was really difficult. the formatting was never consistent, there were frequent hallucinations, and some of it was just ... well, bad. like this, in v2:

"Municipal leaders, notably Federalsburg’s mayor, act as advocates for town‑level concerns such as tax differentials and service parity."

like, *no shit*, really?

and considering how much information i was giving the llm, the results were actually almost *too* short. i was 100% expecting to have to narrow the focus after getting my first output, but it was giving me, like, 25 pages — which, again, comparatively, i knew meant something wasn't processing right. and a lot of those pages were just ... nothing. half-empty tables, mostly, and full tables that said exactly what the paragraph above them had said. it was incredibly frustrating, particularly because it didnt even seem like the llm was ... i don't want to say "trying," but yeah, trying. it would just shit out 25 pages of nonsense in like 12 seconds — every single time. that had not been the case with my education beat book, which took an appropriate amount of time to generate. i really never thought i'd be like "no this needs to take longer."

having had very little luck after a few drafts, i changed course, incredibly frustrated that i had put so much time (and quite a few groq accounts, as well as some of my own money) into this for it to not really work out. so first, i went back to education to see what i could do with that. that didn't work out and nothing i made was exponentially better than what i generated last week. so i came back to local government with an ingenious new approach: check to see if claude had reopened after i hit the limit on both accounts earlier. good news! it had! (genuinely, my sincere apologies — i'm a nightmare, i know, and i am sorry.)

ok, so this was my strategy: try one more time with copilot, then give the script and the output to chatgpt, then rerun chatgpt's script and give the script and output to claude. i also gave claude the non-story data and the file structure for the story data so that it had context on what information was actually available to the llm.

so i gave one of my terrible outputs to chatgpt and it ACTUALLY said this:

```
"The beatbook is pretty strong structurally but nowhere near the standard you want (both for your own reporting and for Howard Center/NYT-style clarity)"
```

ah, the joy of open ai's memory feature. this is what i get for bouncing resume and portfolio ideas off of it two weeks ago.

anyway, it was pretty brutal — rightfully so. it was like "hey, yeah, this reads like you're tripping on acid" (i'm paraphrasing).

it gave me a new script, while copilot had to fix because it had 25 (not joking) issues.

once i got that draft, i gave it to claude. this is a pretty good summation of what it said: "your prompt is burying the model under too much instruction and not enough clear signal about what matters." oh, but also:

```
Use a better model - groq/openai/gpt-oss-120b is not ideal for this. Try claude-3-5-sonnet-20241022 via the Anthropic API directly
```

the "please don't use our competitor's model" part was a nice touch.

it wrote me a script that produced a CONSIDERABLY better output, though i will note that it was also 82 pages long. it was in a completely different league as far as quality, but it still had some redundancies and weird quirks.

so i gave it back to claude and gave it some pointers. it rewrote the script.

102 pages. that script produced 102 pages of 12-point-font content.

there are still some, uh, issues:

```
1. Trace the 
‑million‑pluscostofthe287(g)ICE‑enforcementmodelmentionedonSeptember 30 2025;theFY 2026budgetshowsnoallocation,suggestingahiddenfundingsource.2. ComparethevoteontheAugust 28 2025sewer‑capacitymoratorium(reportedinStory 8)withtheabsenceofarecordedroll‑call;identifyanycommissionerswhorepeatedlyabstainedwithoutexplanation.3. ExaminetheRoyal FarmsdevelopmentapprovalprocessonApril 19 2025foranyundisclosedincentivesorreimbursements,sincethebudgetprovidesnolinefor“commercial‑site‑planassistance.”4. VerifywhethertheAnimalControlComprehensivePlan(Chapter 9)receivedanyfiscalsupport;thebudgetlistsnoanimal‑servicesexpenditurebeyondstandardoperatingcosts.5. Scrutinizetheshort‑term‑rentalregulationdiscussedonNovember 1 2024foramissing
‑million‑pluscostofthe287(g)ICE‑enforcementmodelmentionedonSeptember 30 2025;theFY 2026budgetshowsnoallocation,suggestingahiddenfundingsource.2. ComparethevoteontheAugust 28 2025sewer‑capacitymoratorium(reportedinStory 8)withtheabsenceofarecordedroll‑call;identifyanycommissionerswhorepeatedlyabstainedwithoutexplanation.3. ExaminetheRoyal FarmsdevelopmentapprovalprocessonApril 19 2025foranyundisclosedincentivesorreimbursements,sincethebudgetprovidesnolinefor“commercial‑site‑planassistance.”4. VerifywhethertheAnimalControlComprehensivePlan(Chapter 9)receivedanyfiscalsupport;thebudgetlistsnoanimal‑servicesexpenditurebeyondstandardoperatingcosts.5. Scrutinizetheshort‑term‑rentalregulationdiscussedonNovember 1 2024foramissing‑budget line for enforcement staffing, despite the plan’s projected $‑
```

yeah, i was thinking the same thing, claude.

here's the thing: if i can get it to cut some of the verbose, extraneous nonsense, i'd be ok with it. the main issue is with everything after the "top 3 priorities for immediate investigation" headers. i try to make clear to every llm i've used that this is NOT meant to be a suggestive document — it's a guide. i don't want story ideas, i don't want questions to ask officials, i don't want to know how to write a foia request à la claude. but when i told it to cut the crap after v4, it just invented new crap for v5. the structure is all over the place. it's a work in progress, for sure. but i'm not as upset about it as i was with the other ones. at least the narrative in this one was (mostly) comprehensible. but stay tuned, i plan to keep tweaking it ... as soon as my claude limit resets again.

ok bye