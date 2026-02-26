# Task A: Appointment Slot Recommender
## System Description

You are asked to implement Python functions that can recommend available meeting slots given working hours, busy intervals, meeting duration, optional buffer time, and a candidate window. The function must return chronologically ordered suggestions that fit within working hours and do not overlap busy intervals under buffering rules. It must handle edge cases such as adjacent intervals, tiny gaps, and buffers eliminating availability.

Inputs include: (i) a list of medications with frequencies and permissible time windows;
(ii) user quiet hours during which notifications must not occur;
(iii) a maximum notification rate (e.g., no more than 𝑘 reminders per hour);
(iv) an optional snooze operation that shifts a reminder while preserving constraints. The scheduler outputs the next 𝑁 reminders in chronological order and must behave deterministically under ties. 



## Structure

- **med_scheduler.py** – starter file where you implement. Do not rename this file.
- **test_med_scheduler.py** – Public tests you can run to check basic correctness. Use a test runner such as `pytest` to execute these tests.



## Running Tests

1. Install Python 3 if not already installed.
2. Implement your solution in `med_scheduler.py`.
3. Optionally create `test_med_scheduler.py` and write at least 5 test cases.
4. Run tests using:

```
pytest file_name.py
```

5. Fix any failing tests before moving on. Remember that hidden tests will check additional requirements

 

# How to Run Test Cases 

---

## 1. Install pytest

If you don't already have `pytest` installed, you can install it using pip:

```bash
pip install pytest
```

Verify the installation:

```bash
pytest --version
```

---

## 2. Organize Your Files

Place your implementation and test files in the same directory:

```
/project-folder
    solution.py         # your implementation
    test_solution.py    # your test cases
```

* `solution.py` contains the `is_allocation_feasible` function.
* `test_solution.py` contains the test functions.

> **Note:** If your file names are different, adjust the instructions below accordingly.

---

## 3. Update Test File Import

In `test_solution.py`, import your implementation module. For example:

```python
import pytest
from solution import is_allocation_feasible # replace "solution" with your implementation file name without .py
```
---

## 4. Run All Tests

Navigate to the folder containing the files and run:

```bash
pytest
```

Or with more detailed output:

```bash
pytest -v
```

---

## 5. Run a Specific Test Function

To run a single test function, use the `-k` option:

```bash
pytest -v -k test_name
```

---

## 6. If Your File Names Are Different

* **Test file**: If your test file doesn't match `test_*.py` or `*_test.py`, specify it explicitly:

```bash
pytest mytests.py
```

* Run a single test in a differently named file:

```bash
pytest -v mytests.py -k test_name
```

---

## Summary

1. Install `pytest`
2. Organize files
3. Update the import in test file if necessary
4. Run all tests: `pytest -v`
5. Run a single test: `pytest -v -k <test_name>`
6. Adjust commands if file names differ

---

You are ready to run the test cases for your `is_allocation_feasible` implementation!
