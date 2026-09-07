import html
import random
import re
import unicodedata

import streamlit as st

from language_packs import get_course
from locales import get_interface_language, t
from services.pronunciation_engine import generate_reference_audio


LESSON_TEXT = {
    "en": {
        "title": "Learning Path",
        "subtitle": "Learn the words first, understand the pattern, then practise.",
        "level": "Level",
        "completed": "Lessons completed",
        "course_progress": "Course progress",
        "course_units": "Course units",
        "unit": "Unit {number}",
        "minutes": "{count} min",
        "coins": "{count} coins",
        "start": "Start lesson",
        "review": "Review lesson",
        "learn_first": "Start here before opening the practice games.",
        "words_stage": "Learn words",
        "pattern_stage": "Understand",
        "practice_stage": "Practise",
        "results_stage": "Results",
        "learn_words": "1. Learn the words",
        "learn_words_help": (
            "Study each meaning, pronunciation, and example "
            "before continuing."
        ),
        "meaning": "Meaning",
        "pronunciation": "Pronunciation",
        "example": "Example",
        "example_meaning": "Example meaning",
        "listen": "Listen",
        "audio_error": (
            "Audio is unavailable right now. You can still use "
            "the pronunciation guide."
        ),
        "continue_pattern": "Continue to the pattern",
        "understand": "2. Understand the pattern",
        "understand_help": (
            "This small pattern will help you build your own sentences."
        ),
        "practice_notice": (
            "Next, answer three short questions. You need at least "
            "two correct answers to pass."
        ),
        "start_practice": "Start practice",
        "practice": "3. Practise ({current}/{total})",
        "choose_answer": "Choose one answer",
        "choose_word": "Choose the missing word",
        "arrange_help": (
            "Arrange the words by typing the complete sentence."
        ),
        "your_sentence": "Your sentence",
        "type_answer": "Type your answer",
        "check": "Check answer",
        "correct": "Correct! Great work.",
        "not_quite": (
            "Not quite. The correct answer is: {answer}"
        ),
        "why": "Why: {explanation}",
        "next": "Next question",
        "see_results": "See results",
        "complete_message": (
            "Lesson complete! You answered {correct} of {total} "
            "questions correctly."
        ),
        "earned": (
            "You earned {xp} XP and {coins} coins. The next lesson "
            "is now unlocked."
        ),
        "reviewed": (
            "You reviewed this lesson successfully. Rewards are "
            "given once per lesson."
        ),
        "failed": (
            "You answered {correct} of {total} correctly. You need "
            "{needed} correct answers to pass."
        ),
        "review_help": (
            "Review the vocabulary and pattern, then try again."
        ),
        "retry": "Try lesson again",
        "return_path": "Return to learning path",
        "path_complete": (
            "You completed this beginner learning path!"
        ),
        "not_available": (
            "A learning path is not available for this language yet."
        ),
    },
    "bn": {
        "title": "শেখার পথ",
        "subtitle": (
            "আগে শব্দ শিখুন, গঠন বুঝুন, তারপর অনুশীলন করুন।"
        ),
        "level": "স্তর",
        "completed": "সম্পন্ন পাঠ",
        "course_progress": "কোর্সের অগ্রগতি",
        "course_units": "কোর্স ইউনিট",
        "unit": "ইউনিট {number}",
        "minutes": "{count} মিনিট",
        "coins": "{count} কয়েন",
        "start": "পাঠ শুরু করুন",
        "review": "পাঠ আবার দেখুন",
        "learn_first": (
            "অনুশীলনের গেম খোলার আগে এখান থেকে শুরু করুন।"
        ),
        "words_stage": "শব্দ শিখুন",
        "pattern_stage": "বুঝুন",
        "practice_stage": "অনুশীলন",
        "results_stage": "ফলাফল",
        "learn_words": "১. শব্দ শিখুন",
        "learn_words_help": (
            "এগিয়ে যাওয়ার আগে অর্থ, উচ্চারণ ও উদাহরণ পড়ুন।"
        ),
        "meaning": "অর্থ",
        "pronunciation": "উচ্চারণ",
        "example": "উদাহরণ",
        "example_meaning": "উদাহরণের অর্থ",
        "listen": "শুনুন",
        "audio_error": (
            "অডিও এখন পাওয়া যাচ্ছে না। "
            "উচ্চারণ নির্দেশিকা ব্যবহার করুন।"
        ),
        "continue_pattern": "গঠন শিখতে এগিয়ে যান",
        "understand": "২. গঠন বুঝুন",
        "understand_help": (
            "এই ছোট গঠনটি নিজের বাক্য বানাতে সাহায্য করবে।"
        ),
        "practice_notice": (
            "এখন তিনটি ছোট প্রশ্নের উত্তর দিন। "
            "পাস করতে অন্তত দুটি সঠিক হতে হবে।"
        ),
        "start_practice": "অনুশীলন শুরু করুন",
        "practice": "৩. অনুশীলন ({current}/{total})",
        "choose_answer": "একটি উত্তর বেছে নিন",
        "choose_word": "শূন্যস্থানের শব্দ বেছে নিন",
        "arrange_help": (
            "সম্পূর্ণ বাক্য লিখে শব্দগুলো সাজান।"
        ),
        "your_sentence": "আপনার বাক্য",
        "type_answer": "আপনার উত্তর লিখুন",
        "check": "উত্তর যাচাই করুন",
        "correct": "সঠিক! দারুণ কাজ।",
        "not_quite": "ঠিক হয়নি। সঠিক উত্তর: {answer}",
        "why": "কারণ: {explanation}",
        "next": "পরের প্রশ্ন",
        "see_results": "ফলাফল দেখুন",
        "complete_message": (
            "পাঠ শেষ! {total}টির মধ্যে {correct}টি উত্তর সঠিক হয়েছে।"
        ),
        "earned": (
            "আপনি {xp} XP ও {coins} কয়েন পেয়েছেন। "
            "পরের পাঠ আনলক হয়েছে।"
        ),
        "reviewed": (
            "পাঠটি সফলভাবে আবার দেখেছেন। "
            "প্রতিটি পাঠে একবার পুরস্কার দেওয়া হয়।"
        ),
        "failed": (
            "{total}টির মধ্যে {correct}টি সঠিক। "
            "পাস করতে {needed}টি সঠিক উত্তর দরকার।"
        ),
        "review_help": (
            "শব্দ ও গঠন আবার দেখে চেষ্টা করুন।"
        ),
        "retry": "আবার চেষ্টা করুন",
        "return_path": "শেখার পথে ফিরুন",
        "path_complete": (
            "আপনি এই প্রাথমিক শেখার পথ সম্পন্ন করেছেন!"
        ),
        "not_available": (
            "এই ভাষার শেখার পথ এখনো পাওয়া যাচ্ছে না।"
        ),
    },
    "hi": {
        "title": "सीखने का मार्ग",
        "subtitle": (
            "पहले शब्द सीखें, पैटर्न समझें, फिर अभ्यास करें।"
        ),
        "level": "स्तर",
        "completed": "पूरे किए पाठ",
        "course_progress": "कोर्स प्रगति",
        "course_units": "कोर्स इकाइयाँ",
        "unit": "इकाई {number}",
        "minutes": "{count} मिनट",
        "coins": "{count} सिक्के",
        "start": "पाठ शुरू करें",
        "review": "पाठ दोहराएँ",
        "learn_first": (
            "अभ्यास गेम खोलने से पहले यहाँ से शुरू करें।"
        ),
        "words_stage": "शब्द सीखें",
        "pattern_stage": "समझें",
        "practice_stage": "अभ्यास",
        "results_stage": "परिणाम",
        "learn_words": "1. शब्द सीखें",
        "learn_words_help": (
            "आगे बढ़ने से पहले अर्थ, उच्चारण और उदाहरण पढ़ें।"
        ),
        "meaning": "अर्थ",
        "pronunciation": "उच्चारण",
        "example": "उदाहरण",
        "example_meaning": "उदाहरण का अर्थ",
        "listen": "सुनें",
        "audio_error": (
            "ऑडियो अभी उपलब्ध नहीं है। "
            "उच्चारण मार्गदर्शिका का उपयोग करें।"
        ),
        "continue_pattern": "पैटर्न पर जाएँ",
        "understand": "2. पैटर्न समझें",
        "understand_help": (
            "यह छोटा पैटर्न अपने वाक्य बनाने में मदद करेगा।"
        ),
        "practice_notice": (
            "अब तीन छोटे प्रश्न हल करें। "
            "पास होने के लिए कम से कम दो सही चाहिए।"
        ),
        "start_practice": "अभ्यास शुरू करें",
        "practice": "3. अभ्यास ({current}/{total})",
        "choose_answer": "एक उत्तर चुनें",
        "choose_word": "खाली जगह का शब्द चुनें",
        "arrange_help": (
            "पूरा वाक्य लिखकर शब्दों को सही क्रम में लगाएँ।"
        ),
        "your_sentence": "आपका वाक्य",
        "type_answer": "अपना उत्तर लिखें",
        "check": "उत्तर जाँचें",
        "correct": "सही! बहुत अच्छा।",
        "not_quite": (
            "अभी सही नहीं। सही उत्तर है: {answer}"
        ),
        "why": "क्यों: {explanation}",
        "next": "अगला प्रश्न",
        "see_results": "परिणाम देखें",
        "complete_message": (
            "पाठ पूरा! आपने {total} में से {correct} उत्तर सही दिए।"
        ),
        "earned": (
            "आपने {xp} XP और {coins} सिक्के कमाए। "
            "अगला पाठ खुल गया।"
        ),
        "reviewed": (
            "आपने पाठ सफलतापूर्वक दोहराया। "
            "पुरस्कार प्रति पाठ एक बार मिलता है।"
        ),
        "failed": (
            "{total} में से {correct} सही। "
            "पास होने के लिए {needed} सही उत्तर चाहिए।"
        ),
        "review_help": (
            "शब्द और पैटर्न दोहराकर फिर प्रयास करें।"
        ),
        "retry": "फिर से प्रयास करें",
        "return_path": "सीखने के मार्ग पर लौटें",
        "path_complete": (
            "आपने यह शुरुआती सीखने का मार्ग पूरा कर लिया!"
        ),
        "not_available": (
            "इस भाषा का सीखने का मार्ग अभी उपलब्ध नहीं है।"
        ),
    },
    "fr": {
        "title": "Parcours d’apprentissage",
        "subtitle": (
            "Apprenez les mots, comprenez le modèle, puis pratiquez."
        ),
        "level": "Niveau",
        "completed": "Leçons terminées",
        "course_progress": "Progression du cours",
        "course_units": "Unités du cours",
        "unit": "Unité {number}",
        "minutes": "{count} min",
        "coins": "{count} pièces",
        "start": "Commencer",
        "review": "Réviser",
        "learn_first": (
            "Commencez ici avant d’ouvrir les jeux de pratique."
        ),
        "words_stage": "Mots",
        "pattern_stage": "Comprendre",
        "practice_stage": "Pratiquer",
        "results_stage": "Résultats",
        "learn_words": "1. Apprendre les mots",
        "learn_words_help": (
            "Étudiez le sens, la prononciation et l’exemple "
            "avant de continuer."
        ),
        "meaning": "Sens",
        "pronunciation": "Prononciation",
        "example": "Exemple",
        "example_meaning": "Sens de l’exemple",
        "listen": "Écouter",
        "audio_error": (
            "L’audio est indisponible. "
            "Utilisez le guide de prononciation."
        ),
        "continue_pattern": "Continuer vers le modèle",
        "understand": "2. Comprendre le modèle",
        "understand_help": (
            "Ce petit modèle vous aide à construire "
            "vos propres phrases."
        ),
        "practice_notice": (
            "Répondez à trois questions. "
            "Deux bonnes réponses sont nécessaires."
        ),
        "start_practice": "Commencer la pratique",
        "practice": "3. Pratiquer ({current}/{total})",
        "choose_answer": "Choisissez une réponse",
        "choose_word": "Choisissez le mot manquant",
        "arrange_help": (
            "Écrivez la phrase complète dans le bon ordre."
        ),
        "your_sentence": "Votre phrase",
        "type_answer": "Écrivez votre réponse",
        "check": "Vérifier",
        "correct": "Correct ! Très bien.",
        "not_quite": (
            "Pas encore. La bonne réponse est : {answer}"
        ),
        "why": "Pourquoi : {explanation}",
        "next": "Question suivante",
        "see_results": "Voir les résultats",
        "complete_message": (
            "Leçon terminée ! {correct} réponses correctes sur {total}."
        ),
        "earned": (
            "Vous avez gagné {xp} XP et {coins} pièces. "
            "La leçon suivante est débloquée."
        ),
        "reviewed": (
            "Révision réussie. Les récompenses sont données "
            "une fois par leçon."
        ),
        "failed": (
            "{correct} bonnes réponses sur {total}. "
            "Il en faut {needed} pour réussir."
        ),
        "review_help": (
            "Révisez les mots et le modèle, puis réessayez."
        ),
        "retry": "Réessayer",
        "return_path": "Retour au parcours",
        "path_complete": (
            "Vous avez terminé ce parcours débutant !"
        ),
        "not_available": (
            "Aucun parcours n’est encore disponible pour cette langue."
        ),
    },
    "es": {
        "title": "Ruta de aprendizaje",
        "subtitle": (
            "Aprende las palabras, comprende el patrón "
            "y después practica."
        ),
        "level": "Nivel",
        "completed": "Lecciones completadas",
        "course_progress": "Progreso del curso",
        "course_units": "Unidades del curso",
        "unit": "Unidad {number}",
        "minutes": "{count} min",
        "coins": "{count} monedas",
        "start": "Comenzar",
        "review": "Repasar",
        "learn_first": (
            "Empieza aquí antes de abrir los juegos de práctica."
        ),
        "words_stage": "Palabras",
        "pattern_stage": "Comprender",
        "practice_stage": "Practicar",
        "results_stage": "Resultados",
        "learn_words": "1. Aprende las palabras",
        "learn_words_help": (
            "Estudia el significado, la pronunciación y el ejemplo "
            "antes de continuar."
        ),
        "meaning": "Significado",
        "pronunciation": "Pronunciación",
        "example": "Ejemplo",
        "example_meaning": "Significado del ejemplo",
        "listen": "Escuchar",
        "audio_error": (
            "El audio no está disponible. "
            "Usa la guía de pronunciación."
        ),
        "continue_pattern": "Continuar al patrón",
        "understand": "2. Comprende el patrón",
        "understand_help": (
            "Este pequeño patrón te ayudará a crear "
            "tus propias frases."
        ),
        "practice_notice": (
            "Responde tres preguntas. "
            "Necesitas al menos dos correctas."
        ),
        "start_practice": "Comenzar práctica",
        "practice": "3. Practica ({current}/{total})",
        "choose_answer": "Elige una respuesta",
        "choose_word": "Elige la palabra que falta",
        "arrange_help": (
            "Escribe la oración completa en el orden correcto."
        ),
        "your_sentence": "Tu oración",
        "type_answer": "Escribe tu respuesta",
        "check": "Comprobar",
        "correct": "¡Correcto! Muy bien.",
        "not_quite": (
            "Aún no. La respuesta correcta es: {answer}"
        ),
        "why": "Por qué: {explanation}",
        "next": "Siguiente pregunta",
        "see_results": "Ver resultados",
        "complete_message": (
            "¡Lección terminada! Acertaste {correct} de {total}."
        ),
        "earned": (
            "Ganaste {xp} XP y {coins} monedas. "
            "La siguiente lección está desbloqueada."
        ),
        "reviewed": (
            "Repaso completado. Las recompensas se entregan "
            "una vez por lección."
        ),
        "failed": (
            "Acertaste {correct} de {total}. "
            "Necesitas {needed} para aprobar."
        ),
        "review_help": (
            "Repasa las palabras y el patrón e inténtalo de nuevo."
        ),
        "retry": "Intentar de nuevo",
        "return_path": "Volver a la ruta",
        "path_complete": (
            "¡Completaste esta ruta para principiantes!"
        ),
        "not_available": (
            "Todavía no hay una ruta disponible para este idioma."
        ),
    },
    "ko": {
        "title": "학습 경로",
        "subtitle": (
            "먼저 단어를 배우고, 패턴을 이해한 뒤 연습하세요."
        ),
        "level": "레벨",
        "completed": "완료한 레슨",
        "course_progress": "코스 진도",
        "course_units": "코스 단원",
        "unit": "단원 {number}",
        "minutes": "{count}분",
        "coins": "코인 {count}개",
        "start": "시작",
        "review": "복습",
        "learn_first": (
            "연습 게임을 열기 전에 여기에서 시작하세요."
        ),
        "words_stage": "단어",
        "pattern_stage": "이해",
        "practice_stage": "연습",
        "results_stage": "결과",
        "learn_words": "1. 단어 배우기",
        "learn_words_help": (
            "계속하기 전에 뜻, 발음, 예문을 확인하세요."
        ),
        "meaning": "뜻",
        "pronunciation": "발음",
        "example": "예문",
        "example_meaning": "예문 뜻",
        "listen": "듣기",
        "audio_error": (
            "오디오를 사용할 수 없습니다. 발음 안내를 이용하세요."
        ),
        "continue_pattern": "패턴으로 계속",
        "understand": "2. 패턴 이해하기",
        "understand_help": (
            "이 짧은 패턴으로 나만의 문장을 만들 수 있습니다."
        ),
        "practice_notice": (
            "짧은 문제 세 개를 풀어 보세요. "
            "두 개 이상 맞혀야 통과합니다."
        ),
        "start_practice": "연습 시작",
        "practice": "3. 연습 ({current}/{total})",
        "choose_answer": "답 하나를 고르세요",
        "choose_word": "빠진 단어를 고르세요",
        "arrange_help": (
            "완전한 문장을 올바른 순서로 입력하세요."
        ),
        "your_sentence": "내 문장",
        "type_answer": "답 입력",
        "check": "답 확인",
        "correct": "정답이에요! 잘했어요.",
        "not_quite": "아쉬워요. 정답: {answer}",
        "why": "이유: {explanation}",
        "next": "다음 문제",
        "see_results": "결과 보기",
        "complete_message": (
            "레슨 완료! {total}개 중 {correct}개를 맞혔습니다."
        ),
        "earned": (
            "{xp} XP와 코인 {coins}개를 받았습니다. "
            "다음 레슨이 열렸습니다."
        ),
        "reviewed": (
            "복습을 완료했습니다. "
            "보상은 레슨마다 한 번 지급됩니다."
        ),
        "failed": (
            "{total}개 중 {correct}개 정답입니다. "
            "통과하려면 {needed}개가 필요합니다."
        ),
        "review_help": (
            "단어와 패턴을 복습한 뒤 다시 시도하세요."
        ),
        "retry": "다시 시도",
        "return_path": "학습 경로로 돌아가기",
        "path_complete": "초급 학습 경로를 완료했습니다!",
        "not_available": (
            "이 언어의 학습 경로는 아직 제공되지 않습니다."
        ),
    },
    "ja": {
        "title": "学習コース",
        "subtitle": (
            "まず単語を学び、パターンを理解してから練習しましょう。"
        ),
        "level": "レベル",
        "completed": "完了したレッスン",
        "course_progress": "コースの進捗",
        "course_units": "コース単元",
        "unit": "単元{number}",
        "minutes": "{count}分",
        "coins": "{count}コイン",
        "start": "始める",
        "review": "復習する",
        "learn_first": (
            "練習ゲームを開く前に、ここから始めましょう。"
        ),
        "words_stage": "単語",
        "pattern_stage": "理解",
        "practice_stage": "練習",
        "results_stage": "結果",
        "learn_words": "1. 単語を学ぶ",
        "learn_words_help": (
            "次へ進む前に、意味・発音・例文を確認してください。"
        ),
        "meaning": "意味",
        "pronunciation": "発音",
        "example": "例文",
        "example_meaning": "例文の意味",
        "listen": "聞く",
        "audio_error": (
            "音声を利用できません。発音ガイドを使ってください。"
        ),
        "continue_pattern": "パターンへ進む",
        "understand": "2. パターンを理解する",
        "understand_help": (
            "この短いパターンで自分の文を作れるようになります。"
        ),
        "practice_notice": (
            "3問に答えましょう。合格には2問以上の正解が必要です。"
        ),
        "start_practice": "練習を始める",
        "practice": "3. 練習 ({current}/{total})",
        "choose_answer": "答えを一つ選んでください",
        "choose_word": "空欄の単語を選んでください",
        "arrange_help": (
            "完全な文を正しい順番で入力してください。"
        ),
        "your_sentence": "あなたの文",
        "type_answer": "答えを入力",
        "check": "答えを確認",
        "correct": "正解です！よくできました。",
        "not_quite": "もう少しです。正解：{answer}",
        "why": "理由：{explanation}",
        "next": "次の問題",
        "see_results": "結果を見る",
        "complete_message": (
            "レッスン完了！{total}問中{correct}問正解しました。"
        ),
        "earned": (
            "{xp} XPと{coins}コインを獲得しました。"
            "次のレッスンが開きました。"
        ),
        "reviewed": (
            "復習を完了しました。"
            "報酬は各レッスンで一度だけです。"
        ),
        "failed": (
            "{total}問中{correct}問正解。"
            "合格には{needed}問必要です。"
        ),
        "review_help": (
            "単語とパターンを復習して、もう一度試してください。"
        ),
        "retry": "もう一度挑戦",
        "return_path": "学習コースに戻る",
        "path_complete": "初級学習コースを完了しました！",
        "not_available": (
            "この言語の学習コースはまだありません。"
        ),
    },
}


STAGES = [
    ("vocabulary", "words_stage", "📖"),
    ("grammar", "pattern_stage", "🧠"),
    ("exercise", "practice_stage", "✍️"),
    ("complete", "results_stage", "🏆"),
]


def _safe(value):
    return html.escape(str(value))


def _lt(key, **values):
    code = get_interface_language()
    message = LESSON_TEXT.get(
        code,
        LESSON_TEXT["en"],
    ).get(
        key,
        LESSON_TEXT["en"].get(key, key),
    )

    try:
        return message.format(**values)
    except (KeyError, ValueError):
        return message


def _apply_styles():
    st.markdown(
        """
        <style>
        .wf-learn-hero {
            position: relative;
            overflow: hidden;
            padding: clamp(1.5rem, 4vw, 2.3rem);
            margin: .4rem 0 1rem;
            border-radius: 28px;
            color: white;
            background:
                radial-gradient(
                    circle at 90% 15%,
                    rgba(255,255,255,.23),
                    transparent 28%
                ),
                linear-gradient(
                    135deg,
                    #0f766e,
                    #0891b2 52%,
                    #2563eb
                );
            box-shadow: 0 22px 48px rgba(8,145,178,.20);
        }

        .wf-learn-hero::after {
            content: "📚";
            position: absolute;
            right: 4%;
            bottom: -2.2rem;
            font-size: 9rem;
            opacity: .11;
            transform: rotate(-8deg);
        }

        .wf-learn-chip {
            position: relative;
            z-index: 1;
            display: inline-block;
            padding: .38rem .7rem;
            margin-bottom: .75rem;
            border: 1px solid rgba(255,255,255,.34);
            border-radius: 999px;
            background: rgba(255,255,255,.14);
            font-size: .78rem;
            font-weight: 850;
        }

        .wf-learn-hero h1 {
            position: relative;
            z-index: 1;
            margin: 0;
            color: white;
            font-size: clamp(2rem, 4vw, 3.1rem);
            letter-spacing: -.04em;
        }

        .wf-learn-hero p {
            position: relative;
            z-index: 1;
            max-width: 670px;
            margin: .5rem 0 1.2rem;
            color: rgba(255,255,255,.88);
        }

        .wf-learn-progress-head,
        .wf-learn-stage-row,
        .wf-lesson-top,
        .wf-word-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: .8rem;
        }

        .wf-learn-progress-head {
            position: relative;
            z-index: 1;
            margin-bottom: .42rem;
            font-size: .8rem;
            font-weight: 800;
        }

        .wf-learn-bar {
            position: relative;
            z-index: 1;
            overflow: hidden;
            height: 11px;
            border-radius: 999px;
            background: rgba(255,255,255,.24);
        }

        .wf-learn-bar span {
            display: block;
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg,#fde68a,white);
        }

        .wf-learn-stat {
            min-height: 118px;
            padding: 1rem;
            margin-bottom: .7rem;
            border: 1px solid rgba(148,163,184,.2);
            border-radius: 20px;
            background: var(--secondary-background-color);
            box-shadow: 0 10px 24px rgba(15,23,42,.055);
        }

        .wf-learn-stat-icon {
            font-size: 1.25rem;
        }

        .wf-learn-stat-value {
            margin-top: .45rem;
            color: var(--text-color);
            font-size: 1.45rem;
            font-weight: 900;
        }

        .wf-learn-stat-label {
            margin-top: .2rem;
            color: color-mix(
                in srgb,
                var(--text-color) 65%,
                transparent
            );
            font-size: .76rem;
            font-weight: 750;
        }

        .wf-learn-callout {
            padding: .9rem 1rem;
            margin: .4rem 0 1.25rem;
            border: 1px solid rgba(16,185,129,.25);
            border-radius: 16px;
            color: var(--text-color);
            background: rgba(16,185,129,.09);
            font-weight: 750;
        }

        .wf-learn-section {
            margin: 1.5rem 0 .75rem;
            color: var(--text-color);
            font-size: 1.35rem;
            font-weight: 900;
        }

        .wf-unit-copy {
            margin: -.2rem 0 .8rem;
            color: color-mix(
                in srgb,
                var(--text-color) 67%,
                transparent
            );
        }

        .wf-lesson-card {
            padding: 1rem;
            margin: .35rem 0 .7rem;
            border: 1px solid rgba(148,163,184,.22);
            border-radius: 19px;
            background: var(--secondary-background-color);
            box-shadow: 0 9px 22px rgba(15,23,42,.05);
        }

        .wf-lesson-card.locked {
            opacity: .58;
            box-shadow: none;
        }

        .wf-lesson-title {
            color: var(--text-color);
            font-size: 1.05rem;
            font-weight: 900;
        }

        .wf-lesson-copy {
            margin: .35rem 0 .65rem;
            color: color-mix(
                in srgb,
                var(--text-color) 68%,
                transparent
            );
            font-size: .86rem;
        }

        .wf-lesson-meta {
            display: flex;
            gap: .45rem;
            flex-wrap: wrap;
        }

        .wf-lesson-meta span {
            padding: .28rem .5rem;
            border-radius: 999px;
            color: #0369a1;
            background: rgba(14,165,233,.11);
            font-size: .7rem;
            font-weight: 800;
        }

        .wf-learn-stage-row {
            padding: .65rem;
            margin: .6rem 0 1.2rem;
            border-radius: 17px;
            background: rgba(148,163,184,.10);
        }

        .wf-learn-stage {
            flex: 1;
            padding: .5rem;
            border-radius: 12px;
            color: color-mix(
                in srgb,
                var(--text-color) 58%,
                transparent
            );
            text-align: center;
            font-size: .75rem;
            font-weight: 800;
        }

        .wf-learn-stage.active {
            color: white;
            background: linear-gradient(135deg,#0f766e,#0891b2);
            box-shadow: 0 8px 18px rgba(8,145,178,.2);
        }

        .wf-word-card {
            min-height: 245px;
            padding: 1.15rem;
            margin-bottom: .8rem;
            border: 1px solid rgba(14,165,233,.18);
            border-radius: 21px;
            background:
                linear-gradient(
                    145deg,
                    rgba(14,165,233,.07),
                    transparent 46%
                ),
                var(--secondary-background-color);
            box-shadow: 0 10px 24px rgba(15,23,42,.055);
        }

        .wf-word-number {
            display: grid;
            place-items: center;
            width: 31px;
            height: 31px;
            border-radius: 10px;
            color: #0369a1;
            background: rgba(14,165,233,.12);
            font-size: .75rem;
            font-weight: 900;
        }

        .wf-word-term {
            margin: .75rem 0 .3rem;
            color: var(--text-color);
            font-size: clamp(1.25rem,2.4vw,1.6rem);
            font-weight: 900;
        }

        .wf-word-pronunciation {
            display: inline-block;
            padding: .27rem .55rem;
            margin-bottom: .8rem;
            border-radius: 999px;
            color: #6d28d9;
            background: rgba(139,92,246,.11);
            font-size: .76rem;
            font-weight: 800;
        }

        .wf-word-label {
            color: color-mix(
                in srgb,
                var(--text-color) 57%,
                transparent
            );
            font-size: .68rem;
            font-weight: 900;
            letter-spacing: .07em;
            text-transform: uppercase;
        }

        .wf-word-meaning {
            margin: .18rem 0 .75rem;
            color: var(--text-color);
            font-weight: 760;
        }

        .wf-word-example {
            padding: .7rem .8rem;
            border-left: 4px solid #10b981;
            border-radius: 0 12px 12px 0;
            background: rgba(16,185,129,.08);
            color: var(--text-color);
            line-height: 1.45;
        }

        .wf-word-example small {
            display: block;
            margin-top: .25rem;
            color: color-mix(
                in srgb,
                var(--text-color) 65%,
                transparent
            );
        }

        .wf-pattern-card {
            padding: clamp(1.2rem,3vw,1.7rem);
            margin: .7rem 0 1rem;
            border: 1px solid rgba(139,92,246,.22);
            border-radius: 22px;
            background:
                radial-gradient(
                    circle at 95% 10%,
                    rgba(139,92,246,.14),
                    transparent 30%
                ),
                var(--secondary-background-color);
            box-shadow: 0 12px 28px rgba(15,23,42,.06);
        }

        .wf-pattern-card h3 {
            margin: 0 0 .45rem;
            color: var(--text-color);
        }

        .wf-pattern-card p {
            margin: 0;
            color: color-mix(
                in srgb,
                var(--text-color) 75%,
                transparent
            );
            line-height: 1.65;
        }

        @media (max-width:700px) {
            .wf-learn-hero {
                border-radius: 22px;
            }

            .wf-learn-hero::after {
                font-size: 6rem;
            }

            .wf-learn-stage {
                font-size: .64rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _normalize(value):
    text = unicodedata.normalize(
        "NFKC",
        str(value),
    )
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
    normalized = _normalize(candidate)

    return any(
        normalized == _normalize(answer)
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
    if _find_lesson(course, lesson_id) is None:
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


def _home_button(key):
    if st.button(
        f"← {t('home')}",
        key=key,
    ):
        st.session_state.current_view = "Home"
        st.session_state.pop(
            "course_lesson_run",
            None,
        )
        st.rerun()


def _hero(course, progress):
    flat_lessons = _all_lessons(course)
    total = len(flat_lessons)
    completed = len(progress["completed_lessons"])
    percentage = min(
        completed / max(total, 1) * 100,
        100,
    )
    native_name = course.get(
        "native_name",
        course["language"],
    )
    code = course.get(
        "language_code",
        course["language"][:2].upper(),
    )

    st.markdown(
        (
            '<section class="wf-learn-hero">'
            '<div class="wf-learn-chip">'
            f'🌍 {_safe(code)} · '
            f'{_safe(course["language"])} · '
            f'{_safe(native_name)}'
            "</div>"
            f'<h1>📚 {_safe(_lt("title"))}</h1>'
            f'<p>{_safe(_lt("subtitle"))}</p>'
            '<div class="wf-learn-progress-head">'
            f'<span>{_safe(_lt("course_progress"))}</span>'
            f"<span>{completed}/{total}</span>"
            '</div><div class="wf-learn-bar">'
            f'<span style="width:{percentage:.0f}%"></span>'
            "</div></section>"
        ),
        unsafe_allow_html=True,
    )

    columns = st.columns(3)
    stats = [
        (
            "🎯",
            course["level"],
            _lt("level"),
        ),
        (
            "✅",
            f"{completed}/{total}",
            _lt("completed"),
        ),
        (
            "🪙",
            st.session_state.coins,
            t("coins"),
        ),
    ]

    for column, (
        icon,
        value,
        label,
    ) in zip(columns, stats):
        with column:
            st.markdown(
                (
                    '<div class="wf-learn-stat">'
                    '<div class="wf-learn-stat-icon">'
                    f"{icon}</div>"
                    '<div class="wf-learn-stat-value">'
                    f"{_safe(value)}</div>"
                    '<div class="wf-learn-stat-label">'
                    f"{_safe(label)}</div></div>"
                ),
                unsafe_allow_html=True,
            )

    st.markdown(
        (
            '<div class="wf-learn-callout">'
            f'💡 {_safe(_lt("learn_first"))}'
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    if completed == total and total:
        st.success(_lt("path_complete"))


def _lesson_card(
    lesson,
    completed,
    unlocked,
):
    if completed:
        status_icon = "✅"
    elif unlocked:
        status_icon = "▶️"
    else:
        status_icon = "🔒"

    state_class = "" if unlocked else "locked"

    st.markdown(
        (
            f'<div class="wf-lesson-card {state_class}">'
            '<div class="wf-lesson-top">'
            '<div class="wf-lesson-title">'
            f'{status_icon} {lesson["icon"]} '
            f'{_safe(lesson["title"])}'
            "</div></div>"
            '<div class="wf-lesson-copy">'
            f'{_safe(lesson["objective"])}'
            "</div>"
            '<div class="wf-lesson-meta">'
            "<span>⏱️ "
            f'{_safe(_lt("minutes", count=lesson["estimated_minutes"]))}'
            "</span>"
            f'<span>✨ {lesson["xp_reward"]} XP</span>'
            "<span>🪙 "
            f'{_safe(_lt("coins", count=lesson["coin_reward"]))}'
            "</span></div></div>"
        ),
        unsafe_allow_html=True,
    )


def _render_path(course):
    progress = _course_progress(course["language"])
    completed_ids = set(progress["completed_lessons"])
    flat_lessons = _all_lessons(course)

    _home_button("learning_path_home")
    _hero(course, progress)

    st.markdown(
        (
            '<div class="wf-learn-section">'
            f'🗺️ {_safe(_lt("course_units"))}'
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    flat_position = 0

    for unit_number, unit in enumerate(
        course["units"],
        start=1,
    ):
        unit_completed = sum(
            lesson["id"] in completed_ids
            for lesson in unit["lessons"]
        )

        label = (
            f'{unit["icon"]} '
            f'{_lt("unit", number=unit_number)}: '
            f'{unit["title"]} '
            f'({unit_completed}/{len(unit["lessons"])})'
        )

        with st.expander(
            label,
            expanded=(
                unit_number == 1
                or unit_completed < len(unit["lessons"])
            ),
        ):
            st.markdown(
                (
                    '<div class="wf-unit-copy">'
                    f'{_safe(unit["description"])}'
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

            for lesson in unit["lessons"]:
                lesson_id = lesson["id"]
                completed = lesson_id in completed_ids
                unlocked = _lesson_is_unlocked(
                    flat_lessons,
                    flat_position,
                    completed_ids,
                )
                details, action = st.columns(
                    [4.5, 1.2]
                )

                with details:
                    _lesson_card(
                        lesson,
                        completed,
                        unlocked,
                    )

                with action:
                    st.write("")
                    st.write("")

                    if st.button(
                        (
                            _lt("review")
                            if completed
                            else _lt("start")
                        ),
                        key=f"start_course_{lesson_id}",
                        type=(
                            "primary"
                            if unlocked and not completed
                            else "secondary"
                        ),
                        disabled=not unlocked,
                        use_container_width=True,
                    ):
                        _start_lesson(
                            course,
                            lesson_id,
                        )
                        st.rerun()

                flat_position += 1


def _stage_row(active_stage):
    active_index = next(
        (
            index
            for index, (
                stage,
                _,
                _,
            ) in enumerate(STAGES)
            if stage == active_stage
        ),
        0,
    )
    pieces = []

    for index, (
        _,
        label_key,
        icon,
    ) in enumerate(STAGES):
        state = (
            "active"
            if index == active_index
            else ""
        )
        pieces.append(
            (
                f'<div class="wf-learn-stage {state}">'
                f"{icon} {_safe(_lt(label_key))}"
                "</div>"
            )
        )

    st.markdown(
        (
            '<div class="wf-learn-stage-row">'
            + "".join(pieces)
            + "</div>"
        ),
        unsafe_allow_html=True,
    )


def _lesson_title(
    course,
    lesson,
    stage,
):
    if st.button(
        f"← {_lt('return_path')}",
        key="back_to_course_path",
    ):
        _return_to_path()

    native_name = course.get(
        "native_name",
        course["language"],
    )

    st.caption(
        f'{course["language"]} · '
        f"{native_name} · "
        f'{course["level"]}'
    )
    st.title(
        f'{lesson["icon"]} '
        f'{lesson["title"]}'
    )
    st.write(lesson["objective"])
    _stage_row(stage)


@st.cache_data(show_spinner=False)
def _reference_audio(text, language):
    return generate_reference_audio(
        text,
        language,
        False,
    )


def _audio_text(item):
    value = item.get(
        "audio_text",
        item["term"],
    )

    return re.sub(
        r"\s*\([^)]*\)\s*",
        "",
        value,
    ).strip()


def _word_card(item, number):
    pronunciation = item.get(
        "pronunciation",
        "",
    )
    example_meaning = item.get(
        "example_meaning",
        "",
    )
    top_label = (
        _lt("pronunciation")
        if pronunciation
        else ""
    )

    if pronunciation:
        pronunciation_html = (
            '<div class="wf-word-pronunciation">'
            f"🔤 {_safe(pronunciation)}"
            "</div>"
        )
    else:
        pronunciation_html = ""

    if example_meaning:
        example_meaning_html = (
            "<small>"
            f'{_safe(_lt("example_meaning"))}: '
            f"{_safe(example_meaning)}"
            "</small>"
        )
    else:
        example_meaning_html = ""

    st.markdown(
        (
            '<div class="wf-word-card">'
            '<div class="wf-word-top">'
            '<span class="wf-word-number">'
            f"{number}</span>"
            '<span class="wf-word-label">'
            f"{_safe(top_label)}</span>"
            "</div>"
            '<div class="wf-word-term">'
            f'{_safe(item["term"])}</div>'
            f"{pronunciation_html}"
            '<div class="wf-word-label">'
            f'{_safe(_lt("meaning"))}</div>'
            '<div class="wf-word-meaning">'
            f'{_safe(item["meaning"])}</div>'
            '<div class="wf-word-label">'
            f'{_safe(_lt("example"))}</div>'
            '<div class="wf-word-example">'
            f'{_safe(item["example"])}'
            f"{example_meaning_html}"
            "</div></div>"
        ),
        unsafe_allow_html=True,
    )


def _render_vocabulary(
    course,
    lesson,
    run,
):
    _lesson_title(
        course,
        lesson,
        run["stage"],
    )

    st.markdown(
        f"## {_lt('learn_words')}"
    )
    st.write(_lt("learn_words_help"))

    columns = st.columns(2)

    for index, item in enumerate(
        lesson["vocabulary"]
    ):
        with columns[index % 2]:
            _word_card(
                item,
                index + 1,
            )

            if st.button(
                f"🔊 {_lt('listen')}",
                key=(
                    f'listen_{lesson["id"]}_{index}'
                ),
                use_container_width=True,
            ):
                result = _reference_audio(
                    _audio_text(item),
                    course["language"],
                )

                if result["success"]:
                    st.audio(
                        result["audio"],
                        format="audio/mp3",
                    )
                else:
                    st.warning(
                        _lt("audio_error")
                    )

    if st.button(
        f"{_lt('continue_pattern')} →",
        type="primary",
        key=(
            f'vocabulary_done_{lesson["id"]}'
        ),
        use_container_width=True,
    ):
        run["stage"] = "grammar"
        st.rerun()


def _render_grammar(
    course,
    lesson,
    run,
):
    _lesson_title(
        course,
        lesson,
        run["stage"],
    )

    st.markdown(
        f"## {_lt('understand')}"
    )
    st.write(_lt("understand_help"))

    st.markdown(
        (
            '<div class="wf-pattern-card">'
            f'<h3>🧠 {_safe(lesson["grammar"]["title"])}</h3>'
            f'<p>{_safe(lesson["grammar"]["summary"])}</p>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    st.info(_lt("practice_notice"))

    if st.button(
        f"{_lt('start_practice')} →",
        type="primary",
        key=f'grammar_done_{lesson["id"]}',
        use_container_width=True,
    ):
        run["stage"] = "exercise"
        st.rerun()


def _exercise_input(
    exercise,
    lesson_id,
    exercise_index,
):
    widget_key = (
        f"course_answer_{lesson_id}_"
        f"{exercise_index}"
    )
    exercise_type = exercise["type"]

    if exercise_type == "multiple_choice":
        return st.radio(
            _lt("choose_answer"),
            exercise["options"],
            index=None,
            key=widget_key,
        )

    if (
        exercise_type == "fill_blank"
        and exercise["options"]
    ):
        return st.radio(
            _lt("choose_word"),
            exercise["options"],
            index=None,
            key=widget_key,
        )

    if exercise_type == "word_order":
        words = list(exercise["words"])
        random.Random(
            f"{lesson_id}_{exercise_index}"
        ).shuffle(words)

        st.write(_lt("arrange_help"))
        st.info("   ·   ".join(words))

        return st.text_input(
            _lt("your_sentence"),
            key=widget_key,
        )

    return st.text_input(
        _lt("type_answer"),
        key=widget_key,
    )


def _render_exercise(
    course,
    lesson,
    run,
):
    _lesson_title(
        course,
        lesson,
        run["stage"],
    )

    exercises = lesson["exercises"]
    index = run["exercise_index"]
    exercise = exercises[index]

    st.markdown(
        (
            "## "
            + _lt(
                "practice",
                current=index + 1,
                total=len(exercises),
            )
        )
    )
    st.progress(
        index / len(exercises)
    )
    st.markdown(
        f'### {exercise["prompt"]}'
    )

    candidate = _exercise_input(
        exercise,
        lesson["id"],
        index,
    )
    answer_ready = (
        candidate is not None
        and str(candidate).strip()
    )

    if (
        not run["answered"]
        and st.button(
            _lt("check"),
            type="primary",
            disabled=not answer_ready,
            key=f'check_{lesson["id"]}_{index}',
        )
    ):
        run["was_correct"] = _is_correct(
            candidate,
            exercise,
        )
        run["answered"] = True
        run["attempted_answers"] += 1

        if run["was_correct"]:
            run["correct_answers"] += 1

        st.rerun()

    if not run["answered"]:
        return

    if run["was_correct"]:
        st.success(_lt("correct"))
    else:
        st.error(
            _lt(
                "not_quite",
                answer=exercise["answer"],
            )
        )

    st.info(
        _lt(
            "why",
            explanation=exercise["explanation"],
        )
    )

    final_exercise = (
        index == len(exercises) - 1
    )
    label = (
        _lt("see_results")
        if final_exercise
        else _lt("next")
    )

    if st.button(
        f"{label} →",
        type="primary",
        key=f'next_{lesson["id"]}_{index}',
    ):
        if final_exercise:
            run["stage"] = "complete"
        else:
            run["exercise_index"] += 1
            run["answered"] = False
            run["was_correct"] = False

        st.rerun()


def _award_lesson(
    course,
    lesson,
    run,
):
    progress = _course_progress(
        course["language"]
    )
    lesson_id = lesson["id"]

    if lesson_id in progress["completed_lessons"]:
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

    skills = language_progress.get(
        "skill_levels",
        {},
    )

    if "Vocabulary" in skills:
        skills["Vocabulary"] += 1

    if "Grammar" in skills:
        skills["Grammar"] += 1

    run["rewarded"] = True
    return True


def _render_complete(
    course,
    lesson,
    run,
):
    _lesson_title(
        course,
        lesson,
        "complete",
    )

    total = len(lesson["exercises"])
    correct = run["correct_answers"]
    passing_score = max(
        1,
        (total * 2 + 2) // 3,
    )

    if correct >= passing_score:
        newly_completed = False

        if not run["rewarded"]:
            newly_completed = _award_lesson(
                course,
                lesson,
                run,
            )

        st.success(
            _lt(
                "complete_message",
                correct=correct,
                total=total,
            )
        )

        if newly_completed:
            st.balloons()
            st.info(
                _lt(
                    "earned",
                    xp=lesson["xp_reward"],
                    coins=lesson["coin_reward"],
                )
            )
        else:
            st.info(_lt("reviewed"))

        if st.button(
            _lt("return_path"),
            type="primary",
            key=f'complete_path_{lesson["id"]}',
        ):
            _return_to_path()

        return

    st.error(
        _lt(
            "failed",
            correct=correct,
            total=total,
            needed=passing_score,
        )
    )
    st.write(_lt("review_help"))

    retry, path = st.columns(2)

    with retry:
        if st.button(
            _lt("retry"),
            type="primary",
            key=f'retry_{lesson["id"]}',
            use_container_width=True,
        ):
            _start_lesson(
                course,
                lesson["id"],
            )
            st.rerun()

    with path:
        if st.button(
            _lt("return_path"),
            key=f'failed_path_{lesson["id"]}',
            use_container_width=True,
        ):
            _return_to_path()


def _render_active_lesson(
    course,
    run,
):
    lesson = _find_lesson(
        course,
        run["lesson_id"],
    )

    if lesson is None:
        _return_to_path()
        return

    if run["stage"] == "vocabulary":
        _render_vocabulary(
            course,
            lesson,
            run,
        )
    elif run["stage"] == "grammar":
        _render_grammar(
            course,
            lesson,
            run,
        )
    elif run["stage"] == "exercise":
        _render_exercise(
            course,
            lesson,
            run,
        )
    else:
        _render_complete(
            course,
            lesson,
            run,
        )


def render_lessons():
    _apply_styles()

    language = st.session_state.active_language
    course = get_course(language)

    if course is None:
        _home_button("unsupported_course_home")
        st.title(f"📚 {_lt('title')}")
        st.info(_lt("not_available"))
        return

    run = st.session_state.get(
        "course_lesson_run"
    )

    if (
        run
        and run.get("language") == course["language"]
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