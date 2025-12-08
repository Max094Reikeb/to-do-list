import json
import unittest

from django.test.runner import DiscoverRunner


class JsonTestResult(unittest.TextTestResult):
    """
    Personalized TestResult that saves the test results under JSON file,
    with the `test_case_id` attribut for each test method.
    """

    def __init__(self, stream, descriptions, verbosity, json_path="result_test_auto.json"):
        super().__init__(stream, descriptions, verbosity)
        self.json_path = json_path
        self.tests_data = []

    def _record_test(self, test, status):
        test_id = test.id()
        module_name, class_name, method_name = test_id.rsplit(".", 2)

        cls = test.__class__
        method = getattr(cls, method_name, None)
        test_case_id = getattr(method, "test_case_id", None) if method is not None else None

        self.tests_data.append(
            {
                "test_case_id": test_case_id,
                "test_name": test_id,
                "module": module_name,
                "class": class_name,
                "method": method_name,
                "status": status,
            }
        )

    def addSuccess(self, test):
        super().addSuccess(test)
        self._record_test(test, "passed")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._record_test(test, "failed")

    def addError(self, test, err):
        super().addError(test, err)
        self._record_test(test, "error")

    def stopTestRun(self):
        super().stopTestRun()
        payload = {"tests": self.tests_data}
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)


class JsonTextTestRunner(unittest.TextTestRunner):
    """TextTestRunner that user JsonTestResult to produce the JSON."""

    def __init__(self, *args, json_path="result_test_auto.json", **kwargs):
        super().__init__(*args, **kwargs)
        self.json_path = json_path

    def _makeResult(self):
        return JsonTestResult(
            self.stream,
            self.descriptions,
            self.verbosity,
            json_path=self.json_path,
        )


class JsonTestRunner(DiscoverRunner):
    """Personalized Django runner that uses JsonTextTestRunner."""

    test_runner = JsonTextTestRunner

    def __init__(self, *args, **kwargs):
        self.json_path = kwargs.pop("json_path", "result_test_auto.json")
        super().__init__(*args, **kwargs)

    def run_suite(self, suite, **kwargs):
        runner = self.test_runner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            buffer=self.buffer,
            json_path=self.json_path,
        )
        return runner.run(suite)
