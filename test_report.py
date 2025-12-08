#!/usr/bin/env python3
"""
Reads:
- test_list.yaml : tests list
- result_test_auto.json : Django test report

and it display a textual test report.
"""

import json
import sys
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent
TEST_LIST_PATH = BASE_DIR / "test_list.yaml"
AUTO_RESULTS_PATH = BASE_DIR / "result_test_auto.json"


def load_test_list():
    """Charges test_list.yaml and returns the test list."""
    if not TEST_LIST_PATH.exists():
        print(f"ERROR: {TEST_LIST_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with TEST_LIST_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    tests = data.get("tests", [])
    if not isinstance(tests, list):
        print("ERROR: test_list.yaml does not contain a 'tests' list", file=sys.stderr)
        sys.exit(1)

    return tests


def load_auto_results():
    """Charges result_test_auto.json and returns a dict."""
    if not AUTO_RESULTS_PATH.exists():
        print(f"WARNING: {AUTO_RESULTS_PATH} not found, auto tests will be 'Not found'")
        return {}

    with AUTO_RESULTS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    mapping = {}
    for entry in data.get("tests", []):
        tc_id = entry.get("test_case_id")
        if not tc_id:
            continue
        mapping.setdefault(tc_id, []).append(entry)

    return mapping


def evaluate_auto_status(test_id: str, auto_results_for_id):
    """
    Determines the status for an auto-unittest test:

    - if no entry: "Not found"
    - if at least failed/error: "❌Failed"
    - or else if at least passed: "✅Passed"
    - else: "Not found" (by default)
    """
    if not auto_results_for_id:
        return "️Not found"

    statuses = {entry.get("status") for entry in auto_results_for_id}

    if any(s in ("failed", "error") for s in statuses):
        return "❌ Failed"
    if "passed" in statuses:
        return "✅ Passed"

    return "️Not found"


def compute_test_status(test, auto_results_by_tc):
    """
    Returns the status text for a test:
    - manual        -> "🫱Manual test needed"
    - auto-unittest -> according to what's written in result_test_auto.json
    """
    test_id = test.get("id")
    test_type = test.get("type")

    if not test_id or not test_type:
        return "Invalid test entry"

    if test_type in ("manual", "manual"):
        return "🫱 Manual test needed"

    if test_type == "auto-unittest":
        entries = auto_results_by_tc.get(test_id)
        return evaluate_auto_status(test_id, entries)

    return f"Unknown type '{test_type}'"


def main():
    tests = load_test_list()
    print("Lecture des tests auto via result_test_auto.json…")

    auto_results_by_tc = load_auto_results()
    print("OK")

    for test in tests:
        test_id = test.get("id", "UNKNOWN")
        test_type = test.get("type", "UNKNOWN")
        status_text = compute_test_status(test, auto_results_by_tc)

        print(f"{test_id:<5} | {test_type:<13} | {status_text}")


if __name__ == "__main__":
    main()
