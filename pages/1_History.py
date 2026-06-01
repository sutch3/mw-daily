from __future__ import annotations

import streamlit as st

from mw_daily.analytics import category_counts, question_lookup
from mw_daily.questions import load_questions
from mw_daily.storage import load_attempts
from mw_daily.time_format import format_duration
from mw_daily.ui import apply_global_styles


st.set_page_config(page_title="MW Daily History", page_icon="MW", layout="wide")
apply_global_styles()

if not st.session_state.get("show_history_page"):
    st.switch_page("app.py")

st.markdown(
    """
    <section class="hero-panel">
        <div class="hero-row">
            <div class="brand-mark">S</div>
            <div>
                <div class="eyebrow">My study record</div>
                <h1 class="hero-title">History</h1>
                <p class="lede">Coverage, time taken, question feedback, and the answer history I am building.</p>
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

if st.button("Back to today's question", type="primary", width="content"):
    st.session_state["show_history_page"] = False
    st.switch_page("app.py")

questions = load_questions()
attempts = load_attempts()
lookup = question_lookup(questions)
answered_attempts = [
    attempt for attempt in attempts if attempt.get("status", "answered") == "answered"
]
skipped_attempts = [
    attempt for attempt in attempts if attempt.get("status") == "skipped"
]
rated_attempts_only = [
    attempt for attempt in attempts if attempt.get("status") == "rated"
]

answered_count = len(answered_attempts)
timed_attempts = [
    attempt for attempt in answered_attempts if attempt.get("time_seconds") is not None
]
rated_attempts = [attempt for attempt in attempts if attempt.get("question_quality")]
average_time = (
    sum(int(attempt["time_seconds"]) for attempt in timed_attempts) / len(timed_attempts)
    if timed_attempts
    else None
)
average_quality = (
    sum(int(attempt["question_quality"]) for attempt in rated_attempts) / len(rated_attempts)
    if rated_attempts
    else None
)

metric_columns = st.columns(6)
metric_columns[0].metric("Questions answered", answered_count)
metric_columns[1].metric("Questions rated", len(rated_attempts_only))
metric_columns[2].metric("Questions skipped", len(skipped_attempts))
metric_columns[3].metric("Question bank", len(questions))
metric_columns[4].metric("Average time", format_duration(average_time))
metric_columns[5].metric(
    "Question usefulness",
    f"{average_quality:.1f}/5" if average_quality is not None else "-",
)

st.divider()

st.subheader("Category coverage")
counts = category_counts(answered_attempts, questions)
categories = sorted({question["category"] for question in questions})
if answered_attempts:
    st.bar_chart({category: counts.get(category, 0) for category in categories})
else:
    st.info("No saved answers yet.")

st.divider()
st.subheader("My answer history")

if attempts:
    for attempt in reversed(attempts):
        question = lookup.get(attempt["question_id"], {})
        time_taken = format_duration(attempt.get("time_seconds"))
        status = attempt.get("status", "answered")
        status_labels = {
            "answered": "Answered",
            "rated": "Rated",
            "skipped": "Skipped",
        }
        status_label = status_labels.get(status, "Answered")
        title = (
            f"{attempt['study_date']} · {question.get('category', 'Unknown')} · "
            f"{status_label} · {time_taken}"
        )
        with st.expander(title):
            st.write(question.get("prompt", "Question unavailable."))
            detail_columns = st.columns(4)
            detail_columns[0].metric("Difficulty", question.get("difficulty", "-"))
            detail_columns[1].metric("Mode", attempt.get("mode", "-"))
            detail_columns[2].metric("Time taken", time_taken)
            detail_columns[3].metric(
                "Question usefulness",
                f"{attempt.get('question_quality')}/5"
                if attempt.get("question_quality")
                else "-",
            )
            if status == "rated":
                st.info("I rated this question without answering it.")
            elif status == "skipped":
                st.info("I skipped this question.")
            elif attempt.get("answer"):
                st.markdown("**My answer**")
                st.write(attempt["answer"])
            else:
                st.info("No answer saved for this question.")
            if attempt.get("question_feedback"):
                st.markdown("**Question feedback**")
                st.write(attempt["question_feedback"])
else:
    st.write("No answers saved yet.")
