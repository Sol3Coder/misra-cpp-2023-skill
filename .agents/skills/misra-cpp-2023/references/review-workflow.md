# Existing Project Review Workflow

Use this workflow when asked to review a C++ repository, module, pull request, or file set for MISRA C++:2023 or safety risks.

## Intake

1. Identify the review target and list C++ source/header files.
2. Identify build system: CMake, Make, Bazel, Visual Studio, vendor IDE, or custom scripts.
3. Identify configured C++ standard and target compiler.
4. Identify all macro definitions that affect conditional compilation, including compiler built-ins and command-line definitions.
5. Check whether the project has a safety profile covering exceptions, RTTI, dynamic allocation, recursion, concurrency, interrupts, volatile, hardware access, generated code, and deviations.
6. Check whether static-analysis outputs already exist. Prefer project-approved MISRA tools over heuristics.

## Minimum Gate

Run the most relevant available checks:

```powershell
# Heuristic scan from repository root
python F:\skills\misra\.agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py . --format markdown
```

Also run project-native checks when available:

- Build with warnings as errors when that is already project policy.
- Unit/integration tests.
- `clang-tidy` with project configuration.
- `cppcheck --enable=warning,style,performance,portability`.
- Existing commercial or qualified MISRA checker reports.

## Review Focus

Prioritize:

- Undefined, unspecified, and implementation-defined behavior.
- Lifetime and ownership errors.
- Casts and type conversions.
- Control-flow complexity and recursion.
- Preprocessor use, macros, conditional compilation.
- Global state, initialization order, concurrency, and interrupts.
- Use of C library, raw memory, string, locale, I/O, and environment functions.
- Error handling profile: exceptions, return codes, assertions, fail-safe behavior.
- Header hygiene, ODR, linkage, namespaces, and ABI boundaries.
- Conditional compilation and macro-controlled variants.
- Fully instantiated templates, class/struct semantics, union boundaries, and implicitly generated special member functions.
- Automatically generated code and model/code-generator responsibilities.
- Deviations: every retained violation needs rationale, risk analysis, mitigation, and approval owner.

## Category Handling

- Mandatory: no violations and no deviations are acceptable for a compliance claim.
- Required: violations require formal deviations.
- Advisory: follow where reasonably practical; if not followed, document the justification.
- Disapplied: enforce only when the project has not documented disapplication.

## Analysis Limits

- Decidable single-translation-unit findings are the best fit for automated checking.
- System-scope findings require whole-project or link-set context.
- Undecidable findings may be false positives or missed by tools; record justifications and manual review outcomes.
- Directives cannot be fully validated from source code alone and usually require process evidence.

## Output

Report in this order:

1. Blockers.
2. Major findings.
3. Minor findings.
4. Manual-review/deviation items.
5. Commands run and results.
6. Residual risk and tooling gaps.

Never state that the project is MISRA compliant unless there is evidence from the licensed standard, approved toolchain, complete configuration, and deviation process.
