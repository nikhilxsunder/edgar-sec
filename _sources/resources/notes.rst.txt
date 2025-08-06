.. _api-notes:

Special Notes: Parameter Conversion and Helper Utilities (edgar-sec)
====================================================================

The Edgar-SEC package uses **automatic parameter normalization**, **CIK resolution helpers**, and **async-safe conversion tools** for consistent and clean API usage.

This page summarizes key internal utilities and design patterns.

---

Parameter Conversion in Edgar-SEC
---------------------------------

Edgar-SEC **automatically handles conversions** for common parameter types.

Supported Conversions
^^^^^^^^^^^^^^^^^^^^^

- :class:`datetime.datetime` → `YYYY-MM-DD`:

  .. code-block:: python

      from datetime import datetime
      edgar.get_submissions(
          cik="0000320193",
          start=datetime(2021, 1, 1)
      )

- :class:`str` → padded CIK:

  Automatically zero-fills short CIKs to 10 digits via internal validation.

  .. code-block:: python

      edgar.get_submissions(cik="320193")  # Becomes "0000320193"

- :class:`str` → CY####Q# formatted period:

  .. code-block:: python

      edgar.EdgarHelpers.string_cy_conversion("2022-09-30")  # -> "CY2022Q3"

- :class:`datetime` → CY####Q# formatted period:

  .. code-block:: python

      from datetime import datetime
      edgar.EdgarHelpers.datetime_cy_conversion(datetime(2022, 3, 31))  # -> "CY2022Q1"

---

Helper Methods
--------------

Conversion and validation utilities are accessible via:

- :class:`edgar_sec.EdgarHelpers.get_cik`
- :class:`edgar_sec.EdgarHelpers.get_universe`
- :class:`edgar_sec.EdgarHelpers.cik_validation`
- :class:`edgar_sec.EdgarHelpers.string_cy_conversion`
- :class:`edgar_sec.EdgarHelpers.datetime_cy_conversion`

Each has an async equivalent as well (e.g. `get_cik_async`, `datetime_cy_conversion_async`).

---

CIK Search and Universe Fetching
--------------------------------

Examples:

- Search for a company CIK by name or ticker:

  .. code-block:: python

      edgar.EdgarHelpers.get_cik(ticker="AAPL")
      edgar.EdgarHelpers.get_cik(search_text="Tesla")

- Fetch full company list:

  .. code-block:: python

      universe = edgar.EdgarHelpers.get_universe()
      print(universe[0].name, universe[0].cik)

---

Validating CIK Format
---------------------

CIKs are zero-padded to 10-digit strings automatically.

.. code-block:: python

    edgar.EdgarHelpers.cik_validation("320193")  # -> "0000320193"

Used internally by all client methods.

---

Calendar Period Utilities
-------------------------

For converting reporting periods into SEC-style `CY####Q#` format:

.. code-block:: python

    from edgar_sec import EdgarHelpers
    EdgarHelpers.string_cy_conversion("2023-06-30")     # -> "CY2023Q2"
    EdgarHelpers.datetime_cy_conversion(datetime(2023, 6, 30))  # -> "CY2023Q2"

Validation:

.. code-block:: python

    EdgarHelpers.string_cy_validation("CY2022Q3")  # -> True
    EdgarHelpers.string_cy_validation("2022Q3")    # -> False

---

Async Conversion Utilities
--------------------------

All conversion methods are `async`-safe using `asyncio.to_thread(...)`.

.. code-block:: python

    await edgar.EdgarHelpers.string_cy_conversion_async("2023-06-30")
    await edgar.EdgarHelpers.get_cik_async(ticker="GOOG")

---

Related Topics
^^^^^^^^^^^^^^

- See the full API documentation: :ref:`api-index`
- Real-world usage patterns: :ref:`use-cases`
- Overview of client capabilities: :ref:`api-overview`
