.. _quickstart:

Quick Start Guide
=================

Get started with edgar-sec, a modern Python client for the SEC EDGAR® API. This guide walks you through installation, client setup, fetching filings, handling asynchronous workflows, and working with typed models.

---

Getting Started

No authentication key is required to use the EDGAR public API.
Just install the package and start querying data.

Install edgar-sec using pip or conda (see :ref:`installation` for more options).

.. tab-set::

   .. tab-item:: Synchronous Usage

      .. code-block:: python

         import edgar_sec as ed

         edgar = ed.EdgarAPI()

         # Fetch company filings by CIK
         submission_history = edgar.get_submissions(cik="0000320193")
         print(submission_history.filings)

   .. tab-item:: Asynchronous Usage

       .. code-block:: python

         import edgar_sec as ed
         import asyncio

         async def main():
             edgar = ed.EdgarAPI().Async
             submission_history = await edgar.get_submissions(cik="0000320193")
             print(submission_history.filings)

         asyncio.run(main())

---

Working with Models
-------------------

All responses are returned as strongly typed Python dataclasses:

.. code-block:: python

   import edgar_sec as ed
   edgar = ed.EdgarAPI()
   submission_history = edgar.get_submissions(cik="0000320193")
   print(submission_history.filings)
   print(submission_history.filings[0].filing_date)

Models include:

- :class:`edgar_sec.objects.Address`
- :class:`edgar_sec.objects.FormerName`
- :class:`edgar_sec.objects.File`
- :class:`edgar_sec.objects.Filing`
- :class:`edgar_sec.objects.SubmissionHistory`
- :class:`edgar_sec.objects.UnitDisclosure`
- :class:`edgar_sec.objects.CompanyConcept`
- :class:`edgar_sec.objects.TaxonomyDisclosures`
- :class:`edgar_sec.objects.TaxonomyFacts`
- :class:`edgar_sec.objects.CompanyFacts`
- :class:`edgar_sec.objects.FrameDisclosure`
- :class:`edgar_sec.objects.Frame`
- :class:`edgar_sec.objects.Company`

---

Searching for Filings
---------------------

You can search filings using CIK, ticker, or company name:

.. code-block:: python

   import edgar_sec as ed

   edgar = ed.EdgarAPI()

   # Get submission history by ticker
   submission_history = edgar.get_submissions(ticker="AAPL", type="10-Q")

   # Search for a company's CIK by name substring
   results = ed.EdgarHelpers.get_cik(search="Tesla")

   for match in results:
      print(match.name, match.cik)

---

Caching and Rate Limiting
-------------------------

edgar-sec includes built-in file caching and throttling:

.. code-block:: python

   import edgar_sec as ed

   edgar = ed.EdgarAPI(cache=True, cache_size=500)

   # Caching avoids repeated calls to the same endpoint.

---

What's Next?
^^^^^^^^^^^^

.. grid-item-card:: Full API Reference
    :link: api-index
    :link-type: ref
    :link-alt: API Index

    Learn how to use every endpoint and object class.

.. grid-item-card:: Advanced Usage
    :link: advanced-usage
    :link-type: ref
    :link-alt: Advanced Usage Examples

    Dive into async pipelines, batching, and raw request tuning.

.. grid-item-card:: Parameter Docs
    :link: api-notes
    :link-type: ref
    :link-alt: API Parameter Conversion Notes

    Understand how edgar-sec resolves and validates parameters.

.. grid-item-card:: Contributing Guide
    :link: contributing
    :link-type: ref
    :link-alt: Dev Setup Docs

    Help improve the project — or fork it for your stack.
