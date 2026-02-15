import json

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.tools import StructuredTool

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


def load_search_tools():
    """Load and validate search tools."""
    try:
        tools = load_tools(
            ["searx-search"],
            searx_host=Settings.SEARCHXNG ,
            engines=["google", "bing", "duckduckgo"],
        )

        if not tools:
            print("⚠️  Warning: No tools loaded. Agent will run without search capability.")
            return []

        wrapped_tools = [_wrap_tool_output(tool) for tool in tools]

        print(f"✅ Loaded {len(wrapped_tools)} SearxNG search tool(s)")
        return wrapped_tools

    except Exception as e:
        print(f"⚠️  Warning: Error loading SearxNG tools: {e}")
        print("Agent will continue without search tools.")
        return []


tools = load_search_tools()




