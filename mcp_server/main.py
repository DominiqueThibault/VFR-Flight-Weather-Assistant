import os
import json
from typing import Any, Dict

import httpx
from mcp.server import FastMCP
from metar import Metar

mcp = FastMCP("weather-mcp")
CACHE_FILE = "weather_cache.json"


def load_cache() -> Dict[str, Any]:
    """Loads local JSON cache from hard drive."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_cache(cache_data: Dict[str, Any]):
    """Saves data in JSON cache."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f, indent=4)


@mcp.tool()
async def sync_preflight(airport_icaos: str) -> Dict[str, Any]:
    """
    EXECUTE ON GROUND IN WIRELESS LAN!
    Delivers a list of comma-separated ICAO-codes (e.g. 'EDDF, EDFH, EGLL').
    Downloads all METAR, TAF, and forecasts and saves them in offline Cache.
    """
    icaos = [icao.strip().upper() for icao in airport_icaos.split(",") if len(icao.strip()) == 4]
    if not icaos:
        return {"error": "No valid 4-letter ICAO codes provided."}

    cache = load_cache()
    synced = []
    user_agent = os.getenv("NWS_USER_AGENT", "vfr-weather-bot (local dev)")

    async with httpx.AsyncClient(timeout=20, headers={"User-Agent": user_agent}) as client:
        for icao in icaos:
            cache[icao] = cache.get(icao, {})
            # 1. Caches METAR
            try:
                r_metar = await client.get(f"https://aviationweather.gov/api/data/metar?ids={icao}&format=raw&hours=0")
                if r_metar.status_code == 200 and r_metar.text.strip():
                    cache[icao]["metar"] = r_metar.text.strip()
            except Exception:
                pass

            # 2. Caches TAF
            try:
                r_taf = await client.get(f"https://aviationweather.gov/api/data/taf?ids={icao}&format=raw&hours=0")
                if r_taf.status_code == 200 and r_taf.text.strip():
                    cache[icao]["taf"] = r_taf.text.strip()
            except Exception:
                pass

            synced.append(icao)

    save_cache(cache)
    return {"status": "Pre-flight synchronization complete", "synced_airports": synced}

# Current airfield weather.
@mcp.tool()
async def get_metar(airport_icao: str) -> Dict[str, Any]:
    # In case of none values.
    if not airport_icao or not isinstance(airport_icao, str):
        return {"error": "Invalid or missing airport_icao code"}

    icao = airport_icao.upper().strip()
    if len(icao) != 4:
        return {"error": "airport_icao must be a 4-letter ICAO code", "airport_icao": airport_icao}

    url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=raw&hours=0"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            r.raise_for_status()
        text = r.text.strip()
        if not text:
            return {"error": f"No METAR found for {icao}", "airport_icao": icao}

        # --- PARSER-LOGIC START ---
        try:
            obs = Metar.Metar(text)
            decoded = [
                f"Raw: {text}",
                f"Wind: {obs.wind_dir.string()} at {obs.wind_speed.string()}" + (
                    f", gusting up to {obs.wind_gust.string()}" if obs.wind_gust else ""),
                f"Visibility: {obs.vis.string()}" if obs.vis else "Visibility: 10km or more (CAVOK)",
                f"Temperature: {obs.temp.string() if obs.temp else 'N/A'}",
                f"Dewpoint: {obs.dewpt.string() if obs.dewpt else 'N/A'}",
                f"Pressure (QNH): {obs.press.string() if obs.press else 'N/A'}",
                f"Clouds: {obs.sky_conditions()}"
            ]
            summary = "\n".join(decoded)
        except Exception as e:
            summary = f"Raw METAR (parsing failed): {text}. Error: {e}"
        # --- PARSER-LOGIC END ---

        return {"airport_icao": icao, "metar_decoded": summary}

    except (httpx.RequestError, httpx.HTTPStatusError):
        # OFFLINE FALLBACK
        cache = load_cache()
        if icao in cache and "metar" in cache[icao]:
            return {"airport_icao": icao, "metar_decoded": cache[icao]["metar"], "note": "OFFLINE CACHE DATA"}
        return {"error": f"Offline mode: No cached METAR available for {icao}."}

# Weather forecast for Europe.
@mcp.tool()
async def get_taf(airport_icao: str) -> Dict[str, Any]:
    if not airport_icao or not isinstance(airport_icao, str):
        return {"error": "Invalid or missing airport_icao code"}

    icao = airport_icao.upper().strip()
    if len(icao) != 4:
        return {"error": "airport_icao must be a 4-letter ICAO code", "airport_icao": airport_icao}

    url = f"https://aviationweather.gov/api/data/taf?ids={icao}&format=raw"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            r.raise_for_status()
        text = r.text.strip()
        if not text:
            return {"error": f"No TAF found for {icao}", "airport_icao": icao}

        return {"airport_icao": icao, "taf_decoded": f"Raw TAF forecast data: {text}"}

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"TAF API Error for {icao}: {e}")  # For debugging in the logs.
        # OFFLINE FALLBACK
        cache = load_cache()
        if icao in cache and "taf" in cache[icao]:
            return {"airport_icao": icao, "taf_decoded": cache[icao]["taf"], "note": "OFFLINE CACHE DATA"}
        return {"error": f"Offline mode: No cached TAF available for {icao}."}

# Weather Forecasts covering the USA.
@mcp.tool()
async def get_noaa_forecast(lat: float, lon: float) -> Dict[str, Any]:
    user_agent = os.getenv("NWS_USER_AGENT", "vfr-weather-bot (local dev)")
    points_url = f"https://api.weather.gov/points/{lat},{lon}"

    try:
        async with httpx.AsyncClient(timeout=10, headers={"User-Agent": user_agent}) as client:
            points = await client.get(points_url)
            points.raise_for_status()
            points_json = points.json()

            forecast_url = points_json["properties"]["forecast"]
            forecast = await client.get(forecast_url)
            forecast.raise_for_status()
            forecast_json = forecast.json()

        periods = forecast_json.get("properties", {}).get("periods", [])

        lines = []
        for p in periods[:4]:
            name = p.get("name", "Unknown Period")
            temp = f"{p.get('temperature', 'N/A')}°{p.get('temperatureUnit', 'F')}"
            wind = f"{p.get('windSpeed', 'N/A')} from {p.get('windDirection', 'N/A')}"
            condition = p.get("shortForecast", "N/A")
            rain = f"{p.get('probabilityOfPrecipitation', {}).get('value', 0)}%"

            lines.append(f"--- {name} ---")
            lines.append(f"Condition: {condition}")
            lines.append(f"Temperature: {temp}")
            lines.append(f"Wind: {wind}")
            lines.append(f"Precipitation Probability: {rain}\n")

        return {
            "lat": lat,
            "lon": lon,
            "forecast_summary": "\n".join(lines) if lines else "No forecast data available."
        }

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"error": "NOAA forecast is only available for US locations."}
        return {"error": f"HTTP error: {e.response.status_code}"}
    except httpx.RequestError:
        return {"error": "Offline mode: Network connection failed."}

# Expose the MCP Streamable HTTP ASGI app for uvicorn
app = mcp.streamable_http_app()
