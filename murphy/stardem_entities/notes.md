# star-dem entities — cat murphy, nov. 5

well, i managed to overload copilot AND get rate-limited by groq while working on my FIRST script. then i got rate-limited twice more, and overloaded copilot again.

anyway.

i thought about doing an uncomplicated prompt to start to see how the llm did with relatively minimal instruction. but i'm neurotic and that didn't happen. 

sooooooo i started by writing a prompt that asked for for seven new fields: `content_type`, `people`, `locations`, `institutions`

i gave it relatively similar (though slightly tweaked) content type definitions to the ones i used for the `stardem_topics` assignment — basically i just added "sports" as a content type and gave the llm some examples of each type. i defined `people`, `locations` and `institutions` the way you'd expect.

but then i also had the idea — and i'm somewhat proud of this — to add a couple more arrays with some more specifics on the location/story topic. so, i decided to define three new fields: `events`, `municipalities` and `county`. i wanted `events` only because i feel like some of things they're talking about — farmer's markets, food pantries, etc. — aren't really institutions, but they're kind of important context. i wanted `municipalities` because `locations` could mean a lot of things, and i wanted a field specifically for the names of the towns involved in the story. that also meant i changed my original definition of `locations` to be geared more toward places within municipalities, like rivers and neighborhoods and parks. but most of all, i wanted a `county` field because i was thinking about how to best organize these in the context of a beat book. well, in order to do that, we would need what i brought up in class the other day — a list of the municipalities within each of the five counties the star-dem covers. this was kind of challenging, because the official maryland website lists only official municipalities, not unincorporated communities or cdps. i ultimately used wikipedia's lists. i also gave it three examples of how to extract the metadata — one news example, one calendar example and one sports example.

(note that my prompt wasn't structured to give proper json output, so copilot wrote me a nice script to fix that lol — except that didn't really fix it either and it's still low-key impossible to tell how it did from the .db. also, it only ran ~190 or so before it rate-limited me)

from what i can see, this version of my script did ... ok. the people and institution fields were meh — i didn't specify how many or what kind of people and institutions it should pull, so it pulled all of them. now, this was intentional; i didn't want to start narrow. so, the mediocrity was somewhat anticipated. but the municipality and county fields seemed to do ... good enough? honestly, the county field was probably the best. and i know this isn't exactly high praise, but for a first shot i'm ok with it. it definitely didn't populate some fields, and it definitely didn't always follow directions — namely the part where i said to not include the author's name in the people field. the events field was all over the place — usually it contained either nothing or 10 things, which, to be fair, is in part because i had a lot of calendars in my sample. hence why some looked like this:

`["Tuskegee syphilis experiment", "in vitro fertilization", "Woolworth's sit-in protests" "Air France Concorde crash", "Wikileaks Afghanistan war records", "Ukrainian presidential phone call", "Indigenous residential schools apology"]`

while some looked like this:

`["U.S.A.T. Dorchester sinking"]`

the locations were also kind of a mess. i'd get some like this:

`["Decker Theatre (Chestertown)", "Gibson Center (Chestertown)", "Kent Island Senior Center (Stevensville)"]`

and some like this:

`["Annapolis", "Arundel Olympic Swim Center (Annapolis)", "Rams Head Tavern (Annapolis)", "Rams Head On Stage (Annapolis)", "Island Pub (Stevensville)", "Rehoboth Ale House On the Mile (Rehoboth Beach)", "Lefty's Alley & Eats (Lewes)", "Market Street Public House (Denton)", "Cult Classic Brewing (Stevensville)", "USA Dance Eastern Shore (Easton)", "YMCA Washington (Easton)", "Nanticoke Sportsmen's Club (Seaford)", "Severna Park", "Jones Station Rd (Severna Park)", "25 Jones Station Rd (Severna Park)", "Buckingham Elementary School (Berlin)", "Severna Park High School (Severna Park)", "Severna Park MS (Severna Park)", "Penisula Farm Rd (Arnold)", "Riviera Beach ES (Pasadena)", "Pasadena", "Worcester County Recreation Center (Snow Hill)", "Thompson Island Brewing Company (Rehoboth Beach)", "Reynolds Tavern and 1747 Pub (Annapolis)", "Ocean City Performing Arts Center (Ocean City)", "The Avalon Theatre (Easton)", "Macum Creek Concerts (Kent Island)", "Avalon Foundation Inc (Easton)", "Kent School (Chestertown)", "Stevensville Middle School (Stevensville)", "Lighthouse Christian Academy (Stevensville)", "Chesapeake Middle School (Pasadena)", "Annapolis Senior Center (Annapolis)"]`

yeah. exactly. then again, i could see how this might be helpful if you were looking for community organizations, which is why i'm also hesitant to cut it down.

i appreciated that for the most part the (*municipality*) instruction worked.

(i'll also note that datasette kept failing for some reason. like, it would crash every time i tried to facet by something using it's clickable "suggested" facets, which made it even more difficult to analyze the data.)

but, yeah — it was fine-ish. somewhat on par with what i expected, i guess.

now, my second script made the issues i had with my first one look like nothing. so, after the first run, i wanted to do a couple things. first, i wanted to provide the llm with county information outside of the star-dem's coverage areas. i realized while looking through my first script's output that there were mentions of maryland towns outside of the five counties that the star-dem covers — whether for sports or for whatever other reason. so i added all 19 other md counties to my array, along with every municipality within them. it took a while. i also added back into my script the topic list i used in the last assignment, with some edits meant to reflect the updated topic definitions i proposed to address some of the flaws in my last list. i mean, i did this because ... well, why not? i kind of wanted to test how much i could get groq to do — I'LL COME BACK TO THIS. 

given that the first script's results for the people field weren't particularly impressive, i narrowed it to focus on "important" figures — which i defined as "people like politicians, political candidates, coaches, community leaders, public officials, board members and council members." i also added another new field: sources. i didn't want another list of the people in the story — i wanted a list of the *TYPES* of people. basically, government officials, politicians, residents, advocates, organizers, community leaders, coaches. i also edited my definition of an institution, because the line between that and a location was blurry at best.

... just one problem. it rate-limited me after 55 stories this time, and i had to switch models mid-way through (hence `stardem_with_entries_2_ish.json`). so, apologies for what is admittedly a very strange analysis.

so, for the first 55 entries, which i did with groq/openai/gpt-oss-120b, here's my analysis:

the municipality and county fields were honestly not bad. for example, here's what it did for title "Groove City Festival - Cambridge community enjoys dancing, good eats, street fair":

``` json
{
    "content_type": "News",
    "topic": "Arts & Culture",
    "people": [
        "Albert C. Jones Jr.", 
        "Veronica Taylor", 
        "Victoria Jackson-Stanley", "Lois McCord"
    ],
    "sources": [
        "politicians", 
        "community leaders", 
        "organizers"
    ],
    "events": ["Groove City Culture Fest"], 
    "locations": ["Pine Street (Cambridge)"], 
    "municipalities": ["Cambridge"],
    "county": ["Dorchester County"],
    "institutions": [
        "Groove City Black Heritage and Cultural Group Inc.", 
        "Universal African Dance and Drum Ensemble", 
        "Omega Psi Phi", 
        "City of Cambridge", 
        "Elks Lodge", 
        "Maryland Heritage Way", 
        "Dorchester Center for the Arts", 
        "Delta Sigma Theta"
    ]
}
```

i mean ... i don't hate it. the institutions were a bit much — there are probably too many, in my opinion, at least in the sense that some aren't necessarily "searchable" and aren't likely to be used again, like the sorority names. it would probably be wise to cut it to "important" organizations, which i kind of tried to do between the first and second script, but it didn't work very well, clearly.

here's another ok one for "It's about community - Chesapeake Bay Walk to Defeat ALS set for Oct. 22 in Centreville"

``` json
{
    "content_type": "News",
    "topic": "Sports & Recreation",
    "people": [
        "Pam Clark Edwards", 
        "Meredith Kulbacki", 
        "Morgan Edwards", 
        "Fred Edwards", 
        "June Clark", 
        "Jeff", 
        "Connie Dean", 
        "Barb Thompson", 
        "Bobbie King", 
        "Tara Huang"
    ],
    "sources": [
        "residents", 
        "organizers"
    ],
    "events": ["Chesapeake Bay Walk to Defeat ALS"], 
    "locations": [
        "Route 18 Park (Centreville)", 
        "Queenstown Harbor (Queenstown)", 
        "Rockville (Rockville)"
    ], 
    "municipalities": [
        "Centreville", 
        "Queenstown", 
        "Rockville", 
        "York"
    ],
    "county": [
        "Montgomery County", 
        "Queen Anne's County", 
        "Talbot County"
    ],
    "institutions": [
        "ALS Association", 
        "Johns Hopkins", 
        "Ebb Tide Tent & Party Rentals", 
        "Queen Anne's County Parks and Recreation", 
        "Queen Anne's County Public Schools", 
        "Draper Brothers liquor store", 
        "Pam's Praying Pineapples", 
        "Team Chesapeake Bay"
    ]
}
```

now, listen, there are some repeats and a few less than ideal entries — rockville is in both locations and municipalities, one of the people named is just "jeff" — but again, it's not the worst. admittedly it looks slightly cleaner than the last one.

of course, there were some ... um ... weirder ones.

for most obituaries, the "event" listed was a variation of `["Funeral services"]`. one today in history had `["Hurricane Katrina", "U.S. withdrawal from Afghanistan"]` — the today in history entries always had the funniest ones. one news article had `["Ribbon Cutting"`] as an event. one had `["A Rock Sails By"]`. there was `["Harrison Street Storm Drain Improvement Project"`]. so, yeah, i mean, some of it was insane.

the institutions and locations still overlapped quite a bit, so things like "Queen Anne's County Centre for the Arts (Centreville)" and "Kent Island Library (Kent Island)" would end up in both fields. the llm really struggled to tell what was important, so it would pull everything, hence metadara like this:

`["Heroes & Icons", "Freeform", "getTV", "The Adventures of Superman", "Freaky Friday", "Magnum, p.i."]`

many were completely fine, though, like these:

`["Building African American Minds (BAAM)", "Easton Town Council", "Talbot County Chamber of Commerce", "Unity Landscapes"]`

`["NAACP Caroline County Branch", "Federalsburg Town Council", "Caroline County Health Department", "ACLU of Maryland", "United States District Court", "Caroline County Sheriff's Office", "Federalsburg Police Department", "Men For Change"]`

i liked my sources field, but it definitely needs to be refined. i know what i want, but i'm not sure how to express it. like, i want to be able to look at the story data and see which stories feature quotes from residents, politicians, etc. but i ultimately, i guess, would want a db with something that said *Easton* resident, *Cambridge* politician, *Denton* community leader. maybe that can be adjusted for next time, but i would want to hear what others think because i want something in this arena but i'm sure others would have ideas on how to refine it to make it more useful.

ok, and here's my analysis of the rest of the entries, which i had to run on groq/meta-llama/llama-4-maverick-17b-128e-instruct after getting rate-limited: comparatively, **it sucked.**

this model did SO MUCH worse. and that's really interesting, too — because i really liked this model last time. but the metadata was just ... atrocious. like, mostly unusable. and i don't think it's the prompt, because it seemed to work relatively well on the first 55 using a different model. i don't want to, like, do a deep dive, but outside of the `content_type` and `topic` fields, it failed a good amount of the time to populate the fields. it's difficult to find a story for which it extracted metadata for each of the fields i added. in one case, one of the locations listed was `["pond (Denton)"]`. nuff said.

uv run sqlite-utils insert stardem_entities_2_ish.db stories stories_with_entities_2_ish.json --pk docref
uv run datasette stardem_entities_2_ish.db