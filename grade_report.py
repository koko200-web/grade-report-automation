"""Grade Report Automation

Reads a CSV file with the columns `name` and `score`, checks every row,
assigns a grade, and writes a graded report.
"""

import argparse
import csv
import sys


def calculate_grade(score):
    """Return the letter grade for a score from 0 to 100."""
    if score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def parse_score(text):
    """Turn text into a number between 0 and 100.

    Raises ValueError with a clear message if the text is not usable.
    The caller catches the error, so one bad row never crashes the program.
    """
    text = (text or "").strip()
    if text == "":
        raise ValueError("score is missing")
    try:
        score = float(text)
    except ValueError:
        raise ValueError(f"score '{text}' is not a number")
    if score < 0 or score > 100:
        raise ValueError(f"score {text} is outside the range 0-100")
    return score


def read_scores(path):
    """Read the CSV file.

    Returns (students, rejected):
      students: list of (name, score) for valid rows
      rejected: list of (line_number, message) for bad rows
    """
    students = []
    rejected = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        if "name" not in columns or "score" not in columns:
            raise ValueError("the CSV file needs the columns 'name' and 'score'")

        for row in reader:
            line = reader.line_num  # the real line number in the file
            name = (row.get("name") or "").strip()
            try:
                score = parse_score(row.get("score"))
            except ValueError as error:
                if name:
                    rejected.append((line, f"{name}: {error}"))
                else:
                    rejected.append((line, "name is missing"))
                continue

            if not name:
                rejected.append((line, "name is missing"))
                continue

            students.append((name, score))

    return students, rejected


def write_report(path, students):
    """Write the graded report to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "score", "grade"])
        for name, score in students:
            writer.writerow([name, score, calculate_grade(score)])


def summarise(students):
    """Return (average, grade_counts). Average is None if there are no students."""
    counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for _, score in students:
        counts[calculate_grade(score)] += 1
    if not students:
        return None, counts
    average = sum(score for _, score in students) / len(students)
    return average, counts


def main(argv=None):
    parser = argparse.ArgumentParser(description="Create a graded report from a CSV of scores.")
    parser.add_argument("input", help="CSV file with the columns name,score")
    parser.add_argument("-o", "--output", help="name of the report file")
    args = parser.parse_args(argv)

    output = args.output
    if not output:
        base = args.input[:-4] if args.input.lower().endswith(".csv") else args.input
        output = base + "_graded.csv"

    try:
        students, rejected = read_scores(args.input)
    except FileNotFoundError:
        print(f"Error: file '{args.input}' was not found.")
        return 1
    except ValueError as error:
        print(f"Error: {error}.")
        return 1

    average, counts = summarise(students)

    print(f"Students graded: {len(students)}")
    print(f"Rows rejected:   {len(rejected)}")
    if average is not None:
        print(f"Average score:   {average:.1f}")
        shown = ", ".join(f"{g}: {n}" for g, n in counts.items() if n > 0)
        print(f"Grade counts:    {shown}")

    if rejected:
        print()
        print("Rejected rows (please fix in the input file):")
        for line, message in rejected:
            print(f"  line {line}: {message}")

    write_report(output, students)
    print()
    print(f"Report saved to {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
