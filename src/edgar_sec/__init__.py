# filepath: /src/edgar_sec/__init__.py
#
# Copyright (c) 2025 Nikhil Sunder
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
This module initializes the edgar-sec package.

Imports:
    EdgarAPI: A class that provides methods to interact with the SEC EDGAR API.
    AsyncAPI: An asynchronous version of the EdgarAPI class.
    EdgarHelpers: A class that provides helper methods for the edgar-sec package.
    Address: A class representing an address associated with a company.
    FormerName: A class representing a former name of a company.
    Filing: A class representing a filing made by a company.
    File: A class representing a file associated with a filing.
    SubmissionHistory: A class representing the submission history of a company.
    UnitDisclosure: A class representing a unit disclosure for a company.
    CompanyConcept: A class representing a company concept.
    EntityDisclosure: A class representing an entity disclosure for a company.
    Fact: A class representing a fact associated with a company.
    CompanyFact: A class representing a company fact.
    FrameDisclosure: A class representing a frame disclosure for a company.
    Frame: A class representing a frame associated with a filing.
    Company: A class representing a company in the EDGAR database.
"""
from edgar_sec.__about__ import __title__, __version__, __author__, __license__, __copyright__, __description__, __url__

from . import clients
from . import helpers
from . import objects

from .clients import EdgarAPI
from .helpers import EdgarHelpers
from .objects import (
    Address,
    FormerName,
    Filing,
    File,
    SubmissionHistory,
    UnitDisclosure,
    CompanyConcept,
    TaxonomyDisclosures,
    TaxonomyFacts,
    CompanyFacts,
    FrameDisclosure,
    Frame,
    Company,
)

AsyncAPI = EdgarAPI.AsyncAPI

__all__ = [
    "__title__",
    "__description__",
    "__version__",
    "__copyright__",
    "__author__",
    "__license__",
    "__url__",
    "clients",
    "helpers",
    "objects",
    "EdgarAPI",
    "AsyncAPI",
    "EdgarHelpers",
    "Address",
    "FormerName",
    "Filing",
    "File",
    "SubmissionHistory",
    "UnitDisclosure",
    "CompanyConcept",
    "TaxonomyDisclosures",
    "TaxonomyFacts",
    "CompanyFacts",
    "FrameDisclosure",
    "Frame",
    "Company",
]
