import unicodedata
from difflib import SequenceMatcher

import speech_recognition as sr
import edge_tts


RECOGNITION_LOCALES = {
    "English": "en-US",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "Hindi": "hi-IN",
    "Bengali": "bn-IN",
    "Korean": "ko-KR",
    "Japanese": "ja-JP",
}

TTS_VOICES = {
    "English": "en-US-AndrewNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural",
    "Hindi": "hi-IN-MadhurNeural",
    "Bengali": "bn-IN-BashkarNeural",
    "Korean": "ko-KR-InJoonNeural",
    "Japanese": "ja-JP-KeitaNeural",
}

NORMAL_SPEECH_RATE = "+0%"
SLOW_SPEECH_RATE = "-18%"

SCORE_THRESHOLDS = {
    "Beginner": 55,
    "Elementary": 63,
    "Intermediate": 70,
    "Upper Intermediate": 78,
    "Advanced": 85,
}

COVERAGE_THRESHOLDS = {
    "Beginner": 70,
    "Elementary": 75,
    "Intermediate": 80,
    "Upper Intermediate": 85,
    "Advanced": 90,
}


def normalize_text(text):
    normalized = unicodedata.normalize(
        "NFKC",
        str(text or ""),
    ).casefold()

    cleaned = []

    for character in normalized:
        category = unicodedata.category(character)

        if (
            character.isalnum()
            or character.isspace()
            or category.startswith("M")
        ):
            cleaned.append(character)
        else:
            cleaned.append(" ")

    return " ".join(
        "".join(cleaned).split()
    )


def generate_reference_audio(
    text,
    language,
    slow=False,
):
    phrase = str(text or "").strip()

    if not phrase:
        return {
            "success": False,
            "audio": b"",
            "error": "There is no phrase to read aloud.",
        }

    try:
        speech = edge_tts.Communicate(
            phrase,
            TTS_VOICES.get(
                language,
                TTS_VOICES["English"],
            ),
            rate=(
                SLOW_SPEECH_RATE
                if slow
                else NORMAL_SPEECH_RATE
            ),
        )
        audio = bytearray()

        for chunk in speech.stream_sync():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])

        if not audio:
            raise RuntimeError(
                "The speech service returned no audio."
            )

        return {
            "success": True,
            "audio": bytes(audio),
            "error": None,
        }

    except Exception:
        return {
            "success": False,
            "audio": b"",
            "error": (
                "Reference audio is unavailable right now. "
                "You can still record and check your phrase."
            ),
        }


def transcribe_audio(audio_file, language):
    recognizer = sr.Recognizer()

    locale = RECOGNITION_LOCALES.get(
        language,
        "en-US",
    )

    try:
        audio_file.seek(0)

        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        transcript = recognizer.recognize_google(
            audio_data,
            language=locale,
        )

        return {
            "success": True,
            "transcript": str(transcript).strip(),
            "error": None,
        }

    except sr.UnknownValueError:
        return {
            "success": False,
            "transcript": "",
            "error": (
                "I could not understand that recording. "
                "Move closer to the microphone and try again."
            ),
        }

    except sr.RequestError:
        return {
            "success": False,
            "transcript": "",
            "error": (
                "The speech service is temporarily unavailable. "
                "Please try again in a moment."
            ),
        }

    except (ValueError, OSError, EOFError):
        return {
            "success": False,
            "transcript": "",
            "error": (
                "The recording could not be read. "
                "Please make a new recording."
            ),
        }


def phrase_match_score(
    spoken_text,
    expected_text,
):
    spoken = normalize_text(spoken_text)
    expected = normalize_text(expected_text)

    if not spoken or not expected:
        return 0

    normal_score = SequenceMatcher(
        None,
        spoken,
        expected,
    ).ratio()

    compact_score = SequenceMatcher(
        None,
        spoken.replace(" ", ""),
        expected.replace(" ", ""),
    ).ratio()

    return round(
        max(
            normal_score,
            compact_score,
        ) * 100
    )


def _feedback_units(text, language):
    normalized = normalize_text(text)

    if language == "Japanese":
        return [
            character
            for character in normalized
            if not character.isspace()
        ]

    return normalized.split()


def build_word_feedback(
    transcript,
    expected_phrase,
    language=None,
):
    expected_units = _feedback_units(
        expected_phrase,
        language,
    )

    spoken_units = _feedback_units(
        transcript,
        language,
    )

    matcher = SequenceMatcher(
        None,
        expected_units,
        spoken_units,
        autojunk=False,
    )

    items = []
    extra_units = []
    matched_count = 0

    for (
        tag,
        first_start,
        first_end,
        second_start,
        second_end,
    ) in matcher.get_opcodes():
        expected_chunk = expected_units[
            first_start:first_end
        ]

        spoken_chunk = spoken_units[
            second_start:second_end
        ]

        if tag == "equal":
            matched_count += len(expected_chunk)

            items.extend(
                {
                    "expected": unit,
                    "heard": unit,
                    "status": "matched",
                }
                for unit in expected_chunk
            )

        elif tag == "delete":
            items.extend(
                {
                    "expected": unit,
                    "heard": "",
                    "status": "missing",
                }
                for unit in expected_chunk
            )

        elif tag == "insert":
            extra_units.extend(spoken_chunk)

        else:
            paired_length = min(
                len(expected_chunk),
                len(spoken_chunk),
            )

            for index, unit in enumerate(
                expected_chunk
            ):
                heard = (
                    spoken_chunk[index]
                    if index < paired_length
                    else ""
                )

                items.append(
                    {
                        "expected": unit,
                        "heard": heard,
                        "status": (
                            "different"
                            if heard
                            else "missing"
                        ),
                    }
                )

            extra_units.extend(
                spoken_chunk[paired_length:]
            )

    total_expected = len(expected_units)

    coverage = round(
        matched_count
        / max(total_expected, 1)
        * 100
    )

    return {
        "items": items,
        "extra_units": extra_units,
        "matched_count": matched_count,
        "total_expected": total_expected,
        "coverage": coverage,
        "unit_name": (
            "character"
            if language == "Japanese"
            else "word"
        ),
    }


def _build_coaching_tip(feedback, passed):
    different = [
        item
        for item in feedback["items"]
        if item["status"] == "different"
    ]

    missing = [
        item
        for item in feedback["items"]
        if item["status"] == "missing"
    ]

    if (
        passed
        and feedback["coverage"] == 100
    ):
        return (
            "Excellent—every target part was recognized. "
            "Repeat it once more at a natural pace."
        )

    if different:
        item = different[0]

        return (
            f'Focus on “{item["expected"]}”. '
            f'WordFluent heard “{item["heard"]}”. '
            "Say that part slowly, then repeat "
            "the complete phrase."
        )

    if missing:
        focus = ", ".join(
            item["expected"]
            for item in missing[:3]
        )

        return (
            f"Make these parts clearer: {focus}. "
            "Pause briefly before them, then try "
            "the full phrase."
        )

    if feedback["extra_units"]:
        extras = ", ".join(
            feedback["extra_units"][:3]
        )

        return (
            f"Try again without the extra parts: "
            f"{extras}. Follow the phrase exactly."
        )

    if passed:
        return (
            "Good job. Try it again with a smooth, "
            "natural rhythm."
        )

    return (
        "Listen to the reference, practise in small "
        "parts, then try again."
    )


def evaluate_pronunciation(
    transcript,
    accepted_phrases,
    level,
    language=None,
):
    phrases = [
        str(phrase).strip()
        for phrase in accepted_phrases
        if phrase
    ]

    scored_phrases = [
        (
            phrase_match_score(
                transcript,
                phrase,
            ),
            phrase,
        )
        for phrase in phrases
    ]

    score, closest_phrase = max(
        scored_phrases,
        default=(0, ""),
    )

    feedback = build_word_feedback(
        transcript,
        closest_phrase,
        language,
    )

    required_score = SCORE_THRESHOLDS.get(
        level,
        55,
    )

    required_coverage = COVERAGE_THRESHOLDS.get(
        level,
        70,
    )

    passed = (
        score >= required_score
        and feedback["coverage"]
        >= required_coverage
    )

    return {
        "score": score,
        "required_score": required_score,
        "required_coverage": required_coverage,
        "passed": passed,
        "closest_phrase": closest_phrase,
        "word_feedback": feedback["items"],
        "extra_words": feedback["extra_units"],
        "matched_words": feedback["matched_count"],
        "total_words": feedback["total_expected"],
        "word_coverage": feedback["coverage"],
        "feedback_unit": feedback["unit_name"],
        "coaching_tip": _build_coaching_tip(
            feedback,
            passed,
        ),
    }