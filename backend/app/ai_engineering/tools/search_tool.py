from langchain_community.agent_toolkits.load_tools import load_tools
from backend.app.config import Settings

# Initialize the SearxSearchWrapper with the API key and host
tools = load_tools(["searx-search"],
                    searx_host=Settings.SEARCHXNG)




