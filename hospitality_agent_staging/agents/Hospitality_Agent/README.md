# Hospitality Agent — Resort Ranger

Resort Ranger is an intelligent hospitality assistant built using **Google ADK** and served through a lightweight **Streamlit chat UI**.  
It helps users explore resort information such as room types, amenities, dining options, activities, and policies.

The project is packaged in **Docker** and deployable to **Google Cloud Run** for serverless hosting.

## Framework Used

- **Google ADK (Agent Developer Kit)**  
  Powers the conversational agent, tool execution, and session management.

- **Streamlit**  
  Provides a simple, interactive chat-based UI for user interaction.

- **SQLite (via aiosqlite)**  
  Stores persistent ADK session data during local development.

- **Docker**  
  Packages the application into a portable container for local testing and cloud deployment.

- **Google Cloud Run**  
  Runs the application in a fully managed, serverless environment with automatic scaling.


## Agent Capabilities

The Hospitality Agent (“Resort Ranger”) can assist users with:

- **Resort Information**  
  Name, address, location, contact details, and nearby landmarks.

- **Rooms & Stay**  
  Available room types, check-in and check-out timings.

- **Amenities**  
  Pool, spa, gym, Wi-Fi, kids’ area, shuttle services, and business center.

- **Dining**  
  Restaurant options, cuisines, and operating hours.

- **Spa & Wellness**  
  Available therapies and spa timings.

- **Activities & Experiences**  
  Outdoor activities (kayaking, cycling), nature walks, live events.

- **Policies**  
  Cancellation rules, smoking policies, and pet-friendly options.

The agent retrieves all information through a dedicated ADK tool that returns a structured resort information dictionary.

## 📁 Folder Structure

Below is the simplified structure of the Hospitality Agent project:
Hospitality_Agent/
│
├── agents/
│ └── Hospitality_Agent/
│ ├──   hospitality_agent/
│ │     ├── agent.py # ADK agent + tools
│ │     └── init.py
│ ├── app.py # Streamlit UI
│ ├── main.py # ADK runner + session setup
│ ├── utils.py # Helper functions
│ └── .env # Environment variables (local)
│
├── Dockerfile # Container build config
├── requirements.txt # Project dependencies
└── README.md # Project documentation

## How to Test the Agent Locally

Follow the steps below to run the Hospitality Agent on your local machine.

### 1. Install Dependencies
Make sure you have Python 3.11+ installed, then install project requirements:


pip install -r requirements.txt

- ### Set-Up the Environment variables 

- ### Update the database configuration to point DB_URL to local

- '''bash
- ### python main.py

## How to Test the Streamlit Locally
- ''' base
- ### streamlit run agents/Hospitality_Agent/app.py

## How to Build a Docker Image and Run Locally
## Build a Docker Image & Run Locally

### You can package the Hospitality Agent into a Docker container for consistent execution across environments.

### Build the Docker Image

### Run the following command from the project root:

### ```bash
### docker build -t hospitality-agent .
### docker run -p 8080:8080 hospitality-agent

### Deploy on cloud run
gcloud run deploy hospitality-agent \
--source=hospitality_agent_staging \
--region="$GOOGLE_CLOUD_LOCATION" \
--project="$GOOGLE_CLOUD_PROJECT" \
--allow-unauthenticated




 