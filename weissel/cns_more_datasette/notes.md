 CNS More Datasette 10/8/25

 #### Enrichment 1: Keywords or Sentiment

 Run this enrichment and document in `notes.md`:
- Do the results make sense?
    The results are a good attempt at giving 5 key words for each story. The word Chesapeake appeared at least once in almost every batch of keywords. For some stories the last results seemed like more of a stretch but overall they keyworsd are usable. 
- Any surprising patterns?
    There was a good amount of overlap between the tags and the keywords for some stories. Also words like water and coast appeared a good amount. It would be interesting to sort the new keywords by frequency.
- Anything you don't like about this?
    I hated the inconsistent format. Some had bullet points, some had commas, some had numbers. This is not useful if trying to analyze these further. Partially user error as I could have said give me a number before each one. Also some have nothing to seperate the words so it is hard to tell when the 2 word terms start and end. 

#### Generate Embeddings
 What words or phrases did you try?
    I tried Historical Renovations, Fiscal Policy and Religion. 
- Do the results make sense?
    The results seemed accuratley scored and are a good way to group and compare stories. I personally find analysis like this to be very intersting as the decisions on overlap are being made by data rather than human feel. It is hard for a human to quantify how similar two topics are just from reading them as bias may play into that. Using a computer to make this decision allows the results to be accurate. 
- Anything you don't like about this?
    Not particulaurly, but I feel when stories are not similar to the topic at all there is not really a point in assigning them a nuber as they are so not similar to the topic asked. 