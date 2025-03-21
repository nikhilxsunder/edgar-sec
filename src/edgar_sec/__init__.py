"""
This module initializes the edgar-sec package.

Imports:
    EdgarAPI: A class that provides methods to interact with the SEC EDGAR API.
"""
from.edgar_sec import EdgarAPI
from.edgar_data import (
    Address,
    FormerName,
    Filing,
    File,
    SubmissionHistory,
    UnitDisclosure,
    CompanyConcept,
    EntityDisclosure,
    Fact,
    CompanyFact,
    Frame
)
__all__ = [
    'EdgarAPI',
    'Address',
    'FormerName',
    'Filing',
    'File',
    'SubmissionHistory',
    'UnitDisclosure',
    'CompanyConcept',
    'EntityDisclosure',
    'Fact',
    'CompanyFact',
    'Frame'
]
