import sys
import os
import django
import requests
from django.conf import settings

# Set the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magnetobackend.settings')  # Replace 'your_project_name' with your actual project folder name
django.setup()

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "1033f222-ac23-46c7-bfc3-bfa1d70eadfa"
FLOW_ID = "63039459-7c6b-44f5-8270-1978012b0f0b"
APPLICATION_TOKEN = settings.API_TOKEN
ENDPOINT = "magneto_tutor"  # The endpoint name of the flow


def run_flow(message: str) -> dict:
    """
    Run a flow with a given message.

    :param message: The message to send to the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)

   
    return response.json()