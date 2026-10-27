from uuid import uuid4

import streamlit as st

from components.speaking import (
    get_speaking_scenarios,
)
from locales import t
from services.game_engine import (
    calculate_reward,
    get_exercises,
)
from services.listening_modes import (
    LISTENING_MODES,
    MODE_LABEL_KEYS,
    build_listening_questions,
    check_listening_answer,
    replay_limit,
)
from services.pronunciation_engine import (
    generate_reference_audio,
)


@st.cache_data(
    show_spinner=False,
    ttl=86400,
)
def get_listening_audio(
    phrase,
    language,
    slow,
):
    return generate_reference_audio(
        phrase,
        language,
        slow,
    )


def _question_count(
    exercises,
    scenarios,
    mode,
):
    requested_minutes = int(
        st.session_state.get(
            "session_length",
            5,
        )
    )
    requested_questions = max(
        5,
        requested_minutes // 2,
    )

    if mode == "dialogue":
        return min(
            len(scenarios),
            requested_questions,
        )

    return min(
        len(exercises),
        requested_questions,
    )


def _choice_count():
    if (
        st.session_state.get(
            "difficulty"
        )
        == "Relaxed"
    ):
        return 3

    return 4


def _clear_listening_session():
    st.session_state.pop(
        "listening_game",
        None,
    )

def start_listening_session(
    language,
    mode,
):
    exercises = get_exercises(language)
    scenarios = get_speaking_scenarios(
        language
    )
    total = _question_count(
        exercises,
        scenarios,
        mode,
    )

    st.session_state.listening_game = {
        "id": uuid4().hex[:10],
        "language": language,
        "mode": mode,
        "questions": (
            build_listening_questions(
                exercises,
                scenarios,
                total,
                _choice_count(),
                mode,
            )
        ),
        "round_index": 0,
        "correct": 0,
        "coins": 0,
        "answered": False,
        "selected": None,
        "result": None,
        "reward": 0,
        "audio": b"",
        "audio_error": None,
        "audio_speed": None,
        "audio_plays": 0,
        "complete": False,
    }


def _reset_round(game):
    game["answered"] = False
    game["selected"] = None
    game["result"] = None
    game["reward"] = 0
    game["audio"] = b""
    game["audio_error"] = None
    game["audio_speed"] = None
    game["audio_plays"] = 0

def _play_audio(
    game,
    phrase,
    language,
    slow,
):
    with st.spinner(
        t("preparing_audio")
    ):
        result = get_listening_audio(
            phrase,
            language,
            slow,
        )

    game["audio"] = result["audio"]
    game["audio_error"] = result[
        "error"
    ]
    game["audio_speed"] = (
        t("listen_slow")
        if slow
        else t("listen_normal")
    )

    if result["audio"]:
        game["audio_plays"] += 1

def _render_audio(
    game,
    phrase,
    language,
):
    difficulty = st.session_state.get(
        "difficulty",
        "Balanced",
    )
    limit = replay_limit(difficulty)

    limit_reached = (
        limit is not None
        and game["audio_plays"] >= limit
    )

    normal_column, slow_column = (
        st.columns(2)
    )

    with normal_column:
        if st.button(
            f'🔊 {t("listen_normal")}',
            disabled=limit_reached,
            use_container_width=True,
        ):
            _play_audio(
                game,
                phrase,
                language,
                False,
            )
            st.rerun()

    with slow_column:
        if st.button(
            f'🐢 {t("listen_slow")}',
            disabled=limit_reached,
            use_container_width=True,
        ):
            _play_audio(
                game,
                phrase,
                language,
                True,
            )
            st.rerun()

    if limit is None:
        st.caption(
            t(
                "listening_replays_unlimited"
            )
        )
    else:
        remaining = max(
            0,
            limit - game["audio_plays"],
        )
        st.caption(
            t(
                "listening_replays_left",
                count=remaining,
            )
        )

    if game["audio"]:
        st.caption(
            game["audio_speed"]
        )
        st.audio(
            game["audio"],
            format="audio/mp3",
        )

    elif game["audio_error"]:
        st.warning(
            game["audio_error"]
        )

def _grant_correct_reward(
    game,
    progress,
):
    reward = calculate_reward(
        st.session_state.get(
            "difficulty",
            "Balanced",
        ),
        False,
    )

    game["correct"] += 1
    game["coins"] += reward
    game["reward"] = reward

    st.session_state.coins += reward
    progress["overall_xp"] += reward
    progress["weekly_minutes"] += 1

    skills = progress.setdefault(
        "skill_levels",
        {},
    )
    skills["Listening"] = (
        skills.get(
            "Listening",
            0,
        )
        + 1
    )

def _check_answer(
    game,
    answer,
    progress,
):
    difficulty = st.session_state.get(
        "difficulty",
        "Balanced",
    )
    question = game["questions"][
        game["round_index"]
    ]
    result = check_listening_answer(
        question,
        answer,
        difficulty,
    )

    game["answered"] = True
    game["selected"] = str(
        answer or ""
    ).strip()
    game["result"] = result

    if result["correct"]:
        _grant_correct_reward(
            game,
            progress,
        )
    else:
        game["reward"] = 0
        st.session_state.hearts = max(
            st.session_state.hearts - 1,
            0,
        )

def _next_question(game):
    if (
        game["round_index"] + 1
        >= len(game["questions"])
    ):
        game["complete"] = True
    else:
        game["round_index"] += 1
        _reset_round(game)

    st.rerun()


def _render_no_hearts():
    if st.session_state.hearts > 0:
        return False

    st.error(
        t("no_hearts_remaining")
    )
    enough_coins = (
        st.session_state.coins >= 20
    )

    if st.button(
        t("restore_heart"),
        disabled=not enough_coins,
    ):
        st.session_state.coins -= 20
        st.session_state.hearts = 1
        st.rerun()

    if not enough_coins:
        st.caption(
            t(
                "restore_heart_requirement"
            )
        )

    return True

def _render_setup(language):
    back_column, title_column = (
        st.columns([1, 5])
    )

    with back_column:
        if st.button(
            f'← {t("home")}'
        ):
            st.session_state.current_view = (
                "Home"
            )
            st.rerun()

    with title_column:
        st.title(
            f'🎧 {t("listening_title")}'
        )

    st.write(
        t("listening_v2_instructions")
    )

    selected_mode = st.selectbox(
        t("listening_choose_mode"),
        LISTENING_MODES,
        format_func=lambda mode: t(
            MODE_LABEL_KEYS[mode]
        ),
        key="listening_mode_choice",
    )

    st.info(
        t(
            f"listening_mode_"
            f"{selected_mode}_description"
        )
    )

    language_column, difficulty_column = (
        st.columns(2)
    )

    with language_column:
        st.metric(
            t("language"),
            language,
        )

    with difficulty_column:
        st.metric(
            t("difficulty"),
            st.session_state.get(
                "difficulty",
                "Balanced",
            ),
        )

    if st.button(
        t("listening_start"),
        type="primary",
        use_container_width=True,
    ):
        start_listening_session(
            language,
            selected_mode,
        )
        st.rerun()

def _render_question_input(
    game,
    question,
):
    key_suffix = (
        f'{game["id"]}_'
        f'{game["round_index"]}'
    )

    if question["kind"] == "dictation":
        st.markdown(
            f'### '
            f'{t("listening_type_heard")}'
        )
        return st.text_input(
            t("listening_your_answer"),
            disabled=game["answered"],
            key=(
                f"listening_text_"
                f"{key_suffix}"
            ),
        )

    if question["kind"] == (
        "missing_word"
    ):
        st.markdown(
            f'### '
            f'{t("listening_choose_missing_word")}'
        )
        st.info(
            question["masked_text"]
        )
        label = t(
            "listening_missing_word"
        )

    elif question["kind"] == "dialogue":
        st.markdown(
            f'### '
            f'{t("listening_choose_reply")}'
        )
        label = t(
            "listening_best_reply"
        )

    else:
        st.markdown(
            f'### '
            f'{t("what_did_you_hear")}'
        )
        label = t("choose_meaning")

    return st.radio(
        label,
        question["options"],
        index=None,
        disabled=game["answered"],
        key=(
            f"listening_choice_"
            f"{key_suffix}"
        ),
    )

def _render_feedback(
    game,
    question,
):
    result = game["result"]

    if result["correct"]:
        st.success(
            t(
                "listening_correct",
                reward=game["reward"],
            )
        )
    else:
        st.error(
            t("listening_incorrect")
        )

    if question["kind"] == "dictation":
        st.write(
            t(
                "listening_dictation_match",
                score=result["score"],
                required=result.get(
                    "required",
                    80,
                ),
            )
        )

    st.markdown(
        f'**{t("listening_your_answer")}:** '
        f'{game["selected"]}'
    )
    st.markdown(
        f'**{t("phrase_you_heard")}:** '
        f'{question["audio_text"]}'
    )
    st.markdown(
        f'**{t("meaning")}:** '
        f'{question["translation"]}'
    )

    if question["kind"] == "dialogue":
        st.markdown(
            f'**{t("listening_best_reply")}:** '
            f'{question["correct_answer"]}'
        )
        st.caption(
            question["response_meaning"]
        )

    elif question["kind"] == (
        "missing_word"
    ):
        st.markdown(
            f'**{t("listening_missing_word")}:** '
            f'{question["correct_answer"]}'
        )

    if question.get("transliteration"):
        st.caption(
            question["transliteration"]
        )

    if question.get("explanation"):
        st.info(
            question["explanation"]
        )

    if st.button(
        t("next_audio"),
        type="primary",
        use_container_width=True,
    ):
        _next_question(game)

def _render_complete(game):
    total = len(game["questions"])

    st.title(
        f'🎉 {t("listening_complete")}'
    )
    st.success(
        t(
            "listening_final_score",
            correct=game["correct"],
            total=total,
        )
    )
    st.info(
        t(
            "listening_coins_earned",
            coins=game["coins"],
        )
    )
    replay_column, mode_column = (
        st.columns(2)
    )

    with replay_column:
        if st.button(
            t("listening_play_again"),
            type="primary",
            use_container_width=True,
        ):
            start_listening_session(
                game["language"],
                game["mode"],
            )
            st.rerun()
with mode_column:
        if st.button(
            t("listening_choose_another_mode"),
            use_container_width=True,
        ):
            _clear_listening_session()
            st.rerun()
         
def render_listening():
    language = (
        st.session_state.active_language
    )
    game = st.session_state.get(
        "listening_game"
    )

    valid_game = (
        isinstance(game, dict)
        and game.get("language") == language
        and game.get("mode")
        in LISTENING_MODES
        and bool(game.get("questions"))
    )

    if not valid_game:
        _clear_listening_session()
        _render_setup(language)
        return

    if game["complete"]:
        _render_complete(game)
        return
        question = game["questions"][
        game["round_index"]
    ]
    progress = (
        st.session_state.language_progress[
            language
        ]
    )
    level = (
        progress.get("current_level")
        or "Beginner"
    )

    back_column, title_column = (
        st.columns([1, 5])
    )

    with back_column:
        if st.button(
            f'← {t("home")}'
        ):
            st.session_state.current_view = (
                "Home"
            )
            st.rerun()

    with title_column:
        st.title(
            f'🎧 {t("listening_title")}'
        )
        language_column, level_column, heart_column = (
        st.columns(3)
    )

    with language_column:
        st.metric(
            t("language"),
            language,
        )

    with level_column:
        st.metric(
            t("level"),
            level,
        )

    with heart_column:
        st.metric(
            t("hearts"),
            f'❤️ {st.session_state.hearts}/5',
        )

    st.info(
        t(
            MODE_LABEL_KEYS[
                game["mode"]
            ]
        )
    )
    current_round = (
        game["round_index"] + 1
    )
    total_rounds = len(
        game["questions"]
    )

    st.caption(
        t(
            "listening_round",
            current=current_round,
            total=total_rounds,
        )
    )
    st.progress(
        current_round / total_rounds
    )

    _render_audio(
        game,
        question["audio_text"],
        language,
    )

    answer = _render_question_input(
        game,
        question,
    )

    if game["answered"]:
        _render_feedback(
            game,
            question,
        )
        return

    no_hearts = _render_no_hearts()

    if st.button(
        t("check_answer"),
        type="primary",
        disabled=(
            not str(answer or "").strip()
            or no_hearts
        ),
        use_container_width=True,
    ):
        _check_answer(
            game,
            answer,
            progress,
        )
        st.rerun()