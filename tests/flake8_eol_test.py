import os
import ast
import unittest
from typing import Set
from flake8_eol.flake8_eol import EOLChecker


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

    def test_r_n_eol(self):
        code = "a = 1\r\n"
        self.assertEqual(
            _results(code),
            {"1:1 EOL001 replace '\\r\\n' at the end of the line with '\\n'"},
        )


if __name__ == "__main__":
    unittest.main()
