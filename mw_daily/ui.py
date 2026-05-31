from __future__ import annotations


CATEGORY_ACCENTS = {
    "Viticulture": "#2F7D4C",
    "Vinification": "#6D3153",
    "Wine business": "#9A7A2F",
    "Global wine regions": "#28706C",
    "Current issues": "#A35A3B",
    "Tasting logic": "#486B8F",
    "Research paper skills": "#647260",
}


def category_accent(category: str) -> str:
    return CATEGORY_ACCENTS.get(category, "#7A1F35")


def apply_global_styles() -> None:
    import streamlit as st

    st.markdown(
        """
        <style>
        :root {
            --forest: #1F5A3D;
            --forest-dark: #153F2B;
            --vine: #2F7D4C;
            --leaf: #6FAF6F;
            --grape: #6D3153;
            --ink: #1F251F;
            --muted: #637064;
            --paper: #FCFCF7;
            --mist: #F2F6EE;
            --cream: #FAF7EF;
            --gold: #B59A55;
            --line: #DDE6D8;
            --shadow: 0 18px 45px rgba(31, 90, 61, 0.10);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(111, 175, 111, 0.16), transparent 28rem),
                linear-gradient(180deg, rgba(242, 246, 238, 0.92) 0%, rgba(252, 252, 247, 1) 34%),
                var(--paper);
            color: var(--ink);
        }

        [data-testid="stSidebar"] {
            background: var(--mist);
        }

        .block-container {
            max-width: 1040px;
            padding-top: 1.4rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, p, label, div {
            letter-spacing: 0;
        }

        h1, h2, h3 {
            color: var(--ink);
        }

        .hero-panel {
            border: 1px solid var(--line);
            border-radius: 8px;
            background:
                linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(242, 246, 238, 0.78));
            box-shadow: 0 16px 40px rgba(31, 90, 61, 0.08);
            overflow: hidden;
            padding: 1.15rem 1.2rem 0.85rem;
            margin-bottom: 1rem;
            position: relative;
        }

        .hero-row {
            align-items: center;
            display: flex;
            gap: 1rem;
        }

        .brand-mark {
            align-items: center;
            background: var(--forest);
            border-bottom: 4px solid var(--gold);
            border-radius: 8px;
            color: #FFFFFF;
            display: flex;
            flex: 0 0 auto;
            font-family: Georgia, serif;
            font-size: 1rem;
            font-weight: 700;
            height: 3.1rem;
            justify-content: center;
            width: 3.1rem;
        }

        .eyebrow {
            color: var(--forest);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0;
            text-transform: uppercase;
            margin-bottom: 0.22rem;
        }

        .hero-title {
            font-family: Georgia, serif;
            font-size: clamp(2rem, 4.2vw, 3rem);
            font-weight: 700;
            line-height: 1.03;
            margin: 0;
        }

        .lede {
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.55;
            max-width: 760px;
            margin: 0.5rem 0 0;
        }

        .vine-line {
            margin-top: 0.85rem;
            max-width: 720px;
            opacity: 0.9;
        }

        .vine-line svg {
            display: block;
            height: 38px;
            width: 100%;
        }

        .study-surface {
            background:
                linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(242, 246, 238, 0.72));
            border: 1px solid var(--line);
            border-radius: 8px;
            box-shadow: var(--shadow);
            padding: 1rem;
        }

        .study-card {
            --category-accent: var(--vine);
            border-left: 6px solid var(--category-accent);
            padding: 0.35rem 0 0.4rem 1.15rem;
            background: transparent;
            position: relative;
        }

        .study-card::after {
            display: none;
        }

        .question-prompt {
            font-family: Georgia, serif;
            font-size: clamp(1.45rem, 2.5vw, 1.95rem);
            line-height: 1.38;
            margin: 0.55rem 0 0.35rem;
        }

        .meta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            margin-top: 1rem;
        }

        .pill {
            align-items: center;
            border: 1px solid var(--line);
            border-radius: 999px;
            color: var(--muted);
            display: inline-flex;
            font-size: 0.85rem;
            gap: 0.4rem;
            padding: 0.28rem 0.72rem;
            background: rgba(255, 255, 255, 0.75);
        }

        .pill-accent {
            background: var(--category-accent);
            border-radius: 999px;
            display: inline-block;
            height: 0.55rem;
            width: 0.55rem;
        }

        .quiet-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.84);
            padding: 1rem;
        }

        .section-rule {
            border-top: 1px solid var(--line);
            margin: 1.2rem 0;
        }

        .section-rule.tight {
            margin: 0.95rem 0;
        }

        .workspace-label {
            color: var(--muted);
            font-size: 0.88rem;
            margin-top: -0.45rem;
            margin-bottom: 0.8rem;
        }

        .desk-label {
            color: var(--forest);
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
            text-transform: uppercase;
        }

        [data-testid="stSegmentedControl"] {
            margin-top: 0.15rem;
        }

        [data-testid="stSegmentedControl"] button {
            border: 1px solid var(--line) !important;
            border-radius: 999px !important;
            min-height: 2.55rem;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        [data-testid="stSegmentedControl"] button[aria-pressed="true"],
        [data-testid="stSegmentedControl"] button[aria-selected="true"] {
            background: var(--forest) !important;
            border-color: var(--forest) !important;
            color: #FFFFFF !important;
        }

        div.stButton > button {
            border-radius: 6px;
            border: 1px solid var(--forest);
            font-weight: 650;
        }

        div.stButton > button[kind="primary"] {
            background: var(--forest);
        }

        div.stButton > button:hover {
            border-color: var(--forest-dark);
            color: var(--forest-dark);
        }

        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.8rem 0.95rem;
        }

        textarea, input {
            border-radius: 6px !important;
        }

        .stSlider [data-baseweb="slider"] > div {
            color: var(--forest);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
