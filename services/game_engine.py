import random
import re
import unicodedata
from copy import deepcopy


EXERCISES = {
    "English": [
        {
            "situation": "You are politely asking for water at a café.",
            "translation": "I would like a glass of water.",
            "picture": "🥛 💧",
            "clue": "The sentence begins with “I would...”",
            "answer": "I would like a glass of water",
            "accepted_answers": [],
            "words": [
                "I",
                "would",
                "like",
                "a",
                "glass",
                "of",
                "water",
            ],
            "transliteration": None,
            "explanation": (
                "“Would like” is a polite way to say what you want."
            ),
        }
    ],
    "French": [
        {
            "situation": "You are politely asking for water at a café.",
            "translation": "I would like a glass of water.",
            "picture": "🥛 💧",
            "clue": "The sentence begins with “Je voudrais...”",
            "answer": "Je voudrais un verre d'eau",
            "accepted_answers": [
                "Je voudrais un verre d’eau",
            ],
            "words": [
                "Je",
                "voudrais",
                "un",
                "verre",
                "d'eau",
            ],
            "transliteration": None,
            "explanation": (
                "“Je voudrais” is a polite way to say "
                "“I would like.”"
            ),
        }
    ],
    "Spanish": [
        {
            "situation": "You are politely asking for water at a café.",
            "translation": "I would like a glass of water.",
            "picture": "🥛 💧",
            "clue": "The sentence begins with “Quisiera...”",
            "answer": "Quisiera un vaso de agua",
            "accepted_answers": [],
            "words": [
                "Quisiera",
                "un",
                "vaso",
                "de",
                "agua",
            ],
            "transliteration": None,
            "explanation": (
                "“Quisiera” is a polite way to ask "
                "for something."
            ),
        }
    ],
    "Hindi": [
        {
            "situation": "You are politely asking for water.",
            "translation": "I would like a glass of water.",
            "picture": "🥛 💧",
            "clue": "The sentence begins with “मुझे...”",
            "answer": "मुझे एक गिलास पानी चाहिए",
            "accepted_answers": [],
            "words": [
                "मुझे",
                "एक",
                "गिलास",
                "पानी",
                "चाहिए",
            ],
            "transliteration": (
                "Mujhe ek gilaas paani chahiye"
            ),
            "explanation": (
                "“चाहिए” expresses needing or wanting "
                "something politely."
            ),
        }
    ],
    "Bengali": [
        {
            "situation": "You are politely asking for water.",
            "translation": "I would like a glass of water.",
            "picture": "🥛 💧",
            "clue": "The sentence begins with “আমি...”",
            "answer": "আমি এক গ্লাস জল চাই",
            "accepted_answers": [
                "আমি এক গ্লাস পানি চাই",
            ],
            "words": [
                "আমি",
                "এক",
                "গ্লাস",
                "জল",
                "চাই",
            ],
            "transliteration": (
                "Ami ek glass jol chai"
            ),
            "explanation": (
                "“চাই” expresses wanting something. "
                "Both “জল” and “পানি” are accepted here."
            ),
        }
    ],
    "Korean": [
        {
            "situation": "You are politely asking for water.",
            "translation": "Please give me a glass of water.",
            "picture": "🥛 💧",
            "clue": "The sentence begins with “물...”",
            "answer": "물 한 잔 주세요",
            "accepted_answers": [],
            "words": [
                "물",
                "한",
                "잔",
                "주세요",
            ],
            "transliteration": (
                "Mul han jan juseyo"
            ),
            "explanation": (
                "“주세요” is used to request something "
                "politely."
            ),
        }
    ],
    "Japanese": [
        {
            "situation": "You are politely asking for water.",
            "translation": "Please give me a glass of water.",
            "picture": "🥛 💧",
            "clue": "The sentence begins with “お水を...”",
            "answer": "お水を 一杯 ください",
            "accepted_answers": [
                "お水を一杯ください",
                "水を一杯ください",
            ],
            "words": [
                "お水を",
                "一杯",
                "ください",
            ],
            "transliteration": (
                "Omizu o ippai kudasai"
            ),
            "explanation": (
                "“ください” is used for a polite request."
            ),
        }
    ],
}


def get_exercises(language):
    exercises = EXERCISES.get(
        language,
        EXERCISES["English"],
    )

    return deepcopy(exercises)


def create_shuffled_tiles(exercise):
    tiles = [
        {
            "id": index,
            "word": word,
        }
        for index, word in enumerate(exercise["words"])
    ]

    random.shuffle(tiles)
    return tiles


def remove_latin_accents(text):
    result = []

    for character in text:
        character_name = unicodedata.name(character, "")

        if "LATIN" in character_name:
            decomposed = unicodedata.normalize(
                "NFD",
                character,
            )

            result.extend(
                part
                for part in decomposed
                if unicodedata.category(part) != "Mn"
            )
        else:
            result.append(character)

    return "".join(result)


def normalize_answer(answer, strict=False):
    normalized = answer.strip().casefold()
    normalized = normalized.replace("’", "'")
    normalized = re.sub(
        r"""[.,!?;:¿¡।。！？、'"-]""",
        "",
        normalized,
    )
    normalized = " ".join(normalized.split())

    if not strict:
        normalized = remove_latin_accents(normalized)

    return normalized


def check_answer(user_answer, exercise, level):
    strict_levels = {
        "Upper Intermediate",
        "Advanced",
    }

    strict = level in strict_levels

    accepted_answers = [
        exercise["answer"],
        *exercise.get("accepted_answers", []),
    ]

    normalized_user_answer = normalize_answer(
        user_answer,
        strict,
    )

    return any(
        normalized_user_answer
        == normalize_answer(answer, strict)
        for answer in accepted_answers
    )


def calculate_reward(difficulty, used_hint):
    rewards = {
        "Relaxed": 8,
        "Balanced": 10,
        "Challenging": 15,
        "Custom": 18,
    }

    reward = rewards.get(difficulty, 10)

    if used_hint:
        reward -= 2

    return max(reward, 3)


def get_hint(exercise, hint_number):
    if hint_number == 1:
        return (
            f'The first word is “{exercise["words"][0]}”.'
        )

    if hint_number == 2:
        transliteration = exercise.get("transliteration")

        if transliteration:
            return f"Pronunciation guide: {transliteration}"

        return exercise["clue"]

    return exercise["explanation"]