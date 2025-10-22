# cns edited prompts — cat murphy, oct. 21

## first edited prompt — i tried to get it to really focus on producing reporting *ideas* but it sucked and gave me mostly bullets

Use specific examples from the attached JSON to produce a descriptive but focused narrative guide in Markdown format that an early-career journalist unfamiliar with the area could read to understand the topic, including the key people, locations, current issues and institutions. 

Keep in mind that this is not a historical guide. It is meant to give a new reporter a place to start when they arrive — meaning it should focus primarily on what needs to be covered rather than what has been covered. Suggest stories that haven't been covered, haven't gotten enough coverage or have been covered but may need to be followed up on. 

Be careful about stories that are ongoing or not resolved, such as longer-term events, active lawsuits, policy debates, etc.; identify unfinished reporting, but include a caveat to let the reporter know that it is unclear if the issue has been resolved. Give more weight to stories published in the last year. If a timeline is a fundamental part of the overall story, mention that, but don’t over-emphasize older elements. 

The language should be business casual but easy enough for a high schooler to read. It should not be primarily a list of bullet points, but you can use bullet points for lists of proposed sources or questions relevant to a suggested story angle. 

Make sure you introduce and explain ideas, people and issues with substantive but concise language. Not too many adjectives. Cite stories that may provide useful context, including the story's headline, the link, and the month and year of publication.

cat edited_prompt.txt enhanced_beat_stories_immigration.json | uv run llm -m "claude-sonnet-4.5" > immigration_prototype.md

## second edited prompt — was going for "use as few words as possible" to see if it would sharpen it's response and keep it from getting lost in the sauce; worked pretty well

Using Markdown format, produce a detailed narrative guide for an early-career journalist unfamiliar with the area that would allow them to understand the topic and the relevant people, locations, current issues and institutions. 

It should focus on what needs to be covered rather than what has been covered. Suggest ideas and questions for stories that haven't been covered, are undercovered or need to be followed up on. Be careful about stories that are ongoing or not resolved; include a caveat to let the reporter know that it is unclear if the issue has been resolved. Give more weight to stories published in the last year.

The language should be business casual but easy enough for a high schooler to read. It should not be primarily a list of bullet points. Make sure you introduce and explain ideas, people and issues with substantive but concise language. Not too many adjectives. Cite relevant stories with the headline, link, and month and year of publication.

cat edited_prompt.txt enhanced_beat_stories_immigration_no_content.json | uv run llm -m "claude-sonnet-4.5" > immigration_prototype_4_no_content.md

cat edited_prompt.txt enhanced_beat_stories_immigration.json | uv run llm -m "claude-4-sonnet" > immigration_prototype_5_claude_4_sonnet.md

cat edited_prompt.txt enhanced_beat_stories_sports.json | uv run llm -m "claude-sonnet-4.5" > sports_prototype.md

cat edited_prompt.txt enhanced_beat_stories_education_no_content.json | uv run llm -m "claude-sonnet-4.5" > education_prototype.md

cat edited_prompt.txt enhanced_beat_stories_sports_no_metadata_no_content.json | uv run llm -m "claude-sonnet-4.5" > sports_prototype_2.md

## third edited prompt — straight up just wanted to be bossy

You're a newsroom assistant. Using Markdown format, you need to produce a detailed narrative guide for an early-career journalist unfamiliar with the area to help them understand the topic and the relevant people, locations, current issues and institutions. 

You need to focus on what needs to be covered rather than what has been covered. You must suggest ideas and questions for stories that haven't been covered, are undercovered or need to be followed up on. You have to be careful about stories that are ongoing or not resolved; always include a caveat to let the reporter know that it is unclear if the issue has been resolved. You need to more weight to stories published in the last year.

DO NOT create primarily a list of bullet points. Make sure you thoroughly introduce and explain ideas, people and issues with substantive but concise language. Do not use too many adjectives. No longer than 300 lines. Always cite relevant stories with the headline, link, and month and year of publication. 

cat edited_prompt.txt enhanced_beat_stories_immigration.json | uv run llm -m "claude-sonnet-4.5" > immigration_prototype_3.md