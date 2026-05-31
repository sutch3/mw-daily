from __future__ import annotations

import streamlit as st

from mw_daily.analytics import category_counts, question_lookup
from mw_daily.questions import load_questions
from mw_daily.storage import load_attempts
from mw_daily.time_format import format_duration


st.set_page_config(page_title="MW Daily Progress", page_icon="MW", layout="wide")

st.title("Progress")
st.caption("Coverage, volume, time taken, and Sara's previous answers.")

questions = load_questions()
attempts = load_attempts()
lookup = question_lookup(questions)

answered_count = len(attempts)
timed_attempts = [attempt for attempt in attempts if attempt.get("time_seconds") is not None]
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

metric_columns = st.columns(4)
metric_columns[0].metric("Questions answered", answered_count)
metric_columns[1].metric("Question bank", len(questions))
metric_columns[2].metric("Average time", format_duration(average_time))
metric_columns[3].metric(
    "Question usefulness",
    f"{average_quality:.1f}/5" if average_quality is not None else "-",
)

st.divider()

st.subheader("Category coverage")
counts = category_counts(attempts, questions)
categories = sorted({question["category"] for question in questions})
if attempts:
    st.bar_chart({category: counts.get(category, 0) for category in categories})
else:
    st.info("No saved answers yet.")

st.divider()
st.subheader("Answer history")

if attempts:
    for attempt in reversed(attempts):
        question = lookup.get(attempt["question_id"], {})
        time_taken = format_duration(attempt.get("time_seconds"))
        title = (
            f"{attempt['study_date']} · {question.get('category', 'Unknown')} · "
            f"{time_taken}"
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
            st.markdown("**Sara's answer**")
            st.write(attempt["answer"])
            if attempt.get("question_feedback"):
                st.markdown("**Question feedback**")
                st.write(attempt["question_feedback"])
else:
    st.write("No answers saved yet.")
