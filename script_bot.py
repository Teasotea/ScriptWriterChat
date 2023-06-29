from dotenv import load_dotenv
import os
import streamlit as st
from streamlit_chat import message


from langchain import OpenAI, PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

load_dotenv()

os.environ['OPENAI_API_TOKEN'] = os.environ.get('OPENAI_API_KEY')

template = """
Prepare 680 - 750 words scenario script for video {input}. Use this info about story: {history}. 
Content: 20-word intro with the keywords from the topic sentence coherently present in it (not forced). 
A full story (with sections if necessary) breaking down the timeline of things. Some formatting rules: 
- Put a full-stop after each header and leave one paragraph space above and below 
- Make Sure Some Symbols Are Written Differently: 
a) Use words for dates: 1970s = nineteen-seventies. 
b) Don't use dollar sign: for instance $20 = 20 dollars OR $20 bond = twenty-dollar bond 
c) Use "to" instead of hypen: 2-10 people = 2 to 10 people 
d) Don't use slashes: 20/20 = twenty-twenty 
e) Any symbol should be properly spelt out: 900km/h = 900 kilometers per hour 
f) Number should be read digit-by-digit: 911 = 9-1-1 OR Boeing 707 = Boeing seven-oh-seven 

Avoid in the storylines: 
- Unnecessary repetition of certain events or plot points in a story. 
- Don't add info that don’t align with the topic or perceived narrative of the story 
- Don't give advice or opinions. Keep it almost strictly story. 

Key things to do: 
- If there’s enough content, just write the story as a timeline of the events. 
- If there’s not enough content, write the story using “narratives”. 
This involves making use of the central theme, or idea, or stereotype, or expected presuppositions of the audience to write the story 

To write a story with the narrative, divide the story into different parts: 
1) Backstory: Introduce the topic and the main event in the story. Do not keep main event from the viewers. 
We need to introduce them event early in a way that will hook them and buttress the narrative that we’ve come up with for the story. 
We need to convince the viewers that it is what they should care about. 
Each time we move to a different topic, make transitions into the next sections with this narrative in mind. 
2) Middle: Here, discuss every other thing we can relate to the story and/or the narrative. 
Tell users about: similar cases like the one we’re discussing that explains why what we’re discussing is important, other events in our own story that are a continuation of the events that have occurred. 
3) End: Conclude with a section reprising the narrative. Everything must be a story, so it should be a continued story on the main events of the topic, 
the conclusion of the story, or another story that fits with the narrative."""

script_prompt = PromptTemplate(
    input_variables=["input", "history"],
    template=template
)

llm = OpenAI(
	temperature=0.1,
	model_name="text-davinci-003"
)

conversation = ConversationChain(prompt=script_prompt, llm=llm, memory=ConversationBufferMemory(ai_prefix="ScriptWriter", human_prefix="MainEditor"), verbose=True)

def generate_response(prompt):
    pred = conversation.predict(input=prompt)
    return pred

start_editor = 'Hi!'

start_writer = 'Hi! I am your ScriptWriter. Specify the topic and social media. I will give you a script'
st.title("ScriptWriter Bot")

if 'generated' not in st.session_state:
    st.session_state['generated'] = [start_writer]

if 'past' not in st.session_state:
    st.session_state['past'] = [start_editor]

def get_text():
    input_text = st.text_input("", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = generate_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
