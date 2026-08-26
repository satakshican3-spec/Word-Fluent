import streamlit as st

from components.account import render_account
from components.home import render_home
from components.lessons import render_lessons
from components.progress import render_progress
from components.pronunciation import render_pronunciation
from components.sentence_builder import (
    render_sentence_builder,
)
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


def render_account_shortcut():
    empty_column, account_column = st.columns(
        [5, 1]
    )

    with account_column:
        if st.session_state.authenticated:
            button_label = (
                f"👤 {st.session_state.display_name}"
            )
        else:
            button_label = "👤 Guest"

        if st.button(
            button_label,
            key="global_account_button",
        ):
            st.session_state.current_view = "Account"
            st.rerun()


if st.session_state.current_view != "Account":
    render_account_shortcut()


VIEWS = {
    "Home": render_home,
    "Account": render_account,
    "Sentence Builder": render_sentence_builder,
    "Pronunciation": render_pronunciation,
    "Lessons": render_lessons,
    "Progress": render_progress,
}

current_view = st.session_state.current_view
view_renderer = VIEWS.get(
    current_view,
    render_home,
)

view_renderer()