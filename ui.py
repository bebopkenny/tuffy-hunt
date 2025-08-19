import streamlit as st
import base64
from db import supabase
from typing import Optional, Tuple

# 1. Page config
st.set_page_config(page_title="Tuffy Hunt", layout="wide")

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
    res = supabase.table("teams").select("id, name, slug, game_id").eq("slug", slug).single().execute()
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
    Returns ok message
    """
    team = get_team_by_slug(team_slug)
    if not team:
        return False, "Team not found"
    path = get_path(team["id"])
    if not path:
        return False, "Path not found"

    order, idx = path["station_order"], path["current_index"]
    if idx is None or idx >= len(order):
        return False, "Already finished"

    expected_id = order[idx]
    if scanned_station_id != expected_id:
        return False, "Not your elephant"

    # advance pointer
    new_idx = idx + 1
    supabase.table("paths").update({"current_index": new_idx}).eq(
        "team_id", team["id"]
    ).execute()

    # 👇 add the score event here
    try:
        supabase.table("score_events").insert({
            "team_id": team["id"],
            "station_id": expected_id,   # the one they just completed
            "points": 10
        }).execute()
    except Exception as e:
        # Supabase will throw if they already have a row for this team+station (due to unique index).
        # That’s okay—it means no double awarding.
        print("Score insert skipped:", e)

    return True, "Nice find! (+10)"

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
st.header("Game")

# Left column: play area; Right column: (future) leaderboard
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Team Console")

    # Team slug input (default to your seeded team from Step 1)
    team_slug = st.text_input("Team slug", value="red-1234")

    if team_slug.strip():
        team, next_station, idx = get_next_station(team_slug.strip())

        if not team:
            st.error("Team not found.")
        else:
            st.markdown(f"**Team:** {team['name']}  \n**Step:** {0 if idx is None else idx}")

            if next_station is None:
                st.success("Finished! 🎉")
            else:
                st.info(f"**Riddle:** {RIDDLES.get(next_station['name'], 'No riddle set yet.')}")

                # Fetch station_order so we can simulate good/wrong scans
                path = get_path(team["id"])
                order = path["station_order"]

                expected_id = order[idx]
                # pick a wrong id if available
                wrong_id = None
                for sid in order:
                    if sid != expected_id:
                        wrong_id = sid
                        break

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("📷 Scan (simulate correct)"):
                        ok, msg = advance_if_expected(team_slug, expected_id)
                        if ok:
                            st.success(msg)
                            st.rerun()  # refresh to show the next riddle
                        else:
                            st.error(msg)

                with c2:
                    if st.button("📵 Scan (simulate wrong)"):
                        if wrong_id:
                            ok, msg = advance_if_expected(team_slug, wrong_id)
                            if ok:
                                # should never happen (we chose a wrong_id)
                                st.warning("Unexpectedly advanced with a wrong id.")
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.warning("No alternate station to simulate a wrong scan.")
        # Reset button function
        if st.button("↩️ Reset this team to start"):
          team = get_team_by_slug(team_slug.strip())
          if team:
              supabase.table("paths").update({"current_index": 0}).eq("team_id", team["id"]).execute()
              st.success("Reset to the first station.")
              st.rerun()
        # TESTING for expected station ID
        with st.expander("Debug: expected station id"):
          if team and next_station is not None:
              st.write("Expected ID:", expected_id)
              st.write("Station name:", next_station["name"])      
    else:
        st.warning("Enter your team slug to begin.")