# filepath: /test/clients_test.py
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
Comprehensive unit tests for the clients module.
"""
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime
from collections import deque
import asyncio
import time
import pytest
from cachetools import FIFOCache
import tenacity
from edgar_sec.clients import EdgarAPI
from edgar_sec.__about__ import __title__, __version__, __author__, __license__, __copyright__, __description__, __url__

class TestEdgarAPI:
    # Dunder methods
    def test_init(self):
        api = EdgarAPI(cache_mode=True, cache_size=100)

        assert api.base_url == "https://data.sec.gov"
        assert api.headers == {
            'User-Agent': 'Mozilla/5.0 (compatible; SEC-API/1.0; +https://www.sec.gov)',
            'Accept': 'application/json'
        }
        assert api.cache_mode is True
        assert api.cache_size == 100
        assert isinstance(api.cache, FIFOCache)
        assert api.max_requests_per_second == 10
        assert isinstance(api.request_times, deque)
        assert isinstance(api.lock, asyncio.Lock)
        assert isinstance(api.semaphore, asyncio.Semaphore)
        assert isinstance(api.Async, EdgarAPI.AsyncAPI)

    def test_repr(self):
        api = EdgarAPI()

        assert repr(api) == f"EdgarAPI(cache_mode={api.cache_mode}, cache_size={api.cache_size})"

    def test_str(self):
        api = EdgarAPI()

        assert str(api) == (
            f"EdgarAPI Instance:\n"
            f"Base URL: {api.base_url}\n"
            f"Cache Mode: {'Enabled' if api.cache_mode else 'Disabled'}\n"
            f"Cache Size: {api.cache_size}\n"
            f"Max Requests per Second: {api.max_requests_per_second}\n"
        )

    def test_eq(self):
        api1 = EdgarAPI(cache_mode=True, cache_size=100)
        api2 = EdgarAPI(cache_mode=True, cache_size=100)
        api3 = EdgarAPI(cache_mode=False, cache_size=50)

        assert api1 == api2
        assert api1 != api3
        assert api2 != api3
        assert (api1 == 123) is False

    def test_hash(self):
        api = EdgarAPI(cache_mode=True, cache_size=100)

        assert isinstance(hash(api), int)

    def test_del(self):
        api = EdgarAPI(cache_mode=True, cache_size=100)
        api.cache["test"] = "value"

        assert "test" in api.cache

        with patch.object(api.cache, "clear", wraps=api.cache.clear):
            del api
            import gc
            gc.collect()

    def test_getitem(self):
        api = EdgarAPI(cache_mode=True, cache_size=100)
        api.cache["foo"] = "bar"

        assert api["foo"] == "bar"

        with pytest.raises(AttributeError, match="'baz' not found in cache."):
            _ = api["baz"]

    def test_len(self):
        api = EdgarAPI(cache_mode=True, cache_size=100)
        api.cache["foo"] = "bar"
        api.cache["baz"] = "qux"

        assert len(api) == 2

    def test_contains(self):
        api = EdgarAPI(cache_mode=True, cache_size=100)
        api.cache["foo"] = "bar"

        assert "foo" in api
        assert "baz" not in api

        api2 = EdgarAPI(cache_mode=False, cache_size=100)
        api2.cache["foo"] = "bar"

        assert "foo" not in api2
        assert "baz" not in api2

    def test_setitem(self):
        api = EdgarAPI(cache_mode=True, cache_size=100)
        api["foo"] = "bar"

        assert api.cache["foo"] == "bar"

        with pytest.raises(AttributeError, match="'baz' not found in cache."):
            _ = api["baz"]

    def test_delitem(self):
        api = EdgarAPI(cache_mode=True, cache_size=100)
        api.cache["foo"] = "bar"

        assert "foo" in api.cache

        del api["foo"]

        assert "foo" not in api.cache

        with pytest.raises(AttributeError, match="'baz' not found in cache."):
            del api["baz"]

    def test_call(self):
        api = EdgarAPI(cache_mode=True, cache_size=100)

        assert api() == (
            f"EdgarAPI Instance:\n"
            f"  Base URL: {api.base_url}\n"
            f"  Cache Mode: {'Enabled' if api.cache_mode else 'Disabled'}\n"
            f"  Cache Size: {api.cache_size}\n"
        )

    # Private methods
    @pytest.mark.parametrize(
        "request_offsets,should_sleep",
        [
            ([-70], False),         # Only one old request, after cleanup and append: 1 (should NOT sleep)
            ([-0.8], False),        # Only one recent request, after append: 2 (should NOT sleep)
            ([-0.8, -0.5], True),   # Two recent requests, after append: 3 (should sleep)
            ([-0.8, -0.5, -0.1], True),  # Three recent requests, after append: 4 (should sleep)
        ]
    )
    def test_rate_limited(self, request_offsets, should_sleep):
        api = EdgarAPI(cache_mode=True, cache_size=10)
        api.max_requests_per_second = 3

        now = time.time()
        api.request_times.clear()
        api.request_times.extend([now + offset for offset in request_offsets])

        with patch("time.sleep") as mock_sleep:
            api._EdgarAPI__rate_limited()
            if should_sleep:
                assert mock_sleep.called
                sleep_args = mock_sleep.call_args[0][0]
                assert sleep_args > 0
            else:
                mock_sleep.assert_not_called()

    @pytest.mark.parametrize(
        "cache_mode, use_cache",
        [
            (False, False),  # cache off, should use __get_request
            (True, False),   # cache on, not cached yet, should use __get_request and cache
            (True, True),    # cache on, already cached, should use cache
        ]
    )
    def test_edgar_get_request(self, cache_mode, use_cache):
        api = EdgarAPI(cache_mode=cache_mode, cache_size=10)
        fake_json = {"foo": "bar"}
        url_endpoint = "/test"

        with patch.object(api, "_EdgarAPI__rate_limited", return_value=None):
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = fake_json

            with patch("httpx.Client.get", return_value=mock_response) as mock_get:
                if use_cache:
                    api._EdgarAPI__edgar_get_request(url_endpoint)
                    mock_get.reset_mock()
                result = api._EdgarAPI__edgar_get_request(url_endpoint)
                assert result == fake_json
                if cache_mode and use_cache:
                    mock_get.assert_not_called()
                else:
                    mock_get.assert_called_once()

    # Public methods
    def test_get_submissions(self):
        api = EdgarAPI(cache_mode=True, cache_size=10)
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
        with patch("edgar_sec.clients.EdgarHelpers.get_cik", return_value="0001744489") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation", side_effect=lambda x: x) as mock_cik_validation, \
            patch.object(api, "_EdgarAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.SubmissionHistory.to_object", return_value="submission_obj") as mock_to_object:
            result = api.get_submissions(ticker="DIS")
            mock_get_cik.assert_called_once_with(ticker="DIS")
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with("/submissions/CIK0001744489.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "submission_obj"

        with patch("edgar_sec.clients.EdgarHelpers.get_cik") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation", side_effect=lambda x: x) as mock_cik_validation, \
            patch.object(api, "_EdgarAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.SubmissionHistory.to_object", return_value="submission_obj") as mock_to_object:
            result = api.get_submissions(central_index_key="0001744489")
            mock_get_cik.assert_not_called()
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with("/submissions/CIK0001744489.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "submission_obj"

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key, not both."):
            api.get_submissions(ticker="DIS", central_index_key="0001744489")

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key."):
            api.get_submissions()

    def test_get_company_concept(self):
        api = EdgarAPI(cache_mode=True, cache_size=10)
        fake_response = {
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
        taxonomy = "us-gaap"
        tag = "AccountsPayableCurrent"

        with patch("edgar_sec.clients.EdgarHelpers.get_cik", return_value="0001744489") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation", side_effect=lambda x: x) as mock_cik_validation, \
            patch.object(api, "_EdgarAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.CompanyConcept.to_object", return_value="company_concept_obj") as mock_to_object:
            result = api.get_company_concept(taxonomy=taxonomy, tag=tag, ticker="DIS")
            mock_get_cik.assert_called_once_with(ticker="DIS")
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with(f"/api/xbrl/companyconcept/CIK0001744489/{taxonomy}/{tag}.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "company_concept_obj"

        with patch("edgar_sec.clients.EdgarHelpers.get_cik") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation", side_effect=lambda x: x) as mock_cik_validation, \
            patch.object(api, "_EdgarAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.CompanyConcept.to_object", return_value="company_concept_obj") as mock_to_object:
            result = api.get_company_concept(taxonomy=taxonomy, tag=tag, central_index_key="0001744489")
            mock_get_cik.assert_not_called()
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with(f"/api/xbrl/companyconcept/CIK0001744489/{taxonomy}/{tag}.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "company_concept_obj"

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key, not both."):
            api.get_company_concept(taxonomy=taxonomy, tag=tag, ticker="DIS", central_index_key="0001744489")

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key."):
            api.get_company_concept(taxonomy=taxonomy, tag=tag)

    def test_get_company_facts(self):
        api = EdgarAPI(cache_mode=True, cache_size=10)
        fake_response = {
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

        with patch("edgar_sec.clients.EdgarHelpers.get_cik", return_value="0001744489") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation", side_effect=lambda x: x) as mock_cik_validation, \
            patch.object(api, "_EdgarAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.CompanyFacts.to_object", return_value="company_facts_obj") as mock_to_object:
            result = api.get_company_facts(ticker="DIS")
            mock_get_cik.assert_called_once_with(ticker="DIS")
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with("/api/xbrl/companyfacts/CIK0001744489.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "company_facts_obj"

        with patch("edgar_sec.clients.EdgarHelpers.get_cik") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation", side_effect=lambda x: x) as mock_cik_validation, \
            patch.object(api, "_EdgarAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.CompanyFacts.to_object", return_value="company_facts_obj") as mock_to_object:
            result = api.get_company_facts(central_index_key="0001744489")
            mock_get_cik.assert_not_called()
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with("/api/xbrl/companyfacts/CIK0001744489.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "company_facts_obj"

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key, not both."):
            api.get_company_facts(ticker="DIS", central_index_key="0001744489")

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key."):
            api.get_company_facts()

    def test_get_frames(self):
        api = EdgarAPI(cache_mode=True, cache_size=10)
        fake_response = {
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
        taxonomy = "us-gaap"
        tag = "AccountsPayableCurrent"
        unit = "USD"
        period_str = "CY2019Q1"
        period_dt = datetime(2019, 3, 31)

        with patch("edgar_sec.clients.EdgarHelpers.string_cy_validation", return_value=True) as mock_cy_validation, \
            patch.object(api, "_EdgarAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.Frame.to_object", return_value="frame_obj") as mock_to_object:
            result = api.get_frames(taxonomy, tag, unit, period_str, instantaneous=True)
            mock_cy_validation.assert_called_once_with(period_str)
            mock_get_request.assert_called_once_with(f"/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period_str}I.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "frame_obj"

        with patch("edgar_sec.clients.EdgarHelpers.string_cy_validation", return_value=False) as mock_cy_validation, \
            patch("edgar_sec.clients.EdgarHelpers.string_cy_conversion", return_value="CY2019Q1") as mock_cy_conversion, \
            patch.object(api, "_EdgarAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.Frame.to_object", return_value="frame_obj") as mock_to_object:
            result = api.get_frames(taxonomy, tag, unit, "2019-03-31", instantaneous=True)
            mock_cy_validation.assert_called_once_with("2019-03-31")
            mock_cy_conversion.assert_called_once_with("2019-03-31")
            mock_get_request.assert_called_once_with(f"/api/xbrl/frames/{taxonomy}/{tag}/{unit}/CY2019Q1I.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "frame_obj"

        with patch("edgar_sec.clients.EdgarHelpers.datetime_cy_conversion", return_value="CY2019Q1") as mock_dt_conversion, \
            patch.object(api, "_EdgarAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.Frame.to_object", return_value="frame_obj") as mock_to_object:
            result = api.get_frames(taxonomy, tag, unit, period_dt, instantaneous=True)
            mock_dt_conversion.assert_called_once_with(period_dt)
            mock_get_request.assert_called_once_with(f"/api/xbrl/frames/{taxonomy}/{tag}/{unit}/CY2019Q1I.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "frame_obj"

        with patch("edgar_sec.clients.EdgarHelpers.string_cy_validation", return_value=True) as mock_cy_validation, \
            patch.object(api, "_EdgarAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.Frame.to_object", return_value="frame_obj") as mock_to_object:
            result = api.get_frames(taxonomy, tag, unit, period_str, instantaneous=False)
            mock_cy_validation.assert_called_once_with(period_str)
            mock_get_request.assert_called_once_with(f"/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period_str}.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "frame_obj"

        with pytest.raises(TypeError, match="period must be a string or datetime object."):
            api.get_frames(taxonomy, tag, unit, 12345, instantaneous=True)

class TestAsyncAPI:
    # Dunder methods
    def test_init(self):
        api = EdgarAPI(cache_mode=True, cache_size=100).Async

        assert api.base_url == "https://data.sec.gov"
        assert api.headers == {
            'User-Agent': 'Mozilla/5.0 (compatible; SEC-API/1.0; +https://www.sec.gov)',
            'Accept': 'application/json'
        }
        assert isinstance(api._parent, EdgarAPI)
        assert api.cache_mode is True
        assert api.cache == api._parent.cache
        assert api.base_url == api._parent.base_url
        assert api.headers == api._parent.headers

    def test_repr(self):
        api = EdgarAPI().Async

        assert repr(api) == f"EdgarAPI(cache_mode={api.cache_mode}, cache_size={api._parent.cache_size}).AsyncAPI"

    def test_str(self):
        api = EdgarAPI().Async

        assert str(api) == (
            f"{api._parent.__str__()}\n"
            f"  AsyncAPI Instance:\n"
            f"    Base URL: {api.base_url}\n"
        )

    def test_eq(self):
        api1 = EdgarAPI(cache_mode=True, cache_size=100).Async
        api2 = EdgarAPI(cache_mode=True, cache_size=100).Async
        api3 = EdgarAPI(cache_mode=False, cache_size=50).Async

        assert api1 == api2
        assert api1 != api3
        assert api2 != api3
        assert (api1 == 123) is False

    def test_hash(self):
        api = EdgarAPI(cache_mode=True, cache_size=100).Async

        assert isinstance(hash(api), int)

    def test_del(self):
        api = EdgarAPI(cache_mode=True, cache_size=100).Async
        api.cache["test"] = "value"

        assert "test" in api.cache

        with patch.object(api.cache, "clear", wraps=api.cache.clear):
            del api
            import gc
            gc.collect()

    def test_getitem(self):
        api = EdgarAPI(cache_mode=True, cache_size=100).Async
        api.cache["foo"] = "bar"

        assert api["foo"] == "bar"

        with pytest.raises(AttributeError, match="'baz' not found in cache."):
            _ = api["baz"]

    def test_len(self):
        api = EdgarAPI(cache_mode=True, cache_size=100).Async
        api.cache["foo"] = "bar"
        api.cache["baz"] = "qux"

        assert len(api) == 2

    def test_contains(self):
        api = EdgarAPI(cache_mode=True, cache_size=100).Async
        api.cache["foo"] = "bar"

        assert "foo" in api
        assert "baz" not in api

        api2 = EdgarAPI(cache_mode=False, cache_size=100).Async
        api2.cache["foo"] = "bar"

        assert "foo" in api2
        assert "baz" not in api2

    def test_setitem(self):
        api = EdgarAPI(cache_mode=True, cache_size=100).Async
        api["foo"] = "bar"

        assert api.cache["foo"] == "bar"

        with pytest.raises(AttributeError, match="'baz' not found in cache."):
            _ = api["baz"]

    def test_delitem(self):
        api = EdgarAPI(cache_mode=True, cache_size=100).Async
        api.cache["foo"] = "bar"

        assert "foo" in api.cache

        del api["foo"]

        assert "foo" not in api.cache

        with pytest.raises(AttributeError, match="'baz' not found in cache."):
            del api["baz"]

    def test_call(self):
        api = EdgarAPI(cache_mode=True, cache_size=100).Async

        assert api() == (
            f"EdgarAPI Instance\n"
            f"  AsyncAPI Instance:\n"
            f"    Base URL: {api.base_url}\n"
            f"    Cache Mode: {'Enabled' if api.cache_mode else 'Disabled'}\n"
            f"    Cache Size: {len(api.cache)} items\n"
        )

    # Private methods
    @pytest.mark.asyncio
    async def test_update_semaphore(self, monkeypatch):
        api = EdgarAPI(cache_mode=True, cache_size=10)
        async_api = api.Async

        # Patch time.time to control "now"
        fake_now = 1_000_000.0
        monkeypatch.setattr("time.time", lambda: fake_now)

        # Case 1: No requests in the last second
        api.request_times.clear()
        api.max_requests_per_second = 10
        requests_left, time_left = await async_api._AsyncAPI__update_semaphore()
        assert requests_left == 10
        assert time_left == 1
        assert isinstance(api.semaphore, asyncio.Semaphore)
        assert api.semaphore._value == 10

        # Case 2: Some requests older than 1s should be purged
        api.request_times.clear()
        api.request_times.extend([fake_now - 2, fake_now - 1.5, fake_now - 0.9, fake_now - 0.5])
        api.max_requests_per_second = 10
        requests_left, time_left = await async_api._AsyncAPI__update_semaphore()
        # Only requests within the last second should remain
        assert list(api.request_times) == [fake_now - 0.9, fake_now - 0.5]
        assert requests_left == 8
        assert time_left == 1 - (fake_now - (fake_now - 0.9))
        assert api.semaphore._value == 8

        # Case 3: All requests within last second, requests_left < max_requests_per_second
        api.request_times.clear()
        api.request_times.extend([fake_now - 0.9, fake_now - 0.5, fake_now - 0.1])
        api.max_requests_per_second = 5
        requests_left, time_left = await async_api._AsyncAPI__update_semaphore()
        assert requests_left == 2
        assert time_left == 1 - (fake_now - (fake_now - 0.9))
        assert api.semaphore._value == 2  # new_limit = max(1, requests_left)

        # Case 4: All requests used up (requests_left == 0)
        api.request_times.clear()
        api.request_times.extend([fake_now - 0.9, fake_now - 0.5, fake_now - 0.1, fake_now - 0.05, fake_now - 0.01])
        api.max_requests_per_second = 5
        requests_left, time_left = await async_api._AsyncAPI__update_semaphore()
        assert requests_left == 0
        assert time_left == 1 - (fake_now - (fake_now - 0.9))
        assert api.semaphore._value == 1

        # Case 5: request_times is empty (should not error)
        api.request_times.clear()
        api.max_requests_per_second = 15
        requests_left, time_left = await async_api._AsyncAPI__update_semaphore()
        assert requests_left == 15
        assert time_left == 1
        assert api.semaphore._value == 15

    @pytest.mark.parametrize(
        "request_offsets,requests_left,time_left,expected_sleep",
        [
            ([-70], 1, 1, 1),        # Only one old request, requests_left > 0, sleep 1/1=1
            ([-0.5], 2, 0.5, 0.25),  # Two recent requests, requests_left > 0, sleep 0.5/2=0.25
            ([-0.9, -0.5], 0, 0.8, 0.8),    # All requests used, requests_left == 0, sleep 0.8
            ([-0.9, -0.5, -0.1], 0, 0.6, 0.6) # All requests used, requests_left == 0, sleep 0.6
        ]
    )
    @pytest.mark.asyncio
    async def test_rate_limited(self, request_offsets, requests_left, time_left, expected_sleep, monkeypatch):
        api = EdgarAPI(cache_mode=True, cache_size=10)
        async_api = api.Async

        fake_now = 1_000_000.0
        monkeypatch.setattr("time.time", lambda: fake_now)
        api.request_times.clear()
        for offset in request_offsets:
            api.request_times.append(fake_now + offset)
        api.semaphore = asyncio.Semaphore(1)
        api.lock = asyncio.Lock()

        async def fake_update_semaphore():
            return requests_left, time_left

        monkeypatch.setattr(async_api, "_AsyncAPI__update_semaphore", fake_update_semaphore)

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            await async_api._AsyncAPI__rate_limited()
            mock_sleep.assert_awaited_once_with(expected_sleep)
            # After the call, a new request time should be appended
            assert len(api.request_times) >= 1
            assert api.request_times[-1] == fake_now

    @pytest.mark.asyncio
    async def test_edgar_get_request(self, monkeypatch):

        fake_json = {"foo": "bar"}
        url_endpoint = "/test"

        # Patch rate limiting
        async def fake_rate_limited(*args, **kwargs):
            return None

        # Patch async_cached to just call the function
        def fake_async_cached(cache):
            def decorator(func):
                async def wrapper(*args, **kwargs):
                    return await func(*args, **kwargs)
                return wrapper
            return decorator

        # Dummy AsyncClient for success
        class DummyAsyncClient:
            async def __aenter__(self):
                return self
            async def __aexit__(self, exc_type, exc, tb):
                pass
            async def get(self, url, headers=None, timeout=None):
                mock_response = MagicMock()
                mock_response.raise_for_status.return_value = None
                mock_response.json.return_value = fake_json
                return mock_response

        # Dummy AsyncClient for HTTPStatusError
        class HTTPStatusErrorAsyncClient:
            async def __aenter__(self):
                return self
            async def __aexit__(self, exc_type, exc, tb):
                pass
            async def get(self, url, headers=None, timeout=None):
                import httpx
                raise httpx.HTTPStatusError("fail", request=MagicMock(), response=MagicMock())

        # Dummy AsyncClient for RequestError
        class RequestErrorAsyncClient:
            async def __aenter__(self):
                return self
            async def __aexit__(self, exc_type, exc, tb):
                pass
            async def get(self, url, headers=None, timeout=None):
                import httpx
                raise httpx.RequestError("fail", request=MagicMock())

        # Test both cache modes: cache off and cache on
        for cache_mode in [False, True]:
            api = EdgarAPI(cache_mode=cache_mode, cache_size=10)
            async_api = api.Async

            monkeypatch.setattr(async_api, "_AsyncAPI__rate_limited", fake_rate_limited)
            with patch("httpx.AsyncClient", DummyAsyncClient), \
                patch("edgar_sec.clients.async_cached", fake_async_cached):
                result = await async_api._AsyncAPI__edgar_get_request(url_endpoint)
                assert result == fake_json

        # Test HTTPStatusError
        import httpx
        api = EdgarAPI(cache_mode=False, cache_size=10)
        async_api = api.Async
        monkeypatch.setattr(async_api, "_AsyncAPI__rate_limited", fake_rate_limited)
        with patch("httpx.AsyncClient", HTTPStatusErrorAsyncClient), \
            patch("edgar_sec.clients.async_cached", fake_async_cached):
            with pytest.raises(tenacity.RetryError) as excinfo:
                await async_api._AsyncAPI__edgar_get_request(url_endpoint)
            assert isinstance(excinfo.value.last_attempt.exception(), httpx.HTTPStatusError)

        # Test RequestError
        api = EdgarAPI(cache_mode=False, cache_size=10)
        async_api = api.Async
        monkeypatch.setattr(async_api, "_AsyncAPI__rate_limited", fake_rate_limited)
        with patch("httpx.AsyncClient", RequestErrorAsyncClient), \
            patch("edgar_sec.clients.async_cached", fake_async_cached):
            with pytest.raises(tenacity.RetryError) as excinfo:
                await async_api._AsyncAPI__edgar_get_request(url_endpoint)
            assert isinstance(excinfo.value.last_attempt.exception(), httpx.RequestError)

    # Public methods
    @pytest.mark.asyncio
    async def test_get_submissions(self):
        api = EdgarAPI(cache_mode=True, cache_size=10).Async
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
        with patch("edgar_sec.clients.EdgarHelpers.get_cik_async", return_value="0001744489") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation_async", side_effect=lambda x: x) as mock_cik_validation, \
            patch.object(api, "_AsyncAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.SubmissionHistory.to_object_async", return_value="submission_obj") as mock_to_object:
            result = await api.get_submissions(ticker="DIS")
            mock_get_cik.assert_called_once_with(ticker="DIS")
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with("/submissions/CIK0001744489.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "submission_obj"

        with patch("edgar_sec.clients.EdgarHelpers.get_cik_async") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation_async", side_effect=lambda x: x) as mock_cik_validation, \
            patch.object(api, "_AsyncAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.SubmissionHistory.to_object_async", return_value="submission_obj") as mock_to_object:
            result = await api.get_submissions(central_index_key="0001744489")
            mock_get_cik.assert_not_called()
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with("/submissions/CIK0001744489.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "submission_obj"

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key, not both."):
            await api.get_submissions(ticker="DIS", central_index_key="0001744489")

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key."):
            await api.get_submissions()

    @pytest.mark.asyncio
    async def test_get_company_concept(self):
        api = EdgarAPI(cache_mode=True, cache_size=10).Async
        fake_response = {
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
        taxonomy = "us-gaap"
        tag = "AccountsPayableCurrent"

        with patch("edgar_sec.clients.EdgarHelpers.get_cik_async", return_value="0001744489") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation_async", side_effect=lambda x: x) as mock_cik_validation, \
            patch.object(api, "_AsyncAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.CompanyConcept.to_object_async", return_value="company_concept_obj") as mock_to_object:
            result = await api.get_company_concept(taxonomy=taxonomy, tag=tag, ticker="DIS")
            mock_get_cik.assert_called_once_with(ticker="DIS")
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with(f"/api/xbrl/companyconcept/CIK0001744489/{taxonomy}/{tag}.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "company_concept_obj"

        with patch("edgar_sec.clients.EdgarHelpers.get_cik_async") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation_async", side_effect=lambda x: x) as mock_cik_validation, \
            patch.object(api, "_AsyncAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.CompanyConcept.to_object_async", return_value="company_concept_obj") as mock_to_object:
            result = await api.get_company_concept(taxonomy=taxonomy, tag=tag, central_index_key="0001744489")
            mock_get_cik.assert_not_called()
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with(f"/api/xbrl/companyconcept/CIK0001744489/{taxonomy}/{tag}.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "company_concept_obj"

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key, not both."):
            await api.get_company_concept(taxonomy=taxonomy, tag=tag, ticker="DIS", central_index_key="0001744489")

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key."):
            await api.get_company_concept(taxonomy=taxonomy, tag=tag)

    @pytest.mark.asyncio
    async def test_get_company_facts(self):
        api = EdgarAPI(cache_mode=True, cache_size=10).Async
        fake_response = {
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

        with patch("edgar_sec.clients.EdgarHelpers.get_cik_async", return_value="0001744489") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation_async", return_value="0001744489") as mock_cik_validation, \
            patch.object(api, "_AsyncAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.CompanyFacts.to_object_async", return_value="company_facts_obj") as mock_to_object:
            result = await api.get_company_facts(ticker="DIS")
            mock_get_cik.assert_called_once_with(ticker="DIS")
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with("/api/xbrl/companyfacts/CIK0001744489.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "company_facts_obj"

        with patch("edgar_sec.clients.EdgarHelpers.get_cik_async") as mock_get_cik, \
            patch("edgar_sec.clients.EdgarHelpers.cik_validation_async", return_value="0001744489") as mock_cik_validation, \
            patch.object(api, "_AsyncAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.CompanyFacts.to_object_async", return_value="company_facts_obj") as mock_to_object:
            result = await api.get_company_facts(central_index_key="0001744489")
            mock_get_cik.assert_not_called()
            mock_cik_validation.assert_called_once_with("0001744489")
            mock_get_request.assert_called_once_with("/api/xbrl/companyfacts/CIK0001744489.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "company_facts_obj"

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key, not both."):
            await api.get_company_facts(ticker="DIS", central_index_key="0001744489")

        with pytest.raises(ValueError, match="Provide either ticker or central_index_key."):
            await api.get_company_facts()

    @pytest.mark.asyncio
    async def test_get_frames(self):
        api = EdgarAPI(cache_mode=True, cache_size=10).Async
        fake_response = {
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
        taxonomy = "us-gaap"
        tag = "AccountsPayableCurrent"
        unit = "USD"
        period_str = "CY2019Q1"
        period_dt = datetime(2019, 3, 31)

        with patch("edgar_sec.clients.EdgarHelpers.string_cy_validation_async", return_value=True) as mock_cy_validation, \
            patch.object(api, "_AsyncAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.Frame.to_object_async", return_value="frame_obj") as mock_to_object:
            result = await api.get_frames(taxonomy, tag, unit, period_str, instantaneous=True)
            mock_cy_validation.assert_called_once_with(period_str)
            mock_get_request.assert_called_once_with(f"/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period_str}I.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "frame_obj"

        with patch("edgar_sec.clients.EdgarHelpers.string_cy_validation_async", return_value=False) as mock_cy_validation, \
            patch("edgar_sec.clients.EdgarHelpers.string_cy_conversion_async", return_value="CY2019Q1") as mock_cy_conversion, \
            patch.object(api, "_AsyncAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.Frame.to_object_async", return_value="frame_obj") as mock_to_object:
            result = await api.get_frames(taxonomy, tag, unit, "2019-03-31", instantaneous=True)
            mock_cy_validation.assert_called_once_with("2019-03-31")
            mock_cy_conversion.assert_called_once_with("2019-03-31")
            mock_get_request.assert_called_once_with(f"/api/xbrl/frames/{taxonomy}/{tag}/{unit}/CY2019Q1I.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "frame_obj"

        with patch("edgar_sec.clients.EdgarHelpers.datetime_cy_conversion_async", return_value="CY2019Q1") as mock_dt_conversion, \
            patch.object(api, "_AsyncAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.Frame.to_object_async", return_value="frame_obj") as mock_to_object:
            result = await api.get_frames(taxonomy, tag, unit, period_dt, instantaneous=True)
            mock_dt_conversion.assert_called_once_with(period_dt)
            mock_get_request.assert_called_once_with(f"/api/xbrl/frames/{taxonomy}/{tag}/{unit}/CY2019Q1I.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "frame_obj"

        with patch("edgar_sec.clients.EdgarHelpers.string_cy_validation_async", return_value=True) as mock_cy_validation, \
            patch.object(api, "_AsyncAPI__edgar_get_request", return_value=fake_response) as mock_get_request, \
            patch("edgar_sec.clients.Frame.to_object_async", return_value="frame_obj") as mock_to_object:
            result = await api.get_frames(taxonomy, tag, unit, period_str, instantaneous=False)
            mock_cy_validation.assert_called_once_with(period_str)
            mock_get_request.assert_called_once_with(f"/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period_str}.json")
            mock_to_object.assert_called_once_with(fake_response)
            assert result == "frame_obj"

        with pytest.raises(TypeError, match="period must be a string or datetime object."):
            await api.get_frames(taxonomy, tag, unit, 12345, instantaneous=True)
