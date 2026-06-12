# MISRA C++:2023 Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local `misra-cpp-2023` Codex skill with PDF-derived reference indexes and a runnable C++ safety review scanner.

**Architecture:** Keep `SKILL.md` concise and put detailed guidance in reference files. Use a deterministic Python scanner for minimum gate checks, with tests proving JSON and Markdown reporting behavior.

**Tech Stack:** Poppler `pdftotext.exe`, PowerShell, Python standard library, Codex skill format.

---

### Task 1: Extract Source Text

**Files:**
- Create: `F:\skills\misra\work\misra-cpp-2023.txt`
- Create: `F:\skills\misra\work\extraction-status.md`

- [ ] Run Poppler extraction:

```powershell
.\poppler-26.02.0\Library\bin\pdftotext.exe -layout -enc UTF-8 .\MISRA-CPP-2023_2.pdf .\work\misra-cpp-2023.txt
```

- [ ] If extraction succeeds, record file size and page count in `work\extraction-status.md`.
- [ ] If extraction fails due to permissions, record the failure and do not bypass restrictions.

### Task 2: Create Skill Skeleton

**Files:**
- Create: `F:\skills\misra\.agents\skills\misra-cpp-2023\SKILL.md`
- Create: `F:\skills\misra\.agents\skills\misra-cpp-2023\references\*.md`
- Create: `F:\skills\misra\.agents\skills\misra-cpp-2023\scripts\*.py`
- Create: `F:\skills\misra\.agents\skills\misra-cpp-2023\agents\openai.yaml`

- [ ] Create directories.
- [ ] Write frontmatter with name `misra-cpp-2023`.
- [ ] Include trigger wording for MISRA C++:2023, C++, safety-critical, embedded, automotive, review, compliance, and secure coding.

### Task 3: Build Scanner Test First

**Files:**
- Create: `F:\skills\misra\.agents\skills\misra-cpp-2023\scripts\tests\test_scan_cpp.py`
- Create: `F:\skills\misra\.agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py`

- [ ] Write tests that create temporary C++ files containing C-style casts, dynamic allocation, unsafe C functions, and clean code.
- [ ] Run tests and confirm they fail because `scan_cpp_misra.py` is not implemented.

### Task 4: Implement Scanner

**Files:**
- Modify: `F:\skills\misra\.agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py`

- [ ] Implement recursive file discovery for `.c`, `.cc`, `.cpp`, `.cxx`, `.h`, `.hh`, `.hpp`, `.hxx`.
- [ ] Implement line-based heuristic rules with severity, category, rationale, and remediation.
- [ ] Emit JSON by default and Markdown with `--format markdown`.
- [ ] Support `--fail-on blocker|major|minor|manual-review|none`.

### Task 5: Create References

**Files:**
- Create: `F:\skills\misra\.agents\skills\misra-cpp-2023\references\review-workflow.md`
- Create: `F:\skills\misra\.agents\skills\misra-cpp-2023\references\coding-guidance.md`
- Create: `F:\skills\misra\.agents\skills\misra-cpp-2023\references\rule-index.md`
- Create: `F:\skills\misra\.agents\skills\misra-cpp-2023\references\tooling.md`

- [ ] Write review workflow for existing projects.
- [ ] Write coding guidance for new or modified C++ code.
- [ ] Generate a rule identifier index from extracted text when available.
- [ ] Keep all standard content paraphrased or indexed, not reproduced.

### Task 6: Validate

**Files:**
- Validate: `F:\skills\misra\.agents\skills\misra-cpp-2023`

- [ ] Run scanner tests.
- [ ] Run scanner on a sample project.
- [ ] Run skill quick validation.
- [ ] Document any limitations in the final response.
