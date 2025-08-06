.. _comparison:

Comparison with Other SEC EDGAR Clients
=======================================

edgar-sec is a modern, typed, and async-compatible alternative to existing Python clients for the SEC EDGAR® API.
Below is a side-by-side comparison highlighting key differences.

---

Feature Comparison Table

+-------------------------+-------------------+----------------------+------------------+
| Feature                 | edgar-sec         | sec-edgar-downloader | sec-api-python   |
+=========================+===================+======================+==================+
| Async Support           | Yes               | No                   | No               |
+-------------------------+-------------------+----------------------+------------------+
| Caching                 | Yes (file-based)  | No                   | No               |
+-------------------------+-------------------+----------------------+------------------+
| Rate Limiting           | Yes               | No                   | No               |
+-------------------------+-------------------+----------------------+------------------+
| Typed Models            | Yes               | No                   | No               |
+-------------------------+-------------------+----------------------+------------------+
| Error Handling          | Yes               | No                   | Limited          |
+-------------------------+-------------------+----------------------+------------------+
| CIK/Ticker Resolution   | Yes               | Manual CSV           | Manual Lookup    |
+-------------------------+-------------------+----------------------+------------------+
| Documentation Quality   | Full Sphinx       | Minimal              | Basic            |
+-------------------------+-------------------+----------------------+------------------+
| License                 | AGPL              | MIT                  | MIT              |
+-------------------------+-------------------+----------------------+------------------+

---

Key Differences Explained

.. dropdown:: Async Support
    :color: secondary

    edgar-sec uses `httpx.AsyncClient` and supports async methods natively via `.Async`, allowing concurrent submissions, filings, and concept retrieval.

.. dropdown:: Built-in Caching + Throttling
    :color: secondary

    No need to externally install rate-limiters or memcache — `edgar-sec` includes file-based caching and timestamp-driven request throttling.

.. dropdown:: Typed Dataclass Models
    :color: secondary

    Returns objects like :class:`edgar_sec.objects.Filing` or :class:`edgar_sec.objects.CompanyFacts`, enabling auto-completion and schema validation in IDEs.

.. dropdown:: Helper Utilities
    :color: secondary

    `EdgarHelpers.get_cik(...)` simplifies ticker/company lookups without manual CSVs or web scraping.

.. dropdown:: Designed for Developers
    :color: secondary

    Clear docs, async + sync parity, typed responses, built-in error messaging, and modular architecture make edgar-sec ideal for robust systems.


---

Summary
-------

edgar-sec is the most complete and developer-friendly choice for:

- SEC data pipelines
- Filing history monitoring
- Financial modeling workflows
- High-frequency document ingestion

It embraces modern Python: asyncio, dataclasses, httpx, and tenacity — with a complete test suite and Sphinx docs.

➔ Check real-world examples in :ref:use-cases.
➔ Explore the internal structure at :ref:architecture.

---

Related Topics
--------------

.. grid::
    :gutter: 2

    .. grid-item-card:: Full API Reference
        :link: api-index
        :link-type: ref
        :link-alt: API Index

        View all available methods, endpoints, and data models.

    .. grid-item-card:: Quick Start Tutorial
        :link: quickstart
        :link-type: ref
        :link-alt: Quick Start

        Fetch filings or submissions in just a few lines of code.

    .. grid-item-card:: Advanced Usage Examples
        :link: advanced-usage
        :link-type: ref
        :link-alt: Async + Caching

        Learn how to use caching, batching, and async requests with edgar-sec.
