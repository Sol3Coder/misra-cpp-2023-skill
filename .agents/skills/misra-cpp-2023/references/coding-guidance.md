# New C++ Coding Guidance

Use this when writing or changing C++ under MISRA C++:2023 expectations.

## Design Before Code

Choose the safest simple design:

- Use C++17 unless the project explicitly requires another standard.
- Prefer value types, RAII, `std::array`, bounded containers, `std::span`-like views when available, and explicit ownership.
- Keep functions short, deterministic, and testable.
- Make invalid states unrepresentable with strong types and narrow interfaces.
- Initialize every object explicitly.
- Use `constexpr`, `enum class`, typed constants, and inline functions instead of macros.
- Prefer compile-time bounds and clear preconditions.
- Keep template behavior reviewable after instantiation, not only in the primary template.
- Make special member functions explicit when default generation would hide ownership, lifetime, or copying behavior.
- Keep generated code behind a documented generation profile and review the model/configuration as part of the code.

## Avoid By Default

Avoid these unless the project safety profile explicitly permits them and a deviation is recorded:

- Dynamic allocation in application logic.
- Raw owning pointers.
- C-style casts, `reinterpret_cast`, `const_cast`.
- Unsafe C string/memory/library functions.
- Recursion.
- Function-like macros.
- Inline assembly.
- `goto`, `setjmp`, `longjmp`.
- Global mutable state.
- Unreviewed `volatile`.
- Exceptions or RTTI when the project profile bans them.
- Macro-controlled behavior that is not visible to analysis tools.
- Reliance on compiler-specific, implementation-defined, unspecified, or conditionally supported behavior without documentation.

## Safer Patterns

- Replace owning raw pointers with automatic storage, references, or smart pointers only when dynamic ownership is allowed.
- Replace `#define` constants with `constexpr` or `enum class`.
- Replace function-like macros with `constexpr` functions or templates.
- Replace C arrays with `std::array` where size is fixed and known.
- Replace sentinel integer states with scoped enums.
- Replace unchecked narrowing with explicit range checks.
- Replace cross-module globals with injected dependencies or immutable configuration.
- Replace implicit copy/move behavior with deleted, defaulted, or implemented special member functions that state ownership intent.
- Replace build-variant surprises with documented configuration headers and analysis commands that expose all active macros.

## Completion Gate

Before finalizing C++ code:

1. Compile or at least perform a syntax-aware review if no build is available.
2. Run relevant tests.
3. Run the bundled heuristic scanner on changed files or project root.
4. Confirm templates, generated code, and macro-selected code paths were included in the review scope or listed as gaps.
5. Explain remaining warnings, deviations, and manual-review items.
6. Confirm no blocker or major scanner findings remain unless the user asked for report-only work.
