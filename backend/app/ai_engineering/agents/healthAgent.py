from langchain_groq import ChatGroq
from langchain_groq.prompts import ChatPromptTemplate
from settings import settings
import getpass
import os
import yaml


llm = ChatGroq(
    model="moonshotai/kimi-k2-instruct-0905",
    temperature=0.5,
    max_tokens=700,
    reasoning_format="parsed",
    max_retries=2,api_key=os.environ["GROQ_API_KEY"]
)


#yaml open file


with open ("backend/app/ai_engineering/prompt_engineering/templates/health_agent.yaml","r") as file:
    agent_config = yaml.safe_load(file)

ChatPromptTemplate.from_template(agent_config["prompt_template"])