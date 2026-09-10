import random
from uuid import uuid4

import streamlit as st

from locales import t
from services.game_engine import calculate_reward, get_exercises
from services.pronunciation_engine import (
    generate_reference_audio,
    phrase_match_score,
    transcribe_audio,
)


BASE_SCENES = (
    (
        "☕",
        "At a café, the server asks what you want to drink.",
        "What would you like to drink?",
        "I would like a glass of water.",
    ),
    (
        "👋",
        "You meet someone new and they ask your name.",
        "Hello. What is your name?",
        "My name is Aisha.",
    ),
    (
        "📚",
        "A classmate carries your books for you.",
        "I carried your books for you.",
        "Thank you for your help.",
    ),
    (
        "🍽️",
        "You finish eating and want to pay.",
        "Have you finished your meal?",
        "May I have the bill, please?",
    ),
    (
        "🆘",
        "Someone asks what you need.",
        "Tell me what you need.",
        "Can you help me, please?",
    ),
    (
        "🗺️",
        "A visitor asks which way to turn.",
        "Which way should I turn at the corner?",
        "Turn left at the corner.",
    ),
)

PARTNER_PROMPTS = {
    "English": (
        "What would you like to drink?",
        "Hello. What is your name?",
        "I carried your books for you.",
        "Have you finished your meal?",
        "Tell me what you need.",
        "Which way should I turn at the corner?",
    ),
    "French": (
        "Que souhaitez-vous boire ?",
        "Bonjour. Comment vous appelez-vous ?",
        "J'ai porté vos livres pour vous.",
        "Avez-vous terminé votre repas ?",
        "Dites-moi ce dont vous avez besoin.",
        "De quel côté dois-je tourner au coin de la rue ?",
    ),
    "Spanish": (
        "¿Qué desea beber?",
        "Hola. ¿Cómo se llama?",
        "Le llevé los libros.",
        "¿Ha terminado de comer?",
        "Dígame qué necesita.",
        "¿Hacia dónde debo girar en la esquina?",
    ),
    "Hindi": (
        "आप क्या पीना चाहेंगे?",
        "नमस्ते। आपका नाम क्या है?",
        "मैंने आपकी किताबें उठा दी हैं।",
        "क्या आपने खाना खा लिया?",
        "बताइए, आपको क्या चाहिए।",
        "मुझे कोने पर किस तरफ मुड़ना चाहिए?",
    ),
    "Bengali": (
        "আপনি কী পান করতে চান?",
        "নমস্কার। আপনার নাম কী?",
        "এই নিন আপনার বই।",
        "আপনার খাওয়া শেষ?",
        "বলুন, আপনার কী দরকার?",
        "মোড়ে কোন দিকে ঘুরব?",
    ),
    "Korean": (
        "무엇을 마시고 싶으세요?",
        "안녕하세요. 이름이 뭐예요?",
        "책을 들어 드렸어요.",
        "식사를 다 하셨어요?",
        "무엇이 필요한지 말씀해 주세요.",
        "모퉁이에서 어느 쪽으로 돌아야 해요?",
    ),
    "Japanese": (
        "何を飲みたいですか。",
        "こんにちは。お名前は何ですか。",
        "本を運びました。",
        "食事は終わりましたか。",
        "何が必要か教えてください。",
        "角でどちらに曲がればいいですか。",
    ),
}

SOUND_GUIDES = {
    "English": (
        "eye wood LYKE uh glass uv WAW-ter",
        "my NAYM iz EYE-sha",
        "THANK yoo for yor help",
        "may eye hav thuh bil pleez",
        "kan yoo help mee pleez",
        "turn left at thuh KOR-ner",
    ),
    "French": (
        "zhuh voo-DRAY uhn vair DOH",
        "zhuh mah-PELL EYE-sha",
        "mehr-SEE poor voh-tr ED",
        "pweezh ah-VWAHR lah-dee-SYON seel voo PLEH",
        "poo-vay voo meh-DAY seel voo PLEH",
        "toor-NAY ah gosh oh kwan duh lah roo",
    ),
    "Spanish": (
        "kee-SYEH-rah oon BAH-soh deh AH-gwah",
        "meh YAH-moh EYE-sha",
        "GRAH-syahs por soo ah-YOO-dah",
        "meh TRAH-eh lah KWEHN-tah por fah-BOR",
        "PWEH-deh ah-yoo-DAR-meh por fah-BOR",
        "HEE-reh ah lah ees-KYEHR-dah en lah es-KEE-nah",
    ),
    "Hindi": (
        "mu-jhe ek gi-laas paa-ni chaa-hi-ye",
        "me-raa naam aa-yi-shaa hai",
        "aap-ki ma-dad ke li-ye dhan-ya-vaad",
        "kri-pa-yaa mu-jhe bil dii-ji-ye",
        "kyaa aap me-ri ma-dad kar sak-te hain",
        "ko-ne par baa-yen mu-ri-ye",
    ),
    "Bengali": (
        "aa-mi ek glaas jol chaai",
        "aa-maar naam maa-yaa",
        "aap-naar shaa-haaj-jer jon-no dhon-no-baad",
        "bil-taa din do-yaa ko-re",
        "do-yaa ko-re aa-maa-ke shaa-haaj-jo ko-run",
        "mo-re baam di-ke ghu-run",
    ),
    "Korean": (
        "mul han jan ju-se-yo",
        "je i-reu-meun a-i-sya-ye-yo",
        "do-wa-ju-syeo-seo gam-sa-ham-ni-da",
        "gye-san-seo ju-se-yo",
        "jeo-reul do-wa-ju-sil su i-sseo-yo",
        "mo-tung-i-e-seo wen-jjo-geu-ro do-se-yo",
    ),
    "Japanese": (
        "o-mi-zu o ip-pai ku-da-sai",
        "wa-ta-shi no na-ma-e wa ai-sha des",
        "te-tsu-dat-te ku-da-sat-te a-ri-ga-to-o go-za-i-mas",
        "o-kai-kei o o-ne-gai-shi-mas",
        "te-tsu-dat-te mo-ra-e-mas ka",
        "ka-do o hi-da-ri ni ma-gat-te ku-da-sai",
    ),
}

EXTRA_REPLIES = {
    "English": (
        ("A glass of water please",),
        ("I am Aisha", "I'm Aisha"),
        ("Thank you", "Thanks for your help"),
        ("Can I have the bill please", "The bill please"),
        ("Please help me", "Could you help me please"),
        ("Turn left", "Please turn left at the corner"),
    ),
    "French": (
        ("Je voudrais de l'eau", "Un verre d'eau s'il vous plaît"),
        ("Je suis Aisha",),
        ("Merci", "Merci beaucoup"),
        ("L'addition s'il vous plaît",),
        ("Aidez-moi s'il vous plaît", "Pouvez-vous m'aider"),
        ("Tournez à gauche",),
    ),
    "Spanish": (
        ("Quiero un vaso de agua", "Un vaso de agua por favor"),
        ("Soy Aisha", "Mi nombre es Aisha"),
        ("Gracias", "Muchas gracias"),
        ("La cuenta por favor",),
        ("Ayúdeme por favor", "Puede ayudarme"),
        ("Gire a la izquierda",),
    ),
    "Hindi": (
        ("मुझे पानी चाहिए", "एक गिलास पानी चाहिए"),
        ("मैं आयशा हूँ",),
        ("धन्यवाद", "बहुत धन्यवाद"),
        ("मुझे बिल दीजिए", "बिल दीजिए"),
        ("कृपया मेरी मदद कीजिए", "मेरी मदद कीजिए"),
        ("बाएँ मुड़िए", "कोने पर बाईं ओर मुड़िए"),
    ),
    "Bengali": (
        ("আমি এক গ্লাস পানি চাই", "আমি জল চাই", "আমি পানি চাই"),
        ("আমি মায়া",),
        ("ধন্যবাদ", "অনেক ধন্যবাদ"),
        ("দয়া করে বিলটা দিন", "বিল দিন"),
        ("আমাকে সাহায্য করুন", "একটু সাহায্য করুন"),
        ("বাঁ দিকে ঘুরুন", "বাম দিকে ঘুরুন"),
    ),
    "Korean": (
        ("물 주세요", "물 한 잔 부탁합니다"),
        ("저는 아이샤예요", "아이샤예요"),
        ("감사합니다", "정말 감사합니다"),
        ("계산해 주세요", "계산 부탁합니다"),
        ("도와주세요", "저를 도와주세요"),
        ("왼쪽으로 도세요", "왼쪽으로 가세요"),
    ),
    "Japanese": (
        ("水を一杯ください", "お水をください", "水をください"),
        ("私はアイシャです", "アイシャです"),
        ("ありがとうございます", "どうもありがとうございます"),
        ("お会計お願いします", "お会計をください"),
        ("手伝ってください", "助けてもらえますか"),
        ("左に曲がってください", "角を左に曲がって"),
    ),
}

RESPONSE_INDICES = (0, 2, 5, 10, 14, 12)

BENGALI_OVERRIDES = {
    1: ("আমার নাম মায়া", "My name is Maya."),
    2: ("আপনার সাহায্যের জন্য ধন্যবাদ", "Thank you for your help."),
    3: ("বিলটা দিন, দয়া করে", "May I have the bill, please?"),
    4: ("দয়া করে আমাকে সাহায্য করুন", "Can you help me, please?"),
    5: ("মোড়ে বাঁ দিকে ঘুরুন", "Turn left at the corner."),
}

MATCH_THRESHOLDS = {
    "Relaxed": 45,
    "Balanced": 55,
    "Challenging": 65,
    "Custom": 70,
}


def get_speaking_scenarios(language):
    exercises = get_exercises(language)
    scenarios = []

    for index, base in enumerate(BASE_SCENES):
        icon, situation, prompt_meaning, response_meaning = base
        exercise = exercises[RESPONSE_INDICES[index]]
        response = exercise["answer"]
        accepted = list(exercise.get("accepted_answers", []))

        if language == "Bengali" and index in BENGALI_OVERRIDES:
            response, response_meaning = BENGALI_OVERRIDES[index]

        scenarios.append(
            {
                "icon": icon,
                "situation": situation,
                "prompt": PARTNER_PROMPTS[language][index],
                "prompt_meaning": prompt_meaning,
                "response": response,
                "response_meaning": response_meaning,
                "guide": SOUND_GUIDES[language][index],
                "accepted": [
                    *accepted,
                    *EXTRA_REPLIES[language][index],
                ],
            }
        )

    return scenarios


@st.cache_data(show_spinner=False, ttl=86400)
def get_speaking_audio(text, language, slow):
    return generate_reference_audio(text, language, slow)


def _round_count(scenarios):
    requested = int(st.session_state.get("session_length", 5))
    return min(len(scenarios), max(5, requested // 2))


def start_speaking_session(language):
    scenarios = get_speaking_scenarios(language)

    st.session_state.speaking_game = {
        "id": uuid4().hex[:10],
        "language": language,
        "scenario_indices": random.sample(
            range(len(scenarios)),
            _round_count(scenarios),
        ),
        "round_index": 0,
        "attempt_number": 0,
        "result": None,
        "hint_used": False,
        "correct": 0,
        "coins": 0,
        "complete": False,
        "prompt_audio": b"",
        "prompt_error": None,
        "prompt_speed": None,
        "reply_audio": b"",
        "reply_error": None,
        "reply_speed": None,
    }


def _play_audio(game, text, language, slow, kind):
    with st.spinner(t("preparing_audio")):
        result = get_speaking_audio(text, language, slow)

    game[f"{kind}_audio"] = result["audio"]
    game[f"{kind}_error"] = result["error"]
    game[f"{kind}_speed"] = (
        t("listen_slow") if slow else t("listen_normal")
    )


def _render_audio_controls(game, text, language, kind):
    normal_column, slow_column = st.columns(2)

    with normal_column:
        if st.button(
            f'🔊 {t("listen_normal")}',
            key=(
                f'{kind}_normal_{game["id"]}_'
                f'{game["round_index"]}'
            ),
            use_container_width=True,
        ):
            _play_audio(game, text, language, False, kind)

    with slow_column:
        if st.button(
            f'🐢 {t("listen_slow")}',
            key=(
                f'{kind}_slow_{game["id"]}_'
                f'{game["round_index"]}'
            ),
            use_container_width=True,
        ):
            _play_audio(game, text, language, True, kind)

    if game[f"{kind}_audio"]:
        st.caption(game[f"{kind}_speed"])
        st.audio(
            game[f"{kind}_audio"],
            format="audio/mp3",
        )
    elif game[f"{kind}_error"]:
        st.warning(game[f"{kind}_error"])


def _evaluate_reply(transcript, scenario):
    replies = [
        scenario["response"],
        *scenario["accepted"],
    ]

    score, closest = max(
        (
            (
                phrase_match_score(transcript, reply),
                reply,
            )
            for reply in replies
        ),
        default=(0, scenario["response"]),
    )

    required = MATCH_THRESHOLDS.get(
        st.session_state.get(
            "difficulty",
            "Balanced",
        ),
        55,
    )

    return {
        "score": score,
        "required": required,
        "closest": closest,
        "passed": score >= required,
    }


def _grant_reward(game, progress, score):
    reward = calculate_reward(
        st.session_state.get(
            "difficulty",
            "Balanced",
        ),
        game["hint_used"],
    )

    if score >= 90:
        reward += 3

    game["correct"] += 1
    game["coins"] += reward
    st.session_state.coins += reward
    progress["overall_xp"] += reward
    progress["weekly_minutes"] += 1

    skills = progress.setdefault(
        "skill_levels",
        {},
    )
    skills["Speaking"] = (
        skills.get("Speaking", 0) + 1
    )

    return reward


def _check_reply(
    game,
    scenario,
    audio_file,
    language,
    progress,
):
    with st.spinner(t("speaking_listening_to_you")):
        transcription = transcribe_audio(
            audio_file,
            language,
        )

    if not transcription["success"]:
        game["result"] = {
            "success": False,
            "error": transcription["error"],
        }
        return

    evaluation = _evaluate_reply(
        transcription["transcript"],
        scenario,
    )
    reward = 0

    if evaluation["passed"]:
        reward = _grant_reward(
            game,
            progress,
            evaluation["score"],
        )
    else:
        st.session_state.hearts = max(
            st.session_state.hearts - 1,
            0,
        )

    game["result"] = {
        "success": True,
        "transcript": transcription["transcript"],
        "reward": reward,
        **evaluation,
    }


def _clear_round_audio(game):
    for name in ("prompt", "reply"):
        game[f"{name}_audio"] = b""
        game[f"{name}_error"] = None
        game[f"{name}_speed"] = None


def _retry_round(game):
    game["attempt_number"] += 1
    game["result"] = None
    game["reply_audio"] = b""
    game["reply_error"] = None
    game["reply_speed"] = None
    st.rerun()


def _next_round(game):
    if (
        game["round_index"] + 1
        >= len(game["scenario_indices"])
    ):
        game["complete"] = True
    else:
        game["round_index"] += 1
        game["attempt_number"] = 0
        game["result"] = None
        game["hint_used"] = False
        _clear_round_audio(game)

    st.rerun()


def _render_no_hearts():
    if st.session_state.hearts > 0:
        return False

    st.error(t("no_hearts_remaining"))
    enough_coins = st.session_state.coins >= 20

    if st.button(
        t("restore_heart"),
        disabled=not enough_coins,
    ):
        st.session_state.coins -= 20
        st.session_state.hearts = 1
        st.rerun()

    if not enough_coins:
        st.caption(
            t("restore_heart_requirement")
        )

    return True


def _render_hint(game, scenario):
    if st.toggle(
        t("speaking_show_help"),
        key=(
            f'speaking_hint_{game["id"]}_'
            f'{game["round_index"]}'
        ),
    ):
        game["hint_used"] = True

        st.info(
            f'**{t("speaking_reply_meaning")}:** '
            f'{scenario["response_meaning"]}'
        )

        first_words = " ".join(
            scenario["response"].split()[:2]
        )
        st.caption(
            f'{t("speaking_first_words")}: '
            f'{first_words}…'
        )


def _render_result(game, scenario, language):
    result = game["result"]

    if result is None:
        return

    st.markdown(
        f'### {t("speaking_feedback")}'
    )

    if not result["success"]:
        st.error(result["error"])

        if st.button(
            t("speaking_record_again"),
            type="primary",
        ):
            _retry_round(game)

        return

    st.write(
        f'**{t("speaking_heard")}:** '
        f'{result["transcript"]}'
    )

    st.progress(
        max(
            0.0,
            min(result["score"] / 100, 1.0),
        )
    )

    st.caption(
        t(
            "speaking_match",
            score=result["score"],
            required=result["required"],
        )
    )

    if result["passed"]:
        st.success(
            t(
                "speaking_correct",
                reward=result["reward"],
            )
        )
    else:
        st.error(
            t("speaking_try_another_reply")
        )

    st.markdown(
        f'**{t("speaking_model_reply")}:** '
        f'{scenario["response"]}'
    )
    st.caption(
        f'🔤 {t("speaking_say_it_like")}: '
        f'{scenario["guide"]}'
    )
    st.caption(
        f'{t("meaning")}: '
        f'{scenario["response_meaning"]}'
    )

    _render_audio_controls(
        game,
        scenario["response"],
        language,
        "reply",
    )

    if result["passed"]:
        if st.button(
            t("speaking_next_scene"),
            type="primary",
            use_container_width=True,
        ):
            _next_round(game)
    else:
        retry_column, next_column = st.columns(2)

        with retry_column:
            if st.button(
                t("speaking_record_again"),
                type="primary",
                use_container_width=True,
            ):
                _retry_round(game)

        with next_column:
            if st.button(
                t("speaking_skip_scene"),
                use_container_width=True,
            ):
                _next_round(game)


def _render_complete(game, language):
    st.title(
        f'🗣️ {t("session_complete")}'
    )
    score_column, coin_column = st.columns(2)

    with score_column:
        st.metric(
            t("speaking_score"),
            t(
                "speaking_replies_correct",
                correct=game["correct"],
                total=len(
                    game["scenario_indices"]
                ),
            ),
        )

    with coin_column:
        st.metric(
            t("coins"),
            f'🪙 {game["coins"]}',
        )

    replay_column, home_column = st.columns(2)

    with replay_column:
        if st.button(
            t("play_again"),
            type="primary",
            use_container_width=True,
        ):
            start_speaking_session(language)
            st.rerun()

    with home_column:
        if st.button(
            t("finish_session"),
            use_container_width=True,
        ):
            st.session_state.current_view = "Home"
            st.rerun()


def render_speaking():
    language = st.session_state.active_language

    if (
        "speaking_game"
        not in st.session_state
        or st.session_state.speaking_game[
            "language"
        ]
        != language
    ):
        start_speaking_session(language)

    game = st.session_state.speaking_game

    if game["complete"]:
        _render_complete(game, language)
        return

    scenarios = get_speaking_scenarios(
        language
    )
    scenario = scenarios[
        game["scenario_indices"][
            game["round_index"]
        ]
    ]

    progress = (
        st.session_state.language_progress[
            language
        ]
    )
    level = (
        progress.get("current_level")
        or "Beginner"
    )

    back_column, title_column = st.columns(
        [1, 5]
    )

    with back_column:
        if st.button(
            f'← {t("home")}'
        ):
            st.session_state.current_view = "Home"
            st.rerun()

    with title_column:
        st.title(
            f'🗣️ {t("speaking_title")}'
        )

    st.write(
        t("speaking_instructions")
    )

    language_column, level_column, heart_column = (
        st.columns(3)
    )

    with language_column:
        st.metric(
            t("language"),
            language,
        )

    with level_column:
        st.metric(
            t("level"),
            level,
        )

    with heart_column:
        st.metric(
            t("hearts"),
            f'❤️ {st.session_state.hearts}/5',
        )

    current_round = game["round_index"] + 1
    total_rounds = len(
        game["scenario_indices"]
    )

    st.caption(
        t(
            "speaking_round",
            current=current_round,
            total=total_rounds,
        )
    )
    st.progress(
        (current_round - 1)
        / total_rounds
    )

    st.markdown(
        f'### {scenario["icon"]} '
        f'{t("speaking_situation")}'
    )
    st.info(
        scenario["situation"]
    )

    st.markdown(
        f'### 💬 '
        f'{t("speaking_partner_says")}'
    )
    st.markdown(
        f'## {scenario["prompt"]}'
    )
    st.caption(
        f'{t("meaning")}: '
        f'{scenario["prompt_meaning"]}'
    )

    _render_audio_controls(
        game,
        scenario["prompt"],
        language,
        "prompt",
    )

    st.markdown(
        f'### 🎤 '
        f'{t("speaking_your_turn", target_language=language)}'
    )

    _render_hint(
        game,
        scenario,
    )

    st.caption(
        t("speaking_record_tip")
    )

    audio_file = st.audio_input(
        t("speaking_record_label"),
        sample_rate=16000,
        key=(
            f'speaking_audio_{game["id"]}_'
            f'{game["round_index"]}_'
            f'{game["attempt_number"]}'
        ),
    )

    st.caption(
        t("speaking_privacy")
    )

    no_hearts = _render_no_hearts()

    if st.button(
        t("speaking_check_reply"),
        type="primary",
        disabled=(
            audio_file is None
            or game["result"] is not None
            or no_hearts
        ),
        use_container_width=True,
    ):
        _check_reply(
            game,
            scenario,
            audio_file,
            language,
            progress,
        )
        st.rerun()

    _render_result(
        game,
        scenario,
        language,
    )