# Changelog

All notable changes to edgar-sec will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Property-based testing framework

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

[Unreleased]: https://github.com/nikhilxsunder/edgar-sec/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/nikhilxsunder/edgar-sec/compare/v0.0.2...v1.0.0
[0.0.2]: https://github.com/nikhilxsunder/edgar-sec/compare/v0.0.1...v0.0.2
