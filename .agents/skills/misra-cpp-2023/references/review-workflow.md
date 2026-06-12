# Existing Project Review Workflow

Use this workflow when asked to review a C++ repository, module, pull request, or file set for MISRA C++:2023 or safety risks.

## Intake

1. Identify the review target and list C++ source/header files.
2. Identify build system: CMake, Make, Bazel, Visual Studio, vendor IDE, or custom scripts.
3. Identify configured C++ standard and target compiler.
4. Check whether the project has a safety profile covering exceptions, RTTI, dynamic allocation, recursion, concurrency, interrupts, volatile, hardware access, and deviations.
5. Check whether static-analysis outputs already exist. Prefer project-approved MISRA tools over heuristics.

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
- Deviations: every retained violation needs rationale, risk analysis, mitigation, and approval owner.

## Output

Report in this order:

1. Blockers.
2. Major findings.
3. Minor findings.
4. Manual-review/deviation items.
5. Commands run and results.
6. Residual risk and tooling gaps.

Never state that the project is MISRA compliant unless there is evidence from the licensed standard, approved toolchain, complete configuration, and deviation process.
