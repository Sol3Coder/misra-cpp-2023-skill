# Tooling

The bundled tools are review aids. They do not replace a qualified MISRA checker.

## Heuristic Scanner

JSON output:

```powershell
python F:\skills\misra\.agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py F:\path\to\project
```

Markdown output:

```powershell
python F:\skills\misra\.agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py F:\path\to\project --format markdown
```

Do not fail the command on findings:

```powershell
python F:\skills\misra\.agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py F:\path\to\project --fail-on none
```

Default behavior returns exit code `1` for major or blocker findings.

## Rule Index

Generate a compact identifier index from extracted text:

```powershell
python F:\skills\misra\.agents\skills\misra-cpp-2023\scripts\extract_rule_index.py F:\skills\misra\work\misra-cpp-2023.txt F:\skills\misra\.agents\skills\misra-cpp-2023\references\rule-index.md
```

The index intentionally omits full rule wording. Use the licensed source document for details.

## Optional External Tools

Use project-approved tools when present:

- `clang-tidy`
- `cppcheck`
- Compiler warnings for the target compiler.
- Commercial MISRA C++ analyzers.
- Existing CI reports.

When a tool requires a compilation database, look for `compile_commands.json` or ask how the project is built.
