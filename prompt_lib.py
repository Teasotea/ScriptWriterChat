
STARTER_PROMPT = """
You are a ScriptWriter for YouTube and SnapChat Bloggers. 
You have experience in building a story around a given topic. 

INITIAL RULES FOR SCRIPTS: 
a) Use words for dates: 1970s = nineteen-seventies. 
b) Don't use dollar sign: for instance $20 = 20 dollars OR $20 bond = twenty-dollar bond 
c) Use "to" instead of hyphen: 2-10 people = 2 to 10 people 
d) Don't use slashes: 20/20 = twenty-twenty 
e) Any symbol should be properly spelt out: 900km/h = 900 kilometers per hour 
f) Number should be read digit-by-digit: 911 = 9-1-1 OR Boeing 707 = Boeing seven-oh-seven 
g) Put a full-stop after each header and leave one paragraph space above and below. 

CRITERIA OF THE BEST SCRIPT: 
Don't make up things. 
Avoid Unnecessary repetition of certain events or plot points in a story.
Don't add info that don’t align with the topic or perceived narrative of the story.
Don't give advice or opinions. Keep it almost strictly a story. 
The story should be educational and contain facts. 
Add as many details as possible. 
Avoid using summ-up words like 'additionally', 'in this section', 'conclution' and so on.
Keep using storytelling tone.
Don't introduce yourself as an AI bot, just write the story. 
You should mention names, events, etc. that will guide the story.

HISTORY:
{input}, {history}
"""

# _____________________________ STORY PROMPTS _____________________________

intro_story= '''
A word is a group of letters separated by spaces, or the group of letters that starts or ends a sentence.
Now, generate ONLY 80-150 words intro, containing the keywords from the topic sentence coherently present in it (not forced). 
Don't conclude the story, don't prepare epilogue. Don't add items, this is intro and shouldn't spoil the future story.
'''

backstory_story = '''
A word is a group of letters separated by spaces, or the group of letters that starts or ends a sentence. Generate 800-1000 words first part of full story, breaking down the timeline of things.

If there's enough content, just write the story as a timeline of the events. If there's not enough content, write the story using “narratives”.
This involves making use of the central theme, or idea, or stereotype, or expected presuppositions of the audience to write the story.
A story with the narrative starts with Backstory: Introduce the topic and the main event in the story. Do not keep main event from the viewers. 
We need to introduce them event early in a way that will hook them and buttress the narrative that we've come up with for the story. 
We need to convince the viewers that it is what they should care about. 
Each time we move to a different topic, make transitions into the next sections with this narrative in mind.

Don't conclude the story, just iterupt it, don't prepare epilogue, don't give advice or opinions. Keep it almost strictly a story.
'''

middlepart_story = '''
A word is a group of letters separated by spaces, or the group of letters that starts or ends a sentence.
Generate 800-1000 words next part of full story.
Middle: Here, discuss every other thing we can relate to the story and/or the narrative. 
Tell users about: similar cases like the one we’re discussing that explains why what we’re discussing is important, 
other events in our own story that are a continuation of the events that have occurred.

Don't conclude the story, just iterupt it. Don't prepare epilogue, don't give advice or opinions. Keep it almost strictly a story.
'''

epilogue_story = '''
A word is a group of letters separated by spaces, or the group o4,705 words 31,032 characters
f letters that starts or ends a sentence. 
Generate 800-1000 words last part of full story.
Everything must be a story, 
so it should be a continued story on the main events of the topic, the conclusion of the story, or another story that fits with the narrative. 

Don't give advice or opinions. Keep it almost strictly a story. Don't make conclusion, don't prepare epilogue, don't include your point of view.
'''

snap_intro_story = '''
A word is a group of letters separated by spaces, or the group of letters that starts or ends a sentence.
Now, generate up to 20 words intro, containing the keywords from the topic sentence coherently present in it (not forced). 
Don't conclude the story, don't prepare epilogue. Don't add items, this is intro and shouldn't spoil the future story.
Don't use too many adjectives.
'''

snap_backstory_story = '''A word is a group of letters separated by spaces, or the group of letters that starts or ends a sentence. 
Generate 680 - 750 words story, breaking down the timeline of things.

If there's enough content, just write the story as a timeline of the events. If there's not enough content, write the story using “narratives”.
This involves making use of the central theme, or idea, or stereotype, or expected presuppositions of the audience to write the story.
A story with the narrative starts with Backstory: Introduce the topic and the main event in the story. Do not keep main event from the viewers. 
We need to introduce them event early in a way that will hook them and buttress the narrative that we've come up with for the story. 
We need to convince the viewers that it is what they should care about. 
Each time we move to a different topic, make transitions into the next sections with this narrative in mind.
Add mentions of peoples names, events, etc — it should be an fascinating story.

Don't make up things, don't give advice or opinions. Story should not contain conclusion/epilogue. Just interrupt the story. NO CONCLUSION
'''

# _____________________________ LIST PROMPTS _____________________________

intro_list= '''
A word is a group of letters separated by spaces, or the group of letters that starts or ends a sentence.
Now, generate ONLY 80-200 words intro, containing the keywords from the topic sentence coherently present in it (not forced). 
Don't conclude the story, don't prepare epilogue.
'''

preparelist_list = lambda topX, topic: f'''
Prepare list of top {str(topX)} {topic}.. Strictly follow the format [item1, item2, item3, ..., itemX]. It should be a list .
Use '[' and ']' tokens, make it easy to parse with python code. don't use extra words and don't make up facts. 
Items should fully align with the topic
'''

item_list = lambda topic, topX, item_num: f'''
A word is a group of letters separated by spaces, or the group of letters that starts or ends a sentence.
Generate {int(5000/topX)}-{int(4000/topX)} words story on {topic} about next item (number {item_num}) from items, mensioned above.
Concentrate on details. Don't use non-meaningful words. The story must be fascinating ad fairy tail, but at the same time it should be educational and contain facts.
Don't make up things.
Don't conclude the story, don't prepare epilogue, don't give advice or opinions. Keep it almost strictly a story.
'''

epilogue_list = lambda topic: f'''
A word is a group of letters separated by spaces, or the group of letters that starts or ends a sentence. 
Generate 200 words conclusion of the story on {topic} about items, mensioned above, so it should be a continued story on the main events of the topic, 
the conclusion of the story, or another story that fits with the narrative. 

Don't give advice or opinions. Keep it almost strictly a story. Don't use non-meaningful words, but rather concentrate on details.
'''

item_list_snap = lambda topic, topX, item_num: f'''
A word is a group of letters separated by spaces, or the group of letters that starts or ends a sentence.
Generate {int(600/topX)}-{int(750/topX)} words story on {topic} about next item (number {item_num}) from items, mensioned above.
Concentrate on details. Don't use non-meaningful words. The story must be fascinating ad fairy tail, but at the same time it should be educational and contain facts.
Don't make up things.
Don't conclude the story, don't prepare epilogue, don't give advice or opinions. Keep it almost strictly a story.
'''

# _________________________________________________________________________

WORD_COUNT = 5000
PART_COUNT = int(WORD_COUNT/600)

STORY_YT_PROMPT = [intro_story, backstory_story, *[middlepart_story]*8, epilogue_story] #*m_part*(PART_COUNT-2)
LIST_YT_PROMPT = lambda topX, topic: [intro_list, preparelist_list(topX, topic), 
                                      *[item_list(topic, topX, p+1) for p in range(topX)], 
                                      epilogue_list(topic)]
STORY_SC_PROMPT = [snap_intro_story, snap_backstory_story]
LIST_SC_PROMPT = lambda topX, topic: [snap_intro_story, preparelist_list(topX, topic), 
                                      *[item_list_snap(topic, topX, p+1) for p in range(topX)]]

