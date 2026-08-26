import streamlit as st

from components.home import render_home
from components.sentence_builder import render_sentence_builder
from core.config import APP_NAME, PAGE_ICON
from core.state import initialize_session_state
from core.styles import apply_global_styles


st.set_page_config(
    page_title=APP_NAME,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

initialize_session_state()
apply_global_styles(st.session_state.dark_mode)

if st.session_state.current_view == "Sentence Builder":
    render_sentence_builder()
else:
    render_home()