import streamlit as st

from services.game_engine import get_exercises
from services.pronunciation_engine import (
    evaluate_pronunciation,
    generate_reference_audio,
    transcribe_audio,
)


@st.cache_data(show_spinner=False, ttl=86400)
def get_reference_audio(phrase, language, slow):
    return generate_reference_audio(phrase, language, slow)


def start_pronunciation_round(language, round_number=0):
    exercises = get_exercises(language)
    exercise_index = round_number % len(exercises)
    st.session_state.pronunciation_game = {
        "language": language,
        "round_number": round_number,
        "exercise_index": exercise_index,
        "attempt_number": 0,
        "result": None,
        "reward_granted": False,
        "best_score": 0,
        "previous_score": None,
        "reference_audio": b"",
        "reference_error": None,
        "reference_speed": None,
    }


def calculate_pronunciation_reward(score, difficulty):
    rewards = {
        "Relaxed": 5,
        "Balanced": 8,
        "Challenging": 12,
        "Custom": 15,
    }
    reward = rewards.get(difficulty, 8)
    return reward + 3 if score >= 90 else reward


def _prepare_existing_game(game):
    game.setdefault("best_score", 0)
    game.setdefault("previous_score", None)
    game.setdefault("reference_audio", b"")
    game.setdefault("reference_error", None)
    game.setdefault("reference_speed", None)


def _retry_current_phrase(game):
    game["attempt_number"] += 1
    game["result"] = None
    st.rerun()


def _render_reference_audio(game, exercise, language):
    st.markdown("#### 1. Listen")
    slow = st.toggle(
        "Slow reference",
        key=f"slow_reference_{language}_{game['round_number']}",
    )

    if st.button(
        "🔊 Play reference",
        key=f"play_reference_{language}_{game['round_number']}",
    ):
        with st.spinner("Preparing the reference voice..."):
            reference = get_reference_audio(exercise["answer"], language, slow)

        game["reference_audio"] = reference["audio"]
        game["reference_error"] = reference["error"]
        game["reference_speed"] = "Slow" if slow else "Normal"

    if game["reference_audio"]:
        st.caption(f'{game["reference_speed"]} reference')
        st.audio(game["reference_audio"], format="audio/mp3")
    elif game["reference_error"]:
        st.warning(game["reference_error"])


def _render_word_feedback(result):
    heading = (
        "Character-by-character check"
        if result["feedback_unit"] == "character"
        else "Word-by-word check"
    )
    st.markdown(f"#### {heading}")
    st.caption("✅ recognized · 🟠 different · ❌ not recognized")

    pieces = []
    for item in result["word_feedback"]:
        expected = item["expected"]
        if item["status"] == "matched":
            pieces.append(f"✅ **{expected}**")
        elif item["status"] == "different":
            pieces.append(f'🟠 **{expected}** _(heard: {item["heard"]})_')
        else:
            pieces.append(f"❌ **{expected}**")

    if pieces:
        st.markdown(" &nbsp; ".join(pieces))
    if result["extra_words"]:
        st.caption("Extra parts heard: " + ", ".join(result["extra_words"]))

    st.info(f'💡 Coach tip: {result["coaching_tip"]}')


def _render_success_actions(game, language, reward):
    st.success("Well done! The intended phrase was recognized clearly.")
    if reward > 0:
        st.success(f"You earned {reward} coins!")

    retry_column, next_column = st.columns(2)
    with retry_column:
        if st.button("Practise again"):
            _retry_current_phrase(game)
    with next_column:
        if st.button("Next phrase →", type="primary"):
            start_pronunciation_round(language, game["round_number"] + 1)
            st.rerun()


def _render_result(game, language, level):
    result = game["result"]
    if result is None:
        return

    st.markdown("#### 3. Feedback")
    if not result["success"]:
        st.error(result["error"])
        if st.button("Record again"):
            _retry_current_phrase(game)
        return

    st.write(f'WordFluent heard: **{result["transcript"]}**')
    score_column, coverage_column, best_column = st.columns(3)

    with score_column:
        improvement = result["improvement"]
        st.metric(
            "Phrase match",
            f'{result["score"]}%',
            delta=f"{improvement:+d}%" if improvement is not None else None,
        )
    with coverage_column:
        st.metric("Parts recognized", f'{result["word_coverage"]}%')
    with best_column:
        st.metric("Best this phrase", f'{game["best_score"]}%')

    st.progress(max(0.0, min(result["score"] / 100, 1.0)))
    st.caption(
        f'Attempt {result["attempt"]} · Required for {level}: '
        f'{result["required_score"]}% phrase match and '
        f'{result["required_coverage"]}% parts recognized'
    )
    _render_word_feedback(result)

    if result["passed"]:
        _render_success_actions(game, language, result["reward"])
    else:
        st.warning(
            "You are close. Use the highlighted parts and the coach tip, "
            "then try again."
        )
        st.markdown(f'**Target phrase:** {result["closest_phrase"]}')
        if st.button("Record again"):
            _retry_current_phrase(game)


def render_pronunciation():
    back_column, title_column = st.columns([1, 5])
    with back_column:
        if st.button("← Home"):
            st.session_state.current_view = "Home"
            st.rerun()
    with title_column:
        st.title("🎙️ Pronunciation Coach")

    language = st.session_state.active_language
    if (
        "pronunciation_game" not in st.session_state
        or st.session_state.pronunciation_game["language"] != language
    ):
        start_pronunciation_round(language)

    game = st.session_state.pronunciation_game
    _prepare_existing_game(game)
    exercises = get_exercises(language)
    exercise = exercises[game["exercise_index"]]
    progress = st.session_state.language_progress[language]
    level = progress["current_level"] or "Beginner"

    information_one, information_two, information_three = st.columns(3)
    with information_one:
        st.metric("Language", language)
    with information_two:
        st.metric("Level", level)
    with information_three:
        st.metric("Coins", st.session_state.coins)

    st.markdown("### Say this phrase")
    st.markdown(f"## {exercise['answer']}")
    st.caption(f"Meaning: {exercise['translation']}")

    if exercise.get("transliteration"):
        guide_key = f"pronunciation_guide_{language}_{game['round_number']}"
        if st.toggle("Show pronunciation guide", key=guide_key):
            st.info(exercise["transliteration"])

    st.info(f"Language help: {exercise['explanation']}")
    _render_reference_audio(game, exercise, language)

    st.markdown("#### 2. Record")
    st.caption(
        "Speak naturally in a quiet place. This coach checks which intended "
        "words were recognized; it does not judge your accent or individual sounds."
    )

    audio_file = st.audio_input(
        "Record yourself saying the phrase",
        sample_rate=16000,
        key=(
            f"pronunciation_audio_{language}_{game['round_number']}_"
            f"{game['attempt_number']}"
        ),
    )
    st.caption(
        "Your recording is sent to Google Speech Recognition for transcription. "
        "This screen does not save it."
    )

    if audio_file is None:
        st.caption("Press the microphone, say the phrase, then stop the recording.")
    elif st.button(
        "Check my pronunciation",
        type="primary",
        disabled=game["result"] is not None,
    ):
        with st.spinner("Listening to your recording..."):
            transcription = transcribe_audio(audio_file, language)

        if not transcription["success"]:
            game["result"] = {
                "success": False,
                "error": transcription["error"],
            }
        else:
            accepted_phrases = [
                exercise["answer"],
                *exercise.get("accepted_answers", []),
            ]
            evaluation = evaluate_pronunciation(
                transcription["transcript"],
                accepted_phrases,
                level,
                language,
            )

            previous_score = game["previous_score"]
            improvement = (
                evaluation["score"] - previous_score
                if previous_score is not None
                else None
            )
            game["previous_score"] = evaluation["score"]
            game["best_score"] = max(game["best_score"], evaluation["score"])

            reward = 0
            if evaluation["passed"] and not game["reward_granted"]:
                reward = calculate_pronunciation_reward(
                    evaluation["score"],
                    st.session_state.difficulty,
                )
                st.session_state.coins += reward
                progress["overall_xp"] += reward
                progress["weekly_minutes"] += 1
                progress["skill_levels"]["Pronunciation"] += 1
                game["reward_granted"] = True

            game["result"] = {
                "success": True,
                "transcript": transcription["transcript"],
                "reward": reward,
                "improvement": improvement,
                "attempt": game["attempt_number"] + 1,
                **evaluation,
            }

        st.rerun()

    _render_result(game, language, level)