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
    
# setup miriko
miriko = Miriko(st.session_state["openai_model"], client)

# display title    
st.title("Miriko - Prompt Master")

# display initial message
with st.chat_message("assistant"):
    st.write("Hello, I'm Miriko. I will help you to optimize your prompt.")

# make user can select the model    
# selected_model = st.selectbox(
#     "Select a model",
#     [
#         "gpt-3.5-turbo",
#         "gpt-4",
#     ],
#     index=0,
#     key="model",
# )
# st.session_state["openai_model"] = selected_model
# miriko.update_model(st.session_state["openai_model"])

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
        
        # validate the inputted prompt
        prompt_valid = True if "I need a prompt for" or "I need a prompt to" in prompt else False
        
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
    else :
        # if not submitted display the previous response
        previous_response = "" if "previous_response" not in st.session_state else st.session_state["previous_response"]
        if previous_response != "":
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown(previous_response)
                
# check is finished state
is_finished = False if "is_finished" not in st.session_state else st.session_state["is_finished"]

# display the copy button if the response is finished                
if is_finished:                
    is_copied = st.button("Copy to clipboard", key="copy")
    if is_copied:
        # copy the response to clipboard
        pyperclip.copy(st.session_state["previous_response"])
        
        # display success message and update the finished state
        st.success("Copied to clipboard")
        st.session_state["is_finished"] = False

st.divider()
st.markdown("Miriko - Prompt Master | Testing Version. created by <a href = https://github.com/mikirinkode>mikirinkode</a>", True)