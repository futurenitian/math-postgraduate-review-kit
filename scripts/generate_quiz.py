from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROBLEM_FILE = ROOT / "problems" / "integrals.json"
OUTPUT_FILE = ROOT / "quiz.md"
INLINE_MATH_RE = re.compile(r"\$([^$]+)\$")


def load_problems() -> list[dict[str, Any]]:
    with PROBLEM_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def should_use_display_math(formula: str) -> bool:
    return r"\int" in formula or len(formula) > 24


def render_question(question: str) -> list[str]:
    match = INLINE_MATH_RE.search(question)
    if not match or not should_use_display_math(match.group(1)):
        return [f"**题目：** {question}"]

    prefix = question[: match.start()].strip()
    formula = match.group(1).strip()
    suffix = question[match.end() :].strip()

    if suffix == "。":
        suffix = ""

    lines = [f"**题目：** {prefix}", "", "$$", formula, "$$"]
    if suffix:
        lines.extend(["", suffix])

    return lines


def render_quiz(problems: list[dict[str, Any]]) -> str:
    lines = [
        "# 考研数学积分专题练习",
        "",
        "请独立完成以下题目，再对照题库中的答案与解析进行订正。",
        "",
    ]

    for index, problem in enumerate(problems, start=1):
        tags = "、".join(problem["tags"])
        lines.extend(
            [
                f"## 第 {index} 题（{problem['difficulty']}）",
                "",
                f"**题号：** {problem['id']}",
                "",
                f"**标签：** {tags}",
                "",
            ]
        )
        lines.extend(render_question(str(problem["question"])))
        lines.extend(["", "**作答区：**", "", "> ", ""])

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    problems = load_problems()
    with OUTPUT_FILE.open("w", encoding="utf-8", newline="\n") as file:
        file.write(render_quiz(problems))
    print(f"已生成 {OUTPUT_FILE.name}，共 {len(problems)} 道题。")


if __name__ == "__main__":
    main()
