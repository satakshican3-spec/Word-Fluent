import streamlit as st


def apply_global_styles(dark_mode=False):
    if dark_mode:
        background = "#10131A"
        surface = "#1B202B"
        text = "#F8FAFC"
        muted = "#CBD5E1"
        border = "#303746"
        shadow = "0 14px 35px rgba(0, 0, 0, 0.28)"
    else:
        background = "#F6F7FB"
        surface = "#FFFFFF"
        text = "#172033"
        muted = "#667085"
        border = "#E4E7EC"
        shadow = "0 14px 35px rgba(40, 45, 70, 0.10)"

    st.markdown(
        f"""
        <style>
        :root {{
            --wf-background: {background};
            --wf-surface: {surface};
            --wf-text: {text};
            --wf-muted: {muted};
            --wf-border: {border};
            --wf-shadow: {shadow};
            --wf-purple: #6C63FF;
            --wf-teal: #22B8CF;
        }}

        [data-testid="stAppViewContainer"] {{
            background: var(--wf-background);
            color: var(--wf-text);
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .block-container {{
            max-width: 1200px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }}

        h1, h2, h3, p, label {{
            color: var(--wf-text);
        }}

        .wf-hero {{
            padding: 2.2rem;
            border-radius: 24px;
            background: linear-gradient(
                135deg,
                #6C63FF 0%,
                #4F8FF7 52%,
                #22B8CF 100%
            );
            box-shadow: var(--wf-shadow);
            margin-bottom: 1.5rem;
        }}

        .wf-hero h1 {{
            color: white;
            font-size: 2.6rem;
            margin: 0;
        }}

        .wf-hero p {{
            color: rgba(255, 255, 255, 0.92);
            font-size: 1.1rem;
            margin: 0.5rem 0 0;
        }}

        .wf-logo {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 58px;
            height: 58px;
            margin-bottom: 1rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.18);
            font-size: 1.8rem;
        }}

        .wf-section-title {{
            margin-top: 1.5rem;
            margin-bottom: 0.7rem;
            font-size: 1.45rem;
            font-weight: 800;
            color: var(--wf-text);
        }}

        .wf-card {{
            min-height: 155px;
            padding: 1.2rem;
            border: 1px solid var(--wf-border);
            border-radius: 18px;
            background: var(--wf-surface);
            box-shadow: var(--wf-shadow);
        }}

        .wf-card-icon {{
            font-size: 1.8rem;
            margin-bottom: 0.65rem;
        }}

        .wf-card-title {{
            color: var(--wf-text);
            font-size: 1.05rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }}

        .wf-card-copy {{
            color: var(--wf-muted);
            font-size: 0.9rem;
            line-height: 1.45;
        }}

        .wf-stat {{
            padding: 1rem;
            border: 1px solid var(--wf-border);
            border-radius: 16px;
            background: var(--wf-surface);
        }}

        .wf-stat-label {{
            color: var(--wf-muted);
            font-size: 0.82rem;
            font-weight: 700;
        }}

        .wf-stat-value {{
            color: var(--wf-text);
            font-size: 1.35rem;
            font-weight: 900;
            margin-top: 0.2rem;
        }}

        .wf-language-badge {{
            display: inline-block;
            padding: 0.3rem 0.65rem;
            border-radius: 999px;
            background: rgba(108, 99, 255, 0.13);
            color: var(--wf-purple);
            font-weight: 800;
            font-size: 0.82rem;
        }}

        div.stButton > button {{
            width: 100%;
            min-height: 3rem;
            border: 1px solid var(--wf-border);
            border-radius: 13px;
            background: var(--wf-surface);
            color: var(--wf-text);
            font-weight: 750;
            transition: 0.18s ease;
        }}

        div.stButton > button:hover {{
            border-color: var(--wf-purple);
            color: var(--wf-purple);
            transform: translateY(-1px);
        }}

        button[kind="primary"] {{
            border: none !important;
            background: linear-gradient(
                135deg,
                var(--wf-purple),
                var(--wf-teal)
            ) !important;
            color: white !important;
        }}

        @media (max-width: 700px) {{
            .wf-hero {{
                padding: 1.5rem;
            }}

            .wf-hero h1 {{
                font-size: 2rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )