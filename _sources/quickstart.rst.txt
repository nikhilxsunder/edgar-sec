Quick Start Guide
=================

Getting Started
---------------

The edgar-sec package provides a feature-rich interface to interact with the U.S. Securities and Exchange Commission's EDGAR API. No API key is required.

Basic Usage
-----------

.. code-block:: python

    import edgar_sec as ed

    # Initialize the API client
    edgar = ed.EdgarAPI(cache_mode=True)

    # Get company submission history (recent filings)
    submissions = edgar.get_submissions(central_index_key='0000320193')  # Apple Inc.

    # Access company information
    print(f"Company Name: {submissions.name}")
    print(f"Ticker: {submissions.tickers}")

    # Access recent filings
    for filing in submissions.filings:
        print(f"Form: {filing.form}, Filed: {filing.filing_date}")

    # Get company concept disclosures
    company_concept = edgar.get_company_concept(
        central_index_key='0000320193',
        taxonomy='us-gaap',
        tag='AccountsPayableCurrent'
    )

    # Access the concept data
    print(f"Concept: {company_concept.label}")
    print(f"Description: {company_concept.description}")

    # Access individual disclosures
    for unit in company_concept.units:
        print(f"Value: {unit.val}, Period: {unit.end}, Form: {unit.form}")

Async Usage
-----------

edgar-sec provides native support for asynchronous requests, allowing you to efficiently fetch data in an asynchronous environment.

.. code-block:: python

    import asyncio
    import edgar_sec as ed

    async def main():
        # Initialize the API client
        edgar = ed.EdgarAPI(cache_mode=True)

        # Get company concept disclosures asynchronously
        company_concept = await edgar.Async.get_company_concept(
            central_index_key='0000320193',
            taxonomy='us-gaap',
            tag='AccountsPayableCurrent'
        )

        print(f"Concept: {company_concept.label}")

        # Fetch multiple resources concurrently
        tasks = [
            edgar.Async.get_company_concept('0000320193', 'us-gaap', 'Revenue'),
            edgar.Async.get_company_concept('0000320193', 'us-gaap', 'NetIncomeLoss'),
            edgar.Async.get_company_facts('0000320193')
        ]
        concepts_and_facts = await asyncio.gather(*tasks)

        # Process results
        revenue_concept, income_concept, company_facts = concepts_and_facts
        print(f"Revenue: {revenue_concept.label}")
        print(f"Net Income: {income_concept.label}")

    # Run the async function
    asyncio.run(main())

Working with Company Facts
--------------------------

Get all facts for a company in a single request:

.. code-block:: python

    # Get all facts for a company
    company_facts = edgar.get_company_facts(central_index_key='0000320193')

    # Explore available taxonomies
    for taxonomy in company_facts.facts:
        print(f"Taxonomy: {taxonomy}")

    # Access specific concepts from a taxonomy
    if 'us-gaap' in company_facts.facts:
        us_gaap = company_facts.facts['us-gaap']

        # Access a specific disclosure
        if 'Revenue' in us_gaap.disclosures:
            revenue = us_gaap.disclosures['Revenue']

            # Print information about the disclosure
            print(f"Label: {revenue.label}")
            print(f"Description: {revenue.description}")

            # Access values in different units
            if 'USD' in revenue.units:
                for fact in revenue.units['USD']:
                    print(f"Fiscal Year: {fact.fy}, Period: {fact.fp}, Value: {fact.val}")

Working with Frames
-------------------

Frames allow you to retrieve cross-sectional data for a specific concept across multiple companies:

.. code-block:: python

    # Get a specific frame disclosure
    frame_disclosure = edgar.get_frames(
        taxonomy='us-gaap',
        tag='AccountsPayableCurrent',
        unit='USD',
        period='CY2022Q1I'
    )

    # Access the frame data
    print(f"Concept: {frame_disclosure.label}")
    print(f"Total companies reporting: {frame_disclosure.pts}")

    # Examine individual company disclosures
    for i, company in enumerate(frame_disclosure.frames[:5]):  # First 5 companies
        print(f"{company.entity_name}: ${company.val}")

Caching and Rate Limits
-----------------------

edgar-sec includes built-in caching and rate limiting:

.. code-block:: python

    # Initialize client with caching enabled
    edgar = ed.EdgarAPI(cache_mode=True)

    # The first call to an endpoint makes an API request
    company_facts1 = edgar.get_company_facts("0000320193")

    # Subsequent calls within the cache period return cached data (faster)
    company_facts2 = edgar.get_company_facts("0000320193")  # Uses cache

    # Rate limiting is handled automatically to comply with SEC's 10 requests/second limit

Common CIKs for Examples
-----------------------

Some common Central Index Keys (CIKs) for examples:

- Apple Inc: 0000320193
- Microsoft Corporation: 0000789019
- Amazon.com, Inc: 0001018724
- Alphabet Inc (Google): 0001652044
- Tesla, Inc: 0001318605
- Walmart Inc: 0000104169
- JPMorgan Chase & Co: 0000019617
