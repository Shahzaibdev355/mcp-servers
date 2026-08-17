# chat example using MCPAgent with builtin
# conversation memory

# mcp agent with its builtin conversation
# history capabilities for better contextual InteractiveConsole


import asyncio
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

from mcp_use import MCPAgent, MCPClient
import os


async def run_memory_chat():
    """chat using mcpagent builtin conversation memory"""

    # load_dotenv()
    # os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # config file path
    config_file = "browser_mcp.json"

    print("initializing chat....")

    # creating mcp client and agent with memory enabled
    client = MCPClient.from_config_file(config_file)

    llm = ChatOllama(model="llama3.1:8b", temperature=0)

    # system prompt to prevent the model from sending null/None
    # values for optional airbnb_search parameters, which crashes
    # the Airbnb MCP server's scraper
    system_msg = """When calling airbnb_search, only include parameters you have real values for: location, checkin, 
    checkout, adults. NEVER pass null/None for optional parameters like children, infants, pets, cursor, propertyType 
    — omit them entirely instead."""

    # creating agent
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=5,
        memory_enabled=True,  # enabled builtin conversation memory
        system_prompt=system_msg,
    )

    print("\n Mcp Chat Agent")
    print("type exit or quit to end the conversation")
    print("type clear to clear conversation history")
    print("=============================\n")

    try:
        while True:

            user_input = input("\n Enter text")

            if user_input.lower() in ["exit", "quit"]:
                print("ending conversation....")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("conversation history cleared")
                continue

            print("\n Assitant: ", end="", flush=True)

            try:

                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\n Error: {e}")

    finally:

        # clean up
        if client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_memory_chat())
