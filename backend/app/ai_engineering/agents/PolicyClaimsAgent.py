import yaml
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from app.config import Settings
from app.ai_engineering.tools.search_tool import load_search_tools
from app.ai_engineering.tools.amadeus_tool import loadAmadeusToolkit

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
        
        # Extract system message from YAML
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
        # Using ChatGroq directly is acceptable, but could also use init_chat_model
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=700,
            max_retries=2,
            api_key=Settings.GROQ_API_KEY,
            streaming=False  # Explicitly set streaming preference
        )
        print("✅ LLM initialized successfully")
        return llm
    except Exception as e:
        print(f"❌ Error initializing LLM: {e}")
        exit(1)

llm = initialize_llm()

# -----------------------------
# 3️⃣ Load Tools
# ---------------------
tools = [
    *load_search_tools(),
    *loadAmadeusToolkit(llm),
]

# -----------------------------
# 4️⃣ Initialize Agent with Error Handling Middleware
# -----------------------------
@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors gracefully."""
    try:
        return handler(request)
    except Exception as e:
        # Return a user-friendly error message to the model
        error_msg = f"Tool execution failed: {str(e)}. Please try a different approach or rephrase your query."
        return ToolMessage(
            content=error_msg,
            tool_call_id=request.tool_call["id"]
        )

def initialize_agent():
    """Initialize the agent with proper configuration."""
    try:
        # Modern LangChain API: create_agent handles the agent loop internally
        agent = create_agent(
            llm,
            tools,
            system_prompt=system_prompt,
            middleware=[handle_tool_errors]  # Add error handling middleware
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
    max_history = 20  # Keep last 20 messages for context

    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye! Have a great day.")
                break

            # Invoke agent with current input and chat history
            response = agent.invoke({
                "messages": [
                    *chat_history,
                    HumanMessage(content=user_input)
                ]
            })

            # Extract the agent's response
            # The response contains a 'messages' key with all messages including the response
            if isinstance(response, dict) and "messages" in response:
                # Get the last message (the agent's response)
                last_message = response["messages"][-1]
                agent_response = last_message.content if hasattr(last_message, 'content') else str(last_message)
            else:
                agent_response = str(response)

            print(f"Agent: {agent_response}\n")

            # Update chat history
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=agent_response))

            # Trim history to avoid token limits
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