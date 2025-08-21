import streamlit as st
import base64
from db import supabase
from typing import Optional, Tuple
import random
from llm import ask_grok, guardian_reply
import time


# 1. Page config
st.set_page_config(page_title="Tuffy Hunt", layout="wide")

# Override Streamlit's primary color to orange and hide 'Press Enter to apply'
st.markdown('''
<style>
:root {
    --primary-color: #FF7900 !important;
    --primary: #FF7900 !important;
    --accent: #FF7900 !important;
    --secondary-background-color: #ffe5b4 !important;
}
.st-bb, .st-cb, .st-eb, .st-em, .stTextInput > div > div > input:focus, .stTextInput > div > div > input:active {
    border-color: #FF7900 !important;
    box-shadow: 0 0 0 2px #FF790022 !important;
}
/* Hide 'Press Enter to apply' helper text for all Streamlit text inputs */
div[data-testid="stTextInput"] span:has(svg) + div span,
div[data-testid="stTextInput"] > div > div > span,
div[data-testid="stTextInput"] label + div span,
div[data-testid="stTextInput"] > div > span {
    display: none !important;
}
</style>
''', unsafe_allow_html=True)

# If realtime event landed return quickly to refresh the leaderboard
if st.session_state.get("_lb_bump") is not None:
    st.session_state["_lb_bump"] = None
    st.rerun()

# Animated gradient background and floating elephants
st.markdown(
  """
  <style>
  body, .stApp {
    /* soft white → light orange gradient */
    background: linear-gradient(135deg, #ffffff 0%, #ffe5b4 100%) fixed !important;
    background-attachment: fixed !important;
    /* switch text to dark for readability */
    color: #333 !important;
  }
  h1, h2, h3, h4, h5, h6, p, li, ul, ol, div, a,
  .markdown-text-container, .stMarkdown, .stText,
  .stButton, .st-bb, .st-cb, .st-eb, .st-em {
    color: #333 !important;
  }
  .elephant-bg {
    pointer-events: none;
    position: fixed;
    left: 0; top: 0; width: 100vw; height: 100vh;
    z-index: 0;
    overflow: hidden;
  }
  .elephant-float {
    position: absolute;
    font-size: 2.2rem;
    opacity: 0.7;
    animation: floatUp 8s linear infinite;
  }
  .elephant-float.e1 { left: 10vw; animation-delay: 0s; }
  .elephant-float.e2 { left: 30vw; animation-delay: 2s; }
  .elephant-float.e3 { left: 60vw; animation-delay: 4s; }
  .elephant-float.e4 { left: 80vw; animation-delay: 6s; }
  @keyframes floatUp {
    0% { bottom: -3rem; opacity: 0.7; }
    80% { opacity: 0.7; }
    100% { bottom: 105vh; opacity: 0; }
  }
  </style>
  <div class="elephant-bg">
    <span class="elephant-float e1">🐘</span>
    <span class="elephant-float e2">🐘</span>
    <span class="elephant-float e3">🐘</span>
    <span class="elephant-float e4">🐘</span>
  </div>
  """,
  unsafe_allow_html=True
)


# 2. Top orange banner with images on the left using Streamlit columns

# Helper to load images as base64
def load_base64(path):
  with open(path, "rb") as f:
    b = f.read()
  return base64.b64encode(b).decode()

csuf_png_b64 = load_base64("csuf_logo.png")
acm_svg_b64  = load_base64("acm_logo.svg")

# Fixed top orange banner with images inside
st.markdown(f"""
<style>
.fixed-orange-banner {{
  background-color: #FF7900;
  height: 60px;
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  gap: 12px;
  padding-left: 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}
.fixed-orange-banner img {{
  height: 44px;
  width: auto;
  padding: 2px;
}}
.banner-spacer {{ height: 60px; }}
</style>
<div class="fixed-orange-banner">
  <img src="data:image/png;base64,{csuf_png_b64}" alt="CSUF Logo" style="background:white; box-shadow: 0 0 0 2.5px white; border-radius: 8px; padding:2px;">
  <img src="data:image/svg+xml;base64,{acm_svg_b64}" alt="ACM Logo" style="background:white; box-shadow: 0 0 0 2.5px white; border-radius: 8px; padding:2px;">
</div>
<div class="banner-spacer"></div>
""", unsafe_allow_html=True)


# 3. Main content (responsive)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <h1 style='text-align:center; font-size:2.7rem; font-weight:800;'>
      Welcome to <span style='color:#FF7900;'>Tuffy</span> <span style='color:#1e90ff;'>Hunt</span> 🐘
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown("<h2 style='text-align:center;'>Instructions</h2>", unsafe_allow_html=True)
st.markdown(
        """
        <div style='background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); border: 1px solid #eee; padding: 28px 32px 24px 32px; margin: 20px auto 32px auto; max-width: 650px;'>
            <ul style='margin: 0; font-size: 1.1rem; line-height: 1.5;'>
                <li>Read the guardian bot’s current riddle for your next station.</li>
                <li>Discuss with your teammates and, if needed, ask the bot for one stronger hint per turn.</li>
                <li>Tap <b>Scan</b> and scan the QR code on an elephant.</li>
                <li>If it’s the correct elephant:
                    <ul>
                        <li>You’ll see “Nice find!”</li>
                        <li>You earn 10 points</li>
                        <li>The next riddle appears automatically</li>
                    </ul>
                </li>
                <li>If it’s the wrong elephant:
                    <ul>
                        <li>You’ll see “Not your elephant.”</li>
                        <li>Try again—only the next station in your sequence counts</li>
                    </ul>
                </li>
                <li>Repeat scanning in order until you reach the shared final elephant.</li>
                <li>The first team to scan the final duck wins, but all teams can finish at their own pace.</li>
                <li>Keep an eye on the live leaderboard to track your progress and standings.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
)


# 4. Simulated bottom orange banner (footer)
st.markdown(
  """
  <div style='width:100vw; position:fixed; left:50%; right:50%; bottom:0; margin-left:-50vw; margin-right:-50vw; background-color:#FFC591; height:48px; z-index:1000;'></div>
  """,
  unsafe_allow_html=True
)

# Simulated bottom orange banner (footer) with centered copyright text
st.markdown(
    """
    <div style='width:100vw; position:fixed; left:50%; right:50%; bottom:0; margin-left:-50vw; margin-right:-50vw; background-color:#FF7900; height:48px; z-index:1000; display:flex; align-items:center; justify-content:center;'>
      <span style='color:white; font-size:1rem; font-weight:500;'>© 2025 Kenny Garcia & Dianella Sy. All rights reserved.</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Game helpers 

def get_team_by_slug(slug: str) -> Optional[dict]:
    res = supabase.table("teams")\
        .select("id, name, slug, game_id, won_at")\
        .eq("slug", slug).single().execute()
    return res.data


def get_path(team_id: str) -> Optional[dict]:
    res = supabase.table("paths").select("station_order, current_index").eq("team_id", team_id).single().execute()
    return res.data

def get_station(station_id: str) -> Optional[dict]:
    res = supabase.table("stations").select("id, name").eq("id", station_id).single().execute()
    return res.data

def get_next_station(team_slug: str) -> Tuple[Optional[dict], Optional[dict], Optional[int]]:
    """
    Returns (team, next_station, idx). If finished, next_station is None.
    """
    team = get_team_by_slug(team_slug)
    if not team:
        return None, None, None
    path = get_path(team["id"])
    if not path:
        return team, None, None
    order, idx = path["station_order"], path["current_index"]
    if idx is None or idx >= len(order):
        return team, None, idx
    stn = get_station(order[idx])
    return team, stn, idx

def advance_if_expected(team_slug: str, scanned_station_id: str) -> Tuple[bool, str]:
    """
    Advance path.current_index by 1 only if scanned_station_id == expected.
    Returns (ok, message).
    """
    team = get_team_by_slug(team_slug)
    if not team:
        return False, "Team not found."
    path = get_path(team["id"])
    if not path:
        return False, "Path not found."

    order, idx = path["station_order"], path["current_index"]
    if idx is None or idx >= len(order):
        return False, "Already finished!"

    expected_id = order[idx]
    if scanned_station_id != expected_id:
        return False, "Not your elephant."

    # 1. advance pointer
    new_idx = idx + 1
    supabase.table("paths").update({"current_index": new_idx}).eq(
        "team_id", team["id"]
    ).execute()

    # 2. award points for the station
    try:
        supabase.table("score_events").insert({
            "team_id": team["id"],
            "station_id": expected_id,
            "points": 10
        }).execute()
    except Exception as e:
        # duplicate means they already got these points
        print("Score insert skipped:", e)

    # 3. if they just finished the last station, mark winner timestamp for this team
    finished = new_idx >= len(order)

    if finished and not team.get("won_at"):
        # Try to set won_at for THIS team if it's still null.
        # Note: this does not globally prevent others from setting won_at later.
        # For a strict "first team only" lock, move this to a SQL function or game table.
        try:
            supabase.table("teams").update({"won_at": "now()"}).eq("id", team["id"]).execute()
        except Exception as e:
            print("Setting won_at failed:", e)

    # Message
    if finished:
        return True, "Nice find! (+10) You finished the route."

    return True, "Nice find! (+10)"


# supabase realtime channel
# realtime is not working will work on this later
# if "lb_channel" not in st.session_state:
#     def _on_score_insert(payload):
#         # bump a session var so Streamlit reruns on next tick
#         st.session_state["_lb_bump"] = random.random()

#     st.session_state["lb_channel"] = (
#         supabase
#         .channel("scores_live")
#         .on("postgres_changes",
#             event="INSERT",
#             schema="public",
#             table="score_events",
#             callback=_on_score_insert)
#         .subscribe()
#     )

# Handle scan links in the game

def handle_scan_from_query():
    """
    If the page has team / station / scan=1 in the query string,
    try to advance and show a toast, then clear the params.
    """
    # Read query params with a backward compatible path
    try:
        params = st.query_params
    except Exception:
        params = st.experimental_get_query_params()  # older versions return dict of lists

    def first(v):
        if isinstance(v, list):
            return v[0] if v else None
        return v

    team = first(params.get("team"))
    station = first(params.get("station"))
    scan = first(params.get("scan"))

    # Nothing to do unless all three are present and scan=1
    if not (team and station and str(scan) == "1"):
        return

    ok, msg = advance_if_expected(team, station)
    if ok:
        st.success(msg)
    else:
        st.error(msg)

    # Clear query params so refresh does not trigger the scan
    try:
        st.query_params.clear()
    except Exception:
        st.experimental_set_query_params()

    st.rerun()   # restart the script without the old query string
    return

handle_scan_from_query()
st.header("Game")


RIDDLES = {
    "Library":   "Rows of friends with spines of ink; find the place where ideas link.",
    "Cafeteria": "Clatter and chatter at midday’s peak; hunger ends where trays you seek.",
}

st.markdown("<hr>", unsafe_allow_html=True)

# Left column: play area; Right column: leaderboard
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Team Console")
    team_slug = st.text_input("Team slug", value="red-1234")

    if team_slug.strip():
        team, next_station, idx = get_next_station(team_slug.strip())

        if not team:
            st.error("Team not found.")
        else:
            st.markdown(f"**Team:** {team['name']}  \n**Step:** {0 if idx is None else idx}")

            # guard: path or order may be missing
            path = get_path(team["id"])
            order = (path or {}).get("station_order") or []

            if not order or idx is None or idx >= len(order):
                st.success("Finished! 🎉")
            else:
                # safe to use idx now
                expected_id = order[idx]

                # In case next_station ever comes back None
                station_name = next_station['name'] if next_station else 'Unknown'
                st.info(f"**Riddle:** {RIDDLES.get(station_name, 'No riddle set yet.')}")

                # pick a wrong id if available
                wrong_id = next((sid for sid in order if sid != expected_id), None)

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("📷 Scan (simulate correct)"):
                        ok, msg = advance_if_expected(team_slug, expected_id)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

                with c2:
                    if st.button("📵 Scan (simulate wrong)"):
                        if wrong_id:
                            ok, msg = advance_if_expected(team_slug, wrong_id)
                            if ok:
                                st.warning("Unexpectedly advanced with a wrong id.")
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.warning("No alternate station to simulate a wrong scan.")

            # Reset to start (dev convenience)
            if st.button("↩️ Reset this team to start"):
                t = get_team_by_slug(team_slug.strip())
                if t:
                    supabase.table("paths").update({"current_index": 0}).eq("team_id", t["id"]).execute()
                    st.success("Reset to the first station.")
                    st.rerun()

            # Debug panel
            with st.expander("Debug: expected station id"):
                if team and next_station is not None and idx is not None and idx < len(order):
                    st.write("Expected ID:", expected_id)
                    st.write("Station name:", next_station["name"])
    else:
        st.warning("Enter your team slug to begin.")

    # LLM prototype for styling ↓
    st.markdown("---")
    st.subheader("💬 Guardian Chat")

    if "hints_used" not in st.session_state:
        st.session_state.hints_used = {}  # {station_id: int}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # [(role, text)]
    MAX_HINTS_PER_STATION = 1

    # Current station context
    station_id = None
    station_name = "Unknown"
    seed_riddle = ""
    if team_slug.strip():
        _team, _next_station, _idx = get_next_station(team_slug.strip())
        if _next_station:
            station_id = _next_station["id"]
            station_name = _next_station.get("name", "Unknown")
            seed_riddle = RIDDLES.get(station_name, "No riddle set yet.")

    # Reset hint counter if station changed
    if station_id is not None:
        if st.session_state.get("last_station_id") != station_id:
            st.session_state.hints_used[station_id] = 0
            st.session_state["last_station_id"] = station_id


    # --- Chat Bubble CSS ---
    st.markdown('''
    <style>
    .chat-row { display: flex; margin-bottom: 10px; }
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 70%;
        font-size: 1.08rem;
        line-height: 1.5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        word-break: break-word;
    }
    .chat-user {
        margin-left: auto;
        background: #ffe5b4;
        color: #333;
        border-bottom-right-radius: 6px;
        border-top-right-radius: 18px;
        border-top-left-radius: 18px;
        border-bottom-left-radius: 18px;
    }
    .chat-assistant {
        margin-right: auto;
        background: #f3f3f3;
        color: #222;
        border-bottom-left-radius: 6px;
        border-top-right-radius: 18px;
        border-top-left-radius: 18px;
        border-bottom-right-radius: 18px;
    }
    .thinking-dot {
        display: inline-block;
        width: 8px; height: 8px;
        margin: 0 2px;
        background: #bbb;
        border-radius: 50%;
        animation: blink 1.4s infinite both;
    }
    .thinking-dot:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes blink {
        0%, 80%, 100% { opacity: 0.3; }
        40% { opacity: 1; }
    }
    </style>
    ''', unsafe_allow_html=True)

    # Show chat history with bubbles
    for role, text in st.session_state.chat_history[-10:]:
        if role == "user":
            st.markdown(f'<div class="chat-row"><div class="chat-bubble chat-user">{text}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-row"><div class="chat-bubble chat-assistant">{text}</div></div>', unsafe_allow_html=True)

    # Placeholders for thinking indicator and chat update
    thinking_placeholder = st.empty()
    # Show thinking indicator above the input box if in thinking state
    if hasattr(st.session_state, "_show_thinking") and st.session_state._show_thinking:
        thinking_html = '<div class="chat-row"><div class="chat-bubble chat-assistant"><span class="thinking-dot"></span><span class="thinking-dot"></span><span class="thinking-dot"></span></div></div>'
        thinking_placeholder.markdown(thinking_html, unsafe_allow_html=True)

    # Clear input if requested
    if st.session_state.get("_clear_guardian_input"):
        st.session_state["guardian_input"] = ""
        st.session_state["_clear_guardian_input"] = False
    user_msg = st.text_input("Ask the guardian", key="guardian_input")
    # Custom button styling for Send and Ask for a hint
    st.markdown('''
    <style>
    .stButton > button, .stButton > button:active, .stButton > button:focus, .stButton > button:hover {
        background-color: #FF7900 !important;
        color: #fff !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 1.08rem !important;
        font-weight: 600 !important;
        padding: 0.5em 1.5em !important;
        transition: background 0.2s;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        text-shadow: 0 1px 2px rgba(0,0,0,0.08);
    }
    .stButton > button:hover, .stButton > button:focus {
        background: #FF9800 !important;
        color: #fff !important;
        border: none !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.08);
    }
    .stButton > button * {
        color: #fff !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.08);
    }
    </style>
    ''', unsafe_allow_html=True)
    col_send, col_hint = st.columns(2)
    send_clicked = col_send.button("Send")
    hint_clicked = col_hint.button("Ask for a hint")

    if send_clicked or hint_clicked:
        # Set flag to clear input on next rerun
        st.session_state["_clear_guardian_input"] = True
        if not team_slug.strip():
            st.warning("Enter a team slug first.")
        elif station_id is None:
            st.info("You’ve finished the hunt. Great job.")
        else:
            give_hint = False
            if hint_clicked:
                used = st.session_state.hints_used.get(station_id, 0)
                if used >= MAX_HINTS_PER_STATION:
                    st.info("You’ve used your hint for this station.")
                else:
                    st.session_state.hints_used[station_id] = used + 1
                    give_hint = True

            msg = user_msg or ""
            # Show user message immediately in chat history
            st.session_state.chat_history.append(("user", msg))

            # Set state to show thinking indicator only
            st.session_state._show_thinking = {
                "station_name": station_name,
                "msg": msg,
                "seed_riddle": seed_riddle,
                "give_hint": give_hint
            }
            st.rerun()


    # Step 1: Show thinking indicator if needed
    if hasattr(st.session_state, "_show_thinking") and st.session_state._show_thinking:
        thinking_html = '<div class="chat-row"><div class="chat-bubble chat-assistant"><span class="thinking-dot"></span><span class="thinking-dot"></span><span class="thinking-dot"></span></div></div>'
        thinking_placeholder.markdown(thinking_html, unsafe_allow_html=True)
        # Set up for next rerun to generate reply
        st.session_state._awaiting_guardian = st.session_state._show_thinking
        st.session_state._show_thinking = None
        st.stop()

    # Step 2: Handle the actual LLM reply and typing animation after rerun
    if hasattr(st.session_state, "_awaiting_guardian") and st.session_state._awaiting_guardian:
        params = st.session_state._awaiting_guardian
        reply = guardian_reply(params["station_name"], params["msg"], params["seed_riddle"], params["give_hint"])
        typing_placeholder = thinking_placeholder
        displayed = ""
        for c in reply:
            displayed += c
            typing_html = f'<div class="chat-row"><div class="chat-bubble chat-assistant">{displayed}</div></div>'
            typing_placeholder.markdown(typing_html, unsafe_allow_html=True)
            time.sleep(0.012)
        typing_placeholder.empty()
        st.session_state.chat_history.append(("assistant", reply))
        st.session_state._awaiting_guardian = None
        st.rerun()


with col2:
    st.subheader("🏆 Leaderboard")
    try:
        rows = supabase.rpc("get_leaderboard").execute().data
        if rows:
            medals = {1: '🥇', 2: '🥈', 3: '🥉'}
            for r in rows:
                medal = medals.get(r['rank'], '')
                st.markdown(f"{medal} #{r['rank']}  <b>{r['team_name']}</b>: <b>{r['points']} pts</b>", unsafe_allow_html=True)
        else:
            st.write("No scores yet.")
    except Exception as e:
        st.error(f"Could not load leaderboard. {e}")

    # manual refresh button
    if st.button("↻ Refresh leaderboard"):
        st.rerun()