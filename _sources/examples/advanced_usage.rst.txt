Advanced Usage Examples
=======================

This section provides advanced usage examples for the `edgar-sec` library, including caching, rate limiting, concurrent requests, and sophisticated data extraction techniques.

Caching and Rate Limiting
-------------------------

The `edgar-sec` library includes built-in support for caching and rate limiting to optimize API usage and comply with SEC guidelines.

.. code-block:: python

    import edgar_sec as ed

    # Initialize the API client with caching enabled
    edgar = ed.EdgarAPI(cache_mode=True)

    # First request will hit the API
    apple_facts = edgar.get_company_facts("0000320193")
    print(f"Number of taxonomies: {len(apple_facts.facts)}")

    # Subsequent identical requests will use cache (much faster)
    apple_facts_cached = edgar.get_company_facts("0000320193")

    # The built-in rate limiter ensures you don't exceed 10 API calls per second
    # This is handled automatically for both synchronous and asynchronous requests
    for cik in ["0000320193", "0000789019", "0001652044", "0001018724", "0001326801"]:
        company = edgar.get_submissions(central_index_key=cik)
        print(f"Retrieved data for {company.name}")

Concurrent Requests with AsyncAPI
---------------------------------

You can use the `Async` attribute to make concurrent requests for improved performance.

.. code-block:: python

    import asyncio
    import edgar_sec as ed

    async def fetch_multiple_companies():
        edgar = ed.EdgarAPI(cache_mode=True)

        # Define company CIKs
        companies = {
            "0000320193": "Apple",      # Apple
            "0000789019": "Microsoft",  # Microsoft
            "0001652044": "Alphabet",   # Alphabet (Google)
            "0001018724": "Amazon",     # Amazon
            "0001326801": "Meta"        # Meta (Facebook)
        }

        # Fetch submission history for multiple companies concurrently
        submission_tasks = [
            edgar.Async.get_submissions(cik)
            for cik in companies.keys()
        ]
        submissions = await asyncio.gather(*submission_tasks)

        # Process the results
        for submission, name in zip(submissions, companies.values()):
            print(f"{name} ({submission.name}):")
            print(f"  Ticker: {submission.tickers}")
            print(f"  Recent filing: {submission.filings[0].form} on {submission.filings[0].filing_date}")
            print()

        # Now fetch the same concept across all companies
        concept_tasks = [
            edgar.Async.get_company_concept(cik, "us-gaap", "Assets")
            for cik in companies.keys()
        ]
        concepts = await asyncio.gather(*concept_tasks)

        # Compare assets across companies
        print("Total Assets Comparison:")
        for concept, name in zip(concepts, companies.values()):
            # Get the most recent USD disclosure if available
            if concept.units and hasattr(concept.units[0], 'val'):
                latest = concept.units[0]
                print(f"  {name}: ${latest.val:,} ({latest.fy} {latest.fp})")

    # Run the async function
    asyncio.run(fetch_multiple_companies())

Advanced Data Extraction
------------------------

Extract specific financial metrics from company facts for analysis.

.. code-block:: python

    import edgar_sec as ed
    import pandas as pd
    import matplotlib.pyplot as plt

    # Initialize the API client
    edgar = ed.EdgarAPI(cache_mode=True)

    # Fetch all Apple facts
    apple_facts = edgar.get_company_facts("0000320193")

    # Extract revenue time series
    if "us-gaap" in apple_facts.facts:
        # Look for various revenue concept tags (may vary by company)
        revenue_tags = [
            "Revenue",
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "SalesRevenueNet",
            "RevenueFromContractWithCustomer"
        ]

        # Find the first matching tag
        revenue_tag = next((tag for tag in revenue_tags if tag in apple_facts.facts["us-gaap"].disclosures), None)

        if revenue_tag and "USD" in apple_facts.facts["us-gaap"].disclosures[revenue_tag].units:
            # Extract revenue data
            revenue_data = []
            for fact in apple_facts.facts["us-gaap"].disclosures[revenue_tag].units["USD"]:
                # Only include annual (FY) or quarterly (Q1-Q4) data
                if fact.fp in ["FY", "Q1", "Q2", "Q3", "Q4"]:
                    revenue_data.append({
                        "period": f"{fact.fy} {fact.fp}",
                        "date": fact.end,
                        "revenue": fact.val,
                        "form": fact.form
                    })

            # Convert to DataFrame for analysis
            df = pd.DataFrame(revenue_data)
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date")

            # Only keep 10-K and 10-Q reports
            df = df[df["form"].isin(["10-K", "10-Q"])]

            # Plot the revenue trend
            plt.figure(figsize=(12, 6))
            plt.plot(df["date"], df["revenue"] / 1e9)  # Convert to billions
            plt.title(f"Apple Inc. - {revenue_tag} Over Time")
            plt.xlabel("Date")
            plt.ylabel("Revenue (Billions USD)")
            plt.grid(True)
            plt.show()

Cross-Company Analysis with Frames
----------------------------------

Use the frames API to compare the same financial concept across multiple companies.

.. code-block:: python

    import edgar_sec as ed
    import pandas as pd
    import matplotlib.pyplot as plt

    # Initialize the API client
    edgar = ed.EdgarAPI(cache_mode=True)

    # Get assets for all companies for Q4 2022
    assets_frame = edgar.get_frames(
        taxonomy="us-gaap",
        tag="Assets",
        unit="USD",
        period="CY2022Q4I"  # Calendar Year 2022, Q4, Instantaneous
    )

    print(f"Total companies reporting: {assets_frame.pts}")

    # Extract the top 10 companies by assets
    top_companies = sorted(assets_frame.frames, key=lambda x: x.val, reverse=True)[:10]

    # Convert to DataFrame
    df = pd.DataFrame([
        {"Company": company.entity_name, "Assets (Billions)": company.val / 1e9}
        for company in top_companies
    ])

    # Create a horizontal bar chart
    plt.figure(figsize=(12, 8))
    plt.barh(df["Company"], df["Assets (Billions)"])
    plt.title("Top 10 Companies by Total Assets (Q4 2022)")
    plt.xlabel("Total Assets (Billions USD)")
    plt.grid(True, axis="x")
    plt.tight_layout()
    plt.show()

Error Handling and Validation
-----------------------------

Implement robust error handling to manage API limitations and issues.

.. code-block:: python

    import edgar_sec as ed
    import httpx
    from tenacity import retry, wait_fixed, stop_after_attempt

    # Initialize the API client
    edgar = ed.EdgarAPI(cache_mode=True)

    # Function with enhanced error handling
    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
    def get_company_data(cik):
        try:
            # Attempt to fetch data
            return edgar.get_submissions(central_index_key=cik)
        except ValueError as e:
            # Handle API-specific errors
            if "rate limit" in str(e).lower():
                print(f"Rate limit exceeded, retrying in 2 seconds...")
                raise  # Let retry handle this
            else:
                print(f"API Error: {e}")
                return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"Company with CIK {cik} not found")
                return None
            elif e.response.status_code == 429:
                print(f"Rate limit exceeded, retrying in 2 seconds...")
                raise  # Let retry handle this
            else:
                print(f"HTTP Error: {e}")
                return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    # Try with valid and invalid CIKs
    companies = [
        "0000320193",  # Apple (valid)
        "0000123456",  # Invalid CIK
        "0000789019",  # Microsoft (valid)
    ]

    for cik in companies:
        company = get_company_data(cik)
        if company:
            print(f"Successfully retrieved data for {company.name}")
        else:
            print(f"Failed to retrieve data for CIK {cik}")

Advanced Caching Configuration
------------------------------

Customize the caching behavior to optimize performance for your specific use case.

.. code-block:: python

    import edgar_sec as ed
    from cachetools import TTLCache
    import time

    # Create a custom cache with specific size and TTL
    custom_cache = TTLCache(maxsize=512, ttl=7200)  # 2 hour TTL, larger cache

    # Access the internal attributes to customize the API (advanced usage)
    edgar = ed.EdgarAPI(cache_mode=True)
    edgar.cache = custom_cache  # Replace the default cache

    # Measure performance difference with caching
    start_time = time.time()
    apple_facts = edgar.get_company_facts("0000320193")
    first_request_time = time.time() - start_time

    start_time = time.time()
    apple_facts_cached = edgar.get_company_facts("0000320193")
    cached_request_time = time.time() - start_time

    print(f"First request time: {first_request_time:.2f} seconds")
    print(f"Cached request time: {cached_request_time:.2f} seconds")
    print(f"Speed improvement: {first_request_time / cached_request_time:.1f}x faster")
