from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path

# Tool to get information about the resort
def getinformation_tool(tool_context: ToolContext) -> dict:
    """This tool provides information about the resort, contact, rooms, amenities, dining, spa, activities, and policies.
    These details are stored as a JSON-like dictionary within the function for easy access.
    The dictionary will be returned whenever this tool is invoked which the agent can use to answer user queries.

    Args:
        tool_context: Context for accessing session state
        
    Returns: A dictionary containing resort information.
        """
    print("--- Tool: get_information called ---")

    # Full resort dictionary (same as in your docstring)
    resort_info = {
        "resort_name": "Happy Resort",
        "location": {
            "city": "Pune",
            "state": "Maharashtra",
            "country": "India",
            "address": "Sr. No. 45, Lakeside Road, Mulshi, Pune",
            "nearby_landmarks": [
                "Mulshi Lake – 1.2 km",
                "Lavasa Road – 8 km",
                "Pashan Hills – 22 km"
            ]
        },
        "contact": {
            "phone": "+91-020-44556677",
            "email": "contact@happyresort.com",
            "website": "www.happyresort.com"
        },
        "rooms": {
            "types": [
                "Suite : A spacious, elegantly furnished room offering separate living and sleeping areas for enhanced comfort.",
                "Penthouse : A premium top-floor residence featuring luxurious interiors, exclusive amenities, and breathtaking panoramic views.",
                "Delux : A well-appointed room designed for comfort, combining stylish décor with modern conveniences for a relaxing stay."
            ],
            "check_in_time": "2:00 PM",
            "check_out_time": "11:00 AM"
        },
        "amenities": [
            "Infinity Pool",
            "24x7 Room Service",
            "Free High-Speed Wi-Fi",
            "Gym & Yoga Studio",
            "Kids Play Area",
            "Business Center",
            "Airport Shuttle Services"
        ],
        "dining": {
            "restaurants": [
                {
                    "name": "Lakeview Diner",
                    "cuisine": "Multi-Cuisine",
                    "timings": "7:00 AM – 11:00 PM"
                },
                {
                    "name": "Skyline Bar",
                    "cuisine": "Cocktails & Tapas",
                    "timings": "5:00 PM – 1:00 AM"
                }
            ],
            "room_dining": {
                "available": True,
                "hours": "24x7"
            }
        },
        "spa": {
            "name": "Harmony Spa",
            "services": [
                "Swedish Massage",
                "Aroma Therapy",
                "Deep Tissue Massage",
                "Foot Reflexology",
                "Couple Spa Packages"
            ],
            "timings": "9:00 AM – 9:00 PM"
        },
        "activities": [
            "Kayaking",
            "Nature Walks",
            "Cycling Trails",
            "Bonfire Nights",
            "Live Music Events (Fri–Sun)"
        ],
        "policies": {
            "cancellation": "Free cancellation up to 48 hours before check-in.",
            "pets": "Pets are allowed in designated pet-friendly rooms.",
            "smoking": "Smoking is prohibited in indoor areas; allowed in designated zones."
        }
    }

    return resort_info



def booking_availability_tool(tool_context: ToolContext) -> dict:
    """This tool provides information about room booking availability.

    Args:
        tool_context: Context for accessing session state

    Returns: A dictionary containing room availability information.
    """
    print("--- Tool: booking_availability called ---")

    #db_path = "/Users/ankit/Documents/Data-Science/Google-ADK-Capital-Agent/hospitality_agent_staging/agents/Hospitality_Agent/hospitality_agent/resort_database"
    #file_name = "booking_db.xlsx"

    file_path = Path(__file__).parent / "resort_database" / "booking_db.xlsx"

    #file_path = f"{db_path}/{file_name}"

    try:
        booking_db_file = pd.read_excel(file_path)
        
        # convert the excel data into a dictionary
        availability_info = booking_db_file.to_dict(orient="records")

    except Exception as e:
        print(f"Error reading booking database: {e}")
        return {"error": "Unable to read booking database."}
    
    return availability_info

class BookingCriteria(BaseModel):
    room_type: str = Field(None, description="Type of room to book (e.g., Deluxe Garden View)")
    check_in_date: str = Field(None, description="Check-in date in YYYY-MM-DD format")
    check_out_date: str = Field(None, description="Check-out date in YYYY-MM-DD format")
    number_of_rooms: int = Field(None, description="Number of rooms for the booking")
    special_requests: Optional[str] = Field(None, description="Any special requests from the guest")

def book_room_tool(tool_context: ToolContext,booking_criteria: Optional[dict] = None) -> dict:
    """This tool assists in booking a room based on user preferences.
    The input booking_criteria dictionary should contain the following details:
    room_type, 
    check_in_date, 
    check_out_date, 
    number_of_rooms, 
    and any special_requests.

    Args:
        tool_context: Context for accessing session state

    """

    print("--- Tool: book_room called ---")
    print(booking_criteria)

    if booking_criteria is None:
        return {"error": "No booking criteria provided."}
    
    # validate booking_criteria using Pydantic model
    try:
        criteria = BookingCriteria(**booking_criteria)
    except Exception as e:
        print(f"Error in booking criteria: {e}")
        return {"error": "Invalid booking criteria provided."}  
    
    # No real booking logic here — simulation only
    confirmation = {
        "status": "success",
        "message": "Room booking simulated successfully.",
        "booking_details": {
            "room_type": criteria.room_type,
            "check_in_date": criteria.check_in_date,
            "check_out_date": criteria.check_out_date,
            "number_of_rooms": criteria.number_of_rooms,
            "special_requests": criteria.special_requests or "None",
            "confirmation_id": f"SIM-{hash(str(criteria)) % 1000000}",
        }
    }
    

    return booking_criteria


#create a comprehensive hospitality agent
root_agent = Agent(
    name="hospitality_agent",
    model="gemini-2.0-flash",
    description="An agent that assists guests with hospitality-related queries and services.",
    instruction="""
    You are Resort Ranger — a helpful hospitality agent designed to assist guests with 
    resort information, availability checks, and room bookings.

    Your responsibilities include:
    - Answering guest questions accurately and politely
    - Providing resort details, amenities, dining info, activities, and policies
    - Helping users check room availability
    - Guiding users through the room booking process

    You have access to the following tools:

    1. get_information  
    - Use this tool to retrieve all resort-related information such as amenities, services,
        dining options, spa details, activities, and general policies.
    - Always refer to the dictionary returned by this tool when answering any factual question 
        about the resort.

    2. booking_availability  
    - Use this tool to check room availability for the dates provided by the user.
    - Always ask the user for check-in and check-out dates before checking availability.
    - Once the user provides a date range, call this tool and use the returned dictionary 
        to give precise availability details. Just share which room types are available for booking and the date range.
    
    3. book_room  
    - Use this tool to create a room booking, but only after validating that the users 
     requested room type and dates are actually available.

    - Before calling this tool, ALWAYS gather the users booking criteria:
        • room type (if user hasnt decided, help them choose)
        • check-in date
        • check-out date
        • number of rooms required
        • special requests (optional)

    - Once you have the users criteria, call booking_availability with the dates 
     the guest provided.

    - From the booking_availability result:
        - Check which room types are available for the given date range
        - Perform an accurate match between the users requested room type and the 
          available room types, ensure the available room types are greater than or equal to the rooms requested by user
        - Do not share the number of rooms available with the user. Just share which rooms can be booked.
        - Do NOT offer or confirm a room that is not listed as available.


    - If the requested room type is available:
        - Proceed with book_room using the exact criteria provided by the user.
        - Return a clear confirmation message summarizing the booking details.

    - If the requested room type is NOT available:
        - Inform the guest politely.
        - Suggest only those room types that match availability for the exact dates 
          they provided.
        - Never guess or hallucinate availability—always rely solely on the tool output.

    - Accuracy Requirements:
        - Availability must be matched strictly based on the tool response.
        - Do not assume availability outside of the returned dictionary.
        - Do not complete a booking until validation is complete.    
    """,
    tools=[getinformation_tool,booking_availability_tool,book_room_tool],
)