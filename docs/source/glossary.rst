.. _glossary:

Glossary
========

.. glossary::

    async
        Short for asynchronous programming in Python, allowing non-blocking execution using the ``asyncio`` event loop.
        Used in :mod:`edgar-sec` to fetch EDGAR data concurrently and efficiently.

    cache mode
        A configuration flag in :mod:`edgar-sec` that enables file-based local caching of SEC API responses.
        Reduces latency and avoids repeated downloads of the same data.

    caching
        The practice of storing API responses locally to avoid redundant network calls.
        In :mod:`edgar-sec`, caching is FIFO-based and works across both sync and async clients.

    CIK
        Central Index Key — a unique 10-digit identifier for registrants at the SEC.
        Used to query filings, submissions, and XBRL data.
        See also: :class:`edgar_sec.helpers.EdgarHelpers.get_cik`.

    dataclass
        A Python class decorated with :class:`dataclasses.dataclass` to store structured response objects.
        All EDGAR objects (e.g. :class:`edgar_sec.objects.Filing`, :class:`edgar_sec.objects.CompanyConcept`) in :mod:`edgar-sec` are returned as typed dataclasses.

    rate limiting
        The process of controlling the frequency of API requests.
        :mod:`edgar-sec` enforces a 10-requests-per-second limit for compliance with the SEC's guidelines.

    retry strategy
        A mechanism for automatically re-trying failed requests (e.g., network issues).
        :mod:`edgar-sec` uses `tenacity` with exponential backoff to recover from transient failures.

    submission
        A formal document submitted to the SEC by a company or issuer.
        Includes filings like 10-K, 10-Q, 8-K, etc., and is retrieved using :meth:`edgar_sec.EdgarAPI.get_submissions`.

    filing
        A specific report submitted to the SEC by a registrant, such as a 10-K or 8-K.
        Modeled as :class:`edgar_sec.objects.Filing` in the API response.

    taxonomy
        A standardized classification system (e.g., ``us-gaap``, ``ifrs-full``) used in XBRL filings.
        Required when querying XBRL endpoints like :meth:`edgar_sec.EdgarAPI.get_company_concept`.

    tag
        A disclosure label used in XBRL to identify a financial metric or fact (e.g., ``Assets``, ``NetIncomeLoss``).
        Used alongside taxonomy to extract company-specific or cross-sectional financial data.

    XBRL
        eXtensible Business Reporting Language — the XML-based format used for financial disclosures filed with the SEC.
        Accessible via endpoints like `companyconcept`, `companyfacts`, and `frames`.
