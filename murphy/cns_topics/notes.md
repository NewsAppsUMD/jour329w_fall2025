# cns topic analysis — cat murphy, oct. 2

## patterns:

**types of stories that appear most frequently:**

looking at cns' recent coverage, the majority of stories are about — or at the very least relate to — government and politics in some capacity

**maryland-specific topics that come up repeatedly:**

so, the majority of stories tend to localize national politics rather than cover maryland-specific issues. recent coverage tends to focus on the impact on maryland of federal policies and the maryland angle of national issues like immigration and fema. and more specifically, i'm noticing that cns often focuses on maryland's u.s. senators and representatives and their reactions to the moves of the federal government. even if you look at just the four featured stories on cns' website, the top two are about how maryland lawmakers are reacting to the government shutdown. the third is about the uncertain future of renewable energy projects in maryland ... but the reason for the uncertainty is that the federal government pulled funding from those projects. the only featured story that focuses on a maryland-specific issue — a landfill in baltimore county — is the fourth one.

**coverage areas that seem over-represented:**

oh, well, the federal government/national politics. i kind of explained what i mean above, but cns' most prominent coverage focuses not on maryland-specific issues but on the maryland angle of federal issues.

**coverage areas that seem under-represented:**

i know this is going to come as a shock, but coverage of *actual maryland issues* represents a relatively small percentage of cns' overall coverage, and particularly of its most prominent coverage.

**government level with the most coverage:** 

well, if you look at the *overall* tag counts, the state government historically has received the most coverage. case in point, "maryland" is the no. 2 most-used tag on cns' website overall, and "annapolis," "larry hogan" both "baltimore" tags (lol) are in the top 30. but if you look at the most-used tags over the last year (i edited my code to add this to my "broswer"), only "maryland" appears in the top 30, and even then it's only been used five times. the list of the most-used tags from the last 12 months includes many national political figures, like trump, harris and schumer. there are maryland figures on that list, but *all of the them* are federal reprentatives — van hollen, hoyer, raskin, alsobrooks, elfreth, mfume. and "donald trump" is the leading tag, with 33 stories over the last 12 months — more than double the number tagged "chris van hollen," the second-most used tag in that time. actually, other than "maryland," the only maryland-specific tags in the top 30 are "francis scott key bridge" and "chesapeake bay." so while state government may have gotten the most attention in the past, the federal government gets by far the most coverage today. not great ...

**policy areas appear most in tag names:**

historically, "education" (183), "health" (116), "environment" (110), "budget" (81) and "coronavirus" (75) are the most-used policy tags. but over the last 12 months, assuming elon musk is not a policy issue, the top policy tags are "federal workers," "immigration" and "environment." even beyond those exact tags, there are issue-related tags like "kilmar abrego garcia" for immigration and "chesapeake bay" for environment. this is interesting, because it really does show how cns' focus has shifted away from more maryland-specific issues like education in favor of national issues like federal workers and immigration

**current topics that seem too broad or too narrow:**

honestly, i think most of them are too narrow. case in point, i don't think anyone has ever gone on cns' website and searched "chris van hollen" or "jamie raskin." politics? sure, maybe. but no one is seeking out chris van hollen stories or looking for the latest on jamie raskin. also, why is there a "plane crash" tag. ok, i know why. but like ... come on.

**topic overlap in the tags:**

i sort of touched on this, but the biggest thing i'm noticing in terms of overlap is names: donald trump, chris van hollen, jamie raskin, steny hoyer, angela alsobrooks, sarah elfreth, kamala harris, joe biden, kweisi mfume. every single one of these could be categorized under "government & politics." same goes for "federal workers" and "election 2024" and "tariffs." i suppose you could break this down into "federal government & politics" and "maryland government & politics." but there's no need for 8 billion tags that no one is searching for.

**maryland-specific topics that seem important/deserve their own categories:**

well, it's hard because the most frequently used tags are all about national issues ...

but i mean, i think there should generally be a "local government & politics" tag — because "prince george's county" isn't going to have so many stories that it needs its own tag. the exceptions there are probably annapolis and baltimore, which should get their own tags. i might say chesapeake bay, but even that i think could just be "environment."

## refine the topics

### old list

```
1. Agriculture and Food
2. Animals
3. Armed Forces and National Security
4. Arts & Culture
5. Civil Rights
6. Commerce
7. Congress
8. Justice
9. Budget
10. Education
11. Elections
12. Emergency Management
13. Energy
14. Environmental Protection
15. Families
16. Economy
17. Trade
18. Maryland Government and Politics
19. Federal Government and Politics
20. Health
21. Housing
22. Immigration
23. International Affairs
24. Labor and Employment
25. Law
26. Native Americans
27. Natural Resources
28. Science & Technology
29. History
30. Social Welfare
31. Sports
32. Taxes
33. Transportation and Public Works
34. Chesapeake Bay
35. Baltimore
```

### my list

```
1. Maryland Government & Politics
2. Federal Government & Politics
3. Congress
4. Baltimore
5. D.C.
6. Local
7. Budget & Economy
8. Education
9. Health & Environment
10. Arts & Culture
11. Sports
12. Transportation & Infrastructure
13. International Affairs
```

### explanation

*tags i kept:*

    Maryland Government & Politics
    Federal Government & Politics
    Congress
    Baltimore
    Education
    Arts & Culture
    Sports
    International Affairs

*tags i added:*

    D.C. — nation's capital & location of CNS bureau; necessary for stories that concern Washington as a place, not just an institution 
    
    (see https://cnsmaryland.org/2025/09/17/dc-council-approves-commanders-move-from-maryland-back-to-washington/, https://cnsmaryland.org/2025/05/08/maryland-lawmakers-decry-possible-medicaid-cuts-amid-24-hour-protest-near-us-capitol/, https://cnsmaryland.org/2025/04/17/d-c-s-go-go-museum-showcases-the-music-genres-local-roots-global-influence/)

    Local — encompasses stories that concern local events or features unrelated to government or politics

    (see https://cnsmaryland.org/2024/05/13/prince-georges-has-more-new-businesses-than-any-maryland-county-whats-behind-the-surge/)

*tags i combined/changed:*   

    Budget & Economy — government spending affects the economy, and the economy impacts government spending, so having separate tags doesn't make sense given that stories about one typically involve the other; the few that don't do not need their own category

    (see https://cnsmaryland.org/2025/09/30/government-shutdown-hurts-americans-marylands-van-hollen-and-hoyer-warn/, https://cnsmaryland.org/2025/01/15/gov-moores-proposed-budget-features-tax-reform-and-massive-cuts/)

    Health & Environment — similar to above, health and environment are often intertwined in that most stories about one are directly or indirectly related to the other; given the scope of cns' coverage, there is no need to separate them

    (see https://cnsmaryland.org/2025/09/30/prince-georges-county-data-center-pause-underscores-local-concerns-about-widespread-impacts/, https://cnsmaryland.org/2024/03/12/epa-tightens-air-quality-standard-for-the-first-time-in-12-years/)

    Transportation & Infrastructure — these topics are not only interrelated but also too narrow to tag separately. case in point, "transportation" isn't even a tag on cns' website. a combined tag would encompass everything from the key bridge to the department of transportation to the infrastructure act. (and i took out "public works" because infrastructure largely covers it and because "public works" exists on cns' website but has never actually been used.)

    (see https://cnsmaryland.org/2024/10/17/maryland-building-more-electric-vehicle-charging-stations-with-boost-from-federal-state-funds/, )

*tags i cut:*

    Agriculture & Food — covered by health & environment; current related tags are used relatively rarely used

    Animals — covered by health & environment; current related tags are used relatively rarely
    
    Armed Forces and National Security — covered by federal government & politics

    Civil Rights — covered by federal government & politics, congress or maryland government & politics, depending on context; current civil rights tag hasn't been used in four years

    Commerce — covered by budget & economy; not a current tag 

    Justice — covered either by federal government & politics, maryland government & politics, depending on context; only one of the stories under this tag was published in the past six years and all related tags can be similarly recategorized 

    Elections — covered by federal government & politics, congress or maryland government & politics, depending on context

    Emergency Management — covered by federal government & politics, maryland government & politics or health & environment, depending on context; current emergency management tag has been used twice in total and all related tags can be similarly recategorized

    Energy — covered by federal government & politics, maryland government & politics or transportation & infrastructure, depending on context; current energy tag has 21 stories and all related tags can be similarly recategorized
    
    Environmental Protection — covered by health & environment, federal government & politics or maryland government & politics, depending on context; current environmental protection tag has three stories and all related tags can be similarly recategorized

    Families — current families tag has six stories under it and hasn't been used since 2017
    
    Trade — covered by federal government & politics or budget & economy; trade is not a current tag and related tags account for 10 total stories

    Housing — generally covered by maryland government & politics or local; housing is not a major coverage area for cns and current housing-related tags are used infrequently

    Immigration — covered by federal government & politics or maryland government & politics; it is a current tag, but nearly all the stories under it are about federal policies and the reactions of maryland lawmakers to those policies

    Labor and Employment — covered by budget & economy; the current "labor" and "employment" tags account for a total of 12 stories

    Law — covered by federal government & politics, congress or maryland government & politics

    Native Americans — current tag hasn't been used in three years, and each of the stories under it relate to government, D.C. or covid
    
    Natural Resources — covered by health & environment 

    Science & Technology — cns' coverage of these topics typically falls under federal government & politics or education; current science tag has two stories from the past two years and the teechnology tag hasn't been used in three years
    
    History — current history tag hasn't been used in three years and related stories can typically be recategorized under another tag

    Social Welfare — related stories would likely fall under other tags; not a current tag

    Taxes — covered by budget & economy

    Chesapeake Bay — covered by health & environment

ok bye
-cat