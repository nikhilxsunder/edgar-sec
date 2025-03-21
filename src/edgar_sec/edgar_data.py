"""
Type stub file for edgar_data module.
"""
from dataclasses import dataclass
from typing import List, Union, Dict

@dataclass
class Address:
    """A class representing an address from SEC filing data.

    Attributes:
        address_type (str): The type of address (e.g., 'mailing', 'business').
        street1 (str): The primary street address line.
        street2 (str): The secondary street address line, if any.
        city (str): The city name.
        state_or_country (str): The state or country code.
        zipcode (str): The postal code.
        state_or_country_description (str): The full name of the state or country.

    Returns:
        Address: An object containing formatted address information.

    Note:
        The address_type is typically provided by the key name in the SEC API
        response and is passed separately to the from_dict method.
    """
    address_type: str
    street1: str
    street2: str
    city: str
    state_or_country: str
    zipcode: str
    state_or_country_description: str

    @classmethod
    def from_dict(cls, address_type: str, data: Dict) -> 'Address':
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
            state_or_country_description=data['stateOrCountryDescription']
        )

@dataclass
class FormerName:
    """A class representing a former name of an SEC filing entity.

    Attributes:
        name (str): The previous company name.
        from_date (str): The date when the company began using this name, in YYYY-MM-DD format.
        to_date (str): The date when the company stopped using this name, in YYYY-MM-DD format. May be empty if still in use.

    Returns:
        FormerName: An object containing information about a company's previous name.

    Note:
        This class is typically used when parsing company submission history
        where entities may have changed their names over time. The from_dict method
        handles the API's naming convention where the start date is called 'from'.
    """
    name: str
    from_date: str
    to_date: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'FormerName':
        """
        Parses a dictionary and returns a FormerName object.
        """
        return cls(
            name=data['name'],
            from_date=data['from'],
            to_date=data.get('to', '')
        )

@dataclass
class Filing:
    """A class representing an SEC filing document.

    Attributes:
        accession_number (str): Unique identifier for the filing in the format XXXXXXXXXX-XX-XXXXXX.
        filing_date (str): The date when the filing was submitted to the SEC, in YYYY-MM-DD format.
        report_date (str): The date of the reporting period covered by the filing, in YYYY-MM-DD format.
        acceptance_date_time (str): The date and time when the filing was accepted by the SEC.
        act (str): The securities act (e.g., '33', '34') under which the filing was submitted.
        form (str): The form type (e.g., '10-K', '10-Q', '8-K') of the filing.
        file_number (str): SEC file number assigned to the registrant.
        film_number (str): Film number assigned to the submission.
        items (Union[str, List[str]]): The specific items being reported in the filing.
        core_type (str): The core financial statement disclosure type.
        size (int): The size of the filing document in bytes.
        is_xbrl (bool): Whether the filing includes XBRL data.
        is_inline_xbrl (bool): Whether the filing uses inline XBRL format.
        primary_document (str): The filename of the primary document in the submission.
        primary_doc_description (str): Description of the primary document.

    Returns:
        Filing: An object containing information about an SEC filing document.

    Note:
        Form types include annual reports (10-K), quarterly reports (10-Q),
        current reports (8-K), and various other registration and disclosure forms.
    """
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
    def from_dict(cls, data: Dict) -> 'Filing':
        """
        Parses a dictionary and returns a Filing object.
        """
        return cls(
            accession_number=data['accessionNumber'],
            filing_date=data['filingDate'],
            report_date=data['reportDate'],
            acceptance_date_time=data['acceptanceDateTime'],
            act=data['act'],
            form=data['form'],
            file_number=data['fileNumber'],
            film_number=data['filmNumber'],
            items=data['items'],
            core_type=data.get('core_type', ''),
            size=int(data.get('size', 0)),
            is_xbrl=bool(data.get('isXBRL', False)),
            is_inline_xbrl=bool(data.get('isInlineXBRL', False)),
            primary_document=data.get('primaryDocument', ''),
            primary_doc_description=data.get('primaryDocDescription', '')
        )

@dataclass
class File:
    """A class representing a file reference in SEC EDGAR submission history.

    Attributes:
        name (str): The filename of the additional submission history file.
        filing_count (int): The number of filings contained in the referenced file.
        filing_from (str): The earliest filing date covered in this file, in YYYY-MM-DD format.
        filing_to (str): The latest filing date covered in this file, in YYYY-MM-DD format.

    Returns:
        File: An object containing information about a submission history file reference.

    Note:
        The SEC EDGAR API typically returns the most recent submissions directly
        in the response, with references to additional JSON files for older
        submissions. These file references can be used to retrieve the complete
        filing history for entities with extensive submissions.
    """
    name: str
    filing_count: int
    filing_from: str
    filing_to: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'File':
        """
        Parses a dictionary and returns a File object.
        """
        return cls(
            name=data['name'],
            filing_count=int(data['filingCount']),
            filing_from=data['filingFrom'],
            filing_to=data['filingTo']
        )

@dataclass
class SubmissionHistory:
    """A class representing the complete submission history of an SEC filing entity.

    Attributes:
        cik (str): Central Index Key (CIK) of the entity, a unique identifier assigned by the SEC.
        entity_type (str): The type of entity (e.g., 'operating', 'investment-company', 'private').
        sic (str): Standard Industrial Classification (SIC) code.
        sic_description (str): Text description of the SIC code.
        owner_org (str): Name of the organization if this entity is an owner.
        insider_transaction_for_owner_exists (bool): Whether insider transactions exist for this entity as an owner.
        insider_transaction_for_issuer_exists (bool): Whether insider transactions exist for this entity as an issuer.
        name (str): Legal name of the entity.
        tickers (Union[str, List[str]]): Stock ticker symbol(s) for the entity.
        exchanges (Union[str, List[str]]): Stock exchange(s) where the entity is listed.
        ein (str): Employer Identification Number, a tax ID number.
        description (str): Business description of the entity.
        website (str): The entity's primary website.
        investor_website (str): The entity's investor relations website.
        category (str): SEC category classification.
        fiscal_year_end (str): Month and day of the entity's fiscal year end (MM-DD format).
        state_of_incorporation (str): State or country code where the entity is incorporated.
        state_of_incorporation_description (str): Full name of the state or country of incorporation.
        addresses (Union[Address, List[Address]]): Mailing and business addresses for the entity.
        phone (str): Contact phone number.
        flags (Union[str, List[str]]): Special flags or indicators about the entity.
        former_names (Union[FormerName, List[FormerName]]): Previous names of the entity.
        filings (Union[Filing, List[Filing]]): Recent SEC filings by the entity.
        files (Union[File, List[File]]): References to additional files containing older filings.

    Returns:
        SubmissionHistory: An object containing comprehensive information about an entity's filing history and profile.

    Note:
        This class provides a comprehensive view of an entity's profile and filing
        history as maintained by the SEC. It includes both the entity's current
        information and a record of its historical filings and name changes.
    """
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
    def from_api_response(cls, response: Dict) -> 'SubmissionHistory':
        """
        Parses EDGAR API response and returns a single SubmissionHistory.
        """
        tickers = response.get('tickers', [])
        if isinstance(tickers, list) and len(tickers) == 1:
            tickers = tickers[0]
        exchanges = response.get('exchanges', [])
        if isinstance(exchanges, list) and len(exchanges) == 1:
            exchanges = exchanges[0]
        flags = response.get('flags', [])
        if isinstance(flags, list) and len(flags) == 1:
            flags = flags[0]
        raw_addresses = response.get('addresses', {})
        addresses = [
            Address.from_dict(address_type, address_data)
            for address_type, address_data in raw_addresses.items()
        ]
        if len(addresses) == 1:
            addresses = [addresses[0]]
        raw_former_names = response.get('formerNames', [])
        former_names = [
            FormerName.from_dict(former_name_data)
            for former_name_data in raw_former_names
        ]
        if len(former_names) == 1:
            former_names = [former_names[0]]
        elif not raw_former_names:
            former_names = []
        filings = []
        raw_filings = response.get('filings', {}).get('recent', {})
        if raw_filings:
            num_filings = len(raw_filings.get('accessionNumber', []))
            for i in range(num_filings):
                filing = Filing(
                    accession_number=raw_filings.get('accessionNumber', [])[i] if i < len(raw_filings.get('accessionNumber', [])) else '',
                    filing_date=raw_filings.get('filingDate', [])[i] if i < len(raw_filings.get('filingDate', [])) else '',
                    report_date=raw_filings.get('reportDate', [])[i] if i < len(raw_filings.get('reportDate', [])) else '',
                    acceptance_date_time=raw_filings.get('acceptanceDateTime', [])[i] if i < len(raw_filings.get('acceptanceDateTime', [])) else '',
                    act=raw_filings.get('act', [])[i] if i < len(raw_filings.get('act', [])) else '',
                    form=raw_filings.get('form', [])[i] if i < len(raw_filings.get('form', [])) else '',
                    file_number=raw_filings.get('fileNumber', [])[i] if i < len(raw_filings.get('fileNumber', [])) else '',
                    film_number=raw_filings.get('filmNumber', [])[i] if i < len(raw_filings.get('filmNumber', [])) else '',
                    items=raw_filings.get('items', [])[i] if i < len(raw_filings.get('items', [])) else '',
                    core_type=raw_filings.get('core_type', [])[i] if i < len(raw_filings.get('core_type', [])) else '',
                    size=int(raw_filings.get('size', [])[i]) if i < len(raw_filings.get('size', [])) else 0,
                    is_xbrl=bool(raw_filings.get('isXBRL', [])[i]) if i < len(raw_filings.get('isXBRL', [])) else False,
                    is_inline_xbrl=bool(raw_filings.get('isInlineXBRL', [])[i]) if i < len(raw_filings.get('isInlineXBRL', [])) else False,
                    primary_document=raw_filings.get('primaryDocument', [])[i] if i < len(raw_filings.get('primaryDocument', [])) else '',
                    primary_doc_description=raw_filings.get('primaryDocDescription', [])[i] if i < len(raw_filings.get('primaryDocDescription', [])) else ''
                )
                filings.append(filing)
        if len(filings) == 1:
            filings = [filings[0]]
        raw_files = response.get('files', [])
        files = [File.from_dict(file_data) for file_data in raw_files]
        if len(files) == 1:
            files = [files[0]]
        elif not raw_files:
            files = []
        return cls(
            cik=response.get('cik', ''),
            entity_type=response.get('entityType', ''),
            sic=response.get('sic', ''),
            sic_description=response.get('sicDescription', ''),
            owner_org=response.get('ownerOrg', ''),
            insider_transaction_for_owner_exists=bool(response.get('insiderTransactionForOwnerExists', False)),
            insider_transaction_for_issuer_exists=bool(response.get('insiderTransactionForIssuerExists', False)),
            name=response.get('name', ''),
            tickers=tickers,
            exchanges=exchanges,
            ein=response.get('ein', ''),
            description=response.get('description', ''),
            website=response.get('website', ''),
            investor_website=response.get('investorWebsite', ''),
            category=response.get('category', ''),
            fiscal_year_end=response.get('fiscalYearEnd', ''),
            state_of_incorporation=response.get('stateOfIncorporation', ''),
            state_of_incorporation_description=response.get('stateOfIncorporationDescription', ''),
            addresses=addresses,
            phone=response.get('phone', ''),
            flags=flags,
            former_names=former_names,
            filings=filings,
            files=files
        )

@dataclass
class UnitDisclosure:
    """A class representing a specific financial disclosure for a single unit of measurement.

    Attributes:
        unit (str): The unit of measurement for the disclosed value (e.g., 'USD', 'shares', 'USD-per-shares').
        end (str): The end date of the reporting period, in YYYY-MM-DD format.
        val (int): The numerical value of the disclosure.
        accn (str): The accession number of the filing containing this disclosure.
        fy (str): The fiscal year of the disclosure in the format YYYY.
        fp (str): The fiscal period code (e.g., 'Q1', 'Q2', 'Q3', 'FY' for annual).
        form (str): The SEC form type containing this disclosure (e.g., '10-K', '10-Q').
        filed (str): The date the filing was submitted to the SEC, in YYYY-MM-DD format.
        frame (str): The financial reporting framework reference (e.g., 'CY2022Q1I').
        start (str): The start date of the reporting period, in YYYY-MM-DD format. Empty for point-in-time disclosures.

    Returns:
        UnitDisclosure: An object containing a single financial disclosure value and its metadata.

    Note:
        SEC data often includes both instantaneous values (like assets at a point in time)
        and period values (like revenue for a quarter). When the disclosure represents a
        period, both start and end dates will be populated. For point-in-time disclosures,
        start will be empty.
    """
    unit: str
    end: str
    val: int
    accn: str
    fy: str
    fp: str
    form: str
    filed: str
    frame: str
    start: str = ''

    @classmethod
    def from_dict(cls, data: Dict) -> 'UnitDisclosure':
        """
        Parses a dictionary and returns a UnitDisclosure object.
        """
        return cls(
            unit=data.get('unit', ''),
            end=data.get('end', ''),
            val=int(data.get('val', '')),
            accn=data.get('accn', ''),
            fy=data.get('fy', ''),
            fp=data.get('fp', ''),
            form=data.get('form', ''),
            filed=data.get('filed', ''),
            frame=data.get('frame', ''),
            start=data.get('start', '')
        )

@dataclass
class CompanyConcept:
    """A class representing a specific financial concept for a company from SEC filings.

    Attributes:
        cik (str): Central Index Key (CIK) of the entity, a unique identifier assigned by the SEC.
        taxonomy (str): The reporting taxonomy used (e.g., 'us-gaap', 'dei', 'srt').
        tag (str): The specific concept tag or account name (e.g., 'Assets', 'Revenue', 'EarningsPerShare').
        label (str): Human-readable label describing the financial concept.
        description (str): Detailed explanation of what the financial concept represents.
        entity_name (str): Legal name of the reporting entity.
        units (Union[UnitDisclosure, List[UnitDisclosure]]): Individual disclosure values across different time periods.

    Returns:
        CompanyConcept: An object containing all instances of a specific financial concept reported by a company.

    Note:
        This class provides time-series data for a single financial concept across
        multiple reporting periods. The taxonomy and tag parameters define which
        specific financial data point is being represented. Common taxonomies include
        'us-gaap' (US GAAP accounting standards), 'ifrs' (International standards),
        and 'dei' (Document and Entity Information).
    """
    cik: str
    taxonomy: str
    tag: str
    label: str
    description: str
    entity_name: str
    units: Union[UnitDisclosure, List[UnitDisclosure]]

    @classmethod
    def from_api_response(cls, response: Dict) -> 'CompanyConcept':
        """
        Parses EDGAR API response and returns a single CompanyConcept.
        """
        units_list = []
        raw_units = response.get('units', {})
        for unit_type, disclosures in raw_units.items():
            for disclosure in disclosures:
                disclosure_with_unit = disclosure.copy()
                disclosure_with_unit['unit'] = unit_type
                units_list.append(UnitDisclosure.from_dict(disclosure_with_unit))
        if not units_list:
            units: List[UnitDisclosure] = []
        elif len(units_list) == 1:
            units = [units_list[0]]
        else:
            units = units_list
        return cls(
            cik=str(response.get('cik', '')),
            taxonomy=response.get('taxonomy', ''),
            tag=response.get('tag', ''),
            label=response.get('label', ''),
            description=response.get('description', ''),
            entity_name=response.get('entityName', ''),
            units=units
        )

@dataclass
class EntityDisclosure:
    """A class representing a specific financial concept disclosure for an entity.

    Attributes:
        name (str): The name of the concept tag (e.g., 'Assets', 'Revenue', 'CommonStockSharesOutstanding').
        label (str): Human-readable label describing the financial concept.
        description (str): Detailed explanation of what the financial concept represents.
        units (Dict[str, List[UnitDisclosure]]): A dictionary mapping unit types to lists of disclosure values across different reporting periods.

    Returns:
        EntityDisclosure: An object containing all disclosures of a specific financial concept, organized by unit type.

    Note:
        This class organizes financial concept data by unit of measurement (like USD, shares, etc.)
        to accommodate concepts that might be reported in multiple units across different periods.
        The name parameter represents the specific XBRL tag or concept identifier.
    """
    name: str
    label: str
    description: str
    units: Dict[str, List[UnitDisclosure]]

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> 'EntityDisclosure':
        """
        Parses an entity disclosure from the API response.
        """
        units_dict = {}
        raw_units = data.get('units', {})
        for unit_type, disclosures in raw_units.items():
            units_list = []
            for disclosure in disclosures:
                disclosure_with_unit = disclosure.copy()
                disclosure_with_unit['unit'] = unit_type
                units_list.append(UnitDisclosure.from_dict(disclosure_with_unit))
            units_dict[unit_type] = units_list
        return cls(
            name=name,
            label=data.get('label', ''),
            description=data.get('description', ''),
            units=units_dict
        )

@dataclass
class Fact:
    """A class representing a collection of financial disclosures for a specific taxonomy.

    Attributes:
        taxonomy (str): The reporting taxonomy identifier (e.g., 'us-gaap', 'dei', 'ifrs').
        disclosures (Dict[str, EntityDisclosure]): A dictionary mapping concept tag names to their corresponding disclosure objects.

    Returns:
        Fact: An object containing all disclosures within a specific taxonomy for an entity.

    Note:
        This class organizes financial data hierarchically by taxonomy, representing
        a collection of related financial concepts under a specific accounting standard
        or reporting framework. Common taxonomies include 'us-gaap' (US GAAP accounting
        standards), 'ifrs' (International standards), and 'dei' (Document and Entity
        Information).
    """
    taxonomy: str
    disclosures: Dict[str, EntityDisclosure]

    @classmethod
    def from_dict(cls, taxonomy: str, data: Dict) -> 'Fact':
        """
        Parses a taxonomy fact from the API response.
        """
        disclosures = {}
        for tag_name, tag_data in data.items():
            disclosures[tag_name] = EntityDisclosure.from_dict(tag_name, tag_data)
        return cls(
            taxonomy=taxonomy,
            disclosures=disclosures
        )

@dataclass
class CompanyFact:
    """A class representing the complete collection of financial facts for a company from SEC filings.

    Attributes:
        cik (str): Central Index Key (CIK) of the entity, a unique identifier assigned by the SEC.
        entity_name (str): Legal name of the reporting entity.
        facts (Dict[str, Fact]): A dictionary mapping taxonomy identifiers to their corresponding Fact objects.

    Returns:
        CompanyFact: An object containing all financial facts reported by a company across all taxonomies.

    Note:
        This class represents the highest level container for all financial data for a company,
        organized hierarchically by taxonomy, concept, and unit. It provides access to the
        complete set of financial disclosures that an entity has filed with the SEC in
        machine-readable XBRL format, enabling time-series analysis of financial metrics.
    """
    cik: str
    entity_name: str
    facts: Dict[str, Fact]
    @classmethod
    def from_api_response(cls, response: Dict) -> 'CompanyFact':
        """
        Parses EDGAR API response and returns a single CompanyFacts.
        """
        facts_dict = {}
        facts_data = response.get('facts', {})
        for taxonomy, taxonomy_data in facts_data.items():
            facts_dict[taxonomy] = Fact.from_dict(taxonomy, taxonomy_data)
        return cls(
            cik=str(response.get('cik', '')),
            entity_name=response.get('entityName', ''),
            facts=facts_dict
        )

@dataclass
class FrameDisclosure:
    """A class representing a single financial disclosure from an SEC reporting frame.

    Attributes:
        accn (str): Accession number of the filing containing this disclosure.
        cik (str): Central Index Key (CIK) of the entity making the disclosure.
        entity_name (str): Legal name of the reporting entity.
        loc (str): Location identifier for the disclosure within the filing document.
        end (str): The end date of the reporting period, in YYYY-MM-DD format.
        val (int): The numerical value of the disclosure.

    Returns:
        FrameDisclosure: An object containing a single financial disclosure value and its metadata.

    Note:
        Frame disclosures represent point-in-time snapshots of financial data that allow for
        comparison across multiple companies for the same time period and concept. Unlike
        CompanyConcept objects which show time-series data for a single company, frames provide
        cross-sectional data across multiple companies at a specific point in time.
    """
    accn: str
    cik: str
    entity_name: str
    loc: str
    end: str
    val: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'FrameDisclosure':
        """
        Parses a frame disclosure from the API response.
        """
        return cls(
            accn=data.get('accn', ''),
            cik=str(data.get('cik', '')),
            entity_name=data.get('entityName', ''),
            loc=data.get('loc', ''),
            end=data.get('end', ''),
            val=int(data.get('val', 0))
        )

@dataclass
class Frame:
    """A class representing a collection of financial disclosures across multiple companies for a specific concept and time period.

    Attributes:
        taxonomy (str): The reporting taxonomy identifier (e.g., 'us-gaap', 'dei', 'ifrs').
        tag (str): The specific concept tag or account name (e.g., 'Assets', 'Revenue', 'EarningsPerShare').
        ccp (str): The calculation context parameter defining the reporting context.
        uom (str): The unit of measurement (e.g., 'USD', 'shares', 'USD/shares').
        label (str): Human-readable label describing the financial concept.
        description (str): Detailed explanation of what the financial concept represents.
        pts (int): The number of reporting entities (points) included in the frame.
        frames (List[FrameDisclosure]): A list of individual company disclosures for the concept and time period.

    Returns:
        Frame: An object containing comparable financial disclosures across multiple companies.

    Note:
        Frames are particularly useful for cross-sectional analysis, benchmarking, and
        comparative studies as they provide standardized financial data for multiple companies
        at the same point in time. The frame identifier (ccp) typically includes the calendar
        year, quarter, and whether the value is instantaneous (I) or for a duration (D).
    """
    taxonomy: str
    tag: str
    ccp: str
    uom: str
    label: str
    description: str
    pts: int
    frames: List[FrameDisclosure]

    @classmethod
    def from_api_response(cls, response: Dict) -> 'Frame':
        """
        Parses a dictionary and returns a Frame object.
        """
        frame_disclosures = []
        raw_data = response.get('data', [])
        for disclosure_data in raw_data:
            frame_disclosures.append(FrameDisclosure.from_dict(disclosure_data))
        frames = frame_disclosures
        return cls(
            taxonomy=response.get('taxonomy', ''),
            tag=response.get('tag', ''),
            ccp=response.get('ccp', ''),
            uom=response.get('uom', ''),
            label=response.get('label', ''),
            description=response.get('description', ''),
            pts=int(response.get('pts', 0)),
            frames=frames
        )
