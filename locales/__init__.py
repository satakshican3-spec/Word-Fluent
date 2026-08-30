import streamlit as st


DEFAULT_LANGUAGE = "en"


INTERFACE_LANGUAGES = {
    "en": {
        "name": "English",
        "native": "English",
    },
    "bn": {
        "name": "Bengali",
        "native": "বাংলা",
    },
    "hi": {
        "name": "Hindi",
        "native": "हिन्दी",
    },
    "fr": {
        "name": "French",
        "native": "Français",
    },
    "es": {
        "name": "Spanish",
        "native": "Español",
    },
    "ko": {
        "name": "Korean",
        "native": "한국어",
    },
    "ja": {
        "name": "Japanese",
        "native": "日本語",
    },
}


TRANSLATIONS = {
    "en": {
        "choose_interface_title": "Choose the language you understand",
        "choose_interface_help": (
            "Menus, instructions, and explanations will appear "
            "in this language."
        ),
        "interface_language": "App language",
        "continue": "Continue",
    },
    "bn": {
        "choose_interface_title": "আপনি যে ভাষা বোঝেন তা বেছে নিন",
        "choose_interface_help": (
            "মেনু, নির্দেশনা এবং ব্যাখ্যা এই ভাষায় দেখানো হবে।"
        ),
        "interface_language": "অ্যাপের ভাষা",
        "continue": "চালিয়ে যান",
    },
    "hi": {
        "choose_interface_title": "वह भाषा चुनें जिसे आप समझते हैं",
        "choose_interface_help": (
            "मेनू, निर्देश और व्याख्याएँ इस भाषा में दिखाई देंगी।"
        ),
        "interface_language": "ऐप की भाषा",
        "continue": "जारी रखें",
    },
    "fr": {
        "choose_interface_title": (
            "Choisissez la langue que vous comprenez"
        ),
        "choose_interface_help": (
            "Les menus, les instructions et les explications "
            "apparaîtront dans cette langue."
        ),
        "interface_language": "Langue de l’application",
        "continue": "Continuer",
    },
    "es": {
        "choose_interface_title": "Elige el idioma que entiendes",
        "choose_interface_help": (
            "Los menús, las instrucciones y las explicaciones "
            "aparecerán en este idioma."
        ),
        "interface_language": "Idioma de la aplicación",
        "continue": "Continuar",
    },
    "ko": {
        "choose_interface_title": "이해할 수 있는 언어를 선택하세요",
        "choose_interface_help": (
            "메뉴, 안내, 설명이 이 언어로 표시됩니다."
        ),
        "interface_language": "앱 언어",
        "continue": "계속",
    },
    "ja": {
        "choose_interface_title": "読める言語を選んでください",
        "choose_interface_help": (
            "メニュー、案内、説明がこの言語で表示されます。"
        ),
        "interface_language": "アプリの言語",
        "continue": "続ける",
    },
}


def normalize_language(value):
    if not value:
        return DEFAULT_LANGUAGE

    cleaned = str(value).strip().casefold()

    for code, details in INTERFACE_LANGUAGES.items():
        accepted_values = {
            code.casefold(),
            details["name"].casefold(),
            details["native"].casefold(),
            (
                f"{details['native']} · "
                f"{details['name']}"
            ).casefold(),
        }

        if cleaned in accepted_values:
            return code

    return DEFAULT_LANGUAGE


def get_interface_language():
    return normalize_language(
        st.session_state.get(
            "interface_language",
            DEFAULT_LANGUAGE,
        )
    )


def set_interface_language(value):
    code = normalize_language(value)
    st.session_state["interface_language"] = code
    return code


def language_codes():
    return list(INTERFACE_LANGUAGES.keys())


def language_label(code):
    code = normalize_language(code)
    details = INTERFACE_LANGUAGES[code]

    if details["native"] == details["name"]:
        return details["native"]

    return f"{details['native']} · {details['name']}"


def t(key, language=None, **values):
    code = normalize_language(
        language or get_interface_language()
    )

    text = TRANSLATIONS.get(code, {}).get(key)

    if text is None:
        text = TRANSLATIONS[DEFAULT_LANGUAGE].get(
            key,
            key,
        )

    if not values:
        return text

    try:
        return text.format(**values)
    except (KeyError, ValueError):
        return text

HOME_TRANSLATIONS_TOP = {
    "en": {
        "learning_language": "Learning language",
        "dark_mode": "Dark mode",
        "tagline": "Play. Practise. Pronounce.",
        "learning": "Learning",
    },
    "bn": {
        "learning_language": "শেখার ভাষা",
        "dark_mode": "ডার্ক মোড",
        "tagline": "খেলুন। অনুশীলন করুন। উচ্চারণ করুন।",
        "learning": "শেখা হচ্ছে",
    },
    "hi": {
        "learning_language": "सीखने की भाषा",
        "dark_mode": "डार्क मोड",
        "tagline": "खेलें। अभ्यास करें। उच्चारण करें।",
        "learning": "सीख रहे हैं",
    },
    "fr": {
        "learning_language": "Langue d’apprentissage",
        "dark_mode": "Mode sombre",
        "tagline": "Jouez. Pratiquez. Prononcez.",
        "learning": "Apprentissage",
    },
    "es": {
        "learning_language": "Idioma de aprendizaje",
        "dark_mode": "Modo oscuro",
        "tagline": "Juega. Practica. Pronuncia.",
        "learning": "Aprendiendo",
    },
    "ko": {
        "learning_language": "학습 언어",
        "dark_mode": "다크 모드",
        "tagline": "플레이하세요. 연습하세요. 발음하세요.",
        "learning": "학습 중",
    },
    "ja": {
        "learning_language": "学習言語",
        "dark_mode": "ダークモード",
        "tagline": "遊ぶ。練習する。発音する。",
        "learning": "学習中",
    },
}

for language_code, home_strings in HOME_TRANSLATIONS_TOP.items():
    TRANSLATIONS.setdefault(language_code, {}).update(home_strings)

HOME_TRANSLATIONS_STATS = {
    "en": {
        "coins": "Coins",
        "hearts": "Hearts",
        "language_streak": "{learning_language} streak",
        "days": "{count} days",
        "weekly_goal": "Weekly goal",
        "minutes_short": "{current}/{goal} min",
    },
    "bn": {
        "coins": "কয়েন",
        "hearts": "হার্ট",
        "language_streak": "{learning_language} স্ট্রিক",
        "days": "{count} দিন",
        "weekly_goal": "সাপ্তাহিক লক্ষ্য",
        "minutes_short": "{current}/{goal} মিনিট",
    },
    "hi": {
        "coins": "सिक्के",
        "hearts": "दिल",
        "language_streak": "{learning_language} स्ट्रीक",
        "days": "{count} दिन",
        "weekly_goal": "साप्ताहिक लक्ष्य",
        "minutes_short": "{current}/{goal} मिनट",
    },
    "fr": {
        "coins": "Pièces",
        "hearts": "Cœurs",
        "language_streak": "Série en {learning_language}",
        "days": "{count} jours",
        "weekly_goal": "Objectif hebdomadaire",
        "minutes_short": "{current}/{goal} min",
    },
    "es": {
        "coins": "Monedas",
        "hearts": "Corazones",
        "language_streak": "Racha de {learning_language}",
        "days": "{count} días",
        "weekly_goal": "Objetivo semanal",
        "minutes_short": "{current}/{goal} min",
    },
    "ko": {
        "coins": "코인",
        "hearts": "하트",
        "language_streak": "{learning_language} 연속 학습",
        "days": "{count}일",
        "weekly_goal": "주간 목표",
        "minutes_short": "{current}/{goal}분",
    },
    "ja": {
        "coins": "コイン",
        "hearts": "ハート",
        "language_streak": "{learning_language}の連続学習",
        "days": "{count}日",
        "weekly_goal": "週間目標",
        "minutes_short": "{current}/{goal}分",
    },
}

for language_code, home_strings in HOME_TRANSLATIONS_STATS.items():
    TRANSLATIONS.setdefault(language_code, {}).update(home_strings)

HOME_TRANSLATIONS_LEVELS = {
    "en": {
        "your_learning_level": "Your learning level",
        "choose_starting_level_help": (
            "Choose your starting level. That level and every "
            "level below it will be unlocked."
        ),
        "starting_level": "Starting level",
        "confirm_starting_level": "Confirm starting level",
        "current_level": "Current level",
        "unlocked_levels": "Unlocked levels",
        "level_beginner": "Beginner",
        "level_elementary": "Elementary",
        "level_intermediate": "Intermediate",
        "level_upper_intermediate": "Upper intermediate",
        "level_advanced": "Advanced",
        "levels_unlocked_success": (
            "{level} and every lower level are now unlocked "
            "for {learning_language}."
        ),
    },
    "bn": {
        "your_learning_level": "আপনার শেখার স্তর",
        "choose_starting_level_help": (
            "আপনার শুরুর স্তর বেছে নিন। সেই স্তর এবং তার নিচের "
            "সব স্তর আনলক হবে।"
        ),
        "starting_level": "শুরুর স্তর",
        "confirm_starting_level": "শুরুর স্তর নিশ্চিত করুন",
        "current_level": "বর্তমান স্তর",
        "unlocked_levels": "আনলক করা স্তরসমূহ",
        "level_beginner": "শিক্ষানবিস",
        "level_elementary": "প্রাথমিক",
        "level_intermediate": "মধ্যবর্তী",
        "level_upper_intermediate": "উচ্চ-মধ্যবর্তী",
        "level_advanced": "উন্নত",
        "levels_unlocked_success": (
            "{level} এবং এর নিচের সব স্তর এখন "
            "{learning_language}-এর জন্য আনলক হয়েছে।"
        ),
    },
    "hi": {
        "your_learning_level": "आपका सीखने का स्तर",
        "choose_starting_level_help": (
            "अपना शुरुआती स्तर चुनें। वह स्तर और उसके नीचे के "
            "सभी स्तर अनलॉक हो जाएंगे।"
        ),
        "starting_level": "शुरुआती स्तर",
        "confirm_starting_level": "शुरुआती स्तर की पुष्टि करें",
        "current_level": "वर्तमान स्तर",
        "unlocked_levels": "अनलॉक किए गए स्तर",
        "level_beginner": "शुरुआती",
        "level_elementary": "प्रारंभिक",
        "level_intermediate": "मध्यवर्ती",
        "level_upper_intermediate": "उच्च-मध्यवर्ती",
        "level_advanced": "उन्नत",
        "levels_unlocked_success": (
            "{learning_language} के लिए {level} और उससे नीचे के "
            "सभी स्तर अब अनलॉक हैं।"
        ),
    },
    "fr": {
        "your_learning_level": "Votre niveau d’apprentissage",
        "choose_starting_level_help": (
            "Choisissez votre niveau de départ. Ce niveau et tous "
            "les niveaux inférieurs seront débloqués."
        ),
        "starting_level": "Niveau de départ",
        "confirm_starting_level": "Confirmer le niveau de départ",
        "current_level": "Niveau actuel",
        "unlocked_levels": "Niveaux débloqués",
        "level_beginner": "Débutant",
        "level_elementary": "Élémentaire",
        "level_intermediate": "Intermédiaire",
        "level_upper_intermediate": "Intermédiaire supérieur",
        "level_advanced": "Avancé",
        "levels_unlocked_success": (
            "{level} et tous les niveaux inférieurs sont maintenant "
            "débloqués pour {learning_language}."
        ),
    },
    "es": {
        "your_learning_level": "Tu nivel de aprendizaje",
        "choose_starting_level_help": (
            "Elige tu nivel inicial. Ese nivel y todos los niveles "
            "inferiores se desbloquearán."
        ),
        "starting_level": "Nivel inicial",
        "confirm_starting_level": "Confirmar nivel inicial",
        "current_level": "Nivel actual",
        "unlocked_levels": "Niveles desbloqueados",
        "level_beginner": "Principiante",
        "level_elementary": "Elemental",
        "level_intermediate": "Intermedio",
        "level_upper_intermediate": "Intermedio alto",
        "level_advanced": "Avanzado",
        "levels_unlocked_success": (
            "{level} y todos los niveles inferiores ya están "
            "desbloqueados para {learning_language}."
        ),
    },
    "ko": {
        "your_learning_level": "학습 수준",
        "choose_starting_level_help": (
            "시작 수준을 선택하세요. 선택한 수준과 그 아래의 "
            "모든 수준이 잠금 해제됩니다."
        ),
        "starting_level": "시작 수준",
        "confirm_starting_level": "시작 수준 확인",
        "current_level": "현재 수준",
        "unlocked_levels": "잠금 해제된 수준",
        "level_beginner": "초급",
        "level_elementary": "기초",
        "level_intermediate": "중급",
        "level_upper_intermediate": "중상급",
        "level_advanced": "고급",
        "levels_unlocked_success": (
            "{learning_language}에서 {level} 및 그 아래의 "
            "모든 수준이 잠금 해제되었습니다."
        ),
    },
    "ja": {
        "your_learning_level": "学習レベル",
        "choose_starting_level_help": (
            "開始レベルを選択してください。そのレベル以下の"
            "すべてのレベルがアンロックされます。"
        ),
        "starting_level": "開始レベル",
        "confirm_starting_level": "開始レベルを確定",
        "current_level": "現在のレベル",
        "unlocked_levels": "アンロック済みのレベル",
        "level_beginner": "初心者",
        "level_elementary": "初級",
        "level_intermediate": "中級",
        "level_upper_intermediate": "中上級",
        "level_advanced": "上級",
        "levels_unlocked_success": (
            "{learning_language}で{level}以下のすべての"
            "レベルがアンロックされました。"
        ),
    },
}

for language_code, home_strings in HOME_TRANSLATIONS_LEVELS.items():
    TRANSLATIONS.setdefault(language_code, {}).update(home_strings)

HOME_TRANSLATIONS_SESSION = {
    "en": {
        "session_settings": "Session settings",
        "session_length": "Session length",
        "minutes": "{count} minutes",
        "difficulty": "Difficulty",
        "difficulty_relaxed": "Relaxed",
        "difficulty_balanced": "Balanced",
        "difficulty_challenging": "Challenging",
        "difficulty_custom": "Custom",
    },
    "bn": {
        "session_settings": "সেশন সেটিংস",
        "session_length": "সেশনের সময়",
        "minutes": "{count} মিনিট",
        "difficulty": "কঠিনতার মাত্রা",
        "difficulty_relaxed": "সহজ",
        "difficulty_balanced": "সামঞ্জস্যপূর্ণ",
        "difficulty_challenging": "চ্যালেঞ্জিং",
        "difficulty_custom": "নিজস্ব",
    },
    "hi": {
        "session_settings": "सत्र सेटिंग्स",
        "session_length": "सत्र की अवधि",
        "minutes": "{count} मिनट",
        "difficulty": "कठिनाई",
        "difficulty_relaxed": "आरामदायक",
        "difficulty_balanced": "संतुलित",
        "difficulty_challenging": "चुनौतीपूर्ण",
        "difficulty_custom": "कस्टम",
    },
    "fr": {
        "session_settings": "Paramètres de session",
        "session_length": "Durée de la session",
        "minutes": "{count} minutes",
        "difficulty": "Difficulté",
        "difficulty_relaxed": "Détendu",
        "difficulty_balanced": "Équilibré",
        "difficulty_challenging": "Difficile",
        "difficulty_custom": "Personnalisé",
    },
    "es": {
        "session_settings": "Configuración de la sesión",
        "session_length": "Duración de la sesión",
        "minutes": "{count} minutos",
        "difficulty": "Dificultad",
        "difficulty_relaxed": "Relajado",
        "difficulty_balanced": "Equilibrado",
        "difficulty_challenging": "Desafiante",
        "difficulty_custom": "Personalizado",
    },
    "ko": {
        "session_settings": "세션 설정",
        "session_length": "세션 시간",
        "minutes": "{count}분",
        "difficulty": "난이도",
        "difficulty_relaxed": "편안함",
        "difficulty_balanced": "균형",
        "difficulty_challenging": "도전적",
        "difficulty_custom": "사용자 지정",
    },
    "ja": {
        "session_settings": "セッション設定",
        "session_length": "セッション時間",
        "minutes": "{count}分",
        "difficulty": "難易度",
        "difficulty_relaxed": "リラックス",
        "difficulty_balanced": "バランス",
        "difficulty_challenging": "チャレンジ",
        "difficulty_custom": "カスタム",
    },
}

for language_code, home_strings in HOME_TRANSLATIONS_SESSION.items():
    TRANSLATIONS.setdefault(language_code, {}).update(home_strings)

    HOME_TRANSLATIONS_ACTIVITIES = {
    "en": {
        "choose_activity": "Choose an activity",
        "sentence_builder": "Sentence Builder",
        "sentence_builder_description": "Arrange or type words to build useful sentences.",
        "pronunciation": "Pronunciation",
        "pronunciation_description": "Speak aloud and receive level-based feedback.",
        "lessons": "Lessons",
        "lessons_description": "Learn vocabulary and grammar at your level.",
        "progress": "Progress",
        "progress_description": "View goals, streaks, coins and achievements.",
        "open_activity": "Open {activity}",
        "choose_level_unlock": "Choose a starting level to unlock the activities.",
        "feature_selected": "{activity} selected. We will connect this feature next.",
        "weekly_progress": "Weekly progress",
        "weekly_progress_caption": "{current} of {goal} minutes completed for {learning_language} this week.",
    },
    "bn": {
        "choose_activity": "একটি কার্যক্রম বেছে নিন",
        "sentence_builder": "বাক্য নির্মাতা",
        "sentence_builder_description": "দরকারি বাক্য তৈরি করতে শব্দগুলো সাজান বা টাইপ করুন।",
        "pronunciation": "উচ্চারণ",
        "pronunciation_description": "জোরে বলুন এবং আপনার স্তর অনুযায়ী মতামত পান।",
        "lessons": "পাঠ",
        "lessons_description": "আপনার স্তর অনুযায়ী শব্দভাণ্ডার ও ব্যাকরণ শিখুন।",
        "progress": "অগ্রগতি",
        "progress_description": "লক্ষ্য, ধারাবাহিকতা, কয়েন ও অর্জন দেখুন।",
        "open_activity": "{activity} খুলুন",
        "choose_level_unlock": "কার্যক্রমগুলো আনলক করতে একটি শুরুর স্তর বেছে নিন।",
        "feature_selected": "{activity} নির্বাচন করা হয়েছে। এই বৈশিষ্ট্যটি পরে যুক্ত করা হবে।",
        "weekly_progress": "সাপ্তাহিক অগ্রগতি",
        "weekly_progress_caption": "এই সপ্তাহে {learning_language}-এর জন্য {goal} মিনিটের মধ্যে {current} মিনিট সম্পন্ন হয়েছে।",
    },
    "hi": {
        "choose_activity": "कोई गतिविधि चुनें",
        "sentence_builder": "वाक्य निर्माता",
        "sentence_builder_description": "उपयोगी वाक्य बनाने के लिए शब्दों को क्रम में लगाएँ या टाइप करें।",
        "pronunciation": "उच्चारण",
        "pronunciation_description": "ज़ोर से बोलें और अपने स्तर के अनुसार प्रतिक्रिया पाएँ।",
        "lessons": "पाठ",
        "lessons_description": "अपने स्तर के अनुसार शब्दावली और व्याकरण सीखें।",
        "progress": "प्रगति",
        "progress_description": "लक्ष्य, स्ट्रीक, सिक्के और उपलब्धियाँ देखें।",
        "open_activity": "{activity} खोलें",
        "choose_level_unlock": "गतिविधियाँ अनलॉक करने के लिए शुरुआती स्तर चुनें।",
        "feature_selected": "{activity} चुना गया है। यह सुविधा बाद में जोड़ी जाएगी।",
        "weekly_progress": "साप्ताहिक प्रगति",
        "weekly_progress_caption": "इस सप्ताह {learning_language} के लिए {goal} में से {current} मिनट पूरे हुए।",
    },
    "fr": {
        "choose_activity": "Choisissez une activité",
        "sentence_builder": "Créateur de phrases",
        "sentence_builder_description": "Organisez ou tapez des mots pour créer des phrases utiles.",
        "pronunciation": "Prononciation",
        "pronunciation_description": "Parlez à voix haute et recevez des commentaires adaptés à votre niveau.",
        "lessons": "Leçons",
        "lessons_description": "Apprenez du vocabulaire et de la grammaire adaptés à votre niveau.",
        "progress": "Progrès",
        "progress_description": "Consultez vos objectifs, séries, pièces et réussites.",
        "open_activity": "Ouvrir {activity}",
        "choose_level_unlock": "Choisissez un niveau de départ pour débloquer les activités.",
        "feature_selected": "Activité sélectionnée : {activity}. Cette fonctionnalité sera bientôt disponible.",
        "weekly_progress": "Progression hebdomadaire",
        "weekly_progress_caption": "Cette semaine, {current} minutes sur {goal} ont été réalisées en {learning_language}.",
    },
    "es": {
        "choose_activity": "Elige una actividad",
        "sentence_builder": "Constructor de oraciones",
        "sentence_builder_description": "Ordena o escribe palabras para formar oraciones útiles.",
        "pronunciation": "Pronunciación",
        "pronunciation_description": "Habla en voz alta y recibe comentarios según tu nivel.",
        "lessons": "Lecciones",
        "lessons_description": "Aprende vocabulario y gramática según tu nivel.",
        "progress": "Progreso",
        "progress_description": "Consulta objetivos, rachas, monedas y logros.",
        "open_activity": "Abrir {activity}",
        "choose_level_unlock": "Elige un nivel inicial para desbloquear las actividades.",
        "feature_selected": "Has seleccionado {activity}. Esta función se conectará después.",
        "weekly_progress": "Progreso semanal",
        "weekly_progress_caption": "Esta semana completaste {current} de {goal} minutos de {learning_language}.",
    },
    "ko": {
        "choose_activity": "활동 선택",
        "sentence_builder": "문장 만들기",
        "sentence_builder_description": "단어를 배열하거나 입력하여 유용한 문장을 만드세요.",
        "pronunciation": "발음",
        "pronunciation_description": "소리 내어 말하고 레벨에 맞는 피드백을 받으세요.",
        "lessons": "레슨",
        "lessons_description": "자신의 레벨에 맞는 어휘와 문법을 배우세요.",
        "progress": "진도",
        "progress_description": "목표, 연속 학습, 코인 및 업적을 확인하세요.",
        "open_activity": "{activity} 열기",
        "choose_level_unlock": "활동을 잠금 해제하려면 시작 레벨을 선택하세요.",
        "feature_selected": "{activity}을(를) 선택했습니다. 이 기능은 나중에 연결됩니다.",
        "weekly_progress": "주간 진도",
        "weekly_progress_caption": "이번 주 {learning_language} 학습을 {goal}분 중 {current}분 완료했습니다.",
    },
    "ja": {
        "choose_activity": "アクティビティを選ぶ",
        "sentence_builder": "文作り",
        "sentence_builder_description": "単語を並べるか入力して、役立つ文を作りましょう。",
        "pronunciation": "発音",
        "pronunciation_description": "声に出して話し、レベルに応じたフィードバックを受けましょう。",
        "lessons": "レッスン",
        "lessons_description": "自分のレベルに合った語彙と文法を学びましょう。",
        "progress": "進捗",
        "progress_description": "目標、連続記録、コイン、実績を確認しましょう。",
        "open_activity": "{activity}を開く",
        "choose_level_unlock": "アクティビティを解除するには開始レベルを選んでください。",
        "feature_selected": "{activity}を選択しました。この機能は後で接続されます。",
        "weekly_progress": "週間進捗",
        "weekly_progress_caption": "今週は{learning_language}を{goal}分中{current}分完了しました。",
    },
}

for language_code, activity_strings in HOME_TRANSLATIONS_ACTIVITIES.items():
    TRANSLATIONS.setdefault(language_code, {}).update(activity_strings)