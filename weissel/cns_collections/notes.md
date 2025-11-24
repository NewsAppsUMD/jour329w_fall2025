 "CNS Collections - Sports 10/15/25

- What topic did you choose? Sports
- How many stories are in your topic? 265

### Design Your Metadata Schema
I added "sport" for the type of sport so I know the focus of what it is. And I added "level" to know what type of compition is the focus whether it may be NFL or middle school. 


**Required Fields (all beats should have these):**
- **people**: Array of key people mentioned (names only)
- **geographic_focus**: Primary location (county, city, region, or "statewide")
- **key_institutions**: Organizations, agencies, companies involved
- **sport**: The name of the sport that the story focuses on
- **Level** The level of compeition the story is focused on (youth, high school, College, Professional)

### Analysis and Insights

Using facets and filters, explore patterns in your beat (you should facet by array for metadata or tags):

1. **Key Players**: Who appears most frequently?
    The LLM failed to assigned a person for 113 of the stories so that left many without data for this. However the way it appears when I facet is that if two players are together in one instance but not the other they show up as different people. So "Jadyen Daniels, Jaylen Hurts" shows up seperatley than "Jayden Daniels, Lamar Jackson".
    In other words Jayden Daniels should show up twice but the lumped together with the other people with it. This made it very difficult to see who appears the most. 

2. **Geographic Patterns**: Which areas get the most coverage?
    The same above was true but College Park appeared by far the most often. As well as Baltimore, D.C., Maryland and Annapolis. This is to be expected. 

3. **Institutional Network**: Which organizations appear in stories?
    The NFL got the most stories. This would make sense given the level of coverage and location of CNS. 

    For my topics, sport and level...football and basketball appeared the most and "professional" was the most common tag for level. 


### Evaluation

- What did the structured metadata reveal about this beat?
    It revealed that the CNS sports coverage is mainly on professional sports with a focus on football and basketball. I was suprised that more coverage is not on local or college level sports. It also revealed that the beat is a bit all over the place as many different topics are covered in the sports field. 
- Does your `prototype.md` result seem useful? What does it do well and what does it not do well?
    It seems like it is on the path to being useful but I don't think the people category is that helpful. The best category was the level of sport and the worst was people. 
- Did you change your prompt, and if so, how? Did that work better?
    N/A. Will adjust in the future assignment. 
- What would you do differently with more time or data?
    I would find out how to seperate when using the facet feature. I plan to add a category that describes what type of sports story it is. This will help me in knowing what the coverage is like. For example if the stories are business focused or statistical focues or if they are mostly game recaps. A possible issue is with the sports reporting capstone by Mark Hyman there will be stories that are hyper focused on certain topics and we may need to remove those to get a better sense of the "beat" as opposed to hyper-focused work. 