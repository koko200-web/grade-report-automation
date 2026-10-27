# Grade Report Automation

A small Python tool that turns a spreadsheet of student scores into a graded report.

## The problem

Grading a class by typing each score into a program is slow and easy to get wrong.
This script reads the scores from a CSV file, checks every row, assigns a grade and
produces a report automatically. Rows with problems (missing name, missing or
non-numeric score, score outside 0-100) are reported instead of crashing the program.

## How to run

Requires Python 3.8 or newer. No extra packages are needed.

```
python grade_report.py scores.csv
```

Optional: choose the report file name.

```
python grade_report.py scores.csv -o my_report.csv
```

The input CSV needs two columns, `name` and `score` (see `scores.csv`).

## Example output

```
Students graded: 7
Rows rejected:   4
Average score:   71.5
Grade counts:    A: 3, B: 1, C: 1, D: 1, F: 1

Rejected rows (please fix in the input file):
  line 7: Pauline: score 'abc' is not a number
  line 8: Jonas: score is missing
  line 9: Marta: score 105 is outside the range 0-100
  line 10: name is missing

Report saved to scores_graded.csv
```

## Grade boundaries

| Score  | Grade |
|--------|-------|
| 80-100 | A     |
| 70-79  | B     |
| 60-69  | C     |
| 50-59  | D     |
| 0-49   | F     |

## Tests

```
python -m unittest -v
```

## What I learned / possible next steps

- Reading and writing CSV files with the `csv` module
- Validating data and reporting errors clearly
- Writing unit tests
- Next: support Excel (`.xlsx`) files, and add a chart of the grade distribution
