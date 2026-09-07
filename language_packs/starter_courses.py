"""Starter learning paths for WordFluent's additional languages."""

from copy import deepcopy
from language_packs.expanded_lessons import get_extra_lessons

def _vocabulary(*items):
    return [
        {
            "term": term,
            "pronunciation": pronunciation,
            "meaning": meaning,
            "example": example,
            "example_meaning": example_meaning,
        }
        for (
            term,
            pronunciation,
            meaning,
            example,
            example_meaning,
        ) in items
    ]


def _choice(prompt, answer, explanation, options):
    return {
        "type": "multiple_choice",
        "prompt": prompt,
        "answer": answer,
        "explanation": explanation,
        "options": options,
        "words": [],
        "accepted_answers": [],
    }


def _order(
    prompt,
    answer,
    explanation,
    words,
    accepted_answers=None,
):
    return {
        "type": "word_order",
        "prompt": prompt,
        "answer": answer,
        "explanation": explanation,
        "options": [],
        "words": words,
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


def _course(
    language,
    code,
    native_name,
    title,
    description,
    lessons,
):
    return {
        "language": language,
        "language_code": code,
        "native_name": native_name,
        "level": "Beginner",
        "title": title,
        "description": description,
        "units": [
            {
                "id": f"{code.lower()}-starter-unit",
                "title": "Everyday Foundations",
                "icon": "🌱",
                "description": (
                    "Start with greetings, introductions, "
                    "and useful everyday phrases."
                ),
                "lessons": lessons,
            }
        ],
    }


FRENCH_COURSE = _course(
    "French",
    "FR",
    "Français",
    "French Foundations",
    "Build a practical French foundation for simple conversations.",
    [
        _lesson(
            "fr-beg-1",
            "Greetings and Politeness",
            "👋",
            "Greet someone and use polite everyday expressions.",
            _vocabulary(
                (
                    "Bonjour",
                    "bohn-ZHOOR",
                    "Hello or good morning",
                    "Bonjour, Madame !",
                    "Hello, ma'am!",
                ),
                (
                    "Bonsoir",
                    "bohn-SWAHR",
                    "Good evening",
                    "Bonsoir, Monsieur !",
                    "Good evening, sir!",
                ),
                (
                    "Au revoir",
                    "oh ruh-VWAHR",
                    "Goodbye",
                    "Au revoir, à demain !",
                    "Goodbye, see you tomorrow!",
                ),
                (
                    "S'il vous plaît",
                    "seel voo PLEH",
                    "Please — polite",
                    "Un café, s'il vous plaît.",
                    "A coffee, please.",
                ),
                (
                    "Merci",
                    "mehr-SEE",
                    "Thank you",
                    "Merci beaucoup !",
                    "Thank you very much!",
                ),
            ),
            "Polite French",
            (
                "Use bonjour during the day and bonsoir in the "
                "evening. S'il vous plaît is the polite form of please."
            ),
            [
                _choice(
                    "Which French word means ‘Thank you’?",
                    "Merci",
                    "Merci is the everyday way to say thank you.",
                    ["Bonsoir", "Merci", "Bonjour", "Au revoir"],
                ),
                _choice(
                    "Which phrase is a polite way to say ‘Please’?",
                    "S'il vous plaît",
                    "Use s'il vous plaît in polite situations.",
                    ["Merci", "Au revoir", "S'il vous plaît", "Bonsoir"],
                ),
                _order(
                    "Arrange: A coffee, please.",
                    "Un café s'il vous plaît",
                    "The item comes before the polite phrase.",
                    ["s'il", "Un", "plaît", "café", "vous"],
                ),
            ],
        ),
        _lesson(
            "fr-beg-2",
            "Introduce Yourself",
            "🙂",
            "Say your name and meet someone politely.",
            _vocabulary(
                (
                    "Je m'appelle…",
                    "zhuh mah-PELL",
                    "My name is…",
                    "Je m'appelle Maya.",
                    "My name is Maya.",
                ),
                (
                    "Comment vous appelez-vous ?",
                    "koh-MAHN voo zah-play VOO",
                    "What is your name? — polite",
                    "Bonjour, comment vous appelez-vous ?",
                    "Hello, what is your name?",
                ),
                (
                    "Oui",
                    "wee",
                    "Yes",
                    "Oui, bien sûr.",
                    "Yes, of course.",
                ),
                (
                    "Non",
                    "nohn",
                    "No",
                    "Non, merci.",
                    "No, thank you.",
                ),
                (
                    "Enchanté",
                    "ahn-shahn-TAY",
                    "Nice to meet you",
                    "Enchanté de vous rencontrer.",
                    "Nice to meet you.",
                ),
            ),
            "The phrase je m'appelle",
            (
                "Je means I. The phrase je m'appelle is the natural "
                "way to say ‘my name is’ in French."
            ),
            [
                _choice(
                    "How do you begin saying your name in French?",
                    "Je m'appelle…",
                    "Je m'appelle is followed by your name.",
                    ["Oui", "Enchanté", "Je m'appelle…", "Non"],
                ),
                _choice(
                    "Which word means ‘Yes’?",
                    "Oui",
                    "Oui means yes, while non means no.",
                    ["Non", "Oui", "Merci", "Bonsoir"],
                ),
                _order(
                    "Arrange: My name is Maya.",
                    "Je m'appelle Maya",
                    "Put the name after je m'appelle.",
                    ["Maya", "m'appelle", "Je"],
                ),
            ],
        ),
        _lesson(
            "fr-beg-3",
            "Everyday Essentials",
            "🧭",
            "Ask for basic things and understand useful signs.",
            _vocabulary(
                (
                    "De l'eau",
                    "duh LOH",
                    "Some water",
                    "Je voudrais de l'eau.",
                    "I would like some water.",
                ),
                (
                    "À manger",
                    "ah mahn-ZHAY",
                    "Something to eat",
                    "Je voudrais à manger.",
                    "I would like something to eat.",
                ),
                (
                    "Les toilettes",
                    "lay twah-LET",
                    "The restroom",
                    "Où sont les toilettes ?",
                    "Where is the restroom?",
                ),
                (
                    "Aidez-moi",
                    "ay-day MWAH",
                    "Help me",
                    "Aidez-moi, s'il vous plaît.",
                    "Help me, please.",
                ),
                (
                    "Combien ça coûte ?",
                    "kohm-BYAN sah KOOT",
                    "How much does it cost?",
                    "Combien ça coûte ?",
                    "How much does it cost?",
                ),
            ),
            "Polite requests",
            (
                "Je voudrais means ‘I would like’. It is a useful, "
                "polite beginning when ordering or asking for something."
            ),
            [
                _choice(
                    "Which phrase asks the price?",
                    "Combien ça coûte ?",
                    "Combien ça coûte asks how much something costs.",
                    [
                        "Aidez-moi",
                        "De l'eau",
                        "Combien ça coûte ?",
                        "À manger",
                    ],
                ),
                _choice(
                    "Which phrase means ‘Help me’?",
                    "Aidez-moi",
                    "Aidez-moi is a direct request for help.",
                    [
                        "Aidez-moi",
                        "Les toilettes",
                        "De l'eau",
                        "Merci",
                    ],
                ),
                _order(
                    "Arrange: I would like some water.",
                    "Je voudrais de l'eau",
                    "Je voudrais begins a polite request.",
                    ["l'eau", "voudrais", "de", "Je"],
                ),
            ],
        ),
    ],
)


SPANISH_COURSE = _course(
    "Spanish",
    "ES",
    "Español",
    "Spanish Foundations",
    "Build a practical Spanish foundation for simple conversations.",
    [
        _lesson(
            "es-beg-1",
            "Greetings and Politeness",
            "👋",
            "Greet someone and use polite everyday expressions.",
            _vocabulary(
                (
                    "Hola",
                    "OH-lah",
                    "Hello",
                    "¡Hola, Ana!",
                    "Hello, Ana!",
                ),
                (
                    "Buenos días",
                    "BWEH-nohs DEE-ahs",
                    "Good morning",
                    "Buenos días, señor.",
                    "Good morning, sir.",
                ),
                (
                    "Adiós",
                    "ah-DYOHS",
                    "Goodbye",
                    "Adiós, hasta mañana.",
                    "Goodbye, see you tomorrow.",
                ),
                (
                    "Por favor",
                    "por fah-VOR",
                    "Please",
                    "Agua, por favor.",
                    "Water, please.",
                ),
                (
                    "Gracias",
                    "GRAH-syahs",
                    "Thank you",
                    "Muchas gracias.",
                    "Thank you very much.",
                ),
            ),
            "Everyday politeness",
            (
                "Hola works at any time. Buenos días is used in the "
                "morning. Add por favor to make a request polite."
            ),
            [
                _choice(
                    "Which Spanish word means ‘Thank you’?",
                    "Gracias",
                    "Gracias is the everyday way to say thank you.",
                    ["Hola", "Adiós", "Gracias", "Buenos días"],
                ),
                _choice(
                    "Which phrase means ‘Please’?",
                    "Por favor",
                    "Por favor makes a request polite.",
                    ["Gracias", "Por favor", "Adiós", "Hola"],
                ),
                _order(
                    "Arrange: Water, please.",
                    "Agua por favor",
                    "Put por favor after the thing you request.",
                    ["favor", "Agua", "por"],
                ),
            ],
        ),
        _lesson(
            "es-beg-2",
            "Introduce Yourself",
            "🙂",
            "Say your name and meet someone politely.",
            _vocabulary(
                (
                    "Me llamo…",
                    "meh YAH-moh",
                    "My name is…",
                    "Me llamo Maya.",
                    "My name is Maya.",
                ),
                (
                    "¿Cómo te llamas?",
                    "KOH-moh teh YAH-mahs",
                    "What is your name?",
                    "Hola, ¿cómo te llamas?",
                    "Hello, what is your name?",
                ),
                (
                    "Sí",
                    "see",
                    "Yes",
                    "Sí, claro.",
                    "Yes, of course.",
                ),
                (
                    "No",
                    "noh",
                    "No",
                    "No, gracias.",
                    "No, thank you.",
                ),
                (
                    "Mucho gusto",
                    "MOO-choh GOOS-toh",
                    "Nice to meet you",
                    "Mucho gusto, Maya.",
                    "Nice to meet you, Maya.",
                ),
            ),
            "The phrase me llamo",
            (
                "Use me llamo followed by your name. Cómo te llamas "
                "asks another person what their name is."
            ),
            [
                _choice(
                    "How do you begin saying your name in Spanish?",
                    "Me llamo…",
                    "Me llamo is followed by your name.",
                    ["No", "Mucho gusto", "Me llamo…", "Sí"],
                ),
                _choice(
                    "Which word means ‘Yes’?",
                    "Sí",
                    "Sí means yes, while no means no.",
                    ["No", "Sí", "Hola", "Gracias"],
                ),
                _order(
                    "Arrange: My name is Maya.",
                    "Me llamo Maya",
                    "Put the name after me llamo.",
                    ["Maya", "llamo", "Me"],
                ),
            ],
        ),
        _lesson(
            "es-beg-3",
            "Everyday Essentials",
            "🧭",
            "Ask for basic things and understand useful signs.",
            _vocabulary(
                (
                    "Agua",
                    "AH-gwah",
                    "Water",
                    "Quisiera agua.",
                    "I would like water.",
                ),
                (
                    "Comida",
                    "koh-MEE-dah",
                    "Food",
                    "Necesito comida.",
                    "I need food.",
                ),
                (
                    "El baño",
                    "el BAH-nyoh",
                    "The restroom",
                    "¿Dónde está el baño?",
                    "Where is the restroom?",
                ),
                (
                    "Ayúdeme",
                    "ah-YOO-deh-meh",
                    "Help me — polite",
                    "Ayúdeme, por favor.",
                    "Help me, please.",
                ),
                (
                    "¿Cuánto cuesta?",
                    "KWAHN-toh KWEHS-tah",
                    "How much does it cost?",
                    "¿Cuánto cuesta esto?",
                    "How much does this cost?",
                ),
            ),
            "Polite requests",
            (
                "Quisiera means ‘I would like’. Use it before an item "
                "to make a polite request."
            ),
            [
                _choice(
                    "Which phrase asks the price?",
                    "¿Cuánto cuesta?",
                    "Cuánto cuesta asks how much something costs.",
                    [
                        "Ayúdeme",
                        "Agua",
                        "¿Cuánto cuesta?",
                        "Comida",
                    ],
                ),
                _choice(
                    "Which word means ‘Water’?",
                    "Agua",
                    "Agua means water.",
                    ["Comida", "Agua", "El baño", "Gracias"],
                ),
                _order(
                    "Arrange: I would like water.",
                    "Quisiera agua",
                    "Put the requested item after quisiera.",
                    ["agua", "Quisiera"],
                ),
            ],
        ),
    ],
)


HINDI_COURSE = _course(
    "Hindi",
    "HI",
    "हिन्दी",
    "हिन्दी की शुरुआत — Hindi Foundations",
    "Learn useful Hindi in Devanagari with easy transliteration.",
    [
        _lesson(
            "hi-beg-1",
            "Greetings and Politeness",
            "👋",
            "Greet someone and use polite everyday expressions.",
            _vocabulary(
                (
                    "नमस्ते",
                    "Namaste",
                    "Hello",
                    "नमस्ते, आप कैसे हैं?",
                    "Hello, how are you?",
                ),
                (
                    "सुप्रभात",
                    "Suprabhaat",
                    "Good morning",
                    "सुप्रभात, माँ।",
                    "Good morning, Mom.",
                ),
                (
                    "अलविदा",
                    "Alvida",
                    "Goodbye",
                    "अलविदा, फिर मिलेंगे।",
                    "Goodbye, see you again.",
                ),
                (
                    "कृपया",
                    "Kripaya",
                    "Please",
                    "कृपया बैठिए।",
                    "Please sit.",
                ),
                (
                    "धन्यवाद",
                    "Dhanyavaad",
                    "Thank you",
                    "आपका धन्यवाद।",
                    "Thank you.",
                ),
            ),
            "Respectful greetings",
            (
                "Namaste is a respectful greeting that works in many "
                "situations. Kripaya makes a request polite."
            ),
            [
                _choice(
                    "Which Hindi word means ‘Thank you’?",
                    "धन्यवाद",
                    "धन्यवाद means thank you.",
                    ["नमस्ते", "कृपया", "धन्यवाद", "अलविदा"],
                ),
                _choice(
                    "Which Hindi word means ‘Please’?",
                    "कृपया",
                    "कृपया is used for polite requests.",
                    ["धन्यवाद", "कृपया", "सुप्रभात", "अलविदा"],
                ),
                _order(
                    "Arrange: Please sit.",
                    "कृपया बैठिए",
                    "The polite word comes before the request.",
                    ["बैठिए", "कृपया"],
                    ["kripaya baithiye"],
                ),
            ],
        ),
        _lesson(
            "hi-beg-2",
            "Introduce Yourself",
            "🙂",
            "Say your name and meet someone politely.",
            _vocabulary(
                (
                    "मेरा नाम… है",
                    "Mera naam… hai",
                    "My name is…",
                    "मेरा नाम माया है।",
                    "My name is Maya.",
                ),
                (
                    "आपका नाम क्या है?",
                    "Aapka naam kya hai?",
                    "What is your name? — polite",
                    "नमस्ते, आपका नाम क्या है?",
                    "Hello, what is your name?",
                ),
                (
                    "हाँ",
                    "Haan",
                    "Yes",
                    "हाँ, ज़रूर।",
                    "Yes, certainly.",
                ),
                (
                    "नहीं",
                    "Nahin",
                    "No",
                    "नहीं, धन्यवाद।",
                    "No, thank you.",
                ),
                (
                    "आपसे मिलकर खुशी हुई",
                    "Aapse milkar khushi hui",
                    "Nice to meet you",
                    "आपसे मिलकर खुशी हुई।",
                    "Nice to meet you.",
                ),
            ),
            "Using मेरा नाम",
            (
                "मेरा नाम means ‘my name’. Put your name before है "
                "to complete the introduction."
            ),
            [
                _choice(
                    "Which phrase begins ‘My name is…’?",
                    "मेरा नाम… है",
                    "Use मेरा नाम followed by your name and है.",
                    ["हाँ", "नहीं", "मेरा नाम… है", "धन्यवाद"],
                ),
                _choice(
                    "Which Hindi word means ‘Yes’?",
                    "हाँ",
                    "हाँ means yes, while नहीं means no.",
                    ["नहीं", "हाँ", "कृपया", "नमस्ते"],
                ),
                _order(
                    "Arrange: My name is Maya.",
                    "मेरा नाम माया है",
                    "Hindi normally places है at the end.",
                    ["है", "माया", "मेरा", "नाम"],
                    ["mera naam maya hai"],
                ),
            ],
        ),
        _lesson(
            "hi-beg-3",
            "Everyday Essentials",
            "🧭",
            "Ask for basic things and understand useful words.",
            _vocabulary(
                (
                    "पानी",
                    "Paani",
                    "Water",
                    "मुझे पानी चाहिए।",
                    "I need water.",
                ),
                (
                    "खाना",
                    "Khaana",
                    "Food",
                    "खाना तैयार है।",
                    "The food is ready.",
                ),
                (
                    "शौचालय",
                    "Shauchalaya",
                    "Restroom",
                    "शौचालय कहाँ है?",
                    "Where is the restroom?",
                ),
                (
                    "मेरी मदद कीजिए",
                    "Meri madad kijiye",
                    "Please help me",
                    "कृपया मेरी मदद कीजिए।",
                    "Please help me.",
                ),
                (
                    "यह कितने का है?",
                    "Yah kitne ka hai?",
                    "How much is this?",
                    "यह कितने का है?",
                    "How much is this?",
                ),
            ),
            "Saying what you need",
            (
                "मुझे means ‘to me’ and चाहिए means ‘is needed’. Put "
                "the thing you need between them."
            ),
            [
                _choice(
                    "Which Hindi word means ‘Water’?",
                    "पानी",
                    "पानी means water.",
                    ["खाना", "पानी", "शौचालय", "धन्यवाद"],
                ),
                _choice(
                    "Which phrase asks the price?",
                    "यह कितने का है?",
                    "यह कितने का है asks how much this is.",
                    [
                        "मेरी मदद कीजिए",
                        "यह कितने का है?",
                        "पानी",
                        "खाना",
                    ],
                ),
                _order(
                    "Arrange: I need water.",
                    "मुझे पानी चाहिए",
                    "The thing needed goes before चाहिए.",
                    ["चाहिए", "पानी", "मुझे"],
                    ["mujhe paani chahiye"],
                ),
            ],
        ),
    ],
)


KOREAN_COURSE = _course(
    "Korean",
    "KO",
    "한국어",
    "한국어 시작 — Korean Foundations",
    "Learn useful Korean in Hangul with easy romanization.",
    [
        _lesson(
            "ko-beg-1",
            "Greetings and Politeness",
            "👋",
            "Greet someone and use polite everyday expressions.",
            _vocabulary(
                (
                    "안녕하세요",
                    "Annyeonghaseyo",
                    "Hello — polite",
                    "안녕하세요, 민지 씨.",
                    "Hello, Minji.",
                ),
                (
                    "안녕히 가세요",
                    "Annyeonghi gaseyo",
                    "Goodbye — to someone leaving",
                    "안녕히 가세요!",
                    "Goodbye!",
                ),
                (
                    "부탁합니다",
                    "Butakhamnida",
                    "Please / I ask a favour",
                    "잘 부탁합니다.",
                    "Please take good care of me.",
                ),
                (
                    "감사합니다",
                    "Gamsahamnida",
                    "Thank you — polite",
                    "정말 감사합니다.",
                    "Thank you very much.",
                ),
                (
                    "괜찮아요",
                    "Gwaenchanayo",
                    "It is okay / I am okay",
                    "네, 괜찮아요.",
                    "Yes, I am okay.",
                ),
            ),
            "Polite 요 and 니다 endings",
            (
                "Many polite Korean expressions end in 요 or 니다. "
                "These forms are safe choices with people you do not "
                "know well."
            ),
            [
                _choice(
                    "Which Korean phrase means ‘Thank you’?",
                    "감사합니다",
                    "감사합니다 is a polite way to say thank you.",
                    [
                        "안녕하세요",
                        "감사합니다",
                        "괜찮아요",
                        "안녕히 가세요",
                    ],
                ),
                _choice(
                    "Which phrase is a polite hello?",
                    "안녕하세요",
                    "안녕하세요 is the standard polite greeting.",
                    [
                        "괜찮아요",
                        "부탁합니다",
                        "안녕하세요",
                        "감사합니다",
                    ],
                ),
                _order(
                    "Arrange: Yes, I am okay.",
                    "네 괜찮아요",
                    "네 means yes and comes before 괜찮아요.",
                    ["괜찮아요", "네"],
                    ["ne gwaenchanayo"],
                ),
            ],
        ),
        _lesson(
            "ko-beg-2",
            "Introduce Yourself",
            "🙂",
            "Say your name and meet someone politely.",
            _vocabulary(
                (
                    "제 이름은…입니다",
                    "Je ireumeun…imnida",
                    "My name is…",
                    "제 이름은 마야입니다.",
                    "My name is Maya.",
                ),
                (
                    "이름이 뭐예요?",
                    "Ireumi mwoyeyo?",
                    "What is your name?",
                    "이름이 뭐예요?",
                    "What is your name?",
                ),
                (
                    "네",
                    "Ne",
                    "Yes",
                    "네, 맞아요.",
                    "Yes, that is right.",
                ),
                (
                    "아니요",
                    "Aniyo",
                    "No",
                    "아니요, 괜찮아요.",
                    "No, it is okay.",
                ),
                (
                    "만나서 반가워요",
                    "Mannaseo bangawoyo",
                    "Nice to meet you",
                    "만나서 반가워요!",
                    "Nice to meet you!",
                ),
            ),
            "The topic marker 은",
            (
                "In 제 이름은, 제 means ‘my’, 이름 means ‘name’, and "
                "은 marks the name as the topic."
            ),
            [
                _choice(
                    "Which phrase begins ‘My name is…’?",
                    "제 이름은…입니다",
                    "Place your name before 입니다.",
                    [
                        "네",
                        "아니요",
                        "제 이름은…입니다",
                        "만나서 반가워요",
                    ],
                ),
                _choice(
                    "Which Korean word means ‘No’?",
                    "아니요",
                    "아니요 means no, while 네 means yes.",
                    [
                        "네",
                        "아니요",
                        "감사합니다",
                        "안녕하세요",
                    ],
                ),
                _order(
                    "Arrange: My name is Maya.",
                    "제 이름은 마야입니다",
                    "The name comes before 입니다.",
                    ["마야입니다", "이름은", "제"],
                    ["je ireumeun maya imnida"],
                ),
            ],
        ),
        _lesson(
            "ko-beg-3",
            "Everyday Essentials",
            "🧭",
            "Ask for basic things and understand useful words.",
            _vocabulary(
                (
                    "물",
                    "Mul",
                    "Water",
                    "물 주세요.",
                    "Please give me water.",
                ),
                (
                    "음식",
                    "Eumsik",
                    "Food",
                    "음식이 맛있어요.",
                    "The food is delicious.",
                ),
                (
                    "화장실",
                    "Hwajangsil",
                    "Restroom",
                    "화장실이 어디예요?",
                    "Where is the restroom?",
                ),
                (
                    "도와주세요",
                    "Dowajuseyo",
                    "Please help me",
                    "저를 도와주세요.",
                    "Please help me.",
                ),
                (
                    "얼마예요?",
                    "Eolmayeyo?",
                    "How much is it?",
                    "이거 얼마예요?",
                    "How much is this?",
                ),
            ),
            "Polite requests with 주세요",
            (
                "주세요 means ‘please give me’. Put the item before "
                "주세요 to ask for it politely."
            ),
            [
                _choice(
                    "Which Korean word means ‘Water’?",
                    "물",
                    "물 means water.",
                    ["음식", "물", "화장실", "감사합니다"],
                ),
                _choice(
                    "Which phrase asks the price?",
                    "얼마예요?",
                    "얼마예요 asks how much something is.",
                    [
                        "도와주세요",
                        "얼마예요?",
                        "물",
                        "음식",
                    ],
                ),
                _order(
                    "Arrange: Please give me water.",
                    "물 주세요",
                    "Put the requested item before 주세요.",
                    ["주세요", "물"],
                    ["mul juseyo"],
                ),
            ],
        ),
    ],
)


JAPANESE_COURSE = _course(
    "Japanese",
    "JA",
    "日本語",
    "日本語の基礎 — Japanese Foundations",
    "Learn useful Japanese with script and easy romanization.",
    [
        _lesson(
            "ja-beg-1",
            "Greetings and Politeness",
            "👋",
            "Greet someone and use polite everyday expressions.",
            _vocabulary(
                (
                    "こんにちは",
                    "Konnichiwa",
                    "Hello / good afternoon",
                    "こんにちは、ゆきさん。",
                    "Hello, Yuki.",
                ),
                (
                    "おはようございます",
                    "Ohayou gozaimasu",
                    "Good morning — polite",
                    "おはようございます、先生。",
                    "Good morning, teacher.",
                ),
                (
                    "さようなら",
                    "Sayounara",
                    "Goodbye",
                    "さようなら、また明日。",
                    "Goodbye, see you tomorrow.",
                ),
                (
                    "お願いします",
                    "Onegaishimasu",
                    "Please / I request this",
                    "水をお願いします。",
                    "Water, please.",
                ),
                (
                    "ありがとうございます",
                    "Arigatou gozaimasu",
                    "Thank you — polite",
                    "どうもありがとうございます。",
                    "Thank you very much.",
                ),
            ),
            "Polite expressions",
            (
                "ございます makes greetings and thanks more polite. "
                "お願いします is useful when requesting something."
            ),
            [
                _choice(
                    "Which Japanese phrase means ‘Thank you’?",
                    "ありがとうございます",
                    "ありがとうございます is a polite way to say thank you.",
                    [
                        "こんにちは",
                        "お願いします",
                        "ありがとうございます",
                        "さようなら",
                    ],
                ),
                _choice(
                    "Which phrase means ‘Good morning’?",
                    "おはようございます",
                    "おはようございます is a polite morning greeting.",
                    [
                        "さようなら",
                        "こんにちは",
                        "おはようございます",
                        "お願いします",
                    ],
                ),
                _order(
                    "Arrange: Water, please.",
                    "水をお願いします",
                    "Use を after the requested item.",
                    ["お願いします", "を", "水"],
                    ["mizu o onegaishimasu"],
                ),
            ],
        ),
        _lesson(
            "ja-beg-2",
            "Introduce Yourself",
            "🙂",
            "Say your name and meet someone politely.",
            _vocabulary(
                (
                    "私の名前は…です",
                    "Watashi no namae wa…desu",
                    "My name is…",
                    "私の名前はマヤです。",
                    "My name is Maya.",
                ),
                (
                    "お名前は何ですか？",
                    "Onamae wa nan desu ka?",
                    "What is your name? — polite",
                    "お名前は何ですか？",
                    "What is your name?",
                ),
                (
                    "はい",
                    "Hai",
                    "Yes",
                    "はい、そうです。",
                    "Yes, that is right.",
                ),
                (
                    "いいえ",
                    "Iie",
                    "No",
                    "いいえ、違います。",
                    "No, that is different.",
                ),
                (
                    "はじめまして",
                    "Hajimemashite",
                    "Nice to meet you — first meeting",
                    "はじめまして、マヤです。",
                    "Nice to meet you, I am Maya.",
                ),
            ),
            "The pattern X は Y です",
            (
                "は marks the topic and です completes a polite "
                "statement. In this use, は is pronounced ‘wa’."
            ),
            [
                _choice(
                    "Which phrase begins ‘My name is…’?",
                    "私の名前は…です",
                    "Put your name before です.",
                    [
                        "はい",
                        "いいえ",
                        "私の名前は…です",
                        "はじめまして",
                    ],
                ),
                _choice(
                    "Which Japanese word means ‘No’?",
                    "いいえ",
                    "いいえ means no, while はい means yes.",
                    [
                        "はい",
                        "いいえ",
                        "こんにちは",
                        "さようなら",
                    ],
                ),
                _order(
                    "Arrange: My name is Maya.",
                    "私の名前はマヤです",
                    "The name comes before です.",
                    ["マヤ", "です", "私", "の", "名前", "は"],
                    ["watashi no namae wa maya desu"],
                ),
            ],
        ),
        _lesson(
            "ja-beg-3",
            "Everyday Essentials",
            "🧭",
            "Ask for basic things and understand useful words.",
            _vocabulary(
                (
                    "水",
                    "Mizu",
                    "Water",
                    "水をください。",
                    "Water, please.",
                ),
                (
                    "食べ物",
                    "Tabemono",
                    "Food",
                    "食べ物があります。",
                    "There is food.",
                ),
                (
                    "トイレ",
                    "Toire",
                    "Restroom",
                    "トイレはどこですか？",
                    "Where is the restroom?",
                ),
                (
                    "助けてください",
                    "Tasukete kudasai",
                    "Please help me",
                    "助けてください。",
                    "Please help me.",
                ),
                (
                    "いくらですか？",
                    "Ikura desu ka?",
                    "How much is it?",
                    "これはいくらですか？",
                    "How much is this?",
                ),
            ),
            "Polite requests with ください",
            (
                "ください means ‘please give me’. Use を between the "
                "requested item and ください."
            ),
            [
                _choice(
                    "Which Japanese word means ‘Water’?",
                    "水",
                    "水 means water and is pronounced mizu.",
                    [
                        "食べ物",
                        "水",
                        "トイレ",
                        "こんにちは",
                    ],
                ),
                _choice(
                    "Which phrase asks the price?",
                    "いくらですか？",
                    "いくらですか asks how much something is.",
                    [
                        "助けてください",
                        "いくらですか？",
                        "水",
                        "食べ物",
                    ],
                ),
                _order(
                    "Arrange: Water, please.",
                    "水をください",
                    "Use を after the requested item.",
                    ["ください", "を", "水"],
                    ["mizu o kudasai"],
                ),
            ],
        ),
    ],
)


STARTER_COURSES = {
    "French": FRENCH_COURSE,
    "Spanish": SPANISH_COURSE,
    "Hindi": HINDI_COURSE,
    "Korean": KOREAN_COURSE,
    "Japanese": JAPANESE_COURSE,
}


def get_starter_course(language):
    """Return a safe copy of an additional-language course."""
    course = STARTER_COURSES.get(language)

    if course is None:
        return None

    course = deepcopy(course)
    course["units"][0] ["lessons"].extend(get_extra_lessons(language))
    return course