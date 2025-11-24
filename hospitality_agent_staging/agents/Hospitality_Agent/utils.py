
def display_state(
        session_service, app_name, user_id, session_id, label="Current State"
):
    """Display the current session state in a formatted way."""
    try:
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        #print("----------------- Session State -----------------")
        #print("session:",session)
        #print("------------------------------------------------- ")

        # Format the output with clear sections
        print(f"\n{'-' * 10} {label} {'-' * 10}")

        # Handle the user name
        resort_name = session.state.get("resort_name", "Unknown")
        print(f"Resort:", resort_name)

        # Handle reminders
        location = session.state.get("location", [])
        if location:
            print("Location:",{location})
            
    except Exception as e:
        print(f"Error displaying state: {e}")
