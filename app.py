from hugchat import hugchat
from hugchat.login import Login
import streamlit as st

# Initialize session state variables if they don't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cookies" not in st.session_state:
    st.session_state.cookies = None

st.title("HugChat LLM Chatbot")
st.markdown("Made by Vo1d_s")

sidebar = st.sidebar
sidebar.markdown("## HuggingFace account") 
email = sidebar.text_input("Email", placeholder="Your email", disabled=st.session_state.logged_in)
password = sidebar.text_input("Password (secure)", placeholder="Your password", type="password", disabled=st.session_state.logged_in)  # Hides the password input

if email and password:
    if not st.session_state.logged_in:
        try:
            credentials = Login(email=email, passwd=password)
            st.session_state.cookies = credentials.login()
            st.session_state.logged_in = True
            st.session_state.chatbot = hugchat.ChatBot(st.session_state.cookies)
        except Exception as e:
            sidebar.error(f"Error: {e}")

def stream(prompt):
    for event in st.session_state.chatbot.chat(prompt):
        if event:
            yield event["token"]

def main():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("What is up?", disabled=not st.session_state.logged_in):
        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = st.write_stream(stream(prompt))

        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()