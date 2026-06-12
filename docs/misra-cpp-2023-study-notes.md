# MISRA C++:2023 Study Notes For Skill Use

These notes summarize how this skill should use locally licensed MISRA C++:2023 material. They are a navigation and operating model, not a reproduction of the standard.

## Extracted Structure Observed Locally

- PDF pages reported by Poppler: 254.
- Extracted text bytes: 713766.
- Compact index entries generated: 179.
- Entry types: 175 rules, 4 directives.
- Categories: 5 mandatory, 124 required, 50 advisory.
- Analysis scope: 149 decidable single-translation-unit entries, 6 decidable system entries, 1 undecidable single-translation-unit entry, 19 undecidable system entries, 4 directives without rule-style analysis metadata.

## Operating Model

MISRA C++:2023 review needs three layers:

1. Local coding discipline: avoid high-risk C++ constructs before they enter the codebase.
2. Tool-assisted review: build, tests, compiler diagnostics, static analysis, and the bundled heuristic scanner.
3. Compliance evidence: project profile, deviation records, qualified tool configuration, and human review for undecidable or system-wide rules.

## Skill Implications

- The skill must be strict during code generation and modification because prevention is cheaper than later deviation cleanup.
- The scanner is intentionally conservative and should produce review leads, not legal or certification claims.
- System-level and undecidable entries require build context, whole-program analysis, project policy, or human review.
- The rule index should be used to locate relevant identifiers and source lines in locally licensed source material. Full wording, rationale, examples, and exceptions remain in the licensed source document.

## Minimum Review Record

For each reviewed project or change, record:

- Scope reviewed.
- Build/test/static-analysis commands run.
- Scanner command and result.
- Blocker/major/minor/manual-review findings.
- Deviations accepted by the user or project authority.
- Residual tooling gaps.
