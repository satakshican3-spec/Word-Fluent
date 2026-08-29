import random
import re
import unicodedata

import streamlit as st

from language_packs.english import get_english_course

from language_packs.bengali import get_bengali_course


def _normalize(value):
    text = unicodedata.normalize("NFKC", str(value))
    text = text.casefold().strip().replace("’", "'")
    text = re.sub(
        r"[^\w\s']",
        "",
        text,
        flags=re.UNICODE,
    )
    return " ".join(text.split())


def _accepted_answers(exercise):
    return [
        exercise["answer"],
        *exercise.get("accepted_answers", []),
    ]


def _is_correct(candidate, exercise):
    normalized_candidate = _normalize(candidate)

    return any(
        normalized_candidate == _normalize(answer)
        for answer in _accepted_answers(exercise)
    )


def _all_lessons(course):
    lessons = []

    for unit_index, unit in enumerate(course["units"]):
        for lesson_index, lesson in enumerate(
            unit["lessons"]
        ):
            lessons.append(
                {
                    "unit_index": unit_index,
                    "lesson_index": lesson_index,
                    "unit": unit,
                    "lesson": lesson,
                }
            )

    return lessons


def _find_lesson(course, lesson_id):
    for item in _all_lessons(course):
        if item["lesson"]["id"] == lesson_id:
            return item["lesson"]

    return None


def _course_progress(language):
    if "course_progress" not in st.session_state:
        st.session_state.course_progress = {}

    if language not in st.session_state.course_progress:
        st.session_state.course_progress[language] = {
            "completed_lessons": [],
            "lesson_scores": {},
        }

    return st.session_state.course_progress[language]


def _lesson_is_unlocked(
    flat_lessons,
    position,
    completed_ids,
):
    if position == 0:
        return True

    previous_id = flat_lessons[
        position - 1
    ]["lesson"]["id"]

    return previous_id in completed_ids


def _start_lesson(course, lesson_id):
    lesson = _find_lesson(course, lesson_id)

    if lesson is None:
        return

    st.session_state.course_lesson_run = {
        "language": course["language"],
        "lesson_id": lesson_id,
        "stage": "vocabulary",
        "exercise_index": 0,
        "correct_answers": 0,
        "attempted_answers": 0,
        "answered": False,
        "was_correct": False,
        "rewarded": False,
    }


def _return_to_path():
    st.session_state.pop(
        "course_lesson_run",
        None,
    )
    st.rerun()


def _render_header(course, progress):
    back_column, title_column = st.columns([1, 5])

    with back_column:
        if st.button(
            "← Home",
            key="course_home",
        ):
            st.session_state.current_view = "Home"
            st.session_state.pop(
                "course_lesson_run",
                None,
            )
            st.rerun()

    with title_column:
        st.title("📚 English Learning Path")

    flat_lessons = _all_lessons(course)
    completed_count = len(
        progress["completed_lessons"]
    )
    total_lessons = len(flat_lessons)

    st.write(course["description"])

    metric_one, metric_two, metric_three = (
        st.columns(3)
    )

    with metric_one:
        st.metric(
            "Level",
            course["level"],
        )

    with metric_two:
        st.metric(
            "Lessons completed",
            f"{completed_count}/{total_lessons}",
        )

    with metric_three:
        st.metric(
            "Coins",
            st.session_state.coins,
        )

    completion = completed_count / max(
        total_lessons,
        1,
    )
    st.progress(completion)

    if completed_count == total_lessons:
        st.success(
            "You completed the English Beginner "
            "learning path!"
        )


def _render_path(course):
    progress = _course_progress(
        course["language"]
    )

    completed_ids = set(
        progress["completed_lessons"]
    )

    flat_lessons = _all_lessons(course)

    _render_header(course, progress)

    st.markdown("## Course units")

    flat_position = 0

    for unit_number, unit in enumerate(
        course["units"],
        start=1,
    ):
        unit_completed = sum(
            lesson["id"] in completed_ids
            for lesson in unit["lessons"]
        )

        unit_label = (
            f'{unit["icon"]} Unit {unit_number}: '
            f'{unit["title"]} '
            f'({unit_completed}/'
            f'{len(unit["lessons"])})'
        )

        first_incomplete_unit = any(
            lesson["id"] not in completed_ids
            for lesson in unit["lessons"]
        )

        with st.expander(
            unit_label,
            expanded=(
                unit_number == 1
                or first_incomplete_unit
            ),
        ):
            st.write(unit["description"])

            for lesson in unit["lessons"]:
                lesson_id = lesson["id"]

                completed = (
                    lesson_id in completed_ids
                )

                unlocked = _lesson_is_unlocked(
                    flat_lessons,
                    flat_position,
                    completed_ids,
                )

                with st.container(border=True):
                    (
                        details_column,
                        button_column,
                    ) = st.columns([4, 1])

                    with details_column:
                        if completed:
                            status = "✅"
                        elif unlocked:
                            status = "▶️"
                        else:
                            status = "🔒"

                        st.markdown(
                            f'### {status} '
                            f'{lesson["icon"]} '
                            f'{lesson["title"]}'
                        )

                        st.write(
                            lesson["objective"]
                        )

                        st.caption(
                            f'{lesson["estimated_minutes"]} '
                            f'min · '
                            f'{lesson["xp_reward"]} XP · '
                            f'{lesson["coin_reward"]} coins'
                        )

                    with button_column:
                        if completed:
                            button_label = "Review"
                        else:
                            button_label = "Start"

                        if st.button(
                            button_label,
                            key=(
                                f"start_course_"
                                f"{lesson_id}"
                            ),
                            type=(
                                "primary"
                                if unlocked
                                and not completed
                                else "secondary"
                            ),
                            disabled=not unlocked,
                        ):
                            _start_lesson(
                                course,
                                lesson_id,
                            )
                            st.rerun()

                flat_position += 1


def _lesson_title(lesson):
    if st.button(
        "← Learning path",
        key="back_to_course_path",
    ):
        _return_to_path()

    st.title(
        f'{lesson["icon"]} '
        f'{lesson["title"]}'
    )

    st.caption(lesson["objective"])


def _render_vocabulary(lesson, run):
    _lesson_title(lesson)

    st.markdown("## 1. Learn the words")

    st.write(
        "Read each word and its example "
        "before continuing."
    )

    for item in lesson["vocabulary"]:
        with st.container(border=True):
            st.markdown(
                f'### {item["term"]}'
            )

            st.write(item["meaning"])

            st.caption(
                f'Example: {item["example"]}'
            )

    if st.button(
        "Continue to grammar →",
        type="primary",
        key=f'vocabulary_done_{lesson["id"]}',
    ):
        run["stage"] = "grammar"
        st.rerun()


def _render_grammar(lesson, run):
    _lesson_title(lesson)

    st.markdown(
        "## 2. Understand the pattern"
    )

    with st.container(border=True):
        st.markdown(
            f'### '
            f'{lesson["grammar"]["title"]}'
        )

        st.write(
            lesson["grammar"]["summary"]
        )

    st.info(
        "You will now answer three short "
        "questions. You need at least two "
        "correct answers to pass."
    )

    if st.button(
        "Start practice →",
        type="primary",
        key=f'grammar_done_{lesson["id"]}',
    ):
        run["stage"] = "exercise"
        st.rerun()


def _exercise_input(
    exercise,
    lesson_id,
    exercise_index,
):
    widget_key = (
        f"course_answer_"
        f"{lesson_id}_"
        f"{exercise_index}"
    )

    exercise_type = exercise["type"]

    if exercise_type == "multiple_choice":
        return st.radio(
            "Choose one answer",
            exercise["options"],
            index=None,
            key=widget_key,
        )

    if (
        exercise_type == "fill_blank"
        and exercise["options"]
    ):
        return st.radio(
            "Choose the missing word",
            exercise["options"],
            index=None,
            key=widget_key,
        )

    if exercise_type == "word_order":
        words = list(exercise["words"])

        random.Random(
            f"{lesson_id}_{exercise_index}"
        ).shuffle(words)

        st.write(
            "Arrange these words by typing "
            "the sentence:"
        )

        st.info("   ·   ".join(words))

        return st.text_input(
            "Your sentence",
            key=widget_key,
        )

    return st.text_input(
        "Type your answer",
        key=widget_key,
    )


def _render_exercise(lesson, run):
    _lesson_title(lesson)

    exercises = lesson["exercises"]
    exercise_index = run["exercise_index"]
    exercise = exercises[exercise_index]

    st.markdown(
        f"## 3. Practice "
        f"({exercise_index + 1}/"
        f"{len(exercises)})"
    )

    st.progress(
        exercise_index / len(exercises)
    )

    st.markdown(
        f'### {exercise["prompt"]}'
    )

    candidate = _exercise_input(
        exercise,
        lesson["id"],
        exercise_index,
    )

    answer_ready = (
        candidate is not None
        and str(candidate).strip()
    )

    if not run["answered"]:
        if st.button(
            "Check answer",
            type="primary",
            disabled=not answer_ready,
            key=(
                f'check_{lesson["id"]}_'
                f'{exercise_index}'
            ),
        ):
            was_correct = _is_correct(
                candidate,
                exercise,
            )

            run["answered"] = True
            run["was_correct"] = was_correct
            run["attempted_answers"] += 1

            if was_correct:
                run["correct_answers"] += 1

            st.rerun()

    if run["answered"]:
        if run["was_correct"]:
            st.success(
                "Correct! Great work."
            )
        else:
            st.error(
                "Not quite. The correct "
                f'answer is: '
                f'{exercise["answer"]}'
            )

        st.info(
            f'Why: {exercise["explanation"]}'
        )

        final_exercise = (
            exercise_index
            == len(exercises) - 1
        )

        if final_exercise:
            next_label = "See results →"
        else:
            next_label = "Next question →"

        if st.button(
            next_label,
            type="primary",
            key=(
                f'next_{lesson["id"]}_'
                f'{exercise_index}'
            ),
        ):
            if final_exercise:
                run["stage"] = "complete"
            else:
                run["exercise_index"] += 1
                run["answered"] = False
                run["was_correct"] = False

            st.rerun()


def _award_lesson(course, lesson, run):
    progress = _course_progress(
        course["language"]
    )

    lesson_id = lesson["id"]

    if lesson_id in progress[
        "completed_lessons"
    ]:
        run["rewarded"] = True
        return False

    progress["completed_lessons"].append(
        lesson_id
    )

    progress["lesson_scores"][lesson_id] = {
        "correct": run["correct_answers"],
        "total": len(lesson["exercises"]),
    }

    st.session_state.coins += (
        lesson["coin_reward"]
    )

    language_progress = (
        st.session_state.language_progress[
            course["language"]
        ]
    )

    language_progress["overall_xp"] += (
        lesson["xp_reward"]
    )

    language_progress["weekly_minutes"] += (
        lesson["estimated_minutes"]
    )

    skill_levels = language_progress.get(
        "skill_levels",
        {},
    )

    if "Vocabulary" in skill_levels:
        skill_levels["Vocabulary"] += 1

    if "Grammar" in skill_levels:
        skill_levels["Grammar"] += 1

    run["rewarded"] = True

    return True


def _render_complete(course, lesson, run):
    _lesson_title(lesson)

    total = len(lesson["exercises"])
    correct = run["correct_answers"]

    passing_score = max(
        1,
        (total * 2 + 2) // 3,
    )

    passed = correct >= passing_score

    if passed:
        newly_completed = False

        if not run["rewarded"]:
            newly_completed = _award_lesson(
                course,
                lesson,
                run,
            )

        st.success(
            f"Lesson complete! You answered "
            f"{correct} of {total} questions "
            f"correctly."
        )

        if newly_completed:
            st.balloons()

            st.info(
                f'You earned '
                f'{lesson["xp_reward"]} XP and '
                f'{lesson["coin_reward"]} coins. '
                f'The next lesson is now unlocked.'
            )
        else:
            st.info(
                "You reviewed this lesson "
                "successfully. Rewards are given "
                "once per lesson."
            )

        if st.button(
            "Return to learning path",
            type="primary",
            key=(
                f'complete_path_'
                f'{lesson["id"]}'
            ),
        ):
            _return_to_path()

    else:
        st.error(
            f"You answered {correct} of "
            f"{total} correctly. You need "
            f"{passing_score} correct answers "
            f"to pass."
        )

        st.write(
            "Review the vocabulary and grammar, "
            "then try again."
        )

        retry_column, path_column = (
            st.columns(2)
        )

        with retry_column:
            if st.button(
                "Try lesson again",
                type="primary",
                key=f'retry_{lesson["id"]}',
            ):
                _start_lesson(
                    course,
                    lesson["id"],
                )
                st.rerun()

        with path_column:
            if st.button(
                "Return to learning path",
                key=(
                    f'failed_path_'
                    f'{lesson["id"]}'
                ),
            ):
                _return_to_path()


def _render_active_lesson(course, run):
    lesson = _find_lesson(
        course,
        run["lesson_id"],
    )

    if lesson is None:
        _return_to_path()
        return

    if run["stage"] == "vocabulary":
        _render_vocabulary(lesson, run)

    elif run["stage"] == "grammar":
        _render_grammar(lesson, run)

    elif run["stage"] == "exercise":
        _render_exercise(lesson, run)

    else:
        _render_complete(
            course,
            lesson,
            run,
        )


def render_lessons():
    language = st.session_state.active_language

    if language not in ("English", "Bengali"):
        if st.button(
            "← Home",
            key="unsupported_course_home",
        ):
            st.session_state.current_view = "Home"
            st.rerun()

        st.title("📚 Learning Path")

        st.info(
            "The full interactive course is "
            "currently available for English. "
            "The Bengali course is being added "
            "next."
        )
        return

    if language == "Bengali":
        course = get_bengali_course()
    else:
        course = get_english_course()

    run = st.session_state.get(
        "course_lesson_run")
    

    if (
        run
        and run.get("language")
        == course["language"]
    ):
        _render_active_lesson(
            course,
            run,
        )

    else:
        if run:
            st.session_state.pop(
                "course_lesson_run",
                None,
            )

        _render_path(course)