from hugchat import hugchat
from hugchat.login import Login
import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cookies" not in st.session_state:
    st.session_state.cookies = None

llms = [
    'meta-llama/Meta-Llama-3.1-70B-Instruct', 
    'meta-llama/Meta-Llama-3.1-405B-Instruct-FP8', 
    'CohereForAI/c4ai-command-r-plus', 
    'mistralai/Mixtral-8x7B-Instruct-v0.1', 
    'NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO', 
    '01-ai/Yi-1.5-34B-Chat', 
    'mistralai/Mistral-7B-Instruct-v0.3', 
    'microsoft/Phi-3-mini-4k-instruct'
]

st.title("HugChat LLM Chatbot")
st.markdown("Made by Vo1d_s")

sidebar = st.sidebar
sidebar.markdown("## HuggingFace account") 
email = sidebar.text_input("Email", placeholder="Your email", disabled=st.session_state.logged_in)
password = sidebar.text_input("Password (secure)", placeholder="Your password", type="password", disabled=st.session_state.logged_in)
empty = sidebar.empty()
sidebar.warning("Note: You may get an eamil saying that someone logged into your account because this uses HuggingFace, it is safe.")

def change_system_prompt():
    st.session_state.messages = []
    st.session_state.chatbot.delete_conversation()
    st.session_state.chatbot = hugchat.ChatBot(st.session_state.cookies, system_prompt=st.session_state.sys_prompt, default_llm=st.session_state.selected_llm)
    print(st.session_state.selected_llm)

sidebar.markdown("## Model Configuration")
system_prompt = sidebar.text_input("System prompt (don't leave empty)", placeholder="Model behaviour", on_change=change_system_prompt, key="sys_prompt", disabled=not st.session_state.logged_in)
selected_llm = sidebar.selectbox("LLM (model)", placeholder="Default LLM", on_change=change_system_prompt, options=llms, key="selected_llm", disabled=not st.session_state.logged_in)

if email and password:
    if not st.session_state.logged_in:
        try:
            credentials = Login(email=email, passwd=password)
            st.session_state.cookies = credentials.login()
            st.session_state.logged_in = True
            st.session_state.chatbot = hugchat.ChatBot(st.session_state.cookies)
        except Exception as e:
            empty.error(f"Error: {e}")

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
            try:
                response = st.write_stream(stream(prompt))
            except Exception as e:
                response = f"Error: {e}"
                st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()