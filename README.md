# Most Active Cookie

A command line program that processes a cookie log file and returns the most
active cookie(s) for a given date.

A cookie is considered "most active" if it appears more times than any other
cookie on the specified date. If multiple cookies share the highest count,
all of them are returned.

## Project Structure

```
most-active-cookie/
├── src/
│   ├── most_active_cookie.py   # CLI entry point
│   ├── log_parser.py           # CSV parsing
│   └── analyzer.py             # Core logic (counting, finding most active)
├── tests/
│   ├── test_analyzer.py
│   └── test_parser.py
├── cookie_log.csv              # Sample log file
├── pytest.ini                  # Test runner configuration
├── requirements.txt            # Runtime dependencies
├── requirements-dev.txt        # Development dependencies
├── .gitignore
└── README.md
```

## Setup

**1. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/most_active_cookie.py -f cookie_log.csv -d 2018-12-09
```

`-f`: Path to the cookie log CSV file    
`-d`: Target date in `YYYY-MM-DD` format 

**Example output**

```
AtY0laUfhglK3lC7
```

Note: If multiple cookies tie for most active, each is printed on a separate line.


## Running Tests

Run the full test suite using the command:

```bash
pytest tests/
```

## Design Decisions

**Separation of concerns** — the program is split into three distinct layers:
parsing (`log_parser.py`), analysis (`analyzer.py`), and the CLI
(`most_active_cookie.py`). Each layer can be changed or tested independently.

**File object over filepath** — `parse_log` accepts a file-like object rather
than a filepath. This makes it flexible (works with real files, `StringIO`,
or stdin) and keeps file handling concerns out of the parser.

**Functions over classes** — the analyzer functions are stateless: they take
input and return output with no shared state. In Python, module-level functions
are the cleaner choice in this case. A class would be appropriate if
requirements grew to need shared state, such as keeping a log loaded in memory
and running multiple queries against it.

**Errors to stderr, results to stdout** — following Unix conventions, error
messages are written to `stderr` and the program exits with a non-zero status
code on failure, making it composable with other shell tools.