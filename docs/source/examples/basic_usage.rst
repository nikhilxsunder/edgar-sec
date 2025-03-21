Basic Usage Examples
====================

This section provides basic examples of how to use the `edgar-sec` library to interact with the SEC EDGAR API.

Initializing the API Client
---------------------------

To use the `edgar-sec` library, you first need to initialize the API client. No API key is required.

.. code-block:: python

    import edgar_sec as ed

    # Initialize the API client with caching enabled
    edgar = ed.EdgarAPI(cache_mode=True)

Fetching Company Submission History
-----------------------------------

You can fetch a company's submission history using the `get_submissions` method with the company's Central Index Key (CIK).

.. code-block:: python

    # Fetch submission history for Apple Inc.
    cik = "0000320193"  # Apple Inc. CIK
    submissions = edgar.get_submissions(central_index_key=cik)

    # Display company information
    print(f"Company Name: {submissions.name}")
    print(f"Ticker(s): {submissions.tickers}")
    print(f"Exchange(s): {submissions.exchanges}")

    # Display recent filings
    for filing in submissions.filings:
        print(f"Form: {filing.form}, Filed: {filing.filing_date}")

Getting Company Concept Disclosures
-----------------------------------

You can fetch specific financial concept disclosures using the `get_company_concept` method.

.. code-block:: python

    # Fetch Accounts Payable information for Apple Inc.
    concept = edgar.get_company_concept(
        central_index_key="0000320193",  # Apple Inc.
        taxonomy="us-gaap",              # US GAAP accounting standards
        tag="AccountsPayableCurrent"     # Accounts Payable concept
    )

    # Display concept information
    print(f"Concept: {concept.label}")
    print(f"Description: {concept.description}")

    # Display concept values
    for unit in concept.units:
        print(f"Value: {unit.val}, Period: {unit.end}, Form: {unit.form}")

Working with Company Facts
--------------------------

You can fetch all financial facts for a company using the `get_company_facts` method.

.. code-block:: python

    # Fetch all facts for Apple Inc.
    company_facts = edgar.get_company_facts(central_index_key="0000320193")

    # Display available taxonomies
    print(f"Available taxonomies: {list(company_facts.facts.keys())}")

    # Access a specific concept in the us-gaap taxonomy
    if "us-gaap" in company_facts.facts:
        us_gaap = company_facts.facts["us-gaap"]

        # Check if Revenue concept exists
        if "Revenue" in us_gaap.disclosures:
            revenue = us_gaap.disclosures["Revenue"]

            print(f"Revenue Label: {revenue.label}")
            print(f"Revenue Description: {revenue.description}")

            # Access values in USD
            if "USD" in revenue.units:
                for fact in revenue.units["USD"][:5]:  # First 5 disclosures
                    print(f"FY{fact.fy} {fact.fp}: ${fact.val:,}")

Exploring Frames
----------------

You can explore financial data across multiple companies for the same concept and time period using the `get_frames` method.

.. code-block:: python

    # Get Accounts Payable data for Q1 2023 across companies
    frame = edgar.get_frames(
        taxonomy="us-gaap",                 # US GAAP accounting standards
        tag="AccountsPayableCurrent",       # Accounts Payable concept
        unit="USD",                         # US dollars
        period="CY2023Q1I"                  # Calendar Year 2023, Q1, Instantaneous
    )

    # Display frame information
    print(f"Concept: {frame.label}")
    print(f"Description: {frame.description}")
    print(f"Total companies reporting: {frame.pts}")

    # Display data for the first 5 companies
    for disclosure in frame.frames[:5]:
        print(f"{disclosure.entity_name}: ${disclosure.val:,}")

Using Async Methods
-------------------

The library provides async versions of all methods for use in asynchronous contexts.

.. code-block:: python

    import asyncio
    import edgar_sec as ed

    async def main():
        # Initialize the API client
        edgar = ed.EdgarAPI(cache_mode=True)

        # Fetch multiple resources concurrently
        cik = "0000320193"  # Apple Inc.

        tasks = [
            edgar.Async.get_submissions(central_index_key=cik),
            edgar.Async.get_company_concept(
                central_index_key=cik,
                taxonomy="us-gaap",
                tag="Revenue"
            ),
            edgar.Async.get_company_concept(
                central_index_key=cik,
                taxonomy="us-gaap",
                tag="NetIncomeLoss"
            )
        ]

        submissions, revenue, net_income = await asyncio.gather(*tasks)

        print(f"Company: {submissions.name}")
        print(f"Revenue concept: {revenue.label}")
        print(f"Net Income concept: {net_income.label}")

        if revenue.units and len(revenue.units) > 0:
            latest_revenue = revenue.units[0]
            print(f"Latest Revenue (FY{latest_revenue.fy} {latest_revenue.fp}): ${latest_revenue.val:,}")

        if net_income.units and len(net_income.units) > 0:
            latest_income = net_income.units[0]
            print(f"Latest Net Income (FY{latest_income.fy} {latest_income.fp}): ${latest_income.val:,}")

    # Run the async function
    asyncio.run(main())
