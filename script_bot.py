# from nltk.tokenize import word_tokenize
# import nltk
# nltk.download('punkt')

from dotenv import load_dotenv
import os
import streamlit as st
from streamlit_chat import message

from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

from prompt_lib import STARTER_PROMPT, STORY_YT_PROMPT, LIST_YT_PROMPT, STORY_SC_PROMPT, LIST_SC_PROMPT
from langchain.schema import (SystemMessage, HumanMessage)

SOCIAL_MEDIA = ['YouTube', 'SnapChat']
SCRIPT_TYPE = ['Story Script', 'List Script']

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
    chat = ChatOpenAI(
        temperature=0.1,	
        model_name = "gpt-3.5-turbo"
        )
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(input_variables=["input", "history"], content=STARTER_PROMPT)
            ]
        
    st.header("ScriptWriter Bot 🖋🎥")
    PROMPT = PromptTemplate(template=STARTER_PROMPT , input_variables=["input", 'history'])
    conversation = ConversationChain(prompt=PROMPT, llm=chat, memory=ConversationBufferMemory(ai_prefix="ScriptWriter", human_prefix="MainEditor"), verbose=True)
    short_conversation = ConversationChain(prompt=PROMPT, llm=chat, verbose=True)
    
     # generate a function  that should do try exept and return error message if the response is too long 
    def generate_response(prompt):
        try:
            return conversation.predict(input=prompt)
        except:
            print('Conversation is too long. Trying to generate response anyway.')
            return short_conversation.predict(input=prompt)
        
        # if len(conversation.predict(input=prompt)) <= 1500:
        #     pred = conversation.predict(input=prompt)
        # else:
        #     short_conversation = ConversationChain(prompt=prompt, llm=chat, verbose=True)
            
    with st.sidebar:
        st.header("🖋 Script Details")
        st.subheader("Specify below the topic, type of script, and social media platform: ")
        user_input = st.text_input("Enter the topic: ", key="user_input")
        script_type = st.selectbox("Select the type of script", [None, "List Script", "Story Script"])
        
        if script_type == "List Script":
            topX = st.text_input("Enter number of items in the list (Top X..), X =", key = "top X")
            if topX: topX = int(topX)
            
        platform = st.selectbox("Select platform", [None, "YouTube", "SnapChat"])
        
        is_generate_script = st.button('Generate script')
        if is_generate_script and not user_input:
            st.error("Click the \"Generate script\" button to generate script.")
            
        if 'generated' not in st.session_state:
            start_writer = 'Hi! I am your ScriptWriter Bot! Let\'s get started!'
            st.session_state['generated'] = [start_writer]

        if 'past' not in st.session_state:
            st.session_state['past'] = ['Hi!']
            
        is_edit_mode = st.button('Edit script')
        if is_edit_mode and not user_input:
            st.error("Nothing to edit. Please, enter the topic and click the button to generate script.")
        
        st.write('Click the button to save the script to Google Docs.')
        is_save_script = st.button('Save script to Google Docs')
        if is_save_script and is_generate_script or is_edit_mode:
            st.write('Script will be uploaded.')
        elif is_save_script and not is_generate_script and not is_edit_mode:
            st.error("Nothing to save. Please, enter the topic and click the button to generate script.")

    if user_input and script_type and platform:
        
        if script_type == SCRIPT_TYPE[0] and platform == SOCIAL_MEDIA[0]:
            PROMPT_ORDER = STORY_YT_PROMPT
        elif script_type == SCRIPT_TYPE[0] and platform == SOCIAL_MEDIA[1]:
            PROMPT_ORDER = STORY_SC_PROMPT
        elif script_type == SCRIPT_TYPE[1] and platform == SOCIAL_MEDIA[0]:
            PROMPT_ORDER = LIST_YT_PROMPT(topX, user_input)
        elif script_type == SCRIPT_TYPE[1] and platform == SOCIAL_MEDIA[1]:
            PROMPT_ORDER = LIST_SC_PROMPT(topX, user_input) 
        
        topXitems = []
        print(topX, script_type, platform, PROMPT_ORDER)
            
        if script_type != None and platform != None and is_generate_script:
            st.session_state.messages.append(HumanMessage(content='topic:' + user_input))
            st.session_state.past.append(user_input)
            resulting_response = []
            for i, prompt in enumerate(PROMPT_ORDER):
                with st.spinner("Please, wait. I am in the process of creating script for you..."):
                    if topX:
                        if topXitems == []:
                            final_prompt = 'SESSION INFO: topic - Top ' + str(topX)+ ' ' + user_input + ' ' + prompt
                        else:
                            final_prompt = 'SESSION INFO: topic - Top ' + ', items are: ' + str(topX)+ str(topXitems) + ' ' + user_input + ' ' + prompt 
                    else:
                        final_prompt = 'SESSION INFO: topic - ' + user_input + ' ' + prompt
                    response = generate_response(final_prompt) 
                    if i == 1 and topX:
                        topXitems = response #.split('[')[1].split(']')[0].split(',')
                        resulting_response.append('RESPONSE #' + str(i+1) + ': ' + response)
                    else:
                        resulting_response.append('RESPONSE #' + str(i+1) + ': ' + response)
            resulting_response = ' '.join(resulting_response)
            st.session_state.generated.append(resulting_response)
                
        elif not is_generate_script and not is_edit_mode:
            st.error("Click the \"Generate script\" button to generate script.")
         
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

if __name__ == '__main__':
    main()