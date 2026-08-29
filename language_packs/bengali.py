"""Beginner Bengali course content for WordFluent."""

from copy import deepcopy


def _vocabulary(*items):
    return [
        {"term": term, "meaning": meaning, "example": example}
        for term, meaning, example in items
    ]


def _exercise(
    exercise_type,
    prompt,
    answer,
    explanation,
    *,
    options=None,
    words=None,
    accepted_answers=None,
):
    return {
        "type": exercise_type,
        "prompt": prompt,
        "answer": answer,
        "explanation": explanation,
        "options": options or [],
        "words": words or [],
        "accepted_answers": accepted_answers or [],
    }


def _lesson(
    lesson_id,
    title,
    icon,
    objective,
    vocabulary,
    grammar_title,
    grammar_summary,
    exercises,
):
    return {
        "id": lesson_id,
        "title": title,
        "icon": icon,
        "objective": objective,
        "estimated_minutes": 6,
        "xp_reward": 25,
        "coin_reward": 10,
        "vocabulary": vocabulary,
        "grammar": {
            "title": grammar_title,
            "summary": grammar_summary,
        },
        "exercises": exercises,
    }


BENGALI_COURSE = {
    "language": "Bengali",
    "language_code": "BN",
    "level": "Beginner",
    "title": "বাংলা শুরু — Bengali Foundations",
    "description": (
        "Learn useful Bengali through greetings, family, food, travel, "
        "shopping, and short real-life conversations. Bengali script and "
        "easy transliteration are shown together."
    ),
    "units": [
        {
            "id": "bn-unit-1",
            "title": "First Words",
            "icon": "👋",
            "description": (
                "Greet people, introduce yourself, and ask simple questions."
            ),
            "lessons": [
                _lesson(
                    "bn-1-1",
                    "Greetings and Introductions",
                    "👋",
                    "Say hello, ask how someone is, and introduce yourself.",
                    _vocabulary(
                        (
                            "নমস্কার (Nomoshkar)",
                            "Hello",
                            "নমস্কার! আপনি কেমন আছেন?",
                        ),
                        (
                            "কেমন আছেন? (Kemon achhen?)",
                            "How are you? — polite",
                            "আপনি কেমন আছেন?",
                        ),
                        (
                            "আমি ভালো আছি (Ami bhalo achhi)",
                            "I am well",
                            "ধন্যবাদ, আমি ভালো আছি।",
                        ),
                        (
                            "আমার নাম… (Amar naam…)",
                            "My name is…",
                            "আমার নাম মায়া।",
                        ),
                        (
                            "ধন্যবাদ (Dhonnobad)",
                            "Thank you",
                            "আপনাকে ধন্যবাদ।",
                        ),
                    ),
                    "Present-tense introductions",
                    (
                        "আমি means ‘I’ and আমার means ‘my’. Bengali often "
                        "leaves out the English verb ‘is’: আমার নাম মায়া "
                        "literally means ‘my name Maya’."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            "Which phrase means ‘Hello’?",
                            "নমস্কার (Nomoshkar)",
                            (
                                "নমস্কার is a respectful, widely understood "
                                "greeting."
                            ),
                            options=[
                                "নমস্কার (Nomoshkar)",
                                "ধন্যবাদ (Dhonnobad)",
                                "বিদায় (Biday)",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            "Arrange: My name is Maya.",
                            "আমার নাম মায়া",
                            "আমার = my, নাম = name, মায়া = Maya.",
                            words=["মায়া", "আমার", "নাম"],
                        ),
                        _exercise(
                            "typing",
                            (
                                "Write ‘Thank you’ in Bengali or "
                                "transliteration."
                            ),
                            "ধন্যবাদ",
                            (
                                "ধন্যবাদ is commonly transliterated as "
                                "Dhonnobad or Dhanyabad."
                            ),
                            accepted_answers=[
                                "ধন্যবাদ",
                                "dhonnobad",
                                "dhanyabad",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "bn-1-2",
                    "Polite Essentials",
                    "🙏",
                    "Use polite words for everyday requests and responses.",
                    _vocabulary(
                        (
                            "দয়া করে (Doya kore)",
                            "Please",
                            "দয়া করে বসুন।",
                        ),
                        (
                            "হ্যাঁ (Hya)",
                            "Yes",
                            "হ্যাঁ, আমি যাব।",
                        ),
                        (
                            "না (Na)",
                            "No",
                            "না, ধন্যবাদ।",
                        ),
                        (
                            "মাফ করবেন (Maf korben)",
                            "Excuse me / Sorry",
                            "মাফ করবেন, স্টেশন কোথায়?",
                        ),
                        (
                            "সাহায্য (Shahajjo)",
                            "Help",
                            "আমার সাহায্য দরকার।",
                        ),
                    ),
                    "Making a polite request",
                    (
                        "Place দয়া করে before a request to mean ‘please’. "
                        "The ending করুন or করবেন makes many requests "
                        "respectful."
                    ),
                    [
                        _exercise(
                            "fill_blank",
                            (
                                "___, স্টেশন কোথায়? "
                                "(Excuse me, where is the station?)"
                            ),
                            "মাফ করবেন",
                            (
                                "মাফ করবেন politely gets someone’s "
                                "attention."
                            ),
                            accepted_answers=[
                                "মাফ করবেন",
                                "maf korben",
                            ],
                        ),
                        _exercise(
                            "multiple_choice",
                            "What does ‘দয়া করে’ mean?",
                            "Please",
                            (
                                "দয়া করে is used to make a request "
                                "polite."
                            ),
                            options=[
                                "Please",
                                "Goodbye",
                                "Water",
                            ],
                        ),
                        _exercise(
                            "typing",
                            "Write ‘No, thank you’ in Bengali.",
                            "না, ধন্যবাদ",
                            "না means no and ধন্যবাদ means thank you.",
                            accepted_answers=[
                                "না ধন্যবাদ",
                                "না, ধন্যবাদ",
                                "na dhonnobad",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "bn-1-3",
                    "Numbers and Questions",
                    "🔢",
                    "Count small amounts and ask basic questions.",
                    _vocabulary(
                        (
                            "এক (Ek)",
                            "One",
                            "এক কাপ চা।",
                        ),
                        (
                            "দুই (Dui)",
                            "Two",
                            "দুইটি বই।",
                        ),
                        (
                            "তিন (Tin)",
                            "Three",
                            "তিন জন মানুষ।",
                        ),
                        (
                            "কী? (Ki?)",
                            "What?",
                            "এটা কী?",
                        ),
                        (
                            "কত? (Koto?)",
                            "How much / How many?",
                            "এটার দাম কত?",
                        ),
                    ),
                    "Question words",
                    (
                        "কী asks ‘what’, while কত asks an amount or number. "
                        "A normal sentence becomes a question by using a "
                        "question word and rising tone."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            "Which word means ‘two’?",
                            "দুই (Dui)",
                            "এক = one, দুই = two, তিন = three.",
                            options=[
                                "এক (Ek)",
                                "দুই (Dui)",
                                "তিন (Tin)",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            "এটার দাম ___? (How much is this?)",
                            "কত",
                            (
                                "কত asks about price, quantity, or "
                                "number."
                            ),
                            accepted_answers=[
                                "কত",
                                "koto",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            "Arrange: What is this?",
                            "এটা কী",
                            "এটা means ‘this’ and কী means ‘what’.",
                            words=[
                                "কী",
                                "এটা",
                            ],
                        ),
                    ],
                ),
            ],
        },
        {
            "id": "bn-unit-2",
            "title": "Everyday Life",
            "icon": "🏠",
            "description": (
                "Talk about people, meals, and your daily routine."
            ),
            "lessons": [
                _lesson(
                    "bn-2-1",
                    "Family and People",
                    "👨‍👩‍👧",
                    (
                        "Identify family members and describe people "
                        "simply."
                    ),
                    _vocabulary(
                        (
                            "মা (Ma)",
                            "Mother",
                            "আমার মা বাড়িতে আছেন।",
                        ),
                        (
                            "বাবা (Baba)",
                            "Father",
                            "আমার বাবা কাজে আছেন।",
                        ),
                        (
                            "ভাই (Bhai)",
                            "Brother",
                            "আমার এক ভাই আছে।",
                        ),
                        (
                            "বোন (Bon)",
                            "Sister",
                            "আমার বোন পড়ছে।",
                        ),
                        (
                            "বন্ধু (Bondhu)",
                            "Friend",
                            "রাহুল আমার বন্ধু।",
                        ),
                    ),
                    "Possession with আমার",
                    (
                        "Put আমার before a person or thing to mean ‘my’: "
                        "আমার মা = my mother. Use আছে for ‘there is / have’ "
                        "and আছেন respectfully for a person’s location."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            "What does ‘আমার বোন’ mean?",
                            "My sister",
                            "আমার means my and বোন means sister.",
                            options=[
                                "My sister",
                                "My brother",
                                "My friend",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            (
                                "রাহুল আমার ___. "
                                "(Rahul is my friend.)"
                            ),
                            "বন্ধু",
                            "বন্ধু means friend.",
                            accepted_answers=[
                                "বন্ধু",
                                "bondhu",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            "Arrange: I have one brother.",
                            "আমার এক ভাই আছে",
                            (
                                "This literally says "
                                "‘my one brother exists’."
                            ),
                            words=[
                                "ভাই",
                                "আছে",
                                "আমার",
                                "এক",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "bn-2-2",
                    "Food and Ordering",
                    "🍛",
                    "Name common foods and order something politely.",
                    _vocabulary(
                        (
                            "জল (Jol)",
                            "Water",
                            "আমি জল চাই।",
                        ),
                        (
                            "চা (Cha)",
                            "Tea",
                            "এক কাপ চা দিন।",
                        ),
                        (
                            "ভাত (Bhat)",
                            "Cooked rice",
                            "আমি ভাত খাই।",
                        ),
                        (
                            "খাবার (Khabar)",
                            "Food / meal",
                            "খাবার খুব ভালো।",
                        ),
                        (
                            "চাই (Chai)",
                            "Want",
                            "আমি চা চাই।",
                        ),
                    ),
                    "Saying what you want",
                    (
                        "Use আমি + item + চাই to say ‘I want…’. For a "
                        "polite order, you can say item + দিন, meaning "
                        "‘please give’."
                    ),
                    [
                        _exercise(
                            "word_order",
                            "Arrange: I want tea.",
                            "আমি চা চাই",
                            "আমি = I, চা = tea, চাই = want.",
                            words=[
                                "চাই",
                                "আমি",
                                "চা",
                            ],
                        ),
                        _exercise(
                            "multiple_choice",
                            (
                                "Which sentence politely asks for one "
                                "cup of tea?"
                            ),
                            "এক কাপ চা দিন",
                            (
                                "দিন is a respectful way to ask someone "
                                "to give something."
                            ),
                            options=[
                                "এক কাপ চা দিন",
                                "চা কোথায়",
                                "আমি চা খাই না",
                            ],
                        ),
                        _exercise(
                            "typing",
                            "Write ‘I want water’ in Bengali.",
                            "আমি জল চাই",
                            "Use the pattern আমি + item + চাই.",
                            accepted_answers=[
                                "আমি জল চাই",
                                "ami jol chai",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "bn-2-3",
                    "Daily Routine",
                    "⏰",
                    "Describe simple activities in your day.",
                    _vocabulary(
                        (
                            "সকাল (Shokal)",
                            "Morning",
                            "আমি সকালে উঠি।",
                        ),
                        (
                            "উঠি (Uthi)",
                            "I wake up / get up",
                            "আমি সাতটায় উঠি।",
                        ),
                        (
                            "খাই (Khai)",
                            "I eat",
                            "আমি সকালে নাশতা খাই।",
                        ),
                        (
                            "যাই (Jai)",
                            "I go",
                            "আমি স্কুলে যাই।",
                        ),
                        (
                            "পড়ি (Pori)",
                            "I study / read",
                            "আমি বাংলা পড়ি।",
                        ),
                    ),
                    "First-person present verbs",
                    (
                        "Many first-person Bengali verbs end in ই: খাই "
                        "(I eat), যাই (I go), পড়ি (I study). Bengali "
                        "normally places the verb at the end."
                    ),
                    [
                        _exercise(
                            "fill_blank",
                            "আমি স্কুলে ___. (I go to school.)",
                            "যাই",
                            (
                                "যাই means ‘I go’ and comes at the "
                                "end."
                            ),
                            accepted_answers=[
                                "যাই",
                                "jai",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            "Arrange: I study Bengali.",
                            "আমি বাংলা পড়ি",
                            (
                                "Bengali word order usually keeps the "
                                "verb last."
                            ),
                            words=[
                                "পড়ি",
                                "বাংলা",
                                "আমি",
                            ],
                        ),
                        _exercise(
                            "multiple_choice",
                            "What does ‘আমি সকালে উঠি’ mean?",
                            "I get up in the morning",
                            (
                                "সকাল means morning and উঠি means "
                                "I get up."
                            ),
                            options=[
                                "I get up in the morning",
                                "I eat at night",
                                "I go to the market",
                            ],
                        ),
                    ],
                ),
            ],
        },
        {
            "id": "bn-unit-3",
            "title": "Bengali in the Real World",
            "icon": "🌏",
            "description": (
                "Travel, shop, and make short plans with confidence."
            ),
            "lessons": [
                _lesson(
                    "bn-3-1",
                    "Directions and Travel",
                    "🧭",
                    (
                        "Ask where places are and understand basic "
                        "directions."
                    ),
                    _vocabulary(
                        (
                            "কোথায়? (Kothay?)",
                            "Where?",
                            "স্টেশন কোথায়?",
                        ),
                        (
                            "ডানদিকে (Dandike)",
                            "To the right",
                            "ডানদিকে যান।",
                        ),
                        (
                            "বাঁদিকে (Bandike)",
                            "To the left",
                            "বাঁদিকে ঘুরুন।",
                        ),
                        (
                            "সোজা (Shoja)",
                            "Straight",
                            "সোজা যান।",
                        ),
                        (
                            "কাছে (Kachhe)",
                            "Near",
                            "হোটেলটি কাছে।",
                        ),
                    ),
                    "Asking where something is",
                    (
                        "Put কোথায় after a place to ask where it is: "
                        "স্টেশন কোথায়? Use যান for the polite command "
                        "‘go’."
                    ),
                    [
                        _exercise(
                            "word_order",
                            "Arrange: Where is the station?",
                            "স্টেশন কোথায়",
                            (
                                "The place comes first and কোথায় "
                                "comes last."
                            ),
                            words=[
                                "কোথায়",
                                "স্টেশন",
                            ],
                        ),
                        _exercise(
                            "multiple_choice",
                            "What does ‘সোজা যান’ mean?",
                            "Go straight",
                            (
                                "সোজা means straight and যান is the "
                                "polite form of go."
                            ),
                            options=[
                                "Go straight",
                                "Turn left",
                                "Stop here",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            "___ ঘুরুন। (Turn left.)",
                            "বাঁদিকে",
                            "বাঁদিকে means toward the left.",
                            accepted_answers=[
                                "বাঁদিকে",
                                "bandike",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "bn-3-2",
                    "Shopping and Prices",
                    "🛍️",
                    (
                        "Ask prices, choose an item, and make a simple "
                        "purchase."
                    ),
                    _vocabulary(
                        (
                            "দাম (Dam)",
                            "Price",
                            "এটার দাম কত?",
                        ),
                        (
                            "টাকা (Taka)",
                            "Taka / money",
                            "এটা একশো টাকা।",
                        ),
                        (
                            "সস্তা (Shosta)",
                            "Cheap",
                            "এটা সস্তা।",
                        ),
                        (
                            "দামি (Dami)",
                            "Expensive",
                            "ওটা খুব দামি।",
                        ),
                        (
                            "নেব (Nebo)",
                            "I will take",
                            "আমি এটা নেব।",
                        ),
                    ),
                    "Choosing an item",
                    (
                        "এটা means ‘this’ and ওটা means ‘that’. Use "
                        "আমি এটা নেব for ‘I’ll take this.’ খুব before "
                        "an adjective means ‘very’."
                    ),
                    [
                        _exercise(
                            "word_order",
                            "Arrange: How much is this?",
                            "এটার দাম কত",
                            (
                                "এটার = of this, দাম = price, "
                                "কত = how much."
                            ),
                            words=[
                                "কত",
                                "দাম",
                                "এটার",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            "আমি এটা ___. (I will take this.)",
                            "নেব",
                            "নেব means ‘I will take’.",
                            accepted_answers=[
                                "নেব",
                                "nebo",
                            ],
                        ),
                        _exercise(
                            "multiple_choice",
                            "Which word means ‘expensive’?",
                            "দামি (Dami)",
                            (
                                "দামি means expensive; "
                                "সস্তা means cheap."
                            ),
                            options=[
                                "দামি (Dami)",
                                "সস্তা (Shosta)",
                                "কাছে (Kachhe)",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "bn-3-3",
                    "Plans and Conversation",
                    "💬",
                    (
                        "Invite someone, choose a time, and close a "
                        "conversation."
                    ),
                    _vocabulary(
                        (
                            "আজ (Aj)",
                            "Today",
                            "আজ দেখা হবে।",
                        ),
                        (
                            "আগামীকাল (Agamikal)",
                            "Tomorrow",
                            "আগামীকাল যাব।",
                        ),
                        (
                            "কখন? (Kokhon?)",
                            "When?",
                            "আপনি কখন আসবেন?",
                        ),
                        (
                            "চলুন (Cholun)",
                            "Let’s go",
                            "চলুন, আমরা যাই।",
                        ),
                        (
                            "আবার দেখা হবে (Abar dekha hobe)",
                            "See you again",
                            "ভালো থাকবেন, আবার দেখা হবে।",
                        ),
                    ),
                    "Simple future expressions",
                    (
                        "Time words such as আজ and আগামীকাল usually "
                        "come near the beginning. Future verbs often end "
                        "in ব: যাব = will go, নেব = will take, "
                        "হবে = will be."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            "What does ‘আগামীকাল’ mean?",
                            "Tomorrow",
                            (
                                "আজ means today and আগামীকাল means "
                                "tomorrow."
                            ),
                            options=[
                                "Tomorrow",
                                "Yesterday",
                                "Morning",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            "Arrange: I will go tomorrow.",
                            "আমি আগামীকাল যাব",
                            (
                                "The future verb যাব comes at the "
                                "end."
                            ),
                            words=[
                                "যাব",
                                "আগামীকাল",
                                "আমি",
                            ],
                        ),
                        _exercise(
                            "typing",
                            (
                                "Write ‘See you again’ in Bengali or "
                                "transliteration."
                            ),
                            "আবার দেখা হবে",
                            (
                                "This is a friendly way to say you will "
                                "meet again."
                            ),
                            accepted_answers=[
                                "আবার দেখা হবে",
                                "abar dekha hobe",
                            ],
                        ),
                    ],
                ),
            ],
        },
    ],
}


def get_bengali_course():
    """Return a fresh copy of the Bengali course."""
    return deepcopy(BENGALI_COURSE)