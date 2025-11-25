import asyncio
import os
from dotenv import load_dotenv

# ADK core imports
from google.adk.runners import Runner #exposes HTTP endpoints
from google.adk.sessions import DatabaseSessionService
from google.genai import types

#Import the root agent
from hospitality_agent.agent import root_agent

from utils import display_state


# ================================================================
# 1. Load environment variables (API keys etc.)
# ================================================================
load_dotenv()

# ===== Initialize Persistent Session Service =====
# Using SQLite database for persistent storage

# ================================================================
# 2. Database configuration
#    - LOCAL: sqlite+aiosqlite:///./my_agent_data.db
#    - DOCKER / CLOUD RUN: must use an ABSOLUTE PATH
# ================================================================
DB_URL = "sqlite+aiosqlite:////app/agents/Hospitality_Agent/my_agent_data.db"
#DB_URL = "sqlite+aiosqlite:///./my_agent_data.db"

# ===== Define Initial State =====
initial_state = {
    "resort_name": "Heavenly Escape Resort",
    "location": "Pune",
}

# ================================================================
# 3. This async function sets up:
#       - SessionService
#       - Existing session (or creates a new one)
#       - Runner
#
#   We keep it async because ADK requires "await" calls.
# ================================================================

async def _async_setup(user_id: str):
    APP_NAME = "Hospitality Agent"
    USER_ID = user_id

    session_service = DatabaseSessionService(db_url=DB_URL)

    # ===== PART 3: Session Management - Find or Create =====
    # Check for existing sessions for this user
    existing_sessions = await session_service.list_sessions(
        app_name = APP_NAME,
        user_id = USER_ID,
        )
    
    print("existing_sessions:", existing_sessions)

    if existing_sessions and len(existing_sessions.sessions)>0:
        # Use the most recent session
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        # Create a new session with initial state
        new_session =await session_service.create_session(
            app_name = APP_NAME,
            user_id = USER_ID,
            state = initial_state,
        )
        print(f"Created new session: {new_session.id}")
        SESSION_ID = new_session.id

    # ===== PART 4: Agent Runner Setup =====

    # create a runner with the root_agent
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Return everything needed by Streamlit
    return runner, session_service, APP_NAME, USER_ID, SESSION_ID

# ================================================================
# 4. Sync wrapper for Streamlit
#    Streamlit cannot call async functions → so we wrap it.
#
#    This function runs ONLY ONCE when Streamlit imports main.py.
# ================================================================
def get_runner_and_session(user_id):
    #user_id = ask_input("Enter your User ID", default=None)
    return asyncio.run(_async_setup(user_id))


# ================================================================
# 5. Async function to send user text to the agent
#
#    This wraps:
#       runner.run_async(...)
#
#    It streams events from ADK, finds the final response,
#    and returns it to Streamlit.
# ================================================================
async def run_query_async(runner, user_id, session_id, user_text):
    # Build message content in ADK format
    content = types.Content(
        role="user",
        parts=[types.Part(text=user_text)],
    )

    final_reply = ""

    # ADK returns events (streaming)
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):

        # We only care about the final message
        if event.is_final_response():
            if event.content and event.content.parts:
                final_reply = event.content.parts[0].text

    return final_reply




def ask_input(prompt: str, default: str | None = None) -> str:
    """Small helper to get input with optional default."""
    try:
        val = input(f"{prompt}" + (f" [{default}]" if default else "") + ": ").strip()
    except EOFError:
        # In some environments input() may not be available; fall back to default
        val = ""
    if not val and default is not None:
        return default
    return val


# ================================================================
# (Optional) Standalone testing mode
# This helps you run the agent in console without Streamlit.
# ================================================================
if __name__ == "__main__":
    user_id = ask_input("Enter your User ID", default=None)
    runner, session_service, APP_NAME, USER_ID, SESSION_ID = get_runner_and_session(user_id)

    print(f"\nHospitality Agent Ready!User: {USER_ID}. Type 'exit' to quit.\n")

    while True:
        text = input("You: ").strip()
        if text.lower() == "exit":
            break

        reply = asyncio.run(
            run_query_async(
                runner,
                USER_ID,
                SESSION_ID,
                text
            )
        )

        print("Bot:", reply)