PROMPTS = [
    (
        "You greet someone politely in the morning.",
        "Good morning.",
        "👋",
    ),
    (
        "You introduce yourself to someone new.",
        "My name is Aisha.",
        "🙂",
    ),
    (
        "You politely ask someone their name.",
        "What is your name?",
        "💬",
    ),
    (
        "You politely ask someone to open the door.",
        "Please open the door.",
        "🚪",
    ),
    (
        "A friend helps you and you thank them.",
        "Thank you for your help.",
        "🙏",
    ),
    (
        "You introduce your sister.",
        "She is my sister.",
        "👭",
    ),
    (
        "You describe your daily language practice.",
        "I study the language every day.",
        "📚",
    ),
    (
        "You describe your morning routine.",
        "I eat breakfast in the morning.",
        "🍞",
    ),
    (
        "You order coffee politely at a café.",
        "I would like a cup of coffee.",
        "☕",
    ),
    (
        "You ask for the bill at a restaurant.",
        "May I have the bill, please?",
        "🧾",
    ),
    (
        "You ask for the location of the library.",
        "Where is the library?",
        "📖",
    ),
    (
        "You give someone directions at a corner.",
        "Turn left at the corner.",
        "⬅️",
    ),
    (
        "You explain where the station is.",
        "The station is near the hotel.",
        "🚉",
    ),
    (
        "You politely ask someone for assistance.",
        "Can you help me, please?",
        "🆘",
    ),
]


SENTENCES = {
    "French": [
        "Bonjour",
        "Je m'appelle Aisha",
        "Comment vous appelez-vous",
        "Ouvrez la porte s'il vous plaît",
        "Merci pour votre aide",
        "Elle est ma sœur",
        "J'étudie le français tous les jours",
        "Je prends mon petit-déjeuner le matin",
        "Je voudrais une tasse de café",
        "Puis-je avoir l'addition s'il vous plaît",
        "Où est la bibliothèque",
        "Tournez à gauche au coin de la rue",
        "La gare est près de l'hôtel",
        "Pouvez-vous m'aider s'il vous plaît",
    ],
    "Spanish": [
        "Buenos días",
        "Me llamo Aisha",
        "Cómo se llama",
        "Abra la puerta por favor",
        "Gracias por su ayuda",
        "Ella es mi hermana",
        "Estudio español todos los días",
        "Desayuno por la mañana",
        "Quisiera una taza de café",
        "Me trae la cuenta por favor",
        "Dónde está la biblioteca",
        "Gire a la izquierda en la esquina",
        "La estación está cerca del hotel",
        "Puede ayudarme por favor",
    ],
    "Hindi": [
        "सुप्रभात",
        "मेरा नाम आयशा है",
        "आपका नाम क्या है",
        "कृपया दरवाज़ा खोलिए",
        "आपकी मदद के लिए धन्यवाद",
        "वह मेरी बहन है",
        "मैं हर दिन हिंदी पढ़ती हूँ",
        "मैं सुबह नाश्ता करती हूँ",
        "मुझे एक कप कॉफ़ी चाहिए",
        "कृपया मुझे बिल दीजिए",
        "पुस्तकालय कहाँ है",
        "कोने पर बाएँ मुड़िए",
        "स्टेशन होटल के पास है",
        "क्या आप मेरी मदद कर सकते हैं",
    ],
    "Korean": [
        "안녕하세요",
        "제 이름은 아이샤예요",
        "이름이 뭐예요",
        "문을 열어 주세요",
        "도와주셔서 감사합니다",
        "그녀는 제 여동생이에요",
        "저는 매일 한국어를 공부해요",
        "저는 아침에 아침밥을 먹어요",
        "커피 한 잔 주세요",
        "계산서 주세요",
        "도서관이 어디예요",
        "모퉁이에서 왼쪽으로 도세요",
        "역은 호텔 근처에 있어요",
        "저를 도와주실 수 있어요",
    ],
    "Japanese": [
        "おはよう|ございます",
        "私の|名前は|アイシャです",
        "お名前は|何ですか",
        "ドアを|開けて|ください",
        "手伝って|くださって|ありがとうございます",
        "彼女は|私の|姉です",
        "私は|毎日|日本語を|勉強します",
        "私は|朝ご飯を|食べます",
        "コーヒーを|一杯|ください",
        "お会計を|お願いします",
        "図書館は|どこですか",
        "角を|左に|曲がって|ください",
        "駅は|ホテルの|近くです",
        "手伝って|もらえますか",
    ],
}


def build_multilingual_exercises(language, limit):
    if limit <= 0:
        return []

    answers = SENTENCES.get(language, [])
    converted = []

    for prompt, raw_answer in zip(PROMPTS, answers):
        situation, translation, picture = prompt

        if "|" in raw_answer:
            words = raw_answer.split("|")
            answer = " ".join(words)
            accepted_answers = [raw_answer.replace("|", "")]
        else:
            words = raw_answer.split()
            answer = raw_answer
            accepted_answers = []

        converted.append(
            {
                "situation": situation,
                "translation": translation,
                "picture": picture,
                "clue": f'The answer begins with "{words[0]}".',
                "answer": answer,
                "accepted_answers": accepted_answers,
                "words": words,
                "transliteration": None,
                "explanation": (
                    f'This sentence means "{translation}" in English.'
                ),
            }
        )

        if len(converted) >= limit:
            break

    return converted