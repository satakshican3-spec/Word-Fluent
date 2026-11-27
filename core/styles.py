import streamlit as st


def apply_global_styles(dark_mode=False):
    """Apply WordFluent's shared visual system to every Streamlit page."""
    if dark_mode:
        background = "#0B1020"
        background_soft = "#111A31"
        surface = "#151E35"
        surface_raised = "#1B2742"
        text = "#F7F9FF"
        heading = "#FFFFFF"
        muted = "#AAB6D3"
        border = "rgba(169, 183, 218, 0.18)"
        soft_border = "rgba(169, 183, 218, 0.11)"
        shadow = "0 18px 48px rgba(0, 0, 0, 0.28)"
        soft_shadow = "0 10px 28px rgba(0, 0, 0, 0.20)"
        input = "#111A2E"
    else:
        background = "#F7FAFF"
        background_soft = "#EEF6FF"
        surface = "#FFFFFF"
        surface_raised = "#FFFFFF"
        text = "#263654"
        heading = "#111B3A"
        muted = "#63708B"
        border = "rgba(111, 128, 166, 0.20)"
        soft_border = "rgba(111, 128, 166, 0.12)"
        shadow = "0 18px 48px rgba(64, 84, 134, 0.12)"
        soft_shadow = "0 10px 28px rgba(72, 91, 137, 0.09)"
        input = "#FBFCFF"

    st.markdown(
        f"""
        <style>
        :root {{
            --wf-background: {background};
            --wf-background-soft: {background_soft};
            --wf-surface: {surface};
            --wf-surface-raised: {surface_raised};
            --wf-text: {text};
            --wf-heading: {heading};
            --wf-muted: {muted};
            --wf-border: {border};
            --wf-soft-border: {soft_border};
            --wf-shadow: {shadow};
            --wf-soft-shadow: {soft_shadow};
            --wf-input: {input};
            --wf-purple: #6847F5;
            --wf-purple-dark: #4D2DD0;
            --wf-blue: #3C8CF4;
            --wf-teal: #16C7BF;
            --wf-green: #2DBE78;
            --wf-yellow: #FFBF2F;
            --wf-pink: #EC5EA7;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        [data-testid="stAppViewContainer"] {{
            background:
                radial-gradient(circle at 91% 8%, rgba(22, 199, 191, .12), transparent 24rem),
                radial-gradient(circle at 8% 5%, rgba(104, 71, 245, .10), transparent 25rem),
                linear-gradient(180deg, var(--wf-background) 0%, var(--wf-background-soft) 100%);
            color: var(--wf-text);
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        #MainMenu,
        footer,
        [data-testid="stToolbar"] {{
            visibility: hidden;
        }}

        .block-container {{
            width: min(100%, 1440px);
            max-width: 1440px;
            padding-top: 1rem;
            padding-bottom: 4rem;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--wf-heading);
            letter-spacing: -0.025em;
        }}

        p, label, li {{
            color: var(--wf-text);
        }}

        a {{
            color: var(--wf-purple);
        }}

        /* Welcome screen */
        .wf-welcome-mark {{
            display: grid;
            place-items: center;
            width: 4.5rem;
            height: 4.5rem;
            margin: 2rem auto .45rem;
            border-radius: 1.35rem;
            background: linear-gradient(135deg, var(--wf-purple), var(--wf-teal));
            box-shadow: 0 16px 34px rgba(104, 71, 245, .25);
            font-size: 2.25rem;
        }}

        .wf-welcome-brand {{
            margin-bottom: 1.75rem;
            color: var(--wf-heading);
            font-size: 2rem;
            font-weight: 900;
            text-align: center;
            letter-spacing: -.045em;
        }}

        .wf-welcome-brand span {{
            color: var(--wf-teal);
        }}

        /* Global navigation */
        .wf-brand-lockup {{
            display: flex;
            align-items: center;
            min-height: 3.25rem;
            gap: .7rem;
            white-space: nowrap;
        }}

        .wf-brand-mark {{
            display: grid;
            place-items: center;
            width: 3rem;
            height: 3rem;
            flex: 0 0 3rem;
            border-radius: .95rem;
            background: linear-gradient(135deg, var(--wf-purple) 0%, var(--wf-blue) 50%, var(--wf-teal) 100%);
            box-shadow: 0 10px 24px rgba(104, 71, 245, .24);
            font-size: 1.55rem;
        }}

        .wf-brand-name {{
            color: var(--wf-heading);
            font-size: 1.42rem;
            font-weight: 950;
            line-height: 1;
            letter-spacing: -.045em;
        }}

        .wf-brand-name span {{
            color: var(--wf-teal);
        }}

        .wf-brand-tagline {{
            margin-top: .22rem;
            color: var(--wf-purple);
            font-size: .63rem;
            font-weight: 800;
            letter-spacing: .025em;
        }}

        .wf-nav-divider {{
            height: 1px;
            margin: .72rem 0 1.2rem;
            background: linear-gradient(90deg, transparent, var(--wf-border) 10%, var(--wf-border) 90%, transparent);
        }}

        div[data-testid="stHorizontalBlock"]:has(.wf-brand-lockup) {{
            align-items: center;
        }}

        div[data-testid="stHorizontalBlock"]:has(.wf-brand-lockup) div.stButton > button {{
            min-height: 2.65rem !important;
            padding: .45rem .62rem !important;
            border: 1px solid transparent !important;
            border-radius: 999px !important;
            background: transparent !important;
            box-shadow: none !important;
            color: var(--wf-text) !important;
            font-size: .84rem !important;
            font-weight: 800 !important;
        }}

        div[data-testid="stHorizontalBlock"]:has(.wf-brand-lockup) div.stButton > button[kind="primary"] {{
            border-color: rgba(104, 71, 245, .10) !important;
            background: rgba(104, 71, 245, .12) !important;
            color: var(--wf-purple) !important;
        }}

        div[data-testid="stHorizontalBlock"]:has(.wf-brand-lockup) div.stButton > button:hover {{
            border-color: rgba(104, 71, 245, .22) !important;
            background: rgba(104, 71, 245, .08) !important;
            color: var(--wf-purple) !important;
            transform: translateY(-1px);
        }}

        /* Home hero */
        .wf-hero-copy {{
            padding: clamp(1.1rem, 2vw, 2rem) 0 1rem;
        }}

        .wf-kicker {{
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            padding: .42rem .78rem;
            border: 1px solid rgba(104, 71, 245, .15);
            border-radius: 999px;
            background: rgba(104, 71, 245, .08);
            color: var(--wf-purple);
            font-size: .78rem;
            font-weight: 900;
            letter-spacing: .025em;
        }}

        .wf-hero-title {{
            max-width: 720px;
            margin: 1rem 0 .8rem;
            color: var(--wf-heading);
            font-size: clamp(2.65rem, 5.1vw, 5.35rem);
            font-weight: 950;
            line-height: .96;
            letter-spacing: -.07em;
        }}

        .wf-gradient-text {{
            background: linear-gradient(90deg, var(--wf-purple), var(--wf-blue), var(--wf-teal));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}

        .wf-hero-description {{
            max-width: 650px;
            margin: 0 0 1.1rem;
            color: var(--wf-muted);
            font-size: clamp(1rem, 1.45vw, 1.24rem);
            line-height: 1.65;
        }}

        .wf-feature-strip {{
            display: flex;
            flex-wrap: wrap;
            gap: .65rem 1rem;
            margin-top: 1.15rem;
        }}

        .wf-feature-pill {{
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            color: var(--wf-text);
            font-size: .87rem;
            font-weight: 800;
        }}

        .wf-feature-pill span {{
            display: grid;
            place-items: center;
            width: 2rem;
            height: 2rem;
            border-radius: 50%;
            background: var(--wf-surface);
            box-shadow: var(--wf-soft-shadow);
        }}

        .wf-hero-visual {{
            position: relative;
            min-height: 420px;
            margin-top: .6rem;
            overflow: hidden;
            border: 1px solid rgba(104, 71, 245, .10);
            border-radius: 2.25rem;
            background:
                radial-gradient(circle at 72% 18%, rgba(42, 207, 200, .30), transparent 29%),
                radial-gradient(circle at 20% 80%, rgba(104, 71, 245, .24), transparent 31%),
                linear-gradient(145deg, rgba(238, 245, 255, .98), rgba(246, 240, 255, .96));
            box-shadow: 0 28px 70px rgba(77, 73, 155, .16);
        }}

        .wf-art-globe {{
            position: absolute;
            top: 1.1rem;
            right: 1.25rem;
            font-size: 8.5rem;
            opacity: .24;
            filter: saturate(.85);
        }}

        .wf-art-learner {{
            position: absolute;
            z-index: 3;
            right: 13%;
            bottom: 4.8rem;
            font-size: clamp(7rem, 14vw, 11.5rem);
            line-height: 1;
            filter: drop-shadow(0 22px 22px rgba(63, 54, 137, .22));
        }}

        .wf-art-headphones {{
            position: absolute;
            z-index: 4;
            right: 33%;
            top: 26%;
            font-size: 3.2rem;
            transform: rotate(-10deg);
        }}

        .wf-art-laptop {{
            position: absolute;
            z-index: 5;
            right: 8%;
            bottom: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: .45rem;
            width: 58%;
            min-height: 5.4rem;
            border: 1px solid rgba(255, 255, 255, .85);
            border-radius: 1.2rem 1.2rem .45rem .45rem;
            background: linear-gradient(145deg, #f9fbff, #d9e2f7);
            color: #20266f;
            box-shadow: 0 18px 30px rgba(57, 62, 130, .25);
            font-size: 1.12rem;
        }}

        .wf-art-laptop span {{
            font-size: 1.45rem;
        }}

        .wf-art-books {{
            position: absolute;
            z-index: 4;
            left: 7%;
            bottom: 1.2rem;
            font-size: 5.5rem;
            filter: drop-shadow(0 12px 14px rgba(48, 52, 120, .18));
        }}

        .wf-art-bubble {{
            position: absolute;
            z-index: 6;
            padding: .62rem .9rem;
            border-radius: 1rem 1rem 1rem .25rem;
            color: white;
            box-shadow: 0 12px 24px rgba(70, 62, 145, .17);
            font-size: .95rem;
            font-weight: 900;
            transform: rotate(-4deg);
        }}

        .wf-art-bubble-one {{
            top: 11%;
            left: 8%;
            background: linear-gradient(135deg, #48d3a0, #22b88a);
        }}

        .wf-art-bubble-two {{
            top: 30%;
            left: 2.5%;
            background: linear-gradient(135deg, #7c5af3, #5636d4);
            transform: rotate(3deg);
        }}

        .wf-art-bubble-three {{
            top: 12%;
            right: 23%;
            background: linear-gradient(135deg, #ffb83d, #ff8b3d);
            transform: rotate(3deg);
        }}

        .wf-section-heading {{
            margin: 2.25rem 0 .2rem;
            color: var(--wf-heading);
            font-size: clamp(1.55rem, 2.3vw, 2.15rem);
            font-weight: 950;
            letter-spacing: -.045em;
        }}

        .wf-section-copy {{
            margin: 0 0 1rem;
            color: var(--wf-muted);
            font-size: .95rem;
        }}

        /* Cards */
        .wf-stat {{
            min-height: 6.45rem;
            padding: 1rem 1.05rem;
            border: 1px solid var(--wf-border);
            border-radius: 1.15rem;
            background: linear-gradient(145deg, var(--wf-surface-raised), var(--wf-surface));
            box-shadow: var(--wf-soft-shadow);
        }}

        .wf-stat-label {{
            color: var(--wf-muted);
            font-size: .76rem;
            font-weight: 850;
            letter-spacing: .025em;
            text-transform: uppercase;
        }}

        .wf-stat-value {{
            margin-top: .38rem;
            color: var(--wf-heading);
            font-size: 1.48rem;
            font-weight: 950;
            line-height: 1.15;
        }}

        .wf-activity-card {{
            min-height: 14.4rem;
            padding: 1.25rem;
            border: 1px solid var(--wf-border);
            border-radius: 1.45rem;
            background: linear-gradient(155deg, var(--wf-surface-raised), var(--wf-surface));
            box-shadow: var(--wf-soft-shadow);
            transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
        }}

        .wf-activity-card:hover {{
            border-color: rgba(104, 71, 245, .28);
            box-shadow: var(--wf-shadow);
            transform: translateY(-4px);
        }}

        .wf-activity-icon {{
            display: grid;
            place-items: center;
            width: 5.3rem;
            height: 5.3rem;
            margin: .15rem auto 1rem;
            border-radius: 1.55rem;
            background: var(--wf-card-gradient);
            box-shadow: 0 14px 28px var(--wf-card-shadow);
            font-size: 2.75rem;
        }}

        .wf-activity-title {{
            margin-bottom: .42rem;
            color: var(--wf-heading);
            font-size: 1.22rem;
            font-weight: 950;
            text-align: center;
            letter-spacing: -.025em;
        }}

        .wf-activity-copy {{
            color: var(--wf-muted);
            font-size: .86rem;
            line-height: 1.5;
            text-align: center;
        }}

        .wf-language-card {{
            min-height: 5.8rem;
            padding: .75rem .45rem;
            border: 1px solid var(--wf-border);
            border-radius: 1.08rem;
            background: var(--wf-surface);
            box-shadow: var(--wf-soft-shadow);
            text-align: center;
        }}

        .wf-language-flag {{
            font-size: 2rem;
            line-height: 1.2;
        }}

        .wf-language-name {{
            margin-top: .32rem;
            color: var(--wf-heading);
            font-size: .82rem;
            font-weight: 900;
        }}

        .wf-language-native {{
            margin-top: .06rem;
            color: var(--wf-muted);
            font-size: .69rem;
        }}

        .wf-level-card {{
            padding: 1.15rem 1.25rem;
            border: 1px solid rgba(104, 71, 245, .18);
            border-radius: 1.25rem;
            background: linear-gradient(135deg, rgba(104, 71, 245, .10), rgba(22, 199, 191, .09));
        }}

        .wf-level-card strong {{
            color: var(--wf-heading);
        }}

        .wf-level-card p {{
            margin: .25rem 0 0;
            color: var(--wf-muted);
        }}

        .wf-mini-card {{
            min-height: 7.3rem;
            padding: 1.05rem 1.15rem;
            border: 1px solid var(--wf-border);
            border-radius: 1.15rem;
            background: var(--wf-surface);
            box-shadow: var(--wf-soft-shadow);
        }}

        .wf-mini-card strong {{
            display: block;
            margin: .35rem 0 .2rem;
            color: var(--wf-heading);
            font-size: 1rem;
        }}

        .wf-mini-card p {{
            margin: 0;
            color: var(--wf-muted);
            font-size: .8rem;
            line-height: 1.45;
        }}

        /* Native Streamlit controls */
        div.stButton > button,
        div[data-testid="stFormSubmitButton"] > button {{
            min-height: 2.9rem;
            border: 1px solid var(--wf-border);
            border-radius: .9rem;
            background: var(--wf-surface);
            box-shadow: 0 6px 15px rgba(40, 55, 95, .04);
            color: var(--wf-text);
            font-weight: 850;
            transition: transform .16s ease, border-color .16s ease, box-shadow .16s ease;
        }}

        div.stButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {{
            border-color: rgba(104, 71, 245, .44);
            box-shadow: 0 9px 22px rgba(104, 71, 245, .11);
            color: var(--wf-purple);
            transform: translateY(-1px);
        }}

        button[kind="primary"] {{
            border: none !important;
            background: linear-gradient(120deg, var(--wf-purple), var(--wf-blue), var(--wf-teal)) !important;
            background-size: 180% 180% !important;
            box-shadow: 0 10px 24px rgba(104, 71, 245, .20) !important;
            color: white !important;
        }}

        button[kind="primary"]:hover {{
            background-position: 100% 50% !important;
            color: white !important;
        }}

        button:focus-visible {{
            outline: 3px solid rgba(60, 140, 244, .32) !important;
            outline-offset: 2px;
        }}

        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div,
        [data-baseweb="textarea"] > div,
        [data-testid="stNumberInputContainer"] > div {{
            border-color: var(--wf-border) !important;
            border-radius: .85rem !important;
            background: var(--wf-input) !important;
            color: var(--wf-text) !important;
        }}

        [data-testid="stExpander"] {{
            overflow: hidden;
            border: 1px solid var(--wf-border);
            border-radius: 1rem;
            background: var(--wf-surface);
            box-shadow: var(--wf-soft-shadow);
        }}

        [data-testid="stMetric"] {{
            padding: .85rem 1rem;
            border: 1px solid var(--wf-border);
            border-radius: 1rem;
            background: var(--wf-surface);
        }}

        [data-testid="stProgress"] > div > div {{
            background: linear-gradient(90deg, var(--wf-purple), var(--wf-teal));
        }}

        [data-testid="stAlert"] {{
            border-radius: 1rem;
        }}

        [data-testid="stTabs"] [data-baseweb="tab-list"] {{
            gap: .4rem;
        }}

        [data-testid="stTabs"] button[role="tab"] {{
            border-radius: .8rem .8rem 0 0;
            color: var(--wf-text);
            font-weight: 800;
        }}

        @media (max-width: 900px) {{
            .wf-brand-tagline {{
                display: none;
            }}

            .wf-hero-title {{
                font-size: clamp(2.65rem, 9vw, 4.2rem);
            }}

            .wf-hero-visual {{
                min-height: 360px;
            }}

            div[data-testid="stHorizontalBlock"]:has(.wf-brand-lockup) div.stButton > button {{
                padding: .38rem .35rem !important;
                font-size: .74rem !important;
            }}
        }}

        @media (max-width: 640px) {{
            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .wf-brand-name {{
                font-size: 1.15rem;
            }}

            .wf-brand-mark {{
                width: 2.55rem;
                height: 2.55rem;
                flex-basis: 2.55rem;
            }}

            .wf-activity-card {{
                min-height: auto;
            }}

            .wf-stat {{
                min-height: auto;
            }}

            .wf-hero-visual {{
                min-height: 320px;
            }}

            .wf-art-books {{
                font-size: 4rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
