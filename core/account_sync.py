import streamlit as st

from core.config import (
    DEFAULT_LANGUAGE,
    LANGUAGES,
    MAX_HEARTS,
)
from core.state import create_language_progress
from services.supabase_service import (
    fetch_language_progress,
    fetch_profile,
    save_language_progress,
    save_profile,
)


def save_online_state(user_id):
    profile_data = {
        "id": user_id,
        "display_name": st.session_state.display_name,
        "ui_language": st.session_state.ui_language,
        "dark_mode": st.session_state.dark_mode,
        "difficulty": st.session_state.difficulty,
        "session_length": st.session_state.session_length,
        "coins": st.session_state.coins,
        "hearts": st.session_state.hearts,
    }

    save_profile(profile_data)

    for language, progress in (
        st.session_state.language_progress.items()
    ):
        progress_data = {
            "user_id": user_id,
            "language": language,
            "starting_level": progress[
                "starting_level"
            ],
            "current_level": progress[
                "current_level"
            ],
            "unlocked_levels": progress[
                "unlocked_levels"
            ],
            "overall_xp": progress["overall_xp"],
            "skill_levels": progress["skill_levels"],
            "streak": progress["streak"],
            "weekly_minutes": progress[
                "weekly_minutes"
            ],
            "weekly_goal": progress["weekly_goal"],
            "paused": progress["paused"],
        }

        save_language_progress(progress_data)


def load_online_state(user_id):
    profile = fetch_profile(user_id)

    online_progress = fetch_language_progress(
        user_id
    )

    if not online_progress:
        if profile and profile.get("display_name"):
            st.session_state.display_name = profile[
                "display_name"
            ]

        save_online_state(user_id)
        return "converted"

    if profile:
        profile_fields = [
            "display_name",
            "ui_language",
            "dark_mode",
            "difficulty",
            "session_length",
            "coins",
            "hearts",
        ]

        for field in profile_fields:
            if profile.get(field) is not None:
                st.session_state[field] = profile[field]

    restored_progress = {
        language: create_language_progress()
        for language in LANGUAGES
    }

    progress_fields = [
        "starting_level",
        "current_level",
        "unlocked_levels",
        "overall_xp",
        "skill_levels",
        "streak",
        "weekly_minutes",
        "weekly_goal",
        "paused",
    ]

    for saved_progress in online_progress:
        language = saved_progress["language"]

        if language not in restored_progress:
            continue

        for field in progress_fields:
            if saved_progress.get(field) is not None:
                restored_progress[language][field] = (
                    saved_progress[field]
                )

    st.session_state.language_progress = (
        restored_progress
    )

    return "restored"


def reset_to_guest_state():
    st.session_state.guest_mode = True
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.display_name = "Guest Learner"
    st.session_state.ui_language = "English"
    st.session_state.active_language = (
        DEFAULT_LANGUAGE
    )
    st.session_state.dark_mode = False
    st.session_state.coins = 100
    st.session_state.hearts = MAX_HEARTS
    st.session_state.current_view = "Home"
    st.session_state.difficulty = "Balanced"
    st.session_state.session_length = 5
    st.session_state.language_progress = {
        language: create_language_progress()
        for language in LANGUAGES
    }
    st.session_state.achievements = []