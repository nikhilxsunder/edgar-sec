.. _installation:

Installing Edgar-SEC
====================

Edgar-SEC is available on both **PyPI** and **Conda-Forge**.
This page covers multiple ways to install Edgar-SEC for production or development use.

---

Installation Methods
--------------------

.. tab-set::

   .. tab-item:: pip (PyPI)

      Install the latest stable release from PyPI:

      .. code-block:: bash

         pip install edgar-sec

      Installs core dependencies needed for working with the EDGAR API.

   .. tab-item:: conda (Conda-Forge)

      Install via Conda-Forge:

      .. code-block:: bash

         conda install -c conda-forge edgar-sec

      We recommend creating a new environment:

      .. code-block:: bash

         conda create -n myenv
         conda activate myenv
         conda install -c conda-forge edgar-sec

   .. tab-item:: Development Install (GitHub)

      Clone and install for local development:

      .. code-block:: bash

         git clone https://github.com/nikhilxsunder/edgar-sec.git
         cd edgar-sec
         poetry install

      See :ref:`contributing` for developer guidelines.

---

Optional Enhancements
----------------------

.. dropdown:: Install Type Stubs for Static Typing
   :color: secondary
   :open:

   Boost development experience with type hints (e.g., :mod:`mypy`, :mod:`pyright`):

   .. code-block:: bash

      pip install edgar-sec[types]

   Includes stubs for `cachetools`.

.. dropdown:: Install with Dev Tools
   :color: secondary
   :open:

   To enable dev utilities, and full lint/test support:

   .. code-block:: bash

      pip install edgar-sec[dev]

   See the :ref:`api-overview` for testing setup.

---

Developer Quick Setup
----------------------

.. grid::
   :gutter: 2

   .. grid-item-card:: Development Setup (Poetry)
      :link: https://github.com/nikhilxsunder/edgar-sec
      :link-alt: View Source on GitHub

      Clone the repository and install with all development dependencies:

      .. code-block:: bash

         git clone https://github.com/nikhilxsunder/edgar-sec.git
         cd edgar-sec
         poetry install

   .. grid-item-card:: Alternative Setup (conda + pip)
      :link: https://github.com/nikhilxsunder/edgar-sec
      :link-alt: View Source on GitHub

      Create a dedicated environment manually:

      .. code-block:: bash

         git clone https://github.com/nikhilxsunder/edgar-sec.git
         cd edgar-sec

         conda create -n edgar-sec-dev python=3.10
         conda activate edgar-sec-dev

         pip install -e ".[dev,types]"

         pre-commit install

---

Related Resources
-----------------

.. grid::
   :gutter: 2

   .. grid-item-card:: Installation & Usage Guide
      :link: installation-usage
      :link-type: ref
      :link-alt: Installation and Usage Documentation

      Full beginner tutorial for setting up Edgar-SEC and fetching data.

   .. grid-item-card:: Basic and Advanced Examples
      :link: basic-usage
      :link-type: ref
      :link-alt: Basic and Advanced Usage Examples

      Covers 10-K lookups, metadata search, and JSON-to-model workflows.

   .. grid-item-card:: Parameter Handling Notes
      :link: api-notes
      :link-type: ref
      :link-alt: API Parameter Handling Notes

      Learn how Edgar-SEC automatically validates and transforms parameters.

---
