import streamlit as st
from openai import OpenAI
from datetime import date

client = OpenAI(
    api_key=st.secrets["GROK_API_KEY"],
    base_url=st.secrets["GROK_API_URL"],
)
MODEL = st.secrets.get("GROK_MODEL", "grok-4")

MAX_TOKENS_PER_REPLY = int(st.secrets.get("MAX_TOKENS_PER_REPLY", 180))
TEMPERATURE = float(st.secrets.get("TEMPERATURE", 0.3))

# simple daily budget
DEFAULT_DAILY_REQUESTS = int(st.secrets.get("DAILY_REQUEST_LIMIT", 300))
DEFAULT_DAILY_COMPLETION_TOKENS = int(st.secrets.get("DAILY_COMPLETION_TOKEN_LIMIT", 60000))

def _get_budget():
    today = date.today().isoformat()
    b = st.session_state.get("_guardian_budget")
    if not b or b.get("day") != today:
        b = {
            "day": today,
            "requests_left": DEFAULT_DAILY_REQUESTS,
            "completion_tokens_left": DEFAULT_DAILY_COMPLETION_TOKENS,
        }
        st.session_state["_guardian_budget"] = b
    return b

def _charge_after(resp):
    """Charge the budget based on API-reported usage if available, otherwise estimate."""
    try:
        usage = getattr(resp, "usage", None)
        comp = usage.completion_tokens if usage else MAX_TOKENS_PER_REPLY
    except Exception:
        comp = MAX_TOKENS_PER_REPLY
    b = _get_budget()
    b["requests_left"] = max(0, b["requests_left"] - 1)
    b["completion_tokens_left"] = max(0, b["completion_tokens_left"] - int(comp))

def _check_budget_or_raise():
    b = _get_budget()
    if b["requests_left"] <= 0 or b["completion_tokens_left"] <= 0:
        raise RuntimeError("Daily guardian budget reached. Try again tomorrow or raise the limits.")

# LLM prompt
SYSTEM_PROMPT = """You are the Tuffy Hunt guardian.
Rules:
- You know the current station name and a seed riddle.
- Always start reasoning from the given seed riddle.
- Never reveal the exact station name, sign text, room number, or coordinates outright.
- If give_hint=false: be encouraging; paraphrase or gently nudge. Keep it short.
- If give_hint=true: provide ONE stronger hint that narrows the location, but still no exact name or signage text.
- Answers must be 1–3 short sentences.
"""

def ask_grok(prompt: str) -> str:
    try:
        _check_budget_or_raise()
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS_PER_REPLY,
        )
        _charge_after(resp)
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        return f"[Error: {e}]"

def guardian_reply(station_name: str, user_msg: str, seed_riddle: str, give_hint: bool) -> str:
    intent = "hint" if give_hint else "chat"
    payload = (
        f"Station: {station_name}\n"
        f"Seed riddle: {seed_riddle}\n"
        f"Intent: {intent}\n"
        f"User: {user_msg.strip()}"
    )
    try:
        _check_budget_or_raise()
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": payload},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS_PER_REPLY,
        )
        _charge_after(resp)
        text = (resp.choices[0].message.content or "").strip()
        return text if text else "Hmm… I didn’t quite catch that. Try asking again."
    except Exception:
        return "The guardian had a hiccup. Please try again."
