import json
import os

from langchain_core.tools import StructuredTool
from langchain_groq import ChatGroq

from app.config import Settings


def _wrap_tool_output(tool):
    def _call(**kwargs):
        result = tool.invoke(kwargs)
        if isinstance(result, str):
            return result
        try:
            return json.dumps(result, default=str)
        except TypeError:
            return str(result)

    return StructuredTool.from_function(
        func=_call,
        name=tool.name,
        description=tool.description,
        args_schema=getattr(tool, "args_schema", None),
        return_direct=getattr(tool, "return_direct", False),
    )

def loadAmadeusToolkit(llm: ChatGroq):
    """Load the Amadeus toolkit for travel-related queries."""
    try:
        # Set environment variables first
        os.environ["AMADEUS_CLIENT_ID"] = Settings.AMADEUS_CLIENT_ID
        os.environ["AMADEUS_CLIENT_SECRET"] = Settings.AMADEUS_CLIENT_SECRET
        
        # Import Client from amadeus
        from amadeus import Client
        
        # Import all the modules that need Client to be defined
        import langchain_community.tools.amadeus.base as amadeus_base
        import langchain_community.tools.amadeus.closest_airport as closest_airport_module
        import langchain_community.tools.amadeus.flight_search as flight_search_module
        import langchain_community.agent_toolkits.amadeus.toolkit as toolkit_module
        
        # Inject Client into all modules that have forward references
        amadeus_base.Client = Client
        closest_airport_module.Client = Client
        flight_search_module.Client = Client
        toolkit_module.Client = Client
        
        # Now import the actual classes AFTER injecting Client
        from langchain_community.tools.amadeus.closest_airport import AmadeusClosestAirport
        from langchain_community.tools.amadeus.flight_search import AmadeusFlightSearch
        from langchain_community.agent_toolkits.amadeus.toolkit import AmadeusToolkit
        
        # Rebuild all models in dependency order (base classes first, then derived)
        AmadeusClosestAirport.model_rebuild()
        AmadeusFlightSearch.model_rebuild()
        AmadeusToolkit.model_rebuild()
        
        # Now create the toolkit instance
        amadeus_toolkit = AmadeusToolkit(llm=llm)
        raw_tools = amadeus_toolkit.get_tools()
        tools = [_wrap_tool_output(tool) for tool in raw_tools]
        tool_names = [tool.name for tool in raw_tools]
        print(f"✅ Amadeus toolkit loaded successfully: {tool_names}")
        return tools
        
    except Exception as e:
        print(f"❌ Error loading Amadeus toolkit: {e}")
        return []  # Return empty list to allow agent to continue without Amadeus tools