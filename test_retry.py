"""Basic tests for the retry helper."""

import unittest
from unittest import mock

from retry import retry_with_backoff


class RetryBackoffTests(unittest.TestCase):
    def test_returns_value_on_success(self):
        self.assertEqual(retry_with_backoff(lambda: 42), 42)

    def test_retries_then_succeeds(self):
        calls = []

        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise ValueError("boom")
            return "ok"

        with mock.patch("retry.time.sleep"):
            self.assertEqual(retry_with_backoff(flaky), "ok")
            self.assertEqual(len(calls), 3)

    def test_raises_after_max_attempts(self):
        def always_fails():
            raise ValueError("boom")

        with mock.patch("retry.time.sleep"):
            with self.assertRaises(ValueError):
                retry_with_backoff(always_fails, attempts=3)


if __name__ == "__main__":
    unittest.main()
