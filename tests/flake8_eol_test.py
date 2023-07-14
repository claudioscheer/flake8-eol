import os
import ast
import unittest
from typing import Set
from flake8_eol import EOLChecker


def _results(code: str) -> Set[str]:
    with open("test.py", "w") as f:
        f.write(code)
    checker = EOLChecker(ast.parse(code), "test.py")
    return {f"{line}:{col} {msg}" for line, col, msg, _ in checker.run()}


class TestEOL(unittest.TestCase):
    def tearDown(self) -> None:
        os.remove("test.py")
        return super().tearDown()

    def test_no_code(self):
        code = ""
        self.assertEqual(_results(code), set())

    def test_no_eol(self):
        code = "a = 1"
        self.assertEqual(_results(code), set())

    def test_n_eol(self):
        code = "a = 1\n"
        self.assertEqual(_results(code), set())

    def test_windows_eol(self):
        code = "a = 1\r\nbanana = 2\r\ncad = 3"
        self.assertEqual(
            _results(code),
            {
                "1:6 EOL001 make sure to use '\\n' instead of '\\r\\n' or '\\r'",
                "2:11 EOL001 make sure to use '\\n' instead of '\\r\\n' or '\\r'",
            },
        )

    def test_mac_eol(self):
        code = "a = 1\rbanana = 2\rcad = 3"
        self.assertEqual(
            _results(code),
            {
                "1:6 EOL001 make sure to use '\\n' instead of '\\r\\n' or '\\r'",
                "2:11 EOL001 make sure to use '\\n' instead of '\\r\\n' or '\\r'",
            },
        )

    def test_r_str(self):
        code = "a = 'a\\rb'\nbanana = 2"
        self.assertEqual(_results(code), set())


if __name__ == "__main__":
    unittest.main()
