import sys
import time
from typing import Any, Dict

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather MCP", json_response=True)

_last_request_time = 0.0


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


async def fetch_json(url: str, params: Dict[str, Any]) -> Any:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(
                url,
                params=params,
                headers={"User-Agent": "WeatherMCP-StudentProject"},
            )
            r.raise_for_status()
            return r.json()
    except httpx.TimeoutException:
        raise ValueError("API timeout. Please try again.")
    except httpx.HTTPStatusError as e:
        raise ValueError(f"HTTP error from upstream API: {e.response.status_code}")
    except Exception:
        raise ValueError("Unexpected error contacting upstream API.")


@mcp.tool()
async def geocode_place(query: str) -> Dict[str, Any]:
    """
    Convert place name into latitude and longitude.
    """

    global _last_request_time

    if len(query.strip()) < 2:
        raise ValueError("Query too short.")

    now = time.time()
    if now - _last_request_time < 1:
        wait = 1 - (now - _last_request_time)
        log(f"Rate limit: sleeping {wait:.2f}s")
        time.sleep(wait)

    url = "https://nominatim.openstreetmap.org/search"
    data = await fetch_json(
        url,
        {"q": query, "format": "json", "limit": 1},
    )

    _last_request_time = time.time()

    if not data:
        return {"warning": "No results found."}

    item = data[0]

    return {
        "display_name": item["display_name"],
        "lat": float(item["lat"]),
        "lon": float(item["lon"]),
    }


@mcp.tool()
async def get_forecast(lat: float, lon: float, days: int = 3) -> Dict[str, Any]:
    """
    Get weather forecast from Open-Meteo.
    """

    if not (-90 <= lat <= 90):
        raise ValueError("Invalid latitude.")
    if not (-180 <= lon <= 180):
        raise ValueError("Invalid longitude.")
    if not (1 <= days <= 7):
        raise ValueError("Days must be between 1 and 7.")

    url = "https://api.open-meteo.com/v1/forecast"

    data = await fetch_json(
        url,
        {
            "latitude": lat,
            "longitude": lon,
            "forecast_days": days,
            "timezone": "auto",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        },
    )

    daily = data.get("daily")

    if not daily:
        return {"warning": "No forecast data returned."}

    results = []
    for i in range(len(daily["time"])):
        results.append(
            {
                "date": daily["time"][i],
                "max_temp": daily["temperature_2m_max"][i],
                "min_temp": daily["temperature_2m_min"][i],
                "precipitation": daily["precipitation_sum"][i],
            }
        )

    return {"lat": lat, "lon": lon, "forecast": results}


if __name__ == "__main__":
    mcp.run(transport="stdio")