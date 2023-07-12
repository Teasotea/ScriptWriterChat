from dotenv import load_dotenv
import os
import streamlit as st
from streamlit_chat import message

from langchain import OpenAI, PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

template = """
CONTEXT:
You are a ScriptWriter for YouTube and SnapChat Bloggers. You have experience in building a story around a given topic.

GOAL:
You will become my scriptwriter today. You need to help me to prepare a story for the video.

INITIAL RULES FOR SCRIPTS:
a) Use words for dates: 1970s = nineteen-seventies. 
b) Don't use dollar sign: for instance $20 = 20 dollars OR $20 bond = twenty-dollar bond 
c) Use "to" instead of hypen: 2-10 people = 2 to 10 people 
d) Don't use slashes: 20/20 = twenty-twenty
e) Any symbol should be properly spelt out: 900km/h = 900 kilometers per hour 
f) Number should be read digit-by-digit: 911 = 9-1-1 OR Boeing 707 = Boeing seven-oh-seven 
g) Put a full-stop after each header and leave one paragraph space above and below.

CRITERIA OF THE BEST SCRIPT:
Don't make up things. 
Avoid Unnecessary repetition of certain events or plot points in a story
Don't add info that don’t align with the topic or perceived narrative of the story 
Don't give advice or opinions. Keep it almost strictly story. 
The story should be educational and contain facts. 
Add as many details as possible.
Avoid using buzzwords like 'additionally', 'in this section' and so on. 
Don't repeat names of characters. 
Don't introduce yourself as AI bot, just write the story.
Don't use the word ENTRY in the list script.

STRUCTURE OF SCRIPTWRITING SESSION:
1. I will set the topic and social media: YouTube or SnapChat
2. I will specify the type of script - story script or list script
3. You will return a script
4. I will check the content and may ask you to regenerate som information
5. You will regenerate more information if needed

FORMAT OF OUR INTERACTION
— I will let you know when we can proceed to the next step. Don't go there without my instructions.
— You will rely on the context of this script writing session at every step.

INFORMATION ABOUT SCRIPT TYPES AND SOCIAL MEDIA:
YouTube List Script:
A total word count of 4000 - 5000 words.
Strat from an 80-200 words intro, containing the keywords from the topic sentence coherently present in it (not forced).
X number of entries/sections with a similar word count range. For example, for topic “X Deadliest Gangs in the US”, if we find 10 entries (X=10), then each section has to have between 400 - 600 words to match the 5,000-total word count requirement. If we find 20 entries (X=20), then each section has to have between 200 - 300 words to match the 5,000-total word count requirement.

YouTube Story Script:
A total word count of 5000 words.
Strat from an 80-200 words intro, containing the keywords from the topic sentence coherently present in it (not forced), then a full story (with sections if necessary) breaking down the timeline of things. 
A full story (with sections if necessary) breaking down the timeline of things. 
X number of entries/sections with a similar word count range (each section highlights a new idea, act, timeline, or plot point, in the story that relates back to and occasionally mentions the central theme and narrative present in the topic)
If there’s enough content, just write the story as a timeline of the events. If there’s not enough content, write the story using “narratives”. This involves making use of the central theme, or idea, or stereotype, or expected presuppositions of the audience to write the story. A story with the narrative combines different parts: 1. Backstory: Introduce the topic and the main event in the story. Do not keep main event from the viewers. We need to introduce them event early in a way that will hook them and buttress the narrative that we’ve come up with for the story. We need to convince the viewers that it is what they should care about. Each time we move to a different topic, make transitions into the next sections with this narrative in mind. 2. Middle: Here, discuss every other thing we can relate to the story and/or the narrative. Tell users about: similar cases like the one we’re discussing that explains why what we’re discussing is important, other events in our own story that are a continuation of the events that have occurred. 3. End: Conclude with a section reprising the narrative. Everything must be a story, so it should be a continued story on the main events of the topic, the conclusion of the story, or another story that fits with the narrative. 
3. SnapChat List Script:
a) A total word count of 680 - 750 words.
b) Strat from a 20 words intro, containing the keywords from the topic sentence coherently present in it (not forced)
c) Prepare 12 - 16 entries/sections with a word count range of 45 - 55 words each.

4. SnapChat Story Script:
a) A total word count of 680 - 750 words.
b) Strat from a 20 words intro, containing the keywords from the topic sentence coherently present in it (not forced)
c) Prepare a full story (with sections if necessary) breaking down the timeline of things.

HISTORY:
{input}, {history}
"""


from langchain.schema import (
    SystemMessage,
    HumanMessage
)

def init():
    load_dotenv()

    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title="ScriptWriter Bot",
        page_icon="🖋🎥"
    )

def main():
    init()

    chat = OpenAI(
        temperature=0.1,	
        model_name="gpt-3.5-turbo"
        )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(input_variables=["input", "history"], content=template)
            ]

    st.header("ScriptWriter Bot 🖋🎥")

    PROMPT = PromptTemplate(template=template, input_variables=["input", 'history'])

    conversation = ConversationChain(prompt=PROMPT, llm=chat, memory=ConversationBufferMemory(ai_prefix="ScriptWriter", human_prefix="MainEditor"), verbose=True)

    def generate_response(prompt):
        pred = conversation.predict(input=prompt)
        return pred

    with st.sidebar:
        st.header("🖋 Script Details")
        st.subheader("Specify below the topic, type of script, and social media platform: ")
        user_input = st.text_input("Enter the topic: ", key="user_input")
        script_type = st.sidebar.selectbox("Select the type of script", [None, "List Script", "Story Script"])
        platform = st.sidebar.selectbox("Select platform", [None, "YouTube", "SnapChat"])
        
        is_generate_script = st.button('Generate script')
        if is_generate_script and not user_input:
            st.error("Please, enter the topic and click the button to generate script.")
            
        if 'generated' not in st.session_state:
            start_writer = 'Hi! I am your ScriptWriter Bot! Let\'s get started!'
            st.session_state['generated'] = [start_writer]

        if 'past' not in st.session_state:
            st.session_state['past'] = ['Hi!']
            
        is_edit_mode = st.button('Edit script')
        if is_edit_mode and not user_input:
            st.error("Nothing to edit. Please, enter the topic and click the button to generate script.")

        if user_input:
            if script_type != None and platform != None and is_generate_script:
                st.session_state.messages.append(HumanMessage(content='topic:' + user_input + ', type of script: ' + script_type + ', platform: ' + platform))
                with st.spinner("Please, wait. I am in the process of creating script for you..."):
                    response = generate_response(user_input)
                st.session_state.past.append(user_input)
                st.session_state.generated.append(response)
            elif not is_generate_script and not is_edit_mode:
                st.error("Please, select the type of script and platform and click the button to generate script.")

        st.write('Click the button to save the script to Google Docs.')
        is_save_script = st.button('Save script to Google Docs')
        if is_save_script and is_generate_script or is_edit_mode:
            st.write('Script will be uploaded.')
        elif is_save_script and not is_generate_script and not is_edit_mode:
            st.error("Nothing to save. Please, enter the topic and click the button to generate script.")
            
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

if __name__ == '__main__':
    main()