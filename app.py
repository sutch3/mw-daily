from __future__ import annotations

import random
import time
from datetime import date

import streamlit as st

from mw_daily.questions import question_for_day, load_questions
from mw_daily.storage import save_attempt
from mw_daily.time_format import format_duration
from mw_daily.ui import apply_global_styles, category_accent


st.set_page_config(
    page_title="MW Daily",
    page_icon="MW",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_question_card(question: dict, mode: str) -> None:
    accent = category_accent(question["category"])
    st.markdown(
        f"""<div class="study-card" style="--category-accent: {accent};">
            <div class="eyebrow">Today in MW Daily</div>
            <div class="question-prompt">{question["prompt"]}</div>
            <div class="meta-row">
                <span class="pill"><span class="pill-accent"></span>{question["category"]}</span>
                <span class="pill">{question["difficulty"]}</span>
                <span class="pill">{mode}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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


apply_global_styles()

questions = load_questions()

st.markdown(
    """
    <section class="hero-panel">
        <div class="hero-row">
            <div class="brand-mark">MW</div>
            <div>
                <div class="eyebrow">Master of Wine preparation</div>
                <h1 class="hero-title">MW Daily</h1>
                <p class="lede">One analytical question, one focused answer, one clear piece of feedback. Built for steady MW exam preparation without ceremony.</p>
            </div>
        </div>
    </section>
    """,
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
    st.divider()
    st.subheader("Question feedback")
    quality_key = f"quality_{active_question['id']}_{mode}"
    feedback_key = f"feedback_{active_question['id']}_{mode}"
    quality = st.slider(
        "Question usefulness",
        min_value=1,
        max_value=5,
        value=4,
        key=quality_key,
        help="1 = not useful, 5 = excellent practice question.",
    )
    question_feedback = st.text_area(
        "Notes on this question",
        key=feedback_key,
        height=130,
        placeholder="Optional: too easy, too broad, great topic, needs more tasting logic, not exam-like enough...",
    )

with left:
    render_question_card(active_question, mode)

st.divider()

answer_key = f"answer_{active_question['id']}_{mode}"
reveal_key = f"revealed_{active_question['id']}_{mode}"
timer_key = f"timer_{active_question['id']}_{mode}"

with st.container(border=True):
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

save_col, reveal_col = st.columns([0.28, 0.72], vertical_alignment="center")
with save_col:
    if st.button("Save", type="primary", use_container_width=True):
        if answer.strip() or question_feedback.strip():
            save_attempt(
                {
                    "question_id": active_question["id"],
                    "study_date": date.today().isoformat(),
                    "mode": mode,
                    "answer": answer.strip(),
                    "time_seconds": elapsed_seconds,
                    "question_quality": quality,
                    "question_feedback": question_feedback.strip(),
                }
            )
            st.success("Saved.")
        else:
            st.warning("Write an answer or add question feedback before saving.")

with reveal_col:
    if st.button("Show model answer", use_container_width=True):
        st.session_state[reveal_key] = True

if st.session_state.get(reveal_key, False):
    st.divider()
    render_feedback(active_question)
