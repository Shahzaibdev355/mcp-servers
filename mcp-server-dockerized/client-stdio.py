import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    # server parameters
    server_params = StdioServerParameters(
        command="python",  # the command to run the server
        args=["server.py"],  # args to the comd
    )

    # connect to the server using sse
    async with stdio_client(server_params) as (read_stream, write_stream):
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
