from datetime import datetime
import os
import platform
import shutil

import streamlit as st

from support import get_weather, respond_to_command

st.set_page_config(page_title="JARVIS HUD", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = [
        ("jarvis", "Good evening. All core systems are stable and standing by.")
    ]

st.markdown(
    """
    <style>
    :root{
        --bg:#07111a;--bg2:#0e2431;--panel:rgba(11,28,41,.72);--line:rgba(111,226,255,.24);
        --text:#eef8ff;--muted:#8baab8;--cyan:#8de8ff;--blue:#35b9ff;--glow:0 0 32px rgba(53,185,255,.18);
    }
    [data-testid="stHeader"],[data-testid="stDecoration"]{display:none;}
    .block-container{padding:1.2rem 1.4rem 1.4rem;max-width:1320px;}
    .stApp{
        color:var(--text);
        background:
            radial-gradient(circle at top right, rgba(52,140,177,.22), transparent 24%),
            radial-gradient(circle at left, rgba(17,111,165,.16), transparent 26%),
            linear-gradient(135deg, var(--bg), var(--bg2) 55%, #051018);
    }
    div[data-testid="stMetric"]{
        background:var(--panel);border:1px solid var(--line);border-radius:22px;
        padding:16px 18px;box-shadow:var(--glow);backdrop-filter:blur(14px);
    }
    div[data-testid="stMetricLabel"]{color:var(--muted);}
    .hero,.panel,.console{
        background:var(--panel);border:1px solid var(--line);border-radius:28px;
        box-shadow:var(--glow);backdrop-filter:blur(16px);
    }
    .hero{padding:28px 30px 24px;position:relative;overflow:hidden;min-height:250px;}
    .hero:before{
        content:"";position:absolute;inset:-40% auto auto 60%;width:360px;height:360px;border-radius:50%;
        background:radial-gradient(circle, rgba(141,232,255,.22), transparent 60%);
    }
    .eyebrow{color:var(--cyan);letter-spacing:.24em;font-size:.76rem;text-transform:uppercase;}
    .title{font-size:4.1rem;line-height:.94;font-weight:800;margin:.35rem 0 1rem;}
    .lead{max-width:720px;color:#c5d8e2;font-size:1.02rem;}
    .ring{
        width:210px;height:210px;margin-left:auto;border-radius:50%;position:relative;
        border:1px solid rgba(141,232,255,.28);
        background:
            radial-gradient(circle, rgba(141,232,255,.14), rgba(10,24,33,.12) 42%, transparent 43%),
            conic-gradient(from 160deg, rgba(141,232,255,.06), rgba(141,232,255,.82), rgba(53,185,255,.08));
        box-shadow:inset 0 0 44px rgba(141,232,255,.12),0 0 42px rgba(53,185,255,.16);
        animation:spin 14s linear infinite;
    }
    .ring:before,.ring:after{content:"";position:absolute;inset:18px;border-radius:50%;border:1px solid rgba(141,232,255,.22);}
    .ring:after{inset:54px;background:radial-gradient(circle, rgba(141,232,255,.18), rgba(7,17,26,.95) 65%);}
    .core{
        position:absolute;inset:0;display:grid;place-items:center;font-weight:700;letter-spacing:.2em;
        color:var(--cyan);text-transform:uppercase;font-size:.84rem;
    }
    .panel{padding:20px 22px;height:100%;}
    .panel h3,.console h3{margin:0 0 10px;font-size:1.05rem;}
    .list{display:grid;gap:12px;}
    .item{
        display:flex;justify-content:space-between;gap:12px;padding:12px 14px;border-radius:16px;
        border:1px solid rgba(141,232,255,.12);background:rgba(255,255,255,.02);
    }
    .label{color:var(--muted);font-size:.84rem;text-transform:uppercase;letter-spacing:.08em;}
    .value{font-weight:600;}
    .console{padding:20px 22px;margin-top:1rem;}
    .bubble{
        padding:12px 14px;border-radius:18px;margin:.45rem 0;max-width:820px;border:1px solid var(--line);
    }
    .user{background:rgba(53,185,255,.12);margin-left:auto;}
    .jarvis{background:rgba(255,255,255,.03);}
    .chip{
        display:inline-block;padding:6px 10px;margin:4px 6px 0 0;border-radius:999px;
        border:1px solid rgba(141,232,255,.18);color:var(--muted);font-size:.8rem;
    }
    .stTextInput input{
        background:rgba(255,255,255,.03);color:var(--text);border-radius:14px;border:1px solid var(--line);
    }
    .stButton button{
        width:100%;border-radius:14px;border:1px solid rgba(141,232,255,.3);
        background:linear-gradient(135deg, rgba(53,185,255,.2), rgba(141,232,255,.08));color:var(--text);
    }
    .panel-note{color:#c5d8e2;line-height:1.6;font-size:.97rem;}
    @keyframes spin{to{transform:rotate(360deg);}}
    </style>
    """,
    unsafe_allow_html=True,
)

now = datetime.now()
weather = get_weather("Sugar Land")
disk = shutil.disk_usage("/")
system_name = platform.node() or "Local Core"
used_disk = int((disk.used / disk.total) * 100)
presence = "Attentive" if 6 <= now.hour < 23 else "Low-light Watch"
greeting = "Good morning" if now.hour < 12 else "Good afternoon" if now.hour < 18 else "Good evening"

hero_left, hero_right = st.columns([1.6, 1], vertical_alignment="center")
with hero_left:
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">Human-Centered Tactical Interface</div>
            <div class="title">JARVIS</div>
            <div class="lead">
                {greeting}. This console is tuned for a cleaner, more human interface:
                calm visuals, direct telemetry, and a lightweight command loop that actually responds.
            </div>
            <div style="margin-top:16px">
                <span class="chip">Status: Online</span>
                <span class="chip">Presence: {presence}</span>
                <span class="chip">Weather: {weather}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with hero_right:
    st.markdown('<div class="hero"><div class="ring"><div class="core">Neural Core</div></div></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Local Time", now.strftime("%I:%M %p").lstrip("0"), now.strftime("%A"))
with col2:
    st.metric("Weather", weather.split(",")[0], weather.split(",")[1].strip() if "," in weather else "Live")
with col3:
    st.metric("Disk Usage", f"{used_disk}%", f"{disk.free // (1024**3)} GB free")

left, mid, right = st.columns([1.15, 1, 1])
with left:
    st.markdown(
        f"""
        <div class="panel">
            <h3>Assistant Profile</h3>
            <div class="list">
                <div class="item"><span class="label">Identity</span><span class="value">JARVIS Core</span></div>
                <div class="item"><span class="label">Operator</span><span class="value">Srinivas</span></div>
                <div class="item"><span class="label">Host</span><span class="value">{system_name}</span></div>
                <div class="item"><span class="label">Mode</span><span class="value">Observing + Assisting</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with mid:
    st.markdown(
        f"""
        <div class="panel">
            <h3>AI Link</h3>
            <div class="list">
                <div class="item"><span class="label">Backend</span><span class="value">OpenAI Responses API</span></div>
                <div class="item"><span class="label">Model</span><span class="value">{os.getenv("OPENAI_MODEL", "gpt-4-mini")}</span></div>
                <div class="item"><span class="label">Auth</span><span class="value">`OPENAI_API_KEY`</span></div>
                <div class="item"><span class="label">Chat Mode</span><span class="value">Live AI response</span></div>
            </div>
            <div class="panel-note" style="margin-top:14px;">
                The assistant is now intended to answer through OpenAI instead of local placeholder rules.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        f"""
        <div class="panel">
            <h3>Live Readiness</h3>
            <div class="list">
                <div class="item"><span class="label">Clock</span><span class="value">{now.strftime("%H:%M:%S")}</span></div>
                <div class="item"><span class="label">Date</span><span class="value">{now.strftime("%b %d, %Y")}</span></div>
                <div class="item"><span class="label">Climate</span><span class="value">{weather}</span></div>
                <div class="item"><span class="label">Storage</span><span class="value">{used_disk}% utilized</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="console"><h3>Command Console</h3>', unsafe_allow_html=True)
for role, message in st.session_state.history[-6:]:
    css = "user" if role == "user" else "jarvis"
    st.markdown(f'<div class="bubble {css}">{message}</div>', unsafe_allow_html=True)

with st.form("jarvis_console", clear_on_submit=True):
    command = st.text_input("Issue a command", placeholder="Try: time, weather, status, help")
    submitted = st.form_submit_button("Run Command")

if submitted and command.strip():
    st.session_state.history.append(("user", command.strip()))
    st.session_state.history.append(
        ("jarvis", respond_to_command(command, weather, system_name, st.session_state.history))
    )
    st.rerun()

st.markdown(
    """
    <div style="margin-top:10px;color:#8baab8;font-size:.88rem;">
        Suggested commands: <span class="chip">time</span><span class="chip">weather</span>
        <span class="chip">status</span><span class="chip">who are you</span><span class="chip">help</span>
    </div></div>
    """,
    unsafe_allow_html=True,
)
