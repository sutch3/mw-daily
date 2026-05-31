from __future__ import annotations

import streamlit as st

from mw_daily.analytics import category_counts, question_lookup, weak_areas
from mw_daily.questions import load_questions
from mw_daily.storage import load_attempts


st.set_page_config(page_title="MW Daily Progress", page_icon="MW", layout="wide")

st.title("Progress")
st.caption("Coverage, volume, and weak areas based on Sara's saved self-scores.")

questions = load_questions()
attempts = load_attempts()
lookup = question_lookup(questions)

answered_count = len(attempts)
scored_attempts = [attempt for attempt in attempts if attempt.get("self_score")]
average_score = (
    sum(int(attempt["self_score"]) for attempt in scored_attempts) / len(scored_attempts)
    if scored_attempts
    else 0
)

metric_columns = st.columns(3)
metric_columns[0].metric("Questions answered", answered_count)
metric_columns[1].metric("Question bank", len(questions))
metric_columns[2].metric("Average self-score", f"{average_score:.1f}" if scored_attempts else "-")

st.divider()

coverage_col, weakness_col = st.columns(2)

with coverage_col:
    st.subheader("Category coverage")
    counts = category_counts(attempts, questions)
    categories = sorted({question["category"] for question in questions})
    if attempts:
        st.bar_chart({category: counts.get(category, 0) for category in categories})
    else:
        st.info("No saved answers yet.")

with weakness_col:
    st.subheader("Weak areas")
    weak_rows = weak_areas(attempts, questions)
    if weak_rows:
        for category, score, count in weak_rows[:5]:
            st.write(f"**{category}**: {score:.1f}/5 across {count} answer{'s' if count != 1 else ''}")
    else:
        st.info("Weak areas will appear after Sara saves self-scored answers.")

st.divider()
st.subheader("Recent answers")

if attempts:
    for attempt in reversed(attempts[-10:]):
        question = lookup.get(attempt["question_id"], {})
        with st.expander(f"{attempt['study_date']} · {question.get('category', 'Unknown')} · Score {attempt.get('self_score', '—')}/5"):
            st.write(question.get("prompt", "Question unavailable."))
            st.markdown("**Sara's answer**")
            st.write(attempt["answer"])
else:
    st.write("No answers saved yet.")
