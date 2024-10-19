import os
import requests

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_explanation(error_message, context):
    
    """Generate a human-readable explanation using Groq API."""
    
    if not GROQ_API_KEY:
        return "Unable to generate explanation due to missing API key. Please set the GROQ_API_KEY environment variable."

   #TO-DO THIS WILL NOT WORO 

    return None
    
