# cleaning og script

Create a new script that modifies education_script_v1.py called education_script_v2.py to do the following:
- Combine the `key_organizations` and `key_bodies` fields into `key_organizations`
- Cut the `key_locations` field
- Edit the `key_people` field to ensure that: 
1) All public officials/politicians/board members/council members/etc. are extracted
2) If a person is extracted as a key person in one story, any mention of them in another story should be extracted as a key person
3) Titles are formatted as "Name — Title, {{Organization/Body/Institution}}, {{Municipality}}, {{County}}"
4) All names, titles, organizations, etc. are standardized

# prompt for script to pull only relevant stories

```python
You are generating a beat book that would help a new reporter cover the education beat across five Maryland counties: "Talbot County", "Kent County", "Dorchester County", "Caroline County", "Queen Anne's County".

Create a new python script in `pull_relevant_stories.py`that uses the `llm` command-line tool and subprocess with the model `groq/meta-llama/llama-4-maverick-17b-128e-instruct` to process the stories in `education_stories_with_entities_v2.json` and pull only stories that would be relevant to that beat book.

Examples of stories that would be relevant would be stories about:
- Boards of education
- Political candidates for education positions
- State or local education initiatives
- Public meetings
- Political debates about education
- Public officials
- School officials
- Education policies
- Education legislation and bills
- Education funding
- School staffing
- Curricula
- Attendance rates and absenteeism
- Graduation rates
- Crime
- Recurring events

Examples of stories that are unlikely to be relevant would be feature articles and stories about one-off events, niche events, school clubs, scholarships, and other topics not critical to a reporter's general knowledge of the beat.

Use `relevant_stories` and `not_relevant_stories` to determine which stories should be included or excluded. You should use the score associated with the "Education" topic — either as a primary or secondary topic — as a guide, but do not base your decisions entirely on them. Note, however, that stories with "Education" topic scores > 0.9 are likely to be relevant, and stories with education scores < 0.65 are unlikely to be relevant. Only news stories are relevant, so categorically exclude articles where `content_type` is NOT "News". 

relevant_stories = [
      {
        "title": "Maryland\u2019s Teacher Shortage: Will the Blueprint\u2019s Plan for Better Pay, Training Do Enough?",
        "date": "2024-03-23",
        "author": "Aidan Hughes and Daranee Balachandar Capital News Service",
        "content": "Maryland\u2019s teacher shortage: Will the Blueprint\u2019s plan for better pay, training do enough?\n\n March 23, 2024 | Star Democrat, The (Easton, MD)\n\n Author/Byline: AIDAN HUGHES and DARANEE BALACHANDAR Capital News Service | Section: Business \n \n 1505\n Words \n\n Read News Document\n\n Fifth-grade teacher Melissa Carpenter works a 10-hour day on average during the week, and her job sometimes requires her to put in hours on weekends, too.\"I feel like teaching is one of those jobs where we go to work to do more work \u2014 to do work after work,\" said Carpenter, who teaches at William B. Wade Elementary School in Waldorf, in Charles County.\nCarpenter's long hours are far from unique among Maryland's educators, as the state and nation grapple with a teacher shortage.\nThe U.S. Department of Education keeps a Teacher Shortage Areas database \u2014 and it found that for the current school year, Maryland was short of teachers in 28 subjects, which the state defines as \"areas of certification.\" That's up from 17 five years earlier.\nSome teacher certification areas \u2014 such as English as a second language, health science and special education \u2014 are short on teachers from pre-K through the 12th grade.\nThe Blueprint for Maryland's Future \u2014 a landmark state law reforming public education \u2014 aims to fix that problem by \"elevating the stature of the teaching profession\" through higher pay, better training and stronger recruitment efforts.\nHowever, experts and educators have mixed views about whether that will successfully address the root causes of the shortage.\n\"Money is a huge help, but it's not everything,\" said Simon Birenbaum, director of grading, assessment and scheduling at Baltimore City Public Schools. \"Human capital is the biggest issue, and money can help with that problem, but recruiting, training and retaining high-quality teachers and staff has to be the primary focus. No amount of money can compensate for a lack of highly-skilled educators.\"\nDocumenting the shortageMaryland's teacher woes follow national trends. The National Center for Education Statistics reported 86% of U.S. K-12 public schools faced challenges in hiring teachers for the current school year.\nAmid the shortage, the Blueprint calls for hiring an unspecified number of additional teachers to ease the workload of classroom veterans.\n\"You hear a lot about the teacher shortage \u2014 and how are we going to implement all these Blueprint programs, which require additional staffing, when we have a teacher shortage?\" asked Addie Kaufman, executive director of the Maryland Association of Secondary School Principals.\nShortages stem, in part, from the fact that teachers are leaving the profession. In Prince George's County, 1,126 teachers resigned between July 2022 and July 2023 \u2014 up from 989 the previous year, The Washington Post reported. Meanwhile, 625 resigned in Montgomery County Public Schools, up from 576 a year earlier.\nDorchester County experienced the highest attrition rate in Maryland during the 2021-22 school year at 18%, according to a Department of Education report.\n\"I used to never have people just quit in the middle of the year,\" said Dorchester County Superintendent Dave Bromwell, who recently retired. \"The pandemic told some people, you know what? If you're not happy, move on.\"\nAll those factors end up impacting teachers like Carpenter. She said her grade level saw an influx of students, with around 30 students in her own fifth grade class this year.\n\"Our class sizes are growing, and we don't have the support in place to help some of our struggling learners,\" she said.\n'teaching isn't approved'Schools are suffering from a long-term decline in the number of people interested in becoming teachers.\nThat decline has been ongoing since the mid-'70s, \"but it gets worse and worse and worse, year over year,\" said Mike Hansen, an education policy expert at the Brookings Institution.\nAccording to the State Department of Education, 9,134 people were enrolled in teacher preparation programs in the state in 2012. That number plummeted by about half by 2017, but rose to 6,037 by 2020.\nWhy is teaching becoming less appealing as a career? Zid Mancenido, a lecturer at the Harvard Graduate School of Education, has been studying that issue.\n\"One of the major findings of my research has been that people are taught over time that teaching isn't a great career,\" he said in a 2022 interview on the school's website. \"There are all these tiny interactions they have over their lifetime that give them this feeling that teaching isn't approved, that they should be aspiring to other careers that might be more prestigious or well-paid.\"\nAmid the shortage, many schools hire less-credentialed \"conditional\" teachers \u2014 those who have not yet received their professional certifications. Maryland's issuance of conditional certificates more than doubled between 2018 to 2022, a state Department of Education report said.\nIn Charles County, where Carpenter works, 12.4% of all teachers held conditional certificates by 2021 \u2014 a rate only surpassed by Baltimore City (13.4%) and Prince George's County (14.3%).\nCarpenter said experienced teachers are leaned on to help the conditional hires.\n\"Which would be fine if you had one or two teachers who needed that support. But we have a massive amount of teachers who are conditional right now,\" she said.\nThe Blueprint's pay bumpIn order to address the teacher shortage, the Blueprint provides a number of measures that lawmakers hope will encourage people to become teachers and ensure that existing ones don't leave for more lucrative out-of-state positions \u2014 or exit the profession altogether.\nA key Blueprint initiative increases teacher pay to a minimum of $60,000 by 2026. In some counties, that means a nearly $15,000 pay bump for new teachers.\nDavid Larner, chief human resource and professional development officer at the Howard County Public School System, said the pay raise will attract teachers from other states and build up Maryland's teacher workforce.\n\"If our salaries are higher than salaries in surrounding states \u2026 then candidates are more likely to come,\" Larner explained.\nHowever, Hansen, of the Brookings Institution, expressed skepticism about the likely impact of the measure on the state's teacher shortage.\nHansen argued that rather than a universal rise in minimum salary levels, money should be targeted where it's needed the most \u2014 attracting teacher talent in high-need schools and specialized fields like STEM subjects and special education. He also highlighted research that suggests salary is just one of many factors that can lead to teacher attrition.\n\"I think we need to be paying teachers more \u2014 I don't think paying a $60,000 minimum wage is the way to do it,\" he said.\nBoosting careers and diversityThe Blueprint also aims to improve teacher quality by encouraging educators to obtain additional training.\nThe plan provides for a salary increase of $10,000 for teachers who become National Board Certified, an advanced teaching credential that fewer than 6% of Maryland teachers held at the start of 2023, according to the National Board for Professional Teaching Standards. Teachers in high-need areas may see their annual salaries increase by up to $17,000 by becoming certified.\n\"We want to professionalize the career of teaching, and I think that is absolutely what we should be doing,\" said Stephanie Novak Pappas, principal of the Holabird Academy, an elementary and middle school in Baltimore.\nHowever, Hansen questioned the Blueprint's emphasis on National Board certification.\n\"We don't have a lot of evidence that actually getting your NBC makes you a better teacher,\" Hansen said.\nThe Blueprint also calls on school districts to create a diverse workforce. The Accountability and Implementation Board \u2014 which oversees the Blueprint \u2014 will evaluate those efforts.\nA diverse workforce has significant benefits, according to David Blazar, an education policy expert at the University of Maryland.\nBlazar said that increasing the share of Black teachers has \"exceptionally large impacts on students' short and long term outcomes,\" he said. \"I'd say some of the largest impacts I've seen across all of the educational intervention literature.\"\nBut maximizing the benefits of a more diverse workforce will be complicated, Blazar said. Even if the state's teacher workforce came to match the demographics of its students, there would likely still be \"clustering of Black teachers within certain districts, and within certain schools within districts,\" he said.\nHansen echoed those concerns, and said that teachers nationwide remain even more racially segregated than students. Rather than aiming to make the teachers within individual districts reflect the exact racial demographics as their students, he suggested that policymakers should \"maximize exposure and access to a diverse set of teachers for every student\" across different regions.\nA work in progressBeyond the Blueprint, the General Assembly last year passed the Maryland Educator Shortage Reduction Act, which requires the state to set recruitment goals for teacher education programs, creates an alternative teacher prep program for early childhood educators and establishes a $20,000 yearly stipend for eligible student teachers.\nGov. Wes Moore, who proposed the legislation, said upon signing it that it is intended to place \"world class teachers in every classroom.\"\nCarpenter, the Charles County teacher, said future changes may be necessary, too.\n\"We will have new students next year, and they will [have] different needs. So we need to make sure that we are constantly evolving,\" she said.\nMeanwhile, Sparkle Jefferson, an assistant principal at Flintstone Elementary School in Prince George's County, stressed that reinforcing the teacher workforce is key to the Blueprint's overall success.\n\"It lands in the hands of our educators, and if we don't have educators who are highly qualified or able to do the work, then the Blueprint work would never get accomplished,\" she said.\nLocal News Network Director Jerry Zremski contributed to this report. \n\n \u00a9 Copyright \u00a9 2024 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
        "docref": "news/198005AA32CE8BC8",
        "article_id": "search-hits__hit--5397",
        "content_source": "full_document",
        "year": 2024,
        "month": 3,
        "day": 23,
        "llm_classification": {
        "topic": "Education",
        "score": 0.96,
        "candidates": [
            {
            "topic": "Education",
            "score": 0.96
            },
            {
            "topic": "Business/Economy",
            "score": 0.42
            }
        ],
        "explanation": "The article focuses on Maryland's teacher shortage, policy reforms, pay and training initiatives\u2014all central to the education sector, making Education the best match."
        },
        "llm_classification_meta": {
        "model": "gpt-oss:120b",
        "llm_failed": false
        },
        "content_type": "News",
        "regions": [
        "Maryland",
        "U.S."
        ],
        "municipalities": [
        "Waldorf"
        ],
        "counties": [
        "Charles County",
        "Prince George's County",
        "Montgomery County",
        "Dorchester County",
        "Howard County",
        "Baltimore City"
        ],
        "key_people": [
        "Melissa Carpenter \u2014 Teacher, William B. Wade Elementary School",
        "Simon Birenbaum \u2014 Director of Grading, Assessment and Scheduling, Baltimore City Public Schools",
        "Addie Kaufman \u2014 Executive Director, Maryland Association of Secondary School Principals",
        "Dave Bromwell \u2014 Superintendent, Dorchester County Public Schools",
        "Mike Hansen \u2014 Education Policy Expert, Brookings Institution",
        "Zid Mancenido \u2014 Lecturer, Harvard Graduate School of Education",
        "David Larner \u2014 Chief Human Resource and Professional Development Officer, Howard County Public School System",
        "Stephanie Novak Pappas \u2014 Principal, Holabird Academy",
        "David Blazar \u2014 Education Policy Expert, University of Maryland",
        "Wes Moore \u2014 Governor, State of Maryland",
        "Sparkle Jefferson \u2014 Assistant Principal, Flintstone Elementary School"
        ],
        "key_events": [],
        "key_initiatives": [
        "Blueprint for Maryland's Future",
        "Maryland Educator Shortage Reduction Act"
        ],
        "key_establishments": [
        "William B. Wade Elementary School",
        "Baltimore City Public Schools",
        "Howard County Public School System",
        "Holabird Academy",
        "Flintstone Elementary School",
        "Charles County Public Schools",
        "Prince George's County Public Schools",
        "Montgomery County Public Schools",
        "Dorchester County Public Schools"
        ],
        "key_organizations": [
        "Maryland State Department of Education",
        "Maryland Association of Secondary School Principals",
        "National Board for Professional Teaching Standards",
        "Accountability and Implementation Board",
        "Maryland General Assembly",
        "Brookings Institution",
        "Harvard Graduate School of Education",
        "University of Maryland"
    ]
  },
    {
        "title": "Talibah Chikwendu Appointed to Dorchester Board of Education",
        "date": "date",
        "author": "author name",
        "content": "story content",
        "docref": "docref",
        "article_id": "article id",
        "content_source": "full_document",
        "year": "year",
        "month": "month",
        "day": "day",
        "llm_classification": {
        "topic": "Education",
        "score": 0.92,
        "candidates": [
            {
            "topic": "Education",
            "score": 0.92
            },
            {
            "topic": "Local Government",
            "score": 0.68
            },
            {
            "topic": "Public Notices",
            "score": 0.45
            }
        ],
        "explanation": "The article reports on the appointment of a new member to the Dorchester County Board of Education, focusing on school governance and educational issues, making Education the most relevant category."
        },
        "llm_classification_meta": {
        "model": "gpt-oss:120b",
        "llm_failed": false
        },
        "content_type": "News",
        "regions": [
        "Maryland"
        ],
        "municipalities": [
        "Cambridge"
        ],
        "counties": [
        "Dorchester County"
        ],
        "key_people": [
        "Talibah Chikwendu \u2014 Member, Dorchester County Board of Education",
        "Theresa Stafford \u2014 Former Member, Dorchester County Board of Education"
        ],
        "key_events": [],
        "key_initiatives": [],
        "key_establishments": [
        "Dorchester County Public Schools"
        ],
        "key_organizations": [
        "Dorchester County Board of Education",
        "Dorchester County Council",
        "Dorchester County Public Schools"
        ]
    }
]


not_relevant_stories = [
{
    "title": "TCPS Looks into Creation of Clay Target Shooting Club",
    "date": "2024-03-22",
    "author": "Maggie Trovato",
    "content": "TCPS looks into creation of clay target shooting club\n\n March 22, 2024 | Star Democrat, The (Easton, MD)\n\n Author/Byline: Maggie Trovato | Section: Local News \n \n 562\n Words \n\n Read News Document\n\n EASTON \u2014 The Talbot County Board of Education is hoping to make a decision in May regarding a request for a high school clay target shooting club.At a Board of Education meeting Wednesday, the board heard from five members of the public asking that it approve the creation of the club. The board also heard from Talbot County Public Schools Chief Financial Officer Sarah Jones about the district's research into whether this club could be created at TCPS.\nDuring public comment, Sheriff Joe Gamble spoke on behalf of the Talbot County Sheriff's Office about the importance of having a space for a group of teens to come together and be a part of something.\n\"We all know kids want to be a part of a group, they want to be a part of something,\" he said. \"The Sheriff's Office fully supports another venue for our youth to connect with other people of like-minded and like interests.\"\nAustin Eader, a ninth grader at Easton High School, said that this week he gathered 191 student signatures and 24 teacher and staff signatures from people who support having the club.\nMany of people interested in starting the club, including Talbot Rod & Gun Club President Joe Capozzoli, spoke at a board meeting in October requesting approval to create the club.\nAfter that meeting, TCPS Superintendent Sharon Pepukayi instructed her staff to look into what it would take to make the club happen. At the meeting Wednesday, Assistant Superintendent for Curriculum and Instruction Helga Einhorn said Jones has been leading that charge.\nJones told the board that the district has been meeting with those interested in starting the club to gather more information. She said the biggest concern right now is figuring out if the club could in any way jeopardize the district financially \u2014 particularly from a risk management perspective.\nShe said that although they have heard about the training and safety precautions required to participate in the program, it still involves putting a firearm in students' hands.\n\"We have to be very thoughtful about that,\" she said.\nThe district has gone to its insurance provider, the Maryland Association of Boards of Education Group Insurance Pool. Jones said a discussion around the topic was held at a February MABE meeting, and MABE intends to hold a session and vote on this at its annual meeting in late April.\nJones said the district will need to consider whether MABE will continue to provide liability coverage if an incident were to happen and, if so, whether it would be at an additional cost. She said the district doesn't have these answers yet because MABE hasn't voted on it yet.\nJones said she should have these answers for the May Board of Education meeting.\nBoard President Emily Jackson said the board and district are at MABE's mercy at this point. She said that as long as MABE has this discussion in April, the board should be able to make a firm decision in May regarding the creation of the club.\nAt the end of the meeting, board member Deborah Bridges said she is on board with the creation of the team.\n\"I think it would be a wonderful addition to our county,\" she said. \"I think it's important because girls can do it too. And there's limited access for females these days. And also for the children that can't do regular athletics, because they can be a part of it too.\" \n\n \u00a9 Copyright \u00a9 2024 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
    "docref": "news/197F5860A0A9CD18",
    "article_id": "search-hits__hit--5422",
    "content_source": "full_document",
    "year": 2024,
    "month": 3,
    "day": 22,
    "llm_classification": {
      "topic": "Education",
      "score": 0.86,
      "candidates": [
        {
          "topic": "Education",
          "score": 0.86
        },
        {
          "topic": "Sports",
          "score": 0.58
        },
        {
          "topic": "Public Safety",
          "score": 0.42
        }
      ],
      "explanation": "The article centers on a school board's deliberation over creating a high\u2013school clay target shooting club, focusing on policy, liability, and student participation, which aligns most closely with the Education topic."
    },
    "llm_classification_meta": {
      "model": "gpt-oss:120b",
      "llm_failed": false
    },
    "content_type": "News",
    "regions": [
      "Maryland"
    ],
    "municipalities": [
      "Easton"
    ],
    "counties": [
      "Talbot County"
    ],
    "key_people": [
      "Sarah Jones \u2014 Chief Financial Officer, Talbot County Public Schools",
      "Joe Gamble \u2014 Sheriff, Talbot County Sheriff's Office",
      "Austin Eader \u2014 Student, Easton High School",
      "Joe Capozzoli \u2014 President, Talbot Rod & Gun Club",
      "Sharon Pepukayi \u2014 Superintendent, Talbot County Public Schools",
      "Helga Einhorn \u2014 Assistant Superintendent for Curriculum and Instruction, Talbot County Public Schools",
      "Emily Jackson \u2014 President, Talbot County Board of Education",
      "Deborah Bridges \u2014 Member, Talbot County Board of Education"
    ],
    "key_events": [],
    "key_initiatives": [],
    "key_establishments": [
      "Easton High School",
      "Talbot County Public Schools"
    ],
    "key_organizations": [
      "Talbot County Board of Education",
      "Talbot County Sheriff's Office",
      "Talbot Rod & Gun Club",
      "Maryland Association of Boards of Education Group Insurance Pool"
    ]
  },
  {
    "title": "Books Rife with Sexual Content",
    "date": "2024-03-03",
    "author": "Staff Writer",
    "content": "Books rife with sexual content\n\n March 3, 2024 | Star Democrat, The (Easton, MD)\n\n Author/Byline: Staff Writer | Section: News \n \n 384\n Words \n\n Read News Document\n\n When I first heard about the \"Freedom to Read\" Act, Maryland SB 0738, I was reminded of the words of one of our founders, John Adams : \"Liberty cannot be preserved without a general knowledge among the people, who have a right \u2026 and a desire to know; but besides this, they have a right, an indisputable, unalienable, indefeasible, divine right to that most dreaded and envied kind of knowledge, I mean of the characters and conduct of their rulers.\" (A Dissertation on the Canon and Feudal Law, 1765)So when I heard of the \"Freedom to Read\" Act, I wondered what banned books were suddenly going to be made available to the students of Maryland. I assumed there must be some politically controversial books from the Cold War Era that had been suppressed.\nIt was disappointing when I discovered that the books which Maryland students are being encouraged to read are rife with graphic sexual content, ones which most parents deem inappropriate for their children. Last fall, parents in Carroll County questioned why books with graphic sexual imagery were being made available to children without parental knowledge or consent.\nOne is the autobiography of Jaycee Dugard, who was kidnapped and used as a sex-slave in a cellar for years. I have read Dugard's \"A Stolen Life: A Memoir;\" it as a story of heroism but only for mature readers since it is about a kidnapping and child rape. It does not belong in a school.\nAn article in the Easton Gazette (Feb. 2, 2024) provides details about the \"banned\" books which SB 0738 is intended to liberate. To quote: \"These books have pornographic images or descriptions, the likes of which you could find in Penthouse magazine. The Carroll County Board considered the opinions of parents with children as young as elementary school who complained that these books demonstrating various types of sex such as oral, vaginal, anal, etc. were accessible to students. Some of the books portrayed graphic rape scenes or sexual experimentation in the story lines that were not appropriate for any minor child.\"\nSo when Maryland schools are struggling to achieve basic literacy, how is it helpful to have students' minds filled with images of rape, etc? Why are the wishes of parents ignored and disrespected? What is the agenda?\nMARY-EILEEN RUSSELL\nTalbot County Republican Central Committee\nClaiborne \n\n \u00a9 Copyright \u00a9 2024 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
    "docref": "news/1979310CBA2813A8",
    "article_id": "search-hits__hit--5645",
    "content_source": "full_document",
    "year": 2024,
    "month": 3,
    "day": 3,
    "llm_classification": {
      "topic": "Education",
      "score": 0.94,
      "candidates": [
        {
          "topic": "Education",
          "score": 0.94
        },
        {
          "topic": "Local Government",
          "score": 0.45
        },
        {
          "topic": "Public Safety",
          "score": 0.3
        }
      ],
      "explanation": "The article discusses a state legislative act affecting school curricula and parental concerns about book content, which directly relates to education policy and school reading material."
    },
    "llm_classification_meta": {
      "model": "gpt-oss:120b",
      "llm_failed": false
    },
    "content_type": "Opinion",
    "regions": [
      "Maryland"
    ],
    "municipalities": [
      "Easton",
      "Claiborne"
    ],
    "counties": [
      "Talbot County",
      "Carroll County"
    ],
    "key_people": [
      "Mary-Eileen Russell \u2014 Member, Talbot County Republican Central Committee",
      "John Adams \u2014 Historical Figure (former President of the United States)"
    ],
    "key_events": [],
    "key_initiatives": [
      "Freedom to Read Act",
      "Maryland SB 0738"
    ],
    "key_establishments": [],
    "key_organizations": [
      "Talbot County Republican Central Committee",
      "Carroll County Board of Education"
    ]
  }
]
```

# excerpted prompt for beatbook v1 (see https://chatgpt.com/share/6918d97e-5d48-800c-890b-bdc2e50300de)

```python
You are writing the "Top Three Issues on the Education Beat" section for {county}, Maryland.

You will determine the three biggest issues by analyzing the *full story text*, not just metadata.

Write a section titled "Top Three Issues on the Education Beat".

Requirements:
- Produce **exactly three issues**, each as an **H3 heading (###)**.
- Under each heading, write **1–3 paragraphs of narrative prose**.
- **Do NOT use bullets or lists** in this section.
- Base your assessment primarily on the full story content.
- The writing must feel like a newsroom beat memo for a reporter.

You are writing the "Key Sources to Know" section of a beat book for {county}, Maryland.

Write a “Key Sources to Know” section for {county}.

Requirements:
- Use **H3 headings** to label different source categories (e.g., “### Superintendent and Central Office Leadership”).
- Under each heading, use **bulleted lists**.
- Each bullet should identify:
  - A specific person, position, or office (e.g., superintendent, board chair, principal, union rep)
  - Why they matter and what decisions they influence
  - Why a reporter might contact them
- Keep bullets concise and journalist-friendly.

You are writing the "Key Documents, Records & Websites to Track" section of a beat book for {county}, Maryland.

Write a “Key Documents, Records & Websites to Track” section for {county}.

Requirements:
- Use **H3 headings** for document categories (e.g., “### Budget & Finance Records”).
- Under each heading, use **bulleted lists**.
- Bullets should:
  - Identify a document type (e.g., CIP, budget book, staffing report, discipline dataset)
  - Explain what information it provides
  - Explain why it matters for reporting
- Include county-level and MSDE/Blueprint-related materials.
```

# excerpted prompt for beatbook v2

to copilot: I need a script called `generate_beatbook_v2.py` that takes `generate_beatbook_v1.py` and does the following:

- Simplifies and shortens the output. Maximum of three paragraphs per issue. No "why this matters" sections for sources. Create a consolidated list of data/documents instead of by county.
- Uses groq/qwen/qwen3-32b BUT strips out the content in the <think></think> tags
- Uses only the titles and metadata

```python
You are writing the "Top Three Issues on the Education Beat" section for {county}, Maryland.

You will determine the three biggest issues by analyzing the story titles and metadata.

Write a section titled "Top Three Issues on the Education Beat".

Requirements:
- Produce **exactly three issues**, each as an **H3 heading (###)**.
- Under each heading, write **MAXIMUM THREE PARAGRAPHS** of narrative prose.
- **Do NOT use bullets or lists** in this section.
- Be concise and focused - get to the point quickly.
- Base your assessment on the story titles and metadata provided.
- The writing must feel like a newsroom beat memo for a reporter.

You are writing the "Key Sources to Know" section of a beat book for {county}, Maryland.

Write a "Key Sources to Know" section for {county}.

Requirements:
- Use **H3 headings** to label different source categories (e.g., "### Superintendent and Central Office Leadership").
- Under each heading, use **bulleted lists**.
- Each bullet should identify:
  - A specific person, position, or office (e.g., superintendent, board chair, principal, union rep)
  - What decisions they influence
- Keep bullets concise - NO "why this matters" explanations.

You are creating a consolidated "Key Documents, Records & Websites to Track" section for an education beat book covering five Maryland counties: Talbot County, Kent County, Dorchester County, Caroline County, and Queen Anne's County.

Write a consolidated "Key Documents, Records & Websites to Track" section that applies across all five counties.

Requirements:
- Use **H3 headings** for document categories (e.g., "### Budget & Finance Records", "### Assessment Data").
- Under each heading, use **bulleted lists**.
- Bullets should:
  - Identify a document type (e.g., CIP, budget book, staffing report, discipline dataset)
  - Briefly explain what information it provides
  - Keep explanations concise - one sentence maximum
- Include county-level and MSDE/Blueprint-related materials that apply across counties.
- Do NOT create separate sections for each county - this should be ONE consolidated list.
```

# excerpted prompt for beatbook v3

to copilot: I need a script called `generate_beatbook_v3.py` that takes `generate_beatbook_v2.py` and does the following:

- Prioritizes the most recent coverage — anything from the last year (Nov. 2024 forward) should take precedence, and stories from before then should be used mainly as context
- Uses the titles, sumamries and metadata
- Creates a comprehensive data/document section at the end 

```python
You are writing the "Top Three Issues on the Education Beat" section for {county}, Maryland.

You will determine the three biggest issues by analyzing story titles, summaries, and metadata.

**PRIORITIZE RECENT COVERAGE (Nov 2024 forward)** - These stories should drive your issue selection.
Use historical stories (before Nov 2024) only as context to understand how issues have developed.

Write a section titled "Top Three Issues on the Education Beat".

Requirements:
- Produce **exactly three issues**, each as an **H3 heading (###)**.
- Under each heading, write **MAXIMUM THREE PARAGRAPHS** of narrative prose.
- **Do NOT use bullets or lists** in this section.
- **PRIORITIZE recent coverage** - focus on what's happening now or recently
- Use historical stories only to provide context for ongoing issues
- Be concise and focused - get to the point quickly.
- The writing must feel like a newsroom beat memo for a reporter.

You are writing the "Key Sources to Know" section of a beat book for {county}, Maryland.

**PRIORITIZE people and organizations mentioned in recent coverage (Nov 2024 forward).**

Write a "Key Sources to Know" section for {county}.

Requirements:
- Use **H3 headings** to label different source categories (e.g., "### Superintendent and Central Office Leadership").
- Under each heading, use **bulleted lists**.
- Each bullet should identify:
  - A specific person, position, or office (e.g., superintendent, board chair, principal, union rep)
  - What decisions they influence
- **Prioritize sources from recent stories** - these are the active players
- Keep bullets concise - NO "why this matters" explanations.


You are creating a COMPREHENSIVE "Key Documents, Records & Data Sources to Track" section for an education beat book covering five Maryland counties: Talbot County, Kent County, Dorchester County, Caroline County, and Queen Anne's County.

This should be a thorough reference guide for reporters covering education across these counties.

Write a comprehensive "Key Documents, Records & Data Sources to Track" section.

Requirements:
- Use **H3 headings** for document categories (e.g., "### Budget & Finance Records", "### Assessment & Academic Data", "### Personnel Records", "### Facilities & Capital Planning").
- Under each heading, use **bulleted lists**.
- Be COMPREHENSIVE - include all major document types a reporter would need
- For each bullet:
  - Identify the document type or data source
  - Briefly explain what information it provides (one sentence)
  - Include WHERE to find it when applicable (county websites, MSDE portal, etc.)
- Cover both county-level and state-level (MSDE/Blueprint) materials
- Include recurring reports (annual budgets, MCAP results, etc.)
- Include meeting records (board minutes, agendas, recordings)
- Include data dashboards and online portals
- This should be ONE consolidated list for all five counties - do NOT create separate sections per county.
```

