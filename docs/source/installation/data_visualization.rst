.. _data-visualization:

Data Visualization Examples
============================

This page demonstrates how to **visualize SEC filing data retrieved with edgar-sec** using standard Python libraries such as **Matplotlib**, **Seaborn**, and **Pandas**.
You can integrate edgar-sec into dashboards, analytics workflows, and compliance monitoring tools.

---

.. grid::
    :gutter: 2

    .. grid-item-card:: Filing Volume Line Chart

        Visualize filing activity over time using :mod:`matplotlib.pyplot`.

        .. code-block:: python

            import matplotlib.pyplot as plt
            import edgar_sec as ed

            edgar = ed.EdgarAPI()
            history = edgar.get_submissions(ticker="AAPL")

            dates = [f.filing_date for f in history.filings if f.form == "10-K"]
            dates.sort()

            plt.figure(figsize=(10, 6))
            plt.hist(dates, bins=len(set(dates)), color="navy")
            plt.title("Apple 10-K Filing Dates")
            plt.xlabel("Year")
            plt.ylabel("Number of Filings")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.grid(True)
            plt.show()

    .. grid-item-card:: Form Type Frequency Bar Chart

        Compare the frequency of different SEC form types.

        .. code-block:: python

            import matplotlib.pyplot as plt
            import edgar_sec as ed
            from collections import Counter

            edgar = ed.EdgarAPI()
            history = edgar.get_submissions(ticker="MSFT")

            form_counts = Counter(f.form for f in history.filings)
            forms, counts = zip(*form_counts.most_common())

            plt.figure(figsize=(12, 6))
            plt.bar(forms, counts, color="skyblue")
            plt.title("Form Type Frequency for Microsoft")
            plt.xlabel("Form Type")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

---

Advanced Visualizations
------------------------

.. grid::
    :gutter: 2

    .. grid-item-card:: Filing Activity Heatmap

        Use :mod:`seaborn` to visualize temporal filing density.

        .. code-block:: python

            import seaborn as sns
            import matplotlib.pyplot as plt
            import pandas as pd
            import edgar_sec as ed

            edgar = ed.EdgarAPI()
            history = edgar.get_submissions(ticker="GOOGL")

            df = pd.DataFrame({
                "date": [f.filing_date for f in history.filings],
                "form": [f.form for f in history.filings]
            })
            df["year"] = pd.to_datetime(df["date"]).dt.year
            df["form"] = df["form"].str.upper()

            pivot = df.pivot_table(index="form", columns="year", aggfunc="size", fill_value=0)

            plt.figure(figsize=(10, 6))
            sns.heatmap(pivot, annot=True, fmt="d", cmap="Blues")
            plt.title("Filing Frequency by Form and Year (GOOGL)")
            plt.ylabel("Form Type")
            plt.xlabel("Year")
            plt.tight_layout()
            plt.show()

    .. grid-item-card:: Filing Trends Comparison

        Compare 10-K vs 10-Q over time for a company.

        .. code-block:: python

            import matplotlib.pyplot as plt
            import pandas as pd
            import edgar_sec as ed

            edgar = ed.EdgarAPI()
            history = edgar.get_submissions(ticker="META")

            filings = pd.DataFrame({
                "date": [f.filing_date for f in history.filings],
                "form": [f.form for f in history.filings]
            })
            filings["year"] = pd.to_datetime(filings["date"]).dt.year
            summary = filings.groupby(["year", "form"]).size().unstack(fill_value=0)

            summary[["10-K", "10-Q"]].plot(kind="bar", stacked=True, figsize=(10, 6))
            plt.title("Annual Filing Count: 10-K vs 10-Q (META)")
            plt.xlabel("Year")
            plt.ylabel("Number of Filings")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

---

Related Resources
-----------------

.. grid::
    :gutter: 2
    :margin: 2 0 2 0

    .. grid-item-card:: Basic Usage Guide
        :link: basic-usage
        :link-type: ref
        :link-alt: Getting started with edgar-sec

        Learn how to initialize the client, fetch submissions, and resolve tickers.

    .. grid-item-card:: Advanced Usage
        :link: advanced-usage
        :link-type: ref
        :link-alt: Async features and parameter customization

        Explore asynchronous usage, caching, batching, and retries.

    .. grid-item-card:: Full API Reference
        :link: api-index
        :link-type: ref
        :link-alt: Full API reference documentation

        Browse all available clients, methods, models, and async equivalents.

    .. grid-item-card:: Example Use Cases
        :link: use-cases
        :link-type: ref
        :link-alt: Real-world usage examples

        See practical examples including monitoring, filing analytics, and financial pipelines.
