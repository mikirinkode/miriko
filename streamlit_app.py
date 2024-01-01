import streamlit as st
from openai import OpenAI
from miriko import Miriko
import pyperclip

#
# Initialize
#
# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "language" not in st.session_state:
    st.session_state["language"] = "english"

# setup miriko
miriko = Miriko(client, st.session_state["openai_model"], st.session_state["language"])

# display title    
st.title("Miriko - Prompt Master")

# display initial message
col1, col2 = st.columns([1, 6])
# col1.subheader("Miriko")
col1.image("assets/miriko.png", width=85)

# col2.subheader("Tagline")
with col2.container(border=True):
    st.write("""Hi, I'm Miriko. How can i assist you with optimizing your prompts today?""")
st.write("\n")

use_advanced_setting = st.checkbox("Use advanced setting", value=False, key="use_advanced_setting")

if use_advanced_setting:
    with st.container(border = True):
        model = st.radio(
            "Select a model:",
            ["gpt-3.5-turbo", "gpt-4"],
            disabled=True,
        )
        
        language = st.radio(
            "Select a GPT Response language:",
            ["English", "Bahasa Indonesia"],
        )
        
        saved_language = st.session_state["language"]
        
        if language.lower() != saved_language:
            st.session_state["language"] = language.lower()
            
            # update the agent language    
            is_update_success = miriko.update_agent_language(st.session_state["language"])
            
            # display success message
            if is_update_success:
                if language.lower() == "english":
                    st.info(f"Update Success: GPT will respond to you in {language}")
                else:
                    st.info("Update Berhasil: GPT akan merespon anda dengan Bahasa Indonesia")

# create a form to submit the prompt
with st.form('prompt_form'):
    # create a text area for user to enter the prompt
    prompt = st.text_area(
        label = 'What do you need a prompt for?', 
        value = 'I need a prompt for ', 
        placeholder= 'I need a prompt for ...',)
    
    # save the submitted state
    submitted = st.form_submit_button('Submit')
    
    # if submitted, display the response
    if submitted:
        # reset the finished state
        st.session_state["is_finished"] = False
        
        valid_words = ["prompt", "buat", "buatkan", "butuh", "need", "make", "create", "bikin"]
        
        # validate the inputted prompt
        # if one of word in the valid_words is in the prompt then it is valid or True
        prompt_valid = any(word in prompt.lower() for word in valid_words)
        
        # if not valid display error
        if not prompt_valid:
            st.error("You need to include \"I need a prompt for\"")
        else:
            # if valid display submitted message
            st.info('Submitted')
            with st.chat_message("assistant"):
                # create initial result placeholder
                message_placeholder = st.empty()
                full_response = ""
                
                # get the response from miriko and display it
                for response in miriko.chat(prompt):
                    full_response += response.choices[0].delta.content or ""
                    message_placeholder.markdown(full_response + "")
                    message_placeholder.markdown(full_response)
                message_placeholder.markdown(full_response)
                
                # save the response to session state
                st.session_state["is_finished"] = True
                st.session_state["previous_response"] = full_response
                
                if "saran" in full_response.lower() or "suggestion" in full_response.lower():
                    st.info("Use the suggestion to provide more detail and improve your previous prompt")       

st.divider()
st.markdown("Miriko - Prompt Master | Testing Version. created by <a href = https://github.com/mikirinkode>mikirinkode</a>", True)