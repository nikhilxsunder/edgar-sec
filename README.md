# edgar-sec

## A feature-rich python package for interacting with the US Securities and Exchange Commission API: EDGAR

<div align="center">
    <a href="https://github.com/nikhilxsunder/edgar-sec/actions/workflows/main.yml"><img src="https://github.com/nikhilxsunder/edgar-sec/actions/workflows/main.yml/badge.svg" alt="Build and test GitHub"></a>
    <a href="https://github.com/nikhilxsunder/edgar-sec/actions/workflows/analyze.yml"><img src="https://github.com/nikhilxsunder/edgar-sec/actions/workflows/analyze.yml/badge.svg" alt="Analyze Status"></a>
    <a href="https://github.com/nikhilxsunder/edgar-sec/actions/workflows/test.yml"><img src="https://github.com/nikhilxsunder/edgar-sec/actions/workflows/test.yml/badge.svg" alt="Test Status"></a>
    <a href="https://github.com/nikhilxsunder/edgar-sec/actions/workflows/codeql.yml"><img src="https://github.com/nikhilxsunder/edgar-sec/actions/workflows/codeql.yml/badge.svg" alt="CodeQL"></a>
    <a href="https://pypi.org/project/edgar-sec/"><img src="https://img.shields.io/pypi/v/edgar-sec.svg" alt="PyPI version"></a>
    <a href="https://pepy.tech/projects/edgar-sec"><img src="https://static.pepy.tech/badge/edgar-sec" alt="PyPI Downloads"></a>
    <a href="https://www.bestpractices.dev/projects/10210"><img src="https://www.bestpractices.dev/projects/10210/badge"></a>
    <a href="https://codecov.io/gh/nikhilxsunder/edgar-sec"><img src="https://codecov.io/gh/nikhilxsunder/edgar-sec/graph/badge.svg?token=RDI3Q99UJB" alt="codecov"></a>
    <a href="https://anaconda.org/nikhil.sunder/edgar-sec"><img src="https://img.shields.io/conda/vn/nikhil.sunder/edgar-sec.svg" alt="Conda Version"></a>
    <a href="https://anaconda.org/nikhil.sunder/edgar-sec"><img src="https://img.shields.io/conda/dn/nikhil.sunder/edgar-sec.svg" alt="Conda Downloads"></a>
</div>

### Features

- Native support for asynchronous requests (async).
- All method outputs are mapped to dataclasses for better usability.
- Local caching for easier data access and faster execution times.
- Built-in rate limiter that doesn't exceed 10 calls per second (ignores local caching).
- MyPy compatible type stubs.

### Installation

You can install the package using pip:

```sh
pip install edgar-sec
```

### Using conda

edgar-sec is available on Anaconda through the author's channel:

```sh
conda install -c nikhilxsunder edgar-sec
```

We recommend creating a dedicated environment:

```sh
conda create -n edgar-env
conda activate edgar-env
conda install -c nikhilxsunder edgar-sec
```

Note: edgar-sec will be submitted to conda-forge in the future for broader distribution.

### Rest API Usage

I recommend consulting the documentation at:
https://nikhilxsunder.github.io/edgar-sec/

Here is a simple example of how to use the package:

```python
# EDGAR API
import edgar_sec as ed
edgar = ed.EdgarAPI()

# Get company concept disclosures
company_concept = edgar.get_company_concept(central_index_key='0001067983', taxonomy='us-gaap', tag='AccountsPayableCurrent')
print(company_concept.label)

# Get company concept disclosures (async)
import asyncio
async def main():
    edgar = ed.EdgarAPI()
    company_concept = await edgar.get_company_concept(central_index_key='0001067983', taxonomy='us-gaap', tag='AccountsPayableCurrent')
    print(company_concept.label)
asyncio.run(main())
```

### Important Notes

- OpenSSF Badge in progress.

### Continuous Integration

Edgar-SEC uses GitHub Actions for continuous integration. The following workflows run automatically:

- **Build and Test**: Triggered on every push and pull request to verify the codebase builds and tests pass
- **Analyze**: Runs static code analysis to identify potential issues
- **Test**: Comprehensive test suite with coverage reporting
- **CodeQL**: Security analysis to detect vulnerabilities

These checks ensure that all contributions maintain code quality and don't introduce regressions.

Status badges at the top of this README reflect the current state of our CI pipelines.

### Development

Edgar-SEC uses standard Python packaging tools:

- **Poetry**: For dependency management and package building
- **pytest**: For testing
- **Sphinx**: For documentation generation

To set up the development environment:

```sh
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone https://github.com/nikhilxsunder/edgar-sec.git
cd edgar-sec

# Install dependencies
poetry install

# Run tests
poetry run pytest
```

### Testing

The project uses pytest as its testing framework. Tests are located in the `tests/` directory.

To run the complete test suite:

```sh
poetry run pytest
```

For running tests with coverage reports:

```sh
poetry run pytest --cov=edgar_sec tests/
```

To run a specific test file:

```sh
poetry run pytest tests/test_specific_module.py
```

#### Test Coverage

We aim to maintain a minimum of 80% code coverage across the codebase. This includes:

- Core functionality: 90%+ coverage
- Edge cases and error handling: 80%+ coverage
- Utility functions: 75%+ coverage

Continuous integration automatically runs tests on all pull requests and commits to the main branch.

#### Test Policy

Edgar-SEC requires tests for all new functionality. When contributing:

- All new features must include appropriate tests
- Bug fixes should include tests that verify the fix
- Tests should be added to the automated test suite in the `tests/` directory

## Security

For information about reporting security vulnerabilities in Edgar-SEC, please see our [Security Policy](https://github.com/nikhilxsunder/edgar-sec/blob/main/SECURITY.md).

### Contributing

Contributions are welcome! Please open an issue or submit a pull request.

### License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](https://github.com/nikhilxsunder/edgar-sec/blob/main/LICENSE) file for details.
