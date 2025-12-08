#!/usr/bin/env python3
"""
Reads:
- test_list.yaml : tests list
- result_test_auto.json : Django test report

and it displays:
- status for each TC
- a global statistic resume
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


def determine_auto_status_code(entries):
    """
    Determines a status code for an auto-unittest test:

    - "not_found": no entry in result_test_auto.json
    - "failed"   : at least one 'failed' or 'error'
    - "passed"   : at least one 'passed' and no failed/error
    """
    if not entries:
        return "not_found"

    statuses = {e.get("status") for e in entries}

    if any(s in ("failed", "error") for s in statuses):
        return "failed"
    if "passed" in statuses:
        return "passed"

    return "not_found"


def evaluate_auto_status_display(entries):
    """Returns the 'pretty' version to display (✅ / ❌ / Not found)."""
    code = determine_auto_status_code(entries)
    if code == "passed":
        return "✅ Passed"
    if code == "failed":
        return "❌ Failed"
    return "️Not found"


def compute_test_status_display(test, auto_results_by_tc):
    """
    Returns the status text for a test:
    - manual        -> "🫱Manual test needed"
    - auto-unittest -> according to what's written in result_test_auto.json
    - others       -> "Unknown type ..."
    """
    test_id = test.get("id")
    test_type = test.get("type")

    if not test_id or not test_type:
        return "Invalid test entry"

    if test_type in ("manual", "manual"):
        return "🫱 Manual test needed"

    if test_type == "auto-unittest":
        entries = auto_results_by_tc.get(test_id)
        return evaluate_auto_status_display(entries)

    return f"Unknown type '{test_type}'"


def pct(part, whole):
    """Returns a string 'xx.x%' or 'N/A' if whole == 0."""
    if whole == 0:
        return "N/A"
    return f"{(part * 100.0 / whole):.1f}%"


def main():
    tests = load_test_list()
    print("Lecture des tests auto via result_test_auto.json…")

    auto_results_by_tc = load_auto_results()
    print("OK\n")

    total_tests = 0
    manual_tests = 0
    auto_tests = 0
    auto_passed = 0
    auto_failed = 0
    auto_not_found = 0
    other_type_tests = 0

    for test in tests:
        total_tests += 1
        test_id = test.get("id", "UNKNOWN")
        test_type = test.get("type", "UNKNOWN")

        if test_type in ("manual", "manuel"):
            manual_tests += 1
        elif test_type == "auto-unittest":
            auto_tests += 1
            entries = auto_results_by_tc.get(test_id)
            code = determine_auto_status_code(entries)
            if code == "passed":
                auto_passed += 1
            elif code == "failed":
                auto_failed += 1
            else:
                auto_not_found += 1
        else:
            other_type_tests += 1

        status_text = compute_test_status_display(test, auto_results_by_tc)
        print(f"{test_id:<5} | {test_type:<13} | {status_text}")

    print("\n=== Résumé des tests ===")
    print(f"Nombre total de tests définis dans test_list.yaml : {total_tests}")

    print(
        f"- Tests manuels      : {manual_tests} "
        f"({pct(manual_tests, total_tests)} du total)"
    )

    print(
        f"- Tests auto-unittest: {auto_tests} "
        f"({pct(auto_tests, total_tests)} du total)"
    )

    if other_type_tests:
        print(
            f"- Autres types de tests (ex: auto-selenium) : {other_type_tests} "
            f"({pct(other_type_tests, total_tests)} du total)"
        )

    print("\nParmi les tests auto-unittest :")
    print(
        f"- Avec implémentation (trouvés dans result_test_auto.json) : "
        f"{auto_tests - auto_not_found} "
        f"({pct(auto_tests - auto_not_found, auto_tests)} des tests auto)"
        if auto_tests
        else "- Aucun test auto-unittest défini."
    )

    print(
        f"  - Passés (tous les tests liés au TC sont passés) : "
        f"{auto_passed} ({pct(auto_passed, auto_tests)} des tests auto)"
        if auto_tests
        else ""
    )
    print(
        f"  - Échoués (au moins un test failed/error)        : "
        f"{auto_failed} ({pct(auto_failed, auto_tests)} des tests auto)"
        if auto_tests
        else ""
    )
    print(
        f"  - Not found (aucun test auto pour ce TC)        : "
        f"{auto_not_found} ({pct(auto_not_found, auto_tests)} des tests auto)"
        if auto_tests
        else ""
    )


if __name__ == "__main__":
    main()
