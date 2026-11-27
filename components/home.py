from html import escape

import streamlit as st

from core.config import LANGUAGES, LEVELS, MAX_HEARTS
from locales import (
    get_interface_language,
    language_codes,
    language_label as interface_language_label,
    set_interface_language,
    t,
)

LANGUAGE_FLAGS = {
    "English": "🇬🇧",
    "French": "🇫🇷",
    "Spanish": "🇪🇸",
    "Hindi": "🇮🇳",
    "Bengali": "🇧🇩",
    "Korean": "🇰🇷",
    "Japanese": "🇯🇵",
}

ACTIVITIES = (
    {
        "icon": "📖",
        "title_key": "activity_read_write",
        "description_key": "lessons_description",
        "view": "Lessons",
        "gradient": "linear-gradient(135deg, #4F78FF, #7D55F6)",
        "shadow": "rgba(91, 92, 232, .24)",
    },
    {
        "icon": "🎧",
        "title_key": "activity_listen",
        "description_key": "listening_description",
        "view": "Listening",
        "gradient": "linear-gradient(135deg, #6847F5, #18BFD0)",
        "shadow": "rgba(75, 99, 231, .24)",
    },
    {
        "icon": "🎙️",
        "title_key": "activity_speak",
        "description_key": "speaking_description",
        "view": "Speaking",
        "gradient": "linear-gradient(135deg, #3C8CF4, #35D29D)",
        "shadow": "rgba(45, 169, 190, .24)",
    },
    {
        "icon": "🧩",
        "title_key": "activity_play_practise",
        "description_key": "sentence_builder_description",
        "view": "Sentence Builder",
        "gradient": "linear-gradient(135deg, #8B5CF6, #FFB52E)",
        "shadow": "rgba(160, 99, 177, .22)",
    },
)


def _open_view(view_name):
    st.session_state.current_view = view_name
    st.rerun()


def _translated_level_label(level):
    translation_key = f"level_{level.lower().replace(' ', '_')}"
    return t(translation_key)


def _section_heading(title, description=None):
    st.markdown(
        f'<div class="wf-section-heading">{escape(title)}</div>',
        unsafe_allow_html=True,
    )

    if description:
        st.markdown(
            f'<div class="wf-section-copy">{escape(description)}</div>',
            unsafe_allow_html=True,
        )


def _stat_card(label, value):
    st.markdown(
        f"""
        <div class="wf-stat">
            <div class="wf-stat-label">{escape(str(label))}</div>
            <div class="wf-stat-value">{escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_hero(active_language, progress):
    flag = LANGUAGE_FLAGS.get(active_language, "🌍")
    level = progress.get("current_level")

    copy_column, art_column = st.columns([1.12, 0.88], gap="large")

    with copy_column:
        st.markdown(
            f"""
            <div class="wf-hero-copy">
                <div class="wf-kicker">
                    {flag} {escape(t('learning'))} {escape(active_language)}
                </div>
                <div class="wf-hero-title">
                    {escape(t('hero_learn_language'))}
                    <span class="wf-gradient-text">{escape(t('hero_your_way'))}</span>
                </div>
                <div class="wf-hero-description">
                    {escape(t('hero_description'))}
                </div>
                <div class="wf-feature-strip">
                    <div class="wf-feature-pill"><span>🎮</span>{escape(t('hero_games'))}</div>
                    <div class="wf-feature-pill"><span>🎧</span>{escape(t('listening'))}</div>
                    <div class="wf-feature-pill"><span>🎙️</span>{escape(t('pronunciation'))}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        start_column, coach_column = st.columns(2)

        with start_column:
            if st.button(
                f"{t('start_learning')} →",
                key="home_start_learning",
                type="primary",
                width="stretch",
                disabled=level is None,
            ):
                _open_view("Lessons")

        with coach_column:
            if st.button(
                f"🎙️ {t('pronunciation')}",
                key="home_open_pronunciation",
                width="stretch",
                disabled=level is None,
            ):
                _open_view("Pronunciation")

        if level is None:
            st.caption(t("choose_level_unlock"))

    with art_column:
        st.markdown(
            """
            <div class="wf-hero-visual" aria-hidden="true">
                <div class="wf-art-globe">🌐</div>
                <div class="wf-art-bubble wf-art-bubble-one">¡Hola!</div>
                <div class="wf-art-bubble wf-art-bubble-two">Bonjour!</div>
                <div class="wf-art-bubble wf-art-bubble-three">こんにちは!</div>
                <div class="wf-art-learner">👩🏽‍💻</div>
                <div class="wf-art-headphones">🎧</div>
                <div class="wf-art-books">📚</div>
                <div class="wf-art-laptop">
                    <span>📖</span><strong>WordFluent</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_stats(active_language, progress):
    weekly_goal = max(int(progress.get("weekly_goal") or 1), 1)
    weekly_minutes = int(progress.get("weekly_minutes") or 0)

    stat_columns = st.columns(4)

    with stat_columns[0]:
        _stat_card(t("coins"), f"🪙 {st.session_state.coins}")

    with stat_columns[1]:
        _stat_card(
            t("hearts"),
            f"❤️ {st.session_state.hearts}/{MAX_HEARTS}",
        )

    with stat_columns[2]:
        _stat_card(
            t("language_streak", learning_language=active_language),
            t("days", count=f"🔥 {progress.get('streak', 0)}"),
        )

    with stat_columns[3]:
        _stat_card(
            t("weekly_goal"),
            t(
                "minutes_short",
                current=weekly_minutes,
                goal=weekly_goal,
            ),
        )


def _render_language_picker(active_language):
    _section_heading(
        t("choose_language"),
        t("choose_language_description"),
    )

    language_columns = st.columns(len(LANGUAGES), gap="small")

    for column, (language_name, details) in zip(
        language_columns,
        LANGUAGES.items(),
    ):
        selected = language_name == active_language
        flag = LANGUAGE_FLAGS.get(language_name, "🌍")

        with column:
            st.markdown(
                f"""
                <div class="wf-language-card">
                    <div class="wf-language-flag">{flag}</div>
                    <div class="wf-language-name">{escape(language_name)}</div>
                    <div class="wf-language-native">{escape(details['native_name'])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                t("selected") if selected else t("choose"),
                key=f"choose_language_{language_name}",
                type="primary" if selected else "secondary",
                width="stretch",
                disabled=selected,
            ):
                st.session_state.active_language = language_name
                st.session_state.pop("listening_game", None)
                st.session_state.pop("speaking_game", None)
                st.session_state.pop("pronunciation_game", None)
                st.rerun()


def _render_level_setup(active_language, progress):
    _section_heading(t("your_learning_level"))

    if progress.get("starting_level") is None:
        st.info(t("choose_starting_level_help"))
        selection_column, action_column = st.columns([2.2, 1])

        with selection_column:
            chosen_level = st.selectbox(
                t("starting_level"),
                LEVELS,
                format_func=_translated_level_label,
                key=f"starting_level_choice_{active_language}",
            )

        with action_column:
            st.write("")
            if st.button(
                t("confirm_starting_level"),
                type="primary",
                key=f"confirm_level_{active_language}",
                width="stretch",
            ):
                level_position = LEVELS.index(chosen_level)
                progress["starting_level"] = chosen_level
                progress["current_level"] = chosen_level
                progress["unlocked_levels"] = LEVELS[: level_position + 1]

                st.success(
                    t(
                        "levels_unlocked_success",
                        level=_translated_level_label(chosen_level),
                        learning_language=active_language,
                    )
                )
                st.rerun()

        return True

    st.markdown(
        f"""
        <div class="wf-level-card">
            <strong>{escape(t('current_level'))}: {escape(_translated_level_label(progress['current_level']))}</strong>
            <p>{escape(t('levels_ready', count=len(progress.get('unlocked_levels', [])), language=active_language))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return False


def _render_activities(locked):
    _section_heading(
        t("choose_activity"),
        t("choose_activity_description"),
    )

    activity_columns = st.columns(4, gap="medium")

    for column, activity in zip(activity_columns, ACTIVITIES):
        title = t(activity["title_key"])

        with column:
            st.markdown(
                f"""
                <div class="wf-activity-card"
                     style="--wf-card-gradient:{activity['gradient']};--wf-card-shadow:{activity['shadow']};">
                    <div class="wf-activity-icon">{activity['icon']}</div>
                    <div class="wf-activity-title">{escape(title)}</div>
                    <div class="wf-activity-copy">{escape(t(activity['description_key']))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                t("open_activity", activity=title),
                key=f"home_open_{activity['view']}",
                type="primary",
                width="stretch",
                disabled=locked,
            ):
                _open_view(activity["view"])

    if locked:
        st.caption(t("choose_level_unlock"))


def _render_quick_actions(locked):
    _section_heading(t("more_practice"))
    pronunciation_column, progress_column = st.columns(2)

    with pronunciation_column:
        st.markdown(
            f"""
            <div class="wf-mini-card">
                <div>🎤</div>
                <strong>{escape(t('pronunciation'))}</strong>
                <p>{escape(t('pronunciation_description'))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            t("open_activity", activity=t("pronunciation")),
            key="home_quick_pronunciation",
            width="stretch",
            disabled=locked,
        ):
            _open_view("Pronunciation")

    with progress_column:
        st.markdown(
            f"""
            <div class="wf-mini-card">
                <div>🏆</div>
                <strong>{escape(t('progress'))}</strong>
                <p>{escape(t('progress_description'))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            t("open_activity", activity=t("progress")),
            key="home_quick_progress",
            width="stretch",
        ):
            _open_view("Progress")


def _render_weekly_progress(active_language, progress):
    weekly_goal = max(int(progress.get("weekly_goal") or 1), 1)
    weekly_minutes = int(progress.get("weekly_minutes") or 0)
    weekly_percentage = min(weekly_minutes / weekly_goal, 1.0)

    _section_heading(t("weekly_progress"))
    st.progress(weekly_percentage)
    st.caption(
        t(
            "weekly_progress_caption",
            current=weekly_minutes,
            goal=weekly_goal,
            learning_language=active_language,
        )
    )


def _render_settings():
    with st.expander(f"⚙️ {t('session_settings')}"):
        interface_column, theme_column = st.columns(2)

        with interface_column:
            current_interface_language = get_interface_language()
            selected_interface_language = st.selectbox(
                t("interface_language"),
                options=language_codes(),
                index=language_codes().index(current_interface_language),
                format_func=interface_language_label,
                key="home_interface_language",
            )

            if selected_interface_language != current_interface_language:
                set_interface_language(selected_interface_language)
                st.rerun()

        with theme_column:
            st.toggle(t("dark_mode"), key="dark_mode")

        length_column, difficulty_column = st.columns(2)

        with length_column:
            st.select_slider(
                t("session_length"),
                options=[5, 10, 15, 20, 30],
                key="session_length",
                format_func=lambda minutes: t("minutes", count=minutes),
            )

        with difficulty_column:
            st.selectbox(
                t("difficulty"),
                ["Relaxed", "Balanced", "Challenging", "Custom"],
                format_func=lambda difficulty: t(
                    f"difficulty_{difficulty.lower()}"
                ),
                key="difficulty",
            )


def render_home():
    active_language = st.session_state.active_language
    progress = st.session_state.language_progress[active_language]

    _render_hero(active_language, progress)
    _render_stats(active_language, progress)
    _render_language_picker(active_language)
    locked = _render_level_setup(active_language, progress)
    _render_activities(locked)
    _render_quick_actions(locked)
    _render_weekly_progress(active_language, progress)
    _render_settings()
