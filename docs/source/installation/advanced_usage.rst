.. _advanced-usage:

Advanced Usage Examples
=======================

edgar-sec enables high-performance, robust access to SEC EDGAR data pipelines. This page covers caching, rate limiting, async concurrent requests, parameter control, and error handling.

---

Advanced Client Features
------------------------

.. grid::
    :gutter: 2

    .. grid-item-card:: Caching and Rate Limiting
        :columns: 4
        :link: #caching-and-rate-limiting
        :link-alt: Caching and rate limiting documentation

        Cache responses and throttle API usage to maximize throughput.

    .. grid-item-card:: Async Concurrent Requests
        :columns: 4
        :link: #concurrent-requests-with-async
        :link-alt: Asynchronous concurrent fetches

        Use the Async client to batch multiple EDGAR requests in parallel.

    .. grid-item-card:: Custom API Requests
        :columns: 4
        :link: #customizing-api-requests
        :link-alt: Customizing API requests

        Control filtering, document types, and pagination with ease.

    .. grid-item-card:: Error Handling
        :columns: 4
        :link: #error-handling-and-validation
        :link-alt: Error and exception handling

        Capture and debug common EDGAR edge cases and input errors.

---

Caching and Rate Limiting
-------------------------
