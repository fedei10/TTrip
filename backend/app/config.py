import os 
from dotenv import load_dotenv


load_dotenv()


class Settings:


 #groq
 GROQ_API_KEY = os.getenv("GROQ_API_KEY")
 #searchxng
 SEARCHXNG = os.getenv("SEARCHXNG")
 #asknews api
 ASK_NEWS_API = os.getenv("ASK_NEWS_API")
    #amadeus api
 AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
 AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
 #gemini api
 GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
 #policy agent prompt template path
 POLICY_AGENT_PROMPTEMPLATE_PATH = os.getenv("POLICY_AGENT_PROMPTEMPLATE_PATH")
 #tavily api key
 TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")




settings = Settings()