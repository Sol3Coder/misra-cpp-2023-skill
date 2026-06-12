# MISRA C++:2023 Agent Skill

English | [中文](README.zh-CN.md)

This repository contains a general-purpose AI agent skill for MISRA C++:2023-oriented C++ review, new-code guidance, and heuristic safety gate checks.

This skill was created by GPT-5.5 with xhigh reasoning effort.

## Why There Is No `agents/openai.yaml`

The skill is intended to be portable across agent runtimes. It keeps the common skill entry point, references, and scripts, but does not include OpenAI/Codex-specific UI metadata such as `agents/openai.yaml`.

The `.agents/skills/misra-cpp-2023/` path is only the local repository layout used while authoring. Consumers can copy the `misra-cpp-2023` folder into the skill directory used by their agent runtime.

## Contents

- `.agents/skills/misra-cpp-2023/SKILL.md` - generic skill entry point.
- `.agents/skills/misra-cpp-2023/references/` - review workflow, coding guidance, tooling notes, and compact rule index.
- `.agents/skills/misra-cpp-2023/scripts/scan_cpp_misra.py` - heuristic C++ safety scanner.
- `.agents/skills/misra-cpp-2023/scripts/extract_rule_index.py` - local rule-index generator.

## Local Source Material

The authoring workspace may contain licensed local materials under `docs/source-material/`, including:

- `MISRA-CPP-2023_2.pdf`
- `misra-cpp-2023.txt`
- `misra-cpp-2023-study-notes.md`

That directory is intentionally ignored by git and is not published in this repository.

## Scanner

```powershell
python .agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py <project-or-file> --format markdown
```

The scanner is a review aid, not a certified MISRA checker.

## Copyright Boundary

This repository intentionally excludes the MISRA PDF, extracted full text, and local study notes. Use the licensed MISRA C++:2023 document locally for full wording, examples, rationale, and exceptions.

## Validation

```powershell
python -m unittest discover -s .agents\skills\misra-cpp-2023\scripts\tests -v
```

If your agent runtime provides a skill validator, run it against `.agents/skills/misra-cpp-2023`.
