from dotenv import load_dotenv
import os
import streamlit as st
from streamlit_chat import message

from langchain import OpenAI, PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


template = """
You are scriptwriter. Prepare 4000-6000 words scenario script for YouTube video {input}.Use this info about story: {history}
Use about 500 words to describe each person. Content: Firstly, intro with the keywords from the topic sentence coherently present in it (not forced), 
then, prepare full story (with sections if necessary) breaking down the timeline of things. Some formatting rules: 
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
in a way that makes it seem like it’s a story that’s being told.

Please, don't make up things. The story should be educative and contain facts. Add as many details as possible.
Please avoid using buzzwords like 'addtionally', 'in this section'... 
Don't repeat name of character too many times. Make sure that all information is in line with the topic and true.
"""

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
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

    PROMPT = PromptTemplate(template=template, input_variables=["input", "history"])

    conversation = ConversationChain(prompt=PROMPT, llm=chat, memory=ConversationBufferMemory(ai_prefix="ScriptWriter", human_prefix="MainEditor"), verbose=True)

    def generate_response(prompt):
        pred = conversation.predict(input=prompt)
        return pred

    with st.sidebar:
        user_input = st.text_input("Topic for script: ", key="user_input")

        if 'generated' not in st.session_state:
            start_writer = 'Hi! I am your ScriptWriter. Specify your topic in the slider. I will give you a script'
            st.session_state['generated'] = [start_writer]

        if 'past' not in st.session_state:
            st.session_state['past'] = ['Hi!']

        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = generate_response(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

if __name__ == '__main__':
    main()