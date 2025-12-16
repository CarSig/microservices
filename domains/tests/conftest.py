import pytest
import builtins
import logging

_current_file = None
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

@pytest.fixture(autouse=True)
def disable_app_noise(monkeypatch):
    """
    Suppress noisy print() calls from the app (e.g. request timing),
    but keep pytest output.
    """
    original_print = builtins.print

    def filtered_print(*args, **kwargs):
        if args and isinstance(args[0], str):
            # Suppress request timing lines
            if args[0].startswith("[GET]"):
                return
        original_print(*args, **kwargs)

    monkeypatch.setattr(builtins, "print", filtered_print)

    # Also silence logging, just in case
    logging.getLogger().setLevel(logging.CRITICAL)


def pytest_runtest_logstart(nodeid, location):
    global _current_file
    file_path, _, _ = location

    if file_path != _current_file:
        _current_file = file_path
        file_name = file_path.split("/")[-1].split("\\")[-1]
        print(f"\n== {file_name} ==")


def pytest_runtest_logreport(report):
    if report.when == "call":
        test_name = report.nodeid.split("::")[-1]
        if test_name.startswith("test_"):
            test_name = test_name[5:]
            

        if report.outcome == "passed":
            status = f"{GREEN}✔{RESET}"
        elif report.outcome == "failed":
            status = f"{RED}✘{RESET}"
        else:
            status = f"{YELLOW}{report.outcome.upper()}{RESET}"

        print(f"{test_name} {status}")
