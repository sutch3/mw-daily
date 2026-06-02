from __future__ import annotations

import random
import time
from datetime import date

import requests
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


def countdown_state(
    timer_key: str, countdown_seconds: int
) -> tuple[bool, int, int, bool]:
    running, elapsed_seconds = timer_state(timer_key)
    capped_elapsed = min(elapsed_seconds, countdown_seconds)
    remaining_seconds = max(countdown_seconds - elapsed_seconds, 0)
    is_finished = running and remaining_seconds == 0
    return running, capped_elapsed, remaining_seconds, is_finished


apply_global_styles()

questions = load_questions()

st.markdown(
    """
    <section class="hero-panel">
        <div class="hero-row">
            <div class="brand-mark">S</div>
            <div>
                <div class="eyebrow">Sara's vine-side MW practice</div>
                <h1 class="hero-title">Sara's MW Daily</h1>
                <p class="lede">One corker of a question a day, a clear place to think, and a little guidance when the answer needs uncorking.</p>
            </div>
        </div>
        <div class="vine-line" aria-hidden="true">
            <svg viewBox="0 0 720 46" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 31C92 7 128 44 207 21C286 -2 339 42 413 24C502 2 573 8 710 27" stroke="#2F7D4C" stroke-width="3" stroke-linecap="round"/>
                <path d="M112 20C96 6 76 7 66 20C85 31 101 30 112 20Z" fill="#6FAF6F"/>
                <path d="M314 26C296 11 276 14 266 28C285 38 302 37 314 26Z" fill="#6FAF6F"/>
                <path d="M545 16C529 4 511 6 501 18C518 28 535 27 545 16Z" fill="#6FAF6F"/>
                <circle cx="634" cy="25" r="5" fill="#6D3153"/>
                <circle cx="646" cy="27" r="5" fill="#6D3153"/>
                <circle cx="640" cy="37" r="5" fill="#6D3153"/>
            </svg>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown('<div class="desk-label">My question desk</div>', unsafe_allow_html=True)
    mode_col, random_col, date_col, history_col = st.columns(
        [0.42, 0.2, 0.2, 0.18],
        vertical_alignment="bottom",
    )

    with mode_col:
        mode = st.pills(
            "Question mode",
            ["Daily question", "Random question"],
            default="Daily question",
            key="question_mode",
            width="content",
        )
        mode = mode or "Daily question"

    with random_col:
        if mode == "Random question":
            if "random_question_id" not in st.session_state:
                st.session_state.random_question_id = random.choice(questions)["id"]
            if st.button("New random", width="content"):
                st.session_state.random_question_id = random.choice(questions)["id"]

    with date_col:
        st.caption(f"Study date: {date.today().isoformat()}")

    with history_col:
        if st.button("History", width="content"):
            st.session_state["show_history_page"] = True
            st.switch_page("pages/1_History.py")

    if mode == "Random question":
        active_question = next(
            question for question in questions if question["id"] == st.session_state.random_question_id
        )
    else:
        active_question = question_for_day(questions)

    st.markdown('<div class="section-rule tight"></div>', unsafe_allow_html=True)
    render_question_card(active_question, mode)

    answer_key = f"answer_{active_question['id']}_{mode}"
    reveal_key = f"revealed_{active_question['id']}_{mode}"
    timer_key = f"timer_{active_question['id']}_{mode}"
    timing_mode_key = f"{timer_key}_mode"
    countdown_minutes_key = f"{timer_key}_countdown_minutes"
    quality_key = f"quality_{active_question['id']}_{mode}"
    feedback_key = f"feedback_{active_question['id']}_{mode}"
    feedback_notice_key = f"feedback_notice_{active_question['id']}_{mode}"
    timing_mode = st.session_state.get(timing_mode_key, "Stopwatch")
    countdown_minutes = int(st.session_state.get(countdown_minutes_key, 30))
    if timing_mode == "Countdown":
        timer_running, elapsed_seconds, remaining_seconds, countdown_finished = countdown_state(
            timer_key, countdown_minutes * 60
        )
    else:
        timer_running, elapsed_seconds = timer_state(timer_key)
        remaining_seconds = 0
        countdown_finished = False

    def save_current_attempt(status: str, answer_text: str) -> bool:
        try:
            save_attempt(
                {
                    "question_id": active_question["id"],
                    "study_date": date.today().isoformat(),
                    "mode": mode,
                    "status": status,
                    "answer": answer_text.strip(),
                    "time_seconds": elapsed_seconds,
                    "question_quality": quality,
                    "question_feedback": question_feedback.strip(),
                }
            )
        except requests.RequestException:
            st.error("I couldn't save to GitHub just now. Try again in a minute.")
            return False
        return True

    st.markdown('<div class="section-rule tight"></div>', unsafe_allow_html=True)
    feedback_left, feedback_right = st.columns([0.38, 0.62], vertical_alignment="top")

    with feedback_left:
        st.markdown("**Rate this question.**")
        quality = st.slider(
            "Question usefulness",
            min_value=1,
            max_value=5,
            value=4,
            key=quality_key,
            help="1 = not useful, 5 = excellent practice question.",
            label_visibility="collapsed",
        )

    with feedback_right:
        question_feedback = st.text_area(
            "Question notes",
            key=feedback_key,
            height=92,
            placeholder="Too easy, too broad, great topic, needs more tasting logic...",
        )
        if st.button("Save feedback", use_container_width=True):
            if save_current_attempt("rated", ""):
                st.session_state[feedback_notice_key] = "Feedback saved."

        if st.session_state.get(feedback_notice_key):
            st.success(st.session_state[feedback_notice_key])

with st.container(border=True):
    st.subheader("Response workspace")
    st.markdown(
        '<p class="workspace-label">Time my attempt, write my answer, or open the model answer as a study aid.</p>',
        unsafe_allow_html=True,
    )
    timing_setup_cols = st.columns([0.36, 0.24, 0.4], vertical_alignment="bottom")

    with timing_setup_cols[0]:
        selected_timing_mode = st.pills(
            "Timing tool",
            ["Stopwatch", "Countdown"],
            default=timing_mode,
            key=timing_mode_key,
            width="content",
        )
        timing_mode = selected_timing_mode or "Stopwatch"

    with timing_setup_cols[1]:
        if timing_mode == "Countdown":
            countdown_minutes = st.number_input(
                "Minutes",
                min_value=1,
                max_value=180,
                value=countdown_minutes,
                step=5,
                key=countdown_minutes_key,
                disabled=timer_running,
            )

    if timing_mode == "Countdown":
        timer_running, elapsed_seconds, remaining_seconds, countdown_finished = countdown_state(
            timer_key, int(countdown_minutes) * 60
        )
    else:
        timer_running, elapsed_seconds = timer_state(timer_key)
        remaining_seconds = 0
        countdown_finished = False

    timer_columns = st.columns([0.18, 0.18, 0.18, 0.23, 0.23], vertical_alignment="center")

    with timer_columns[0]:
        if st.button("Start", use_container_width=True, disabled=timer_running):
            st.session_state[f"{timer_key}_started_at"] = time.time()
            st.rerun()
    with timer_columns[1]:
        if st.button("Stop", use_container_width=True, disabled=not timer_running):
            st.session_state[f"{timer_key}_elapsed_seconds"] = elapsed_seconds
            st.session_state[f"{timer_key}_started_at"] = None
            st.rerun()
    with timer_columns[2]:
        if st.button("Reset", use_container_width=True):
            st.session_state[f"{timer_key}_elapsed_seconds"] = 0
            st.session_state[f"{timer_key}_started_at"] = None
            st.rerun()
    with timer_columns[3]:
        st.metric("Time taken", format_duration(elapsed_seconds))
    with timer_columns[4]:
        if timing_mode == "Countdown":
            st.metric("Time remaining", format_duration(remaining_seconds))
        else:
            st.metric("Timing mode", "Stopwatch")

    if countdown_finished:
        st.warning("Time is up.")

    answer = st.text_area(
        "My answer",
        key=answer_key,
        height=260,
        placeholder="Write a structured MW-style answer: define the issue, compare causes or options, weigh trade-offs, then reach a judgement.",
    )

    save_col, skip_col, reveal_col = st.columns([0.24, 0.24, 0.52], vertical_alignment="center")
    with save_col:
        if st.button("Save", type="primary", use_container_width=True):
            if answer.strip() or question_feedback.strip():
                if save_current_attempt("answered", answer):
                    st.success("Saved.")
            else:
                st.warning("Write an answer or add question feedback before saving.")

    with skip_col:
        if st.button("Skip question", use_container_width=True):
            if save_current_attempt("skipped", ""):
                st.success("Skipped and saved to history.")

    with reveal_col:
        if st.button("Show model answer", use_container_width=True):
            st.session_state[reveal_key] = True

if st.session_state.get(reveal_key, False):
    st.divider()
    render_feedback(active_question)
