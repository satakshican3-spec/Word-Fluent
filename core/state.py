from copy import deepcopy

import streamlit as st

from core.config import (
    DEFAULT_LANGUAGE,
    DEFAULT_WEEKLY_GOAL,
    LANGUAGES,
    MAX_HEARTS,
    SKILL_COLORS,
)


def create_language_progress():
    return {
        "starting_level": None,
        "current_level": None,
        "unlocked_levels": [],
        "overall_xp": 0,
        "skill_levels": {
            skill: 0 for skill in SKILL_COLORS
        },
        "streak": 0,
        "weekly_minutes": 0,
        "weekly_goal": DEFAULT_WEEKLY_GOAL,
        "paused": False,
    }


def initialize_session_state():
    persistent_keys = [
        "active_language",
        "ui_language",
        "dark_mode",
        "difficulty",
        "session_length",
    ]

    for key in persistent_keys:
        if key in st.session_state:
            st.session_state[key] = st.session_state[key]

    defaults = {
        "guest_mode": True,
        "display_name": "Guest Learner",
        "ui_language": "English",
        "active_language": DEFAULT_LANGUAGE,
        "dark_mode": False,
        "coins": 100,
        "hearts": MAX_HEARTS,
        "current_view": "Home",
        "difficulty": "Balanced",
        "session_length": 5,
        "language_progress": {
            language: create_language_progress()
            for language in LANGUAGES
        },
        "achievements": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = deepcopy(value)