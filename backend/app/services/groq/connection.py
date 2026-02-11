"""
Groq API connection and testing service.
Handles connection setup and health checks for Groq AI services.
"""


from http import client
import os
from langchain_groq import ChatGroq
from app.config import settings
import requests
from groq import Groq

def test_groq_connection():

    client=Groq(
        api_key=settings.GROQ_API_KEY,
    )

    val = client.chat.completions.create(
        messages=[
            {
                "role": "user",
            "content": "Explain the importance of fast language models",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    if (val):
        return "Groq connection successful"
    else:
        raise Exception("Groq connection failed")
    