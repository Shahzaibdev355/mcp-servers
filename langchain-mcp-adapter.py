# chat example using langchain-mcp-adapters
# with manual conversation memory (message list)
# built on LangGraph's create_react_agent


import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient

# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent

import os


async def run_memory_chat():
    """chat using create_react_agent with manual conversation memory"""

    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    print("initializing chat....")

    # server config — same servers as browser_mcp.json, translated
    # to langchain-mcp-adapters' expected format (command/args/transport)
    client = MultiServerMCPClient(
        {
            "playwright": {
                "command": "npx",
                "args": ["@playwright/mcp@latest"],
                "transport": "stdio",
                "env": {"DISPLAY": ":1"},
            },
            # "airbnb": {
            #     "command": "npx",
            #     "args": ["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
            #     "transport": "stdio",
            # },
            # "tavily": {
            #     "command": "npx",
            #     "args": [
            #         "-y",
            #         "mcp-remote",
            #         "https://mcp.tavily.com/mcp/?tavilyApiKey="
            #         + os.getenv("TAVILY_API_KEY"),
            #     ],
            #     "transport": "stdio",
            # },
        }
    )

    # loading tools from all configured mcp servers
    # tools = await client.get_tools()

    # i have some limitation regarding model so will limit to one tool
    all_tools = await client.get_tools()

    # tools = [
    #     tool
    #     for tool in all_tools
    #     if tool.name == "tavily_search"
    # ]

    tools = [
        tool
        for tool in all_tools
        if tool.name == "browser_navigate"
    ]



    print(f"Loaded {len(tools)} tools: {[t.name for t in tools]}")

    llm = ChatGroq(model="openai/gpt-oss-120b")

    # creating the react agent (langgraph's prebuilt agent loop)
    # agent = create_react_agent(llm, tools)
    agent = create_agent(
        llm,
        tools,
        # prompt="""You are an Airbnb search assistant.
        # When calling tools:
        # - Only include parameters that are actually provided or required.
        # - NEVER send null values.
        # - Do not include minPrice, maxPrice, propertyType, or cursor unless needed.
        # - For airbnb_search, use the exact tool schema.
        # """,

        # system_prompt="""
        # You are a web search assistant.

        # When answering questions:
        # - Use the available Tavily search tool when the user asks for current,
        # factual, or web-based information.
        # - Prefer the search tool instead of answering from your own knowledge
        # when web search is requested.
        # - Pass only parameters required by the tool schema.
        # - NEVER send null values.
        # - Return search results clearly and concisely.
        # """,

        system_prompt="""
        You are a browser automation assistant.

        When the user asks you to open or navigate to a website:
        - Use the browser_navigate tool.
        - Do not answer from your own knowledge.
        - Only navigate to the URL requested by the user.
        - Do not use any other tools.
        """
    )

    # manual conversation history — replicates mcp_use's memory_enabled=True
    conversation_history = []

    print("\n Mcp Chat Agent")
    print("type exit or quit to end the conversation")
    print("type clear to clear conversation history")
    print("=============================\n")

    try:
        while True:

            user_input = input("\n Enter text: ")

            if user_input.lower() in ["exit", "quit"]:
                print("ending conversation....")
                break

            if user_input.lower() == "clear":
                conversation_history.clear()
                print("conversation history cleared")
                continue

            print("\n Assistant: searching", end="", flush=True)

            try:
                # append user message to running history
                conversation_history.append({"role": "user", "content": user_input})

                response = await agent.ainvoke({"messages": conversation_history})

                # extract the assistant's final reply
                ai_message = response["messages"][-1]
                print(ai_message.content)

                # append assistant reply so next turn has context
                conversation_history.append(
                    {"role": "assistant", "content": ai_message.content}
                )

            except Exception as e:
                print(f"\n Error: {e}")

    finally:
        # langchain-mcp-adapters' MultiServerMCPClient manages
        # sessions internally per call; no manual close needed here
        pass


if __name__ == "__main__":
    asyncio.run(run_memory_chat())
