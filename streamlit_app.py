import streamlit as st
from openai import OpenAI
from miriko import Miriko

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

    
st.title("Miriko - Prompt Master")
with st.chat_message("assistant"):
    st.write("Hello, I'm Miriko. I will help you to optimize your prompt.")
    
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


with st.form('prompt_form'):
    prompt = st.text_area(
        label = 'What do you need a prompt for?', 
        value = 'I need a prompt for ', 
        placeholder= 'I need a prompt for ...',)
    submitted = st.form_submit_button('Submit')
    
    prompt_valid = True if "I need a prompt for" or "I need a prompt to" in prompt else False
     
    if submitted:
        if not prompt_valid:
            st.error("You need to include \"I need a prompt for\"")
        else:
            st.info('Submitted')
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in miriko.chat(prompt):
                    full_response += response.choices[0].delta.content or ""
                    message_placeholder.markdown(full_response + "")
                    message_placeholder.markdown(full_response)

