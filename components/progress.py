import streamlit as st

from core.config import (
    MAX_HEARTS,
    SKILL_COLORS,
)


def unlock_achievements(language, progress):
    possible_badges = []

    if progress["overall_xp"] > 0:
        possible_badges.append(
            "🌱 First Steps"
        )

    if (
        progress["skill_levels"][
            "Sentence Builder"
        ] > 0
    ):
        possible_badges.append(
            f"🧩 {language} Sentence Starter"
        )

    if (
        progress["skill_levels"][
            "Pronunciation"
        ] > 0
    ):
        possible_badges.append(
            f"🎙️ {language} Voice Starter"
        )

    if progress["streak"] >= 5:
        possible_badges.append(
            f"🔥 {language} Five-Day Streak"
        )

    for badge in possible_badges:
        if badge not in st.session_state.achievements:
            st.session_state.achievements.append(badge)


def render_progress():
    back_column, title_column = st.columns([1, 5])

    with back_column:
        if st.button("← Home"):
            st.session_state.current_view = "Home"
            st.rerun()

    with title_column:
        st.title("🏆 Your Progress")

    language = st.session_state.active_language
    progress = st.session_state.language_progress[
        language
    ]

    unlock_achievements(
        language,
        progress,
    )

    st.subheader(f"{language} progress")

    metric_one, metric_two, metric_three, metric_four = (
        st.columns(4)
    )

    with metric_one:
        st.metric(
            "Overall XP",
            progress["overall_xp"],
        )

    with metric_two:
        st.metric(
            "Current streak",
            f'{progress["streak"]} days',
        )

    with metric_three:
        st.metric(
            "Coins",
            st.session_state.coins,
        )

    with metric_four:
        st.metric(
            "Hearts",
            (
                f'{st.session_state.hearts}/'
                f'{MAX_HEARTS}'
            ),
        )

    if progress["starting_level"] is None:
        st.warning(
            "Choose a starting level on the homepage "
            "to begin tracking this language."
        )
        return

    level_one, level_two = st.columns(2)

    with level_one:
        st.info(
            f'Current level: '
            f'**{progress["current_level"]}**'
        )

    with level_two:
        st.info(
            f'Unlocked levels: '
            f'**{len(progress["unlocked_levels"])}**'
        )

    st.markdown("### Weekly goal")

    goal_options = [
        30,
        60,
        90,
        120,
        180,
    ]

    selected_goal = st.selectbox(
        "Weekly learning goal",
        goal_options,
        index=goal_options.index(
            progress["weekly_goal"]
        ),
        format_func=(
            lambda minutes: f"{minutes} minutes"
        ),
        key=f"progress_goal_{language}",
    )

    progress["weekly_goal"] = selected_goal

    weekly_percentage = min(
        progress["weekly_minutes"]
        / progress["weekly_goal"],
        1.0,
    )

    st.progress(weekly_percentage)

    st.caption(
        f'{progress["weekly_minutes"]} of '
        f'{progress["weekly_goal"]} minutes completed.'
    )

    paused = st.toggle(
        "Pause this language without losing its streak",
        value=progress["paused"],
        key=f"pause_progress_{language}",
    )

    progress["paused"] = paused

    if paused:
        st.warning(
            f"{language} is paused. Its streak will remain safe."
        )

    st.markdown("### Skill progress")

    for skill, color in SKILL_COLORS.items():
        practice_points = progress[
            "skill_levels"
        ][skill]

        skill_level = (
            practice_points // 20
        ) + 1

        points_toward_next_level = (
            practice_points % 20
        )

        st.markdown(
            f"""
            <div style="
                color: {color};
                font-weight: 800;
                margin-top: 0.8rem;
            ">
                {skill} · Level {skill_level}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(
            points_toward_next_level / 20
        )

        st.caption(
            f"{points_toward_next_level}/20 practice "
            "points toward the next skill level."
        )

    st.markdown("### Achievements")

    if st.session_state.achievements:
        badge_columns = st.columns(
            min(
                3,
                len(st.session_state.achievements),
            )
        )

        for index, badge in enumerate(
            st.session_state.achievements
        ):
            column = badge_columns[
                index % len(badge_columns)
            ]

            with column:
                st.success(badge)

    else:
        st.info(
            "Complete your first activity to unlock a badge."
        )