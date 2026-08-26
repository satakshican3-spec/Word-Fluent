import unicodedata
from difflib import SequenceMatcher

import speech_recognition as sr


RECOGNITION_LOCALES = {
    "English": "en-US",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "Hindi": "hi-IN",
    "Bengali": "bn-IN",
    "Korean": "ko-KR",
    "Japanese": "ja-JP",
}


def normalize_text(text):
    normalized = unicodedata.normalize(
        "NFKC",
        text,
    ).casefold()

    cleaned_characters = []

    for character in normalized:
        category = unicodedata.category(character)

        if (
            character.isalnum()
            or character.isspace()
            or category.startswith("M")
        ):
            cleaned_characters.append(character)
        else:
            cleaned_characters.append(" ")

    return " ".join(
        "".join(cleaned_characters).split()
    )


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
                "Try speaking a little more slowly."
            ),
        }

    except sr.RequestError:
        return {
            "success": False,
            "transcript": "",
            "error": (
                "The speech service is temporarily unavailable. "
                "Please try again."
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


def phrase_match_score(spoken_text, expected_text):
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
        max(normal_score, compact_score) * 100
    )


def evaluate_pronunciation(
    transcript,
    accepted_phrases,
    level,
):
    thresholds = {
        "Beginner": 55,
        "Elementary": 63,
        "Intermediate": 70,
        "Upper Intermediate": 78,
        "Advanced": 85,
    }

    scored_phrases = [
        (
            phrase_match_score(
                transcript,
                phrase,
            ),
            phrase,
        )
        for phrase in accepted_phrases
    ]

    score, closest_phrase = max(
        scored_phrases,
        default=(0, ""),
    )

    required_score = thresholds.get(level, 55)

    return {
        "score": score,
        "required_score": required_score,
        "passed": score >= required_score,
        "closest_phrase": closest_phrase,
    }