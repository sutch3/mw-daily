from __future__ import annotations


CATEGORY_ACCENTS = {
    "Viticulture": "#4F7D5A",
    "Vinification": "#7A1F35",
    "Wine business": "#B7892C",
    "Global wine regions": "#2F6F73",
    "Current issues": "#A34E35",
    "Tasting logic": "#4D5E8F",
    "Research paper skills": "#6F6265",
}


def category_accent(category: str) -> str:
    return CATEGORY_ACCENTS.get(category, "#7A1F35")


def apply_global_styles() -> None:
    import streamlit as st

    st.markdown(
        """
        <style>
        :root {
            --burgundy: #7A1F35;
            --burgundy-dark: #521525;
            --ink: #211B1D;
            --muted: #6F6265;
            --paper: #FFFDFC;
            --blush: #F8F3F1;
            --gold: #B7892C;
            --sage: #4F7D5A;
            --teal: #2F6F73;
            --line: #E8DCD7;
            --shadow: 0 18px 50px rgba(35, 31, 32, 0.08);
        }

        .stApp {
            background:
                linear-gradient(180deg, rgba(248, 243, 241, 0.78) 0%, rgba(255, 253, 252, 1) 34%),
                var(--paper);
            color: var(--ink);
        }

        [data-testid="stSidebar"] {
            background: var(--blush);
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
            border-bottom: 1px solid var(--line);
            background: transparent;
            padding: 0.4rem 0 1.05rem;
            margin-bottom: 1.15rem;
        }

        .hero-row {
            align-items: center;
            display: flex;
            gap: 1rem;
        }

        .brand-mark {
            align-items: center;
            background: var(--burgundy);
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
            color: var(--burgundy);
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

        .study-card {
            --category-accent: var(--burgundy);
            border: 1px solid var(--line);
            border-left: 8px solid var(--category-accent);
            border-radius: 8px;
            padding: 1.45rem;
            background: #FFFFFF;
            box-shadow: 0 10px 34px rgba(35, 31, 32, 0.06);
            position: relative;
        }

        .study-card::after {
            background:
                linear-gradient(90deg, var(--category-accent), transparent);
            bottom: 0;
            content: "";
            height: 4px;
            left: 0;
            opacity: 0.75;
            position: absolute;
            right: 0;
        }

        .question-prompt {
            font-family: Georgia, serif;
            font-size: clamp(1.35rem, 2.3vw, 1.78rem);
            line-height: 1.38;
            margin: 0.8rem 0 0.35rem;
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
            background: var(--blush);
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

        .workspace-label {
            color: var(--muted);
            font-size: 0.88rem;
            margin-top: -0.45rem;
            margin-bottom: 0.8rem;
        }

        div.stButton > button {
            border-radius: 6px;
            border: 1px solid var(--burgundy);
            font-weight: 650;
        }

        div.stButton > button[kind="primary"] {
            background: var(--burgundy);
        }

        div.stButton > button:hover {
            border-color: var(--burgundy-dark);
            color: var(--burgundy-dark);
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
        </style>
        """,
        unsafe_allow_html=True,
    )
