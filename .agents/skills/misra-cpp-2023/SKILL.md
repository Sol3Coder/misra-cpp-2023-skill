---
name: misra-cpp-2023
description: Use when reviewing, writing, or modifying C++ for MISRA C++:2023, safety-critical, embedded, automotive, secure coding, compliance, static analysis, undefined behavior, portability, or code-safety enforcement.
---

# MISRA C++:2023

## Core Rule

Treat MISRA C++:2023 as a mandatory safety gate for C++ work. Before claiming a C++ change is complete, check the code against this skill, run available tooling, run the bundled scanner, and report any residual manual-review or deviation items.

Do not claim full MISRA compliance from this skill alone. A compliance claim requires the licensed standard, project deviation records, qualified/static-analysis tooling, compiler configuration, and system-level review.

## Workflow

1. Identify scope: files changed or project root, C++ standard, compiler, build system, target platform, and whether exceptions/RTTI/dynamic allocation are allowed.
2. Load the relevant reference:
   - Existing project review: `references/review-workflow.md`
   - New or modified C++ code: `references/coding-guidance.md`
   - Tool setup and commands: `references/tooling.md`
   - Rule lookup: `references/rule-index.md`
3. Run available project checks first: build, tests, compiler warnings, `clang-tidy`, `cppcheck`, or existing MISRA tools.
4. Run the bundled scanner:

```powershell
python .agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py <project-or-file> --format markdown
```

5. Fix blocker and major findings before completion unless the user explicitly asks for a report only.
6. Record remaining findings as deviations or manual-review items with file, line, rationale, and proposed mitigation.

## Enforcement

- For generated or edited C++ code, prefer C++17, deterministic control flow, RAII, fixed ownership, bounded resources, explicit initialization, and narrow interfaces.
- Avoid dynamic allocation, raw owning pointers, C-style casts, `reinterpret_cast`, `const_cast`, unsafe C library calls, recursion, global mutable state, function-like macros, inline assembly, `goto`, `setjmp`/`longjmp`, and unreviewed `volatile`.
- If a project profile allows an otherwise risky feature, document that profile before using it.
- If tooling and heuristics disagree, treat the stricter result as the next review item until resolved.
- If the requested implementation conflicts with a safety rule, explain the conflict and propose a compliant design.

## Reporting

Return findings ordered by severity:

- `blocker`: must fix or explicitly deviate before release.
- `major`: should fix before completion; needs written rationale if retained.
- `minor`: improve when touching nearby code.
- `manual-review`: needs human or project-tool confirmation.

For each finding include: file, line, risk, relevant rule identifier when known, recommended fix, and whether it was verified by tooling or heuristic scan.

## Copyright Boundary

The local PDF text may be used for navigation and lookup by licensed users. Do not reproduce large verbatim sections of the MISRA standard in responses or skill files. Use `references/rule-index.md` to locate rule identifiers and consult the licensed source document for full wording, examples, rationale, and exceptions.
