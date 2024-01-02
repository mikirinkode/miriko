import streamlit as st
from openai import OpenAI
from miriko import Miriko
import main_page as main_page

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
col1.image("assets/mirikowaving.png", width=85)

# col2.subheader("Tagline")
with col2.container(border=True):
    st.write("""Hi, I'm Miriko. How can i assist you with optimizing your prompts today?""")
st.write("\n")

tab1, tab2, tab3 = st.tabs(["Playground", "How To", "About"])

with tab1:
    # display playground
    main_page.display_playground(st, miriko)

with tab2:
    # display how to
    main_page.display_how_to(st)
    
with tab3:
    # display about
    main_page.display_about(st)


st.divider()
st.markdown("Miriko - Prompt Master | Testing Version. This code is open source and available <a href = https://github.com/mikirinkode/miriko-prompt-master>[here on Github]</a>", unsafe_allow_html=True)