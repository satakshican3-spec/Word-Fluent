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
from locales import language_codes, language_label, set_interface_language, t


st.set_page_config(
    page_title=APP_NAME,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

initialize_session_state()
apply_global_styles(st.session_state.dark_mode)
def render_interface_language_setup():
    if st.session_state.get("interface_language_selected"):
        return

    selected_language = st.session_state.get(
        "interface_language_choice",
        "en",
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
        use_container_width=True,
    ):
        set_interface_language(selected_language)
        st.session_state.interface_language_selected = True
        st.rerun()

    st.stop()


def render_interface_language_setup():
    if st.session_state.get("interface_language_selected"):
        return

    selected_language = st.session_state.get(
        "interface_language_choice",
        "en",
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
        use_container_width=True,
    ):
        set_interface_language(selected_language)
        st.session_state.interface_language_selected = True
        st.rerun()

    st.stop()

render_interface_language_setup()

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