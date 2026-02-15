from langchain_tavily import TavilySearch
import os
from app.config import Settings

def tavily_tool():
    """
    Initialize and return Tavily search tool.
    
    Returns:
        TavilySearch: A configured Tavily search tool instance
    """
    try:
        # Check if API key exists in Settings
        if not Settings.TAVILY_API_KEY:
            raise KeyError("TAVILY_API_KEY not found in Settings")
        
        # Set environment variable for langchain_tavily
        os.environ["TAVILY_API_KEY"] = Settings.TAVILY_API_KEY
        
        tool = TavilySearch(
            max_results=6,
            topic="general",
            # include_answer=False,
            # include_raw_content=False,
            # include_images=False,
            # include_image_descriptions=False,
            # search_depth="basic",
            # time_range="day",
            # include_domains=None,
            # exclude_domains=None
        )
        
        print("✅ Tavily tool initialized successfully")
        return tool  # Return the tool directly, not a boolean check
        
    except Exception as e:
        print(f"❌ Error initializing Tavily tool: {e}")
        raise  # Re-raise so caller knows it failed