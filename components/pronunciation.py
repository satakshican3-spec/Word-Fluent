import streamlit as st

from services.game_engine import get_exercises
from services.pronunciation_engine import (
    evaluate_pronunciation,
    transcribe_audio,
)


def start_pronunciation_round(
    language,
    round_number=0,
):
    exercises = get_exercises(language)
    exercise_index = round_number % len(exercises)

    st.session_state.pronunciation_game = {
        "language": language,
        "round_number": round_number,
        "exercise_index": exercise_index,
        "attempt_number": 0,
        "result": None,
        "reward_granted": False,
    }


def calculate_pronunciation_reward(
    score,
    difficulty,
):
    rewards = {
        "Relaxed": 5,
        "Balanced": 8,
        "Challenging": 12,
        "Custom": 15,
    }

    reward = rewards.get(difficulty, 8)

    if score >= 90:
        reward += 3

    return reward


def render_pronunciation():
    back_column, title_column = st.columns([1, 5])

    with back_column:
        if st.button("← Home"):
            st.session_state.current_view = "Home"
            st.rerun()

    with title_column:
        st.title("🎙️ Pronunciation")

    language = st.session_state.active_language

    if (
        "pronunciation_game" not in st.session_state
        or st.session_state.pronunciation_game[
            "language"
        ] != language
    ):
        start_pronunciation_round(language)

    game = st.session_state.pronunciation_game
    exercises = get_exercises(language)
    exercise = exercises[game["exercise_index"]]

    progress = st.session_state.language_progress[
        language
    ]

    level = progress["current_level"] or "Beginner"

    information_one, information_two, information_three = (
        st.columns(3)
    )

    with information_one:
        st.metric("Language", language)

    with information_two:
        st.metric("Level", level)

    with information_three:
        st.metric(
            "Coins",
            st.session_state.coins,
        )

    st.markdown("### Say this phrase")

    st.markdown(
        f"## {exercise['answer']}"
    )

    st.caption(
        f"Meaning: {exercise['translation']}"
    )

    if exercise.get("transliteration"):
        if st.toggle(
            "Show pronunciation guide",
            key=(
                f"pronunciation_guide_{language}_"
                f"{game['round_number']}"
            ),
        ):
            st.info(exercise["transliteration"])

    st.info(
        f"Language help: {exercise['explanation']}"
    )

    st.caption(
        "Speak naturally in a quiet place. This prototype "
        "checks whether the intended words were recognized; "
        "it does not judge your accent."
    )

    audio_file = st.audio_input(
        "Record yourself saying the phrase",
        sample_rate=16000,
        key=(
            f"pronunciation_audio_{language}_"
            f"{game['round_number']}_"
            f"{game['attempt_number']}"
        ),
    )

    if audio_file is None:
        st.caption(
            "Press the microphone, say the phrase, "
            "then stop the recording."
        )
    else:
        if st.button(
            "Check my pronunciation",
            type="primary",
            disabled=game["result"] is not None,
        ):
            with st.spinner(
                "Listening to your recording..."
            ):
                transcription = transcribe_audio(
                    audio_file,
                    language,
                )

            if not transcription["success"]:
                game["result"] = {
                    "success": False,
                    "error": transcription["error"],
                }

            else:
                accepted_phrases = [
                    exercise["answer"],
                    *exercise.get(
                        "accepted_answers",
                        [],
                    ),
                ]

                evaluation = evaluate_pronunciation(
                    transcription["transcript"],
                    accepted_phrases,
                    level,
                )

                reward = 0

                if (
                    evaluation["passed"]
                    and not game["reward_granted"]
                ):
                    reward = (
                        calculate_pronunciation_reward(
                            evaluation["score"],
                            st.session_state.difficulty,
                        )
                    )

                    st.session_state.coins += reward
                    progress["overall_xp"] += reward
                    progress["weekly_minutes"] += 1

                    progress["skill_levels"][
                        "Pronunciation"
                    ] += 1

                    game["reward_granted"] = True

                game["result"] = {
                    "success": True,
                    "transcript": transcription[
                        "transcript"
                    ],
                    "reward": reward,
                    **evaluation,
                }

            st.rerun()

    result = game["result"]

    if result is not None:
        if not result["success"]:
            st.error(result["error"])

            if st.button("Record again"):
                game["attempt_number"] += 1
                game["result"] = None
                st.rerun()

        else:
            st.markdown("### Your feedback")

            st.write(
                f'WordFluent heard: **'
                f'{result["transcript"]}**'
            )

            st.progress(
                result["score"] / 100
            )

            st.caption(
                f'Speech match: {result["score"]}% '
                f'· Required for {level}: '
                f'{result["required_score"]}%'
            )

            if result["passed"]:
                st.success(
                    "Well done! The intended phrase "
                    "was recognized clearly."
                )

                if result["reward"] > 0:
                    st.success(
                        f'You earned '
                        f'{result["reward"]} coins!'
                    )

                if st.button(
                    "Next pronunciation phrase →",
                    type="primary",
                ):
                    start_pronunciation_round(
                        language,
                        game["round_number"] + 1,
                    )
                    st.rerun()

            else:
                st.warning(
                    "You are close. Listen to each word "
                    "and try saying the phrase again."
                )

                st.markdown(
                    f'**Target phrase:** '
                    f'{result["closest_phrase"]}'
                )

                if st.button("Record again"):
                    game["attempt_number"] += 1
                    game["result"] = None
                    st.rerun()