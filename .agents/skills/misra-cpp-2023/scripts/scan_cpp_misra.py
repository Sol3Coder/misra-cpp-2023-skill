#!/usr/bin/env python3
"""Heuristic MISRA C++:2023 safety scanner.

This is a review aid, not a certified MISRA checker.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


CPP_EXTENSIONS = {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"}
SEVERITY_ORDER = {
    "blocker": 4,
    "major": 3,
    "minor": 2,
    "manual-review": 1,
    "none": 0,
}


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    category: str
    pattern: re.Pattern[str]
    message: str
    remediation: str


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    category: str
    file: str
    line: int
    message: str
    evidence: str
    remediation: str


RULES: Sequence[Rule] = (
    Rule(
        "MISRA-HEUR-DYNALLOC",
        "major",
        "resource-lifetime",
        re.compile(r"\b(new|delete)\b|std::make_unique\s*<|std::make_shared\s*<"),
        "Dynamic allocation or release requires project-level justification in critical C++.",
        "Prefer static storage, bounded containers, object pools, or documented ownership policy.",
    ),
    Rule(
        "MISRA-HEUR-UNSAFE-C",
        "major",
        "library-safety",
        re.compile(r"\b(strcpy|strcat|sprintf|gets|scanf|sscanf|memcpy|memmove|memset)\s*\("),
        "Potentially unsafe C library call or raw memory operation.",
        "Use bounded, typed abstractions and prove buffer sizes and object lifetimes.",
    ),
    Rule(
        "MISRA-HEUR-CSTYLE-CAST",
        "major",
        "type-safety",
        re.compile(
            r"(?<!\w)\(\s*(?:const\s+|volatile\s+|signed\s+|unsigned\s+)?"
            r"(?:bool|char|short|int|long|float|double|std::[a-zA-Z_]\w*|[A-Z]\w*(?:::\w+)*)"
            r"(?:\s*[*&])?\s*\)\s*[\w(*]"
        ),
        "C-style cast hides the exact conversion being performed.",
        "Use a named C++ cast only when justified, and avoid narrowing or representation casts.",
    ),
    Rule(
        "MISRA-HEUR-REINTERPRET-CAST",
        "blocker",
        "type-safety",
        re.compile(r"\breinterpret_cast\s*<"),
        "Representation-changing cast needs strict justification.",
        "Avoid reinterpret_cast; isolate hardware or serialization boundaries and document deviation.",
    ),
    Rule(
        "MISRA-HEUR-CONST-CAST",
        "major",
        "type-safety",
        re.compile(r"\bconst_cast\s*<"),
        "const_cast can violate const-correctness and object invariants.",
        "Preserve const-correctness through interfaces; document any unavoidable legacy boundary.",
    ),
    Rule(
        "MISRA-HEUR-GOTO",
        "blocker",
        "control-flow",
        re.compile(r"\bgoto\b|\b(longjmp|setjmp)\s*\("),
        "Unstructured non-local control flow is unsafe for review and resource lifetime reasoning.",
        "Use structured control flow, RAII, and explicit error propagation.",
    ),
    Rule(
        "MISRA-HEUR-EXCEPTION",
        "manual-review",
        "error-handling",
        re.compile(r"\b(throw|try|catch)\b"),
        "Exception usage needs review against the project's error-handling profile.",
        "Confirm exceptions are allowed; otherwise use explicit status/result types.",
    ),
    Rule(
        "MISRA-HEUR-MACRO-PARAM",
        "major",
        "preprocessor",
        re.compile(r"^\s*#\s*define\s+\w+\s*\([^)]*\)"),
        "Function-like macro can bypass type checking and evaluate arguments unexpectedly.",
        "Prefer constexpr functions, templates, enum classes, or typed inline functions.",
    ),
    Rule(
        "MISRA-HEUR-UNION",
        "major",
        "object-model",
        re.compile(r"\bunion\s+\w*"),
        "Union usage requires object lifetime and active member analysis.",
        "Prefer std::variant or a documented low-level representation boundary.",
    ),
    Rule(
        "MISRA-HEUR-GLOBAL-MUTABLE",
        "manual-review",
        "state",
        re.compile(r"^\s*(?!constexpr\b|const\b)(?:static\s+)?(?:std::)?[A-Za-z_]\w*(?:::\w+)?(?:\s*[*&])?\s+\w+\s*(?:=|\{)"),
        "Possible namespace-scope mutable object; confirm initialization and concurrency safety.",
        "Prefer local state, const objects, dependency injection, and explicit synchronization.",
    ),
    Rule(
        "MISRA-HEUR-VARIADIC",
        "major",
        "type-safety",
        re.compile(r"\.\.\."),
        "Variadic functions and packs require careful type and bounds review.",
        "Avoid C-style variadics; constrain template packs and document all call patterns.",
    ),
    Rule(
        "MISRA-HEUR-VOLATILE",
        "manual-review",
        "hardware-concurrency",
        re.compile(r"\bvolatile\b"),
        "volatile usage must be limited to justified hardware or signal boundaries.",
        "Use atomics for concurrency; isolate hardware registers behind reviewed interfaces.",
    ),
    Rule(
        "MISRA-HEUR-ASM",
        "blocker",
        "portability",
        re.compile(r"\b(asm|__asm__|__asm)\b"),
        "Inline assembly is non-portable and needs explicit deviation approval.",
        "Move assembly behind a narrow platform abstraction with documented verification.",
    ),
)


def discover_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix.lower() in CPP_EXTENSIONS else []
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in CPP_EXTENSIONS
        and not any(part in {".git", "build", "cmake-build-debug", "cmake-build-release"} for part in path.parts)
    )


def strip_line_comment(line: str) -> str:
    in_string = False
    escaped = False
    for idx, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if not in_string and line[idx : idx + 2] == "//":
            return line[:idx]
    return line


def scan_file(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        rel = str(path)
        return [
            Finding(
                "MISRA-HEUR-READ-ERROR",
                "manual-review",
                "tooling",
                rel,
                0,
                f"Could not read file: {exc}",
                "",
                "Check file permissions and encoding.",
            )
        ]

    rel_path = str(path.relative_to(root) if path.is_relative_to(root) else path)
    function_names = collect_function_names(lines)

    for line_no, line in enumerate(lines, start=1):
        code = strip_line_comment(line).strip()
        if not code:
            continue
        for rule in RULES:
            if rule.pattern.search(code):
                if rule.rule_id == "MISRA-HEUR-GLOBAL-MUTABLE" and not looks_like_global(line, lines, line_no):
                    continue
                findings.append(
                    Finding(
                        rule.rule_id,
                        rule.severity,
                        rule.category,
                        rel_path,
                        line_no,
                        rule.message,
                        code,
                        rule.remediation,
                    )
                )
        for function_name in function_names.get(line_no, ()):
            if has_recursive_call(function_name, code):
                findings.append(
                    Finding(
                        "MISRA-HEUR-RECURSION",
                        "major",
                        "control-flow",
                        rel_path,
                        line_no,
                        "Possible direct recursion; recursion needs project-level justification.",
                        code,
                        "Replace with bounded iteration or prove recursion depth and stack usage.",
                    )
                )
    return findings


def collect_function_names(lines: Sequence[str]) -> dict[int, list[str]]:
    active_functions: dict[int, list[str]] = {}
    current: list[tuple[str, int]] = []
    function_decl = re.compile(r"\b([A-Za-z_]\w*)\s*\([^;{}]*\)\s*(?:const\s*)?(?:noexcept\s*)?(?:->\s*[\w:<>*&\s]+)?\s*\{")
    depth = 0

    for line_no, line in enumerate(lines, start=1):
        code = strip_line_comment(line)
        match = function_decl.search(code)
        if match and not re.search(r"\b(if|for|while|switch|catch)\s*\(", code):
            current.append((match.group(1), depth))
        if current:
            active_functions[line_no] = [name for name, _ in current]
        depth += code.count("{") - code.count("}")
        while current and depth <= current[-1][1]:
            current.pop()
    return active_functions


def has_recursive_call(function_name: str, code: str) -> bool:
    return re.search(rf"\b{re.escape(function_name)}\s*\(", code) is not None and not re.search(
        rf"\b{re.escape(function_name)}\s*\([^;{{}}]*\)\s*(?:const\s*)?(?:noexcept\s*)?\s*\{{", code
    )


def looks_like_global(line: str, lines: Sequence[str], line_no: int) -> bool:
    if line.startswith((" ", "\t")):
        return False
    before = "\n".join(lines[: max(0, line_no - 1)])
    return before.count("{") == before.count("}")


def build_report(root: Path) -> dict[str, object]:
    files = discover_files(root)
    findings: list[Finding] = []
    for path in files:
        findings.extend(scan_file(path, root if root.is_dir() else root.parent))

    counts: dict[str, int] = {severity: 0 for severity in SEVERITY_ORDER if severity != "none"}
    for finding in findings:
        counts[finding.severity] += 1

    return {
        "tool": "scan_cpp_misra.py",
        "note": "Heuristic review aid only; not a certified MISRA compliance result.",
        "root": str(root),
        "summary": {
            "files_scanned": len(files),
            "findings": len(findings),
            "by_severity": counts,
        },
        "findings": [asdict(finding) for finding in findings],
    }


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def to_markdown(report: dict[str, object]) -> str:
    summary = report["summary"]
    findings = report["findings"]
    lines = [
        "# MISRA C++:2023 Heuristic Scan",
        "",
        str(report["note"]),
        "",
        f"- Root: `{report['root']}`",
        f"- Files scanned: {summary['files_scanned']}",
        f"- Findings: {summary['findings']}",
        "",
        "| Severity | Rule | File | Line | Message |",
        "|---|---|---|---:|---|",
    ]
    if not findings:
        lines.append("| none | none | - | - | No heuristic findings. |")
    else:
        for finding in findings:
            lines.append(
                "| {severity} | {rule_id} | `{file}` | {line} | {message} |".format(
                    severity=markdown_escape(finding["severity"]),
                    rule_id=markdown_escape(finding["rule_id"]),
                    file=markdown_escape(finding["file"]),
                    line=markdown_escape(finding["line"]),
                    message=markdown_escape(finding["message"]),
                )
            )
    return "\n".join(lines) + "\n"


def should_fail(report: dict[str, object], fail_on: str) -> bool:
    threshold = SEVERITY_ORDER[fail_on]
    if threshold == 0:
        return False
    return any(SEVERITY_ORDER[finding["severity"]] >= threshold for finding in report["findings"])


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="C++ source file or project directory to scan")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument(
        "--fail-on",
        choices=("blocker", "major", "minor", "manual-review", "none"),
        default="major",
        help="Return exit code 1 when a finding at or above this severity exists.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = args.path.resolve()
    report = build_report(root)
    if args.format == "markdown":
        sys.stdout.write(to_markdown(report))
    else:
        json.dump(report, sys.stdout, indent=2)
        sys.stdout.write("\n")
    return 1 if should_fail(report, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
