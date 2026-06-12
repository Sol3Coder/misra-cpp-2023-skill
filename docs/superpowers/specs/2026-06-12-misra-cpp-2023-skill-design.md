# MISRA C++:2023 Skill Design

## Goal

Create a local Codex skill named `misra-cpp-2023` that guides C++ code generation, modification, and review against MISRA C++:2023 and safety-oriented C++ practices.

## Source Handling

Use the local PDF at `F:\skills\misra\MISRA-CPP-2023_2.pdf` and the local Poppler tools under `F:\skills\misra\poppler-26.02.0`.

The PDF is marked encrypted with copying disabled. The workflow must try normal Poppler extraction only. If extraction is blocked, it must not bypass PDF permissions. The skill must not embed large verbatim sections of the standard. It may use local derivative indexes, headings, rule identifiers, and short paraphrased guidance.

## Skill Location

Create the skill at:

`F:\skills\misra\.agents\skills\misra-cpp-2023`

The skill should include:

- `SKILL.md`: short trigger and workflow guidance.
- `references/`: searchable reference notes and rule index derived from authorized local extraction.
- `scripts/`: deterministic helper tools for project scanning and report generation.
- `agents/openai.yaml`: UI metadata for Codex skill discovery.

## Behavior

The skill must trigger for:

- Reviewing an existing C++ project for MISRA C++:2023, safety, undefined behavior, maintainability, or embedded/automotive compliance.
- Writing or modifying C++ code where MISRA, safety-critical, automotive, embedded, secure coding, or compliance is relevant.
- Enforcing safety rules before completion when C++ files are changed.

The skill must require the agent to:

- Inspect build system and language standard before judging code.
- Prefer compiler diagnostics, clang-tidy, cppcheck, existing MISRA tooling, and project tests when available.
- Run the bundled heuristic scanner as a minimum gate.
- Classify findings as blocker, major, minor, or manual-review.
- Treat heuristic hits as leads, not proof.
- Refuse to claim MISRA compliance unless a qualified toolchain and deviation process support that claim.

## Scanner Scope

The bundled scanner should be deliberately conservative. It should detect common risk patterns useful during coding and review:

- Dynamic allocation in application code.
- C-style casts and `reinterpret_cast`.
- Unsafe C library calls.
- `goto`, `longjmp`, `setjmp`.
- Exception usage where banned by project profile.
- Macros with parameters and suspicious preprocessor use.
- Recursion signals.
- Global mutable state signals.
- Union usage.
- Raw owning pointer signals.
- `const_cast`, volatile, inline assembly, variadic functions.

The scanner must emit JSON and Markdown so it can be used in automation or read by humans.

## Deliverables

1. Converted text or a clear extraction-failed note.
2. Rule/reference index files.
3. `misra-cpp-2023` skill.
4. Unit tests for the scanner.
5. Validation output for the skill and scripts.

## Non-Goals

- Do not reproduce the MISRA standard.
- Do not build a certified MISRA checker.
- Do not silently bypass encrypted PDF restrictions.
- Do not modify arbitrary C++ projects during review unless explicitly asked.
