import yaml
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent
from app.config import Settings
from app.ai_engineering.tools.search_tool import load_search_tools
from app.ai_engineering.tools.amadeus_tool import loadAmadeusToolkit
from app.ai_engineering.tools.tavily_tool import tavily_tool

# -----------------------------
# 1️⃣ Load Prompt Template
# -----------------------------
def load_system_prompt() -> str:
    """Load and validate system prompt from YAML file."""
    try:
        yaml_path = Settings.POLICY_AGENT_PROMPTEMPLATE_PATH
        with open(yaml_path, "r") as f:
            yaml_data = yaml.safe_load(f)

        if not isinstance(yaml_data, list):
            raise ValueError("YAML content must be a list of message tuples")
        
        system_message = ""
        for message in yaml_data:
            if isinstance(message, (list, tuple)) and len(message) == 2:
                role, content = message
                if role == "system":
                    system_message = content
                    break
        
        if not system_message:
            raise ValueError("No system message found in YAML template")
        
        return system_message

    except FileNotFoundError:
        print(f"❌ Error: YAML file not found at {yaml_path}")
        exit(1)
    except Exception as e:
        print(f"❌ Error loading YAML: {e}")
        exit(1)

system_prompt = load_system_prompt()

# -----------------------------
# 2️⃣ Initialize LLM
# -----------------------------
def initialize_llm():
    """Initialize the language model with proper configuration."""
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=700,
            max_retries=2,
            api_key=Settings.GROQ_API_KEY,
            streaming=False
        )
        print("✅ LLM initialized successfully")
        return llm
    except Exception as e:
        print(f"❌ Error initializing LLM: {e}")
        exit(1)

llm = initialize_llm()

# -----------------------------
# 3️⃣ Load Tools with Validation
# -----------------------------
def load_tools_with_checkup(llm):
    """
    Load all tools with proper validation and error handling.
    Returns a flat list of valid tool objects.
    """
    tools = []
    
    # 1. Load search tools (SearxNG)
    try:
        search_tools = load_search_tools()
        if not isinstance(search_tools, (list, tuple)):
            search_tools = [search_tools]
        # Validate each tool
        for tool in search_tools:
            if hasattr(tool, 'name') and callable(getattr(tool, 'invoke', None)):
                tools.append(tool)
                print(f"✅ Loaded search tool: {tool.name}")
            else:
                print(f"⚠️  Skipped invalid search tool: {tool}")
    except Exception as e:
        print(f"⚠️  Search tools failed to load: {e}")
    
    # 2. Load Amadeus toolkit
    try:
        amadeus_tools = loadAmadeusToolkit(llm)
        if not isinstance(amadeus_tools, (list, tuple)):
            amadeus_tools = [amadeus_tools]
        for tool in amadeus_tools:
            if hasattr(tool, 'name'):
                tools.append(tool)
                print(f"✅ Loaded Amadeus tool: {tool.name}")
    except Exception as e:
        print(f"⚠️  Amadeus toolkit failed to load: {e}")
    
    # 3. Load Tavily tool with proper unpacking check
    try:
        tavily_result = tavily_tool()
        
        # Handle different return types: single tool, list, or tuple
        if isinstance(tavily_result, tuple):
            # If it's a tuple, extract the tool (usually first element)
            tavily_tools = list(tavily_result)
            print(f"ℹ️  Tavily returned tuple, unpacked to {len(tavily_tools)} items")
        elif not isinstance(tavily_result, list):
            tavily_tools = [tavily_result]
        else:
            tavily_tools = tavily_result
        
        # Validate and add Tavily tools
        valid_tavily_count = 0
        for tool in tavily_tools:
            # Check if it's a valid tool (has name and is callable/invocable)
            if hasattr(tool, 'name') and callable(getattr(tool, 'invoke', None)):
                tools.append(tool)
                valid_tavily_count += 1
                print(f"✅ Loaded Tavily tool: {tool.name}")
            else:
                print(f"⚠️  Skipped invalid Tavily item: {type(tool)} - {tool}")
        
        if valid_tavily_count == 0:
            raise ValueError("No valid Tavily tools found in result")
            
    except Exception as e:
        print(f"⚠️  Tavily tool failed to load: {e}")
        # Optionally exit if Tavily is critical: exit(1)
    
    # Final validation
    if not tools:
        print("❌ No tools loaded successfully. Agent cannot function.")
        exit(1)
    
    print(f"\n📦 Total tools loaded: {len(tools)}")
    return tools

# Load tools with checkup
tools = load_tools_with_checkup(llm)

# -----------------------------
# 4️⃣ Initialize Agent
# -----------------------------
def initialize_agent():
    """Initialize the agent with proper configuration."""
    try:
        agent = create_agent(
            llm,
            tools,  # Now guaranteed to be a flat list of valid tool objects
            system_prompt=system_prompt
        )
        print("✅ Agent initialized successfully")
        return agent
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        exit(1)

agent = initialize_agent()

# -----------------------------
# 5️⃣ Interactive Chat Loop
# -----------------------------
def run_chat_loop():
    """Run the interactive chat loop with the agent."""
    print("\n🤖 Claims Processor Agent ready! Type 'exit' or 'quit' to leave.\n")
    
    chat_history = []
    max_history = 20

    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye! Have a great day.")
                break

            response = agent.invoke({
                "messages": [
                    *chat_history,
                    HumanMessage(content=user_input)
                ]
            })

            if isinstance(response, dict) and "messages" in response:
                last_message = response["messages"][-1]
                agent_response = last_message.content if hasattr(last_message, 'content') else str(last_message)
            else:
                agent_response = str(response)

            print(f"Agent: {agent_response}\n")

            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=agent_response))

            if len(chat_history) > max_history:
                chat_history = chat_history[-max_history:]

        except KeyboardInterrupt:
            print("\n\n⚠️  Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Agent encountered an error: {e}")
            print("Please try again or rephrase your question.\n")

if __name__ == "__main__":
    run_chat_loop()