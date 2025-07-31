# filepath: /test/objects_test.py
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
Comprehensive tests for the objects module.
"""

import pytest
from edgar_sec.objects import (
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
    Company
)
from edgar_sec.__about__ import __title__, __version__, __author__, __license__, __copyright__, __description__, __url__

class TestAddress:
    def test_address_to_object(self):
        address_type = "primary"
        data = {
            "street1": "123 Main St",
            "street2": "Suite 100",
            "city": "Anytown",
            "stateOrCountry": "CA",
            "zipCode": "12345",
            "stateOrCountryDescription": "California",
            "isForeignLocation": 0,
            "foreignStateTerritory": None,
            "country": None,
            "countryCode": None
        }
        address = Address.to_object(address_type, data)
        assert isinstance(address, Address)
        assert address.address_type == "primary"
        assert address.street1 == "123 Main St"
        assert address.street2 == "Suite 100"
        assert address.city == "Anytown"
        assert address.state_or_country == "CA"
        assert address.zipcode == "12345"
        assert address.state_or_country_description == "California"
        assert address.is_foreign_location is False
        assert address.foreign_state_territory is None
        assert address.country is None
        assert address.country_code is None

    @pytest.mark.asyncio
    async def test_address_to_object_async(self):
        address_type = "primary"
        data = {
            "street1": "123 Main St",
            "street2": "Suite 100",
            "city": "Anytown",
            "stateOrCountry": "CA",
            "zipCode": "12345",
            "stateOrCountryDescription": "California",
            "isForeignLocation": 0,
            "foreignStateTerritory": None,
            "country": None,
            "countryCode": None
        }
        address = await Address.to_object_async(address_type, data)
        assert isinstance(address, Address)
        assert address.address_type == "primary"
        assert address.street1 == "123 Main St"
        assert address.street2 == "Suite 100"
        assert address.city == "Anytown"
        assert address.state_or_country == "CA"
        assert address.zipcode == "12345"
        assert address.state_or_country_description == "California"
        assert address.is_foreign_location is False
        assert address.foreign_state_territory is None
        assert address.country is None
        assert address.country_code is None

class TestFormerName:
    def test_former_name_to_object(self):
        data = {
            "name": "Old Company Name",
            "from": "2023-01-01",
            "to": "2023-12-31"
        }
        former_name = FormerName.to_object(data)
        assert isinstance(former_name, FormerName)
        assert former_name.name == "Old Company Name"
        assert former_name.from_date == "2023-01-01"
        assert former_name.to_date == "2023-12-31"

    @pytest.mark.asyncio
    async def test_former_name_to_object_async(self):
        data = {
            "name": "Old Company Name",
            "from": "2023-01-01",
            "to": "2023-12-31"
        }
        former_name = await FormerName.to_object_async(data)
        assert isinstance(former_name, FormerName)
        assert former_name.name == "Old Company Name"
        assert former_name.from_date == "2023-01-01"
        assert former_name.to_date == "2023-12-31"

class TestFiling:
    def test_filing_to_object(self):
        data = {
            "accessionNumber": ["0001234567-23-000001"],
            "filingDate": ["2023-01-01"],
            "reportDate": ["2023-01-02"],
            "acceptanceDateTime": ["2023-01-03T12:00:00"],
            "act": ["34"],
            "form": ["10-K"],
            "fileNumber": ["001-23456"],
            "filmNumber": ["123456789"],
            "items": ["1, 2, 3"],
            "core_type": ["XBRL"],
            "size": [123],
            "isXBRL": [1],
            "isInlineXBRL": [0],
            "primaryDocument": ["0001234567-23-000001.txt"],
            "primaryDocDescription": ["Annual Report"]
        }
        filing = Filing.to_object(data, 0)
        assert isinstance(filing, Filing)
        assert filing.accession_number == "0001234567-23-000001"
        assert filing.filing_date == "2023-01-01"
        assert filing.report_date == "2023-01-02"
        assert filing.acceptance_date_time == "2023-01-03T12:00:00"
        assert filing.act == "34"
        assert filing.form == "10-K"
        assert filing.file_number == "001-23456"
        assert filing.film_number == "123456789"
        assert filing.items == "1, 2, 3"
        assert filing.core_type == "XBRL"
        assert filing.size == 123
        assert filing.is_xbrl is True
        assert filing.is_inline_xbrl is False
        assert filing.primary_document == "0001234567-23-000001.txt"
        assert filing.primary_doc_description == "Annual Report"

    @pytest.mark.asyncio
    async def test_filing_to_object_async(self):
        data = {
            "accessionNumber": ["0001234567-23-000001"],
            "filingDate": ["2023-01-01"],
            "reportDate": ["2023-01-02"],
            "acceptanceDateTime": ["2023-01-03T12:00:00"],
            "act": ["34"],
            "form": ["10-K"],
            "fileNumber": ["001-23456"],
            "filmNumber": ["123456789"],
            "items": ["1, 2, 3"],
            "core_type": ["XBRL"],
            "size": [123],
            "isXBRL": [1],
            "isInlineXBRL": [0],
            "primaryDocument": ["0001234567-23-000001.txt"],
            "primaryDocDescription": ["Annual Report"]
        }
        filing = await Filing.to_object_async(data, 0)
        assert isinstance(filing, Filing)
        assert filing.accession_number == "0001234567-23-000001"
        assert filing.filing_date == "2023-01-01"
        assert filing.report_date == "2023-01-02"
        assert filing.acceptance_date_time == "2023-01-03T12:00:00"
        assert filing.act == "34"
        assert filing.form == "10-K"
        assert filing.file_number == "001-23456"
        assert filing.film_number == "123456789"
        assert filing.items == "1, 2, 3"
        assert filing.core_type == "XBRL"
        assert filing.size == 123
        assert filing.is_xbrl is True
        assert filing.is_inline_xbrl is False
        assert filing.primary_document == "0001234567-23-000001.txt"
        assert filing.primary_doc_description == "Annual Report"

class TestFile:
    def test_file_to_object(self):
        data = {
            "name": "example.txt",
            "filingCount": 2,
            "filingFrom": "2023-01-01",
            "filingTo": "2023-12-31"
        }
        file = File.to_object(data)
        assert isinstance(file, File)
        assert file.name == "example.txt"
        assert file.filing_count == 2
        assert file.filing_from == "2023-01-01"
        assert file.filing_to == "2023-12-31"

    @pytest.mark.asyncio
    async def test_file_to_object_async(self):
        data = {
            "name": "example.txt",
            "filingCount": 2,
            "filingFrom": "2023-01-01",
            "filingTo": "2023-12-31"
        }
        file = await File.to_object_async(data)
        assert isinstance(file, File)
        assert file.name == "example.txt"
        assert file.filing_count == 2
        assert file.filing_from == "2023-01-01"
        assert file.filing_to == "2023-12-31"

class TestSubmissionHistory:
    def test_submission_history_to_object(self):
        fake_response = {
            "cik": "0001744489",
            "entityType": "operating",
            "sic": "7990",
            "sicDescription": "Services-Miscellaneous Amusement & Recreation",
            "ownerOrg": "07 Trade & Services",
            "insiderTransactionForOwnerExists": 1,
            "insiderTransactionForIssuerExists": 0,
            "name": "Walt Disney Co",
            "tickers": ["DIS"],
            "exchanges": ["NYSE"],
            "ein": "830940635",
            "lei": None,
            "description": "",
            "website": "",
            "investorWebsite": "",
            "category": "Large accelerated filer",
            "fiscalYearEnd": "0927",
            "stateOfIncorporation": "DE",
            "stateOfIncorporationDescription": "DE",
            "addresses":
            {
                "mailing":
                {
                    "street1": "500 SOUTH BUENA VISTA STREET",
                    "street2": None,
                    "city": "BURBANK",
                    "stateOrCountry": "CA",
                    "zipCode": "91521",
                    "stateOrCountryDescription": "CA",
                    "isForeignLocation": 0,
                    "foreignStateTerritory": None,
                    "country": None,
                    "countryCode": None
                },
                "business":
                {
                    "street1": "500 SOUTH BUENA VISTA STREET",
                    "street2": None,
                    "city": "BURBANK",
                    "stateOrCountry": "CA",
                    "zipCode": "91521",
                    "stateOrCountryDescription": "CA",
                    "isForeignLocation": 0,
                    "foreignStateTerritory": None,
                    "country": None,
                    "countryCode": None
                }
            },
            "phone": "(818) 560-1000",
            "flags": "",
            "formerNames":[
                {
                    "name": "TWDC Holdco 613 Corp",
                    "from": "2018-06-25T04:00:00.000Z",
                    "to": "2018-06-28T04:00:00.000Z"
                },
                {
                    "name": "TWDC Holdco 613 Corp.",
                    "from":"2018-06-27T04:00:00.000Z",
                    "to":"2018-06-27T04:00:00.000Z"
                }
            ],
            "filings":
            {
                "recent":
                {
                    "accessionNumber":[
                        "0001628280-25-034115",
                        "0001628280-25-034114",
                        "0001628280-25-034113"
                    ],
                    "filingDate":[
                        "2025-07-02",
                        "2025-07-02",
                        "2025-07-02"
                    ],
                    "reportDate":[
                        "2025-06-30",
                        "2025-06-30",
                        "2025-06-30"
                    ],
                    "acceptanceDateTime":[
                        "2025-07-02T23:59:54.000Z",
                        "2025-07-02T23:59:43.000Z",
                        "2025-07-02T23:59:33.000Z"
                    ],
                    "act":[
                        "34",
                        "34",
                        "33"
                    ],
                    "form":[
                        "4",
                        "4",
                        "4"
                    ],
                    "fileNumber":[
                        "001-38842",
                        "001-38842",
                        "001-38842"
                    ],
                    "filmNumber":[
                        "25919394",
                        "25919184",
                        "25919183"
                    ],
                    "items":[
                        "7.01,9.01",
                        "2.02,9.01",
                        "5.07,9.01"
                    ],
                    "core_type":[
                        "4",
                        "XBRL",
                        "11-K"
                    ],
                    "size":[
                        5434,
                        6163,
                        6028
                    ],
                    "isXBRL":[
                        1,
                        0,
                        1
                    ],
                    "isInlineXBRL":[
                        0,
                        0,
                        0
                    ],
                    "primaryDocument":[
                        "xslF345X05/wk-form4_1751500787.xml",
                        "xslF345X05/wk-form4_1751500777.xml",
                        "xslF345X05/wk-form4_1751500765.xml"
                    ],
                    "primaryDocDescription":[
                        "FORM 4",
                        "FORM 4",
                        "FORM 4"
                    ]
                },
                "files":[
                    {
                        "name":"CIK0001744489-submissions-001.json",
                        "filingCount":7,
                        "filingFrom":"2018-06-25",
                        "filingTo":"2019-03-18"
                    }
                ]
            }
        }
        submission_history = SubmissionHistory.to_object(fake_response)
        assert isinstance(submission_history, SubmissionHistory)
        assert submission_history.cik == "0001744489"
        assert submission_history.entity_type == "operating"
        assert submission_history.sic == "7990"
        assert submission_history.sic_description == "Services-Miscellaneous Amusement & Recreation"
        assert submission_history.owner_org == "07 Trade & Services"
        assert submission_history.insider_transaction_for_owner_exists is True
        assert submission_history.insider_transaction_for_issuer_exists is False
        assert submission_history.name == "Walt Disney Co"
        assert isinstance(submission_history.tickers, list)
        assert submission_history.tickers[0] == "DIS"
        assert isinstance(submission_history.exchanges, list)
        assert submission_history.exchanges[0] == "NYSE"
        assert submission_history.ein == "830940635"
        assert submission_history.lei is None
        assert submission_history.description == ""
        assert submission_history.website == ""
        assert submission_history.investor_website == ""
        assert submission_history.category == "Large accelerated filer"
        assert submission_history.fiscal_year_end == "0927"
        assert submission_history.state_of_incorporation == "DE"
        assert submission_history.state_of_incorporation_description == "DE"
        assert isinstance(submission_history.addresses, list)
        assert isinstance(submission_history.addresses[0], Address)
        assert submission_history.phone == "(818) 560-1000"
        assert submission_history.flags == ""
        assert isinstance(submission_history.former_names, list)
        assert isinstance(submission_history.former_names[0], FormerName)
        assert isinstance(submission_history.filings, list)
        assert isinstance(submission_history.filings[0], Filing)
        assert isinstance(submission_history.files, list)
        assert isinstance(submission_history.files[0], File)

    @pytest.mark.asyncio
    async def test_submission_history_to_object_async(self):
        fake_response = {
            "cik": "0001744489",
            "entityType": "operating",
            "sic": "7990",
            "sicDescription": "Services-Miscellaneous Amusement & Recreation",
            "ownerOrg": "07 Trade & Services",
            "insiderTransactionForOwnerExists": 1,
            "insiderTransactionForIssuerExists": 0,
            "name": "Walt Disney Co",
            "tickers": ["DIS"],
            "exchanges": ["NYSE"],
            "ein": "830940635",
            "lei": None,
            "description": "",
            "website": "",
            "investorWebsite": "",
            "category": "Large accelerated filer",
            "fiscalYearEnd": "0927",
            "stateOfIncorporation": "DE",
            "stateOfIncorporationDescription": "DE",
            "addresses":
            {
                "mailing":
                {
                    "street1": "500 SOUTH BUENA VISTA STREET",
                    "street2": None,
                    "city": "BURBANK",
                    "stateOrCountry": "CA",
                    "zipCode": "91521",
                    "stateOrCountryDescription": "CA",
                    "isForeignLocation": 0,
                    "foreignStateTerritory": None,
                    "country": None,
                    "countryCode": None
                },
                "business":
                {
                    "street1": "500 SOUTH BUENA VISTA STREET",
                    "street2": None,
                    "city": "BURBANK",
                    "stateOrCountry": "CA",
                    "zipCode": "91521",
                    "stateOrCountryDescription": "CA",
                    "isForeignLocation": 0,
                    "foreignStateTerritory": None,
                    "country": None,
                    "countryCode": None
                }
            },
            "phone": "(818) 560-1000",
            "flags": "",
            "formerNames":[
                {
                    "name": "TWDC Holdco 613 Corp",
                    "from": "2018-06-25T04:00:00.000Z",
                    "to": "2018-06-28T04:00:00.000Z"
                },
                {
                    "name": "TWDC Holdco 613 Corp.",
                    "from":"2018-06-27T04:00:00.000Z",
                    "to":"2018-06-27T04:00:00.000Z"
                }
            ],
            "filings":
            {
                "recent":
                {
                    "accessionNumber":[
                        "0001628280-25-034115",
                        "0001628280-25-034114",
                        "0001628280-25-034113"
                    ],
                    "filingDate":[
                        "2025-07-02",
                        "2025-07-02",
                        "2025-07-02"
                    ],
                    "reportDate":[
                        "2025-06-30",
                        "2025-06-30",
                        "2025-06-30"
                    ],
                    "acceptanceDateTime":[
                        "2025-07-02T23:59:54.000Z",
                        "2025-07-02T23:59:43.000Z",
                        "2025-07-02T23:59:33.000Z"
                    ],
                    "act":[
                        "34",
                        "34",
                        "33"
                    ],
                    "form":[
                        "4",
                        "4",
                        "4"
                    ],
                    "fileNumber":[
                        "001-38842",
                        "001-38842",
                        "001-38842"
                    ],
                    "filmNumber":[
                        "25919394",
                        "25919184",
                        "25919183"
                    ],
                    "items":[
                        "7.01,9.01",
                        "2.02,9.01",
                        "5.07,9.01"
                    ],
                    "core_type":[
                        "4",
                        "XBRL",
                        "11-K"
                    ],
                    "size":[
                        5434,
                        6163,
                        6028
                    ],
                    "isXBRL":[
                        1,
                        0,
                        1
                    ],
                    "isInlineXBRL":[
                        0,
                        0,
                        0
                    ],
                    "primaryDocument":[
                        "xslF345X05/wk-form4_1751500787.xml",
                        "xslF345X05/wk-form4_1751500777.xml",
                        "xslF345X05/wk-form4_1751500765.xml"
                    ],
                    "primaryDocDescription":[
                        "FORM 4",
                        "FORM 4",
                        "FORM 4"
                    ]
                },
                "files":[
                    {
                        "name":"CIK0001744489-submissions-001.json",
                        "filingCount":7,
                        "filingFrom":"2018-06-25",
                        "filingTo":"2019-03-18"
                    }
                ]
            }
        }
        submission_history = await SubmissionHistory.to_object_async(fake_response)
        assert isinstance(submission_history, SubmissionHistory)
        assert submission_history.cik == "0001744489"
        assert submission_history.entity_type == "operating"
        assert submission_history.sic == "7990"
        assert submission_history.sic_description == "Services-Miscellaneous Amusement & Recreation"
        assert submission_history.owner_org == "07 Trade & Services"
        assert submission_history.insider_transaction_for_owner_exists is True
        assert submission_history.insider_transaction_for_issuer_exists is False
        assert submission_history.name == "Walt Disney Co"
        assert isinstance(submission_history.tickers, list)
        assert submission_history.tickers[0] == "DIS"
        assert isinstance(submission_history.exchanges, list)
        assert submission_history.exchanges[0] == "NYSE"
        assert submission_history.ein == "830940635"
        assert submission_history.lei is None
        assert submission_history.description == ""
        assert submission_history.website == ""
        assert submission_history.investor_website == ""
        assert submission_history.category == "Large accelerated filer"
        assert submission_history.fiscal_year_end == "0927"
        assert submission_history.state_of_incorporation == "DE"
        assert submission_history.state_of_incorporation_description == "DE"
        assert isinstance(submission_history.addresses, list)
        assert isinstance(submission_history.addresses[0], Address)
        assert submission_history.phone == "(818) 560-1000"
        assert submission_history.flags == ""
        assert isinstance(submission_history.former_names, list)
        assert isinstance(submission_history.former_names[0], FormerName)
        assert isinstance(submission_history.filings, list)
        assert isinstance(submission_history.filings[0], Filing)
        assert isinstance(submission_history.files, list)
        assert isinstance(submission_history.files[0], File)

class TestUnitDisclosure:
    def test_unit_disclosure_to_object(self):
        data = {
            "unit": "USD",
            "end": "2022-12-31",
            "val": 1000.0,
            "accn": "001-38842",
            "fy": "2022",
            "fp": "FY",
            "form": "10-K",
            "filed": "2023-01-31",
            "frame": "2022-12-31",
            "start": "2022-01-01"
        }
        unit_disclosure = UnitDisclosure.to_object(data, "USD")
        assert isinstance(unit_disclosure, UnitDisclosure)
        assert unit_disclosure.units == "USD"
        assert unit_disclosure.end == "2022-12-31"
        assert unit_disclosure.val == 1000.0
        assert unit_disclosure.accn == "001-38842"
        assert unit_disclosure.fy == "2022"
        assert unit_disclosure.fp == "FY"
        assert unit_disclosure.form == "10-K"
        assert unit_disclosure.filed == "2023-01-31"
        assert unit_disclosure.frame == "2022-12-31"
        assert unit_disclosure.start == "2022-01-01"

    @pytest.mark.asyncio
    async def test_unit_disclosure_to_object_async(self):
        data = {
            "unit": "USD",
            "end": "2022-12-31",
            "val": 1000.0,
            "accn": "001-38842",
            "fy": "2022",
            "fp": "FY",
            "form": "10-K",
            "filed": "2023-01-31",
            "frame": "2022-12-31",
            "start": "2022-01-01"
        }
        unit_disclosure = await UnitDisclosure.to_object_async(data, "USD")
        assert isinstance(unit_disclosure, UnitDisclosure)
        assert unit_disclosure.units == "USD"
        assert unit_disclosure.end == "2022-12-31"
        assert unit_disclosure.val == 1000.0
        assert unit_disclosure.accn == "001-38842"
        assert unit_disclosure.fy == "2022"
        assert unit_disclosure.fp == "FY"
        assert unit_disclosure.form == "10-K"
        assert unit_disclosure.filed == "2023-01-31"
        assert unit_disclosure.frame == "2022-12-31"
        assert unit_disclosure.start == "2022-01-01"

class TestCompanyConcept:
    def test_company_concept_to_object(self):
        response = {
            "cik": 1744489,
            "taxonomy": "us-gaap",
            "tag": "AccountsPayableCurrent",
            "label": "Accounts Payable, Current",
            "description": "Carrying value as of the balance sheet date of liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received that are used in an entity's business. Used to reflect the current portion of the liabilities (due within one year or within the normal operating cycle if longer).",
            "entityName": "WALT DISNEY CO/",
            "units":
            {
                "USD":[
                    {
                        "end": "2017-09-30",
                        "val": 6305000000,
                        "accn": "0001744489-19-000173",
                        "fy": None,
                        "fp": None,
                        "form": "8-K",
                        "filed": "2019-08-14",
                        "frame": "CY2017Q3I"
                    },
                    {
                        "end": "2018-09-29",
                        "val": 6503000000,
                        "accn": "0001744489-19-000173",
                        "fy": None,
                        "fp": None,
                        "form": "8-K",
                        "filed": "2019-08-14"
                    },
                    {
                        "end": "2018-09-29",
                        "val": 6503000000,
                        "accn": "0001744489-19-000225",
                        "fy": 2019,
                        "fp": "FY",
                        "form": "10-K",
                        "filed": "2019-11-20",
                        "frame": "CY2018Q3I"
                    }
                ]
            }
        }
        company_concept = CompanyConcept.to_object(response)
        assert isinstance(company_concept, CompanyConcept)
        assert company_concept.cik == "1744489"
        assert company_concept.taxonomy == "us-gaap"
        assert company_concept.tag == "AccountsPayableCurrent"
        assert company_concept.label == "Accounts Payable, Current"
        assert company_concept.description == (
            "Carrying value as of the balance sheet date of liabilities incurred "
            "(and for which invoices have typically been received) and payable to "
            "vendors for goods and services received that are used in an entity's "
            "business. Used to reflect the current portion of the liabilities (due "
            "within one year or within the normal operating cycle if longer)."
        )
        assert company_concept.entity_name == "WALT DISNEY CO/"
        assert isinstance(company_concept.units, list)
        assert isinstance(company_concept.units[0], UnitDisclosure)

    @pytest.mark.asyncio
    async def test_company_concept_to_object_async(self):
        response = {
            "cik": 1744489,
            "taxonomy": "us-gaap",
            "tag": "AccountsPayableCurrent",
            "label": "Accounts Payable, Current",
            "description": "Carrying value as of the balance sheet date of liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received that are used in an entity's business. Used to reflect the current portion of the liabilities (due within one year or within the normal operating cycle if longer).",
            "entityName": "WALT DISNEY CO/",
            "units":
            {
                "USD":[
                    {
                        "end": "2017-09-30",
                        "val": 6305000000,
                        "accn": "0001744489-19-000173",
                        "fy": None,
                        "fp": None,
                        "form": "8-K",
                        "filed": "2019-08-14",
                        "frame": "CY2017Q3I"
                    },
                    {
                        "end": "2018-09-29",
                        "val": 6503000000,
                        "accn": "0001744489-19-000173",
                        "fy": None,
                        "fp": None,
                        "form": "8-K",
                        "filed": "2019-08-14"
                    },
                    {
                        "end": "2018-09-29",
                        "val": 6503000000,
                        "accn": "0001744489-19-000225",
                        "fy": 2019,
                        "fp": "FY",
                        "form": "10-K",
                        "filed": "2019-11-20",
                        "frame": "CY2018Q3I"
                    }
                ]
            }
        }
        company_concept = await CompanyConcept.to_object_async(response)
        assert isinstance(company_concept, CompanyConcept)
        assert company_concept.cik == "1744489"
        assert company_concept.taxonomy == "us-gaap"
        assert company_concept.tag == "AccountsPayableCurrent"
        assert company_concept.label == "Accounts Payable, Current"
        assert company_concept.description == (
            "Carrying value as of the balance sheet date of liabilities incurred "
            "(and for which invoices have typically been received) and payable to "
            "vendors for goods and services received that are used in an entity's "
            "business. Used to reflect the current portion of the liabilities (due "
            "within one year or within the normal operating cycle if longer)."
        )
        assert company_concept.entity_name == "WALT DISNEY CO/"
        assert isinstance(company_concept.units, list)
        assert isinstance(company_concept.units[0], UnitDisclosure)

class TestTaxonomyDisclosures:
    def test_taxonomy_disclosures_to_object(self):
        response = {
            "label": "Entity Common Stock, Shares Outstanding",
            "description": "Indicate number of shares or other units outstanding of each of registrant's classes of capital or common stock or other ownership interests, if and as stated on cover of related periodic report. Where multiple classes or units exist define each class/interest by adding class of stock items such as Common Class A [Member], Common Class B [Member] or Partnership Interest [Member] onto the Instrument [Domain] of the Entity Listings, Instrument.",
            "units":
            {
                "shares":[
                    {
                        "end": "2019-05-01",
                        "val": 1799698922,
                        "accn": "0001744489-19-000100",
                        "fy": 2019,
                        "fp": "Q2",
                        "form": "10-Q",
                        "filed": "2019-05-08",
                        "frame": "CY2019Q1I"
                    },
                    {
                        "end": "2019-07-31",
                        "val": 1801379029,
                        "accn": "0001744489-19-000167",
                        "fy": 2019,
                        "fp": "Q3",
                        "form": "10-Q",
                        "filed": "2019-08-06",
                        "frame": "CY2019Q2I"
                    },
                    {
                        "end": "2019-11-13",
                        "val": 1802398289,
                        "accn": "0001744489-19-000225",
                        "fy": 2019,
                        "fp": "FY",
                        "form": "10-K",
                        "filed": "2019-11-20",
                        "frame": "CY2019Q3I"
                    }
                ]
            }
        }
        taxonomy_disclosures = TaxonomyDisclosures.to_object(response, "EntityCommonStockSharesOutstanding")
        assert isinstance(taxonomy_disclosures, TaxonomyDisclosures)
        assert taxonomy_disclosures.label == "Entity Common Stock, Shares Outstanding"
        assert taxonomy_disclosures.description == (
            "Indicate number of shares or other units outstanding of each of registrant's classes of capital or common stock or other ownership interests, if and as stated on cover of related periodic report. Where multiple classes or units exist define each class/interest by adding class of stock items such as Common Class A [Member], Common Class B [Member] or Partnership Interest [Member] onto the Instrument [Domain] of the Entity Listings, Instrument."
        )
        assert isinstance(taxonomy_disclosures.units, list)
        assert isinstance(taxonomy_disclosures.units[0], UnitDisclosure)

    @pytest.mark.asyncio
    async def test_taxonomy_disclosures_to_object_async(self):
        response = {
            "label": "Entity Common Stock, Shares Outstanding",
            "description": "Indicate number of shares or other units outstanding of each of registrant's classes of capital or common stock or other ownership interests, if and as stated on cover of related periodic report. Where multiple classes or units exist define each class/interest by adding class of stock items such as Common Class A [Member], Common Class B [Member] or Partnership Interest [Member] onto the Instrument [Domain] of the Entity Listings, Instrument.",
            "units":
            {
                "shares":[
                    {
                        "end": "2019-05-01",
                        "val": 1799698922,
                        "accn": "0001744489-19-000100",
                        "fy": 2019,
                        "fp": "Q2",
                        "form": "10-Q",
                        "filed": "2019-05-08",
                        "frame": "CY2019Q1I"
                    },
                    {
                        "end": "2019-07-31",
                        "val": 1801379029,
                        "accn": "0001744489-19-000167",
                        "fy": 2019,
                        "fp": "Q3",
                        "form": "10-Q",
                        "filed": "2019-08-06",
                        "frame": "CY2019Q2I"
                    },
                    {
                        "end": "2019-11-13",
                        "val": 1802398289,
                        "accn": "0001744489-19-000225",
                        "fy": 2019,
                        "fp": "FY",
                        "form": "10-K",
                        "filed": "2019-11-20",
                        "frame": "CY2019Q3I"
                    }
                ]
            }
        }
        taxonomy_disclosures = TaxonomyDisclosures.to_object(response, "EntityCommonStockSharesOutstanding")
        assert isinstance(taxonomy_disclosures, TaxonomyDisclosures)
        assert taxonomy_disclosures.label == "Entity Common Stock, Shares Outstanding"
        assert taxonomy_disclosures.description == (
            "Indicate number of shares or other units outstanding of each of registrant's classes of capital or common stock or other ownership interests, if and as stated on cover of related periodic report. Where multiple classes or units exist define each class/interest by adding class of stock items such as Common Class A [Member], Common Class B [Member] or Partnership Interest [Member] onto the Instrument [Domain] of the Entity Listings, Instrument."
        )
        assert isinstance(taxonomy_disclosures.units, list)
        assert isinstance(taxonomy_disclosures.units[0], UnitDisclosure)

class TestTaxonomyFacts:
    def test_taxonomy_facts_to_object(self):
        response = {
            "EntityCommonStockSharesOutstanding":
            {
                "label": "Entity Common Stock, Shares Outstanding",
                "description": "Indicate number of shares or other units outstanding of each of registrant's classes of capital or common stock or other ownership interests, if and as stated on cover of related periodic report. Where multiple classes or units exist define each class/interest by adding class of stock items such as Common Class A [Member], Common Class B [Member] or Partnership Interest [Member] onto the Instrument [Domain] of the Entity Listings, Instrument.",
                "units":
                {
                    "shares":[
                        {
                            "end": "2019-05-01",
                            "val": 1799698922,
                            "accn": "0001744489-19-000100",
                            "fy": 2019,
                            "fp": "Q2",
                            "form": "10-Q",
                            "filed": "2019-05-08",
                            "frame": "CY2019Q1I"
                        },
                        {
                            "end": "2019-07-31",
                            "val": 1801379029,
                            "accn": "0001744489-19-000167",
                            "fy": 2019,
                            "fp": "Q3",
                            "form": "10-Q",
                            "filed": "2019-08-06",
                            "frame": "CY2019Q2I"
                        },
                        {
                            "end": "2019-11-13",
                            "val": 1802398289,
                            "accn": "0001744489-19-000225",
                            "fy": 2019,
                            "fp": "FY",
                            "form": "10-K",
                            "filed": "2019-11-20",
                            "frame": "CY2019Q3I"
                        }
                    ]
                }
            }
        }
        taxonomy_facts = TaxonomyFacts.to_object(response, "dei")
        assert isinstance(taxonomy_facts, TaxonomyFacts)
        assert taxonomy_facts.taxonomy == "dei"
        assert isinstance(taxonomy_facts.disclosures, list)
        assert isinstance(taxonomy_facts.disclosures[0], TaxonomyDisclosures)

    @pytest.mark.asyncio
    async def test_taxonomy_facts_to_object_async(self):
        response = {
            "EntityCommonStockSharesOutstanding":
            {
                "label": "Entity Common Stock, Shares Outstanding",
                "description": "Indicate number of shares or other units outstanding of each of registrant's classes of capital or common stock or other ownership interests, if and as stated on cover of related periodic report. Where multiple classes or units exist define each class/interest by adding class of stock items such as Common Class A [Member], Common Class B [Member] or Partnership Interest [Member] onto the Instrument [Domain] of the Entity Listings, Instrument.",
                "units":
                {
                    "shares":[
                        {
                            "end": "2019-05-01",
                            "val": 1799698922,
                            "accn": "0001744489-19-000100",
                            "fy": 2019,
                            "fp": "Q2",
                            "form": "10-Q",
                            "filed": "2019-05-08",
                            "frame": "CY2019Q1I"
                        },
                        {
                            "end": "2019-07-31",
                            "val": 1801379029,
                            "accn": "0001744489-19-000167",
                            "fy": 2019,
                            "fp": "Q3",
                            "form": "10-Q",
                            "filed": "2019-08-06",
                            "frame": "CY2019Q2I"
                        },
                        {
                            "end": "2019-11-13",
                            "val": 1802398289,
                            "accn": "0001744489-19-000225",
                            "fy": 2019,
                            "fp": "FY",
                            "form": "10-K",
                            "filed": "2019-11-20",
                            "frame": "CY2019Q3I"
                        }
                    ]
                }
            }
        }
        taxonomy_facts = await TaxonomyFacts.to_object_async(response, "dei")
        assert isinstance(taxonomy_facts, TaxonomyFacts)
        assert taxonomy_facts.taxonomy == "dei"
        assert isinstance(taxonomy_facts.disclosures, list)
        assert isinstance(taxonomy_facts.disclosures[0], TaxonomyDisclosures)

class TestCompanyFacts:
    def test_company_facts_to_object(self):
        response = {
            "cik":1744489,
            "entityName":"WALT DISNEY CO/",
            "facts":
            {
                "dei":
                {
                    "EntityCommonStockSharesOutstanding":
                    {
                        "label": "Entity Common Stock, Shares Outstanding",
                        "description": "Indicate number of shares or other units outstanding of each of registrant's classes of capital or common stock or other ownership interests, if and as stated on cover of related periodic report. Where multiple classes or units exist define each class/interest by adding class of stock items such as Common Class A [Member], Common Class B [Member] or Partnership Interest [Member] onto the Instrument [Domain] of the Entity Listings, Instrument.",
                        "units":
                        {
                            "shares":[
                                {
                                    "end": "2019-05-01",
                                    "val": 1799698922,
                                    "accn": "0001744489-19-000100",
                                    "fy": 2019,
                                    "fp": "Q2",
                                    "form": "10-Q",
                                    "filed": "2019-05-08",
                                    "frame": "CY2019Q1I"
                                },
                                {
                                    "end": "2019-07-31",
                                    "val": 1801379029,
                                    "accn": "0001744489-19-000167",
                                    "fy": 2019,
                                    "fp": "Q3",
                                    "form": "10-Q",
                                    "filed": "2019-08-06",
                                    "frame": "CY2019Q2I"
                                },
                                {
                                    "end": "2019-11-13",
                                    "val": 1802398289,
                                    "accn": "0001744489-19-000225",
                                    "fy": 2019,
                                    "fp": "FY",
                                    "form": "10-K",
                                    "filed": "2019-11-20",
                                    "frame": "CY2019Q3I"
                                }
                            ]
                        }
                    },
                    "AccountsPayableCurrent":
                    {
                        "label":"Accounts Payable, Current",
                        "description":"Carrying value as of the balance sheet date of liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received that are used in an entity's business. Used to reflect the current portion of the liabilities (due within one year or within the normal operating cycle if longer).",
                        "units":
                        {
                            "USD":[
                                {
                                    "end":"2017-09-30",
                                    "val":6305000000,
                                    "accn":"0001744489-19-000173",
                                    "fy":None,
                                    "fp":None,
                                    "form":"8-K",
                                    "filed":"2019-08-14",
                                    "frame":"CY2017Q3I"
                                },
                                {
                                    "end":"2018-09-29",
                                    "val":6503000000,
                                    "accn":"0001744489-19-000173",
                                    "fy":None,
                                    "fp":None,
                                    "form":"8-K",
                                    "filed":"2019-08-14"
                                },
                                {
                                    "end":"2018-09-29",
                                    "val":6503000000,
                                    "accn":"0001744489-19-000225",
                                    "fy":2019,
                                    "fp":"FY",
                                    "form":"10-K",
                                    "filed":"2019-11-20",
                                    "frame":"CY2018Q3I"
                                }
                            ]
                        }
                    }
                },
                "us-gaap":
                {
                    "AccountsPayableAndAccruedLiabilitiesCurrent":
                    {
                        "label": "Accounts Payable and Accrued Liabilities, Current",
                        "description": "Sum of the carrying values as of the balance sheet date of obligations incurred through that date and due within one year (or the operating cycle, if longer), including liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received, taxes, interest, rent and utilities, accrued salaries and bonuses, payroll taxes and fringe benefits.",
                        "units":
                        {
                            "USD":[
                                {
                                    "end": "2017-09-30",
                                    "val": 8855000000,
                                    "accn": "0001744489-19-000173",
                                    "fy": None,
                                    "fp": None,
                                    "form": "8-K",
                                    "filed": "2019-08-14",
                                    "frame": "CY2017Q3I"
                                },
                                {
                                    "end": "2018-09-29",
                                    "val": 9479000000,
                                    "accn": "0001744489-19-000100",
                                    "fy": 2019,
                                    "fp": "Q2",
                                    "form": "10-Q",
                                    "filed": "2019-05-08"
                                },
                                {
                                    "end": "2018-09-29",
                                    "val": 9479000000,
                                    "accn": "0001744489-19-000167",
                                    "fy": 2019,
                                    "fp": "Q3",
                                    "form": "10-Q",
                                    "filed": "2019-08-06"
                                }
                            ]
                        }
                    }
                }
            }
        }
        company_facts = CompanyFacts.to_object(response)
        assert isinstance(company_facts, CompanyFacts)
        assert company_facts.cik == "1744489"
        assert company_facts.entity_name == "WALT DISNEY CO/"
        assert isinstance(company_facts.facts, list)
        assert isinstance(company_facts.facts[0], TaxonomyFacts)

    @pytest.mark.asyncio
    async def test_company_facts_to_object_async(self):
        response = {
            "cik":1744489,
            "entityName":"WALT DISNEY CO/",
            "facts":
            {
                "dei":
                {
                    "EntityCommonStockSharesOutstanding":
                    {
                        "label": "Entity Common Stock, Shares Outstanding",
                        "description": "Indicate number of shares or other units outstanding of each of registrant's classes of capital or common stock or other ownership interests, if and as stated on cover of related periodic report. Where multiple classes or units exist define each class/interest by adding class of stock items such as Common Class A [Member], Common Class B [Member] or Partnership Interest [Member] onto the Instrument [Domain] of the Entity Listings, Instrument.",
                        "units":
                        {
                            "shares":[
                                {
                                    "end": "2019-05-01",
                                    "val": 1799698922,
                                    "accn": "0001744489-19-000100",
                                    "fy": 2019,
                                    "fp": "Q2",
                                    "form": "10-Q",
                                    "filed": "2019-05-08",
                                    "frame": "CY2019Q1I"
                                },
                                {
                                    "end": "2019-07-31",
                                    "val": 1801379029,
                                    "accn": "0001744489-19-000167",
                                    "fy": 2019,
                                    "fp": "Q3",
                                    "form": "10-Q",
                                    "filed": "2019-08-06",
                                    "frame": "CY2019Q2I"
                                },
                                {
                                    "end": "2019-11-13",
                                    "val": 1802398289,
                                    "accn": "0001744489-19-000225",
                                    "fy": 2019,
                                    "fp": "FY",
                                    "form": "10-K",
                                    "filed": "2019-11-20",
                                    "frame": "CY2019Q3I"
                                }
                            ]
                        }
                    },
                    "AccountsPayableCurrent":
                    {
                        "label":"Accounts Payable, Current",
                        "description":"Carrying value as of the balance sheet date of liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received that are used in an entity's business. Used to reflect the current portion of the liabilities (due within one year or within the normal operating cycle if longer).",
                        "units":
                        {
                            "USD":[
                                {
                                    "end":"2017-09-30",
                                    "val":6305000000,
                                    "accn":"0001744489-19-000173",
                                    "fy":None,
                                    "fp":None,
                                    "form":"8-K",
                                    "filed":"2019-08-14",
                                    "frame":"CY2017Q3I"
                                },
                                {
                                    "end":"2018-09-29",
                                    "val":6503000000,
                                    "accn":"0001744489-19-000173",
                                    "fy":None,
                                    "fp":None,
                                    "form":"8-K",
                                    "filed":"2019-08-14"
                                },
                                {
                                    "end":"2018-09-29",
                                    "val":6503000000,
                                    "accn":"0001744489-19-000225",
                                    "fy":2019,
                                    "fp":"FY",
                                    "form":"10-K",
                                    "filed":"2019-11-20",
                                    "frame":"CY2018Q3I"
                                }
                            ]
                        }
                    }
                },
                "us-gaap":
                {
                    "AccountsPayableAndAccruedLiabilitiesCurrent":
                    {
                        "label": "Accounts Payable and Accrued Liabilities, Current",
                        "description": "Sum of the carrying values as of the balance sheet date of obligations incurred through that date and due within one year (or the operating cycle, if longer), including liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received, taxes, interest, rent and utilities, accrued salaries and bonuses, payroll taxes and fringe benefits.",
                        "units":
                        {
                            "USD":[
                                {
                                    "end": "2017-09-30",
                                    "val": 8855000000,
                                    "accn": "0001744489-19-000173",
                                    "fy": None,
                                    "fp": None,
                                    "form": "8-K",
                                    "filed": "2019-08-14",
                                    "frame": "CY2017Q3I"
                                },
                                {
                                    "end": "2018-09-29",
                                    "val": 9479000000,
                                    "accn": "0001744489-19-000100",
                                    "fy": 2019,
                                    "fp": "Q2",
                                    "form": "10-Q",
                                    "filed": "2019-05-08"
                                },
                                {
                                    "end": "2018-09-29",
                                    "val": 9479000000,
                                    "accn": "0001744489-19-000167",
                                    "fy": 2019,
                                    "fp": "Q3",
                                    "form": "10-Q",
                                    "filed": "2019-08-06"
                                }
                            ]
                        }
                    }
                }
            }
        }
        company_facts = await CompanyFacts.to_object_async(response)
        assert isinstance(company_facts, CompanyFacts)
        assert company_facts.cik == "1744489"
        assert company_facts.entity_name == "WALT DISNEY CO/"
        assert isinstance(company_facts.facts, list)
        assert isinstance(company_facts.facts[0], TaxonomyFacts)

class TestFrameDisclosure:
    def test_frame_disclosure_to_object(self):
        response = {
            "accn": "0001104659-19-016320",
            "cik": 1750,
            "entityName": "AAR CORP.",
            "loc": "US-IL",
            "end": "2019-02-28",
            "val": 218600000
        }
        disclosure = FrameDisclosure.to_object(response)
        assert isinstance(disclosure, FrameDisclosure)
        assert disclosure.accn == "0001104659-19-016320"
        assert disclosure.cik == "1750"
        assert disclosure.entity_name == "AAR CORP."
        assert disclosure.loc == "US-IL"
        assert disclosure.end == "2019-02-28"
        assert disclosure.val == 218600000

    @pytest.mark.asyncio
    async def test_frame_disclosure_to_object_async(self):
        response = {
            "accn": "0001104659-19-016320",
            "cik": 1750,
            "entityName": "AAR CORP.",
            "loc": "US-IL",
            "end": "2019-02-28",
            "val": 218600000
        }
        disclosure = await FrameDisclosure.to_object_async(response)
        assert isinstance(disclosure, FrameDisclosure)
        assert disclosure.accn == "0001104659-19-016320"
        assert disclosure.cik == "1750"
        assert disclosure.entity_name == "AAR CORP."
        assert disclosure.loc == "US-IL"
        assert disclosure.end == "2019-02-28"
        assert disclosure.val == 218600000

class TestFrame:
    def test_frame_disclosure_to_object(self):
        response = {
            "taxonomy": "us-gaap",
            "tag": "AccountsPayableCurrent",
            "ccp": "CY2019Q1I",
            "uom": "USD",
            "label": "Accounts Payable, Current",
            "description": "Carrying value as of the balance sheet date of liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received that are used in an entity's business. Used to reflect the current portion of the liabilities (due within one year or within the normal operating cycle if longer).",
            "pts": 3390,
            "data":[
                {
                    "accn": "0001104659-19-016320",
                    "cik": 1750,
                    "entityName": "AAR CORP.",
                    "loc": "US-IL",
                    "end": "2019-02-28",
                    "val": 218600000
                },
                {
                    "accn": "0001264931-19-000067",
                    "cik": 1961,
                    "entityName": "WORLDS INC.",
                    "loc": "US-MA",
                    "end": "2019-03-31",
                    "val": 797908
                },
                {
                    "accn": "0001026608-19-000026",
                    "cik": 2098,
                    "entityName": "Acme United Corporation",
                    "loc": "US-CT",
                    "end": "2019-03-31",
                    "val":5672000
                }
            ]
        }
        frame = Frame.to_object(response)
        assert isinstance(frame, Frame)
        assert frame.taxonomy == "us-gaap"
        assert frame.tag == "AccountsPayableCurrent"
        assert frame.ccp == "CY2019Q1I"
        assert frame.uom == "USD"
        assert frame.label == "Accounts Payable, Current"
        assert frame.description == (
            "Carrying value as of the balance sheet date of liabilities incurred "
            "(and for which invoices have typically been received) and payable to "
            "vendors for goods and services received that are used in an entity's "
            "business. Used to reflect the current portion of the liabilities (due "
            "within one year or within the normal operating cycle if longer)."
        )
        assert frame.pts == 3390
        assert isinstance(frame.disclosures, list)
        assert isinstance(frame.disclosures[0], FrameDisclosure)

    @pytest.mark.asyncio
    async def test_frame_disclosure_to_object_async(self):
        response = {
            "taxonomy": "us-gaap",
            "tag": "AccountsPayableCurrent",
            "ccp": "CY2019Q1I",
            "uom": "USD",
            "label": "Accounts Payable, Current",
            "description": "Carrying value as of the balance sheet date of liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received that are used in an entity's business. Used to reflect the current portion of the liabilities (due within one year or within the normal operating cycle if longer).",
            "pts": 3390,
            "data":[
                {
                    "accn": "0001104659-19-016320",
                    "cik": 1750,
                    "entityName": "AAR CORP.",
                    "loc": "US-IL",
                    "end": "2019-02-28",
                    "val": 218600000
                },
                {
                    "accn": "0001264931-19-000067",
                    "cik": 1961,
                    "entityName": "WORLDS INC.",
                    "loc": "US-MA",
                    "end": "2019-03-31",
                    "val": 797908
                },
                {
                    "accn": "0001026608-19-000026",
                    "cik": 2098,
                    "entityName": "Acme United Corporation",
                    "loc": "US-CT",
                    "end": "2019-03-31",
                    "val":5672000
                }
            ]
        }
        frame = await Frame.to_object_async(response)
        assert isinstance(frame, Frame)
        assert frame.taxonomy == "us-gaap"
        assert frame.tag == "AccountsPayableCurrent"
        assert frame.ccp == "CY2019Q1I"
        assert frame.uom == "USD"
        assert frame.label == "Accounts Payable, Current"
        assert frame.description == (
            "Carrying value as of the balance sheet date of liabilities incurred "
            "(and for which invoices have typically been received) and payable to "
            "vendors for goods and services received that are used in an entity's "
            "business. Used to reflect the current portion of the liabilities (due "
            "within one year or within the normal operating cycle if longer)."
        )
        assert frame.pts == 3390
        assert isinstance(frame.disclosures, list)
        assert isinstance(frame.disclosures[0], FrameDisclosure)

class TestCompany:
    def test_company_to_object(self):
        data = {
            "cik_str":1045810,
            "ticker":"NVDA",
            "title":"NVIDIA CORP"
        }
        company = Company.to_object(data)
        assert isinstance(company, Company)
        assert company.cik == "1045810"
        assert company.ticker == "NVDA"
        assert company.title == "NVIDIA CORP"

    @pytest.mark.asyncio
    async def test_company_to_object_async(self):
        data = {
            "cik_str":1045810,
            "ticker":"NVDA",
            "title":"NVIDIA CORP"
        }
        company = await Company.to_object_async(data)
        assert isinstance(company, Company)
        assert company.cik == "1045810"
        assert company.ticker == "NVDA"
        assert company.title == "NVIDIA CORP"
