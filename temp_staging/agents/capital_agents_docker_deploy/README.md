# This project contains an example of deploying a Google ADK agent on Cloud Run instance uisng Gcloud docker
# This is focussed on the steps to create docker image, test locally & then deploy on cloud run

# Here is a step by step guide for this usecase

######
#### Step 1 - Enter the project directory and create and activate the python virtual environment
#### python3 -m venv .venv
#### source .venv/bin/activate

#### Step 2 - Install the required packges listed in requirements.txt
#### pip install -r requirements.txt

#### Step3 - Assume the following folder structure, download the agent.py & __init__.py file
#### Root folder - Google-ADK-Capital-Agent
#### Sub-Folder - capital_agents_docker_deply
####   --> agent.py
####   --> __init__.py
####   -->.env

#### Step4 -  update the following files in the .env file
#### export GOOGLE_CLOUD_PROJECT=just-metric-476211-h8
#### export GOOGLE_CLOUD_LOCATION=us-central1
#### export GOOGLE_API_KEY= ###

#### Step5 - Test if you agent is working
#### When in root folder run the following:
#### adk run capital_agents_docker_deploy

#### Step6 - Expose the environment variables to make them available for deployment
#### source capital_agents_docker_deploy/.env

#### Step 7 -  create a new structure as follows to containerize the application
#### Create a temp_staging folder which should look as follows:
"""
temp_staging\
|--Dockerfile
|--agents/
|. |-- __init__.py
|. |-- capital_agents_docker_deploy
|.     |-- __init__.py
|.     |-- agent.py
|.--requirements.txt
"""

#### Step 7 - Configure Gcloud SDK and setup the environment variables
#### <To Be Updated>


#### Step 8 - Update the contents of the dockerfile to point to the current agent. Test the docker image locally as follows
#### Build and run the image by running the following command
#### docker build -t capital-agent .
#### docker run -p 8080:8080 -e PORT=8080 capital-agent

#### Test by opening tis on browser
#### http://localhost:8080

#### Step 9: Deploy on cloud run 
#### run the following command from outside of temp_staging folder
gcloud run deploy capital-agent-service \
--source=temp_staging \
--region="$GOOGLE_CLOUD_LOCATION" \
--project="$GOOGLE_CLOUD_PROJECT" \
--allow-unauthenticated

