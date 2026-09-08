import random
from uuid import uuid4

import streamlit as st

from locales import t
from services.game_engine import (
    calculate_reward,
    get_exercises,
)
from services.pronunciation_engine import (
    generate_reference_audio,
)


@st.cache_data(show_spinner=False, ttl=86400)
def get_listening_audio(phrase, language, slow):
    return generate_reference_audio(
        phrase,
        language,
        slow,
    )


def _question_count(exercises):
    requested_minutes = int(
        st.session_state.get(
            "session_length",
            5,
        )
    )

    return min(
        len(exercises),
        max(5, requested_minutes // 2),
    )


def _choice_count():
    if st.session_state.get("difficulty") == "Relaxed":
        return 3

    return 4


def _build_questions(exercises):
    question_total = _question_count(exercises)
    choice_total = _choice_count()
    chosen_indices = random.sample(
        range(len(exercises)),
        question_total,
    )
    questions = []

    for exercise_index in chosen_indices:
        correct_meaning = str(
            exercises[exercise_index]["translation"]
        ).strip()
        other_meanings = []

        for other_index, exercise in enumerate(exercises):
            meaning = str(
                exercise.get("translation", "")
            ).strip()

            if (
                other_index != exercise_index
                and meaning
                and meaning.casefold()
                != correct_meaning.casefold()
                and meaning not in other_meanings
            ):
                other_meanings.append(meaning)

        wrong_choices = random.sample(
            other_meanings,
            min(
                choice_total - 1,
                len(other_meanings),
            ),
        )
        options = [
            correct_meaning,
            *wrong_choices,
        ]
        random.shuffle(options)

        questions.append(
            {
                "exercise_index": exercise_index,
                "options": options,
            }
        )

    return questions


def start_listening_session(language):
    exercises = get_exercises(language)

    st.session_state.listening_game = {
        "id": uuid4().hex[:10],
        "language": language,
        "questions": _build_questions(exercises),
        "round_index": 0,
        "correct": 0,
        "coins": 0,
        "answered": False,
        "selected": None,
        "was_correct": False,
        "reward": 0,
        "audio": b"",
        "audio_error": None,
        "audio_speed": None,
        "complete": False,
    }


def _reset_round_audio(game):
    game["audio"] = b""
    game["audio_error"] = None
    game["audio_speed"] = None


def _play_audio(game, phrase, language, slow):
    with st.spinner(t("preparing_audio")):
        result = get_listening_audio(
            phrase,
            language,
            slow,
        )

    game["audio"] = result["audio"]
    game["audio_error"] = result["error"]
    game["audio_speed"] = (
        t("listen_slow")
        if slow
        else t("listen_normal")
    )


def _render_audio(game, phrase, language):
    normal_column, slow_column = st.columns(2)

    with normal_column:
        if st.button(
            f'🔊 {t("listen_normal")}',
            use_container_width=True,
        ):
            _play_audio(
                game,
                phrase,
                language,
                False,
            )

    with slow_column:
        if st.button(
            f'🐢 {t("listen_slow")}',
            use_container_width=True,
        ):
            _play_audio(
                game,
                phrase,
                language,
                True,
            )

    if game["audio"]:
        st.caption(game["audio_speed"])
        st.audio(
            game["audio"],
            format="audio/mp3",
        )
    elif game["audio_error"]:
        st.warning(game["audio_error"])


def _grant_correct_reward(game, progress):
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
        skills.get("Listening", 0) + 1
    )


def _check_answer(
    game,
    selected,
    correct_meaning,
    progress,
):
    game["answered"] = True
    game["selected"] = selected
    game["was_correct"] = (
        selected == correct_meaning
    )

    if game["was_correct"]:
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
    if game["round_index"] + 1 >= len(
        game["questions"]
    ):
        game["complete"] = True
    else:
        game["round_index"] += 1
        game["answered"] = False
        game["selected"] = None
        game["was_correct"] = False
        game["reward"] = 0
        _reset_round_audio(game)

    st.rerun()


def _render_feedback(game, exercise):
    if game["was_correct"]:
        st.success(
            t(
                "listening_correct",
                reward=game["reward"],
            )
        )
    else:
        st.error(t("listening_incorrect"))

    st.markdown(
        f'**{t("phrase_you_heard")}:** '
        f'{exercise["answer"]}'
    )
    st.markdown(
        f'**{t("meaning")}:** '
        f'{exercise["translation"]}'
    )

    if exercise.get("transliteration"):
        st.caption(exercise["transliteration"])

    if exercise.get("explanation"):
        st.info(exercise["explanation"])

    if st.button(
        t("next_audio"),
        type="primary",
        use_container_width=True,
    ):
        _next_question(game)


def _render_no_hearts():
    if st.session_state.hearts > 0:
        return False

    st.error(t("no_hearts_remaining"))
    enough_coins = st.session_state.coins >= 20

    if st.button(
        t("restore_heart"),
        disabled=not enough_coins,
    ):
        st.session_state.coins -= 20
        st.session_state.hearts = 1
        st.rerun()

    if not enough_coins:
        st.caption(
            t("restore_heart_requirement")
        )

    return True


def _render_complete(game, language):
    st.title(f'🎧 {t("session_complete")}')
    score_column, coin_column = st.columns(2)

    with score_column:
        st.metric(
            t("listening_score"),
            t(
                "listening_questions_correct",
                correct=game["correct"],
                total=len(game["questions"]),
            ),
        )

    with coin_column:
        st.metric(
            t("coins"),
            f'🪙 {game["coins"]}',
        )

    replay_column, home_column = st.columns(2)

    with replay_column:
        if st.button(
            t("play_again"),
            type="primary",
            use_container_width=True,
        ):
            start_listening_session(language)
            st.rerun()

    with home_column:
        if st.button(
            t("finish_session"),
            use_container_width=True,
        ):
            st.session_state.current_view = "Home"
            st.rerun()


def render_listening():
    language = st.session_state.active_language

    if (
        "listening_game" not in st.session_state
        or st.session_state.listening_game[
            "language"
        ]
        != language
    ):
        start_listening_session(language)

    game = st.session_state.listening_game

    if game["complete"]:
        _render_complete(game, language)
        return

    exercises = get_exercises(language)
    question = game["questions"][
        game["round_index"]
    ]
    exercise = exercises[
        question["exercise_index"]
    ]
    progress = st.session_state.language_progress[
        language
    ]
    level = progress.get("current_level") or "Beginner"

    back_column, title_column = st.columns([1, 5])

    with back_column:
        if st.button(f'← {t("home")}'):
            st.session_state.current_view = "Home"
            st.rerun()

    with title_column:
        st.title(f'🎧 {t("listening_title")}')

    st.write(t("listening_instructions"))

    language_column, level_column, heart_column = st.columns(3)

    with language_column:
        st.metric(t("language"), language)

    with level_column:
        st.metric(t("level"), level)

    with heart_column:
        st.metric(
            t("hearts"),
            f'❤️ {st.session_state.hearts}/5',
        )

    current_round = game["round_index"] + 1
    total_rounds = len(game["questions"])

    st.caption(
        t(
            "listening_round",
            current=current_round,
            total=total_rounds,
        )
    )
    st.progress(
        (current_round - 1) / total_rounds
    )

    st.markdown(
        f'### {t("what_did_you_hear")}'
    )

    _render_audio(
        game,
        exercise["answer"],
        language,
    )

    selected = st.radio(
        t("choose_meaning"),
        question["options"],
        index=None,
        disabled=game["answered"],
        key=(
            f'listening_choice_{game["id"]}_'
            f'{game["round_index"]}'
        ),
    )

    no_hearts = _render_no_hearts()

    if st.button(
        t("check_answer"),
        type="primary",
        disabled=(
            selected is None
            or game["answered"]
            or no_hearts
        ),
        use_container_width=True,
    ):
        _check_answer(
            game,
            selected,
            exercise["translation"],
            progress,
        )
        st.rerun()

    if game["answered"]:
        _render_feedback(
            game,
            exercise,
        )