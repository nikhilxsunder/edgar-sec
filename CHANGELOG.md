# Changelog

All notable changes to edgar-sec will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] -

### Changed

- Updated [pre-commit-config.yaml](https://github.com/nikhilxsunder/edgar-sec/blob/main/.pre-commit-config.yaml)
- Conda/Conda-Forge version now 2.0.0 in both meta.yaml files
- Complete overhaul of sphinx documentation
- Changed sphinx theme to [pydata-sphinx-theme](https://pypi.org/project/pydata-sphinx-theme/)
- Updated [pyproject.toml](https://github.com/nikhilxsunder/edgar-sec/blob/main/pyproject.toml)
- Updated imports for [**init**.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/src/edgar_sec/__init__.py)
- edgar_sec.py renamed to [clients.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/src/edgar_sec/clients.py)
- edgar_data.py renamed to [objects.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/src/edgar_sec/objects.py)
- Markdown documents updated:
  - [CHANGELOG.md](https://github.com/nikhilxsunder/edgar-sec/blob/main/CHANGELOG.md)
  - [CONTRIBUTING.md](https://github.com/nikhilxsunder/edgar-sec/blob/main/CONTRIBUTING.md)
  - [README.md](https://github.com/nikhilxsunder/edgar-sec/blob/main/README.md)
  - [SECURITY.md](https://github.com/nikhilxsunder/edgar-sec/blob/main/SECURITY.md)

### Added

- Created [conda-forge](https://github.com/nikhilxsunder/edgar-sec/tree/main/conda-forge) directory.
  - Added [meta.yaml](https://github.com/nikhilxsunder/edgar-sec/blob/main/conda-forge/meta.yaml) for conda-forge.
- Added [asyncache](https://pypi.org/project/asyncache/) dependency
- Added favicon file: [edgar-sec-favicon.ico](https://github.com/nikhilxsunder/edgar-sec/blob/main/docs/source/_static/edgar-sec-favicon.ico)
- Added logo file: [edgar-sec-logo.png](https://github.com/nikhilxsunder/edgar-sec/blob/main/docs/source/_static/edgar-sec-logo.png)
- Added [json_ld.js(https://github.com/nikhilxsunder/edgar-sec/blob/main/docs/source/_static/json_ld.js)] for sphinx
- Added sphinx autosummary templates:
  - [attribute.rst](https://github.com/nikhilxsunder/edgar-sec/blob/main/docs/source/_templates/autosummary/attribute.rst)
  - [class.rst](https://github.com/nikhilxsunder/edgar-sec/blob/main/docs/source/_templates/autosummary/class.rst)
  - [method.rst](https://github.com/nikhilxsunder/edgar-sec/blob/main/docs/source/_templates/autosummary/method.rst)
- Added sphinx dependencies:
  - [sphinxext-opengraph](https://pypi.org/project/sphinxext-opengraph/)
  - [sphinx-design](https://pypi.org/project/sphinx_design/)
- Added [robots.txt](https://github.com/nikhilxsunder/edgar-sec/blob/main/docs/source/robots.txt)
- Added [sync_about_version.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/scripts/sync_about_version.py)
- Added [sync_conda_forge_version.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/scripts/sync_conda_forge_version.py)
- Added [sync_conf_version.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/scripts/sync_conf_version.py)
- Added [**about**.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/src/edgar_sec/__about__.py)
- Added [helpers.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/src/edgar_sec/helpers.py)
- Added complete test suite:
  - [clients_test.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/tests/clients_test.py)
  - [objects_test.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/tests/objects_test.py)
  - [helpers_test.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/tests/helpers_test.py)
- Markdown documents added:
  - [DCO.md](https://github.com/nikhilxsunder/edgar-sec/blob/main/DCO.md)
  - [ROADMAP.md](https://github.com/nikhilxsunder/edgar-sec/blob/main/ROADMAP.md)
- Added security analysis through [Socket](https://socket.dev/pypi/package/edgar-sec/overview)

### Fixed

- Fixed dependency list in [sync_conda_recipe.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/scripts/sync_conda_recipe.py)
- Fixed return objects in [objects.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/src/edgar_sec/objects.py)
- Fixed caching implementations in [clients.py](https://github.com/nikhilxsunder/edgar-sec/blob/main/src/edgar_sec/clients.py)
- Achieved OpenSSF Gold
- Achieved 100% test coverage on [Codecov](https://app.codecov.io/gh/nikhilxsunder/edgar-sec)

### Removed

- Deleted update_feedstock.py
- Deleted type stub files:
  - edgar_data.pyi
  - edgar_sec.pyi

## [1.0.1] - 2025-03-21

### Fixed

- Minor patch for publishing error (Anaconda)

## [1.0.0] - 2025-03-21

### Added

- EdgarAPI class for interacting with SEC EDGAR API
- Full async support through EdgarAPI.Async
- Data classes for structured responses
- Built-in caching using cachetools
- Rate limiting to comply with SEC's 10 requests/second guideline
- Type stubs (edgar_sec.pyi, edgar_data.pyi)
- Comprehensive test suite
- GitHub Actions workflows:
  - Analyze (linting, type checking)
  - CodeQL (security scanning)
  - Tests and Coverage
  - Documentation build and deploy
- Documentation: QuickStart, API Reference, Examples
- GPG signing for package releases
- Security policy and contribution guidelines
- Sphinx documentation structure
- Test coverage reporting in GitHub Actions
- Anaconda Distribution

### Changed

- Updated project structure to use Poetry for dependency management
- Improved error handling for API requests
- Enhanced documentation with real-world examples

## [0.0.2] - 2025-02-10

### Added

- Initial project structure
- Basic EdgarAPI class
- Simple configuration for API requests
- Initial README and documentation
- GitHub repository setup
- First working prototype for SEC EDGAR API interaction

## [0.0.1] - 2025-02-09

### Added

- Project initialization
- License file
- Basic package configuration
- Initial directory structure

[Unreleased]: https://github.com/nikhilxsunder/edgar-sec/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/nikhilxsunder/edgar-sec/compare/v1.0.1...v2.0.0
[1.0.1]: https://github.com/nikhilxsunder/edgar-sec/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/nikhilxsunder/edgar-sec/compare/v0.0.2...v1.0.0
[0.0.2]: https://github.com/nikhilxsunder/edgar-sec/compare/v0.0.1...v0.0.2
