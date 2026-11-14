import random

from services.pronunciation_engine import (
    normalize_text,
    phrase_match_score,
)


LISTENING_MODES = (
    "mixed",
    "meaning",
    "dictation",
    "missing_word",
    "dialogue",
)

MODE_LABEL_KEYS = {
    "mixed": "listening_mode_mixed",
    "meaning": "listening_mode_meaning",
    "dictation": "listening_mode_dictation",
    "missing_word": "listening_mode_missing_word",
    "dialogue": "listening_mode_dialogue",
}

DICTATION_THRESHOLDS = {
    "Relaxed": 70,
    "Balanced": 80,
    "Challenging": 90,
    "Custom": 90,
}

REPLAY_LIMITS = {
    "Relaxed": None,
    "Balanced": 4,
    "Challenging": 2,
    "Custom": 2,
}


def replay_limit(difficulty):
    return REPLAY_LIMITS.get(difficulty, 4)


def _sample_unique(values, excluded, amount):
    candidates = []
    excluded_normalized = normalize_text(excluded)

    for value in values:
        value = str(value or "").strip()

        if (
            value
            and normalize_text(value) != excluded_normalized
            and value not in candidates
        ):
            candidates.append(value)

    random.shuffle(candidates)
    return candidates[:amount]

def _meaning_question(
    exercise,
    exercises,
    choice_total,
):
    correct = str(
        exercise["translation"]
    ).strip()
    wrong = _sample_unique(
        [
            item.get("translation")
            for item in exercises
        ],
        correct,
        choice_total - 1,
    )
    options = [correct, *wrong]
    random.shuffle(options)

    return {
        "kind": "meaning",
        "audio_text": str(
            exercise["answer"]
        ).strip(),
        "correct_answer": correct,
        "accepted_answers": [correct],
        "options": options,
        "masked_text": "",
        "translation": correct,
        "transliteration": exercise.get(
            "transliteration"
        ),
        "explanation": exercise.get(
            "explanation"
        ),
    }


def _dictation_question(exercise):
    answer = str(
        exercise["answer"]
    ).strip()

    return {
        "kind": "dictation",
        "audio_text": answer,
        "correct_answer": answer,
        "accepted_answers": [
            answer,
            *exercise.get(
                "accepted_answers",
                [],
            ),
        ],
        "options": [],
        "masked_text": "",
        "translation": str(
            exercise["translation"]
        ).strip(),
        "transliteration": exercise.get(
            "transliteration"
        ),
        "explanation": exercise.get(
            "explanation"
        ),
    }

def _missing_word_question(
    exercise,
    exercises,
    choice_total,
):
    answer = str(
        exercise["answer"]
    ).strip()
    words = [
        str(word).strip()
        for word in exercise.get(
            "words",
            [],
        )
        if str(word).strip()
    ]

    if not words:
        words = answer.split()

    missing_index = random.randrange(
        len(words)
    )
    missing_word = words[missing_index]

    masked_words = list(words)
    masked_words[missing_index] = "_____"
    masked_text = " ".join(masked_words)

    all_words = [
        word
        for item in exercises
        for word in item.get(
            "words",
            [],
        )
    ]
    wrong = _sample_unique(
        all_words,
        missing_word,
        choice_total - 1,
    )
    options = [missing_word, *wrong]
    random.shuffle(options)

    return {
        "kind": "missing_word",
        "audio_text": answer,
        "correct_answer": missing_word,
        "accepted_answers": [missing_word],
        "options": options,
        "masked_text": masked_text,
        "translation": str(
            exercise["translation"]
        ).strip(),
        "transliteration": exercise.get(
            "transliteration"
        ),
        "explanation": exercise.get(
            "explanation"
        ),
    }

def _dialogue_question(
    scenario,
    scenarios,
    choice_total,
):
    correct = str(
        scenario["response"]
    ).strip()
    wrong = _sample_unique(
        [
            item.get("response")
            for item in scenarios
        ],
        correct,
        choice_total - 1,
    )
    options = [correct, *wrong]
    random.shuffle(options)

    return {
        "kind": "dialogue",
        "audio_text": str(
            scenario["prompt"]
        ).strip(),
        "correct_answer": correct,
        "accepted_answers": [correct],
        "options": options,
        "masked_text": "",
        "translation": str(
            scenario["prompt_meaning"]
        ).strip(),
        "response_meaning": str(
            scenario["response_meaning"]
        ).strip(),
        "transliteration": None,
        "explanation": None,
    }


def _mode_sequence(
    selected_mode,
    question_total,
):
    if selected_mode != "mixed":
        return [
            selected_mode
        ] * question_total

    modes = list(
        LISTENING_MODES[1:]
    )
    sequence = []

    while len(sequence) < question_total:
        random.shuffle(modes)
        sequence.extend(modes)

    return sequence[:question_total]



def build_listening_questions(
    exercises,
    scenarios,
    question_total,
    choice_total,
    selected_mode,
):
    exercises = list(exercises or [])
    scenarios = list(scenarios or [])

    if not exercises and not scenarios:
        return []

    modes = _mode_sequence(
        selected_mode,
        question_total,
    )

    random.shuffle(exercises)
    random.shuffle(scenarios)

    questions = []
    exercise_index = 0
    scenario_index = 0

    for mode in modes:
        if mode == "dialogue" and scenarios:
            scenario = scenarios[
                scenario_index % len(scenarios)
            ]
            scenario_index += 1

            question = _dialogue_question(
                scenario,
                scenarios,
                choice_total,
            )

        elif not exercises:
            scenario = scenarios[
                scenario_index % len(scenarios)
            ]
            scenario_index += 1

            question = _dialogue_question(
                scenario,
                scenarios,
                choice_total,
            )

        else:
            exercise = exercises[
                exercise_index % len(exercises)
            ]
            exercise_index += 1

            if mode == "dictation":
                question = _dictation_question(
                    exercise
                )

            elif mode == "missing_word":
                question = _missing_word_question(
                    exercise,
                    exercises,
                    choice_total,
                )

            else:
                question = _meaning_question(
                    exercise,
                    exercises,
                    choice_total,
                )

        questions.append(question)

    return questions
    
def check_listening_answer(
    question,
    user_answer,
    difficulty,
):
    answer = str(
        user_answer or ""
    ).strip()

    if not answer:
        return {
            "correct": False,
            "score": 0,
        }

    if question["kind"] == "dictation":
        scores = [
            phrase_match_score(
                answer,
                accepted,
            )
            for accepted in question[
                "accepted_answers"
            ]
        ]
        score = max(
            scores,
            default=0,
        )
        required = (
            DICTATION_THRESHOLDS.get(
                difficulty,
                80,
            )
        )

        return {
            "correct": score >= required,
            "score": score,
            "required": required,
        }

    correct = (
        normalize_text(answer)
        == normalize_text(
            question["correct_answer"]
        )
    )

    return {
        "correct": correct,
        "score": 100 if correct else 0,
    }