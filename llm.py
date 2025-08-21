import os
from openai import OpenAI

MODEL = "grok-4"

def load_secrets():
    # Try to use Streamlit secrets if available
    try:
        import streamlit as st
        return (
            st.secrets["GROK_API_KEY"],
            st.secrets.get("GROK_API_URL", "https://api.x.ai/v1"),
            st.secrets.get("GROK_MODEL", MODEL),
        )
    except Exception:
        # Fallback: read from .streamlit/secrets.toml manually
        import tomllib  # built into Python 3.11+
        with open(".streamlit/secrets.toml", "rb") as f:
            conf = tomllib.load(f)
        return (
            conf["GROK_API_KEY"],
            conf.get("GROK_API_URL", "https://api.x.ai/v1"),
            conf.get("GROK_MODEL", MODEL),
        )

api_key, base_url, MODEL = load_secrets()

client = OpenAI(api_key=api_key, base_url=base_url)

def ask_grok(prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[Error: {e}]"

if __name__ == "__main__":
    resp = ask_grok("Hello Grok, just testing connection from Tuffy Hunt!")
    print(resp)
