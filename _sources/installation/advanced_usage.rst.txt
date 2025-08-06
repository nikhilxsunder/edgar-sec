.. _advanced-usage:

Advanced Usage Examples
=======================

edgar-sec enables **high-throughput**, **resilient** EDGAR® data pipelines.
This page covers **file caching**, **rate limiting**, **concurrent async requests**, **parameter customization**, and **error handling**.

---

Advanced Client Features
-------------------------

.. grid::
    :gutter: 2

    .. grid-item-card:: Caching and Rate Limiting
        :columns: 4
        :link: #caching-and-rate-limiting
        :link-alt: Caching and rate limiting documentation

        Automatically cache responses and throttle API requests to comply with EDGAR limits.

    .. grid-item-card:: Async Concurrent Requests
        :columns: 4
        :link: #concurrent-requests-with-async
        :link-alt: Asynchronous requests using AsyncAPI

        Fetch multiple endpoints concurrently using :attr:`edgar_sec.EdgarAPI.Async`.

    .. grid-item-card:: Parameter Customization
        :columns: 4
        :link: #customizing-api-requests
        :link-alt: API parameter formatting

        Use datetime, list, and string inputs seamlessly with auto-conversion.

    .. grid-item-card:: Error Handling
        :columns: 4
        :link: #error-handling-and-validation
        :link-alt: Exception catching and validation

        Raise clear, typed exceptions for invalid inputs and failed requests.

---

Caching and Rate Limiting
-------------------------

.. dropdown:: See Example
    :color: primary
    :open:

    .. code-block:: python

        import edgar_sec as ed

        edgar = ed.EdgarAPI(cache_mode=True, cache_size=512)

        submission = edgar.get_submissions(ticker="MSFT")
        print(submission.entity_type)

        # Cached if repeated:
        filing = edgar.get_company_facts("AAPL")

edgar-sec enforces the **10 requests per second** SEC limit and supports **file-based caching**.

---

Concurrent Requests with Async
------------------------------

.. dropdown:: See Example
    :color: primary

    .. code-block:: python

        import edgar_sec as ed
        import asyncio

        async def fetch_all():
            edgar = ed.EdgarAPI().Async
            tickers = ["AAPL", "TSLA", "MSFT"]
            tasks = [edgar.get_submissions(ticker=t) for t in tickers]
            results = await asyncio.gather(*tasks)

            for result in results:
                print(result.name, len(result.filings))

        asyncio.run(fetch_all())

Perfect for **data collection pipelines** and **bulk processing**.

---

Customizing API Requests
-------------------------

.. dropdown:: See Example
    :color: secondary

    .. code-block:: python

        from datetime import datetime
        import edgar_sec as ed

        edgar = ed.EdgarAPI()
        frame = edgar.get_frames(
            taxonomy="us-gaap",
            tag="RevenueFromContractWithCustomerExcludingAssessedTax",
            unit="USD",
            period=datetime(2022, 3, 31),
            instantaneous=True
        )
        print(frame.data[0].entity_name, frame.data[0].val)

Use **datetime**, **CIKs**, or **tickers** — edgar-sec converts and validates them for you.

---

Error Handling and Validation
------------------------------

.. dropdown:: See Example
    :color: danger

    .. code-block:: python

        import edgar_sec as ed

        edgar = ed.EdgarAPI()

        try:
            edgar.get_submissions(ticker=None)
        except ValueError as e:
            print("Validation error:", e)

        try:
            edgar.get_company_concept("us-gaap", "InvalidTag", ticker="AAPL")
        except Exception as e:
            print("API error:", e)

Descriptive error messages help you debug quickly.

---

Related Resources
-----------------

.. grid::
    :gutter: 2
    :margin: 2 0 2 0

    .. grid-item-card:: API Notes
        :link: api-notes
        :link-type: ref
        :link-alt: API behavior notes

        Learn how edgar-sec handles parameter coercion and conversion.

    .. grid-item-card:: API Reference
        :link: api-index
        :link-type: ref
        :link-alt: edgar-sec API documentation

        Full documentation for all client methods and models.

    .. grid-item-card:: Use Cases
        :link: use-cases
        :link-type: ref
        :link-alt: Real-world usage

        Async pipelines, research workflows, document parsing, and more.
