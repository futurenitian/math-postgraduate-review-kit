from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBLEM_FILE = ROOT / "problems" / "integrals.json"
OUTPUT_FILE = ROOT / "quiz.md"


def load_problems() -> list[dict[str, object]]:
    with PROBLEM_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def render_quiz(problems: list[dict[str, object]]) -> str:
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
                f"**题目：** {problem['question']}",
                "",
                "**作答区：**",
                "",
                "> ",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    problems = load_problems()
    OUTPUT_FILE.write_text(render_quiz(problems), encoding="utf-8")
    print(f"已生成 {OUTPUT_FILE.name}，共 {len(problems)} 道题。")


if __name__ == "__main__":
    main()

