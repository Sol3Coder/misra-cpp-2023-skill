#!/usr/bin/env python3
"""Create a compact rule index from extracted MISRA C++:2023 text."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


ENTRY_RE = re.compile(r"^\s*(Rule|Dir)\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)\s+(.+?)\s*$")
CATEGORY_RE = re.compile(r"^\s*Category\s+(Mandatory|Required|Advisory)\s*$")
ANALYSIS_RE = re.compile(r"^\s*Analysis\s+(.+?)\s*$")


@dataclass
class Entry:
    kind: str
    number: str
    category: str = ""
    analysis: str = ""
    line: int = 0

    @property
    def identifier(self) -> str:
        return f"{self.kind} {self.number}"


def normalize_space(value: str) -> str:
    return " ".join(value.strip().split())


def collect_entries(text: str) -> list[Entry]:
    entries: list[Entry] = []
    current: Entry | None = None
    title_continuation = False

    lines = text.splitlines()
    for idx, line in enumerate(lines):
        match = ENTRY_RE.match(line)
        if match:
            kind, number, title = match.groups()
            title = normalize_space(title)
            current = Entry(kind=kind, number=number, line=idx + 1)
            entries.append(current)
            title_continuation = len(title) < 12 or not title.endswith((".", "?", ")"))
            continue

        if current and title_continuation:
            stripped = normalize_space(line)
            if stripped and not stripped.startswith(("Category", "Analysis", "Rationale", "Exception")):
                title_continuation = not stripped.endswith((".", "?", ")"))
                continue
            title_continuation = False

        if current:
            category = CATEGORY_RE.match(line)
            if category and not current.category:
                current.category = category.group(1)
                continue
            analysis = ANALYSIS_RE.match(line)
            if analysis and not current.analysis:
                current.analysis = normalize_space(analysis.group(1))
                continue

    return dedupe(entries)


def dedupe(entries: Sequence[Entry]) -> list[Entry]:
    result: dict[str, Entry] = {}
    for entry in entries:
        existing = result.get(entry.identifier)
        if existing is None:
            result[entry.identifier] = entry
            continue
        if entry.category and not existing.category:
            existing.category = entry.category
        if entry.analysis and not existing.analysis:
            existing.analysis = entry.analysis
    return list(result.values())


def to_markdown(entries: Sequence[Entry], source: Path) -> str:
    lines = [
        "# MISRA C++:2023 Rule Index",
        "",
        "This compact index was generated from the locally extracted PDF text.",
        "It lists identifiers, categories, analysis metadata, and local source line numbers only; consult the licensed standard for full wording, examples, rationale, and exceptions.",
        "",
        f"Source text: `{source}`",
        f"Entries: {len(entries)}",
        "",
        "| Identifier | Category | Analysis | Source line |",
        "|---|---|---|---:|",
    ]
    for entry in entries:
        lines.append(
            f"| {entry.identifier} | {entry.category or '-'} | {entry.analysis or '-'} | {entry.line} |"
        )
    return "\n".join(lines) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    text = args.source.read_text(encoding="utf-8", errors="replace")
    entries = collect_entries(text)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(to_markdown(entries, args.source), encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
