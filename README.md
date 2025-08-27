# Tuffy Hunt

Tuffy Hunt is an interactive campus scavenger hunt game built for the ACM chapter at California State University, Fullerton.  
Teams race to find QR-coded elephants placed around campus while guided by riddles from the Guardian chatbot.  

## Overview

Each team is assigned a path of stations across campus. The Guardian chatbot provides a riddle for the next station.  
Teams must solve the riddle, locate the physical elephant, and scan its QR code. The backend validates progress, awards points, and updates the leaderboard.  

The first team to reach the final elephant wins, but all teams can complete the hunt at their own pace.  

## Features

- Guardian chatbot powered by xAI Grok
  - Provides short riddles and limited hints
  - Refuses to reveal exact station names
- Supabase backend for all game state
  - Teams, stations, paths, and scoring stored in database tables
  - Server-side validation of scans
- QR-coded elephants
  - Each QR encodes the team slug, station ID, and scan flag
  - Only the expected station advances the team
- Real-time leaderboard
  - Displays ranks, scores, and standings during play
- Streamlit frontend
  - Branding and instructions page
  - Guardian chat interface with styled bubbles
  - Live leaderboard view

## Architecture
![Architecture](https://sdmntpreastus.oaiusercontent.com/files/00000000-d85c-61f9-9b29-a743e5b3617c/raw?se=2025-08-27T01%3A05%3A33Z&sp=r&sv=2024-08-04&sr=b&scid=58b86b10-1ab5-5a41-a6ee-7b7305c304c9&skoid=31bc9c1a-c7e0-460a-8671-bf4a3c419305&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-08-26T21%3A56%3A58Z&ske=2025-08-27T21%3A56%3A58Z&sks=b&skv=2024-08-04&sig=WGm9xV9Ywxjg25wZnNgdWbK1ot0f2xNG2Dzu2uDaoOE%3D)
- Frontend  
  Built in Streamlit. Handles chat UI, team input, QR scan handling, and leaderboard rendering.  

- Backend  
  Supabase (Postgres + API) stores:
  - `teams`: slugs, names, winner timestamps
  - `stations`: station IDs and metadata
  - `paths`: ordered station list per team and current progress
  - `score_events`: point logs for each correct scan  

- Guardian LLM  
  Grok is called via the OpenAI-compatible API. Each response is seeded by the station’s riddle and scrubbed for restricted aliases. Responses are short and consistent, with one stronger hint available per station.  

- QR Generation  
  QR codes are generated with Python. Each encodes a deep link in the form:  
```https://<app-url>/?team=<slug>&station=<station_id>&scan=1```

## Technology Stack

- Python 3.10+
- Streamlit for the frontend
- Supabase for database and RPC functions
- OpenAI client for xAI Grok integration
- QRCode and Pillow for QR generation

## Installation

Clone the repository and install requirements:

```bash
git clone https://github.com/<your-org>/tuffy-hunt.git
cd tuffy-hunt
pip install -r requirements.txt
```

## Configuration

Secrets are stored in ```bash .streamlit/secrets.toml```:
```toml
SUPABASE_URL = "..."
SUPABASE_ANON_KEY = "..."

GROK_API_KEY = "..."
GROK_API_URL = "https://api.x.ai/v1"
GROK_MODEL   = "grok-4-0709"

MAX_TOKENS_PER_REPLY = "160"
TEMPERATURE = "0.25"
DAILY_REQUEST_LIMIT = "200"
DAILY_COMPLETION_TOKEN_LIMIT = "50000"
```

Provide a .streamlit/secrets.toml.example in the repository for setup instructions.

## Running Locally
```bash streamlit run ui.py```
Open the app http://localhost:8501

Use ```bash qrs.py``` to generate QR packs per team:

```bash
python qrs.py --base-url "http://localhost:8501" --team red-1234
```

