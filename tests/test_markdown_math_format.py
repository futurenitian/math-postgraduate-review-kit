from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_PATHS = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "quiz.md",
    *sorted((ROOT / "topics").glob("*.md")),
]
STRUCTURED_TEXT_PATHS = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "quiz.md",
    ROOT / "scripts" / "generate_quiz.py",
    ROOT / "tests" / "test_problem_format.py",
    ROOT / "problems" / "integrals.json",
    *sorted((ROOT / "topics").glob("*.md")),
]


def iter_lines() -> list[tuple[Path, int, str]]:
    lines = []
    for path in MARKDOWN_PATHS:
        if not path.exists():
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            lines.append((path, line_number, line))
    return lines


def test_display_math_delimiters_are_on_their_own_lines() -> None:
    for path, line_number, line in iter_lines():
        if "$$" not in line:
            continue

        assert line.strip() == "$$", (
            f"{path}:{line_number} 的行间公式分隔符必须单独占一行"
        )


def test_display_math_is_not_started_inside_list_items() -> None:
    for path, line_number, line in iter_lines():
        stripped = line.lstrip()
        starts_like_list_item = stripped.startswith(("- ", "* ")) or (
            len(stripped) > 2 and stripped[0].isdigit() and stripped[1:3] == ". "
        )

        assert not (starts_like_list_item and "$$" in stripped), (
            f"{path}:{line_number} 不要在列表项同一行写行间公式"
        )


def test_no_text_code_block_for_math() -> None:
    for path, line_number, line in iter_lines():
        assert line.strip() != "```text", (
            f"{path}:{line_number} 不要使用 text 代码块展示数学公式"
        )


def test_no_thin_space_before_differential() -> None:
    forbidden_patterns = (r"\,dx", r"\,dt", r"\,du", r"\,dy", r"\,dv")

    for path, line_number, line in iter_lines():
        assert not any(pattern in line for pattern in forbidden_patterns), (
            f"{path}:{line_number} 积分微分请使用 \\mathrm{{d}}x 等写法"
        )


def test_key_files_keep_real_line_breaks() -> None:
    minimum_line_counts = {
        ROOT / "topics" / "integrals.md": 50,
        ROOT / "quiz.md": 20,
        ROOT / "scripts" / "generate_quiz.py": 30,
    }

    for path, minimum in minimum_line_counts.items():
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        assert line_count > minimum, f"{path} 需要保留真实多行结构"


def test_structured_files_do_not_have_very_long_lines() -> None:
    for path in STRUCTURED_TEXT_PATHS:
        if not path.exists():
            continue

        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            assert len(line) <= 180, f"{path}:{line_number} 行过长，疑似缺少真实换行"
