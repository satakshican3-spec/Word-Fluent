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

    if (
        "sentence_game" not in st.session_state
        or st.session_state.sentence_game["language"]
        != language
    ):
        start_round(language)

    game = st.session_state.sentence_game
    exercises = get_exercises(language)
    exercise = exercises[game["exercise_index"]]

    progress = st.session_state.language_progress[language]
    level = progress["current_level"] or "Beginner"

    information_one, information_two, information_three = (
        st.columns(3)
    )

    with information_one:
        st.metric(t("language"), language)

    with information_two:
        st.metric(t("level"), level)

    with information_three:
        st.metric(
            t("hearts"),
            f"{st.session_state.hearts}/5",
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
            "Restore one heart for 20 coins",
            disabled=not can_restore,
        ):
            st.session_state.coins -= 20
            st.session_state.hearts = 1
            st.rerun()

        if not can_restore:
            st.caption(
                "You need at least 20 coins to restore a heart."
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
            if st.button(
                f"{t('next_challenge')} →",
                type="primary",
            ):
                start_round(
                    language,
                    game["round_number"] + 1,
                )
                st.rerun()