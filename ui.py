import streamlit as st
import base64

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