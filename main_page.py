def display_playground(st, miriko):
    use_advanced_setting = st.checkbox("Use optional setting", value=False, key="use_advanced_setting")

    # show advanced setting
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
                    st.text("You can copy the result here:")
                    st.code(full_response, language="text")       

def display_how_to(st):
    st.markdown("#### 1. Write down what you need a prompt for")
    st.write("For example:")
    st.code("I need a prompt for writing a poem", language="text")
    st.markdown("#### 2. Wait and look at the result")
    st.write("After you click the 'Submit' button, you will see the result in the chat box.")
    st.write("here is an example of the result:")
    
    with st.expander("See the full Result"):    
        with st.chat_message("assistant"):    
            st.code("""
    1. Role: Creative Poet

    2. Instructions:
    - Start by brainstorming some themes or emotions you want to explore in your poem.
    - Choose a specific topic or image that resonates with you.
    - Begin with a captivating opening line or phrase that grabs the reader's attention.
    - Use vivid and descriptive language to paint a picture or evoke emotions.
    - Experiment with different poetic techniques such as similes, metaphors, alliteration, or rhyme to enhance the poem's impact.
    - Create a rhythmic flow by varying the line lengths and using poetic devices like repetition or enjambment.
    - Reflect on the chosen topic or image throughout the poem, exploring different angles and perspectives.
    - Craft a powerful conclusion that leaves the reader with a lasting impression.

    3. Context: Imagine you are attending a poetry reading event and need a captivating and engaging poem to share with the audience. Your goal is to create a piece that resonates with the listeners, elicits emotions, and showcases your poetic abilities.

    4. Constraints:
    - Keep the poem length within 10-20 lines.
    - Maintain a consistent tone and style throughout the poem.
    - Avoid using offensive or explicit language.
    - Consider the time limit for reading the poem aloud, ensuring it fits within the allocated time.

    5. Examples:
    As the golden sun dips below the horizon, A symphony of colors paints the sky, Dancing hues of orange, pink, and blue, Whispering the beauty of a world renewed.

    Silent trees sway in the evening breeze, Their outstretched branches, like arms embracing the night, The fragrance of fresh rain lingers in the air, Inviting thoughts of life's gentle, soothing rhythms.

    I walk barefoot on the dew-kissed grass, Feeling the earth's heartbeat beneath my feet, Inspired by nature's raw and untamed grace, My pen dances, eager to translate this silent symphony.

    Serenading birds sing their joyful melodies, Notes of freedom and resilience fill the air, In this harmonious moment, I find solace, Nature's poetry, my soul's endless affair.

    6. Suggestions:
    - Please add more context about the intended audience or any specific emotions you want the poem to evoke.
    - Consider adding specific language or imagery preferences for the poem to align with your creative vision.
    - It would be helpful to mention if there are any specific poetic devices or styles you prefer or wish to avoid in the poem.
                    """, language = "text")
        
    st.markdown("#### 3. Use the suggestion to improve your previous prompt")
    st.write("If you are not satisfied with the result, you can use the suggestion to improve your previous prompt.")
    st.write("For example, if you want to add more context, you can add more context like this:")
    st.markdown("##### Previous Suggestion:")
    st.code("""
            6. Suggestions:
- Please add more context about the intended audience or any specific emotions you want the poem to evoke.
- Consider adding specific language or imagery preferences for the poem to align with your creative vision.
- It would be helpful to mention if there are any specific poetic devices or styles you prefer or wish to avoid in the poem.
            """, language="text")
    st.markdown("##### New Prompt")
    st.write("Look at to the previous suggestion, you can specify about what is the poem about and who is the audience like this:")
    st.code("""I need a prompt for writing a poem about love and mother. \nThis poem will be used on Mother's Day Event""", language="text")
    
    with st.expander("See the full Result"):    
        with st.chat_message("assistant"):    
            st.code("""
1. Role: Creative Experience Poet

2. Instructions:
   - Start by expressing the deep and unconditional love a mother possesses.
   - Describe the selfless sacrifices that a mother makes for her child.
   - Highlight the bond between a mother and her child, emphasizing the nurturing and protective nature of a mother's love.
   - Explore the moments of joy, happiness, and laughter shared between a mother and child.
   - Acknowledge the strength and resilience of a mother, portraying her as a source of strength and comfort.
   - Convey gratitude towards mothers and celebrate their role in our lives.
   
3. Context: Mother's Day Event where the poem will be read out loud to celebrate and honor mothers.

4. Constraints:
   - Poem should be appropriate for a general audience and suitable for a public event.
   - Use language that is respectful and inclusive.
   - Poem should not exceed X number of lines or minutes to fit within the event time frame.
   
5. Examples:
   - A mother's love is like the warm sun,  
     Lighting up our lives when things go down,
     With every smile, she makes our hearts dance,
     Guiding us with love, leaving no chance.

   - In her gentle arms, solace we find,
     A love so pure, so patient, so kind,
     Through joyous laughter and tears we shed,
     A mother's love, forever widespread.
     
6. Suggestions:
   - Please add more context regarding the specific theme or tone you would like the poem to have.
   - Could you provide an approximate number of lines or minutes the poem should be?
   - It would be helpful to know the age range or demographic of the audience attending the event.
                    """, language = "text")
    
    st.markdown("#### 4. Repeat step 1 to 3 until you are satisfied with the result")
    st.write("Repeat step 1 to 3 until you get the perfect prompt or you are satisfied with the result.")
    st.markdown("#### 5. Finally, Copy the prompt and use it with ChatGPT")
    st.markdown("- Finally your prompt is ready and you can use the prompt with ChatGPT or other by copying the prompt and paste it into the prompt box in ChatGPT. \n- Make Sure you copy it from the Role to the Example section")
    
def display_about(st):
    st.subheader("What Prompt Master is?")
    
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("assets/miriko.png", width=100)
    with col2:
        st.write("Welcome to “The Prompt Master”! A Customized AI Agent that helps you talk to AI models, like ChatGPT, more effectively.")
        st.write("You know how sometimes you ask GPT about something, and you are not satisfied with the results? This is often due to the lack of detail in the question / instructions.")
    st.write("That's where “The Prompt Master” comes in. This agent has provided instruction to help optimize your prompts using RICCE (Role, Instruction, Context, Constraint and Example) format. Whether you're looking to generate a poem, write a story, or get answers to your questions, “The Prompt Master” can help you craft the perfect prompt.")
    st.write("Prompt Master is powered by OpenAI API and Streamlit.")
    st.write()
    st.subheader("Credits")
    st.markdown("Thanks to Moritz Kremb, as this website is basically an improved prompt that he shared and adopted into web version. You can check his post at this link <a href=https://www.thepromptwarrior.com/p/turn-prompt-super-prompt>Turn Prompt to Super Prompt</a>", unsafe_allow_html=True)