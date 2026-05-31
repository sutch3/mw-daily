from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


QUESTION_PATH = Path(__file__).resolve().parent.parent / "data" / "questions.json"
QUESTION_PARTS_PATH = Path(__file__).resolve().parent.parent / "data" / "question_parts"


def load_questions() -> list[dict[str, Any]]:
    if QUESTION_PARTS_PATH.exists():
        questions: list[dict[str, Any]] = []
        for path in sorted(QUESTION_PARTS_PATH.glob("questions_*.json")):
            with path.open("r", encoding="utf-8") as file:
                questions.extend(json.load(file))
        if questions:
            return questions

    with QUESTION_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def question_for_day(questions: list[dict[str, Any]], day: date | None = None) -> dict[str, Any]:
    active_day = day or date.today()
    index = active_day.toordinal() % len(questions)
    return questions[index]


def find_question(questions: list[dict[str, Any]], question_id: str) -> dict[str, Any]:
    return next(question for question in questions if question["id"] == question_id)
