# 考研数学复习系统

这是一个面向考研数学复习的小型资料库，当前聚焦于高等数学中的积分专题。仓库包含专题笔记、题库数据、自动组卷脚本和格式测试，方便持续扩展到极限、导数、级数、线性代数、概率统计等内容。

## 目录结构

- `topics/integrals.md`：积分专题复习笔记
- `problems/integrals.json`：积分专题题库
- `scripts/generate_quiz.py`：根据题库生成中文练习卷
- `tests/test_problem_format.py`：题库格式测试
- `quiz.md`：自动生成的中文练习卷

## 使用方法

安装并使用 `pytest` 后，可以运行：

```bash
pytest
```

生成练习卷：

```bash
python scripts/generate_quiz.py
```

默认会读取 `problems/integrals.json`，并生成 `quiz.md`。

## 复习建议

1. 先阅读 `topics/integrals.md`，梳理核心概念和常见方法。
2. 再完成 `quiz.md` 中的题目，不要急着看答案。
3. 对照题库中的解析，整理错题原因。
4. 每周补充新题，并运行测试确保题库格式稳定。

