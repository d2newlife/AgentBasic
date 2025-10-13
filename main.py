import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from util.tools import save_tool

load_dotenv()  # take environment variables from .env.

# Ensure GOOGLE_API_KEY is set in your .env file
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

class LLMRresponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    
# Initialize the Google Generative AI LLM for Langchain
# Using "gemini-pro" as a general-purpose model.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.7)
parser = PydanticOutputParser(pydantic_object=LLMRresponse)


prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a helpful research assistant that provides concise and accurate information.
            Answer the user query and user necessary tools.
            Wrap the otuput in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,  # Add the custom tool to the agent
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"query": query})
print(raw_response)

print("...............................\n")


"""
A couple of issues the raw response various, sometimes output will be a key value pair, sometimes a list of key value pairs.
The agent seems to use the tool regardless of whether it is needed or not.
"""
try:
    structured_response = parser.parse(raw_response["output"])
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)