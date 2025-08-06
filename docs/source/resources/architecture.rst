.. _architecture:

Internal Architecture
=====================

Edgar-SEC is built to be modular, typed, and asynchronous-ready, designed for scalable, secure interaction with the SEC EDGAR® API.

This page outlines the internal client structure, core mechanisms, and the design philosophy guiding Edgar-SEC.

---

Class Hierarchy Overview
------------------------

.. dropdown:: Expand Class Hierarchy
    :color: secondary

    - :class:`edgar_sec.EdgarAPI` (main sync client)

    - :class:`edgar_sec.AsyncAPI` (async client variant)

    ➤ Call EdgarAPI().Async to access async methods for each endpoint.➤ Use edgar_sec.EdgarHelpers for static utility helpers like CIK resolution.

See :ref:`api-overview` for endpoint-specific breakdowns.

---

Key Internal Mechanisms
-----------------------

.. grid::
    :gutter: 2

    .. grid-item-card:: Rate Limiting
        :link-alt: SEC API Rate Limits

        Enforces EDGAR's safe usage limits using a timestamp-based limiter.
        Prevents accidental denial-of-service and burst requests.

    .. grid-item-card:: Retry Strategy
        :link-alt: Request Retry Logic

        Automatic retry on network failures via `tenacity` with exponential backoff.
        Applies to all sync and async endpoints.

    .. grid-item-card:: Local File Caching
        :link-alt: Response Caching

        File-based FIFO cache system stores successful responses.
        Enabled via `cache_mode=True` and configurable with `cache_size`.

    .. grid-item-card:: Asynchronous Engine
        :link-alt: Async Design

        Fully async using `httpx.AsyncClient` + `asyncio.Lock`.
        Supports concurrent SEC submission fetches with minimal blocking.

    .. grid-item-card:: Structured Dataclasses
        :link-alt: Typed Result Models

        All endpoints return structured, type-safe objects like:

        - :class:`edgar_sec.objects.SubmissionHistory`
        - :class:`edgar_sec.objects.CompanyConcept`
        - :class:`edgar_sec.objects.CompanyFacts`
        - :class:`edgar_sec.objects.Frame`

        Enforces safe unpacking, IDE integration, and schema reliability.

    .. grid-item-card:: Helper Utilities
        :link-alt: Input Coercion and Validation

        Parameter conversion, type coercion, and validation handled through shared static methods.
        Ensures consistent behavior between sync and async clients.

---

Design Philosophy
-----------------

.. dropdown:: Principles Behind the Package
    :color: primary

    - **Type-Safe**: Uses Python :class:`dataclasses.dataclass` models for every response.

    - **Async-Ready**: Fully asynchronous client with sync fallback.

    - **Performant**: Built-in caching, retry logic, and minimal overhead.

    - **Robust**: Validates inputs and ensures graceful failure modes.

    - **Developer-Oriented**: Concise naming, inline docs, static typing, and modern architecture.

---

Related Topics
----------------

.. grid::
    :gutter: 2

    .. grid-item-card:: Full API Reference
        :link: api-index
        :link-type: ref
        :link-alt: API Index

        Documentation for every function, model, and endpoint.

    .. grid-item-card:: Quick Start Guide
        :link: quickstart
        :link-type: ref
        :link-alt: Quickstart

        Install and run sync or async data pipelines in seconds.

    .. grid-item-card:: Advanced Usage
        :link: advanced-usage
        :link-type: ref
        :link-alt: Async and Caching

        Learn to chain async requests, apply caching, and debug errors.

    .. grid-item-card:: API Overview
        :link: api-overview
        :link-type: ref
        :link-alt: API Structure

        Understand how Edgar-SEC organizes methods, helpers, and classes.
