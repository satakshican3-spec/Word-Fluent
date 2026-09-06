import html

import streamlit as st

from core.config import LANGUAGES, LEVELS, MAX_HEARTS, SKILL_COLORS
from locales import get_interface_language, t


TEXT = {
    "en": {
        "title": "Your Progress",
        "subtitle": "See your momentum, goals, and growing skills.",
        "journey": "Course journey",
        "levels": "{current} of {total} levels unlocked",
        "not_selected": "Not selected",
        "xp": "Overall XP",
        "streak": "Current streak",
        "time": "Learning time",
        "weekly": "Weekly goal",
        "weekly_help": "A little practice each week adds up.",
        "goal_complete": "Weekly goal complete!",
        "remaining": "{count} min remaining",
        "complete": "{count}% complete",
        "goal_setting": "Weekly learning goal",
        "minutes": "{count} minutes",
        "pause": "Pause this language",
        "pause_help": "Your streak stays safe while this language is paused.",
        "paused": "{language} is paused. Your streak is protected.",
        "skills": "Skill progress",
        "skills_help": "Every activity strengthens a different part of your fluency.",
        "points": "{current}/{goal} practice points",
        "level": "Level {level}",
        "achievements": "Achievements",
        "achievements_help": "Keep practising to turn every badge into colour.",
        "unlocked_count": "{current}/{total} unlocked",
        "unlocked": "Unlocked",
        "locked": "Locked",
        "choose_level": "Choose your starting level first",
        "choose_level_help": "Return home and choose a level to start tracking this language.",
        "return_home": "Choose a level on Home",
        "Vocabulary": "Vocabulary",
        "Grammar": "Grammar",
        "Listening": "Listening",
        "Speaking": "Speaking",
        "Pronunciation": "Pronunciation",
        "Sentence Builder": "Sentence Builder",
        "first": "First Steps",
        "first_help": "Earn your first XP.",
        "sentence": "Sentence Starter",
        "sentence_help": "Complete a Sentence Builder challenge.",
        "voice": "Voice Starter",
        "voice_help": "Complete a pronunciation challenge.",
        "fire": "Five-Day Fire",
        "fire_help": "Reach a five-day learning streak.",
        "goal": "Goal Getter",
        "goal_help": "Complete your weekly learning goal.",
        "climber": "Skill Climber",
        "climber_help": "Raise any skill to level 2.",
    },
    "bn": {
        "title": "আপনার অগ্রগতি",
        "subtitle": "আপনার ধারাবাহিকতা, লক্ষ্য এবং বেড়ে ওঠা দক্ষতা দেখুন।",
        "journey": "কোর্সের যাত্রা",
        "levels": "{total}টির মধ্যে {current}টি স্তর আনলক",
        "not_selected": "বেছে নেওয়া হয়নি",
        "xp": "মোট XP",
        "streak": "বর্তমান স্ট্রিক",
        "time": "শেখার সময়",
        "weekly": "সাপ্তাহিক লক্ষ্য",
        "weekly_help": "প্রতি সপ্তাহের অল্প অনুশীলনও বড় ফল দেয়।",
        "goal_complete": "সাপ্তাহিক লক্ষ্য পূর্ণ!",
        "remaining": "আর {count} মিনিট বাকি",
        "complete": "{count}% সম্পূর্ণ",
        "goal_setting": "সাপ্তাহিক শেখার লক্ষ্য",
        "minutes": "{count} মিনিট",
        "pause": "এই ভাষাটি বিরতিতে রাখুন",
        "pause_help": "ভাষাটি বিরতিতে থাকলে আপনার স্ট্রিক নিরাপদ থাকবে।",
        "paused": "{language} বিরতিতে আছে। আপনার স্ট্রিক সুরক্ষিত।",
        "skills": "দক্ষতার অগ্রগতি",
        "skills_help": "প্রতিটি কার্যক্রম আপনার সাবলীলতার আলাদা অংশ উন্নত করে।",
        "points": "{current}/{goal} অনুশীলন পয়েন্ট",
        "level": "স্তর {level}",
        "achievements": "অর্জন",
        "achievements_help": "সব ব্যাজ রঙিন করতে অনুশীলন চালিয়ে যান।",
        "unlocked_count": "{current}/{total} আনলক",
        "unlocked": "আনলক হয়েছে",
        "locked": "লক করা",
        "choose_level": "প্রথমে আপনার শুরুর স্তর বেছে নিন",
        "choose_level_help": "অগ্রগতি শুরু করতে হোমে ফিরে একটি স্তর বেছে নিন।",
        "return_home": "হোমে স্তর বেছে নিন",
        "Vocabulary": "শব্দভাণ্ডার",
        "Grammar": "ব্যাকরণ",
        "Listening": "শোনা",
        "Speaking": "কথা বলা",
        "Pronunciation": "উচ্চারণ",
        "Sentence Builder": "বাক্য নির্মাতা",
        "first": "প্রথম পদক্ষেপ",
        "first_help": "আপনার প্রথম XP অর্জন করুন।",
        "sentence": "বাক্যের শুরু",
        "sentence_help": "একটি বাক্য নির্মাণ চ্যালেঞ্জ শেষ করুন।",
        "voice": "কণ্ঠের শুরু",
        "voice_help": "একটি উচ্চারণ চ্যালেঞ্জ শেষ করুন।",
        "fire": "পাঁচ দিনের আগুন",
        "fire_help": "পাঁচ দিনের শেখার স্ট্রিক অর্জন করুন।",
        "goal": "লক্ষ্য বিজয়ী",
        "goal_help": "আপনার সাপ্তাহিক লক্ষ্য পূর্ণ করুন।",
        "climber": "দক্ষতায় উন্নতি",
        "climber_help": "যেকোনো দক্ষতা স্তর ২-এ নিন।",
    },
    "hi": {
        "title": "आपकी प्रगति",
        "subtitle": "अपनी गति, लक्ष्य और बढ़ते कौशल देखें।",
        "journey": "कोर्स यात्रा",
        "levels": "{total} में से {current} स्तर अनलॉक",
        "not_selected": "चुना नहीं गया",
        "xp": "कुल XP",
        "streak": "वर्तमान स्ट्रीक",
        "time": "सीखने का समय",
        "weekly": "साप्ताहिक लक्ष्य",
        "weekly_help": "हर सप्ताह थोड़ा अभ्यास भी बड़ा परिणाम देता है।",
        "goal_complete": "साप्ताहिक लक्ष्य पूरा!",
        "remaining": "{count} मिनट बाकी",
        "complete": "{count}% पूरा",
        "goal_setting": "साप्ताहिक सीखने का लक्ष्य",
        "minutes": "{count} मिनट",
        "pause": "इस भाषा को रोकें",
        "pause_help": "भाषा रुकी होने पर आपकी स्ट्रीक सुरक्षित रहेगी।",
        "paused": "{language} रुकी हुई है। आपकी स्ट्रीक सुरक्षित है।",
        "skills": "कौशल प्रगति",
        "skills_help": "हर गतिविधि आपकी भाषा की अलग क्षमता को मजबूत करती है।",
        "points": "{current}/{goal} अभ्यास अंक",
        "level": "स्तर {level}",
        "achievements": "उपलब्धियाँ",
        "achievements_help": "हर बैज को रंगीन बनाने के लिए अभ्यास करते रहें।",
        "unlocked_count": "{current}/{total} अनलॉक",
        "unlocked": "अनलॉक",
        "locked": "लॉक",
        "choose_level": "पहले अपना शुरुआती स्तर चुनें",
        "choose_level_help": "प्रगति शुरू करने के लिए होम पर स्तर चुनें।",
        "return_home": "होम पर स्तर चुनें",
        "Vocabulary": "शब्दावली",
        "Grammar": "व्याकरण",
        "Listening": "सुनना",
        "Speaking": "बोलना",
        "Pronunciation": "उच्चारण",
        "Sentence Builder": "वाक्य निर्माता",
        "first": "पहला कदम",
        "first_help": "अपना पहला XP कमाएँ।",
        "sentence": "वाक्य की शुरुआत",
        "sentence_help": "एक वाक्य निर्माण चुनौती पूरी करें।",
        "voice": "आवाज़ की शुरुआत",
        "voice_help": "एक उच्चारण चुनौती पूरी करें।",
        "fire": "पाँच दिन की आग",
        "fire_help": "पाँच दिन की सीखने की स्ट्रीक बनाएँ।",
        "goal": "लक्ष्य विजेता",
        "goal_help": "अपना साप्ताहिक लक्ष्य पूरा करें।",
        "climber": "कौशल पर्वतारोही",
        "climber_help": "किसी कौशल को स्तर 2 तक पहुँचाएँ।",
    },
    "fr": {
        "title": "Votre progression",
        "subtitle": "Suivez votre élan, vos objectifs et vos compétences.",
        "journey": "Parcours du cours",
        "levels": "{current} niveaux sur {total} débloqués",
        "not_selected": "Non sélectionné",
        "xp": "XP total",
        "streak": "Série actuelle",
        "time": "Temps d’apprentissage",
        "weekly": "Objectif hebdomadaire",
        "weekly_help": "Un peu de pratique chaque semaine fait la différence.",
        "goal_complete": "Objectif hebdomadaire atteint !",
        "remaining": "Encore {count} min",
        "complete": "{count}% terminé",
        "goal_setting": "Objectif d’apprentissage hebdomadaire",
        "minutes": "{count} minutes",
        "pause": "Mettre cette langue en pause",
        "pause_help": "Votre série reste protégée pendant la pause.",
        "paused": "Le cours de {language} est en pause.",
        "skills": "Progression des compétences",
        "skills_help": "Chaque activité renforce une partie différente de votre maîtrise.",
        "points": "{current}/{goal} points de pratique",
        "level": "Niveau {level}",
        "achievements": "Réussites",
        "achievements_help": "Continuez à pratiquer pour colorer chaque badge.",
        "unlocked_count": "{current}/{total} débloqués",
        "unlocked": "Débloqué",
        "locked": "Verrouillé",
        "choose_level": "Choisissez d’abord votre niveau de départ",
        "choose_level_help": "Retournez à l’accueil et choisissez un niveau.",
        "return_home": "Choisir un niveau à l’accueil",
        "Vocabulary": "Vocabulaire",
        "Grammar": "Grammaire",
        "Listening": "Écoute",
        "Speaking": "Expression orale",
        "Pronunciation": "Prononciation",
        "Sentence Builder": "Constructeur de phrases",
        "first": "Premiers pas",
        "first_help": "Gagnez votre premier XP.",
        "sentence": "Début en phrases",
        "sentence_help": "Terminez un défi de construction de phrase.",
        "voice": "Première voix",
        "voice_help": "Terminez un défi de prononciation.",
        "fire": "Flamme de cinq jours",
        "fire_help": "Atteignez une série de cinq jours.",
        "goal": "Objectif atteint",
        "goal_help": "Terminez votre objectif hebdomadaire.",
        "climber": "Compétence en hausse",
        "climber_help": "Montez une compétence au niveau 2.",
    },
    "es": {
        "title": "Tu progreso",
        "subtitle": "Mira tu impulso, tus objetivos y tus habilidades.",
        "journey": "Ruta del curso",
        "levels": "{current} de {total} niveles desbloqueados",
        "not_selected": "Sin seleccionar",
        "xp": "XP total",
        "streak": "Racha actual",
        "time": "Tiempo de estudio",
        "weekly": "Objetivo semanal",
        "weekly_help": "Un poco de práctica cada semana suma mucho.",
        "goal_complete": "¡Objetivo semanal completado!",
        "remaining": "Faltan {count} min",
        "complete": "{count}% completado",
        "goal_setting": "Objetivo semanal de aprendizaje",
        "minutes": "{count} minutos",
        "pause": "Pausar este idioma",
        "pause_help": "Tu racha estará protegida mientras esté pausado.",
        "paused": "{language} está pausado. Tu racha está protegida.",
        "skills": "Progreso de habilidades",
        "skills_help": "Cada actividad fortalece una parte diferente de tu fluidez.",
        "points": "{current}/{goal} puntos de práctica",
        "level": "Nivel {level}",
        "achievements": "Logros",
        "achievements_help": "Sigue practicando para llenar de color cada insignia.",
        "unlocked_count": "{current}/{total} desbloqueados",
        "unlocked": "Desbloqueado",
        "locked": "Bloqueado",
        "choose_level": "Primero elige tu nivel inicial",
        "choose_level_help": "Vuelve al inicio y elige un nivel.",
        "return_home": "Elegir un nivel en Inicio",
        "Vocabulary": "Vocabulario",
        "Grammar": "Gramática",
        "Listening": "Comprensión auditiva",
        "Speaking": "Expresión oral",
        "Pronunciation": "Pronunciación",
        "Sentence Builder": "Constructor de frases",
        "first": "Primeros pasos",
        "first_help": "Consigue tu primer XP.",
        "sentence": "Primera frase",
        "sentence_help": "Completa un reto del Constructor de frases.",
        "voice": "Primera voz",
        "voice_help": "Completa un reto de pronunciación.",
        "fire": "Fuego de cinco días",
        "fire_help": "Alcanza una racha de cinco días.",
        "goal": "Meta conseguida",
        "goal_help": "Completa tu objetivo semanal.",
        "climber": "Habilidad en ascenso",
        "climber_help": "Sube cualquier habilidad al nivel 2.",
    },
    "ko": {
        "title": "나의 학습 진도",
        "subtitle": "학습 흐름, 목표, 성장하는 실력을 확인하세요.",
        "journey": "코스 여정",
        "levels": "{total}개 중 {current}개 레벨 잠금 해제",
        "not_selected": "선택하지 않음",
        "xp": "전체 XP",
        "streak": "현재 연속 학습",
        "time": "학습 시간",
        "weekly": "주간 목표",
        "weekly_help": "매주 조금씩 연습하면 큰 변화가 생깁니다.",
        "goal_complete": "주간 목표 달성!",
        "remaining": "{count}분 남음",
        "complete": "{count}% 완료",
        "goal_setting": "주간 학습 목표",
        "minutes": "{count}분",
        "pause": "이 언어 일시 정지",
        "pause_help": "일시 정지 중에도 연속 학습 기록은 보호됩니다.",
        "paused": "{language} 학습이 일시 정지되었습니다.",
        "skills": "기술 진도",
        "skills_help": "각 활동은 유창성의 서로 다른 부분을 키워 줍니다.",
        "points": "연습 포인트 {current}/{goal}",
        "level": "레벨 {level}",
        "achievements": "업적",
        "achievements_help": "계속 연습해서 모든 배지를 컬러로 바꿔 보세요.",
        "unlocked_count": "{current}/{total} 잠금 해제",
        "unlocked": "잠금 해제",
        "locked": "잠김",
        "choose_level": "먼저 시작 레벨을 선택하세요",
        "choose_level_help": "홈으로 돌아가 레벨을 선택하세요.",
        "return_home": "홈에서 레벨 선택",
        "Vocabulary": "어휘",
        "Grammar": "문법",
        "Listening": "듣기",
        "Speaking": "말하기",
        "Pronunciation": "발음",
        "Sentence Builder": "문장 만들기",
        "first": "첫걸음",
        "first_help": "첫 XP를 획득하세요.",
        "sentence": "첫 문장",
        "sentence_help": "문장 만들기 도전을 완료하세요.",
        "voice": "첫 목소리",
        "voice_help": "발음 도전을 완료하세요.",
        "fire": "5일의 불꽃",
        "fire_help": "5일 연속 학습을 달성하세요.",
        "goal": "목표 달성",
        "goal_help": "주간 학습 목표를 완료하세요.",
        "climber": "실력 상승",
        "climber_help": "아무 기술이나 레벨 2로 올리세요.",
    },
    "ja": {
        "title": "学習の進捗",
        "subtitle": "学習の勢い、目標、伸びているスキルを確認しましょう。",
        "journey": "コースの道のり",
        "levels": "{total}レベル中{current}レベルをアンロック",
        "not_selected": "未選択",
        "xp": "合計XP",
        "streak": "現在の連続記録",
        "time": "学習時間",
        "weekly": "週間目標",
        "weekly_help": "毎週少しずつの練習が大きな力になります。",
        "goal_complete": "週間目標を達成しました！",
        "remaining": "残り{count}分",
        "complete": "{count}%完了",
        "goal_setting": "週間学習目標",
        "minutes": "{count}分",
        "pause": "この言語を一時停止",
        "pause_help": "一時停止中も連続記録は守られます。",
        "paused": "{language}は一時停止中です。",
        "skills": "スキルの進捗",
        "skills_help": "各アクティビティで流暢さの異なる部分が伸びます。",
        "points": "練習ポイント {current}/{goal}",
        "level": "レベル{level}",
        "achievements": "実績",
        "achievements_help": "練習を続けて、すべてのバッジに色を付けましょう。",
        "unlocked_count": "{current}/{total}アンロック",
        "unlocked": "アンロック済み",
        "locked": "ロック中",
        "choose_level": "まず開始レベルを選んでください",
        "choose_level_help": "ホームに戻ってレベルを選んでください。",
        "return_home": "ホームでレベルを選ぶ",
        "Vocabulary": "単語",
        "Grammar": "文法",
        "Listening": "リスニング",
        "Speaking": "スピーキング",
        "Pronunciation": "発音",
        "Sentence Builder": "文づくり",
        "first": "はじめの一歩",
        "first_help": "最初のXPを獲得しましょう。",
        "sentence": "最初の文",
        "sentence_help": "文づくりチャレンジを完了しましょう。",
        "voice": "最初の声",
        "voice_help": "発音チャレンジを完了しましょう。",
        "fire": "5日間の炎",
        "fire_help": "5日連続学習を達成しましょう。",
        "goal": "目標達成",
        "goal_help": "週間学習目標を達成しましょう。",
        "climber": "スキルアップ",
        "climber_help": "いずれかのスキルをレベル2にしましょう。",
    },
}


SKILL_ICONS = {
    "Vocabulary": "📖",
    "Grammar": "🧠",
    "Listening": "🎧",
    "Speaking": "💬",
    "Pronunciation": "🎙️",
    "Sentence Builder": "🧩",
}


def _safe(value):
    return html.escape(str(value))


def _text(key, **values):
    language = get_interface_language()
    message = TEXT.get(language, TEXT["en"]).get(
        key,
        TEXT["en"].get(key, key),
    )

    try:
        return message.format(**values)
    except (KeyError, ValueError):
        return message


def _level_name(level):
    if not level:
        return _text("not_selected")

    translation_key = (
        f"level_{str(level).lower().replace(' ', '_')}"
    )
    translated = t(translation_key)

    if translated == translation_key:
        return level

    return translated


def _apply_styles():
    st.markdown(
        """
        <style>
        .wf-pg-hero {
            position: relative;
            overflow: hidden;
            padding: 2rem;
            margin: .35rem 0 1.25rem;
            border: 1px solid rgba(99, 102, 241, .20);
            border-radius: 28px;
            color: white;
            background:
                radial-gradient(
                    circle at 88% 18%,
                    rgba(255,255,255,.24),
                    transparent 26%
                ),
                linear-gradient(
                    135deg,
                    #4338ca 0%,
                    #2563eb 52%,
                    #0891b2 100%
                );
            box-shadow: 0 22px 48px rgba(37,99,235,.20);
        }

        .wf-pg-hero::after {
            content: "🏆";
            position: absolute;
            right: 4%;
            bottom: -2.3rem;
            font-size: 9rem;
            opacity: .11;
            transform: rotate(-9deg);
        }

        .wf-pg-eyebrow {
            position: relative;
            z-index: 1;
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            padding: .36rem .72rem;
            margin-bottom: .8rem;
            border: 1px solid rgba(255,255,255,.32);
            border-radius: 999px;
            background: rgba(255,255,255,.15);
            font-size: .8rem;
            font-weight: 800;
            letter-spacing: .04em;
        }

        .wf-pg-hero h1 {
            position: relative;
            z-index: 1;
            margin: 0;
            color: white;
            font-size: clamp(2rem, 4vw, 3.2rem);
            letter-spacing: -.04em;
        }

        .wf-pg-hero p {
            position: relative;
            z-index: 1;
            max-width: 620px;
            margin: .45rem 0 1.35rem;
            color: rgba(255,255,255,.86);
            font-size: 1rem;
        }

        .wf-pg-journey-top,
        .wf-pg-weekly-head,
        .wf-pg-weekly-foot,
        .wf-pg-skill-head,
        .wf-pg-skill-foot {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: .8rem;
        }

        .wf-pg-journey-top {
            position: relative;
            z-index: 1;
            margin-bottom: .45rem;
            font-size: .82rem;
            font-weight: 750;
        }

        .wf-pg-journey,
        .wf-pg-bar {
            overflow: hidden;
            height: 11px;
            border-radius: 999px;
            background: rgba(148,163,184,.23);
        }

        .wf-pg-journey {
            position: relative;
            z-index: 1;
            background: rgba(255,255,255,.24);
        }

        .wf-pg-journey span,
        .wf-pg-bar span {
            display: block;
            height: 100%;
            border-radius: inherit;
        }

        .wf-pg-journey span {
            background: linear-gradient(90deg, #fde68a, white);
            box-shadow: 0 0 14px rgba(255,255,255,.75);
        }

        .wf-pg-stat {
            min-height: 142px;
            padding: 1.05rem 1.1rem;
            margin-bottom: .65rem;
            border: 1px solid rgba(148,163,184,.22);
            border-radius: 22px;
            background: var(--secondary-background-color);
            box-shadow: 0 12px 28px rgba(15,23,42,.07);
        }

        .wf-pg-stat-icon {
            display: inline-grid;
            place-items: center;
            width: 38px;
            height: 38px;
            margin-bottom: .7rem;
            border-radius: 12px;
            font-size: 1.15rem;
            background: var(--wf-stat-bg);
        }

        .wf-pg-stat-value {
            color: var(--text-color);
            font-size: 1.6rem;
            font-weight: 850;
            line-height: 1;
        }

        .wf-pg-stat-label {
            margin-top: .4rem;
            color: color-mix(
                in srgb,
                var(--text-color) 68%,
                transparent
            );
            font-size: .78rem;
            font-weight: 700;
        }

        .wf-pg-section {
            display: flex;
            align-items: end;
            justify-content: space-between;
            gap: 1rem;
            margin: 1.6rem 0 .8rem;
        }

        .wf-pg-section h2 {
            margin: 0;
            color: var(--text-color);
            font-size: 1.35rem;
            letter-spacing: -.02em;
        }

        .wf-pg-section p {
            margin: .2rem 0 0;
            color: color-mix(
                in srgb,
                var(--text-color) 66%,
                transparent
            );
            font-size: .87rem;
        }

        .wf-pg-count {
            flex: 0 0 auto;
            padding: .35rem .65rem;
            border-radius: 999px;
            color: #4338ca;
            background: rgba(99,102,241,.12);
            font-size: .76rem;
            font-weight: 850;
        }

        .wf-pg-weekly {
            padding: 1.2rem 1.25rem;
            border: 1px solid rgba(59,130,246,.18);
            border-radius: 22px;
            background: linear-gradient(
                135deg,
                rgba(59,130,246,.10),
                rgba(6,182,212,.06)
            );
        }

        .wf-pg-weekly-head {
            margin-bottom: .8rem;
        }

        .wf-pg-weekly-value {
            color: var(--text-color);
            font-size: 1.55rem;
            font-weight: 850;
        }

        .wf-pg-weekly-note {
            color: color-mix(
                in srgb,
                var(--text-color) 68%,
                transparent
            );
            font-size: .82rem;
            font-weight: 700;
        }

        .wf-pg-weekly .wf-pg-bar span {
            background: linear-gradient(90deg, #2563eb, #06b6d4);
        }

        .wf-pg-weekly-foot {
            margin-top: .65rem;
            font-size: .77rem;
            font-weight: 750;
        }

        .wf-pg-skill {
            min-height: 148px;
            padding: 1rem 1.05rem;
            margin-bottom: .8rem;
            border: 1px solid rgba(148,163,184,.20);
            border-radius: 20px;
            background: var(--secondary-background-color);
            box-shadow: 0 10px 24px rgba(15,23,42,.055);
        }

        .wf-pg-skill-head {
            margin-bottom: .85rem;
        }

        .wf-pg-skill-name {
            display: flex;
            align-items: center;
            gap: .65rem;
            min-width: 0;
            color: var(--text-color);
            font-weight: 820;
        }

        .wf-pg-skill-icon {
            display: inline-grid;
            flex: 0 0 auto;
            place-items: center;
            width: 38px;
            height: 38px;
            border-radius: 12px;
            background: var(--wf-skill-soft);
        }

        .wf-pg-skill-level {
            color: var(--wf-skill);
            font-size: .78rem;
            font-weight: 850;
        }

        .wf-pg-skill .wf-pg-bar span {
            background: var(--wf-skill);
        }

        .wf-pg-skill-foot {
            margin-top: .55rem;
            color: color-mix(
                in srgb,
                var(--text-color) 64%,
                transparent
            );
            font-size: .75rem;
            font-weight: 700;
        }

        .wf-pg-badge {
            min-height: 178px;
            padding: 1.15rem;
            margin-bottom: .75rem;
            border: 1px solid rgba(148,163,184,.22);
            border-radius: 22px;
            text-align: center;
            background: var(--secondary-background-color);
            box-shadow: 0 10px 24px rgba(15,23,42,.055);
        }

        .wf-pg-badge.locked {
            opacity: .56;
            filter: grayscale(.75);
            box-shadow: none;
        }

        .wf-pg-badge-icon {
            display: grid;
            place-items: center;
            width: 54px;
            height: 54px;
            margin: 0 auto .65rem;
            border-radius: 18px;
            background: linear-gradient(
                135deg,
                rgba(99,102,241,.16),
                rgba(6,182,212,.12)
            );
            font-size: 1.65rem;
        }

        .wf-pg-badge-title {
            color: var(--text-color);
            font-weight: 850;
        }

        .wf-pg-badge-help {
            min-height: 38px;
            margin: .28rem 0 .55rem;
            color: color-mix(
                in srgb,
                var(--text-color) 64%,
                transparent
            );
            font-size: .76rem;
            line-height: 1.35;
        }

        .wf-pg-badge-state {
            display: inline-block;
            padding: .25rem .55rem;
            border-radius: 999px;
            color: #047857;
            background: rgba(16,185,129,.12);
            font-size: .7rem;
            font-weight: 850;
        }

        .wf-pg-badge.locked .wf-pg-badge-state {
            color: var(--text-color);
            background: rgba(148,163,184,.16);
        }

        .wf-pg-empty {
            padding: 1.2rem;
            margin: 1rem 0;
            border: 1px solid rgba(245,158,11,.24);
            border-radius: 20px;
            background: rgba(245,158,11,.09);
        }

        .wf-pg-empty strong {
            display: block;
            margin-bottom: .25rem;
            color: var(--text-color);
        }

        @media (max-width: 760px) {
            .wf-pg-hero {
                padding: 1.4rem;
                border-radius: 22px;
            }

            .wf-pg-hero::after {
                font-size: 6rem;
            }

            .wf-pg-stat {
                min-height: 124px;
            }

            .wf-pg-section {
                align-items: start;
                flex-direction: column;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def unlock_achievements(language, progress):
    skills = progress.get("skill_levels", {})

    badges = []

    if progress.get("overall_xp", 0) > 0:
        badges.append("🌱 First Steps")

    if skills.get("Sentence Builder", 0) > 0:
        badges.append(f"🧩 {language} Sentence Starter")

    if skills.get("Pronunciation", 0) > 0:
        badges.append(f"🎙️ {language} Voice Starter")

    if progress.get("streak", 0) >= 5:
        badges.append(f"🔥 {language} Five-Day Streak")

    if progress.get("weekly_minutes", 0) >= max(
        progress.get("weekly_goal", 60),
        1,
    ):
        badges.append(f"🎯 {language} Weekly Goal")

    if max(skills.values(), default=0) >= 20:
        badges.append(f"🚀 {language} Skill Climber")

    for badge in badges:
        if badge not in st.session_state.achievements:
            st.session_state.achievements.append(badge)


def _render_back_button():
    if st.button(f"← {t('home')}"):
        st.session_state.current_view = "Home"
        st.rerun()


def _render_hero(language, progress):
    current_level = progress.get("current_level")
    unlocked = len(progress.get("unlocked_levels", []))
    total = len(LEVELS)

    journey_percent = min(
        max(unlocked / max(total, 1) * 100, 0),
        100,
    )

    language_details = LANGUAGES.get(language, {})
    native_name = language_details.get(
        "native_name",
        language,
    )

    st.markdown(
        (
            '<section class="wf-pg-hero">'
            '<div class="wf-pg-eyebrow">'
            f'🌍 {_safe(native_name)} · '
            f'{_safe(_level_name(current_level))}'
            '</div>'
            f'<h1>🏆 {_safe(_text("title"))}</h1>'
            f'<p>{_safe(_text("subtitle"))}</p>'
            '<div class="wf-pg-journey-top">'
            f'<span>{_safe(_text("journey"))}</span>'
            '<span>'
            f'{_safe(_text("levels", current=unlocked, total=total))}'
            '</span>'
            '</div>'
            '<div class="wf-pg-journey">'
            f'<span style="width:{journey_percent:.0f}%"></span>'
            '</div>'
            '</section>'
        ),
        unsafe_allow_html=True,
    )


def _stat_card(icon, value, label, color):
    st.markdown(
        (
            '<div class="wf-pg-stat" '
            f'style="--wf-stat-bg:{color}1f">'
            f'<div class="wf-pg-stat-icon">{icon}</div>'
            f'<div class="wf-pg-stat-value">{_safe(value)}</div>'
            f'<div class="wf-pg-stat-label">{_safe(label)}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def _render_stats(progress):
    columns = st.columns(4)

    values = [
        (
            "✨",
            progress.get("overall_xp", 0),
            _text("xp"),
            "#8B5CF6",
        ),
        (
            "🔥",
            t("days", count=progress.get("streak", 0)),
            _text("streak"),
            "#F97316",
        ),
        (
            "🪙",
            st.session_state.coins,
            t("coins"),
            "#F59E0B",
        ),
        (
            "❤️",
            f"{st.session_state.hearts}/{MAX_HEARTS}",
            t("hearts"),
            "#EF4444",
        ),
    ]

    for column, details in zip(columns, values):
        with column:
            _stat_card(*details)


def _section_heading(icon, title, description, count=""):
    count_html = ""

    if count:
        count_html = (
            f'<span class="wf-pg-count">{_safe(count)}</span>'
        )

    st.markdown(
        (
            '<div class="wf-pg-section">'
            '<div>'
            f'<h2>{icon} {_safe(title)}</h2>'
            f'<p>{_safe(description)}</p>'
            '</div>'
            f'{count_html}'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def _render_weekly_goal(language, progress):
    goal_options = [30, 60, 90, 120, 180]
    current_goal = progress.get("weekly_goal", 60)

    if current_goal not in goal_options:
        current_goal = 60

    _section_heading(
        "🎯",
        _text("weekly"),
        _text("weekly_help"),
    )

    goal_column, settings_column = st.columns([1.7, 1])

    with settings_column:
        selected_goal = st.selectbox(
            _text("goal_setting"),
            goal_options,
            index=goal_options.index(current_goal),
            format_func=lambda minutes: _text(
                "minutes",
                count=minutes,
            ),
            key=f"progress_goal_{language}",
        )

        progress["weekly_goal"] = selected_goal

        paused = st.toggle(
            _text("pause"),
            value=progress.get("paused", False),
            key=f"pause_progress_{language}",
            help=_text("pause_help"),
        )

        progress["paused"] = paused

    weekly_minutes = progress.get("weekly_minutes", 0)
    goal = max(progress.get("weekly_goal", 60), 1)

    percentage = min(
        max(weekly_minutes / goal * 100, 0),
        100,
    )

    remaining = max(goal - weekly_minutes, 0)

    if remaining == 0:
        note = _text("goal_complete")
    else:
        note = _text("remaining", count=remaining)

    with goal_column:
        st.markdown(
            (
                '<div class="wf-pg-weekly">'
                '<div class="wf-pg-weekly-head">'
                '<div class="wf-pg-weekly-value">'
                f'{weekly_minutes}/{goal} min'
                '</div>'
                '<div class="wf-pg-weekly-note">'
                f'{_safe(note)}'
                '</div>'
                '</div>'
                '<div class="wf-pg-bar">'
                f'<span style="width:{percentage:.0f}%"></span>'
                '</div>'
                '<div class="wf-pg-weekly-foot">'
                f'<span>{_safe(_text("time"))}</span>'
                '<span>'
                f'{_safe(_text("complete", count=round(percentage)))}'
                '</span>'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    if progress.get("paused"):
        st.warning(_text("paused", language=language))


def _render_skill_card(skill, points):
    color = SKILL_COLORS[skill]
    level = points // 20 + 1
    toward_next = points % 20
    percentage = toward_next / 20 * 100
    icon = SKILL_ICONS.get(skill, "⭐")

    st.markdown(
        (
            '<div class="wf-pg-skill" '
            f'style="--wf-skill:{color};'
            f'--wf-skill-soft:{color}1f">'
            '<div class="wf-pg-skill-head">'
            '<div class="wf-pg-skill-name">'
            '<span class="wf-pg-skill-icon">'
            f'{icon}'
            '</span>'
            f'<span>{_safe(_text(skill))}</span>'
            '</div>'
            '<span class="wf-pg-skill-level">'
            f'{_safe(_text("level", level=level))}'
            '</span>'
            '</div>'
            '<div class="wf-pg-bar">'
            f'<span style="width:{percentage:.0f}%"></span>'
            '</div>'
            '<div class="wf-pg-skill-foot">'
            '<span>'
            f'{_safe(_text("points", current=toward_next, goal=20))}'
            '</span>'
            f'<span>{round(percentage)}%</span>'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def _render_skills(progress):
    _section_heading(
        "📈",
        _text("skills"),
        _text("skills_help"),
    )

    left, right = st.columns(2)
    skill_columns = [left, right]

    for index, skill in enumerate(SKILL_COLORS):
        points = int(
            progress.get("skill_levels", {}).get(skill, 0)
        )

        with skill_columns[index % 2]:
            _render_skill_card(skill, points)


def _badge_specs(progress):
    skills = progress.get("skill_levels", {})

    return [
        (
            "🌱",
            "first",
            "first_help",
            progress.get("overall_xp", 0) > 0,
        ),
        (
            "🧩",
            "sentence",
            "sentence_help",
            skills.get("Sentence Builder", 0) > 0,
        ),
        (
            "🎙️",
            "voice",
            "voice_help",
            skills.get("Pronunciation", 0) > 0,
        ),
        (
            "🔥",
            "fire",
            "fire_help",
            progress.get("streak", 0) >= 5,
        ),
        (
            "🎯",
            "goal",
            "goal_help",
            progress.get("weekly_minutes", 0)
            >= max(progress.get("weekly_goal", 60), 1),
        ),
        (
            "🚀",
            "climber",
            "climber_help",
            max(skills.values(), default=0) >= 20,
        ),
    ]


def _render_badge(
    icon,
    title_key,
    help_key,
    unlocked,
):
    state_class = "unlocked" if unlocked else "locked"
    state_text = (
        _text("unlocked")
        if unlocked
        else _text("locked")
    )
    display_icon = icon if unlocked else "🔒"

    st.markdown(
        (
            f'<div class="wf-pg-badge {state_class}">'
            '<div class="wf-pg-badge-icon">'
            f'{display_icon}'
            '</div>'
            '<div class="wf-pg-badge-title">'
            f'{_safe(_text(title_key))}'
            '</div>'
            '<div class="wf-pg-badge-help">'
            f'{_safe(_text(help_key))}'
            '</div>'
            '<span class="wf-pg-badge-state">'
            f'{_safe(state_text)}'
            '</span>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def _render_achievements(progress):
    badges = _badge_specs(progress)

    unlocked_total = sum(
        1
        for *_, unlocked in badges
        if unlocked
    )

    _section_heading(
        "🏅",
        _text("achievements"),
        _text("achievements_help"),
        _text(
            "unlocked_count",
            current=unlocked_total,
            total=len(badges),
        ),
    )

    columns = st.columns(3)

    for index, badge in enumerate(badges):
        with columns[index % 3]:
            _render_badge(*badge)


def _render_choose_level():
    st.markdown(
        (
            '<div class="wf-pg-empty">'
            '<strong>'
            f'🧭 {_safe(_text("choose_level"))}'
            '</strong>'
            f'<span>{_safe(_text("choose_level_help"))}</span>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    if st.button(
        _text("return_home"),
        type="primary",
    ):
        st.session_state.current_view = "Home"
        st.rerun()


def render_progress():
    _apply_styles()
    _render_back_button()

    language = st.session_state.active_language
    progress = st.session_state.language_progress[
        language
    ]

    unlock_achievements(language, progress)
    _render_hero(language, progress)
    _render_stats(progress)

    if progress.get("starting_level") is None:
        _render_choose_level()
        return

    _render_weekly_goal(language, progress)
    _render_skills(progress)
    _render_achievements(progress)