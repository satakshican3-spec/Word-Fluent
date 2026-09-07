"""Course catalogue for every WordFluent learning language."""

from language_packs.bengali import get_bengali_course
from language_packs.english import get_english_course
from language_packs.starter_courses import get_starter_course


def get_course(language):
    """Return the learning path for a supported language."""
    if language == "English":
        return get_english_course()

    if language == "Bengali":
        return get_bengali_course()

    return get_starter_course(language)