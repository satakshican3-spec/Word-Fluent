import streamlit as st

from core.config import (
    APP_NAME,
    LANGUAGES,
    LEVELS,
    MAX_HEARTS,
    SKILL_COLORS,
    TAGLINE,
)


def language_label(language_name):
    language = LANGUAGES[language_name]

    return (
        f"{language['code']} · {language_name} "
        f"({language['native_name']})"
    )


def stat_card(label, value):
    st.markdown(
        f"""
        <div class="wf-stat">
            <div class="wf-stat-label">{label}</div>
            <div class="wf-stat-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def activity_card(icon, title, description, color):
    st.markdown(
        f"""
        <div class="wf-card" style="border-top: 4px solid {color};">
            <div class="wf-card-icon">{icon}</div>
            <div class="wf-card-title">{title}</div>
            <div class="wf-card-copy">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home():
    language_names = list(LANGUAGES.keys())

    setting_one, setting_two, setting_three = st.columns(
        [2.2, 2.2, 1]
    )

    with setting_one:
        st.selectbox(
            "Learning language",
            language_names,
            key="active_language",
            format_func=language_label,
        )

    with setting_two:
        st.selectbox(
            "Menu language",
            language_names,
            key="ui_language",
            format_func=language_label,
        )

    with setting_three:
        st.toggle(
            "Dark mode",
            key="dark_mode",
        )

    active_language = st.session_state.active_language
    language_data = LANGUAGES[active_language]

    progress = st.session_state.language_progress[
        active_language
    ]

    st.markdown(
        f"""
        <div class="wf-hero">
            <div class="wf-logo">📖 🎙️</div>
            <h1>{APP_NAME}</h1>
            <p>{TAGLINE}</p>
            <p>
                Learning {active_language}
                · {language_data["native_name"]}
                · {language_data["code"]}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stat_one, stat_two, stat_three, stat_four = st.columns(4)

    with stat_one:
        stat_card(
            "Coins",
            f"🪙 {st.session_state.coins}",
        )

    with stat_two:
        stat_card(
            "Hearts",
            f"❤️ {st.session_state.hearts}/{MAX_HEARTS}",
        )

    with stat_three:
        stat_card(
            f"{active_language} streak",
            f"🔥 {progress['streak']} days",
        )

    with stat_four:
        stat_card(
            "Weekly goal",
            (
                f"{progress['weekly_minutes']}/"
                f"{progress['weekly_goal']} min"
            ),
        )

    st.markdown(
        '<div class="wf-section-title">Your learning level</div>',
        unsafe_allow_html=True,
    )

    if progress["starting_level"] is None:
        st.info(
            "Choose your starting level. That level and every "
            "level below it will be unlocked."
        )

        chosen_level = st.selectbox(
            "Starting level",
            LEVELS,
            key=f"starting_level_choice_{active_language}",
        )

        if st.button(
            "Confirm starting level",
            type="primary",
            key=f"confirm_level_{active_language}",
        ):
            level_position = LEVELS.index(chosen_level)

            progress["starting_level"] = chosen_level
            progress["current_level"] = chosen_level
            progress["unlocked_levels"] = LEVELS[
                : level_position + 1
            ]

            st.success(
                f"{chosen_level} and every lower level "
                f"are now unlocked for {active_language}."
            )

            st.rerun()

    else:
        level_one, level_two = st.columns(2)

        with level_one:
            stat_card(
                "Current level",
                progress["current_level"],
            )

        with level_two:
            stat_card(
                "Unlocked levels",
                len(progress["unlocked_levels"]),
            )

    st.markdown(
        '<div class="wf-section-title">Session settings</div>',
        unsafe_allow_html=True,
    )

    preference_one, preference_two = st.columns(2)

    with preference_one:
        st.select_slider(
            "Session length",
            options=[5, 10, 15, 20, 30],
            key="session_length",
            format_func=lambda minutes: f"{minutes} minutes",
        )

    with preference_two:
        st.selectbox(
            "Difficulty",
            [
                "Relaxed",
                "Balanced",
                "Challenging",
                "Custom",
            ],
            key="difficulty",
        )

    st.markdown(
        '<div class="wf-section-title">Choose an activity</div>',
        unsafe_allow_html=True,
    )

    activities = [
        (
            "🧩",
            "Sentence Builder",
            "Arrange or type words to build useful sentences.",
            SKILL_COLORS["Sentence Builder"],
        ),
        (
            "🎙️",
            "Pronunciation",
            "Speak aloud and receive level-based feedback.",
            SKILL_COLORS["Pronunciation"],
        ),
        (
            "📚",
            "Lessons",
            "Learn vocabulary and grammar at your level.",
            SKILL_COLORS["Grammar"],
        ),
        (
            "🏆",
            "Progress",
            "View goals, streaks, coins and achievements.",
            SKILL_COLORS["Vocabulary"],
        ),
    ]

    activity_columns = st.columns(4)
    level_not_selected = progress["starting_level"] is None

    for index, activity in enumerate(activities):
        icon, title, description, color = activity

        with activity_columns[index]:
            activity_card(
                icon,
                title,
                description,
                color,
            )

            if st.button(
                f"Open {title}",
                key=f"open_{title}",
                type="primary" if index == 0 else "secondary",
                disabled=level_not_selected,
            ):
                st.session_state.current_view = title
                st.rerun()

    if level_not_selected:
        st.caption(
            "Choose a starting level to unlock the activities."
        )
    elif st.session_state.current_view != "Home":
        st.info(
            f"{st.session_state.current_view} selected. "
            "We will connect this feature next."
        )

    weekly_goal = progress["weekly_goal"]
    weekly_minutes = progress["weekly_minutes"]
    weekly_percentage = min(
        weekly_minutes / weekly_goal,
        1.0,
    )

    st.markdown(
        '<div class="wf-section-title">Weekly progress</div>',
        unsafe_allow_html=True,
    )

    st.progress(weekly_percentage)

    st.caption(
        f"{weekly_minutes} of {weekly_goal} minutes completed "
        f"for {active_language} this week."
    )