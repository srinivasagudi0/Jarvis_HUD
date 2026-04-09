import streamlit as st
#import streamlit.components.v1 as components

st.set_page_config(page_title="My Streamlit App", page_icon=":sparkles:", layout="wide")
st.title("Welcome Boss")

#components.html(
    """
    <div style="
        width: 300px;
        border: 1px solid black;
        padding: 10px;
        margin: 10px;
        background-color: #ccc;
        border-radius: 10px;
    ">
        <h3>Time</h3>
        <p>{}</p>
    </div>
    """,
    height=180,
    scrolling=False
)
