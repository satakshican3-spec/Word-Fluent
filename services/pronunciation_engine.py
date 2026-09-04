import unicodedata
from difflib import SequenceMatcher
from io import BytesIO

import speech_recognition as sr
from gtts import gTTS
from gtts.tts import gTTSError


RECOGNITION_LOCALES = {
    "English": "en-US",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "Hindi": "hi-IN",
    "Bengali": "bn-IN",
    "Korean": "ko-KR",
    "Japanese": "ja-JP",
}

TTS_LANGUAGE_CODES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "Hindi": "hi",
    "Bengali": "bn",
    "Korean": "ko",
    "Japanese": "ja",
}

SCORE_THRESHOLDS = {
    "Beginner": 55,
    "Elementary": 63,
    "Intermediate": 70,
    "Upper Intermediate": 78,
    "Advanced": 85,
}