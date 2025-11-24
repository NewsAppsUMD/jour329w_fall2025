 Star-Democrat Draft Beat Book 11/17/25

I chose to look at sports and specifically the high school sports beat. With over 150 stories a year specificlaly about high school sports from the star democrat this is topic deserving of a beat book. 

In order to get the below prompt to run I spent a few hours narrowin down my Json file. I removed every other story twice to end up with only 42 stories from 2024. I cut all the full text from stories as well as other metadata. I am left with 42 stories with these categories of info: 

"title": 
    "date": 
    "author": 
    "year": 
    "month": 
    "day": 
    "metadata_sport": 
    "metadata_story_type": 
    "metadata_location": 
    "metadata_teams": 
    "entities_quoted_people": 
    "metadata_level_of_play": 
    "metadata_competition_type": 
    "metadata_outcome": 
    "metadata_importance": 

Code: cat prompt.txt sour
ce_stories_every_other.json | uv run llm -m groq/openai/gpt-oss-120b > prototype_v1.md

Prompt: Create a comprehensive beat guide for a reporter covering sports on the Eastern Shore. Use the provided stories as source material to introduce the key people, teams, institutions, and recurring issues that define the local sports landscape.
Introduce the journalist to the topic as if you were an expert guide. The guide should focus on how to do the job in the future. 

The language should be business casual, and it should not be primarily a list of bullet points, but you can use bullet points for checklists or proposed sources or locations for a suggested story angle. 

The guide should clearly explain:
	•	Who the reporter should know in the sports world on the eastern shore. 
	•	Which sports matter most on the Eastern Shore 
	•	How to structure the reporting year


I created this prompt by combining the CNS prompt I had and then using the narrative guide prompt. 

prototype_v1.md: **Eastern Shore Sports Beat – A Practical Guide for the Modern High‑School Reporter**  
*(Prepared by a longtime beat veteran for anyone stepping into the Maryland Eastern Shore high‑school arena.  All dates, names and story ideas are drawn from the 2024 coverage archive.)*  

---

### 1.  Why the Eastern Shore is a Unique Beat  

The Eastern Shore isn’t a single city; it’s a patchwork of small towns—Centreville, Easton, Stevensville, Queen Anne’s, Wicomico, Kent County and beyond—each with a proud high‑school sports tradition.  Because the schools are the community’s social hub, a game is never just a game; it’s a story about family ties, school spirit, local economies, and, increasingly, the challenges of maintaining competitive programs with limited resources.

In the 2024 cycle you’ll notice three recurring themes:

| Theme | How it shows up | What it means for you |
|-------|----------------|-----------------------|
| **Playoff intensity** – almost every sport spikes in coverage after the regular season (e.g., the “Warriors extend win streak” basketball recap, the “Sabres finish strong on way to crown” soccer playoffs). | Build a pipeline of pre‑season expectations, mid‑season checkpoints, and post‑game analysis. |
| **Coaching turnover & new philosophies** – “Warriors battle but can’t extend win streak against undefeated Bennett” (new soccer coach, new offensive system). | Track coaching hires, philosophy changes, and the ripple effect on player development. |
| **Community & safety issues** – the Carver Vo‑Tech basketball game stopped by an altercation; the “Girls wrestling champions receive acclamation” feature on gender equity. | Look for stories that go beyond the box score: facility upgrades, Title IX compliance, mental‑health initiatives, and community fundraising. |

---

### 2.  Who You Need to Know  

Below is a *who‑what‑where* matrix that captures the most‑quoted coaches, administrators and recurring “go‑to” sources.  Treat each name as a starting point for deeper relationships; most of them are open to a quick coffee or a post‑game chat.

| School / Institution | Primary Contacts (coach, AD, PR) | Typical Story Angles |
|----------------------|-----------------------------------|----------------------|
| **Queen Anne’s County High (Lions)** | Jeff Hollis (boys basketball), Dionte Hynson (football), Brian Mooney (football), Aaron Stewart (softball), Jamie Leventry (volleyball) | Title runs (volleyball three‑peat), defensive streaks (soccer shutouts), community outreach. |
| **Easton High (Warriors)** | Matt Griffith (football), Gabe Kane (soccer), Butch Waller (basketball), David Fisher (softball), Laura Harding (field hockey) | New‑coach impact, rivalry with Queen Anne’s, multi‑sport athletes (e.g., Marshall Bailey). |
| **Kent Island High** | Josh August (wrestling), Justin Holland (track & field), Bobby Woolley (lacrosse), Kim Neff (field hockey) | Rapid rise in wrestling & lacrosse, indoor track championships. |
| **St. Michaels High** | Boo Ricketts (basketball), Brian Femi (baseball), Dave Morrissette (baseball) | Tournament performances (Peake Challenge), baseball dominance. |
| **Colonel Richardson High** | David Fisher (softball), Bryan Hall (wrestling) | Consistent softball power (10‑0 win), wrestling program growth. |
| **Cambridge‑South Dorchester High** | Rob Burnham (football, field hockey), Shawn Parker (basketball) | “Vikings” brand, cross‑sport coaching synergy. |
| **North Dorchester & James M. Bennett** | Various; often the athletic director is the gateway (e.g., Harold Somerville at Kent County). | Opponent perspective for rivalry pieces. |
| **County & Tournament Organizers** | *Peake Challenge* committee (Wye Mills), *Eastern Shore Athletic Association* (wrestling), *Maryland Interscholastic Athletic Association* (track). | Event previews, rule changes, logistics. |

**Quick tip:** Keep a “contact log” in a spreadsheet with columns for *Name, School, Sport, Email, Preferred Contact Method, Last Interaction*.  Update it after every game—those small “thanks for the quote” notes build goodwill.

---

### 3.  The Sports That Matter Most  

While every sport gets a story, the data set shows a clear hierarchy based on volume, community interest and postseason relevance:

1. **Basketball (boys & girls)** – 12+ recaps, frequent tournament previews, high‑impact players (Vince Gilberto, Marshall Bailey).  
2. **Football** – Seasonal previews (Sept, Oct), playoff battles, big community draw (Easton vs. North Carolina, Vikings vs. Fort Hill).  
3. **Wrestling** – Growing participation, especially girls’ program (feature on Queens Anne’s champions).  
4. **Track & Field (indoor/outdoor)** – Regional championships, standout athletes (Todd, Sumayah Wilkins).  
5. **Baseball / Softball** – Consistent coverage of regular‑season dominance (St. Michaels, Colonel Richardson).  
6. **Soccer** – Emerging rivalry narrative (Easton vs. Bennett, Queens Anne’s shutouts).  
7. **Lacrosse** – High‑scoring titles (Kent Island vs. Decatur).  
8. **Field Hockey & Volleyball** – Playoff storylines, especially for Easton and Queens Anne’s.

When you plan your calendar, allocate **core weeks** (basketball in Jan–Mar, football Sep–Nov, wrestling Feb–Mar) and **satellite weeks** for the “second‑tier” sports.  Even a single human‑interest angle (e.g., a senior’s final season) can elevate a lesser‑covered sport into front‑page territory.

---

### 4.  Structuring the Reporting Year  

Think of the season as a **four‑phase cycle** that mirrors the academic calendar:

| Phase | Timing | Primary Deliverables | Sample Story Types |
|-------|--------|----------------------|--------------------|
| **Pre‑Season Planning** | Early August – Mid‑September | • Calendar of games, tournaments, and championship dates.<br>• “Preview” pieces (e.g., *“TALL TASK”* football preview).<br>• Coaching change interviews. | • “A FINE BLEND” football preseason outlook.<br>• Peake Challenge preview (Feb 10). |
| **Regular‑Season Pulse** | Mid‑Sept – Late Feb (football, basketball, wrestling) / Mar–May (track, lacrosse, baseball) | • Game‑by‑game recaps (use the “who‑said‑what” formula).<br>• Mid‑season check‑ins (win‑streaks, injury updates).<br>• Feature on training facilities or community support. | • “Warriors extend win streak” (basketball).<br>• “Girls wrestling champions receive acclamation” (feature). |
| **Playoff & Championship Spotlight** | Late Feb – Early Nov (depending on sport) | • Tournament previews (Peake Challenge, regional wrestling).<br>• Live‑blogging or rapid‑turnaround recaps of knockout games.<br>• Human‑interest pieces on senior athletes and title‑chasing coaches. | • “Sabres finish strong on way to crown” (soccer).<br>• “Todd earns four titles; Vikes win boys crown” (track). |
| **Wrap‑Up & Off‑Season** | December – Early January | • End‑of‑year round‑ups (top athletes, coaching awards).<br>• “Where are they now?” for graduating seniors.<br>• Preview of next year’s schedule, facility upgrades, recruiting pipelines. | • “Lions serve up 3rd straight title” (volleyball).<br>• “Queens Anne’s extends North shutout streak” (soccer). |

**Practical workflow tip:**  
- **Create a master spreadsheet** titled *Eastern Shore Sports Calendar* with columns for *Date, Sport, Opponent, Venue, Story Angle, Deadline, Assigned Writer*.  Populate it from school websites and the Maryland Interscholastic Athletic Association (MIAA) releases.  
- **Set weekly “story blocks.”** For example, every Thursday you have a 250‑word recap deadline for the previous night’s basketball game; every Monday a 500‑word feature on a standout wrestler.  This cadence helps you meet tight publishing windows without burning out.

---

### 5.  Story‑Finding Checklist (Bullet Form)  

Below is a quick‑reference list you can paste into your notes app.  Tick the boxes each week to make sure you’re covering all the angles.

- **Game Recap Essentials**  
  - Score, key stats, turning point.  
  - At least two quotes (coach & player).  
  - Context: win‑streak, rivalry, playoff implication.  

- **Human‑Interest Angles**  
  - Senior’s final season / “last dance.”  
  - Family of multi‑sport athletes (e.g., a basketball star who also plays lacrosse).  
  - Community fundraisers for equipment or facility upgrades.  

- **Trend Tracking**  
  - Win‑streaks or losing streaks (e.g., Easton’s early‑season basketball surge).  
  - Injury reports and depth‑chart adjustments.  
  - Coaching philosophy shifts (new offensive system, defensive emphasis).  

- **Recurring Events**  
  - **Peake Challenge** (Feb 10) – a must‑cover tournament for basketball.  
  - **Regional Wrestling Championships** (Feb 23/25).  
  - **Track & Field Regionals** (May 18).  

- **Key Dates to Flag**  
  - First Friday of September: start of football season.  
  - Last week of January: high‑school basketball regular season concludes.  
  - Mid‑April: softball & baseball championships.  
  - Early June: end of track season, awards ceremony.

---

### 6.  Sample Pitch Packages  

**A. “The Rise of Girls’ Wrestling on the Eastern Shore”**  
- **Hook:** The recent feature on Queens Anne’s champions (June 7) shows a surge in participation and community support.  
- **Sources:** Coach David Stricker (Queens Anne’s), Athletic directors from Kent Island and St. Michaels, parents of wrestlers, Maryland Girls’ Wrestling Association.  
- **Angles:** Title IX compliance, scholarship opportunities, training facilities, athlete profiles (e.g., Julia Reburn).  

**B. “From the Sidelines to the Spotlight: New Coaches Redefining Small‑Town Football”**  
- **Hook:** New head coach Matt Griffith’s impact on Easton’s offense (Sept 10 soccer preview, Oct 8 soccer loss) and the ripple effect on recruiting.  
- **Sources:** Coaches (Griffith, Burnham, Mooney), players (Mikey O’Connor, Zach Davis), local high‑school football analysts.  
- **Angles:** Tactical changes, community expectations, comparative win‑loss before/after hire.  

**C. “The Peake Challenge: A Tournament That Unites the Shore”**  
- **Hook:** The February 10 preview lists 13 high schools; the tournament has become a regional showcase for talent.  
- **Sources:** Tournament director (Wye Mills school board), coaches (Boo Ricketts, Jeff Hollis), past MVPs.  
- **Angles:** Economic impact on host town, scouting opportunities, alumni stories.  

---

### 7.  Practical Tips for a Sustainable Beat  

1. **Be a “Community Reporter.”** Attend the pep rallies, school board meetings and local fundraisers.  A story about a new weight‑room can become a front‑page piece when you hear the school principal’s budget concerns first.  
2. **Leverage Social Media Wisely.** Most coaches post game‑day line‑ups on Twitter or Instagram.  Use those posts to verify quotes and get instant reactions—just double‑check with a quick email.  
3. **Maintain a “Story Bank.”** Every time you hear a promising quote or an odd statistic, jot it down.  You’ll have a ready reservoir when a deadline looms.  
4. **Watch the Calendar for “Off‑Season” Stories.** The offseason is the perfect time for deep‑dive features (e.g., “Where are the 2022 seniors now?”).  
5. **Balance Speed with Accuracy.** The Carver‑Vo‑Tech altercation (Mar 9) shows how a rushed story can miss the broader context (security policies, district response).  Verify facts before the first deadline hits.  

---

### 8.  Quick Reference – Key Schools & Their Signature Sports  

| School | Signature Sport(s) | Recent Highlight |
|--------|-------------------|------------------|
| Queen Anne’s County High | Basketball, Volleyball, Soccer | Three‑peat volleyball titles (Oct 29) |
| Easton High | Football, Basketball, Field Hockey | Overtime field‑hockey win (Oct 15) |
| Kent Island High | Wrestling, Lacrosse, Track | Indoor track championship (Feb 6) |
| St. Michaels High | Basketball (Peake Challenge), Baseball | 4‑1 baseball win vs. North Dorchester (Apr 10) |
| Colonel Richardson High | Softball, Wrestling | 10‑0 softball shutout (Mar 26) |
| Cambridge‑South Dorchester High | Football, Lacrosse, Basketball | 46‑8 football blowout (Oct 4) |
| North Dorchester High | Football, Basketball | 54‑30 basketball win (Dec 6) |

---

### 9.  Closing Thought  

Covering the Eastern Shore isn’t about chasing national headlines; it’s about telling the stories that matter to families sitting on the bleachers, to the students who’ll remember a newspaper clipping decades later, and to the towns that rally around their high‑school teams.  By keeping a tight calendar, nurturing a reliable network of coaches and administrators, and always digging a little deeper than the final score, you’ll turn the everyday rhythm of games into a compelling narrative that keeps readers coming back week after week.

Welcome to the beat—now go get those quotes, watch those overtime goals, and remember that on the Eastern Shore every victory feels like a community celebration.  



*Prepared for the newsroom on 18 Nov 2025.*


## Thoughts from V1 ##

Overall this is a weak beat book. The issue with taking data from 2024 is that people may be outdated. I also don't think the information needs to be as person dense rather it would work better if it was general informtion. I don't need the names of coaches, ad and players as a different LLM can get that info easily I need the LLM to explain that having the names of those people is important. 

The structuring the year works well and would be helpful to someone who is newer to sports coverage. 

I found this tip to be helpful for local sports. "Leverage Social Media Wisely.** Most coaches post game‑day line‑ups on Twitter or Instagram.  Use those posts to verify quotes and get instant reactions—just double‑check with a quick email. "

However the schools and their signature sport section is useless becasue it has old info and not enough of it. 

The guide needs more info on how the reporter should plan their week to get to all this coverage and what types of stories matter the most to the community. 


Prompt 2: Create a comprehensive beat guide for a reporter covering sports on the Eastern Shore. Use the provided stories as source material to introduce the key people, teams, institutions, and recurring issues that define the local sports landscape.
Introduce the journalist to the topic as if you were an expert guide. The guide should focus on how to do the job in the future. 

The language should be business casual, and it should not be primarily a list of bullet points, but you can use bullet points for checklists or proposed sources or locations for a suggested story angle. 

The guide should clearly explain:
	- 	What sports matter most
    - How the reporter should strcuture their life and work schedule to attend late night games 
    - tips on forming relationships with local coaches
    - How to write different types of sports stories
    - How to track statistics, rosters, and standings across seasons and leagues.
    - What makes a strong sports feature story
    - what to avoid as a local sports reporter
    - how to balance competitive sports during crossover and playoff seasons


Code 2: cat prompt.txt source_stories_every_other.json | uv run llm -m groq/openai/gpt-oss-120b > prototype_v2.md

Prompt: Create a comprehensive beat guide for a reporter covering sports on the Eastern Shore. Use the provided stories as source material to introduce the key people, teams, institutions, and recurring issues that define the local sports landscape.
Introduce the journalist to the topic as if you were an expert guide. The guide should focus on how to do the job in the future. 

The language should be business casual, and it should not be primarily a list of bullet points, but you can use bullet points for checklists or proposed sources or locations for a suggested story angle. 

The guide should clearly explain:
	- 	What sports matter most
    - How the reporter should strcuture their life and work schedule to attend late night games 
    - tips on forming relationships with local coaches
    - How to write different types of sports stories
    - How to track statistics, rosters, and standings across seasons and leagues.
    - What makes a strong sports feature story
    - what to avoid as a local sports reporter
    - how to balance competitive sports during crossover and playoff seasons




Prototype_v2: ## Eastern Shore Sports‑Beat Handbook  
*Your go‑to companion for covering high‑school athletics on Maryland’s Eastern Shore.  Think of it as a living map rather than a static checklist—use it to plot the season, meet the right people, and spot the storylines that keep the community turning its eyes (and radios) to the gym, the field, and the track.*

---

### 1. Why the Eastern Shore is a unique beat  

The Eastern Shore is a patchwork of small towns—Centreville, Easton, Queen Anne’s County, St. Michael’s, Stevensville, and beyond—where high‑school sport is the social glue.  Games are community events, rivalries stretch back generations, and every victory (or controversy) reverberates through town halls, PTA meetings, and the local paper.  

Because most of the action is **high‑school**, the beat is less about professional contracts and more about:

* **Coaches who double as teachers and civic leaders** – they are the gatekeepers of access and the most reliable source of background.
* **Student‑athletes who are also “local kids”** – their families, graduation plans, and college aspirations are part of the story.
* **District and county athletic directors** – they shape schedules, eligibility rules, and funding decisions that affect every sport.
* **Community institutions** – the school board, local businesses (sponsors), and the Eastern Shore’s media ecosystem all influence coverage.

Understanding those relationships is the foundation for any story that goes beyond a simple game recap.

---

### 2. Who to know – the “who‑list” (not a pure bullet list, but a quick‑reference guide)

| Category | Key Names (from recent coverage) | What they bring to the beat |
|----------|----------------------------------|-----------------------------|
| **Principal Administrators** | **Brian Mooney** (Queen Anne’s County High), **Harold Somerville** (Kent County High), **Rob Burnham** (Cambridge‑South Dorchester) | Scheduling, budget approvals, discipline decisions (e.g., the Carver‑Queen Anne’s altercation). |
| **Head Coaches – Basketball** | **Jeff Hollis** (QAH Lions), **Dionte Hynson** (Easton Warriors), **Butch Waller** (Wicomico Indians), **Gary Hofmann** (Carver Vo‑Tech) | Game strategy, player development, pre‑season outlooks. |
| **Head Coaches – Football** | **Matt Griffith** (Easton Warriors), **Brian Mooney** (QAH Lions), **Rob Burnham** (Cambridge‑South Dorchester), **Zack Alkire** (Fort Hill) | Play‑calling trends, injury reports, recruiting pipelines. |
| **Head Coaches – Wrestling** | **Josh August** (Kent Island Buccaneers), **Tommy Sitar** (Harford Vo‑Tech), **David Stricker** (QAH Lions) | Tournament brackets, weight‑class issues, gender‑equity developments (girls’ championships). |
| **Head Coaches – Soccer / Field Hockey / Lacrosse** | **Avery Brice** (Easton soccer), **Laura Harding** (Easton field hockey), **Bobby Woolley** (Kent Island lacrosse) | Seasonal rivalries, player‑spotlight opportunities. |
| **Athlete Voices** | **Vince Gilberto** (QAH Lions basketball star), **Marshall Bailey** (Easton Warriors), **Olivia Orrell** (Easton field hockey OT hero), **Micah Quinn** (Kent Island lacrosse) | First‑hand accounts, human‑interest angles, college‑recruiting chatter. |
| **Media & Community Partners** | **Bill/William Haufe** (Chesapeake Publishing), **Andrea Grabenstein** (feature writer), local radio sports hosts | Story distribution, photo/video resources, cross‑promotion. |
| **Support Staff & Administrators** | **Justin Holland** (track & field coach), **Jamie Leventry** (volleyball coach), **Kim Neff** (field hockey) | Access to practice footage, insight into training regimens. |

**How to use it:**  
- **Introductory email**: Reach out to each coach before the season starts, introduce yourself, and ask for a quick “team snapshot” (roster, goals, key story ideas).  
- **Quarterly check‑ins**: Meet district athletic directors after each sport’s championship to gauge policy changes (e.g., eligibility, safety protocols).  
- **Student‑athlete profiles**: Invite standout players like Gilberto or Orrell for a brief sit‑down; they’ll often point you toward teammates with compelling back‑stories.

---

### 3. The sports that dominate the Eastern Shore beat  

While every sport gets coverage, the following five generate the most consistent news flow, attendance, and community conversation:

1. **Basketball (boys & girls)** – Seasonal rhythm runs from November‑March, with high‑stakes playoffs (e.g., the “Carver‑QAH” game stopped by an altercation).  
2. **Football** – The fall staple (August‑December). Rivalry weeks (e.g., Easton vs. North Caroline) and playoff previews dominate local chatter.  
3. **Wrestling** – Strong participation on both boys’ and girls’ sides; tournaments at Berlin, Centreville, and the “Girls Wrestling Champions” story illustrate growing interest.  
4. **Soccer & Field Hockey** – Both have grown in the last two years; the “Orrell overtime goal” and the “Sabres finish strong” playoff run show that the sports attract high‑school and community attention.  
5. **Track & Field / Lacrosse / Softball/Baseball** – Seasonal peaks in spring (March‑May) with regional championships (e.g., “Todd earns four titles; Vikes win boys crown”).

**Secondary sports worth watching:** Volleyball (Queen Anne’s three‑peat), baseball/softball (St. Michael’s Saints, Colonel Richardson), and emerging girls’ programs (girls’ wrestling, field hockey).  

**Recurring themes** that appear across all sports:

- **Rivalries & geography** – Easton vs. Queen Anne’s; Kent Island vs. Stevensville; the “North shutout streak” in soccer.  
- **Coaching transitions** – New head coaches (e.g., Easton soccer’s Gabe Kane, basketball’s first‑year coach at North Dorchester).  
- **Player safety & discipline** – The Carver‑QAH altercation, wrestling weight‑class disputes, and COVID‑era health protocols.  
- **College recruitment** – Senior athletes who are being scouted (basketball’s Gilberto, lacrosse’s Quinn).  
- **Gender equity** – Girls’ wrestling championships, expanding field‑hockey programs, and Title IX discussions at the district level.

---

### 4. Mapping the reporting year – a seasonal workflow  

| Timeframe | Primary Sports | Core Story Types | Suggested Angles |
|-----------|----------------|------------------|-----------------|
| **Late July – Early August** | Football (pre‑season), Soccer (pre‑season) | **Previews** | “A Fine Blend” (QAH football preview), “TALL TASK” (Kent County football preview). Interview coaches, ask about roster cuts, new schemes, and community expectations. |
| **Mid‑August – Mid‑September** | Football (regular season), Basketball (non‑conference), Soccer (early season) | **Game Recaps, Early‑Season Trends** | Highlight standout performances (e.g., Ensminger/Monroy for Warriors), note early injuries, and capture fan attendance numbers. |
| **Late September – Early November** | Football (playoffs race), Basketball (conference play), Lacrosse (regular season) | **Feature Stories, Rivalry Pieces** | Dig into the history of the Easton‑Queen Anne’s rivalry, profile a senior athlete (e.g., Marshall Bailey), explore coaching philosophies (Rob Burnham’s “going back in time”). |
| **Mid‑November – Early December** | Basketball (playoffs), Soccer (regular season), Field Hockey (regular season) | **Playoff Recaps, Human‑Interest** | Capture the emotional weight of “Warriors battle but can’t extend win streak”, or the “Orrell overtime goal” story. |
| **December – Early January** | Winter break – *planning* | **Season Review, Off‑Season Angles** | Compile “Year‑in‑Review” graphics, interview district athletic directors about budget and facility upgrades, preview upcoming winter sports (wrestling, indoor track). |
| **January – March** | Wrestling (tournaments), Indoor Track (championships), Basketball (regular season) | **Tournament Previews, Championship Recaps** | Use “Peake Challenge” (basketball tournament preview) as a template for wrestling previews (Bayside tourney). Highlight the “Girls wrestling champions receive acclamation” as a feature on gender equity. |
| **April – May** | Baseball, Softball, Lacrosse, Outdoor Track | **Championship Coverage, Senior Spotlights** | Focus on “Todd earns four titles; Vikes win boys crown”, “Quinn, Bucs strike quick to earn title”, and senior athlete college‑commit stories. |
| **June – August** | Off‑season (training, camps), Summer leagues | **Community Angles, Facility Stories** | Look at summer camps hosted by local colleges, talk about facility upgrades (e.g., new turf at Queen Anne’s), and preview the upcoming fall sports calendar. |

**Tips for staying ahead:**  

- **Mark every district‑wide tournament** (Peake Challenge, Bayside wrestling tourney, regional track championships) on a master calendar.  
- **Set alerts** for each school’s athletic department page—most post schedules, results, and press releases within 24 hours.  
- **Assign “story windows”**: for each sport, allocate a 2‑week deep‑dive period where you chase feature ideas, then shift to quick‑turn recaps for the remainder of the season.  

---

### 5. Story‑angle toolbox – recurring issues to mine  

| Issue | Example from the archive | Angle to pursue |
|-------|--------------------------|-----------------|
| **Altercations & Discipline** | “QA’s‑Carver playoff cut short by altercation” (Mar 9) | Investigate the district’s policy on on‑court violence, interview coaches on how they manage tempers, and profile a player who turned a disciplinary setback into leadership. |
| **Coaching Changes** | “Warriors survive Bulldogs’ rally” (Sept 20) – first year coach Matt Griffith | Profile a rookie head coach, explore their philosophy versus veteran counterparts, and gauge community reaction. |
| **Gender Equity & Girls’ Programs** | “Girls wrestling champions receive acclamation” (June 7) | Track the growth of girls’ wrestling, compare participation numbers over the last five years, and speak with Title IX officials. |
| **Small‑Town Rivalries** | “Lions push but can’t get ahead of Easton” (May 1) – lacrosse | Write a “Rivalry‑of‑the‑Month” column, pairing a head‑to‑head record with community anecdotes (e.g., local businesses offering “Lions” discounts). |
| **College Recruiting** | “Vince Gilberto’s season‑high 33 points” (Jan 3) | Follow a senior athlete through the recruiting process—camp invitations, campus visits, and the final decision. |
| **Facility & Funding** | No explicit story, but many games at municipal fields (Stevensville, Wye Mills) | Investigate how school budgets affect upgrades (lighting, turf) and the impact on player safety. |
| **Community Impact** | “Warriors extend win streak” (Jan 25) – high attendance | Examine how a winning program boosts local business (restaurants, merch sellers) and community pride. |

---

### 6. Quick‑reference checklist – contacts, locations, and resources  

- **Core Contact List** (update each semester)  
  - Athletic Directors: Brian Mooney (QAH), Harold Somerville (Kent County), Rob Burnham (Cambridge‑South Dorchester)  
  - Media Relations: Bill Haufe (Chesapeake Publishing), Andrea Grabenstein (features)  
  - Coaches: Jeff Hollis, Dionte Hynson, Matt Griffith, Laura Harding, Justin Holland, Jamie Leventry  

- **Key Venues**  
  - **Centreville High School Gym** – QAH Lions basketball, wrestling regionals  
  - **Easton High School Complex** – football, soccer, field hockey, basketball  
  - **Stevensville (Kent Island) Stadium** – lacrosse, wrestling, track championships  
  - **Wye Mills School** – Peake Challenge tournament (basketball)  
  - **Berlin High School** – Bayside wrestling tourney  

- **Annual Event Calendar (high‑lights)**  
  - **July** – Pre‑season football & soccer meetings (district)  
  - **August 10‑15** – Football season opener (local coverage)  
  - **Sept 10** – Soccer season opener (Easton vs. Wicomico)  
  - **Oct 4‑15** – Football rivalry weeks (Cambridge‑South Dorchester vs. Kent County, etc.)  
  - **Nov 1‑15** – Basketball playoffs (regional & district)  
  - **Feb 10** – Peake Challenge basketball tournament  
  - **Mar 20‑30** – Regional wrestling & indoor track championships  
  - **May 1‑20** – Outdoor track, baseball/softball, lacrosse finals  

- **Digital Resources**  
  - Maryland Public Secondary Schools Athletic Association (MPSSAA) site – official brackets, eligibility notices.  
  - School district Facebook pages – live updates, photo albums.  
  - Local radio (WESM, WMAR) – post‑game interviews and community sentiment.  

---

### 7. Best practices for a sustainable beat  

1. **Build trust before the deadline.** Attend a few practices without a recorder, introduce yourself to the booster clubs, and let coaches know you’re there to amplify—not sensationalize—their work.  
2. **Balance speed with depth.** A game recap is essential, but follow each with a 300‑word “what it means” paragraph that links the result to season goals, player milestones, or community impact.  
3. **Leverage multimedia.** Ask coaches for photo permission during practice; use Instagram stories for quick score updates; embed short video clips of key moments (e.g., Orrell’s overtime goal).  
4. **Stay on top of compliance.** High‑school athletes are minors—verify parental consent for any personal profile, and double‑check the MPSSAA eligibility rules before publishing.  
5. **Cross‑publish with local partners.** Offer story teasers to the county’s radio stations; collaborate with the school yearbook for archival photos. This widens reach and builds goodwill.  

---

### 8. Putting it all together – your first 90‑day plan  

| Week | Action | Goal |
|------|--------|------|
| 1‑2 | Meet the **district athletic director** and **key coaches** (football, basketball, wrestling). Collect season preview packets. | Establish primary sources and gather official schedules. |
| 3‑4 | Attend the **first football practice** at Easton and QAH; record anecdotes and photo opportunities. | Build a “human‑interest” bank for future feature pieces. |
| 5‑6 | Cover the **Peake Challenge** (basketball) and **Bayside wrestling tourney**. Gather quotes from coaches like **Boo Ricketts** and **Josh August**. | Deliver tournament previews and recaps; identify standout athletes. |
| 7‑8 | Write a **season‑opening feature** on a senior athlete (e.g., **Vince Gilberto**). Pitch it to the editor as a “local hero” story. | Showcase the human side of the beat, increase readership. |
| 9‑12 | Produce a **mid‑season analysis** on the football rivalry week (Easton vs. North Caroline; Cambridge‑South Dorchester vs. Kent County). Include stats, fan sentiment, and coach commentary. | Position yourself as the go‑to analyst for the community. |
| 13‑14 | Review the **first wave of disciplinary incidents** (e.g., Carver‑QAH game). Interview the district’s compliance officer and produce a short investigative piece. | Demonstrate depth and responsibility in coverage. |
| 15‑16 | Draft a **season‑in‑review calendar** for the next year, noting dates for all major tournaments and preseason meetings. Share it with coaches and editors. | Provide a useful reference and reinforce your role as a beat coordinator. |

---

## Closing Thought  

Covering Eastern Shore sports is less about chasing headline‑grabbing moments and more about weaving together the **people, the place, and the pride** that each game represents.  By knowing the coaches who shape the teams, the athletes who embody the community’s hopes, and the calendar that dictates the rhythm of competition, you’ll turn ordinary recaps into stories that matter to every resident—from the kid on the bleachers to the senior who’s been coaching for 30 years.  

Use this guide as a launchpad, update it with the names and events that surface each season, and you’ll quickly become the trusted voice that the Eastern Shore turns to when it wants to know what’s happening on the field, in the gym, and on the track. Happy reporting!


## Thoughts on v2 ##

I really like this intro: * **Coaches who double as teachers and civic leaders** – they are the gatekeepers of access and the most reliable source of background.
* **Student‑athletes who are also “local kids”** – their families, graduation plans, and college aspirations are part of the story.
* **District and county athletic directors** – they shape schedules, eligibility rules, and funding decisions that affect every sport.
* **Community institutions** – the school board, local businesses (sponsors), and the Eastern Shore’s media ecosystem all influence coverage.

Understanding those relationships is the foundation for any story that goes beyond a simple game recap.


This does a good job setting the stakes for the beat. I need to tell it to cut the part about who to know with specific people becasue it gave me many names who may be meaningless now. 

However I liked the tips on how to reach out to them.

I have to find out a better way to create a sports calendar the format it gave is yuck. 

I like the idea of this: ### 8. Putting it all together – your first 90‑day plan  

But it needs more information to do this better. 

### Final Evaluation

I got my .Json to a point where I could create a beat book but I am far off from a good draft. I need to shift the focus from specific names to general tips. The second draft is better at doing this but still focused too much on names and locations that are easily figured out. 

The best part of the beat book is the start and setting the stakes for high school sports and how to approach it. I want the LLM to add a section on what no to do and failures to avoid. 

Going foward I want to breakdown each section of the guide and have the LLM create my beat book section by section and have it run 5 attempts per section and then decide on what pieces I like best. 