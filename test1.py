import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient


async def test_duckduckgo():

    print("Starting DuckDuckGo MCP...")

    client = MultiServerMCPClient(
        {
            "duckduckgo-search": {
                "command": "npx",
                "args": ["-y", "duckduckgo-mcp-server"],
                "transport": "stdio",
            }
        }
    )

    # Load MCP tools
    tools = await client.get_tools()

    print(f"\nLoaded tools: {[tool.name for tool in tools]}")

    # Find the DuckDuckGo search tool
    search_tool = next(
        tool for tool in tools
        if tool.name == "duckduckgo_web_search"
    )

    print("\nCalling duckduckgo_web_search directly...")
    print("========================================")

    try:
        result = await search_tool.ainvoke({
            "query": "latest Python 3.14 news",
            "count": 5
        })

        print("\nSUCCESS!")
        print("========================================")
        print(result)

    except Exception as e:
        print("\nMCP TOOL ERROR!")
        print("========================================")
        print(type(e).__name__)
        print(e)


if __name__ == "__main__":
    asyncio.run(test_duckduckgo())