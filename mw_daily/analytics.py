from __future__ import annotations

from collections import Counter
from typing import Any


def question_lookup(questions: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {question["id"]: question for question in questions}


def category_counts(
    attempts: list[dict[str, Any]], questions: list[dict[str, Any]]
) -> Counter[str]:
    lookup = question_lookup(questions)
    counts: Counter[str] = Counter()
    for attempt in attempts:
        question = lookup.get(attempt["question_id"])
        if question:
            counts[question["category"]] += 1
    return counts
