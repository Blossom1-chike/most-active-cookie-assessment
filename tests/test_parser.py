import pytest
from io import StringIO
from src.log_parser import parse_csv_log

"""
    Unit tests for the log_parser module (parse_csv_log).
    
    Each test is fully independent, input is constructed inline using
    StringIO, so no real files, no shared state, and no cleanup needed.
    Tests can run in any order and will always produce consistent results.
    
    Naming convention: test_<function>_<scenario>
    Long descriptive names are intentional because they serve as documentation
    and make failures immediately understandable without reading the body.
"""

# Helper function
def make_log(*data_lines: str) -> StringIO:
    """
    A helper function that builds a valid CSV log file as a StringIO object.
    Note: it automatically inserts the required header line so each test
    only needs to specify the data rows it cares about.
    """
    lines = ["cookie,timestamp"] + list(data_lines)
    return StringIO("\n".join(lines))


class TestParseLog:

    def test_parse_csv_log_returns_correct_cookie_id_from_single_record(self):
        """
        The cookie ID in the first field of each CSV row should be
        extracted exactly as it appears, without modification.
        """
        f = make_log("AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00")

        records = parse_csv_log(f)

        assert records[0][0] == "AtY0laUfhglK3lC7"

    def test_parse_csv_log_extracts_date_portion_only_from_timestamp(self):
        """
        Only the date portion (YYYY-MM-DD) should be kept from the
        timestamp. The time and timezone components must be discarded.
        """
        f = make_log("AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00")

        records = parse_csv_log(f)

        assert records[0][1] == "2018-12-09"

    def test_parse_csv_log_parses_all_records_from_multi_row_file(self):
        """
        Every data row in the file should produce exactly one tuple
        in the result, in the same order they appear in the file.
        """
        f = make_log(
            "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00",
            "SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00",
            "4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00",
        )

        records = parse_csv_log(f)

        assert len(records) == 3
        assert records[1] == ("SAZuXPGUrfbcn5UA", "2018-12-08")
        assert records[2] == ("4sMM2LxV07bPJzwf", "2018-12-07")

    def test_parse_csv_log_returns_empty_list_for_header_only_file(self):
        """
        A file that contains only the header line and no data rows
        is valid input and should return an empty list.
        """
        f = StringIO("cookie,timestamp\n")

        records = parse_csv_log(f)

        assert records == []

    def test_parse_csv_log_skips_blank_lines_without_raising_an_error(self):
        """
        Blank lines anywhere in the file after the header should be
        silently ignored and not counted as records.
        """
        f = StringIO(
            "cookie,timestamp\n"
            "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
            "\n"
            "SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n"
        )

        records = parse_csv_log(f)

        assert len(records) == 2

    def test_parse_csv_log_raises_value_error_for_line_missing_comma_separator(self):
        """
        A line that cannot be split into exactly two fields should raise
        a ValueError. This guards against corrupted or malformed log files.
        """
        f = make_log("BADLINE_WITHOUT_COMMA")

        with pytest.raises(ValueError, match="Malformed line"):
            parse_csv_log(f)

    def test_parse_csv_log_includes_line_number_in_error_message_for_malformed_line(self):
        """
        The ValueError raised for a malformed line must include the line
        number to help with debugging real log files. The first data row
        is line 2 (after the header), so the second data row is line 3.
        """
        f = make_log(
            "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00",
            "BADLINE",  # this is line 3 in the file
        )

        with pytest.raises(ValueError, match="line 3"):
            parse_csv_log(f)