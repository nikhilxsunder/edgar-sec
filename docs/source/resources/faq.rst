.. _faq:

Frequently Asked Questions (FAQ)
================================

Answers to the most common questions about edgar-sec, the modern Python client for the SEC EDGAR® API.

---

What is edgar-sec?

.. dropdown:: See Answer
    :color: secondary

    edgar-sec is a fully typed, async-capable, and performance-oriented Python SDK for working with the SEC EDGAR API.

    Highlights:

    - Synchronous and asynchronous access via EdgarAPI() and EdgarAPI().Async,
    - Structured @dataclass response models (e.g. Filing, CompanyFacts),
    - Built-in file caching and automatic retry/backoff with tenacity,
    - No API key or authentication required.

    ➔ See the :ref:`quickstart` for an example.

---

How does edgar-sec compare to other EDGAR clients?
--------------------------------------------------

.. dropdown:: See Answer
    :color: secondary

    Unlike legacy tools or scraping-based methods, edgar-sec provides:

    - True async support with httpx.AsyncClient
    - Structured typed models instead of raw JSON
    - Built-in caching + rate-limiting
    - Robust helper utilities (e.g. get_cik() search by name/ticker)
    - Extensive docs and test coverage

    ➔ See the detailed :ref:`comparison` for a breakdown.

---

Is caching supported?
---------------------

.. dropdown:: See Answer
    :color: secondary

    Yes — edgar-sec supports local file-based FIFO caching.

    - Configure via EdgarAPI(cache_mode=True, cache_size=1000)
    - Applies to both sync and async methods
    - Eliminates redundant requests and reduces bandwidth

    .. code-block:: python

        import edgar_sec as ed
        edgar = ed.EdgarAPI(cache_mode=True, cache_size=500)

    ➔ See :ref:`advanced-usage` for more.

---

Can I use edgar-sec asynchronously?
-----------------------------------

.. dropdown:: See Answer
    :color: secondary

    Yes — all endpoints have async equivalents using edgar = `EdgarAPI().Async`

    .. code-block:: python

        import edgar_sec as ed
        import asyncio

        async def main():
            edgar = ed.EdgarAPI().Async
            data = await edgar.get_submissions(ticker="AAPL")
            print(data.company_name)

        asyncio.run(main())

    Async support enables concurrent filing fetches and scalable automation.

---

What helper tools are included?

.. dropdown:: See Answer
    :color: secondary

    edgar-sec includes a built-in static helper:
        - :class:`edgar_sec.helpers.EdgarHelpers` contains utility methods like CIK resolution.

    .. code-block:: python

        import edgar_sec as ed

        results = ed.EdgarHelpers.get_cik(ticker="AAPL")
        print(results)


---

Related Topics

.. grid::
    :gutter: 2

    .. grid-item-card:: Quick Start Guide
        :link: quickstart
        :link-type: ref
        :link-alt: edgar-sec Quickstart

        Install, fetch submissions, and start working with typed results.

    .. grid-item-card:: Full API Documentation
        :link: api-index
        :link-type: ref
        :link-alt: API Reference

        Explore every method, parameter, and dataclass object.

    .. grid-item-card:: Example Projects
        :link: use-cases
        :link-type: ref
        :link-alt: edgar-sec Use Cases

        Real-world pipelines and batch jobs using the edgar-sec SDK.

    .. grid-item-card:: Internal Architecture
        :link: architecture
        :link-type: ref
        :link-alt: Design Structure

        Understand the modular client layout and retry mechanisms.
