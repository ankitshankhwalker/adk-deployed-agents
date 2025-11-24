import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from hospitality_agent.agent import root_agent
from google.genai import types
from utils import display_state


load_dotenv()

# ===== PART 1: Initialize Persistent Session Service =====
# Using SQLite database for persistent storage

#db_url = "sqlite:///./my_agent_data.db"

#when testing locally, use:
#db_url = "sqlite+aiosqlite:///./my_agent_data.db"

#when running in docker container, use:
db_url = "sqlite+aiosqlite:////app/agents/Hospitality_Agent/my_agent_data.db"


session_service = DatabaseSessionService(db_url=db_url)

# ===== PART 2: Define Initial State =====
initial_state = {
    "resort_name": "Heavenly Escape Resort",
    "location": "Pune",
}

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


async def main_async():
    # Setup constants
    APP_NAME = "Hospitality Agent"
    USER_ID = "Ankit Kamat"

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

    # ===== PART 5: Interactive Conversation Loop =====
    print("Welcome to the Hospitality Agent! Type 'exit' to quit.")
    while True:
        #print("-------------------Existing Sessions-------------------")
        #display_state(
        #    session_service,
        #    APP_NAME,
        #    USER_ID,
        #    SESSION_ID,
        #    label="Conversation Start Session State"
        #)
        #print("-------------------------------------------------------")
        user_input = ask_input("You")
        if user_input.lower() in {"exit", "quit"}:
            print("\n👋 Ending chat. Goodbye!")
            break

        content = types.Content(role="user", parts=[types.Part(text=user_input)])
        bot_reply = ""

        async for event in runner.run_async(
            user_id=USER_ID, session_id=SESSION_ID, new_message=content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                bot_reply = event.content.parts[0].text
                print(f"🤖 Bot: {event.content.parts[0].text}\n")
        
        #print("-------------------Existing Sessions-------------------")
        #display_state(
        #    session_service,
        #    APP_NAME,
        #    USER_ID,
        #    SESSION_ID,
        #    label="Conversation End Session State"
        #)
        #print("-------------------------------------------------------")

if __name__ == "__main__":
    asyncio.run(main_async())