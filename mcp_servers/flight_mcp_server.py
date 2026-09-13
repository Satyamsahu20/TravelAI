# pip install mcp requests

from mcp.server.fastmcp import FastMCP
import requests
import os

from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("Flight Data Server")

AERODATABOX_API_KEY = os.getenv("AERODATABOX_API_KEY")

HEADERS = {
    "X-RapidAPI-Key": AERODATABOX_API_KEY,
    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com",
}


@mcp.tool()
def list_airports(search: str = "", limit: int = 10, offset: int = 0):
    response = requests.get(
        "https://aerodatabox.p.rapidapi.com/airports/search/term",
        headers=HEADERS,
        params={"q": search, "limit": limit},
    )
    data = response.json()
    return data.get("items", [])[:limit]


@mcp.tool()
def list_airlines(search: str = "", limit: int = 10, offset: int = 0):
    response = requests.get(
        "https://aerodatabox.p.rapidapi.com/airlines/search/term",
        headers=HEADERS,
        params={"q": search, "limit": limit},
    )
    data = response.json()
    return data.get("items", [])[:limit]


if __name__ == "__main__":
    mcp.run()