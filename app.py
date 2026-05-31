from __future__ import annotations

import random
import time
from datetime import date

import streamlit as st

from mw_daily.questions import question_for_day, load_questions
from mw_daily.storage import save_attempt
from mw_daily.time_format import format_duration


st.set_page_config(
    page_title="MW Daily",
    page_icon="MW",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --burgundy: #7A1F35;
            --ink: #231F20;
            --muted: #6F6265;
            --paper: #FFFDFC;
            --blush: #F8F3F1;
            --line: #E9DEDB;
        }

        .stApp {
            background: var(--paper);
            color: var(--ink);
        }

        [data-testid="stSidebar"] {
            background: var(--blush);
        }

        .block-container {
            max-width: 1080px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: 0;
        }

        .eyebrow {
            color: var(--burgundy);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .lede {
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.6;
            max-width: 760px;
            margin-bottom: 1.5rem;
        }

        .study-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1.45rem;
            background: #FFFFFF;
            box-shadow: 0 18px 45px rgba(35, 31, 32, 0.06);
        }

        .question-prompt {
            font-size: 1.45rem;
            line-height: 1.45;
            margin: 0.75rem 0 0.25rem;
        }

        .meta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            margin-top: 1rem;
        }

        .pill {
            border: 1px solid var(--line);
            border-radius: 999px;
            color: var(--muted);
            font-size: 0.85rem;
            padding: 0.28rem 0.7rem;
            background: var(--blush);
        }

        div.stButton > button {
            border-radius: 6px;
            border: 1px solid var(--burgundy);
        }

        div.stButton > button[kind="primary"] {
            background: var(--burgundy);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_question_card(question: dict, mode: str) -> None:
    st.markdown('<div class="study-card">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Today in MW Daily</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-prompt">{question["prompt"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="meta-row">
            <span class="pill">{question["category"]}</span>
            <span class="pill">{question["difficulty"]}</span>
            <span class="pill">{mode}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_feedback(question: dict) -> None:
    st.subheader("Model Answer")
    st.write(question["model_answer"])

    columns = st.columns(3)
    with columns[0]:
        st.markdown("**Key marking points**")
        for point in question["marking_points"]:
            st.markdown(f"- {point}")
    with columns[1]:
        st.markdown("**Common traps**")
        for trap in question["common_traps"]:
            st.markdown(f"- {trap}")
    with columns[2]:
        st.markdown("**Follow-up reading**")
        for topic in question["follow_up_topics"]:
            st.markdown(f"- {topic}")


def timer_state(timer_key: str) -> tuple[bool, int]:
    started_at = st.session_state.get(f"{timer_key}_started_at")
    saved_seconds = int(st.session_state.get(f"{timer_key}_elapsed_seconds", 0))
    if started_at is None:
        return False, saved_seconds
    return True, saved_seconds + int(time.time() - started_at)


apply_styles()

questions = load_questions()

st.markdown('<div class="eyebrow">Master of Wine preparation</div>', unsafe_allow_html=True)
st.title("MW Daily")
st.markdown(
    '<p class="lede">One analytical question, one focused answer, one clear piece of feedback. Built for steady MW exam preparation without ceremony.</p>',
    unsafe_allow_html=True,
)

left, right = st.columns([0.64, 0.36], vertical_alignment="top")

with right:
    st.subheader("Mode")
    mode = st.radio(
        "Choose study mode",
        ["Daily question", "Random question"],
        label_visibility="collapsed",
    )

    if mode == "Random question":
        if "random_question_id" not in st.session_state:
            st.session_state.random_question_id = random.choice(questions)["id"]
        if st.button("New random question"):
            st.session_state.random_question_id = random.choice(questions)["id"]
        active_question = next(
            question for question in questions if question["id"] == st.session_state.random_question_id
        )
    else:
        active_question = question_for_day(questions)

    st.caption(f"Study date: {date.today().isoformat()}")

with left:
    render_question_card(active_question, mode)

st.divider()

answer_key = f"answer_{active_question['id']}_{mode}"
score_key = f"score_{active_question['id']}_{mode}"
reveal_key = f"revealed_{active_question['id']}_{mode}"
timer_key = f"timer_{active_question['id']}_{mode}"

st.subheader("Timed answer")
timer_running, elapsed_seconds = timer_state(timer_key)
timer_columns = st.columns([0.2, 0.2, 0.2, 0.4], vertical_alignment="center")

with timer_columns[0]:
    if st.button("Start timer", use_container_width=True, disabled=timer_running):
        st.session_state[f"{timer_key}_started_at"] = time.time()
        st.rerun()
with timer_columns[1]:
    if st.button("Stop timer", use_container_width=True, disabled=not timer_running):
        st.session_state[f"{timer_key}_elapsed_seconds"] = elapsed_seconds
        st.session_state[f"{timer_key}_started_at"] = None
        st.rerun()
with timer_columns[2]:
    if st.button("Reset timer", use_container_width=True):
        st.session_state[f"{timer_key}_elapsed_seconds"] = 0
        st.session_state[f"{timer_key}_started_at"] = None
        st.rerun()
with timer_columns[3]:
    st.metric("Time taken", format_duration(elapsed_seconds))

answer = st.text_area(
    "Sara's answer",
    key=answer_key,
    height=260,
    placeholder="Write a structured MW-style answer: define the issue, compare causes or options, weigh trade-offs, then reach a judgement.",
)

score = st.slider(
    "Self-score",
    min_value=1,
    max_value=5,
    value=3,
    key=score_key,
    help="1 = weak answer, 5 = exam-ready answer.",
)

save_col, reveal_col = st.columns([0.28, 0.72], vertical_alignment="center")
with save_col:
    if st.button("Save answer", type="primary", use_container_width=True):
        if answer.strip():
            save_attempt(
                {
                    "question_id": active_question["id"],
                    "study_date": date.today().isoformat(),
                    "mode": mode,
                    "answer": answer.strip(),
                    "self_score": score,
                    "time_seconds": elapsed_seconds,
                }
            )
            st.success("Saved.")
        else:
            st.warning("Write an answer before saving.")

with reveal_col:
    if st.button("Reveal model answer", use_container_width=True):
        st.session_state[reveal_key] = True

if st.session_state.get(reveal_key, False):
    st.divider()
    render_feedback(active_question)
