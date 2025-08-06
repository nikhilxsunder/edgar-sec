# Test Coverage Report

Last updated: 2025-08-06

## Coverage Summary

Overall coverage: 100%

## Detailed Coverage

```
============================= test session starts ==============================
platform linux -- Python 3.11.13, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/runner/work/edgar-sec/edgar-sec
configfile: pyproject.toml
plugins: cov-6.2.1, asyncio-1.1.0, anyio-4.10.0, hypothesis-6.137.1, mock-3.14.1
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 83 items

tests/clients_test.py .............................................      [ 54%]
tests/helpers_test.py ............                                       [ 68%]
tests/objects_test.py ..........................                         [100%]

================================ tests coverage ================================
_______________ coverage: platform linux, python 3.11.13-final-0 _______________

Name                         Stmts   Miss  Cover
------------------------------------------------
src/edgar_sec/__about__.py       7      0   100%
src/edgar_sec/__init__.py        9      0   100%
src/edgar_sec/clients.py       244      0   100%
src/edgar_sec/helpers.py       110      0   100%
src/edgar_sec/objects.py       209      0   100%
------------------------------------------------
TOTAL                          579      0   100%
Coverage XML written to file coverage.xml
============================== 83 passed in 5.70s ==============================
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
