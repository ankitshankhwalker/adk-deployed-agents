# streamlit_app.py
import streamlit as st
import asyncio
from main import get_runner_and_session, run_query_async

st.set_page_config(page_title="Resort Ranger Agent", page_icon="🏨", layout="centered")

st.title(" 🏨 Resort Ranger")

# -------------------------------------------------------
# 1. Initialize backend ONCE
# -------------------------------------------------------
@st.cache_resource
def init_backend():
    return get_runner_and_session()

runner, session_service, APP_NAME, USER_ID, SESSION_ID = init_backend()

# -------------------------------------------------------
# 2. Initialize chat history
# -------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []   # {"role": "user"/"assistant", "text": "..."}


# -------------------------------------------------------
# 3. Insert welcome message ON FIRST LOAD ONLY
# -------------------------------------------------------
if "welcome_shown" not in st.session_state:
    welcome_text = (
        "👋 **Welcome to Resort Ranger!**\n\n"
        "I'm your Hospitality Assistant. I can help you with:\n"
        "• Resort details (location, contact info)\n"
        "• Room types & check-in / check-out timings\n"
        "• Amenities like pool, spa, gym, kids area\n"
        "• Dining options & restaurant timings\n"
        "• Activities & nearby attractions\n"
        "• Policies, cancellations, or anything else!\n\n"
        "Ask me anything about your stay 😊"
    )

    st.session_state.messages.append({"role": "assistant", "text": welcome_text})
    st.session_state.welcome_shown = True

# -------------------------------------------------------
# 3. Render chat (Streamlit native chat UI)
# -------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])


# -------------------------------------------------------
# 4. Chat input (Streamlit built-in)
# -------------------------------------------------------
user_input = st.chat_input("Ask something about the resort...")

if user_input:
    # Show user's message
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate agent reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = asyncio.run(
                run_query_async(runner, USER_ID, SESSION_ID, user_input)
            )
            st.markdown(reply)

    # Save reply
    st.session_state.messages.append({"role": "assistant", "text": reply})
