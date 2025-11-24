# Use a slim python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' myuser

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY --chown=myuser:myuser agents/Hospitality_Agent/ ./agents/Hospitality_Agent/

# Switch to the non-root user
USER myuser

#Set the PATH environment variable for the non-root user's package
ENV PATH="/home/myuser/.local/bin:${PATH}"

# Set the environment variable for google cloud runtime
ENV GOOGLE_GENAI_USE_VERTEXAI=0

# Expose the port that the application will run on
EXPOSE 8080

# The command to run the ADK web server
# This scans the '/aap/agents' directory for discoverable agents
# matching the pattern in the example
# For deploying on cloud run, not setting up port 8080 as default but taking it automatically
CMD ["python", "/app/agents/Hospitality_Agent/main.py"]


