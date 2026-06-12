import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scan_cpp_misra.py"


def run_scan(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class ScanCppMisraTests(unittest.TestCase):
    def test_reports_common_safety_risks_as_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "unsafe.cpp"
            source.write_text(
                """
#include <cstring>

int recurse(int x) {
    return x ? recurse(x - 1) : 0;
}

void f(char *dst, const char *src) {
    int *p = new int(42);
    std::strcpy(dst, src);
    auto raw = (int) *p;
    delete p;
}
""",
                encoding="utf-8",
            )

            result = run_scan(tmp_path)

            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            rule_ids = {finding["rule_id"] for finding in report["findings"]}
            self.assertIn("MISRA-HEUR-DYNALLOC", rule_ids)
            self.assertIn("MISRA-HEUR-UNSAFE-C", rule_ids)
            self.assertIn("MISRA-HEUR-CSTYLE-CAST", rule_ids)
            self.assertIn("MISRA-HEUR-RECURSION", rule_ids)
            self.assertEqual(report["summary"]["files_scanned"], 1)
            self.assertGreaterEqual(report["summary"]["findings"], 4)


    def test_clean_code_passes_with_no_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "safe.cpp"
            source.write_text(
                """
#include <array>
#include <cstdint>

std::int32_t sum(const std::array<std::int32_t, 3>& values) noexcept {
    std::int32_t total { 0 };
    for (const auto value : values) {
        total += value;
    }
    return total;
}
""",
                encoding="utf-8",
            )

            result = run_scan(tmp_path)

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["findings"], [])
            self.assertEqual(report["summary"]["files_scanned"], 1)


    def test_markdown_output_contains_findings_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "macro.hpp"
            source.write_text(
                """
#define SQUARE(x) ((x) * (x))
union Packet { int i; float f; };
""",
                encoding="utf-8",
            )

            result = run_scan(tmp_path, "--format", "markdown", "--fail-on", "none")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| Severity | Rule | File | Line | Message |", result.stdout)
            self.assertIn("MISRA-HEUR-MACRO-PARAM", result.stdout)
            self.assertIn("MISRA-HEUR-UNION", result.stdout)


if __name__ == "__main__":
    unittest.main()
