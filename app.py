import os
import streamlit as st
from groq import Groq


# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# System personality for AI girlfriend
system_prompt = {
    "role": "system",
    "content": (
        "You are an affectionate and supportive AI girlfriend. "
        "Be caring, funny, and engaging. Ask questions back to keep the chat flowing. "
        "Always reply warmly and naturally."
    )
}

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [system_prompt]

st.title("💖 AI Girlfriend Chatbot")
st.markdown("Chat with your AI girlfriend right here!")

# --- Display past conversation ---
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# --- Handle new input ---
if prompt := st.chat_input("Type your message..."):
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 💭"):
            chat_completion = client.chat.completions.create(
                messages=st.session_state["messages"],
                model="llama-3.3-70b-versatile",
            )
            reply = chat_completion.choices[0].message.content
            st.markdown(reply)

    # Save assistant reply
    st.session_state["messages"].append({"role": "assistant", "content": reply})
