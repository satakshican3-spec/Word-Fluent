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
        },
        {
            "situation": "You meet your teacher at 8:00 a.m.",
            "translation": "Good morning.",
            "picture": "🌅👋",
            "clue": "The first word is Good.",
            "answer": "Good morning",
            "accepted_answers": [],
            "words": ["Good", "morning"],
            "transliteration": None,
            "explanation": "Good morning is a greeting used earlier in the day.",
        },
        {
            "situation": "You are introducing yourself to a new classmate.",
            "translation": "My name is Aisha.",
            "picture": "👋🙂",
            "clue": "The sentence begins with My.",
            "answer": "My name is Aisha",
            "accepted_answers": [],
            "words": ["My", "name", "is", "Aisha"],
            "transliteration": None,
            "explanation": "Use My name is to introduce yourself.",
        },
        {
            "situation": "You want to ask a new person their name.",
            "translation": "What is your name?",
            "picture": "🗣️❓",
            "clue": "The sentence begins with What.",
            "answer": "What is your name",
            "accepted_answers": [],
            "words": ["What", "is", "your", "name"],
            "transliteration": None,
            "explanation": "What is your name is a polite introduction question.",
        },
        {
            "situation": "You politely ask someone to open the door.",
            "translation": "Please open the door.",
            "picture": "🚪🙏",
            "clue": "The sentence begins with Please.",
            "answer": "Please open the door",
            "accepted_answers": [],
            "words": ["Please", "open", "the", "door"],
            "transliteration": None,
            "explanation": "Please makes a request sound polite.",
        },
    {
            "situation": "A classmate helps you carry your books.",
            "translation": "Thank you for your help.",
            "picture": "📚🤝",
            "clue": "The sentence begins with Thank.",
            "answer": "Thank you for your help",
            "accepted_answers": [],
            "words": ["Thank", "you", "for", "your", "help"],
            "transliteration": None,
            "explanation": "Thank you shows appreciation.",
        },
        {
            "situation": "You are showing someone a photo of your sister.",
            "translation": "She is my sister.",
            "picture": "👧🖼️",
            "clue": "The sentence begins with She.",
            "answer": "She is my sister",
            "accepted_answers": [],
            "words": ["She", "is", "my", "sister"],
            "transliteration": None,
            "explanation": "Use my for a person connected to you.",
        },
        {
            "situation": "You describe something you do each day.",
            "translation": "I study English every day.",
            "picture": "📚✏️",
            "clue": "The sentence begins with I study.",
            "answer": "I study English every day",
            "accepted_answers": [],
            "words": ["I", "study", "English", "every", "day"],
            "transliteration": None,
            "explanation": "The simple present describes routines and repeated actions.",
        },
        {
            "situation": "You describe your morning routine.",
            "translation": "I eat breakfast in the morning.",
            "picture": "🍳🌅",
            "clue": "The sentence begins with I eat.",
            "answer": "I eat breakfast in the morning",
            "accepted_answers": [],
            "words": ["I", "eat", "breakfast", "in", "the", "morning"],
            "transliteration": None,
            "explanation": "In the morning tells when the action happens.",
        },
        {
            "situation": "You politely order coffee at a café.",
            "translation": "I would like a coffee, please.",
            "picture": "☕🙏",
            "clue": "The sentence begins with I would.",
            "answer": "I would like a coffee please",
            "accepted_answers": [],
            "words": ["I", "would", "like", "a", "coffee", "please"],
            "transliteration": None,
            "explanation": "I would like and please make an order polite.",
        },
        {
            "situation": "You have finished eating and want to pay.",
            "translation": "May I have the bill, please?",
            "picture": "🧾🍽️",
            "clue": "The sentence begins with May I.",
            "answer": "May I have the bill please",
            "accepted_answers": [],
            "words": ["May", "I", "have", "the", "bill", "please"],
            "transliteration": None,
            "explanation": "May I have is a polite way to ask for something.",
        },
        {
            "situation": "You are looking for the library and ask someone.",
            "translation": "Where is the library?",
            "picture": "📚🗺️",
            "clue": "The sentence begins with Where.",
            "answer": "Where is the library",
            "accepted_answers": [],
            "words": ["Where", "is", "the", "library"],
            "transliteration": None,
            "explanation": "Use Where is to ask for the location of one place.",
        },
        {
            "situation": "You tell someone which way to turn at the corner.",
            "translation": "Turn left at the corner.",
            "picture": "⬅️🛣️",
            "clue": "The sentence begins with Turn.",
            "answer": "Turn left at the corner",
            "accepted_answers": [],
            "words": ["Turn", "left", "at", "the", "corner"],
            "transliteration": None,
            "explanation": "Turn left gives someone a direction.",
        },
        {
            "situation": "You explain that the station is close to the hotel.",
            "translation": "The station is near the hotel.",
            "picture": "🚉🏨",
            "clue": "The sentence begins with The station.",
            "answer": "The station is near the hotel",
            "accepted_answers": [],
            "words": ["The", "station", "is", "near", "the", "hotel"],
            "transliteration": None,
            "explanation": "Near means not far away.",
        },
        {
            "situation": "You have a problem and politely ask someone for help.",
            "translation": "Can you help me, please?",
            "picture": "🆘🤝",
            "clue": "The sentence begins with Can you.",
            "answer": "Can you help me please",
            "accepted_answers": [],
            "words": ["Can", "you", "help", "me", "please"],
            "transliteration": None,
            "explanation": "Can you help me is a direct and polite request.",
        },
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