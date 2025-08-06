.. _use-cases:

Example Use Cases
=================

Edgar-SEC powers SEC filing dashboards, async data pipelines, compliance monitoring, and quantitative research using the official EDGAR® API.

Explore how to use Edgar-SEC in production systems, research environments, or data-driven applications:

---

Filing Dashboard Development
----------------------------

.. dropdown:: See Example
    :color: secondary
    :open:

    Combine edgar-sec with:

    - Pandas, Polars, or DuckDB for ETL workflows,
    - Plotly, Altair, or Matplotlib for visualizations,
    - Dash, Streamlit, or Gradio for deployment.

    Applications include:

    - Visualizing 10-K/10-Q form counts over time,
    - Monitoring submission patterns by sector,
    - Flagging outlier disclosures for review.

---

Asynchronous Ingestion Pipelines
--------------------------------

.. dropdown:: See Example
    :color: secondary

    Use edgar = ed.EdgarAPI().Async to run concurrent submission or concept fetches.

    Ideal for:

    - Daily batch jobs that refresh filings across hundreds of tickers,
    - Compliance systems for near real-time EDGAR intake,
    - Automating archival of fundamental metrics (XBRL facts).

    Built-in asyncio, retry logic, and throttling ensure reliability at scale.

---

CIK and Metadata Indexing
-------------------------

.. dropdown:: See Example
    :color: secondary

    Use EdgarHelpers.get_cik(...) to build searchable lookup tools or name→CIK mappings.

    - Index all S&P 500 company CIKs,
    - Normalize common entity name aliases,
    - Build autocomplete tools for research dashboards.

    This avoids scraping or manual CSV management.

---

Fundamental Disclosure Analysis
-------------------------------

.. dropdown:: See Example
    :color: secondary

    Retrieve and structure XBRL data with:

    - get_company_facts()
    - get_company_concepts()
    - get_frames()

    Research workflows include:

    - Comparing debt-to-equity ratios across firms,
    - Tracking reported vs restated earnings over time,
    - Building real-time disclosure-based models.

---

Related Resources
-----------------

.. grid::
    :gutter: 2

    .. grid-item-card:: Full API Documentation
        :link: api-index
        :link-type: ref
        :link-alt: edgar-sec Full API Reference

        Explore all endpoints, object models, and helper utilities.

    .. grid-item-card:: Quick Start Guide
        :link: quickstart
        :link-type: ref
        :link-alt: Quick Start for edgar-sec

        Learn how to fetch SEC data in under five lines of code.

    .. grid-item-card:: Parameter Handling
        :link: api-notes
        :link-type: ref
        :link-alt: Parameter Notes

        Understand how date, type, and ID conversions work.

    .. grid-item-card:: Advanced Usage
        :link: advanced-usage
        :link-type: ref
        :link-alt: Advanced Examples

        Async, batching, caching, and retry-enabled ingestion pipelines.
