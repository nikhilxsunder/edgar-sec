.. _resources-index:

Resources
=========

Explore advanced topics, usage strategies, design internals, and comparisons for **Edgar-SEC**, a modern Python client for the **SEC EDGAR® API**.

This section contains **essential guides** to help you **use Edgar-SEC effectively**, **compare it with other tools**, and **understand its internal architecture**.

---

Contents
--------

.. toctree::
    :maxdepth: 2
    :caption: Resources

    faq
    comparison
    use_cases
    api_overview
    architecture

---

Additional API Notes
--------------------

Important topics related to edgar-sec's internal behavior:

.. toctree::
    :maxdepth: 1

    notes

Topics include:

* Parameter handling (e.g., :class:`datetime.datetime`, :class:`list`, :class:`bool`, :class:`int`, coercion),
* Async design: :class:`edgar_sec.AsyncAPI` nested client pattern,
* Model hierarchy and helper access patterns (e.g., :meth:`edgar_sec.EdgarAPI.get_submissions`, :meth:`edgar_sec.helpers.EdgarHelpers.get_cik`).

For internal structure and code flow, see :ref:`architecture`.

---

Related Topics
--------------

.. grid::
    :gutter: 2

    .. grid-item-card:: Full API Reference
        :link: api-index
        :link-type: ref
        :link-alt: edgar-sec Method Documentation

        Explore detailed documentation for all edgar-sec methods, clients, and models.

    .. grid-item-card:: Quick Start Guide
        :link: quickstart
        :link-type: ref
        :link-alt: Quick Start for edgar-sec

        Learn how to install, configure, and make your first SEC query.

    .. grid-item-card:: Installation and Setup
        :link: installation-usage
        :link-type: ref
        :link-alt: Installation and Configuration Guide

        Step-by-step installation guide using pip, conda, or GitHub.
