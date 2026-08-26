import random

import streamlit as st

from services.game_engine import get_exercises


LESSON_SECTIONS = [
    "1 · Learn",
    "2 · Break it down",
    "3 · Quick check",
]


def create_quiz_options(exercise):
    words = exercise["words"]

    reversed_sentence = " ".join(
        reversed(words)
    )

    rotated_sentence = " ".join(
        words[1:] + words[:1]
    )

    possible_options = [
        exercise["answer"],
        reversed_sentence,
        rotated_sentence,
    ]

    unique_options = []

    for option in possible_options:
        if option not in unique_options:
            unique_options.append(option)

    random_generator = random.Random(
        exercise["answer"]
    )

    random_generator.shuffle(unique_options)

    return unique_options


def start_lesson(
    language,
    lesson_number=0,
):
    exercises = get_exercises(language)

    exercise_index = (
        lesson_number % len(exercises)
    )

    exercise = exercises[exercise_index]

    st.session_state.lesson_game = {
        "language": language,
        "lesson_number": lesson_number,
        "exercise_index": exercise_index,
        "quiz_options": create_quiz_options(
            exercise
        ),
        "feedback": None,
        "completed": False,
        "reward": 0,
        "rewarded": False,
    }


def calculate_lesson_reward(difficulty):
    rewards = {
        "Relaxed": 8,
        "Balanced": 12,
        "Challenging": 16,
        "Custom": 20,
    }

    return rewards.get(difficulty, 12)


def render_lessons():
    back_column, title_column = st.columns([1, 5])

    with back_column:
        if st.button("← Home"):
            st.session_state.current_view = "Home"
            st.rerun()

    with title_column:
        st.title("📚 Lessons")

    language = st.session_state.active_language

    if (
        "lesson_game" not in st.session_state
        or st.session_state.lesson_game[
            "language"
        ] != language
    ):
        start_lesson(language)

    game = st.session_state.lesson_game
    exercises = get_exercises(language)

    exercise = exercises[
        game["exercise_index"]
    ]

    progress = st.session_state.language_progress[
        language
    ]

    level = progress["current_level"] or "Beginner"

    information_one, information_two, information_three = (
        st.columns(3)
    )

    with information_one:
        st.metric(
            "Language",
            language,
        )

    with information_two:
        st.metric(
            "Level",
            level,
        )

    with information_three:
        st.metric(
            "Coins",
            st.session_state.coins,
        )

    st.caption(
        f'Lesson {game["exercise_index"] + 1} '
        f'of {len(exercises)}'
    )

    section = st.radio(
        "Lesson steps",
        LESSON_SECTIONS,
        horizontal=True,
        key=(
            f'lesson_section_{language}_'
            f'{game["lesson_number"]}'
        ),
    )

    if section == "1 · Learn":
        st.markdown("### Real-life situation")

        st.info(exercise["situation"])

        st.markdown("### Meaning")

        st.write(exercise["translation"])

        st.markdown("### Target sentence")

        st.success(exercise["answer"])

        if exercise.get("transliteration"):
            if st.toggle(
                "Show transliteration",
                key=(
                    f'lesson_transliteration_'
                    f'{language}_'
                    f'{game["lesson_number"]}'
                ),
            ):
                st.info(
                    exercise["transliteration"]
                )

        st.markdown("### Helpful clue")

        st.write(exercise["clue"])

        st.caption(
            "When you are ready, select "
            "“2 · Break it down” above."
        )

    elif section == "2 · Break it down":
        st.markdown("### Sentence words")

        word_columns = st.columns(
            min(
                5,
                len(exercise["words"]),
            )
        )

        for index, word in enumerate(
            exercise["words"]
        ):
            column = word_columns[
                index % len(word_columns)
            ]

            with column:
                st.info(word)

        st.markdown("### How it works")

        st.write(exercise["explanation"])

        st.markdown("### Full sentence")

        st.success(exercise["answer"])

        st.caption(
            "Read the sentence aloud, then select "
            "“3 · Quick check” above."
        )

    else:
        st.markdown("### Choose the correct sentence")

        st.write(
            f'Which sentence correctly means: '
            f'**{exercise["translation"]}**'
        )

        selected_answer = st.radio(
            "Your answer",
            game["quiz_options"],
            index=None,
            disabled=game["completed"],
            key=(
                f'lesson_quiz_{language}_'
                f'{game["lesson_number"]}'
            ),
        )

        if st.button(
            "Check lesson answer",
            type="primary",
            disabled=(
                selected_answer is None
                or game["completed"]
            ),
        ):
            if selected_answer == exercise["answer"]:
                game["feedback"] = "correct"
                game["completed"] = True

                if not game["rewarded"]:
                    reward = calculate_lesson_reward(
                        st.session_state.difficulty
                    )

                    game["reward"] = reward
                    game["rewarded"] = True

                    st.session_state.coins += reward
                    progress["overall_xp"] += reward
                    progress["weekly_minutes"] += 2

                    progress["skill_levels"][
                        "Vocabulary"
                    ] += 1

                    progress["skill_levels"][
                        "Grammar"
                    ] += 1

            else:
                game["feedback"] = "incorrect"

            st.rerun()

        if game["feedback"] == "incorrect":
            st.error(
                "Not quite. Look carefully at the "
                "word order and try again."
            )

            st.info(
                f'Lesson help: '
                f'{exercise["explanation"]}'
            )

        if game["feedback"] == "correct":
            st.success(
                "Correct! You completed this lesson."
            )

            st.success(
                f'You earned {game["reward"]} coins.'
            )

            st.markdown(
                f'**Correct sentence:** '
                f'{exercise["answer"]}'
            )

            action_one, action_two = st.columns(2)

            with action_one:
                if st.button(
                    "🧩 Practise in Sentence Builder"
                ):
                    st.session_state.current_view = (
                        "Sentence Builder"
                    )
                    st.rerun()

            with action_two:
                if len(exercises) > 1:
                    if st.button(
                        "Next lesson →",
                        type="primary",
                    ):
                        start_lesson(
                            language,
                            game["lesson_number"] + 1,
                        )
                        st.rerun()
                else:
                    st.info(
                        "You completed the available "
                        "starter lesson for this language."
                    )