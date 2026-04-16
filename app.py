# JARVIS HUD (rewritten by me).
# I'll probably clean this up later when I have time.

import streamlit as st
import os
import platform
import shutil
from datetime import datetime

from support import get_weather, respond_to_command

st.set_page_config(page_title="JARVIS HUD", layout="wide")

# init chat history (basic)
if "history" not in st.session_state:
    st.session_state.history = [
        ("jarvis", "Good evening. Systems look stable.")
    ]

# --- styles (final hopefully if no errors!) ---
st.markdown("""
<style>
    body {
        background: #0d1a22;
        color: #e6f2ff;
    }
    .hero-box {
        padding: 20px;
        border-radius: 18px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 18px;
    }
    .bubble {
        padding: 10px 14px;
        border-radius: 12px;
        margin: 6px 0;
        max-width: 720px;
    }
    .bubble.user {
        background: rgba(70,150,255,0.18);
        margin-left: auto;
    }
    .bubble.jarvis {
        background: rgba(255,255,255,0.07);
    }
    .chip {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        margin-right: 6px;
        font-size: .8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- system info ---
now = datetime.now()
weather = get_weather("Sugar Land")
disk = shutil.disk_usage("/")
used_pct = int((disk.used / disk.total) * 100)
host = platform.node() or "LocalHost"

# greeting (simple)
if now.hour < 12:
    greet = "Good morning"
elif now.hour < 18:
    greet = "Good afternoon"
else:
    greet = "Good evening"

presence = "Attentive" if 6 <= now.hour < 23 else "Low-light Watch"

# --- HERO ---
st.markdown(f"""
<div class="hero-box">
    <h1 style="margin:0;font-size:2.6rem;">JARVIS</h1>
    <p style="opacity:.85;margin-top:4px;">{greet}. Interface online.</p>
    <div style="margin-top:10px;">
        <span class="chip">Status: Online</span>
        <span class="chip">Presence: {presence}</span>
        <span class="chip">Weather: {weather}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- METRICS ---
c1, c2, c3 = st.columns(3)
c1.metric("Local Time", now.strftime("%I:%M %p").lstrip("0"), now.strftime("%A"))
c2.metric("Weather", weather.split(",")[0], weather.split(",")[1] if "," in weather else "")
c3.metric("Disk Usage", f"{used_pct}%", f"{disk.free // (1024**3)} GB free")

# dumb me thought commenting would work in streamlit, instead it just shows up as text.
def dummy():
    # these look nice but too much info for now and are also repetitive with the panels below, if you want them just uncomment.
    # --- PANELS ---
    left, mid, right = st.columns(3)

    with left:
        st.subheader("Assistant Profile")
        st.write("**Identity:** JARVIS Core")
        st.write("**Operator:** Srinivas")
        st.write(f"**Host:** {host}")
        st.write("**Mode:** Observing + Assisting")

    with mid:
        st.subheader("AI Link")
        st.write("**Backend:** OpenAI Responses API")
        st.write(f"**Model:** {os.getenv('OPENAI_MODEL', 'gpt-4-mini')}")
        st.write("**Auth:** OPENAI_API_KEY")
        st.caption("Using live OpenAI responses now.")

    with right:
        st.subheader("Live Readiness")
        st.write(f"**Clock:** {now.strftime('%H:%M:%S')}")
        st.write(f"**Date:** {now.strftime('%b %d, %Y')}")
        st.write(f"**Climate:** {weather}")
        st.write(f"**Storage:** {used_pct}% used")

#dummy()

# --- COMMAND CONSOLE ---
st.markdown("### Command Console")

# show last few messages
for role, msg in st.session_state.history[-6:]:
    css = "user" if role == "user" else "jarvis"
    st.markdown(f'<div class="bubble {css}">{msg}</div>', unsafe_allow_html=True)

# input form
with st.form("console", clear_on_submit=True):
    cmd = st.text_input("Issue a command", placeholder="Try: time, weather, status, help")
    run = st.form_submit_button("execute")
    # will take like 1 hr to implement so just hang in there, I got this, promise.
    voice = st.checkbox("Voice input (not implemented yet)", disabled=True)

if run and cmd.strip():
    st.session_state.history.append(("user", cmd.strip()))
    reply = respond_to_command(cmd, weather, host, st.session_state.history)
    st.session_state.history.append(("jarvis", reply))
    st.rerun()

st.caption("Suggested: time • weather • status • who are you • help")

