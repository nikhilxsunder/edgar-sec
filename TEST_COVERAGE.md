# Test Coverage Report

Last updated: 2025-04-30

## Coverage Summary

Overall coverage: 91%

## Detailed Coverage

```
============================= test session starts ==============================
platform linux -- Python 3.11.12, pytest-8.3.5, pluggy-1.5.0
rootdir: /home/runner/work/edgar-sec/edgar-sec
configfile: pyproject.toml
plugins: cov-3.0.0, hypothesis-6.130.0, anyio-4.9.0, asyncio-0.15.1, mock-3.14.0
collected 26 items

tests/edgar_data_test.py ..........                                      [ 38%]
tests/edgar_sec_test.py ................                                 [100%]

---------- coverage: platform linux, python 3.11.12-final-0 ----------
Name                          Stmts   Miss  Cover
-------------------------------------------------
src/edgar_sec/__init__.py         3      0   100%
src/edgar_sec/edgar_data.py     222      5    98%
src/edgar_sec/edgar_sec.py      119     25    79%
-------------------------------------------------
TOTAL                           344     30    91%
Coverage XML written to file coverage.xml


======================== 26 passed, 2 warnings in 3.06s ========================
```

## Running Test Coverage Locally

To run the test suite with coverage:

```bash
pytest --cov=src/edgar_sec tests/
```

For a detailed HTML report:

```bash
pytest --cov=src/edgar_sec tests/ --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view the report.

## Coverage Goals

- Maintain at least 80% overall coverage
- All public APIs should have 100% coverage
- Focus on testing edge cases and error conditions
