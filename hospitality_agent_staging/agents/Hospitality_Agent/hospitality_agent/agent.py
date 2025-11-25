from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

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
                "Deluxe Garden View",
                "Premium Lake View",
                "Executive Suite",
                "Family Villa"
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

#create a comprehensive hospitality agent
root_agent = Agent(
    name="hospitality_agent",
    model="gemini-2.0-flash",
    description="An agent that assists guests with hospitality-related queries and services.",
    instruction="""
    You are a hospitality agent designed to assist guests with their needs during their stay.
    

    You have access to the following tools:
    - get_information: Use this tool to provide guests with information about the resort, its amenities, services, and local attractions.
    Always aim to provide accurate and helpful information to enhance the guest experience.
    The information is provided in the dictionary returned from getinformation tool.
    """,
    tools=[getinformation_tool],
)