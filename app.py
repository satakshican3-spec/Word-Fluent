import streamlit as st

from components.account import render_account
from components.home import render_home
from components.lessons import render_lessons
from components.listening_v2 import render_listening
from components.progress import render_progress
from components.pronunciation import render_pronunciation
from components.sentence_builder import render_sentence_builder
from components.speaking import render_speaking
from core.config import APP_NAME, PAGE_ICON, TAGLINE
from core.state import initialize_session_state
from core.styles import apply_global_styles
from locales import (
    language_codes,
    language_label,
    set_interface_language,
    t,
)


st.set_page_config(
    page_title=APP_NAME,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

initialize_session_state()
apply_global_styles(st.session_state.dark_mode)


VIEWS = {
    "Home": render_home,
    "Account": render_account,
    "Listening": render_listening,
    "Speaking": render_speaking,
    "Sentence Builder": render_sentence_builder,
    "Pronunciation": render_pronunciation,
    "Lessons": render_lessons,
    "Progress": render_progress,
}


def go_to(view_name):
    """Open a WordFluent page and refresh the Streamlit screen."""
    if view_name not in VIEWS:
        view_name = "Home"

    st.session_state.current_view = view_name
    st.rerun()


def render_interface_language_setup():
    if st.session_state.get("interface_language_selected"):
        return

    selected_language = st.session_state.get(
        "interface_language_choice",
        "en",
    )

    left_space, setup_column, right_space = st.columns([1, 2.2, 1])

    with setup_column:
        st.markdown(
            """
            <div class="wf-welcome-mark">📖</div>
            <div class="wf-welcome-brand">Word<span>Fluent</span></div>
            """,
            unsafe_allow_html=True,
        )
        st.title(
            f"🌍 {t('choose_interface_title', language=selected_language)}"
        )
        st.write(
            t("choose_interface_help", language=selected_language)
        )

        selected_language = st.selectbox(
            t("interface_language", language=selected_language),
            options=language_codes(),
            format_func=language_label,
            key="interface_language_choice",
        )

        if st.button(
            t("continue", language=selected_language),
            type="primary",
            width="stretch",
        ):
            set_interface_language(selected_language)
            st.session_state.interface_language_selected = True
            st.rerun()

    st.stop()


def render_top_navigation():
    """Render the same compact navigation bar on every app page."""
    current_view = st.session_state.current_view
    account_name = (
        st.session_state.display_name
        if st.session_state.authenticated
        else t("guest")
    )

    columns = st.columns([2.35, 0.9, 0.95, 0.95, 0.95, 0.95, 1.15])

    with columns[0]:
        st.markdown(
            f"""
            <div class="wf-brand-lockup">
                <div class="wf-brand-mark">📖</div>
                <div>
                    <div class="wf-brand-name">Word<span>Fluent</span></div>
                    <div class="wf-brand-tagline">{TAGLINE}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    navigation_items = [
        ("Home", t("home")),
        ("Lessons", t("lessons")),
        ("Listening", t("listening")),
        ("Speaking", t("speaking")),
        ("Progress", t("progress")),
    ]

    for column, (view_name, label) in zip(
        columns[1:6],
        navigation_items,
    ):
        with column:
            if st.button(
                label,
                key=f"nav_{view_name}",
                type="primary" if current_view == view_name else "secondary",
                width="stretch",
            ):
                go_to(view_name)

    with columns[6]:
        if st.button(
            f"👤 {account_name}",
            key="nav_account",
            type="primary" if current_view == "Account" else "secondary",
            width="stretch",
        ):
            go_to("Account")

    st.markdown('<div class="wf-nav-divider"></div>', unsafe_allow_html=True)


render_interface_language_setup()
render_top_navigation()

current_view = st.session_state.get("current_view", "Home")
view_renderer = VIEWS.get(current_view, render_home)
view_renderer()
