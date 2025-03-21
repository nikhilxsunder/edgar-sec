Installation
============

Using pip
---------

You can install edgar-sec using pip:

.. code-block:: bash

   pip install edgar-sec

Using conda
-----------

edgar-sec is available on Anaconda through the author's channel. You can install it with conda:

.. code-block:: bash

   conda install nikhilxsunder::edgar-sec

We recommend creating a dedicated environment for your project:

.. code-block:: bash

   conda create -n myenv
   conda activate myenv
   conda install nikhilxsunder::edgar-sec

Note: edgar-sec will be submitted to conda-forge in the future for broader distribution.

Optional Type Stubs
------------------

If you need type stubs for development (e.g., for `cachetools`), you can install the optional dependencies:

Using pip:

.. code-block:: bash

   pip install edgar-sec[types]

Development Installation
------------------------

For development purposes, you can install the package with all development dependencies:

Using Poetry (recommended):

.. code-block:: bash

    git clone https://github.com/nikhilxsunder/edgar-sec.git
    cd edgar-sec
    poetry install

Using pip:

.. code-block:: bash

    git clone https://github.com/nikhilxsunder/edgar-sec.git
    cd edgar-sec

    # Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate

    # Install in development mode with dev dependencies
    pip install -e ".[dev,types]"

    # Install pre-commit hooks
    pre-commit install

Requirements
-----------

edgar-sec has the following dependencies:

* Python 3.9 or newer
* httpx - For HTTP requests
* tenacity - For retry logic
* cachetools - For caching API responses

All dependencies are automatically installed when using pip or conda.
