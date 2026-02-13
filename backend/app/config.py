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
 AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
 AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")
 #gemini api
 GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")





settings = Settings()