import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()

"""
run server before running the script
server is configured to use sse transport
server is listening on port 8050

first run
uv run server.py

"""


async def main():

    # connect to the server using sse
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            # initialize the connection
            await session.initialize()

            # list available tools
            tools_result = await session.list_tools()
            print("Available tools: ")
            for tool in tools_result.tools:
                print(f" - {tool.name}: {tool.description}")

            # calling the weather tool
            result = await session.call_tool("get_alerts", arguments={"state": "CA"})
            print(f"the weather alerts are = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())