import requests
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from langchain.chat_models import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=GEMINI_API_KEY)

def search_trending_topics(topic):
    url = f"https://serper.dev/search"
    headers = {"X-API-KEY": "your_serper_key_here"}  # Replace this if you get access
    params = {"q": topic}
    try:
        response = requests.get(url, headers=headers, params=params)
        return str(response.json())
    except:
        return "Unable to fetch trending topics."

def generate_script(topic):
    prompt = f"""
    Write a detailed and engaging YouTube script for the topic: {topic}.
    Include: Hook, Introduction, 3 Key Points, and a Conclusion with CTA.
    """
    return llm.invoke(prompt).content
