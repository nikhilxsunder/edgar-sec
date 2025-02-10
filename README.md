# edgar-sec
## A simple python wrapper for interacting with the US Securities and Exchange Commission API: EDGAR
## This package is still in beta please try it out and please report any comments, concerns, and issues.

[![Build and test GitHub](https://github.com/nikhilxsunder/edgar-sec/actions/workflows/main.yml/badge.svg)](https://github.com/nikhilxsunder/edgar-sec/actions)
[![PyPI version](https://img.shields.io/pypi/v/edgar-sec.svg)](https://pypi.org/project/edgar-sec/)
[![Downloads](https://img.shields.io/pypi/dm/edgar-sec.svg)](https://pypi.org/project/edgar-sec/)

### Latest Update

- Complete methods for all EDGAR Endpoints

### Installation

You can install the package using pip:

```sh
pip install edgar-sec
```

### Rest API Usage

I recommend consulting the offical SEC EDGAR documentation at: 
https://www.sec.gov/search-filings/edgar-application-programming-interfaces

Here is a simple example of how to use the package:

```python
# Imports
from edgar-sec import EdgarAPI

# EDGAR API
client = EdgarAPI()

# Get company concept disclosures
company_concept = client.get_company_concept(central_index_key='0001067983', taxonomy='us-gaap', tag='AccountsPayableCurrent')
print(company_concept)
```

### Important Notes

- Currently all all responses are returned as text.
- Store your API keys and secrets in environment variables or secure storage solutions.
- Do not hardcode your API keys and secrets in your scripts.

### Features

- Get company filing data
- Get Historical data
- Interact with all SEC EDGAR API endpoints

## Next Update 

- Pandas dataframe output

### Planned Updates

- XBLR parsing options
- Polars dataframe outtput

### Contributing

Contributions are welcome! Please open an issue or submit a pull request.

### License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.