import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import extract_rule_index


class ExtractRuleIndexTests(unittest.TestCase):
    def test_ignores_rule_references_without_metadata(self) -> None:
        text = """
Some introductory text mentions Rule 8.2.6 as an example.

Rule 8.2.6
Category Required
Analysis Decidable, Single Translation Unit
"""

        entries = extract_rule_index.collect_entries(text)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].identifier, "Rule 8.2.6")
        self.assertEqual(entries[0].line, 4)
        self.assertEqual(entries[0].category, "Required")
        self.assertEqual(entries[0].analysis, "Decidable, Single Translation Unit")


if __name__ == "__main__":
    unittest.main()
