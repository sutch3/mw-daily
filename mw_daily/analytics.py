from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean
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


def weak_areas(
    attempts: list[dict[str, Any]], questions: list[dict[str, Any]]
) -> list[tuple[str, float, int]]:
    lookup = question_lookup(questions)
    scores_by_category: dict[str, list[int]] = defaultdict(list)
    for attempt in attempts:
        score = attempt.get("self_score")
        question = lookup.get(attempt["question_id"])
        if question and score:
            scores_by_category[question["category"]].append(int(score))

    rows = [
        (category, mean(scores), len(scores))
        for category, scores in scores_by_category.items()
    ]
    return sorted(rows, key=lambda row: (row[1], -row[2]))
