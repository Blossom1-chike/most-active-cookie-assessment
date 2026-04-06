import subprocess
import sys
import os

"""
    Integration tests for the most-active-cookie program.

    Unlike unit tests which test each layer in isolation, these tests
    exercise the full pipeline from CLI args - file read - parse - analyze - stdout.
    They catch wiring bugs between layers that unit tests cannot detect.
"""

# Path to the CLI entry point relative to the project root.
# Assumes pytest is always run from the project root, which is
# enforced by pytest.ini being present there.
CLI = os.path.join("src", "most_active_cookie.py")


def run_cli(*args: str) -> subprocess.CompletedProcess:
    """
    Run the CLI program as a subprocess and capture its output.

    This exercises the full pipeline exactly as an end user or
    downstream consumer would — via the command line.

    Args:
        *args: Command line arguments to pass to the program.

    Returns:
        A CompletedProcess instance with stdout, stderr, and returncode.
    """
    return subprocess.run(
        [sys.executable, CLI, *args],
        capture_output=True,
        text=True,
    )


class TestEndToEndPipeline:

    def test_returns_most_active_cookie_for_given_date(self, tmp_path):
        """
        The full pipeline should return the cookie with the highest
        occurrence count for the given date, written to stdout.
        """
        log_file = tmp_path / "cookie_log.csv"
        log_file.write_text(
            "cookie,timestamp\n"
            "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
            "SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n"
            "AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00\n"
        )

        result = run_cli("-f", str(log_file), "-d", "2018-12-09")

        assert result.returncode == 0
        assert result.stdout.strip() == "AtY0laUfhglK3lC7"

    def test_returns_all_tied_cookies_on_separate_lines(self, tmp_path):
        """
        When multiple cookies share the highest count, each must appear
        on its own line in stdout, no extra formatting or headers.
        """
        log_file = tmp_path / "cookie_log.csv"
        log_file.write_text(
            "cookie,timestamp\n"
            "AtY0laUfhglK3lC7,2018-12-08T14:19:00+00:00\n"
            "SAZuXPGUrfbcn5UA,2018-12-08T10:13:00+00:00\n"
        )

        result = run_cli("-f", str(log_file), "-d", "2018-12-08")

        assert result.returncode == 0
        output_lines = result.stdout.strip().splitlines()
        assert set(output_lines) == {"AtY0laUfhglK3lC7", "SAZuXPGUrfbcn5UA"}

    def test_produces_no_output_for_date_with_no_entries(self, tmp_path):
        """
        When no cookies exist for the given date, stdout should be
        empty, no error, no placeholder text.
        """
        log_file = tmp_path / "cookie_log.csv"
        log_file.write_text(
            "cookie,timestamp\n"
            "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
        )

        result = run_cli("-f", str(log_file), "-d", "2018-12-01")

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_writes_error_to_stderr_and_exits_nonzero_for_missing_file(self):
        """
        When the specified file does not exist, the program must write
        an error message to stderr and exit with a non-zero status code.
        """
        result = run_cli("-f", "nonexistent.csv", "-d", "2018-12-09")

        assert result.returncode != 0
        assert "Error" in result.stderr

    def test_output_contains_only_cookie_ids_with_no_extra_formatting(self, tmp_path):
        """
        stdout must contain only raw cookie IDs, no headers, labels, or decorators.
        """
        log_file = tmp_path / "cookie_log.csv"
        log_file.write_text(
            "cookie,timestamp\n"
            "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
        )

        result = run_cli("-f", str(log_file), "-d", "2018-12-09")

        assert result.returncode == 0
        assert ":" not in result.stdout
        assert result.stdout.strip() == "AtY0laUfhglK3lC7"