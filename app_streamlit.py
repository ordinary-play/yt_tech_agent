import streamlit as st
from agent import run_agent
from fetch_trends import fetch_all_trends

st.set_page_config(page_title="Tech Script Agent", page_icon="🤖", layout="wide")

st.title("🤖 Tech Script Agent")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type a tech topic or 'fetch' for trending..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent response
    with st.chat_message("assistant"):
        with st.spinner("Generating script..."):
            if prompt.lower().startswith("fetch"):
                topics = fetch_all_trends()
                if topics:
                    topic = topics[0]
                    result = run_agent(topic)
                    response = f"**Trending topic chosen:** {topic}\n\n{result['script']}"
                else:
                    response = "No trending topics found."
            else:
                result = run_agent(prompt)
                response = f"**Generated script for:** {prompt}\n\n{result['script']}"

            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
