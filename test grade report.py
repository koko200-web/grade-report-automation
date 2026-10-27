import csv
import os
import tempfile
import unittest

from grade_report import calculate_grade, parse_score, read_scores, write_report, summarise


class TestGrades(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual(calculate_grade(100), "A")
        self.assertEqual(calculate_grade(80), "A")
        self.assertEqual(calculate_grade(79.9), "B")
        self.assertEqual(calculate_grade(70), "B")
        self.assertEqual(calculate_grade(60), "C")
        self.assertEqual(calculate_grade(50), "D")
        self.assertEqual(calculate_grade(49.9), "F")
        self.assertEqual(calculate_grade(0), "F")


class TestParseScore(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(parse_score("85"), 85.0)
        self.assertEqual(parse_score(" 72.5 "), 72.5)

    def test_invalid(self):
        for bad in ["abc", "", "   ", None, "105", "-1"]:
            with self.assertRaises(ValueError):
                parse_score(bad)


class TestFiles(unittest.TestCase):
    def make_csv(self, text):
        folder = tempfile.mkdtemp()
        path = os.path.join(folder, "scores.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write(text)
        return path

    def test_rejects_bad_rows_with_line_numbers(self):
        path = self.make_csv("name,score\nAna,90\nBen,abc\n,50\nCy,\n")
        students, rejected = read_scores(path)
        self.assertEqual(students, [("Ana", 90.0)])
        self.assertEqual([line for line, _ in rejected], [3, 4, 5])

    def test_missing_columns(self):
        path = self.make_csv("student,mark\nAna,90\n")
        with self.assertRaises(ValueError):
            read_scores(path)

    def test_report_and_summary(self):
        students = [("Ana", 90.0), ("Ben", 40.0)]
        folder = tempfile.mkdtemp()
        out = os.path.join(folder, "out.csv")
        write_report(out, students)
        with open(out, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["grade"], "A")
        self.assertEqual(rows[1]["grade"], "F")
        average, counts = summarise(students)
        self.assertEqual(average, 65.0)
        self.assertEqual(counts["A"], 1)
        self.assertEqual(counts["F"], 1)


if __name__ == "__main__":
    unittest.main()
