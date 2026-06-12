# MISRA C++:2023 Agent Skill

English | [中文](README.zh-CN.md)

This repository contains a general-purpose AI agent skill for MISRA C++:2023-oriented C++ review, new-code guidance, and heuristic safety gate checks.

This skill was created by GPT-5.5 with xhigh reasoning effort.

## Contents

- `.agents/skills/misra-cpp-2023/SKILL.md` - generic skill entry point.
- `.agents/skills/misra-cpp-2023/references/` - review workflow, coding guidance, tooling notes, and compact rule index.
- `.agents/skills/misra-cpp-2023/scripts/scan_cpp_misra.py` - heuristic C++ safety scanner.
- `.agents/skills/misra-cpp-2023/scripts/extract_rule_index.py` - local rule-index generator.
- `docs/misra-cpp-2023-study-notes.md` - public study notes and operating model, without standard text reproduction.

## Local Source Material

This repository does not include the MISRA C++:2023 PDF or the converted full-text extraction. To regenerate the local rule index or consult full wording, place your licensed local materials under `docs/source-material/`:

- `MISRA-CPP-2023_2.pdf`
- `misra-cpp-2023.txt`

That directory is intentionally ignored by git and is not published. The public study notes live at `docs/misra-cpp-2023-study-notes.md`.

## Scanner

```powershell
python .agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py <project-or-file> --format markdown
```

The scanner is a review aid, not a certified MISRA checker.

## Copyright Boundary

This repository intentionally excludes the MISRA PDF and extracted full text. Use the licensed MISRA C++:2023 document locally for full wording, examples, rationale, and exceptions.

## Validation

```powershell
python -m unittest discover -s .agents\skills\misra-cpp-2023\scripts\tests -v
```

If your agent runtime provides a skill validator, run it against `.agents/skills/misra-cpp-2023`.
