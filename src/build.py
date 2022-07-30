import logging
from subprocess import check_call
import sys
import unittest

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    level=logging.DEBUG,
)


def format() -> None:
    check_call(["black", "src"])


def lint() -> None:
    check_call(["flake8", "--exclude=.venv,ansible,vendor,__pycache__"])


def typecheck() -> None:
    check_call(
        [
            "mypy",
            "--warn-unused-configs",
            "--show-error-codes",
            "--exclude",
            "(.venv|ansible|vendor*)/$",
            "--config-file",
            "./pyproject.toml",
            "./src",
        ]
    )


def test(pattern: str = "test*.py") -> None:
    loader = unittest.TestLoader()
    tests = loader.discover(".", pattern)
    test_runner = unittest.runner.TextTestRunner()
    test_runner.run(tests)


def test_single() -> None:
    test(sys.argv[-1])


def build() -> None:
    lint()
    typecheck()
    test()
