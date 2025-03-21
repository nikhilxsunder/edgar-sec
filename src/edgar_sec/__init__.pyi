"""
Type stub file for the edgar-sec package.
This package provides utilities for interacting with the SEC EDGAR API.
"""
from typing import Dict, List, Union, Any, Optional

from edgar_sec.edgar_sec import EdgarAPI
from edgar_sec.edgar_data import (
    Address,
    CompanyConcept,
    CompanyFact,
    EntityDisclosure,
    Fact,
    File,
    Filing,
    FormerName,
    Frame,
    FrameDisclosure,
    SubmissionHistory,
    UnitDisclosure
)

__all__: List[str] = [
    "EdgarAPI",
    "Address",
    "CompanyConcept",
    "CompanyFact",
    "EntityDisclosure",
    "Fact",
    "File",
    "Filing",
    "FormerName",
    "Frame",
    "FrameDisclosure",
    "SubmissionHistory",
    "UnitDisclosure"
]
