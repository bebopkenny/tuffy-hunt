import streamlit as st
import base64
from db import supabase
from typing import Optional, Tuple
import random
from llm import ask_grok, guardian_reply


# 1. Page config
st.set_page_config(page_title="Tuffy Hunt", layout="wide")

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
    <ul style='margin: 20px auto; max-width: 600px; font-size: 1.1rem; line-height: 1.5;'>
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
    """,
    unsafe_allow_html=True
)

# 4. “Let’s Get Started” button (centered, mobile-friendly, with hover effect)
st.markdown(
  """
  <style>
  .start-btn {
    background-color: #FF7900;
    color: white !important;
    padding: 12px 25px;
    font-size: 1.1rem;
    border-radius: 6px;
    text-decoration: none !important;
    transition: background-color 0.2s ease;
    display: inline-block;
  }
    .start-btn:hover, .start-btn:focus, .start-btn:active {
      background-color: #FF9800;
      color: white !important;
      text-decoration: none !important;
    }
  </style>
  <div style='display:flex; justify-content:center; margin:30px 0;'>
    <a href="#start" class="start-btn">Let's Get Started</a>
  </div>
  """,
  unsafe_allow_html=True
)

# 5. Simulated bottom orange banner (footer)
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
    st.subheader("Guardian Chat")

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

    # Show chat history
    for role, text in st.session_state.chat_history[-10:]:
        if role == "user":
            st.write(f"**You:** {text}")
        else:
            st.write(f"**Guardian:** {text}")

    user_msg = st.text_input("Ask the guardian", key="guardian_input")
    col_send, col_hint = st.columns(2)
    send_clicked = col_send.button("Send")
    hint_clicked = col_hint.button("Ask for a hint")

    if send_clicked or hint_clicked:
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
            st.session_state.chat_history.append(("user", msg))
            reply = guardian_reply(station_name, msg, seed_riddle, give_hint)
            st.session_state.chat_history.append(("assistant", reply))
            st.rerun()


with col2:
    st.subheader("Leaderboard")
    try:
        rows = supabase.rpc("get_leaderboard").execute().data
        if rows:
            for r in rows:
                st.write(f"#{r['rank']}  {r['team_name']}: {r['points']} pts")
        else:
            st.write("No scores yet.")
    except Exception as e:
        st.error(f"Could not load leaderboard. {e}")

    # manual refresh button
    if st.button("↻ Refresh leaderboard"):
        st.rerun()
