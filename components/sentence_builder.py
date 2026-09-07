import html
import random
from collections import Counter

import streamlit as st

from locales import t
from services.game_engine import (
    calculate_reward,
    check_answer,
    get_exercises,
    get_hint,
    normalize_answer,
)


SESSION_LENGTHS = [5, 10, 15]
DISTRACTOR_COUNTS = {
    "Relaxed": 0,
    "Balanced": 0,
    "Challenging": 2,
    "Custom": 3,
}


def _apply_styles():
    st.markdown(
        """
        <style>
        .wf-sb-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
            margin: .2rem 0 .7rem;
        }
        .wf-sb-heading h1 {
            margin: 0;
            color: var(--wf-text);
            font-size: clamp(1.8rem, 4vw, 2.55rem);
            font-weight: 900;
            letter-spacing: -.035em;
        }
        .wf-sb-status {
            display: flex;
            gap: .5rem;
            flex-wrap: wrap;
        }
        .wf-sb-pill {
            padding: .48rem .72rem;
            border: 1px solid var(--wf-border);
            border-radius: 999px;
            background: var(--wf-surface);
            color: var(--wf-text);
            font-weight: 800;
            box-shadow: 0 6px 18px rgba(40, 45, 70, .07);
        }
        .wf-sb-intro {
            padding: clamp(1.35rem, 4vw, 2.25rem);
            margin: .9rem 0 1.25rem;
            border: 1px solid var(--wf-border);
            border-radius: 24px;
            background:
                radial-gradient(
                    circle at 94% 4%,
                    rgba(34,184,207,.22),
                    transparent 34%
                ),
                linear-gradient(
                    145deg,
                    rgba(108,99,255,.15),
                    var(--wf-surface) 54%
                );
            box-shadow: var(--wf-shadow);
        }
        .wf-sb-intro-icon {
            display: grid;
            place-items: center;
            width: 3.5rem;
            height: 3.5rem;
            margin-bottom: .8rem;
            border-radius: 17px;
            background: linear-gradient(
                135deg,
                #6C63FF,
                #22B8CF
            );
            font-size: 1.7rem;
            box-shadow: 0 10px 24px rgba(108,99,255,.24);
        }
        .wf-sb-intro h2 {
            margin: 0 0 .4rem;
            color: var(--wf-text);
        }
        .wf-sb-intro p {
            margin: 0;
            color: var(--wf-muted);
            line-height: 1.55;
        }
        .wf-sb-prompt {
            display: grid;
            grid-template-columns: auto 1fr;
            align-items: center;
            gap: 1rem;
            padding: clamp(1.1rem, 3vw, 1.55rem);
            margin: .9rem 0 1.15rem;
            border: 1px solid var(--wf-border);
            border-radius: 20px;
            background:
                linear-gradient(
                    135deg,
                    rgba(108,99,255,.13),
                    rgba(34,184,207,.08)
                ),
                var(--wf-surface);
            box-shadow: 0 12px 28px rgba(40,45,70,.08);
        }
        .wf-sb-picture {
            display: grid;
            place-items: center;
            min-width: 4.2rem;
            min-height: 4.2rem;
            padding: .55rem;
            border-radius: 17px;
            background: var(--wf-surface);
            font-size: 2rem;
        }
        .wf-sb-kicker {
            margin-bottom: .3rem;
            color: var(--wf-purple);
            font-size: .78rem;
            font-weight: 900;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        .wf-sb-situation {
            color: var(--wf-text);
            font-size: clamp(1.05rem, 2.4vw, 1.3rem);
            font-weight: 850;
            line-height: 1.4;
        }
        .wf-sb-meaning {
            margin-top: .4rem;
            color: var(--wf-muted);
            line-height: 1.45;
        }
        .wf-sb-label {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            margin: 1rem 0 .5rem;
            color: var(--wf-text);
            font-weight: 850;
        }
        .wf-sb-label small {
            color: var(--wf-muted);
        }
        .wf-sb-empty {
            display: grid;
            place-items: center;
            min-height: 4rem;
            color: var(--wf-muted);
            text-align: center;
        }
        .wf-sb-feedback {
            display: flex;
            gap: .5rem;
            flex-wrap: wrap;
            margin: .8rem 0;
        }
        .wf-sb-feedback span {
            padding: .48rem .68rem;
            border-radius: 10px;
            font-weight: 800;
        }
        .wf-sb-correct {
            background: rgba(34,197,94,.14);
            color: var(--wf-text);
        }
        .wf-sb-moved {
            background: rgba(245,158,11,.16);
            color: var(--wf-text);
        }
        .wf-sb-missing {
            background: rgba(239,68,68,.13);
            color: var(--wf-text);
        }
        .wf-sb-finish {
            padding: clamp(1.4rem, 4vw, 2.2rem);
            margin: .8rem 0 1.2rem;
            border-radius: 24px;
            background: linear-gradient(
                135deg,
                #6C63FF,
                #4F8FF7,
                #22B8CF
            );
            color: white;
            text-align: center;
            box-shadow: var(--wf-shadow);
        }
        .wf-sb-finish h2,
        .wf-sb-finish p {
            color: white;
        }
        .wf-sb-finish h2 {
            margin: 0 0 .35rem;
        }
        .wf-sb-finish p {
            margin: 0;
            opacity: .9;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--wf-border);
            border-radius: 18px;
            background: var(--wf-surface);
            box-shadow: 0 8px 22px rgba(40,45,70,.06);
        }
        div[data-testid="stButton"] > button {
            border-radius: 13px;
        }
        div[data-testid="stButton"] > button:disabled {
            opacity: .48;
        }
        @media (max-width: 700px) {
            .wf-sb-prompt {
                grid-template-columns: 1fr;
            }
            .wf-sb-picture {
                width: fit-content;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _safe(value):
    return html.escape(str(value))


def _exercise_order(
    exercise_count,
    total_rounds,
):
    order = []

    while len(order) < total_rounds:
        group = list(range(exercise_count))
        random.shuffle(group)

        if (
            order
            and group
            and group[0] == order[-1]
        ):
            group.append(group.pop(0))

        order.extend(group)

    return order[:total_rounds]


def _distractors(
    exercises,
    exercise_index,
    count,
):
    answer_words = {
        normalize_answer(word)
        for word in exercises[
            exercise_index
        ]["words"]
    }

    choices = []
    seen = set(answer_words)

    for index, exercise in enumerate(
        exercises
    ):
        if index == exercise_index:
            continue

        for word in exercise.get(
            "words",
            [],
        ):
            normalized = normalize_answer(
                word
            )

            if (
                normalized
                and normalized not in seen
            ):
                choices.append(word)
                seen.add(normalized)

    random.shuffle(choices)

    return choices[:count]


def _new_tiles(
    language,
    exercise_index,
):
    exercises = get_exercises(language)
    exercise = exercises[exercise_index]

    tiles = [
        {
            "id": f"answer_{index}",
            "word": word,
        }
        for index, word in enumerate(
            exercise["words"]
        )
    ]

    count = DISTRACTOR_COUNTS.get(
        st.session_state.difficulty,
        0,
    )

    tiles.extend(
        {
            "id": f"extra_{index}",
            "word": word,
        }
        for index, word in enumerate(
            _distractors(
                exercises,
                exercise_index,
                count,
            )
        )
    )

    random.shuffle(tiles)

    return tiles


def start_session(
    language,
    total_rounds,
):
    exercise_count = len(
        get_exercises(language)
    )

    st.session_state.sentence_session = {
        "language": language,
        "total_rounds": total_rounds,
        "exercise_order": _exercise_order(
            exercise_count,
            total_rounds,
        ),
        "completed": 0,
        "wrong": 0,
        "coins": 0,
        "combo": 0,
        "best_combo": 0,
        "finished": False,
        "celebrated": False,
    }

    start_round(language, 0)


def start_round(
    language,
    round_number,
):
    session = (
        st.session_state.sentence_session
    )

    exercise_index = session[
        "exercise_order"
    ][round_number]

    st.session_state.sentence_game = {
        "language": language,
        "round_number": round_number,
        "exercise_index": exercise_index,
        "tiles": _new_tiles(
            language,
            exercise_index,
        ),
        "selected": [],
        "hints": [],
        "answered": False,
        "reward": 0,
        "combo_bonus": 0,
        "feedback": None,
        "last_wrong_order": None,
    }


def _current_session(language):
    session = st.session_state.get(
        "sentence_session"
    )

    required = {
        "exercise_order",
        "completed",
        "wrong",
        "combo",
    }

    if (
        session
        and session.get("language")
        == language
        and required <= session.keys()
    ):
        return session

    st.session_state.pop(
        "sentence_session",
        None,
    )

    st.session_state.pop(
        "sentence_game",
        None,
    )

    return None


def _selected_tiles(game):
    lookup = {
        tile["id"]: tile
        for tile in game["tiles"]
    }

    return [
        lookup[tile_id]
        for tile_id in game["selected"]
        if tile_id in lookup
    ]


def _candidate(game):
    return " ".join(
        tile["word"]
        for tile in _selected_tiles(game)
    )


def _normalized_words(words):
    return [
        normalize_answer(word)
        for word in words
    ]


def _word_feedback(
    game,
    exercise,
):
    expected_words = list(
        exercise["words"]
    )

    chosen_words = [
        tile["word"]
        for tile in _selected_tiles(game)
    ]

    expected = _normalized_words(
        expected_words
    )

    chosen = _normalized_words(
        chosen_words
    )

    chosen_counts = Counter(chosen)
    expected_counts = Counter(expected)
    words = []

    for index, word in enumerate(
        expected_words
    ):
        normalized = expected[index]

        if (
            index < len(chosen)
            and chosen[index] == normalized
        ):
            status = "correct"

        elif chosen_counts[normalized]:
            status = "moved"

        else:
            status = "missing"

        words.append(
            {
                "word": word,
                "status": status,
            }
        )

    extra_counts = dict(
        chosen_counts - expected_counts
    )

    extras = []

    for word, normalized in zip(
        chosen_words,
        chosen,
    ):
        if extra_counts.get(
            normalized,
            0,
        ):
            extras.append(word)
            extra_counts[normalized] -= 1

    return {
        "words": words,
        "extras": extras,
    }


def _render_header(
    language,
    level,
    combo,
):
    back, heading = st.columns([1, 5])

    with back:
        if st.button(f"← {t('home')}"):
            st.session_state.current_view = "Home"
            st.rerun()

    with heading:
        st.markdown(
            (
                '<div class="wf-sb-heading">'
                f'<h1>🧩 {_safe(t("sentence_builder"))}</h1>'
                '<div class="wf-sb-status">'
                '<span class="wf-sb-pill">'
                f'❤️ {st.session_state.hearts}/5'
                '</span>'
                '<span class="wf-sb-pill">'
                f'🔥 {combo}'
                '</span>'
                '<span class="wf-sb-pill">'
                f'🪙 {st.session_state.coins}'
                '</span>'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    st.caption(
        f"{t('language')}: {language} · "
        f"{t('level')}: {level}"
    )




def _render_setup(
    language,
    level,
):
    _render_header(
        language,
        level,
        0,
    )

    st.markdown(
        (
            '<section class="wf-sb-intro">'
            '<div class="wf-sb-intro-icon">🧩</div>'
            f'<h2>{_safe(t("choose_session_length"))}</h2>'
            f'<p>{_safe(t("sentence_builder_description"))}</p>'
            '</section>'
        ),
        unsafe_allow_html=True,
    )


    with st.container(border=True):
        st.markdown(
            f"### 📚 {t('learn_before_practice_title')}"
        )
        st.write(t("learn_before_practice_help"))

        if st.button(
            f"📚 {t('open_learning_path')} →",
            key=f"open_learning_path_{language}",
            use_container_width=True,
        ):
            st.session_state.current_view = "Lessons"
            st.rerun()

    length = (
        st.segmented_control(
            t("session_length"),
            SESSION_LENGTHS,
            default=5,
            format_func=lambda count: t(
                "round_count",
                count=count,
            ),
            key=(
                f"sentence_round_count_"
                f"{language}"
            ),
        )
        or 5
    )

    if st.button(
        f"{t('start_session')} →",
        type="primary",
        use_container_width=True,
    ):
        start_session(
            language,
            length,
        )

        st.rerun()


def _render_prompt(exercise):
    st.markdown(
        (
            '<section class="wf-sb-prompt">'
            f'<div class="wf-sb-picture">{_safe(exercise["picture"])}</div>'
            '<div>'
            f'<div class="wf-sb-kicker">{_safe(t("current_round"))}</div>'
            f'<div class="wf-sb-situation">{_safe(exercise["situation"])}</div>'
            '</div>'
            '</section>'
        ),
        unsafe_allow_html=True,
    )

def _tile_grid(
    game,
    tiles,
    selected,
):
    if not tiles:
        st.markdown(
            (
                '<div class="wf-sb-empty">'
                f'{_safe(t("select_words_in_order"))}'
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        return

    for start in range(
        0,
        len(tiles),
        4,
    ):
        row = tiles[start:start + 4]
        columns = st.columns(len(row))

        for column, tile in zip(
            columns,
            row,
        ):
            with column:
                if selected:
                    label = (
                        f'{tile["word"]}  ×'
                    )
                    key_start = "picked"

                else:
                    label = tile["word"]
                    key_start = "tile"

                key = (
                    f"{key_start}_"
                    f'{game["round_number"]}_'
                    f'{tile["id"]}'
                )

                if st.button(
                    label,
                    key=key,
                    disabled=game["answered"],
                ):
                    if selected:
                        game["selected"].remove(
                            tile["id"]
                        )

                    else:
                        game["selected"].append(
                            tile["id"]
                        )

                    game["feedback"] = None
                    st.rerun()


def _render_builder(
    game,
    exercise,
):
    selected = _selected_tiles(game)

    selected_ids = set(
        game["selected"]
    )

    available = [
        tile
        for tile in game["tiles"]
        if tile["id"] not in selected_ids
    ]

    st.markdown(
        (
            '<div class="wf-sb-label">'
            f'<span>{_safe(t("your_sentence"))}</span>'
            "<small>"
            f'{len(selected)}/{len(exercise["words"])}'
            "</small>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        _tile_grid(
            game,
            selected,
            True,
        )

    st.markdown(
        (
            '<div class="wf-sb-label">'
            "<span>"
            f'{_safe(t("answer_method_word_tiles"))}'
            "</span>"
            "<small>↓</small>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        _tile_grid(
            game,
            available,
            False,
        )


def _render_feedback(feedback):
    icons = {
        "correct": "✓",
        "moved": "↔",
        "missing": "×",
    }

    pieces = [
        (
            f'<span class="wf-sb-'
            f'{item["status"]}">'
            f'{icons[item["status"]]} '
            f'{_safe(item["word"])}'
            "</span>"
        )
        for item in feedback["words"]
    ]

    st.markdown(
        (
            '<div class="wf-sb-feedback">'
            + "".join(pieces)
            + "</div>"
        ),
        unsafe_allow_html=True,
    )

    if feedback["extras"]:
        st.caption(
            "➕ "
            + " · ".join(
                feedback["extras"]
            )
        )


def _next_hint(
    game,
    exercise,
):
    number = len(game["hints"]) + 1

    if number > 1:
        return get_hint(
            exercise,
            min(number, 3),
        )

    chosen = _normalized_words(
        [
            tile["word"]
            for tile in _selected_tiles(
                game
            )
        ]
    )

    expected = _normalized_words(
        exercise["words"]
    )

    prefix = 0

    for (
        chosen_word,
        expected_word,
    ) in zip(chosen, expected):
        if chosen_word != expected_word:
            break

        prefix += 1

    if prefix == 0:
        return get_hint(
            exercise,
            1,
        )

    position = min(
        prefix,
        len(expected) - 1,
    )

    return (
        f"→ "
        f'{exercise["words"][position]}'
    )


def _render_controls(
    game,
    exercise,
):
    left = 3 - len(game["hints"])

    hint, undo, clear = st.columns(
        [1.25, 1, 1]
    )

    with hint:
        if st.button(
            f"💡 {t('use_hint', count=left)}",
            disabled=left == 0,
        ):
            game["hints"].append(
                _next_hint(
                    game,
                    exercise,
                )
            )

            st.rerun()

    with undo:
        if st.button(
            f"↶ {t('undo_last_word')}",
            disabled=not game["selected"],
        ):
            game["selected"].pop()
            game["feedback"] = None
            st.rerun()

    with clear:
        if st.button(
            f"⌫ {t('clear_sentence')}",
            disabled=not game["selected"],
        ):
            game["selected"] = []
            game["feedback"] = None
            st.rerun()

    for hint_text in game["hints"]:
        st.info(
            t(
                "hint_message",
                hint=hint_text,
            )
        )


def _no_hearts():
    if st.session_state.hearts:
        return False

    st.error(
        t("no_hearts_remaining")
    )

    can_restore = (
        st.session_state.coins >= 20
    )

    if st.button(
        t("restore_heart"),
        disabled=not can_restore,
    ):
        st.session_state.coins -= 20
        st.session_state.hearts = 1
        st.rerun()

    if not can_restore:
        st.caption(
            t(
                "restore_heart_requirement"
            )
        )

    return True


def _check(
    game,
    session,
    exercise,
    level,
    progress,
):
    if check_answer(
        _candidate(game),
        exercise,
        level,
    ):
        session["completed"] += 1
        session["combo"] += 1

        session["best_combo"] = max(
            session["best_combo"],
            session["combo"],
        )

        base = calculate_reward(
            st.session_state.difficulty,
            bool(game["hints"]),
        )

        bonus = min(
            max(
                session["combo"] - 1,
                0,
            ),
            3,
        )

        reward = base + bonus

        session["coins"] += reward
        st.session_state.coins += reward
        progress["overall_xp"] += reward
        progress["weekly_minutes"] += 1

        progress["skill_levels"][
            "Sentence Builder"
        ] += 1

        game.update(
            answered=True,
            reward=reward,
            combo_bonus=bonus,
            feedback={
                "result": "correct",
                **_word_feedback(
                    game,
                    exercise,
                ),
            },
        )

        return

    signature = tuple(
        game["selected"]
    )

    if (
        signature
        != game["last_wrong_order"]
    ):
        st.session_state.hearts = max(
            st.session_state.hearts - 1,
            0,
        )

        session["wrong"] += 1
        session["combo"] = 0

        game["last_wrong_order"] = (
            signature
        )

    game["feedback"] = {
        "result": "incorrect",
        **_word_feedback(
            game,
            exercise,
        ),
    }


def _open_pronunciation(
    game,
    language,
):
    st.session_state.pronunciation_game = {
        "language": language,
        "round_number": game[
            "round_number"
        ],
        "exercise_index": game[
            "exercise_index"
        ],
        "attempt_number": 0,
        "result": None,
        "reward_granted": False,
        "best_score": 0,
        "previous_score": None,
        "reference_audio": b"",
        "reference_error": None,
        "reference_speed": None,
    }

    st.session_state.current_view = (
        "Pronunciation"
    )

    st.rerun()


def _render_result(
    game,
    session,
    exercise,
    language,
):
    feedback = game["feedback"]

    if not feedback:
        return

    if feedback["result"] == "incorrect":
        st.error(
            t("incorrect_answer")
        )

        _render_feedback(feedback)

        st.info(
            t(
                "grammar_help",
                explanation=exercise[
                    "explanation"
                ],
            )
        )

        return

    st.success(
        t(
            "correct_reward",
            reward=game["reward"],
        )
    )

    _render_feedback(feedback)

    st.info(
        t(
            "why_it_works",
            explanation=exercise[
                "explanation"
            ],
        )
    )

    if game["combo_bonus"]:
        st.caption(
            f'🔥 +{game["combo_bonus"]}'
        )

    bonus, next_column = st.columns(2)

    with bonus:
        if st.button(
            f"🎙️ {t('pronunciation_bonus')}"
        ):
            _open_pronunciation(
                game,
                language,
            )

    with next_column:
        finished = (
            session["completed"]
            >= session["total_rounds"]
        )

        if finished:
            label = t("finish_session")
        else:
            label = (
                f"{t('next_challenge')} →"
            )

        if st.button(
            label,
            type="primary",
        ):
            if finished:
                session["finished"] = True

                st.session_state.pop(
                    "sentence_game",
                    None,
                )

            else:
                start_round(
                    language,
                    game["round_number"] + 1,
                )

            st.rerun()


def _render_finish(
    language,
    level,
    session,
):
    _render_header(
        language,
        level,
        session["best_combo"],
    )

    if not session["celebrated"]:
        session["celebrated"] = True
        st.balloons()

    st.markdown(
        (
            '<section class="wf-sb-finish">'
            "<h2>"
            f'🏆 {_safe(t("session_complete"))}'
            "</h2>"
            "<p>"
            f'{_safe(t("sentence_builder_description"))}'
            "</p>"
            "</section>"
        ),
        unsafe_allow_html=True,
    )

    total = (
        session["completed"]
        + session["wrong"]
    )

    accuracy = round(
        session["completed"]
        / max(total, 1)
        * 100
    )

    one, two, three, four = (
        st.columns(4)
    )

    with one:
        st.metric(
            t("correct_answers"),
            (
                f'{session["completed"]}/'
                f'{session["total_rounds"]}'
            ),
        )

    with two:
        st.metric(
            t("session_coins"),
            session["coins"],
        )

    with three:
        st.metric(
            "🎯",
            f"{accuracy}%",
        )

    with four:
        st.metric(
            "🔥",
            session["best_combo"],
        )

    if st.button(
        t("play_again"),
        type="primary",
        use_container_width=True,
    ):
        st.session_state.pop(
            "sentence_session",
            None,
        )

        st.session_state.pop(
            "sentence_game",
            None,
        )

        st.rerun()


def _render_round(
    language,
    level,
    progress,
    session,
):
    if (
        "sentence_game"
        not in st.session_state
    ):
        start_round(
            language,
            session["completed"],
        )

    game = st.session_state.sentence_game

    exercise = get_exercises(
        language
    )[game["exercise_index"]]

    _render_header(
        language,
        level,
        session["combo"],
    )

    st.progress(
        (
            session["completed"]
            / session["total_rounds"]
        ),
        text=t(
            "session_progress",
            completed=session[
                "completed"
            ],
            total=session[
                "total_rounds"
            ],
        ),
    )

    st.caption(
        f'{t("current_round")}: '
        f'{game["round_number"] + 1}/'
        f'{session["total_rounds"]}'
    )

    _render_prompt(exercise)

    _render_builder(
        game,
        exercise,
    )

    if not game["answered"]:
        _render_controls(
            game,
            exercise,
        )

    no_hearts = _no_hearts()

    ready = (
        len(game["selected"])
        == len(exercise["words"])
    )

    if (
        not game["answered"]
        and st.button(
            t("check_answer"),
            type="primary",
            use_container_width=True,
            disabled=(
                not ready
                or no_hearts
            ),
        )
    ):
        _check(
            game,
            session,
            exercise,
            level,
            progress,
        )

        st.rerun()

    _render_result(
        game,
        session,
        exercise,
        language,
    )


def render_sentence_builder():
    _apply_styles()

    language = (
        st.session_state.active_language
    )

    progress = (
        st.session_state.language_progress[
            language
        ]
    )

    level = (
        progress["current_level"]
        or "Beginner"
    )

    session = _current_session(
        language
    )

    if session is None:
        _render_setup(
            language,
            level,
        )

    elif session["finished"]:
        _render_finish(
            language,
            level,
            session,
        )

    else:
        _render_round(
            language,
            level,
            progress,
            session,
        )