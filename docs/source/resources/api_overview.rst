.. _api-overview:

Edgar-SEC API Overview
======================

Edgar-SEC provides a modular, typed client interface for interacting with the SEC EDGAR® API, supporting both synchronous and asynchronous workflows with a consistent dataclass model layer.

This page summarizes the main client components, supported endpoints, and enhanced runtime features.

---

Client Architecture
-------------------

.. dropdown:: Expand Client Class Hierarchy
    :color: secondary

    - :class:`edgar_sec.EdgarAPI` - Unified synchronous client

      - :class:`edgar_sec.AsyncAPI` - Asynchronous client wrapper

    Each interface shares a common internal design:

    :meth:`edgar_sec.EdgarAPI.get_submissions` → synchronous

    :meth:`edgar_sec.AsyncAPI.get_submissions` → asynchronous

    Each class is accessed as an attribute:

    - :attr:`edgar_sec.EdgarAPI.Async` → instance of the asynchronous client (:class:`edgar_sec.AsyncAPI`)

    Helpers are exposed via :class:`edgar_sec.EdgarHelpers` for common tasks like CIK lookups, pagination, and data validation.

    :meth:`edgar_sec.EdgarHelpers.get_cik` → CIK search (synchronous)
    :meth:`edgar_sec.EdgarHelpers.get_cik_async` → CIK search (asynchronous)

---

Client Capabilities
-------------------

.. grid::
    :gutter: 2

    .. grid-item-card:: Company Submissions
        Retrieve complete filing history and metadata for public companies by CIK or ticker.

    .. grid-item-card:: Filings
        Extract detailed filing data including accession numbers, document types, and report dates.

    .. grid-item-card:: Company Concepts
        Get standardized accounting disclosures and labels from XBRL submissions.

    .. grid-item-card:: Company Facts
        Parse historical fundamental metrics for key entities.

    .. grid-item-card:: Frames
        Explore cross-company time-sliced XBRL frames for a concept and period.

    .. grid-item-card:: CIK Lookups
        Resolve tickers and names to CIKs via helper utilities.

---

Enhanced API Features
---------------------

.. grid::
    :gutter: 2

    .. grid-item-card:: File-Based Caching
        Enable disk-backed caching of responses using `cache_mode=True` and `cache_size`.

    .. grid-item-card:: Retry & Timeout
        Robust retry logic with exponential backoff via `tenacity` for fault-tolerant requests.

    .. grid-item-card:: Built-In Rate Limiting
        Configurable per-minute limits prevent SEC throttling.

    .. grid-item-card:: Typed Dataclasses
        All responses are structured into typed Python objects like:

        - :class:`edgar_sec.objects.Filing`
        - :class:`edgar_sec.objects.SubmissionHistory`
        - :class:`edgar_sec.objects.Company`
        - :class:`edgar_sec.objects.CompanyFacts`

    .. grid-item-card:: Async Compatibility
        Native `async` interface supports concurrent submission retrieval and scalable batch jobs.

---

Related Topics
--------------

.. grid::
    :gutter: 2

    .. grid-item-card:: Full API Reference
        :link: api-index
        :link-type: ref
        :link-alt: API Index

        View complete documentation for every method and model.

    .. grid-item-card:: Quick Start Guide
        :link: quickstart
        :link-type: ref
        :link-alt: Quickstart Tutorial

        Learn how to initialize, query, and explore SEC filings in minutes.

    .. grid-item-card:: Async & Caching Examples
        :link: advanced-usage
        :link-type: ref
        :link-alt: Advanced Usage Examples

        Explore concurrency patterns, retries, and caching in production.

    .. grid-item-card:: Architecture Overview
        :link: architecture
        :link-type: ref
        :link-alt: Internal Design & Structure

        Understand how edgar-sec is structured internally and how components interact.
