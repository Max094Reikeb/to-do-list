from __future__ import annotations

import os
import sys
import time

from axe_selenium_python import Axe
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo.settings")

import django  # noqa: E402

django.setup()

from tasks.models import Task  # noqa: E402

task = Task.objects.create(title="Axe Test Task", complete=False)
TASK_ID = task.id

URLS = [
    "http://127.0.0.1:8000/",
    f"http://127.0.0.1:8000/update_task/{TASK_ID}/",
    f"http://127.0.0.1:8000/delete_task/{TASK_ID}/",
    "http://127.0.0.1:8000/admin/login/",
]


def run_axe_on_url(driver: webdriver.Chrome, url: str) -> bool:
    """
    Launch axe-core on a URL and return True if there is no
    violation WCAG 2.1 level A (tag 'wcag2a').
    """
    print(f"\n=== Checking accessibility for {url} ===")
    driver.get(url)
    time.sleep(1)

    axe = Axe(driver)
    axe.inject()
    results = axe.run()

    violations = results.get("violations", [])

    wcag2a_violations = [
        v for v in violations if "wcag2a" in v.get("tags", [])
    ]

    if wcag2a_violations:
        print(f"{len(wcag2a_violations)} WCAG 2.1 A violation(s) found on {url}:")
        for v in wcag2a_violations:
            print(f"  - {v['id']}: {v['description']}")
            print(f"    Help: {v.get('helpUrl', 'no helpUrl')}")
        return False

    print(f"{url} passed WCAG 2.1 A checks (0 violations).")
    return True


def main() -> int:
    options = Options()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    all_ok = True
    try:
        for url in URLS:
            ok = run_axe_on_url(driver, url)
            if not ok:
                all_ok = False
    finally:
        driver.quit()

    if not all_ok:
        print("\nAccessibility checks failed (WCAG 2.1 A violations detected).")
        return 1

    print("\nAll accessibility checks passed (WCAG 2.1 A = 100%).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
