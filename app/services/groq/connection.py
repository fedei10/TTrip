"""
Groq API connection and testing service.
Handles connection setup and health checks for Groq AI services.
"""


import os
from langchain_groq import ChatGroq
from app.config import settings
import requests

def test_chat_groq_connection():
    """
    Test the Groq API connection by making a simple request.
    Returns True if the connection is successful, False otherwise.
    """
    try:
        llm = ChatGroq(api_key=settings.GROQ_API_KEY,
                       model="meta-llama/llama-guard-4-12b",
                          temperature=0.0
                          ,max_tokens=40
                       )
        message = "Hello, Groq!"
        response = llm.chat([{"role": "user", "content": message}])
        print(f"Groq response: {response}")
        return True
        

    except Exception as e:
        print(f"Groq connection error: {e}")
        return False
def test_groq_connection():
    """
    Test the Groq API connection.
""" 
    api_key = settings.GROQ_API_KEY
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

