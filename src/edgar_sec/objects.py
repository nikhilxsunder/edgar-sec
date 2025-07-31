# filepath: /src/edgar_sec/objects.py
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
This module defines data classes for the EDGAR API responses.
"""

from dataclasses import dataclass
import asyncio
from typing import List, Dict, Optional
from edgar_sec.__about__ import __title__, __version__, __author__, __license__, __copyright__, __description__, __url__

@dataclass
class Address:
    """
    A class representing an address from SEC filing data.
    """
    address_type: str
    street1: str
    street2: str
    city: str
    state_or_country: str
    zipcode: str
    state_or_country_description: str
    is_foreign_location: bool
    foreign_state_territory: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None

    @classmethod
    def to_object(cls, address_type: str, data: Dict) -> 'Address':
        """
        Parses a dictionary and returns an Address object.
        """
        return cls(
            address_type=address_type,
            street1=data['street1'],
            street2=data.get('street2', '') if data.get('street2') else '',
            city=data['city'],
            state_or_country=data['stateOrCountry'],
            zipcode=data['zipCode'],
            state_or_country_description=data['stateOrCountryDescription'],
            is_foreign_location=bool(data.get('isForeignLocation', False)),
            foreign_state_territory=data.get('foreignStateTerritory'),
            country=data.get('country'),
            country_code=data.get('countryCode')
        )
    @classmethod
    async def to_object_async(cls, address_type: str, data: Dict) -> 'Address':
        """
        Asynchronously parses a dictionary and returns an Address object.
        """
        return await asyncio.to_thread(cls.to_object, address_type, data)

@dataclass
class FormerName:
    """
    A class representing a former name of an SEC filing entity.
    """
    name: str
    from_date: str
    to_date: str

    @classmethod
    def to_object(cls, data: Dict) -> 'FormerName':
        """
        Parses a dictionary and returns a FormerName object.
        """
        return cls(
            name=data['name'],
            from_date=data['from'],
            to_date=data.get('to', '')
        )
    @classmethod
    async def to_object_async(cls, data: Dict) -> 'FormerName':
        """
        Asynchronously parses a dictionary and returns a FormerName object.
        """
        return await asyncio.to_thread(cls.to_object, data)

@dataclass
class File:
    """
    A class representing a file reference in SEC EDGAR submission history.
    """
    name: str
    filing_count: int
    filing_from: str
    filing_to: str

    @classmethod
    def to_object(cls, data: Dict) -> 'File':
        """
        Parses a dictionary and returns a File object.
        """
        return cls(
            name=data['name'],
            filing_count=int(data['filingCount']),
            filing_from=data['filingFrom'],
            filing_to=data['filingTo']
        )
    @classmethod
    async def to_object_async(cls, data: Dict) -> 'File':
        """
        Asynchronously parses a dictionary and returns a File object.
        """
        return await asyncio.to_thread(cls.to_object, data)

@dataclass
class Filing:
    """
    A class representing an SEC filing document.
    """
    accession_number: str
    filing_date: str
    report_date: str
    acceptance_date_time: str
    act: str
    form: str
    file_number: str
    film_number: str
    items: List[str]
    core_type: str
    size: int
    is_xbrl: bool
    is_inline_xbrl: bool
    primary_document: str
    primary_doc_description: str

    @classmethod
    def to_object(cls, data: Dict, index: int) -> 'Filing':
        """
        Parses a dictionary and returns a Filing object.
        """
        return cls(
            accession_number=data['accessionNumber'][index],
            filing_date=data['filingDate'][index],
            report_date=data['reportDate'][index],
            acceptance_date_time=data['acceptanceDateTime'][index],
            act=data['act'][index],
            form=data['form'][index],
            file_number=data['fileNumber'][index],
            film_number=data['filmNumber'][index],
            items=data['items'][index],
            core_type=data.get('core_type', '')[index],
            size=int(data.get('size', 0)[index]),
            is_xbrl=bool(data.get('isXBRL', False)[index]),
            is_inline_xbrl=bool(data.get('isInlineXBRL', False)[index]),
            primary_document=data.get('primaryDocument', '')[index],
            primary_doc_description=data.get('primaryDocDescription', '')[index],
        )
    @classmethod
    async def to_object_async(cls, data: Dict, index: int) -> 'Filing':
        """
        Asynchronously parses a dictionary and returns a Filing object.
        """
        return await asyncio.to_thread(cls.to_object, data, index)

@dataclass
class SubmissionHistory:
    """
    A class representing the complete submission history of an SEC filing entity.
    """
    cik: str
    entity_type: str
    sic: str
    sic_description: str
    owner_org: str
    insider_transaction_for_owner_exists: bool
    insider_transaction_for_issuer_exists: bool
    name: str
    tickers: List[str]
    exchanges: List[str]
    ein: str
    description: str
    website: str
    investor_website: str
    category: str
    fiscal_year_end: str
    state_of_incorporation: str
    state_of_incorporation_description: str
    addresses: List[Address]
    phone: str
    flags: str
    former_names: List[FormerName]
    filings: List[Filing]
    files: List[File]
    lei: Optional[str] = None

    @classmethod
    def to_object(cls, response: Dict) -> 'SubmissionHistory':
        """
        Parses EDGAR API response and returns a single SubmissionHistory.
        """
        return cls(
            cik=response.get('cik', ''),
            entity_type=response.get('entityType', ''),
            sic=response.get('sic', ''),
            sic_description=response.get('sicDescription', ''),
            owner_org=response.get('ownerOrg', ''),
            insider_transaction_for_owner_exists=bool(response.get('insiderTransactionForOwnerExists', False)),
            insider_transaction_for_issuer_exists=bool(response.get('insiderTransactionForIssuerExists', False)),
            name=response.get('name', ''),
            tickers=list(response.get('tickers', [])),
            exchanges=list(response.get('exchanges', [])),
            ein=response.get('ein', ''),
            lei=response.get('lei', None),
            description=response.get('description', ''),
            website=response.get('website', ''),
            investor_website=response.get('investorWebsite', ''),
            category=response.get('category', ''),
            fiscal_year_end=response.get('fiscalYearEnd', ''),
            state_of_incorporation=response.get('stateOfIncorporation', ''),
            state_of_incorporation_description=response.get('stateOfIncorporationDescription', ''),
            addresses=[Address.to_object(address_type, address_data) for address_type, address_data in response.get('addresses', {}).items()],
            phone=response.get('phone', ''),
            flags=response.get('flags', ''),
            former_names=[FormerName.to_object(former_name_data) for former_name_data in response.get('formerNames', [])],
            filings=[Filing.to_object(response.get('filings', {}).get('recent', {}), i) for i in range(len(response.get('filings', {}).get('recent', {}).get('accessionNumber', [])))],
            files=[File.to_object(file_data) for file_data in response.get('filings', {}).get('files', [])],
        )
    @classmethod
    async def to_object_async(cls, response: Dict) -> 'SubmissionHistory':
        """
        Asynchronously parses EDGAR API response and returns a single SubmissionHistory.
        """
        return cls(
            cik=response.get('cik', ''),
            entity_type=response.get('entityType', ''),
            sic=response.get('sic', ''),
            sic_description=response.get('sicDescription', ''),
            owner_org=response.get('ownerOrg', ''),
            insider_transaction_for_owner_exists=bool(response.get('insiderTransactionForOwnerExists', False)),
            insider_transaction_for_issuer_exists=bool(response.get('insiderTransactionForIssuerExists', False)),
            name=response.get('name', ''),
            tickers=list(response.get('tickers', [])),
            exchanges=list(response.get('exchanges', [])),
            ein=response.get('ein', ''),
            lei=response.get('lei', None),
            description=response.get('description', ''),
            website=response.get('website', ''),
            investor_website=response.get('investorWebsite', ''),
            category=response.get('category', ''),
            fiscal_year_end=response.get('fiscalYearEnd', ''),
            state_of_incorporation=response.get('stateOfIncorporation', ''),
            state_of_incorporation_description=response.get('stateOfIncorporationDescription', ''),
            addresses=[await Address.to_object_async(address_type, address_data) for address_type, address_data in response.get('addresses', {}).items()],
            phone=response.get('phone', ''),
            flags=response.get('flags', ''),
            former_names=[await FormerName.to_object_async(former_name_data) for former_name_data in response.get('formerNames', [])],
            filings=[await Filing.to_object_async(response.get('filings', {}).get('recent', {}), i) for i in range(len(response.get('filings', {}).get('recent', {}).get('accessionNumber', [])))],
            files=[await File.to_object_async(file_data) for file_data in response.get('filings', {}).get('files', [])],
        )

@dataclass
class UnitDisclosure:
    """
    A class representing a specific financial disclosure for a single unit of measurement.
    """
    units: str
    end: str
    val: float
    accn: str
    fy: str
    fp: str
    form: str
    filed: str
    frame: str
    start: Optional[str]

    @classmethod
    def to_object(cls, data: Dict, units: str) -> 'UnitDisclosure':
        """
        Parses a dictionary and returns a UnitDisclosure object.
        """
        return cls(
            units=units,
            end=data.get('end', ''),
            val=float(data.get('val', '')),
            accn=data.get('accn', ''),
            fy=data.get('fy', ''),
            fp=data.get('fp', ''),
            form=data.get('form', ''),
            filed=data.get('filed', ''),
            frame=data.get('frame', ''),
            start=data.get('start', '')
        )
    @classmethod
    async def to_object_async(cls, data: Dict, units: str) -> 'UnitDisclosure':
        """
        Asynchronously parses a dictionary and returns a UnitDisclosure object.
        """
        return await asyncio.to_thread(cls.to_object, data, units)

@dataclass
class CompanyConcept:
    """
    A class representing a specific financial concept for a company from SEC filings.
    """
    cik: str
    taxonomy: str
    tag: str
    label: str
    description: str
    entity_name: str
    units: List[UnitDisclosure]

    @classmethod
    def to_object(cls, response: Dict) -> 'CompanyConcept':
        """
        Parses EDGAR API response and returns a single CompanyConcept.
        """
        return cls(
            cik=str(response.get('cik', '')),
            taxonomy=response.get('taxonomy', ''),
            tag=response.get('tag', ''),
            label=response.get('label', ''),
            description=response.get('description', ''),
            entity_name=response.get('entityName', ''),
            units=[UnitDisclosure.to_object(disclosure, unit_type) for unit_type, disclosures in response.get('units', {}).items() for disclosure in disclosures]
        )
    @classmethod
    async def to_object_async(cls, response: Dict) -> 'CompanyConcept':
        """
        Asynchronously parses EDGAR API response and returns a single CompanyConcept.
        """
        return cls(
            cik=str(response.get('cik', '')),
            taxonomy=response.get('taxonomy', ''),
            tag=response.get('tag', ''),
            label=response.get('label', ''),
            description=response.get('description', ''),
            entity_name=response.get('entityName', ''),
            units=[await UnitDisclosure.to_object_async(disclosure, unit_type) for unit_type, disclosures in response.get('units', {}).items() for disclosure in disclosures]
        )

@dataclass
class TaxonomyDisclosures:
    """
    A class representing a specific financial concept disclosure for an entity.
    """
    name: str
    label: str
    description: str
    units: List[UnitDisclosure]

    @classmethod
    def to_object(cls, data: Dict, name: str) -> 'TaxonomyDisclosures':
        """
        Parses an entity disclosure from the API response.
        """
        return cls(
            name=name,
            label=data.get('label', ''),
            description=data.get('description', ''),
            units=[UnitDisclosure.to_object(disclosure, unit_type) for unit_type, disclosures in data.get('units', {}).items() for disclosure in disclosures]
        )
    @classmethod
    async def to_object_async(cls, data: Dict, name: str) -> 'TaxonomyDisclosures':
        """
        Asynchronously parses an entity disclosure from the API response.
        """
        return cls(
            name=name,
            label=data.get('label', ''),
            description=data.get('description', ''),
            units=[await UnitDisclosure.to_object_async(disclosure, unit_type) for unit_type, disclosures in data.get('units', {}).items() for disclosure in disclosures]
        )

@dataclass
class TaxonomyFacts:
    """
    A class representing a collection of financial disclosures for a specific taxonomy.
    """
    taxonomy: str
    disclosures: List[TaxonomyDisclosures]

    @classmethod
    def to_object(cls, data: Dict, taxonomy: str) -> 'TaxonomyFacts':
        """
        Parses a taxonomy fact from the API response.
        """
        return cls(
            taxonomy=taxonomy,
            disclosures=[TaxonomyDisclosures.to_object(tag_data, tag_name) for tag_name, tag_data in data.items()]
        )
    @classmethod
    async def to_object_async(cls, data: Dict, taxonomy: str) -> 'TaxonomyFacts':
        """
        Asynchronously parses a taxonomy fact from the API response.
        """
        return cls(
            taxonomy=taxonomy,
            disclosures=[await TaxonomyDisclosures.to_object_async(tag_data, tag_name) for tag_name, tag_data in data.items()]
        )

@dataclass
class CompanyFacts:
    """
    A class representing the complete collection of financial facts for a company from SEC filings.
    """
    cik: str
    entity_name: str
    facts: List[TaxonomyFacts]

    @classmethod
    def to_object(cls, response: Dict) -> 'CompanyFacts':
        """
        Parses EDGAR API response and returns a single CompanyFacts.
        """
        return cls(
            cik=str(response.get('cik', '')),
            entity_name=response.get('entityName', ''),
            facts=[TaxonomyFacts.to_object(taxonomy_data, taxonomy) for taxonomy, taxonomy_data in response.get('facts', {}).items()]
        )
    @classmethod
    async def to_object_async(cls, response: Dict) -> 'CompanyFacts':
        """
        Asynchronously parses EDGAR API response and returns a single CompanyFacts.
        """
        return cls(
            cik=str(response.get('cik', '')),
            entity_name=response.get('entityName', ''),
            facts=[await TaxonomyFacts.to_object_async(taxonomy_data, taxonomy) for taxonomy, taxonomy_data in response.get('facts', {}).items()]
        )

@dataclass
class FrameDisclosure:
    """
    A class representing a single financial disclosure from an SEC reporting frame.
    """
    accn: str
    cik: str
    entity_name: str
    loc: str
    end: str
    val: float

    @classmethod
    def to_object(cls, data: Dict) -> 'FrameDisclosure':
        """
        Parses a frame disclosure from the API response.
        """
        return cls(
            accn=data.get('accn', ''),
            cik=str(data.get('cik', '')),
            entity_name=data.get('entityName', ''),
            loc=data.get('loc', ''),
            end=data.get('end', ''),
            val=float(data.get('val', ''))
        )
    @classmethod
    async def to_object_async(cls, data: Dict) -> 'FrameDisclosure':
        """
        Asynchronously parses a frame disclosure from the API response.
        """
        return await asyncio.to_thread(cls.to_object, data)

@dataclass
class Frame:
    """
    A class representing a collection of financial disclosures across multiple companies for a specific concept and time period.
    """
    taxonomy: str
    tag: str
    ccp: str
    uom: str
    label: str
    description: str
    pts: int
    disclosures: List[FrameDisclosure]

    @classmethod
    def to_object(cls, response: Dict) -> 'Frame':
        """
        Parses a dictionary and returns a Frame object.
        """
        return cls(
            taxonomy=response.get('taxonomy', ''),
            tag=response.get('tag', ''),
            ccp=response.get('ccp', ''),
            uom=response.get('uom', ''),
            label=response.get('label', ''),
            description=response.get('description', ''),
            pts=int(response.get('pts', 0)),
            disclosures=[FrameDisclosure.to_object(disclosure_data) for disclosure_data in response.get('data', [])]
        )
    @classmethod
    async def to_object_async(cls, response: Dict) -> 'Frame':
        """
        Asynchronously parses a dictionary and returns a Frame object.
        """
        return cls(
            taxonomy=response.get('taxonomy', ''),
            tag=response.get('tag', ''),
            ccp=response.get('ccp', ''),
            uom=response.get('uom', ''),
            label=response.get('label', ''),
            description=response.get('description', ''),
            pts=int(response.get('pts', 0)),
            disclosures=[await FrameDisclosure.to_object_async(disclosure_data) for disclosure_data in response.get('data', [])]
        )

@dataclass
class Company:
    """A class representing a company in the Edgar SEC database.

    Attributes:
        cik (str): The Central Index Key (CIK) of the company.
        ticker (str): The stock ticker symbol of the company.
        title (str): The name of the company.
    """
    cik: str
    ticker: str
    title: str

    @classmethod
    def to_object(cls, data: dict) -> 'Company':
        """
        Create a Company instance from a dictionary.
        """
        return cls(
            cik=str(data.get('cik_str', '')),
            ticker=data.get('ticker', ''),
            title=data.get('title', '')
        )
    @classmethod
    async def to_object_async(cls, data: dict) -> 'Company':
        """
        Asynchronously create a Company instance from a dictionary.
        """
        return await asyncio.to_thread(cls.to_object, data)
