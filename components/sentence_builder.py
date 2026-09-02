import streamlit as st
from locales import t

from services.game_engine import (
    calculate_reward,
    check_answer,
    create_shuffled_tiles,
    get_exercises,
    get_hint,
)


PROMPT_TYPES = [
    "Situation",
    "Translation",
    "Picture",
    "Target-language clue",
]

SESSION_LENGTHS = [5, 10, 15]

def start_round(language, round_number=0):
    exercises = get_exercises(language)
    exercise_index = round_number % len(exercises)
    exercise = exercises[exercise_index]

    st.session_state.sentence_game = {
        "language": language,
        "round_number": round_number,
        "exercise_index": exercise_index,
        "tiles": create_shuffled_tiles(exercise),
        "selected_tile_ids": [],
        "hints": [],
        "answered": False,
        "correct": False,
        "reward": 0,
        "feedback": None,
    }

def start_session(language, total_rounds):
    st.session_state.sentence_session = {
        "language": language,
        "total_rounds": total_rounds,
        "completed_rounds": 0,
        "correct_answers": 0,
        "coins_earned": 0,
        "finished": False,
    }
    start_round(language)

def answer_from_tiles(game):
    tile_lookup = {
        tile["id"]: tile["word"]
        for tile in game["tiles"]
    }

    selected_words = [
        tile_lookup[tile_id]
        for tile_id in game["selected_tile_ids"]
    ]

    return " ".join(selected_words)


def render_sentence_builder():
    back_column, title_column = st.columns([1, 5])

    with back_column:
        if st.button(f"← {t('home')}"):
            st.session_state.current_view = "Home"
            st.rerun()

    with title_column:
        st.title(f"🧩 {t('sentence_builder')}")

    language = st.session_state.active_language

    session = st.session_state.get("sentence_session")

    if session and session["language"] != language:
        st.session_state.pop("sentence_session", None)
        st.session_state.pop("sentence_game", None)
        session = None

    if session is None:
        st.subheader(t("choose_session_length"))

        selected_length = st.radio(
            t("session_length"),
            SESSION_LENGTHS,
            horizontal=True,
            format_func=lambda count: t(
                "round_count",
                count=count,
            ),
            key=f"sentence_session_length_{language}",
        )

        if st.button(
            t("start_session"),
            type="primary",
        ):
            start_session(language, selected_length)
            st.rerun()

        return

    if session["finished"]:
        st.success(t("session_complete"))

        result_one, result_two = st.columns(2)

        with result_one:
            st.metric(
                t("correct_answers"),
                (
                    f'{session["correct_answers"]}/'
                    f'{session["total_rounds"]}'
                ),
            )

        with result_two:
            st.metric(
                t("session_coins"),
                session["coins_earned"],
            )

        if st.button(
            t("play_again"),
            type="primary",
        ):
            st.session_state.pop("sentence_session", None)
            st.session_state.pop("sentence_game", None)
            st.rerun()

        return

    if "sentence_game" not in st.session_state:
        start_round(language)

    game = st.session_state.sentence_game
    exercises = get_exercises(language)
    exercise = exercises[game["exercise_index"]]

    progress = st.session_state.language_progress[language]
    level = progress["current_level"] or "Beginner"

    completed_rounds = session["completed_rounds"]
    total_rounds = session["total_rounds"]

    st.progress(
        completed_rounds / total_rounds,
        text=t(
            "session_progress",
            completed=completed_rounds,
            total=total_rounds,
        ),
    )

    st.caption(
        f"{t('language')}: {language} · "
        f"{t('level')}: {level}"
    )

    round_column, score_column = st.columns(2)
    hearts_column, coins_column = st.columns(2)

    with round_column:
        st.metric(
            t("current_round"),
            f'{game["round_number"] + 1}/{total_rounds}',
        )

    with score_column:
        st.metric(
            t("correct_answers"),
            session["correct_answers"],
        )

    with hearts_column:
        st.metric(
            t("hearts"),
            f"{st.session_state.hearts}/5",
        )

    with coins_column:
        st.metric(
            t("session_coins"),
            session["coins_earned"],
        )

    st.caption(t("sentence_builder_instructions"))

    prompt_types = st.multiselect(
    t("choose_prompt_types"),
    PROMPT_TYPES,
    default=[
        "Situation",
        "Translation",
    ],
    format_func=lambda prompt_type: t(
        f"prompt_type_{prompt_type.lower().replace(' ', '_').replace('-', '_')}"
    ),
    key=f"prompt_types_{language}",
)

    if not prompt_types:
        st.warning(t("select_prompt_type_warning"))

    if "Situation" in prompt_types:
        st.info(
    t(
        "real_life_situation",
        situation=exercise["situation"],
    )
)

    if "Translation" in prompt_types:
        st.markdown(
            f"**{t('meaning')}:** {exercise['translation']}")

    if "Picture" in prompt_types:
        st.markdown(
            f"## {exercise['picture']}"
        )

    if "Target-language clue" in prompt_types:
        st.markdown(
    f"**{t('clue')}:** {exercise['clue']}"
)

    if exercise.get("transliteration"):
        show_transliteration = st.toggle(
            t("show_transliteration"),
            key=f"show_transliteration_{language}",
        )

        if show_transliteration:
            st.caption(
                exercise["transliteration"]
            )

    input_method = st.radio(
    t("answer_method"),
    [
        "Word tiles",
        "Typing",
    ],
    format_func=lambda method: t(
        f"answer_method_{method.lower().replace(' ', '_')}"
    ),
    horizontal=True,
    key=f"sentence_method_{language}",
)

    candidate_answer = ""

    if input_method == "Word tiles":
        candidate_answer = answer_from_tiles(game)

        st.markdown(f"#### {t('your_sentence')}")

        if candidate_answer:
            st.success(candidate_answer)
        else:
            st.caption(t("select_words_in_order"))

        selected_ids = set(game["selected_tile_ids"])

        available_tiles = [
            tile
            for tile in game["tiles"]
            if tile["id"] not in selected_ids
        ]

        if available_tiles:
            tile_columns = st.columns(
                min(4, len(available_tiles))
            )

            for position, tile in enumerate(available_tiles):
                column = tile_columns[
                    position % len(tile_columns)
                ]

                with column:
                    if st.button(
                        tile["word"],
                        key=(
                            f"tile_{language}_"
                            f"{game['round_number']}_"
                            f"{tile['id']}"
                        ),
                        disabled=game["answered"],
                    ):
                        game["selected_tile_ids"].append(
                            tile["id"]
                        )
                        st.rerun()

        undo_column, clear_column = st.columns(2)

        with undo_column:
            if st.button(
                t("undo_last_word"),
                disabled=(
                    not game["selected_tile_ids"]
                    or game["answered"]
                ),
            ):
                game["selected_tile_ids"].pop()
                st.rerun()

        with clear_column:
            if st.button(
                t("clear_sentence"),
                disabled=(
                    not game["selected_tile_ids"]
                    or game["answered"]
                ),
            ):
                game["selected_tile_ids"] = []
                st.rerun()

    else:
        candidate_answer = st.text_input(
            t("type_your_sentence"),
            key=(
                f"typed_answer_{language}_"
                f"{game['round_number']}"
            ),
            disabled=game["answered"],
        )

    hints_left = 3 - len(game["hints"])

    if st.button(
        t("use_hint", count=hints_left),
        disabled=(
            hints_left == 0
            or game["answered"]
        ),
    ):
        hint_number = len(game["hints"]) + 1

        game["hints"].append(
            get_hint(
                exercise,
                hint_number,
            )
        )

    for hint in game["hints"]:
        st.warning(t("hint_message", hint=hint))

    no_hearts = st.session_state.hearts <= 0

    if no_hearts:
        st.error(
            t("no_hearts_remaining")
        )

        can_restore = st.session_state.coins >= 20

        if st.button(
            t("restore_heart"),
            disabled=not can_restore,
        ):
            st.session_state.coins -= 20
            st.session_state.hearts = 1
            st.rerun()

        if not can_restore:
            st.caption(
                t("restore_heart_requirement")
            )

    answer_ready = bool(candidate_answer.strip())

    if st.button(
        t("check_answer"),
        type="primary",
        disabled=(
            not answer_ready
            or not prompt_types
            or game["answered"]
            or no_hearts
        ),
    ):
        is_correct = check_answer(
            candidate_answer,
            exercise,
            level,
        )

        if is_correct:
            used_hint = bool(game["hints"])

            reward = calculate_reward(
                st.session_state.difficulty,
                used_hint,
            )

            session["completed_rounds"] += 1
            session["correct_answers"] += 1
            session["coins_earned"] += reward

            game["answered"] = True
            game["correct"] = True
            game["reward"] = reward
            game["feedback"] = "correct"

            st.session_state.coins += reward

            progress["overall_xp"] += reward
            progress["weekly_minutes"] += 1
            progress["skill_levels"][
                "Sentence Builder"
            ] += 1
        else:
            st.session_state.hearts = max(
                st.session_state.hearts - 1,
                0,
            )

            game["feedback"] = "incorrect"

        st.rerun()
    if game["feedback"] == "incorrect":
        st.error(t("incorrect_answer"))

        st.info(
    t(
        "grammar_help",
        explanation=exercise["explanation"],
    )
)

    if game["feedback"] == "correct":
        st.success(
    t(
        "correct_reward",
        reward=game["reward"],
    )
)

        st.info(
    t(
        "why_it_works",
        explanation=exercise["explanation"],
    )
)

        st.markdown(
            f"**{t('correct_sentence')}:** {exercise['answer']}"
        )

        bonus_column, next_column = st.columns(2)

        with bonus_column:
            if st.button(
                f"🎙️ {t('pronunciation_bonus')}"
            ):
                st.info(t("pronunciation_bonus_info"))

        with next_column:
            session_is_complete = (
                session["completed_rounds"]
                >= session["total_rounds"]
            )

            next_label = (
                t("finish_session")
                if session_is_complete
                else f"{t('next_challenge')} →"
            )

            if st.button(
                next_label,
                type="primary",
            ):
                if session_is_complete:
                    session["finished"] = True
                    st.session_state.pop("sentence_game", None)
                else:
                    start_round(
                        language,
                        game["round_number"] + 1,
                    )

                st.rerun()