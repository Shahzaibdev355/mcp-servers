from typing import Any
import httpx #async client
from mcp.server.fastmcp import FastMCP

# initilize fastMCP server
mcp = FastMCP("weather")

#constants
NWS_API+BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a req to the nws api with proper error handling"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert features into a readable string"""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'unknown')}
        Description: {props.get('description', 'no description available')}
        Instructions: {props.get('instruction', 'no specific instruction')}
    """
