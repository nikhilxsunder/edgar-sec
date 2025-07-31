.. _home:

Edgar-SEC: A Modern Python Client for SEC EDGAR® API
====================================================

**edgar-sec** is a lightweight, typed, and modern Python package for accessing the **U.S. Securities and Exchange Commission (SEC) EDGAR® API**.
It offers both **synchronous and asynchronous** endpoints, with **structured dataclasses**, **built-in caching**, **rate limiting**, and **developer-friendly error handling**.

Install Edgar-SEC
-----------------

.. tab-set::

   .. tab-item:: pip

     .. code-block:: bash

        pip install edgar-sec

   .. tab-item:: conda

     .. code-block:: bash

        conda install -c conda-forge edgar-sec

See :ref:`installation` for advanced options.

---

Badges
------

.. grid::
    :gutter: 2

    .. grid-item-card:: Build Status
       :columns: 4
       :link: https://github.com/nikhilxsunder/edgar-sec/actions/workflows/main.yml
       :link-alt: GitHub Build Status

       Github Actions build status.

       .. image:: https://github.com/nikhilxsunder/edgar-sec/actions/workflows/main.yml/badge.svg
          :alt: Build Status
          :align: center

    .. grid-item-card:: Static Analysis
       :columns: 4
       :link: https://github.com/nikhilxsunder/edgar-sec/actions/workflows/analyze.yml
       :link-alt: GitHub Static Analysis Status

       Code linting and static analysis status.

       .. image:: https://github.com/nikhilxsunder/edgar-sec/actions/workflows/analyze.yml/badge.svg
          :alt: Static Analysis Status
          :align: center

    .. grid-item-card:: Unit Test Status
       :columns: 4
       :link: https://github.com/nikhilxsunder/edgar-sec/actions/workflows/test.yml
       :link-alt: GitHub Unit Tests

       Unit test coverage for critical components.

       .. image:: https://github.com/nikhilxsunder/edgar-sec/actions/workflows/test.yml/badge.svg
          :alt: Unit Test Status
          :align: center

    .. grid-item-card:: Security Analysis
       :columns: 4
       :link: https://github.com/nikhilxsunder/edgar-sec/actions/workflows/codeql.yml
       :link-alt: GitHub Security CodeQL Scan

       GitHub CodeQL security scanning.

       .. image:: https://github.com/nikhilxsunder/edgar-sec/actions/workflows/codeql.yml/badge.svg
          :alt: OpenSSF
          :align: center

    .. grid-item-card:: OpenSSF Best Practices
       :columns: 4
       :link: https://www.bestpractices.dev/projects/10210
       :link-alt: View edgar-sec on PyPI

       Open Source Security Foundation (OpenSSF) Gold Badge.

       .. image:: https://www.bestpractices.dev/projects/10210/badge
          :alt: OpenSSF Best Practices Certified
          :align: center

    .. grid-item-card:: Code Coverage
       :columns: 4
       :link: https://app.codecov.io/gh/nikhilxsunder/edgar-sec
       :link-alt: Code Coverage with Codecov

       Codecov test coverage report.

       .. image:: https://codecov.io/gh/nikhilxsunder/edgar-sec/graph/badge.svg
          :alt: Code Coverage
          :align: center

    .. grid-item-card:: Socket Security Score
       :columns: 4
       :link: https://socket.dev/pypi/package/edgar-sec/overview/2.0.0/tar-gz
       :link-alt: Socket Security Analysis

       Security risk analysis via Socket.dev.

       .. image:: https://socket.dev/api/badge/pypi/package/edgar-sec/2.0.0?artifact_id=tar-gz
          :alt: Socket Security Score
          :align: center

    .. grid-item-card:: Packaging Status
       :columns: 4
       :link: https://repology.org/project/python%3Aedgar-sec/versions
       :link-alt: Packaging Status Repology

       Repology packaging status across Linux distributions.

       .. image:: https://repology.org/badge/tiny-repos/python%3Aedgar-sec.svg
          :alt: Packaging Status
          :align: center

    .. grid-item-card:: PyPI Version
       :columns: 4
       :link: https://pypi.org/project/edgar-sec/
       :link-alt: View Edgar-SEC on PyPI

       Latest version released on PyPI.

       .. image:: https://img.shields.io/pypi/v/edgar-sec.svg
          :alt: PyPI Version
          :align: center

    .. grid-item-card:: PyPI Downloads
       :columns: 4
       :link: https://pepy.tech/project/edgar-sec
       :link-alt: PyPI Download Statistics

       Download stats via Pepy.tech.

       .. image:: https://pepy.tech/badge/edgar-sec
          :alt: PyPI Downloads
          :align: center

    .. grid-item-card:: Conda-Forge Version
       :columns: 4
       :link: https://anaconda.org/conda-forge/edgar-sec
       :link-alt: View Edgar-SEC on Conda-Forge

       Conda-Forge published version.

       .. image:: https://anaconda.org/conda-forge/edgar-sec/badges/version.svg
          :alt: Conda-Forge Version
          :align: center

    .. grid-item-card:: Conda-Forge Downloads
       :columns: 4
       :link: https://anaconda.org/conda-forge/edgar-sec
       :link-alt: Conda-Forge Download Statistics

       Number of downloads from Conda-Forge.

       .. image:: https://anaconda.org/conda-forge/edgar-sec/badges/downloads.svg
          :alt: Conda-Forge Downloads
          :align: center

Key Features
------------

.. dropdown:: Typed Models
   :color: primary
   :icon: database

   Structured Python `@dataclass` models for filings, metadata, entities, and submissions.

.. dropdown:: Async + Sync Clients
   :color: secondary
   :icon: rocket

   Fully asynchronous and synchronous interfaces via :class:`edgar_sec.clients.EdgarAPI` and :class:`edgar_sec.clients.EdgarAPI.AsyncAPI`.

.. dropdown:: File Caching
   :color: primary
   :icon: archive

   Caches responses to disk to reduce redundant API calls and accelerate development.

   Caches responses to disk to reduce redundant API calls and accelerate development.

   :icon: archive

   Caches responses to disk to reduce redundant API calls and accelerate development.

.. dropdown:: Built-in Rate Limiting
   :color: secondary
   :icon: clock

   Auto-throttling respects SEC EDGAR API limits — no extra config required.

.. dropdown:: Pythonic Error Handling
   :color: primary
   :icon: bug

   Designed for transparency and reliability — clear exceptions for all edge cases.

Resources
---------

Explore the documentation:

.. toctree::
   :maxdepth: 2
   :caption: Get Started

   installation/index

.. toctree::
   :maxdepth: 2
   :caption: Developer Reference

   api/index
   resources/index
   glossary

.. toctree::
   :maxdepth: 1
   :caption: Project

   contributing
   changelog
   code_of_conduct
   security
   license
