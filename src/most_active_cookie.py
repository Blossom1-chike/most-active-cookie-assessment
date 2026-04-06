import argparse
import sys

from analyzer import count_cookies_on_target_date, find_most_active_cookies
from log_parser import parse_csv_log

def main():
    """
    This function is the main entry point which calls the functions that parses CLI arguments, processes the log file,
    and prints the most active cookie(s) for the given date to stdout.

    Errors are written to stderr and exit with a non-zero status code
    to signal failure to the calling shell.
    """
    args = _parse_args()

    try:
        # open and read csv log file 
        with open(args.filename, "r") as f:
            records = parse_csv_log(f) #parses csv into list of tuples
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    counts = count_cookies_on_target_date(records, args.date)
    most_active_cookies = find_most_active_cookies(counts)

    for cookie in most_active_cookies:
        print(cookie)


def _parse_args() -> argparse.Namespace:
    """
    This function defines and parses command line arguments.

    It is prefixed with an underscore to signal this is an internal helper
    not intended to be called directly by external code.

    Returns:
        A Namespace object with:
            - filename: path to the cookie log CSV file
            - date: target date in YYYY-MM-DD format
    """
    parser = argparse.ArgumentParser(description="Find the most active cookie(s) in a log file for a given date.")
    parser.add_argument("-f", dest="filename", required=True, help="Path to cookie log CSV file")
    parser.add_argument("-d", dest="date", required=True, help="Target date in YYYY-MM-DD format")
    return parser.parse_args()


if __name__ == "__main__":
    main()