import streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

with open("background.svg", "rb") as f:
    svg_data = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <style>
    .block-container {{
        padding-top: 0;
        padding-right: 0;
        padding-bottom: 0;
        padding-left: 0;
        max-width: 100%;
    }}

    .stApp {{
        background-image: url("data:image/svg+xml;base64,{svg_data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        min-height: 100vh;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(
    """
    <div class="clock-wrap">
        <div id="clock" class="time-box"></div>
    </div>

    <style>
    body {
        margin: 0;
        background: transparent;
    }

    .clock-wrap {
        width: 100%;
        display: flex;
        justify-content: flex-start;
        padding-top: 58px;
        padding-left: 12px;
    }

    .time-box {
        background-color: rgb(24, 94, 148);
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 24px;
        color: black;
        transform: rotate(10deg);
        font-weight: bold;
        box-shadow: 0 0 10px rgba(7, 7, 115);
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    </style>

    <script>
    function updateClock() {
        document.getElementById("clock").innerText =
            new Date().toLocaleTimeString();
    }

    updateClock();
    setInterval(updateClock, 1000);
    </script>
    """,
    height=120,
)

