# MISRA C++:2023 Codex Skill

Local Codex skill for MISRA C++:2023-oriented C++ review, new-code guidance, and heuristic safety gate checks.

## Contents

- `.agents/skills/misra-cpp-2023/SKILL.md` - skill entry point.
- `.agents/skills/misra-cpp-2023/references/` - review workflow, coding guidance, tooling notes, and compact rule index.
- `.agents/skills/misra-cpp-2023/scripts/scan_cpp_misra.py` - heuristic C++ safety scanner.
- `.agents/skills/misra-cpp-2023/scripts/extract_rule_index.py` - local rule-index generator.
- `docs/superpowers/` - design and implementation notes.
- `work/misra-cpp-2023-study-notes.md` - local study summary.

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
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents\skills\misra-cpp-2023
```
