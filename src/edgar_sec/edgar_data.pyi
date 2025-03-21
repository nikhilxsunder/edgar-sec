from dataclasses import dataclass
from typing import Dict, List, Union

@dataclass
class Address:
    address_type: str
    street1: str
    street2: str
    city: str
    state_or_country: str
    zipcode: str
    state_or_country_description: str

    @classmethod
    def from_dict(cls, address_type: str, data: Dict) -> 'Address': ...

@dataclass
class FormerName:
    name: str
    from_date: str
    to_date: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'FormerName': ...

@dataclass
class Filing:
    accession_number: str
    filing_date: str
    report_date: str
    acceptance_date_time: str
    act: str
    form: str
    file_number: str
    film_number: str
    items: Union[str, List[str]]
    core_type: str
    size: int
    is_xbrl: bool
    is_inline_xbrl: bool
    primary_document: str
    primary_doc_description: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'Filing': ...

@dataclass
class File:
    name: str
    filing_count: int
    filing_from: str
    filing_to: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'File': ...

@dataclass
class SubmissionHistory:
    cik: str
    entity_type: str
    sic: str
    sic_description: str
    owner_org: str
    insider_transaction_for_owner_exists: bool
    insider_transaction_for_issuer_exists: bool
    name: str
    tickers: Union[str, List[str]]
    exchanges: Union[str, List[str]]
    ein: str
    description: str
    website: str
    investor_website: str
    category: str
    fiscal_year_end: str
    state_of_incorporation: str
    state_of_incorporation_description: str
    addresses: Union[Address, List[Address]]
    phone: str
    flags: Union[str, List[str]]
    former_names: Union[FormerName, List[FormerName]]
    filings: Union[Filing, List[Filing]]
    files: Union[File, List[File]]

    @classmethod
    def from_api_response(cls, response: Dict) -> 'SubmissionHistory': ...

@dataclass
class UnitDisclosure:
    unit: str
    end: str
    val: int
    accn: str
    fy: str
    fp: str
    form: str
    filed: str
    frame: str
    start: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'UnitDisclosure': ...

@dataclass
class CompanyConcept:
    cik: str
    taxonomy: str
    tag: str
    label: str
    description: str
    entity_name: str
    units: Union[UnitDisclosure, List[UnitDisclosure]]

    @classmethod
    def from_api_response(cls, response: Dict) -> 'CompanyConcept': ...

@dataclass
class EntityDisclosure:
    name: str
    label: str
    description: str
    units: Dict[str, List[UnitDisclosure]]

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> 'EntityDisclosure': ...

@dataclass
class Fact:
    taxonomy: str
    disclosures: Dict[str, EntityDisclosure]

    @classmethod
    def from_dict(cls, taxonomy: str, data: Dict) -> 'Fact': ...

@dataclass
class CompanyFact:
    cik: str
    entity_name: str
    facts: Dict[str, Fact]

    @classmethod
    def from_api_response(cls, response: Dict) -> 'CompanyFact': ...

@dataclass
class FrameDisclosure:
    accn: str
    cik: str
    entity_name: str
    loc: str
    end: str
    val: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'FrameDisclosure': ...

@dataclass
class Frame:
    taxonomy: str
    tag: str
    ccp: str
    uom: str
    label: str
    description: str
    pts: int
    frames: List[FrameDisclosure]

    @classmethod
    def from_api_response(cls, response: Dict) -> 'Frame': ...
