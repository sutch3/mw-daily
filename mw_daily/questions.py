from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


QUESTION_PATH = Path(__file__).resolve().parent.parent / "data" / "questions.json"


def load_questions() -> list[dict[str, Any]]:
    with QUESTION_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def question_for_day(questions: list[dict[str, Any]], day: date | None = None) -> dict[str, Any]:
    active_day = day or date.today()
    index = active_day.toordinal() % len(questions)
    return questions[index]


def find_question(questions: list[dict[str, Any]], question_id: str) -> dict[str, Any]:
    return next(question for question in questions if question["id"] == question_id)
