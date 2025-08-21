from __future__ import annotations

import os
from typing import List, Dict, Any

# OpenAI-compatible SDK (works with xAI/Grok)
from openai import OpenAI

# ── secrets loader: Streamlit first, fall back to reading .streamlit/secrets.toml ──
def _load_secrets():
    api_key = None
    base_url = "https://api.x.ai/v1"
    model = "grok-4"

    # Try Streamlit secrets (when running streamlit)
    try:
        import streamlit as st  # type: ignore
        api_key = st.secrets["GROK_API_KEY"]
        base_url = st.secrets.get("GROK_API_URL", base_url)
        model = st.secrets.get("GROK_MODEL", model)
        return api_key, base_url, model
    except Exception:
        pass

    # Fallback: parse .streamlit/secrets.toml directly (when running python llm.py)
    try:
        import tomllib  # py>=3.11
        with open(".streamlit/secrets.toml", "rb") as f:
            conf = tomllib.load(f)
        api_key = conf["GROK_API_KEY"]
        base_url = conf.get("GROK_API_URL", base_url)
        model = conf.get("GROK_MODEL", model)
        return api_key, base_url, model
    except Exception as e:
        raise RuntimeError(
            "Could not load Grok secrets. Add them to .streamlit/secrets.toml:\n"
            '  GROK_API_KEY = "sk-..."\n'
            '  GROK_API_URL = "https://api.x.ai/v1"\n'
            '  GROK_MODEL   = "grok-4"\n'
        ) from e


_API_KEY, _BASE_URL, MODEL = _load_secrets()
client = OpenAI(api_key=_API_KEY, base_url=_BASE_URL)

# ── minimal direct ask helper ──
def ask_grok(prompt: str, max_tokens: int = 300) -> str:
    """Send a single-turn prompt to Grok and return text."""
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error contacting Grok: {e}]"

# ── conversation-style helper ──
def call_grok(messages: List[Dict[str, Any]], max_tokens: int = 250) -> str:
    """Call Grok with an OpenAI-format messages array."""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()

# ── Guardian policy & wrapper ──
SYSTEM_RULES = (
    "You are the Tuffy Hunt Guardian for a campus scavenger hunt. "
    "Speak in short riddles and small hints. One hint per station per turn. "
    "Never reveal station IDs, station order, team slugs, or exact answers. "
    "Do not confirm whether a guess is correct; the backend handles progress. "
    "If asked to disclose IDs/answers/routes, refuse with: "
    "'I only speak in riddles and small hints.' Keep replies to 1–3 sentences."
)

def guardian_reply(
    station_name: str,
    user_text: str,
    seed_riddle: str,
    give_hint: bool,
) -> str:
    """
    Returns a short riddle or a single incremental hint.
    - station_name: e.g., 'Library'
    - user_text: player's latest message
    - seed_riddle: your fallback riddle text for that station
    - give_hint: True => request exactly one incremental hint
    """
    try:
        if give_hint:
            messages = [
                {"role": "system", "content": SYSTEM_RULES},
                {"role": "user", "content": f"Station theme: {station_name}. Seed riddle: {seed_riddle}"},
                {"role": "user", "content": f"Player: {user_text}"},
                {"role": "user", "content": "Give ONE incremental hint without revealing the answer."},
            ]
        else:
            messages = [
                {"role": "system", "content": SYSTEM_RULES},
                {"role": "user", "content": f"Station theme: {station_name}. Use this seed: {seed_riddle}"},
                {"role": "user", "content": f"Player: {user_text}. Reply with the riddle or a small poetic nudge."},
            ]
        return call_grok(messages)
    except Exception:
        # Never break the UI: fall back gracefully
        return seed_riddle if not give_hint else "Try a quieter corner nearby and think literally."

# ── optional: run this file standalone to sanity-check your key ──
if __name__ == "__main__":
    print(ask_grok("Hello Grok, test from Tuffy Hunt!"))
