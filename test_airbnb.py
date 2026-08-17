import asyncio
from mcp_use import MCPClient


async def main():
    client = MCPClient.from_config_file("browser_mcp.json")

    try:
        await client.create_all_sessions()

        session = client.get_session("airbnb")

        result = await session.call_tool(
            name="airbnb_search",
            arguments={
                "location": "Paris",
                "checkin": "2026-09-01",
                "checkout": "2026-09-03",
                "adults": 2,
                "propertyType": "hotel_room",
            },
        )

        print("RESULT:")
        print(result)

    finally:
        await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(main())