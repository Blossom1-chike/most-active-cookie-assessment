from typing import List, TextIO

def parse_csv_log(file: TextIO) -> List[tuple[str, str]]:
    """
    This functions parses a cookie log CSV into a list of (cookie, date) tuples.

    Args:
        file: This is a file-like object (open file, StringIO, stdin) with an iterable of lines in CSV format.

    Returns:
        A list of (cookie_id, date_string) tuples 

    Raises:
        A ValueError: If a line does not conform to the expected two-field CSV format.
    """
    records = []
    next(file)  # skips the header line: "cookie,timestamp"

    for line_number, line in enumerate(file, start=2):
        line = line.strip()
        if not line:
            continue  # skip blank lines gracefully

        parts = line.split(",")

        if len(parts) != 2:
            raise ValueError(f"Malformed line {line_number}: '{line}'")

        cookie = parts[0].strip()
        timestamp = parts[1].strip()

        # Extract the date portion only, e.g "2018-12-09T14:19:00+00:00" split by T gives "2018-12-09"
        date = timestamp.split("T")[0]
        records.append((cookie, date))

    return records