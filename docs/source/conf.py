# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# imports
import os
import sys

# -- Project information -----------------------------------------------------
project = 'edgar-sec'
copyright = '2025, Nikhil Sunder'
author = 'Nikhil Sunder'
release = '2.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'myst_parser',
    'sphinxcontrib.googleanalytics',
    'sphinx_sitemap',
    'sphinxext.opengraph',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.graphviz',
    'sphinx.ext.extlinks',
    'sphinx.ext.doctest',
    "sphinx_design",
    'pydata_sphinx_theme',
]

# myst
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 4

# path
sys.path.insert(0, os.path.abspath('../..'))

# google analytics
googleanalytics_id = 'G-HM6ZC88602'
googleanalytics_enabled = True

# sitemap
sitemap_filename = "sitemap.xml"
sitemap_url_scheme = "{link}"

# html
html_baseurl = 'https://nikhilxsunder.github.io/edgar-sec/'
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "logo": {
        "image_light": "_static/edgar-sec-logo.png",
        "image_dark": "_static/edgar-sec-logo.png",
    },
    "header_links_before_dropdown": 5,
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": [ "navbar-icon-links"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/nikhilxsunder/edgar-sec",
            "icon": "fab fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/edgar-sec/",
            "icon": "fab fa-python",
        },
        {
            "name": "Conda-Forge",
            "url": "https://anaconda.org/conda-forge/edgar-sec",
            "icon": "fas fa-database",
        },
        {
            "name": "Codecov",
            "url": "https://app.codecov.io/gh/nikhilxsunder/edgar-sec",
            "icon": "fas fa-umbrella",
        },
        {
            "name": "Socket",
            "url": "https://socket.dev/pypi/package/edgar-sec/overview/2.1.1/tar-gz",
            "icon": "fas fa-shield",
        },
        {
            "name": "OpenSSF",
            "url": "https://www.bestpractices.dev/en/projects/10210?criteria_level=2",
            "icon": "fas fa-trophy",
        },
    ],
    "navbar_align": "right",
    "primary_sidebar_end": ["sidebar-ethical-ads"],
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version", "theme-version"],
    "use_edit_page_button": True,
    "show_toc_level": 1,
    "show_prev_next": True,
    "announcement": """
        <div class="sidebar-message">
            Version 2 is now available!
            Please check the
            <a href="resources/notes.html" target="_self">
                special notes page
            </a>
            for more information.
        </div>
    """,
}
html_static_path = ['_static']
html_title = "edgar-sec"
html_favicon = "_static/edgar-sec-favicon.ico"
html_logo = "_static/edgar-sec-logo.png"
html_context = {
    "github_user": "nikhilxsunder",
    "github_repo": "edgar-sec",
    "github_version": "main",
    "doc_path": "docs/source",
}
html_meta ={
    "description": "A feature-rich python-package for interacting with the US Securities and Exchange Commission API: EDGAR",
    "keywords": "edgar, sec, api, financial data, economic data, data analysis, data science"
}
html_js_files = [
    'json_ld.js',
]
html_show_copyright = True
html_last_updated_fmt = '%b %d, %Y'

templates_path = ['_templates']

# autodocs
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
autodoc_typehints = "description"
autodoc_typehints_format = "short"

# md/rst
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# opengraph
ogp_site_url = "https://nikhilxsunder.github.io/edgar-sec/"
ogp_image = "https://nikhilxsunder.github.io/edgar-sec/_static/edgar-sec-logo.png"
ogp_description_length = 300
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta property="og:locale" content="en_US" />',
    '<meta property="og:site_name" content="EDGAR SEC Documentation" />',
    '<meta property="og:url" content="https://nikhilxsunder.github.io/edgar-sec/" />',
    '<meta property="og:image:alt" content="EDGAR SEC Logo" />',
]
ogp_enable_meta_description = True

# intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    "tenacity": ("https://tenacity.readthedocs.io/en/latest/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

# autosummary
autosummary_generate = True

# extlinks
extlinks = {
    'python-doc': ('https://docs.python.org/3/library/%s', 'Python Docs: %s'),
    'edgar-api': ('https://www.sec.gov/search-filings/edgar-application-programming-interfaces', 'EDGAR API Docs: %s'),
    'github': ('https://github.com/nikhilxsunder/edgar-sec/%s', 'GitHub: %s'),
}
