# filepath: /test/helpers_test.py
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
Comprehensive tests for the helpers module.
"""

from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime
import pytest
from edgar_sec.helpers import EdgarHelpers
from edgar_sec.objects import Company
from edgar_sec.__about__ import __title__, __version__, __author__, __license__, __copyright__, __description__, __url__

class TestRequestHelpers:
    @patch("httpx.Client")
    def test_get_cik(self, mock_client):
        fake_response = {
            "0":
            {
                "cik_str":1045810,
                "ticker":"NVDA",
                "title":"NVIDIA CORP"
            },
            "1":
            {
                "cik_str":789019,
                "ticker":"MSFT",
                "title":"MICROSOFT CORP"
            },
            "2":
            {
                "cik_str":320193,
                "ticker":"AAPL",
                "title":"Apple Inc."
            },
            "3":
            {
                "cik_str":1018724,
                "ticker":"AMZN",
                "title":"AMAZON COM INC"
            }
        }

        def fake_json():
            return [v for v in fake_response.values()]

        mock_instance = MagicMock()
        mock_instance.get.return_value.json = fake_json
        mock_instance.get.return_value.raise_for_status = lambda: None
        mock_client.return_value.__enter__.return_value = mock_instance

        assert EdgarHelpers.get_cik(ticker="AAPL") == 320193
        assert EdgarHelpers.get_cik(search_text="nvidia") == 1045810
        with pytest.raises(ValueError, match="Ticker 'TSLA' not found"):
            EdgarHelpers.get_cik(ticker="TSLA")
        with pytest.raises(ValueError, match="Search text 'foobar' not found"):
            EdgarHelpers.get_cik(search_text="foobar")
        with pytest.raises(ValueError, match="Provide exactly one of ticker or search_text."):
            EdgarHelpers.get_cik()
        with pytest.raises(ValueError, match="Provide exactly one of ticker or search_text."):
            EdgarHelpers.get_cik(ticker="AAPL", search_text="Apple")

    @patch("httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_get_cik_async(self, mock_client):
        fake_response = {
            "0":
            {
                "cik_str":1045810,
                "ticker":"NVDA",
                "title":"NVIDIA CORP"
            },
            "1":
            {
                "cik_str":789019,
                "ticker":"MSFT",
                "title":"MICROSOFT CORP"
            },
            "2":
            {
                "cik_str":320193,
                "ticker":"AAPL",
                "title":"Apple Inc."
            },
            "3":
            {
                "cik_str":1018724,
                "ticker":"AMZN",
                "title":"AMAZON COM INC"
            }
        }

        def fake_json():
            return [v for v in fake_response.values()]

        mock_instance = AsyncMock()
        mock_instance.get.return_value.json = fake_json
        mock_instance.get.return_value.raise_for_status = lambda: None
        mock_client.return_value.__aenter__.return_value = mock_instance

        assert await EdgarHelpers.get_cik_async(ticker="NVDA") == 1045810
        assert await EdgarHelpers.get_cik_async(search_text="microsoft") == 789019
        with pytest.raises(ValueError, match="Ticker 'TSLA' not found"):
            await EdgarHelpers.get_cik_async(ticker="TSLA")
        with pytest.raises(ValueError, match="Search text 'foobar' not found"):
            await EdgarHelpers.get_cik_async(search_text="foobar")
        with pytest.raises(ValueError, match="Provide exactly one of ticker or search_text."):
            await EdgarHelpers.get_cik_async()
        with pytest.raises(ValueError, match="Provide exactly one of ticker or search_text."):
            await EdgarHelpers.get_cik_async(ticker="NVDA", search_text="NVIDIA")

    @patch("httpx.Client")
    def test_get_universe(self, mock_client):
        fake_response = {
            "0":
            {
                "cik_str":1045810,
                "ticker":"NVDA",
                "title":"NVIDIA CORP"
            },
            "1":
            {
                "cik_str":789019,
                "ticker":"MSFT",
                "title":"MICROSOFT CORP"
            },
            "2":
            {
                "cik_str":320193,
                "ticker":"AAPL",
                "title":"Apple Inc."
            },
            "3":
            {
                "cik_str":1018724,
                "ticker":"AMZN",
                "title":"AMAZON COM INC"
            }
        }

        def fake_json():
            return [v for v in fake_response.values()]

        mock_instance = MagicMock()
        mock_instance.get.return_value.json = fake_json
        mock_instance.get.return_value.raise_for_status = lambda: None
        mock_client.return_value.__enter__.return_value = mock_instance

        universe = EdgarHelpers.get_universe()
        assert len(universe) == 4
        assert isinstance(universe[0], Company)
        assert isinstance(universe[1], Company)
        assert isinstance(universe[2], Company)
        assert isinstance(universe[3], Company)
        assert universe[0].cik == "1045810"
        assert universe[1].ticker == "MSFT"
        assert universe[2].title == "Apple Inc."
        assert universe[3].cik == "1018724"

    @patch("httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_get_universe_async(self, mock_client):
        fake_response = {
            "0":
            {
                "cik_str":1045810,
                "ticker":"NVDA",
                "title":"NVIDIA CORP"
            },
            "1":
            {
                "cik_str":789019,
                "ticker":"MSFT",
                "title":"MICROSOFT CORP"
            },
            "2":
            {
                "cik_str":320193,
                "ticker":"AAPL",
                "title":"Apple Inc."
            },
            "3":
            {
                "cik_str":1018724,
                "ticker":"AMZN",
                "title":"AMAZON COM INC"
            }
        }

        def fake_json():
            return [v for v in fake_response.values()]

        mock_instance = AsyncMock()
        mock_instance.get.return_value.json = fake_json
        mock_instance.get.return_value.raise_for_status = lambda: None
        mock_client.return_value.__aenter__.return_value = mock_instance

        universe = await EdgarHelpers.get_universe_async()
        assert len(universe) == 4
        assert isinstance(universe[0], Company)
        assert isinstance(universe[1], Company)
        assert isinstance(universe[2], Company)
        assert isinstance(universe[3], Company)
        assert universe[0].cik == "1045810"
        assert universe[1].ticker == "MSFT"
        assert universe[2].title == "Apple Inc."
        assert universe[3].cik == "1018724"

class TestConversionHelpers:
    def test_datetime_cy_conversion_all_cases(self):

        assert EdgarHelpers.datetime_cy_conversion(datetime(2024, 1, 15)) == "CY2024Q1"
        assert EdgarHelpers.datetime_cy_conversion(datetime(2024, 3, 31)) == "CY2024Q1"
        assert EdgarHelpers.datetime_cy_conversion(datetime(2024, 4, 1)) == "CY2024Q2"
        assert EdgarHelpers.datetime_cy_conversion(datetime(2024, 6, 30)) == "CY2024Q2"
        assert EdgarHelpers.datetime_cy_conversion(datetime(2024, 7, 1)) == "CY2024Q3"
        assert EdgarHelpers.datetime_cy_conversion(datetime(2024, 9, 30)) == "CY2024Q3"
        assert EdgarHelpers.datetime_cy_conversion(datetime(2024, 10, 1)) == "CY2024Q4"
        assert EdgarHelpers.datetime_cy_conversion(datetime(2024, 12, 31)) == "CY2024Q4"

        with pytest.raises(TypeError, match="period must be a datetime object."):
            EdgarHelpers.datetime_cy_conversion("invalid_type")

    @pytest.mark.asyncio
    async def test_datetime_cy_conversion_async(self):

        assert await EdgarHelpers.datetime_cy_conversion_async(datetime(2024, 1, 15)) == "CY2024Q1"
        assert await EdgarHelpers.datetime_cy_conversion_async(datetime(2024, 3, 31)) == "CY2024Q1"
        assert await EdgarHelpers.datetime_cy_conversion_async(datetime(2024, 4, 1)) == "CY2024Q2"
        assert await EdgarHelpers.datetime_cy_conversion_async(datetime(2024, 6, 30)) == "CY2024Q2"
        assert await EdgarHelpers.datetime_cy_conversion_async(datetime(2024, 7, 1)) == "CY2024Q3"
        assert await EdgarHelpers.datetime_cy_conversion_async(datetime(2024, 9, 30)) == "CY2024Q3"
        assert await EdgarHelpers.datetime_cy_conversion_async(datetime(2024, 10, 1)) == "CY2024Q4"
        assert await EdgarHelpers.datetime_cy_conversion_async(datetime(2024, 12, 31)) == "CY2024Q4"

        with pytest.raises(TypeError, match="period must be a datetime object."):
            await EdgarHelpers.datetime_cy_conversion_async("invalid_type")

    def test_string_cy_conversion(self):

        assert EdgarHelpers.string_cy_conversion("2024-01-15") == "CY2024Q1"
        assert EdgarHelpers.string_cy_conversion("2024-03-31") == "CY2024Q1"
        assert EdgarHelpers.string_cy_conversion("2024-04-01") == "CY2024Q2"
        assert EdgarHelpers.string_cy_conversion("2024-06-30") == "CY2024Q2"
        assert EdgarHelpers.string_cy_conversion("2024-07-01") == "CY2024Q3"
        assert EdgarHelpers.string_cy_conversion("2024-09-30") == "CY2024Q3"
        assert EdgarHelpers.string_cy_conversion("2024-10-01") == "CY2024Q4"
        assert EdgarHelpers.string_cy_conversion("2024-12-31") == "CY2024Q4"

        with pytest.raises(TypeError, match="period must be a string."):
            EdgarHelpers.string_cy_conversion(0)

        with pytest.raises(ValueError, match="Invalid date format. Must be in 'YYYY-MM-DD' format."):
            EdgarHelpers.string_cy_conversion("invalid_date")

    @pytest.mark.asyncio
    async def test_string_cy_conversion_async(self):

        assert await EdgarHelpers.string_cy_conversion_async("2024-01-15") == "CY2024Q1"
        assert await EdgarHelpers.string_cy_conversion_async("2024-03-31") == "CY2024Q1"
        assert await EdgarHelpers.string_cy_conversion_async("2024-04-01") == "CY2024Q2"
        assert await EdgarHelpers.string_cy_conversion_async("2024-06-30") == "CY2024Q2"
        assert await EdgarHelpers.string_cy_conversion_async("2024-07-01") == "CY2024Q3"
        assert await EdgarHelpers.string_cy_conversion_async("2024-09-30") == "CY2024Q3"
        assert await EdgarHelpers.string_cy_conversion_async("2024-10-01") == "CY2024Q4"
        assert await EdgarHelpers.string_cy_conversion_async("2024-12-31") == "CY2024Q4"

        with pytest.raises(TypeError, match="period must be a string."):
            await EdgarHelpers.string_cy_conversion_async(0)

        with pytest.raises(ValueError, match="Invalid date format. Must be in 'YYYY-MM-DD' format."):
            await EdgarHelpers.string_cy_conversion_async("invalid_date")

class TestValidationHelpers:
    def test_string_cy_validation(self):
        assert EdgarHelpers.string_cy_validation("CY2024") is True
        assert EdgarHelpers.string_cy_validation("CY2024Q1") is True
        assert EdgarHelpers.string_cy_validation("CY2024Q2") is True
        assert EdgarHelpers.string_cy_validation("CY2024Q3") is True
        assert EdgarHelpers.string_cy_validation("CY2024Q4") is True

        with pytest.raises(TypeError, match="period must be a string."):
            EdgarHelpers.string_cy_validation(12345)

        assert EdgarHelpers.string_cy_validation("CY2024Q5") is False
        assert EdgarHelpers.string_cy_validation("CY2024Q0") is False
        assert EdgarHelpers.string_cy_validation("2024-01-01") is False

    @pytest.mark.asyncio
    async def test_string_cy_validation_async(self):
        assert await EdgarHelpers.string_cy_validation_async("CY2024") is True
        assert await EdgarHelpers.string_cy_validation_async("CY2024Q1") is True
        assert await EdgarHelpers.string_cy_validation_async("CY2024Q2") is True
        assert await EdgarHelpers.string_cy_validation_async("CY2024Q3") is True
        assert await EdgarHelpers.string_cy_validation_async("CY2024Q4") is True

        with pytest.raises(TypeError, match="period must be a string."):
            await EdgarHelpers.string_cy_validation_async(12345)

        assert await EdgarHelpers.string_cy_validation_async("CY2024Q5") is False
        assert await EdgarHelpers.string_cy_validation_async("CY2024Q0") is False
        assert await EdgarHelpers.string_cy_validation_async("2024-01-01") is False

    def test_cik_validation(self):
        assert EdgarHelpers.cik_validation("1744489") == "0001744489"
        assert EdgarHelpers.cik_validation("1234567890") == "1234567890"

        with pytest.raises(TypeError, match="central_index_key must be a string."):
            EdgarHelpers.cik_validation(1234567890)

        with pytest.raises(ValueError, match="CIK must be 10 digits or less."):
            EdgarHelpers.cik_validation("123456789123")

    @pytest.mark.asyncio
    async def test_cik_validation_async(self):
        assert await EdgarHelpers.cik_validation_async("1744489") == "0001744489"
        assert await EdgarHelpers.cik_validation_async("1234567890") == "1234567890"

        with pytest.raises(TypeError, match="central_index_key must be a string."):
            await EdgarHelpers.cik_validation_async(1234567890)

        with pytest.raises(ValueError, match="CIK must be 10 digits or less."):
            await EdgarHelpers.cik_validation_async("123456789123")
