from dotenv import load_dotenv
from praisonaiagents import Agent, MCP
import os

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

print("initializing chat....")

agent = Agent(
    instructions="""You are a multi-tool agent. Select the correct tool based on user input.
When calling airbnb_search, only include parameters you have real values for:
location, checkin, checkout, adults. Never pass null for optional fields.""",
    llm="ollama/llama3.1:8b",
    tools=[
        MCP("npx @playwright/mcp@latest"),
        MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"),
        MCP("npx -y duckduckgo-mcp-server"),
    ],
)

print("\n Mcp Chat Agent")
print("type exit or quit to end the conversation")
print("=============================\n")

while True:
    user_input = input("\n Enter text: ")

    if user_input.lower() in ["exit", "quit"]:
        print("ending conversation....")
        break

    print("\n Assistant: ", end="", flush=True)

    try:
        response = agent.start(user_input)
        print(response)
    except Exception as e:
        print(f"\n Error: {e}")
