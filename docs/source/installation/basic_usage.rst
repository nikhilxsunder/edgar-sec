.. _basic-usage:

Basic Usage Examples
=====================

This page shows how to quickly start using the :mod:`edgar_sec` package to interact with the **SEC EDGAR® API**.
You'll learn how to **initialize a client**, **fetch submission history**, **extract XBRL facts**, and **look up tickers or CIKs**.

If you're new to edgar-sec, start here!

---

Getting Started
---------------

.. grid::
   :gutter: 2

   .. grid-item-card:: Initialize the Client

      .. code-block:: python

         import edgar_sec as ed
         edgar = ed.EdgarAPI()

      No API key needed — EDGAR data is public.
      See :ref:`advanced-usage` for async and caching options.

   .. grid-item-card:: Fetch Submission History

      .. code-block:: python

         submission_history = edgar.get_submissions(ticker="AAPL")
         print(submission_history.filings[0].form, submission_history.filings[0].filing_date)

      Retrieve the last 1,000+ SEC filings for a company.
      Returns a :class:`edgar_sec.objects.SubmissionHistory` object.

   .. grid-item-card:: Fetch Company XBRL Facts

      .. code-block:: python

         facts = edgar.get_company_facts(ticker="AAPL")
         revenue = facts.facts["us-gaap"].disclosures.get("RevenueFromContractWithCustomerExcludingAssessedTax")
         if revenue and "USD" in revenue.units:
             print(f"Latest revenue: ${revenue.units['USD'][0].val}")

      Load all tagged XBRL disclosures for a company.
      Access structured concepts via taxonomy and tag.

   .. grid-item-card:: Get Company Concept

      .. code-block:: python

         concept = edgar.get_company_concept(
             taxonomy="us-gaap",
             tag="Assets",
             ticker="MSFT"
         )
         print(concept.units[0].val)

      Query a specific financial disclosure (e.g. Assets, Liabilities).

---

Helper Utilities
----------------

.. dropdown:: Convert Ticker to CIK
   :color: secondary
   :open:

   .. code-block:: python

      results = ed.EdgarHelpers.get_cik(search="Tesla")
      for match in results:
         print(match.name, match.cik)

   Returns list of :class:`edgar_sec.objects.Company` matches.
   Useful for mapping names or tickers to official identifiers.

.. dropdown:: Validate and Convert Period Strings
   :color: secondary
   :open:

   .. code-block:: python

      from datetime import datetime
      from edgar_sec.helpers import EdgarHelpers

      period = EdgarHelpers.datetime_cy_conversion(datetime(2022, 3, 1))
      print(period)  # CY2022Q1

   Used to construct correct period identifiers for frame queries.

---

Related Resources
-----------------

.. grid::
   :gutter: 2

   .. grid-item-card:: Advanced Usage
      :link: advanced-usage
      :link-type: ref
      :link-alt: Advanced Usage Documentation

      Learn about async clients, batching, caching, and retries.

   .. grid-item-card:: Full API Reference
      :link: api-index
      :link-type: ref
      :link-alt: Complete Edgar-SEC API Reference

      Detailed docs for all methods, models, and endpoints.

   .. grid-item-card:: Parameter Conversion Guide
      :link: api-notes
      :link-type: ref
      :link-alt: Automatic Parameter Conversion

      Understand how edgar-sec validates and transforms arguments.
