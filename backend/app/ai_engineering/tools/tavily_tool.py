from langchain_tavily import TavilySearch
import getpass
import os
from app.config import Settings
def tavily_tool():
  try:
    os.environ.get("TAVILY_API_KEY")
    os.environ["TAVILY_API_KEY"] = Settings.TAVILY_API_KEY 
  except KeyError as e:
    raise KeyError(f"⚠️  Warning: TAVILY_API_KEY not found in environment variables. Please set it before using the Tavily tool. Error details: {e}")
  tool = TavilySearch(
     max_results=6,
    topic="general,travel,health,finance,rules",
    #include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
   )
  return tool