from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBLEM_FILE = ROOT / "problems" / "integrals.json"
REQUIRED_FIELDS = {
    "id",
    "topic",
    "difficulty",
    "question",
    "answer",
    "solution",
    "tags",
}
ALLOWED_DIFFICULTIES = {"基础", "中等", "提高"}


def load_problems() -> list[dict[str, object]]:
    with PROBLEM_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_integral_problem_file_exists() -> None:
    assert PROBLEM_FILE.exists()


def test_integral_problems_have_required_fields() -> None:
    problems = load_problems()
    assert problems, "题库不能为空"

    for problem in problems:
        assert REQUIRED_FIELDS <= problem.keys()


def test_integral_problem_ids_are_unique() -> None:
    problems = load_problems()
    ids = [problem["id"] for problem in problems]

    assert len(ids) == len(set(ids))


def test_integral_problem_values_are_valid() -> None:
    problems = load_problems()

    for problem in problems:
        assert isinstance(problem["id"], str) and problem["id"].startswith("INT-")
        assert problem["topic"] == "积分"
        assert problem["difficulty"] in ALLOWED_DIFFICULTIES
        assert isinstance(problem["question"], str) and problem["question"].strip()
        assert isinstance(problem["answer"], str) and problem["answer"].strip()
        assert isinstance(problem["solution"], str) and problem["solution"].strip()
        assert isinstance(problem["tags"], list) and problem["tags"]
        assert all(isinstance(tag, str) and tag.strip() for tag in problem["tags"])


def test_integral_problem_formulas_use_latex_delimiters() -> None:
    problems = load_problems()

    for problem in problems:
        combined_text = " ".join(
            str(problem[field]) for field in ("question", "answer", "solution")
        )
        assert "$" in combined_text
        assert "∫" not in combined_text

