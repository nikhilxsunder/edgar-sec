#!/usr/bin/env python3
"""
Script to synchronize conda-recipe/meta.yaml with pyproject.toml.
This ensures the conda recipe always has the correct version and URL.
"""
import re
import sys
import os
from pathlib import Path
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Python < 3.11

def main():
    """Main function to sync meta.yaml with pyproject.toml"""
    repo_root = Path(__file__).parent.parent
    pyproject_path = repo_root / "pyproject.toml"
    meta_yaml_path = repo_root / "conda-recipe" / "meta.yaml"

    # Ensure the conda-recipe directory exists
    if not meta_yaml_path.parent.exists():
        print(f"Creating conda-recipe directory at {meta_yaml_path.parent}")
        os.makedirs(meta_yaml_path.parent, exist_ok=True)

    # Load pyproject.toml
    try:
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomllib.load(f)
    except FileNotFoundError:
        print(f"Error: {pyproject_path} not found!")
        return 1

    # Extract data from pyproject.toml
    try:
        poetry_data = pyproject_data["tool"]["poetry"]
        package_name = poetry_data["name"]
        version = poetry_data["version"]
    except KeyError as e:
        print(f"Error: Missing required key in pyproject.toml: {e}")
        return 1

    # Read existing meta.yaml if it exists
    if meta_yaml_path.exists():
        with open(meta_yaml_path, "r") as f:
            meta_content = f.read()
    else:
        meta_content = get_default_meta_template()

    # Update version in meta.yaml
    version_pattern = r'version: [\"\']?[\d\.]+[\"\']?'
    meta_content = re.sub(version_pattern, f'version: {version}', meta_content)

    # Update package URL in meta.yaml
    url_pattern = r'url: "https://pypi\.io/packages/source/[a-z]/[a-z0-9\-]+/[a-z0-9\-]+-[\d\.]+\.tar\.gz"'
    first_letter = package_name[0]
    new_url = f'url: "https://pypi.io/packages/source/{first_letter}/{package_name}/{package_name}-{version}.tar.gz"'
    meta_content = re.sub(url_pattern, new_url, meta_content)

    # Write updated content back
    with open(meta_yaml_path, "w") as f:
        f.write(meta_content)

    print(f"Updated {meta_yaml_path} with version {version} from {pyproject_path}")
    print("Note: Dependencies need to be manually managed in meta.yaml")
    return 0

def get_default_meta_template():
    """Return a default meta.yaml template if file doesn't exist"""
    return """# filepath: conda-recipe/meta.yaml
package:
  name: edgar-sec
  version: 0.0.0

source:
  url: "https://pypi.io/packages/source/e/edgar-sec/edgar-sec-0.0.0.tar.gz"
  # sha256: will be added after publishing to PyPI

build:
  noarch: python
  number: 0
  script: |
    python -m pip install . -vv

requirements:
  host:
    - python >=3.9,<4.0
    - pip
    - poetry-core >=1.0.0
  run:
    - python >=3.9,<4.0
    - httpx
    - tenacity
    - conda-forge::cachetools

test:
  imports:
    - edgar_sec
  requires:
    - pip
  commands:
    - pip check

about:
  home: "https://github.com/nikhilxsunder/edgar-sec"
  doc_url: "https://nikhilxsunder.github.io/edgar-sec/"
  dev_url: "https://github.com/nikhilxsunder/edgar-sec"
  license: AGPL-3.0-or-later
  license_family: AGPL
  license_file: LICENSE
  summary: "A feature-rich python package for interacting with the US Securities and Exchange Commission API: EDGAR"
  description: |
    edgar-sec is a Python package for interacting with the US Securities and Exchange Commission EDGAR API.
    It provides a feature-rich interface with:
    - Native support for asynchronous requests (async)
    - All method outputs are mapped to dataclasses for better usability
    - Local caching for easier data access and faster execution times
    - Built-in rate limiter that doesn't exceed 10 calls per second
    - MyPy compatible type stubs

extra:
  recipe-maintainers:
    - nikhilxsunder
"""

if __name__ == "__main__":
    sys.exit(main())
