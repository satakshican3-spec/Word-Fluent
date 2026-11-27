# WordFluent

**Play. Practise. Pronounce.**

WordFluent is a multilingual learning app built with Streamlit. It combines lessons, sentence building, listening, speaking, pronunciation feedback, progress tracking, and optional Supabase accounts.

## Learning languages

- English
- French
- Spanish
- Hindi
- Bengali
- Korean
- Japanese

The interface can also be displayed in any of these seven languages.

## Main features

- Structured vocabulary and grammar lessons
- Sentence Builder with word tiles and typed answers
- Listening Practice v2 with meaning, dictation, missing-word, dialogue, and mixed modes
- Speaking scenarios with recorded replies
- Pronunciation Coach with speech recognition and word-level feedback
- Coins, hearts, levels, streaks, achievements, and weekly goals
- Guest mode and optional Supabase account syncing
- Responsive light/dark WordFluent design

## Run locally or in Codespaces

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Using `python -m streamlit` is recommended because it works even when the standalone `streamlit` command is not on the terminal path.

## Optional account setup

Guest learning works without any secrets. To enable account registration and progress syncing, create `.streamlit/secrets.toml` with:

```toml
SUPABASE_URL = "your-project-url"
SUPABASE_PUBLISHABLE_KEY = "your-publishable-key"
```

Never commit the real secrets file. It is already excluded by `.gitignore`.
