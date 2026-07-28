"""Unit tests for safe aggregate essential-model diagnostics."""

from __future__ import annotations

import unittest

from scripts.ml.evaluate_essential_model import frequent_confusions


class EssentialModelEvaluationTests(unittest.TestCase):
    def test_frequent_confusions_excludes_correct_predictions(self) -> None:
        result = frequent_confusions(
            ["Credit card", "Credit card", "Mortgage", "Mortgage"],
            ["Mortgage", "Mortgage", "Mortgage", "Credit card"],
        )
        self.assertEqual(result[0], {"actual": "Credit card", "predicted": "Mortgage", "count": 2})
        self.assertEqual(result[1], {"actual": "Mortgage", "predicted": "Credit card", "count": 1})

    def test_frequent_confusions_contains_no_input_text(self) -> None:
        result = frequent_confusions(["A", "B"], ["B", "B"])
        self.assertEqual(result, [{"actual": "A", "predicted": "B", "count": 1}])
        self.assertNotIn("narrative", str(result).lower())


if __name__ == "__main__":
    unittest.main()
