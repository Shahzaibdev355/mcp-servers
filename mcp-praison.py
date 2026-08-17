from praisonaiagents import Agent, MCP

search_agent = Agent(
    instructions="""You help book appartments on Airbnb""",
    llm="ollama/llama3.1:8b",
    tools = MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
)

search_agent.start("must use airbnb_search tool and get price hotel in paris for 2 nights from Aug 20 to Aug 22, 2026")