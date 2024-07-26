import streamlit as st
import cohere
import os
import dotenv

dotenv.load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

client = cohere.Client(api_key=COHERE_API_KEY)

st.set_page_config(page_title="LLM Chatbot")
st.title("LLM Chatbot")
st.markdown("Made by Vo1d_s")

def update_chat():
    st.session_state.messages = []

sidebar = st.sidebar
#preamble_input = sidebar.text_input("Behaviour", placeholder="You are an assistant.", on_change=update_chat)
temperature_slider = sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
max_tokens_slider = sidebar.slider("Max Tokens", min_value=10, max_value=1000, value=500, step=5)
frequency_penalty_slider = sidebar.slider("Frequency penalty", min_value=0.0, max_value=1.0, value=0.75, step=0.05)

def chat(prompt):
    response = ""
    for event in client.chat_stream(
        message=prompt,
        #preamble=preamble_input or "You are an assistant.",
        preamble="You are a helpfull assistant, you adapt to whatever the user says, so you can share likes and dislikes.",
        chat_history=st.session_state.messages,
        temperature=temperature_slider,
        max_tokens=max_tokens_slider,
        frequency_penalty=frequency_penalty_slider
    ):
        if event.event_type == "text-generation":
            response = response + event.text
            yield event.text
            
        if event.event_type == "stream-end":
            return response
def main():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message("assistant" if message["role"] == "CHATBOT" else "user"):
            st.write(message["message"])

    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.write(prompt)
        
        st.session_state.messages.append({"role": "USER", "message": prompt})

        with st.chat_message("assistant"):
            response = st.write_stream(chat(prompt))

        st.session_state.messages.append({"role": "CHATBOT", "message": response})

if __name__ == "__main__":
    main()