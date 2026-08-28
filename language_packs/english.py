"""English Beginner course content for WordFluent."""

from copy import deepcopy


def _vocabulary(*items):
    return [
        {
            "term": term,
            "meaning": meaning,
            "example": example,
        }
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


ENGLISH_COURSE = {
    "language": "English",
    "level": "Beginner",
    "title": "English Foundations",
    "description": (
        "Build practical English for introductions, daily life, "
        "food, travel, and asking for help."
    ),
    "units": [
        {
            "id": "en_beginner_unit_1",
            "title": "First Conversations",
            "icon": "👋",
            "description": (
                "Greet people and begin a polite conversation."
            ),
            "lessons": [
                _lesson(
                    "en_beg_1_1",
                    "Hello and Goodbye",
                    "👋",
                    "Use greetings at the correct time of day.",
                    _vocabulary(
                        (
                            "Hello",
                            "A greeting that works at any time",
                            "Hello, Maya!",
                        ),
                        (
                            "Good morning",
                            "A greeting used earlier in the day",
                            "Good morning, Mr. Lee.",
                        ),
                        (
                            "Good evening",
                            "A greeting used later in the day",
                            "Good evening, everyone.",
                        ),
                        (
                            "Goodbye",
                            "A polite word used when leaving",
                            "Goodbye! See you tomorrow.",
                        ),
                        (
                            "See you later",
                            "An informal way to say goodbye",
                            "See you later, Ana.",
                        ),
                    ),
                    "Greetings",
                    (
                        "Use “Good morning” earlier in the day and "
                        "“Good evening” later in the day. “Hello” "
                        "works at almost any time."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            (
                                "Which greeting works at almost "
                                "any time?"
                            ),
                            "Hello",
                            "“Hello” is a general greeting.",
                            options=[
                                "Hello",
                                "Goodbye",
                                "Good night",
                                "See you later",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            (
                                "Good ___, Mr. Lee. "
                                "It is 8:00 a.m."
                            ),
                            "morning",
                            (
                                "We normally say “Good morning” "
                                "at 8:00 a.m."
                            ),
                            options=[
                                "morning",
                                "evening",
                                "bye",
                                "later",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            "Build a friendly goodbye.",
                            "See you later",
                            (
                                "“See you later” is a friendly, "
                                "informal goodbye."
                            ),
                            words=[
                                "later",
                                "See",
                                "you",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "en_beg_1_2",
                    "Introduce Yourself",
                    "🙂",
                    (
                        "Say your name and ask another "
                        "person’s name."
                    ),
                    _vocabulary(
                        (
                            "My name is...",
                            "A way to introduce your name",
                            "My name is Aisha.",
                        ),
                        (
                            "I am...",
                            "A shorter way to introduce yourself",
                            "I am Daniel.",
                        ),
                        (
                            "What is your name?",
                            "A question asking someone’s name",
                            "Hello. What is your name?",
                        ),
                        (
                            "Nice to meet you",
                            (
                                "A polite phrase after an "
                                "introduction"
                            ),
                            "Nice to meet you, Daniel.",
                        ),
                    ),
                    "The verb “to be”",
                    (
                        "Use “I am” for yourself and “you are” "
                        "for the person you are speaking to. "
                        "“I’m” is the short form of “I am.”"
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            (
                                "Which sentence introduces "
                                "your name?"
                            ),
                            "My name is Aisha.",
                            (
                                "“My name is...” directly "
                                "introduces your name."
                            ),
                            options=[
                                "My name is Aisha.",
                                "What is your name?",
                                "See you later.",
                                "You are welcome.",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            "I ___ Daniel.",
                            "am",
                            "Use “am” after the subject “I.”",
                            options=[
                                "am",
                                "is",
                                "are",
                                "be",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            "Build the question.",
                            "What is your name?",
                            (
                                "This is the standard question "
                                "for asking a name."
                            ),
                            words=[
                                "your",
                                "name?",
                                "What",
                                "is",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "en_beg_1_3",
                    "Polite Words",
                    "✨",
                    "Make simple requests sound respectful.",
                    _vocabulary(
                        (
                            "Please",
                            "A polite word used when asking",
                            "Please open the door.",
                        ),
                        (
                            "Thank you",
                            "A phrase showing appreciation",
                            "Thank you for your help.",
                        ),
                        (
                            "You’re welcome",
                            (
                                "A polite reply to "
                                "“Thank you”"
                            ),
                            "You’re welcome!",
                        ),
                        (
                            "Excuse me",
                            "A polite way to get attention",
                            (
                                "Excuse me, where is "
                                "the station?"
                            ),
                        ),
                        (
                            "Sorry",
                            "A word used to apologize",
                            "Sorry, I am late.",
                        ),
                    ),
                    "Polite requests",
                    (
                        "Add “please” to a request. Use "
                        "“excuse me” before interrupting or "
                        "asking a stranger a question."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            (
                                "What should you say after "
                                "someone helps you?"
                            ),
                            "Thank you",
                            "“Thank you” shows appreciation.",
                            options=[
                                "Thank you",
                                "Excuse me",
                                "Goodbye",
                                "My name is",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            (
                                "___ me, where is "
                                "the washroom?"
                            ),
                            "Excuse",
                            (
                                "“Excuse me” politely gets "
                                "someone’s attention."
                            ),
                            options=[
                                "Excuse",
                                "Thank",
                                "Welcome",
                                "Meet",
                            ],
                        ),
                        _exercise(
                            "typing",
                            (
                                "Type a polite request "
                                "for water."
                            ),
                            "Water, please.",
                            (
                                "Adding “please” makes the "
                                "request polite."
                            ),
                            accepted_answers=[
                                "Please give me water.",
                                "Can I have water, please?",
                                (
                                    "Could I have some water, "
                                    "please?"
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        },
        {
            "id": "en_beginner_unit_2",
            "title": "Daily Life",
            "icon": "🏠",
            "description": (
                "Talk about people, actions, and routines."
            ),
            "lessons": [
                _lesson(
                    "en_beg_2_1",
                    "People and Family",
                    "👨‍👩‍👧",
                    (
                        "Identify important people "
                        "in your life."
                    ),
                    _vocabulary(
                        (
                            "Family",
                            "People related to one another",
                            "My family lives in Calgary.",
                        ),
                        (
                            "Parent",
                            "A mother or father",
                            "My parent is at work.",
                        ),
                        (
                            "Brother",
                            "A male sibling",
                            "I have one brother.",
                        ),
                        (
                            "Sister",
                            "A female sibling",
                            "My sister is a student.",
                        ),
                        (
                            "Friend",
                            "A person you know and like",
                            "Sam is my friend.",
                        ),
                    ),
                    "Possessive words",
                    (
                        "Use “my” for something connected "
                        "to you and “your” for something "
                        "connected to the listener."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            (
                                "Which word means a "
                                "male sibling?"
                            ),
                            "Brother",
                            "A brother is a male sibling.",
                            options=[
                                "Brother",
                                "Sister",
                                "Parent",
                                "Friend",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            "Mina is ___ sister.",
                            "my",
                            (
                                "Use “my” for a person "
                                "connected to you."
                            ),
                            options=[
                                "my",
                                "I",
                                "me",
                                "mine is",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            "Build the sentence.",
                            "Sam is my friend.",
                            (
                                "The normal order is subject "
                                "+ verb + description."
                            ),
                            words=[
                                "friend.",
                                "Sam",
                                "my",
                                "is",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "en_beg_2_2",
                    "Everyday Actions",
                    "🚶",
                    (
                        "Describe common actions in "
                        "the present tense."
                    ),
                    _vocabulary(
                        (
                            "Eat",
                            "To have food",
                            "I eat breakfast at home.",
                        ),
                        (
                            "Drink",
                            "To have a liquid",
                            "I drink water.",
                        ),
                        (
                            "Work",
                            "To do a job",
                            "They work in an office.",
                        ),
                        (
                            "Study",
                            "To learn about a subject",
                            "We study English.",
                        ),
                        (
                            "Go",
                            "To move to another place",
                            "I go to school.",
                        ),
                    ),
                    "Simple present",
                    (
                        "Use the simple present for habits "
                        "and repeated actions. Example: "
                        "“I study every day.”"
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            (
                                "Which verb means to learn "
                                "about a subject?"
                            ),
                            "Study",
                            (
                                "To study means to spend "
                                "time learning."
                            ),
                            options=[
                                "Study",
                                "Drink",
                                "Go",
                                "Eat",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            (
                                "I ___ water every "
                                "morning."
                            ),
                            "drink",
                            (
                                "We use “drink” for water "
                                "and other liquids."
                            ),
                            options=[
                                "drink",
                                "eat",
                                "study",
                                "work",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            (
                                "Build the daily-routine "
                                "sentence."
                            ),
                            "I study English every day.",
                            (
                                "Time expressions often "
                                "come at the end."
                            ),
                            words=[
                                "day.",
                                "English",
                                "I",
                                "every",
                                "study",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "en_beg_2_3",
                    "Time and Routines",
                    "🕒",
                    (
                        "Say when everyday activities "
                        "happen."
                    ),
                    _vocabulary(
                        (
                            "Morning",
                            "The early part of the day",
                            "I work in the morning.",
                        ),
                        (
                            "Afternoon",
                            "The middle part of the day",
                            (
                                "We study in the "
                                "afternoon."
                            ),
                        ),
                        (
                            "Evening",
                            "The later part of the day",
                            "I cook in the evening.",
                        ),
                        (
                            "Today",
                            "The present day",
                            "I am busy today.",
                        ),
                        (
                            "Tomorrow",
                            "The day after today",
                            "See you tomorrow.",
                        ),
                    ),
                    "Time prepositions",
                    (
                        "Use “in” with parts of the day: "
                        "in the morning, in the afternoon, "
                        "and in the evening."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            (
                                "Which word means the day "
                                "after today?"
                            ),
                            "Tomorrow",
                            "Tomorrow is the next day.",
                            options=[
                                "Tomorrow",
                                "Today",
                                "Morning",
                                "Evening",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            (
                                "I study ___ the "
                                "afternoon."
                            ),
                            "in",
                            (
                                "Use “in” with "
                                "“the afternoon.”"
                            ),
                            options=[
                                "in",
                                "on",
                                "at",
                                "to",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            "Build the sentence.",
                            "I work in the morning.",
                            (
                                "Use “in the morning” "
                                "as the time phrase."
                            ),
                            words=[
                                "morning.",
                                "work",
                                "the",
                                "I",
                                "in",
                            ],
                        ),
                    ],
                ),
            ],
        },
        {
            "id": "en_beginner_unit_3",
            "title": "Real-Life English",
            "icon": "🌍",
            "description": (
                "Use English in common public situations."
            ),
            "lessons": [
                _lesson(
                    "en_beg_3_1",
                    "At a Café",
                    "☕",
                    "Order food and drinks politely.",
                    _vocabulary(
                        (
                            "Menu",
                            (
                                "A list of available food "
                                "and drinks"
                            ),
                            "May I see the menu?",
                        ),
                        (
                            "Water",
                            "A common clear drink",
                            "I would like some water.",
                        ),
                        (
                            "Coffee",
                            (
                                "A hot or cold drink made "
                                "from coffee beans"
                            ),
                            "One coffee, please.",
                        ),
                        (
                            "Bill",
                            "The amount you must pay",
                            (
                                "May I have the bill, "
                                "please?"
                            ),
                        ),
                        (
                            "I would like...",
                            (
                                "A polite phrase for "
                                "ordering"
                            ),
                            (
                                "I would like a "
                                "sandwich."
                            ),
                        ),
                    ),
                    "Polite ordering",
                    (
                        "Use “I would like...” instead of "
                        "“I want...” for a more polite order."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            (
                                "Which phrase is the "
                                "most polite order?"
                            ),
                            (
                                "I would like a coffee, "
                                "please."
                            ),
                            (
                                "“I would like...” and "
                                "“please” make a polite order."
                            ),
                            options=[
                                (
                                    "I would like a coffee, "
                                    "please."
                                ),
                                "Coffee now.",
                                "Give coffee.",
                                "I coffee.",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            "May I see the ___?",
                            "menu",
                            (
                                "A menu lists the café’s "
                                "food and drinks."
                            ),
                            options=[
                                "menu",
                                "station",
                                "morning",
                                "family",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            (
                                "Build a polite request "
                                "for the bill."
                            ),
                            (
                                "May I have the bill, "
                                "please?"
                            ),
                            (
                                "This is a common polite "
                                "request at a restaurant."
                            ),
                            words=[
                                "bill,",
                                "May",
                                "please?",
                                "the",
                                "I",
                                "have",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "en_beg_3_2",
                    "Asking for Directions",
                    "🗺️",
                    (
                        "Ask where a place is and understand "
                        "basic directions."
                    ),
                    _vocabulary(
                        (
                            "Where is...?",
                            (
                                "A question asking for "
                                "a location"
                            ),
                            "Where is the library?",
                        ),
                        (
                            "Left",
                            (
                                "The direction opposite "
                                "right"
                            ),
                            (
                                "Turn left at the "
                                "corner."
                            ),
                        ),
                        (
                            "Right",
                            (
                                "The direction opposite "
                                "left"
                            ),
                            (
                                "The bank is on the "
                                "right."
                            ),
                        ),
                        (
                            "Straight",
                            "Forward without turning",
                            (
                                "Go straight for "
                                "one block."
                            ),
                        ),
                        (
                            "Near",
                            "Not far away",
                            (
                                "The station is near "
                                "the hotel."
                            ),
                        ),
                    ),
                    "Location questions",
                    (
                        "Use “Where is...” for one place "
                        "and “Where are...” for more than "
                        "one place."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            (
                                "Which question asks "
                                "for a location?"
                            ),
                            "Where is the station?",
                            (
                                "“Where is...” asks about "
                                "the location of one place."
                            ),
                            options=[
                                "Where is the station?",
                                "What is your name?",
                                "How old are you?",
                                (
                                    "Would you like "
                                    "coffee?"
                                ),
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            (
                                "Go ___ for one "
                                "block."
                            ),
                            "straight",
                            (
                                "“Go straight” means "
                                "continue forward."
                            ),
                            options=[
                                "straight",
                                "near",
                                "name",
                                "please",
                            ],
                        ),
                        _exercise(
                            "word_order",
                            "Build the direction.",
                            "Turn left at the corner.",
                            (
                                "The direction begins with "
                                "the action “Turn.”"
                            ),
                            words=[
                                "corner.",
                                "left",
                                "Turn",
                                "the",
                                "at",
                            ],
                        ),
                    ],
                ),
                _lesson(
                    "en_beg_3_3",
                    "Getting Help",
                    "🆘",
                    (
                        "Ask for help and explain "
                        "a simple problem."
                    ),
                    _vocabulary(
                        (
                            "Help",
                            "Support given to someone",
                            "Can you help me?",
                        ),
                        (
                            "I need...",
                            (
                                "A phrase expressing "
                                "something necessary"
                            ),
                            "I need a doctor.",
                        ),
                        (
                            "I don’t understand",
                            (
                                "A phrase used when "
                                "something is unclear"
                            ),
                            (
                                "Sorry, I don’t "
                                "understand."
                            ),
                        ),
                        (
                            "Please repeat",
                            (
                                "A request asking someone "
                                "to say it again"
                            ),
                            (
                                "Please repeat that "
                                "slowly."
                            ),
                        ),
                        (
                            "Emergency",
                            (
                                "A serious situation needing "
                                "immediate help"
                            ),
                            (
                                "This is an "
                                "emergency."
                            ),
                        ),
                    ),
                    "Can for requests",
                    (
                        "Use “Can you...?” for a simple "
                        "request. Add “please” to make "
                        "the request more polite."
                    ),
                    [
                        _exercise(
                            "multiple_choice",
                            (
                                "What can you say when "
                                "speech is unclear?"
                            ),
                            "Please repeat.",
                            (
                                "“Please repeat” asks the "
                                "speaker to say it again."
                            ),
                            options=[
                                "Please repeat.",
                                "Good evening.",
                                "One coffee.",
                                "Turn right.",
                            ],
                        ),
                        _exercise(
                            "fill_blank",
                            "Can you ___ me?",
                            "help",
                            (
                                "“Can you help me?” is a "
                                "direct request for support."
                            ),
                            options=[
                                "help",
                                "meet",
                                "drink",
                                "morning",
                            ],
                        ),
                        _exercise(
                            "typing",
                            (
                                "Type a sentence asking "
                                "someone to repeat slowly."
                            ),
                            (
                                "Please repeat that "
                                "slowly."
                            ),
                            (
                                "This politely asks the "
                                "speaker to say it again "
                                "slowly."
                            ),
                            accepted_answers=[
                                (
                                    "Can you repeat that "
                                    "slowly, please?"
                                ),
                                (
                                    "Please say that "
                                    "again slowly."
                                ),
                                (
                                    "Could you repeat that "
                                    "slowly, please?"
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        },
    ],
}


def get_english_course():
    """Return a copy that the game can safely use."""
    return deepcopy(ENGLISH_COURSE)