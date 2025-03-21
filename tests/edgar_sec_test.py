import pytest
from edgar_sec.edgar_data import (
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
    FrameDisclosure,
    Frame
)

class TestAddressClass:
    """Test cases for the Address class."""

    def test_from_dict(self):
        """Test creating an Address object from a dictionary."""
        address_dict = {
            "street1": "1 Apple Park Way",
            "street2": "Building 1",
            "city": "Cupertino",
            "stateOrCountry": "CA",
            "zipCode": "95014",
            "stateOrCountryDescription": "CALIFORNIA"
        }

        address = Address.from_dict("business", address_dict)

        assert address.address_type == "business"
        assert address.street1 == "1 Apple Park Way"
        assert address.street2 == "Building 1"
        assert address.city == "Cupertino"
        assert address.state_or_country == "CA"
        assert address.zipcode == "95014"
        assert address.state_or_country_description == "CALIFORNIA"

    def test_from_dict_missing_street2(self):
        """Test handling missing optional street2 field."""
        address_dict = {
            "street1": "1 Apple Park Way",
            "city": "Cupertino",
            "stateOrCountry": "CA",
            "zipCode": "95014",
            "stateOrCountryDescription": "CALIFORNIA"
        }

        address = Address.from_dict("business", address_dict)
        assert address.street2 == ""


class TestFormerNameClass:
    """Test cases for the FormerName class."""

    def test_from_dict(self):
        """Test creating a FormerName object from a dictionary."""
        former_name_dict = {
            "name": "Apple Computer, Inc.",
            "from": "1976-04-01",
            "to": "2007-01-09"
        }

        former_name = FormerName.from_dict(former_name_dict)

        assert former_name.name == "Apple Computer, Inc."
        assert former_name.from_date == "1976-04-01"
        assert former_name.to_date == "2007-01-09"

    def test_from_dict_missing_to_date(self):
        """Test handling missing optional to field."""
        former_name_dict = {
            "name": "Apple Computer, Inc.",
            "from": "1976-04-01"
        }

        former_name = FormerName.from_dict(former_name_dict)
        assert former_name.to_date == ""


class TestFilingClass:
    """Test cases for the Filing class."""

    def test_from_dict(self):
        """Test creating a Filing object from a dictionary."""
        filing_dict = {
            "accessionNumber": "0000320193-22-000001",
            "filingDate": "2022-01-28",
            "reportDate": "2021-12-25",
            "acceptanceDateTime": "2022-01-28T16:09:16.000Z",
            "act": "34",
            "form": "10-Q",
            "fileNumber": "001-36743",
            "filmNumber": "22555717",
            "items": ["7.01", "9.01"],
            "size": 8888888,
            "isXBRL": True,
            "isInlineXBRL": True,
            "primaryDocument": "q1-2022.htm",
            "primaryDocDescription": "Form 10-Q"
        }

        filing = Filing.from_dict(filing_dict)

        assert filing.accession_number == "0000320193-22-000001"
        assert filing.filing_date == "2022-01-28"
        assert filing.report_date == "2021-12-25"
        assert filing.form == "10-Q"
        assert filing.items == ["7.01", "9.01"]
        assert filing.size == 8888888
        assert filing.is_xbrl is True
        assert filing.is_inline_xbrl is True
        assert filing.primary_document == "q1-2022.htm"


class TestFileClass:
    """Test cases for the File class."""

    def test_from_dict(self):
        """Test creating a File object from a dictionary."""
        file_dict = {
            "name": "CIK0000320193-submissions-001.json",
            "filingCount": 100,
            "filingFrom": "2020-01-01",
            "filingTo": "2021-01-01"
        }

        file_obj = File.from_dict(file_dict)

        assert file_obj.name == "CIK0000320193-submissions-001.json"
        assert file_obj.filing_count == 100
        assert file_obj.filing_from == "2020-01-01"
        assert file_obj.filing_to == "2021-01-01"


class TestSubmissionHistoryClass:
    """Test cases for the SubmissionHistory class."""

    def test_from_api_response_minimal(self):
        """Test creating a SubmissionHistory object from a minimal API response."""
        response = {
            "cik": "0000320193",
            "entityType": "operating",
            "sic": "3571",
            "sicDescription": "ELECTRONIC COMPUTERS",
            "name": "Apple Inc.",
            "tickers": ["AAPL"],
            "exchanges": ["NASDAQ"]
        }

        history = SubmissionHistory.from_api_response(response)

        assert history.cik == "0000320193"
        assert history.entity_type == "operating"
        assert history.sic == "3571"
        assert history.name == "Apple Inc."
        assert history.tickers == "AAPL"  # Single item list converts to string
        assert history.exchanges == "NASDAQ"

    def test_from_api_response_full(self):
        """Test creating a SubmissionHistory object from a complete API response."""
        response = {
            "cik": "0000320193",
            "entityType": "operating",
            "sic": "3571",
            "sicDescription": "ELECTRONIC COMPUTERS",
            "name": "Apple Inc.",
            "tickers": ["AAPL", "APPL"],  # Multiple tickers
            "exchanges": ["NASDAQ"],
            "addresses": {
                "business": {
                    "street1": "1 Apple Park Way",
                    "city": "Cupertino",
                    "stateOrCountry": "CA",
                    "zipCode": "95014",
                    "stateOrCountryDescription": "CALIFORNIA"
                }
            },
            "filings": {
                "recent": {
                    "accessionNumber": ["0000320193-22-000001"],
                    "filingDate": ["2022-01-28"],
                    "reportDate": ["2021-12-25"],
                    "acceptanceDateTime": ["2022-01-28T16:09:16.000Z"],
                    "act": ["34"],
                    "form": ["10-Q"],
                    "fileNumber": ["001-36743"],
                    "filmNumber": ["22555717"],
                    "items": [""],
                    "size": [8888888],
                    "isXBRL": [1],
                    "isInlineXBRL": [1],
                    "primaryDocument": ["q1-2022.htm"],
                    "primaryDocDescription": ["10-Q"]
                }
            }
        }

        history = SubmissionHistory.from_api_response(response)

        assert history.cik == "0000320193"
        assert history.name == "Apple Inc."
        assert history.tickers == ["AAPL", "APPL"]  # Multiple items stay as list
        assert len(history.addresses) == 1
        assert len(history.filings) == 1
        assert history.filings[0].form == "10-Q"


class TestUnitDisclosureClass:
    """Test cases for the UnitDisclosure class."""

    def test_from_dict(self):
        """Test creating a UnitDisclosure object from a dictionary."""
        disclosure_dict = {
            "unit": "USD",
            "end": "2021-12-25",
            "val": 54763000000,
            "accn": "0000320193-22-000001",
            "fy": "2022",
            "fp": "Q1",
            "form": "10-Q",
            "filed": "2022-01-28",
            "frame": "CY2021Q4I",
            "start": "2021-09-26"
        }

        disclosure = UnitDisclosure.from_dict(disclosure_dict)

        assert disclosure.unit == "USD"
        assert disclosure.end == "2021-12-25"
        assert disclosure.val == 54763000000
        assert disclosure.accn == "0000320193-22-000001"
        assert disclosure.fy == "2022"
        assert disclosure.fp == "Q1"
        assert disclosure.form == "10-Q"
        assert disclosure.filed == "2022-01-28"
        assert disclosure.frame == "CY2021Q4I"
        assert disclosure.start == "2021-09-26"

    def test_from_dict_missing_start(self):
        """Test handling missing optional start field."""
        disclosure_dict = {
            "unit": "USD",
            "end": "2021-12-25",
            "val": 54763000000,
            "accn": "0000320193-22-000001",
            "fy": "2022",
            "fp": "Q1",
            "form": "10-Q",
            "filed": "2022-01-28",
            "frame": "CY2021Q4I"
        }

        disclosure = UnitDisclosure.from_dict(disclosure_dict)
        assert disclosure.start == ""


class TestCompanyConceptClass:
    """Test cases for the CompanyConcept class."""

    def test_from_api_response(self):
        """Test creating a CompanyConcept object from an API response."""
        response = {
            "cik": "0000320193",
            "taxonomy": "us-gaap",
            "tag": "AccountsPayableCurrent",
            "label": "Accounts Payable, Current",
            "description": "Carrying value of obligations incurred and payable to vendors",
            "entityName": "Apple Inc.",
            "units": {
                "USD": [
                    {
                        "end": "2021-12-25",
                        "val": 54763000000,
                        "accn": "0000320193-22-000001",
                        "fy": "2022",
                        "fp": "Q1",
                        "form": "10-Q",
                        "filed": "2022-01-28",
                        "frame": "CY2021Q4I"
                    }
                ]
            }
        }

        concept = CompanyConcept.from_api_response(response)

        assert concept.cik == "0000320193"
        assert concept.taxonomy == "us-gaap"
        assert concept.tag == "AccountsPayableCurrent"
        assert concept.label == "Accounts Payable, Current"
        assert concept.entity_name == "Apple Inc."
        assert len(concept.units) == 1
        assert concept.units[0].unit == "USD"
        assert concept.units[0].val == 54763000000


class TestEntityDisclosureClass:
    """Test cases for the EntityDisclosure class."""

    def test_from_dict(self):
        """Test creating an EntityDisclosure object from a dictionary."""
        disclosure_dict = {
            "label": "Accounts Payable, Current",
            "description": "Carrying value of obligations incurred and payable to vendors",
            "units": {
                "USD": [
                    {
                        "end": "2021-12-25",
                        "val": 54763000000,
                        "accn": "0000320193-22-000001",
                        "fy": "2022",
                        "fp": "Q1",
                        "form": "10-Q",
                        "filed": "2022-01-28",
                        "frame": "CY2021Q4I"
                    }
                ]
            }
        }

        entity_disclosure = EntityDisclosure.from_dict("AccountsPayableCurrent", disclosure_dict)

        assert entity_disclosure.name == "AccountsPayableCurrent"
        assert entity_disclosure.label == "Accounts Payable, Current"
        assert entity_disclosure.description == "Carrying value of obligations incurred and payable to vendors"
        assert "USD" in entity_disclosure.units
        assert len(entity_disclosure.units["USD"]) == 1
        assert entity_disclosure.units["USD"][0].val == 54763000000


class TestFactClass:
    """Test cases for the Fact class."""

    def test_from_dict(self):
        """Test creating a Fact object from a dictionary."""
        fact_dict = {
            "AccountsPayableCurrent": {
                "label": "Accounts Payable, Current",
                "description": "Carrying value of obligations incurred and payable to vendors",
                "units": {
                    "USD": [
                        {
                            "end": "2021-12-25",
                            "val": 54763000000,
                            "accn": "0000320193-22-000001",
                            "fy": "2022",
                            "fp": "Q1",
                            "form": "10-Q",
                            "filed": "2022-01-28",
                            "frame": "CY2021Q4I"
                        }
                    ]
                }
            }
        }

        fact = Fact.from_dict("us-gaap", fact_dict)

        assert fact.taxonomy == "us-gaap"
        assert "AccountsPayableCurrent" in fact.disclosures
        assert fact.disclosures["AccountsPayableCurrent"].label == "Accounts Payable, Current"


class TestCompanyFactClass:
    """Test cases for the CompanyFact class."""

    def test_from_api_response(self):
        """Test creating a CompanyFact object from an API response."""
        response = {
            "cik": "0000320193",
            "entityName": "Apple Inc.",
            "facts": {
                "us-gaap": {
                    "AccountsPayableCurrent": {
                        "label": "Accounts Payable, Current",
                        "description": "Carrying value of obligations incurred and payable to vendors",
                        "units": {
                            "USD": [
                                {
                                    "end": "2021-12-25",
                                    "val": 54763000000,
                                    "accn": "0000320193-22-000001",
                                    "fy": "2022",
                                    "fp": "Q1",
                                    "form": "10-Q",
                                    "filed": "2022-01-28",
                                    "frame": "CY2021Q4I"
                                }
                            ]
                        }
                    }
                }
            }
        }

        company_fact = CompanyFact.from_api_response(response)

        assert company_fact.cik == "0000320193"
        assert company_fact.entity_name == "Apple Inc."
        assert "us-gaap" in company_fact.facts
        assert "AccountsPayableCurrent" in company_fact.facts["us-gaap"].disclosures


class TestFrameDisclosureClass:
    """Test cases for the FrameDisclosure class."""

    def test_from_dict(self):
        """Test creating a FrameDisclosure object from a dictionary."""
        disclosure_dict = {
            "accn": "0000320193-22-000001",
            "cik": "320193",
            "entityName": "Apple Inc.",
            "loc": "US-CA",
            "end": "2021-12-25",
            "val": 54763000000
        }

        frame_disclosure = FrameDisclosure.from_dict(disclosure_dict)

        assert frame_disclosure.accn == "0000320193-22-000001"
        assert frame_disclosure.cik == "320193"
        assert frame_disclosure.entity_name == "Apple Inc."
        assert frame_disclosure.loc == "US-CA"
        assert frame_disclosure.end == "2021-12-25"
        assert frame_disclosure.val == 54763000000


class TestFrameClass:
    """Test cases for the Frame class."""

    def test_from_api_response(self):
        """Test creating a Frame object from an API response."""
        response = {
            "taxonomy": "us-gaap",
            "tag": "AccountsPayableCurrent",
            "ccp": "CY2021Q4I",
            "uom": "USD",
            "label": "Accounts Payable, Current",
            "description": "Carrying value of obligations incurred and payable to vendors",
            "pts": 3000,
            "data": [
                {
                    "accn": "0000320193-22-000001",
                    "cik": "320193",
                    "entityName": "Apple Inc.",
                    "loc": "US-CA",
                    "end": "2021-12-25",
                    "val": 54763000000
                },
                {
                    "accn": "0001961-22-000001",
                    "cik": "1961",
                    "entityName": "Company XYZ",
                    "loc": "US-NY",
                    "end": "2021-12-31",
                    "val": 1000000
                }
            ]
        }

        frame = Frame.from_api_response(response)

        assert frame.taxonomy == "us-gaap"
        assert frame.tag == "AccountsPayableCurrent"
        assert frame.ccp == "CY2021Q4I"
        assert frame.uom == "USD"
        assert frame.label == "Accounts Payable, Current"
        assert frame.pts == 3000
        assert len(frame.frames) == 2
        assert frame.frames[0].cik == "320193"
        assert frame.frames[0].val == 54763000000
        assert frame.frames[1].cik == "1961"
        assert frame.frames[1].val == 1000000
