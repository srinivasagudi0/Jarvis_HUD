import os

import requests
from openai import OpenAI


def get_weather(city="Sugar Land"):
    sources = (
        ("https://wttr.in/{city}?format=j1", lambda data: from_wttr(data)),
        (
            "https://api.open-meteo.com/v1/forecast?latitude=29.6197&longitude=-95.6349&current=temperature_2m,weather_code",
            lambda data: from_open_meteo(data),
        ),
    )
    for url, parser in sources:
        try:
            response = requests.get(url.format(city=city), timeout=4)
            response.raise_for_status()
            return parser(response.json())
        except (requests.RequestException, KeyError, IndexError, ValueError, TypeError):
            continue
    return "Unavailable"


def from_wttr(data):
    current = data["current_condition"][0]
    return f'{current["temp_C"]}°C, {current["weatherDesc"][0]["value"]}'


def from_open_meteo(data):
    current = data["current"]
    labels = {0: "Clear", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast", 61: "Rain"}
    return f'{round(current["temperature_2m"])}°C, {labels.get(current["weather_code"], "Stable skies")}'


def respond_to_command(command, weather, system_name, history=None):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OpenAI is not configured. Set `OPENAI_API_KEY` to enable live AI chat."
    prompt = (
        f"System name: {system_name}\n"
        f"Weather: {weather}\n"
        "You are JARVIS, a refined AI desktop assistant. Sound human, calm, and concise. "
        "Be directly useful and avoid fake system claims.\n\n"
        f"{conversation_text(history or [])}\n"
        f"User: {command}"
    )
    try:
        response = OpenAI(api_key=api_key).responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-mini"),
            input=prompt,
            temperature=0.7,
            max_output_tokens=220,
        )
        text = getattr(response, "output_text", "").strip()
        return text or read_response_output(response)
    except Exception as exc:
        return f"OpenAI request failed: {exc}"


def conversation_text(history):
    lines = []
    for role, message in history[-6:]:
        speaker = "User" if role == "user" else "Jarvis"
        lines.append(f"{speaker}: {message}")
    return "\n".join(lines) or "Conversation: none yet."


def read_response_output(response):
    for item in getattr(response, "output", []):
        for content in getattr(item, "content", []):
            text = getattr(content, "text", "").strip()
            if text:
                return text
    return "The model returned no text."
