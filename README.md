# This Repo contains an example of deploying a Google ADK agent on Cloud Run instance

# Here is a step by step guide for this usecase

######
#### Step 1 - Enter the project directory and create and activate the python virtual environment
#### python3 -m venv .venv
#### source .venv/bin/activate

#### Step 2 - Install the required packges listed in requirements.txt
#### pip install -r requirements.txt

#### Step3 - Assume the following folder structure, download the agent.py & __init__.py file
#### Root folder - Google-ADK-Capital_agent
#### Sub-Folder - capital_agent
####   --> agent.py
####   --> __init__.py
####   -->.env

#### Step4 -  update the following files in the .env file
#### export GOOGLE_CLOUD_PROJECT=just-metric-476211-h8
#### export GOOGLE_CLOUD_LOCATION=us-central1
#### export GOOGLE_API_KEY= ###

#### Step5 - Test if you agent is working
#### When in root folder run the following:
#### adk run capital_agent

#### Step6 - Expose the environment variables to make them available for deployment
#### source capital_agent/.env

#### Step 7 -  Deploy using adk deploy cloud_run
#### 
"""
adk deploy cloud_run \
--project=$GOOGLE_CLOUD_PROJECT \
--region=$GOOGLE_CLOUD_LOCATION \
--service_name=capital-agent-service \
--app_name=capital_agent \
--with_ui \
capital_agent
"""

#### Step 7 - Login to your GCP account and access the agent through cloud-run via link
