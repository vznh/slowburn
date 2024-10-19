# Importing Required libraries
import time
import requests
 
# Define access token
token = 'Bearer <Your_access_token>'

# Take name of agent from user
name = input('Please give name of your agent? ')
 
# Create payload for agent creation request
agent_creation_data = {
    "name": name
}
 
# Post request to create an agent and store address
response_agent = requests.post("https://agentverse.ai/v1/hosting/agents", json=agent_creation_data, headers={
    "Authorization": token
}).json()
address = response_agent['address']
print(f'Agent Address : {address}')