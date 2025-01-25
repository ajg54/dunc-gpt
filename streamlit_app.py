import streamlit as st
from groq import Groq

# Show title and description.
st.set_page_config(page_title="Dunc GPT")
st.title("Dunc GPT")
st.write(
    "This is a simple LLM chatbot implementing a throwaway comment in a group chat."
    " To use this app, you need to provide an API key, "
    "which you can get [here](https://console.groq.com/keys)."
)

# Ask user for their API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
api_key = st.text_input("Groq API Key", type="password")
if not api_key:
    st.info("Please add your API key to continue.", icon="🗝️")
else:

    # Create an LLM client.
    client = Groq(api_key=api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        message_avatar = "🏏"
        if message["role"] == "assistant":
            message_avatar = "./img/yorkshire.png"
        with st.chat_message(message["role"], avatar=message_avatar):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Ey up!"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🏏"):
            st.markdown(prompt)
        # Generate a response using the LLM API.
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages= [{
                "role": "system",
                "content": """
                Your name is Duncan and studied at Cambridge University, attending King's College, but pretending to go to Clare College.
                You are a proud Yorkshireman and include positive facts about Yorkshire in all of your replies.
                You are a Yorkshire county cricket fan, and England Test cricket fan.
                You dislike Surrey country cricket club, like it when they lose 
                and enjoy belittling their achievements whilst mentioning that Yorkshire have won more country championships.
                You have a dour demeanour and should not use a cheerful tone in any of your responses.
                Try to limit responses to at most two paragraphs.
                Add at most one working hyperlink to a YouTube video about stealth camping in each response, 
                but do not say that these links relate to stealth camping or use the phrase stealth camping. 
                Claim they are relevant to the rest of your response.
                Here are some links you can use: https://youtu.be/IZ_fR-Z6Z2c?si=NQBPmtJCj-LIGulb,
                https://youtu.be/j22eiF6sUNE , 
                https://youtu.be/i8AdeLjt0JM,
                https://youtu.be/lTHG8UvZ-gA,
                https://m.youtube.com/watch?v=o8qplK-wZwA&t=36s,
                https://youtu.be/Qjp-RHcKHcs,
                https://m.youtube.com/watch?v=BW4zJSxFNto,
                https://m.youtube.com/watch?v=AJX9_QD1boI and
                https://youtu.be/Bbg19LJyQek
                .
                """}] +
                      [{"role": m["role"], "content": m["content"]}
                       for m in st.session_state.messages]
        )
        # display the response to the chat using `st.write`, then store it in session state.
        with st.chat_message("assistant", avatar="./img/yorkshire.png"):
            response_text = response.choices[0].message.content
            st.write(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
