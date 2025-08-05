### Roadmap

The following outlines the planned development trajectory for the edgar-sec project over the next year:

1. **Short-Term Goals (Next 3–6 Months):**
   - Achieve 100% test coverage across all modules.
   - Refactor and expand documentation with updated usage examples, async workflows, and real-world EDGAR scenarios.
   - Improve error handling and user-facing exceptions for common edge cases (e.g., malformed CIKs, rate limits).

2. **Mid-Term Goals (6–12 Months):**
   - Add support for time series construction from XBRL filings using intelligent tag mapping and reconciliation.
   - Integrate polars and dask for scalable dataframe outputs.
   - Implement local caching and incremental diff-based updates for repeat filing lookups.

3. **Long-Term Goals (Beyond 12 Months):**
   - Build a web-based explorer for EDGAR filings powered by the edgar-sec backend.
   - Support multi-language bindings (e.g., R, Julia) via FFI or REST interface.
   - Explore integration with LLM agents and economic copilots for AI-assisted filing analysis.

This roadmap is dynamic and may evolve based on community feedback, regulatory changes, or ecosystem opportunities.
