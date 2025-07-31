# filepath: /src/edgar_sec/helpers.py
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
This module defines helper methods for the edgar-sec package.
"""

from typing import Optional, List, Union
from datetime import datetime
import asyncio
import re
import httpx
from edgar_sec.objects import Company
from edgar_sec.__about__ import __title__, __version__, __author__, __license__, __copyright__, __description__, __url__

class EdgarHelpers:
    """
    A class containing helper methods for the Edgar SEC module.
    """
    @staticmethod
    def get_cik(ticker:Optional[str]=None, search_text: Optional[str]=None) -> Union[str,List[str]]:
        """
        Helper method to get the CIK (Central Index Key) for a given ticker symbol.

        Args:
            ticker (str): The ticker symbol of the company.
            search_text (str): The name of the company to search for.

        Returns:
            str | List[str]: The CIK of the company or a list of CIKs if multiple matches are found.

        Raises:
            ValueError: If neither ticker nor search_text is provided, or if both are provided.

        Example:

        """
        if (ticker is None and search_text is None) or (ticker and search_text):
            raise ValueError("Provide exactly one of ticker or search_text.")
        with httpx.Client() as client:
            response = client.get(url='https://www.sec.gov/files/company_tickers.json')
            response.raise_for_status()
            data = response.json()
            if ticker:
                for item in data:
                    if item['ticker'] == ticker:
                        return item['cik_str']
                raise ValueError(f"Ticker '{ticker}' not found in the SEC EDGAR database.")
            else:
                assert search_text is not None
                for item in data:
                    if search_text.lower() in item['title'].lower():
                        return item['cik_str']
                raise ValueError(f"Search text '{search_text}' not found in the SEC EDGAR database.")
    @staticmethod
    def get_universe() -> List[Company]:
        """
        Helper method to get the universe of companies from the SEC EDGAR database.

        Returns:
            List[Company]: A list of Company instances representing the universe of companies.
        """
        with httpx.Client() as client:
            response = client.get(url='https://www.sec.gov/files/company_tickers.json')
            response.raise_for_status()
            data = response.json()
            return [Company.to_object(item) for item in data]
    @staticmethod
    def datetime_cy_conversion(period: datetime) -> str:
        """
        Helper method to convert a reporting period in datetime format to the 'CY####Q#' format.

        Args:
            period (datetime): The reporting period as a datetime object.

        Returns:
            str: The reporting period in 'CY####Q#' format.
        """
        if not isinstance(period, datetime):
            raise TypeError("period must be a datetime object.")
        if period.month in [1, 2, 3]:
            return f"CY{period.year}Q{1}"
        elif period.month in [4, 5, 6]:
            return f"CY{period.year}Q{2}"
        elif period.month in [7, 8, 9]:
            return f"CY{period.year}Q{3}"
        else:
            return f"CY{period.year}Q{4}"
    @staticmethod
    def string_cy_conversion(period: str) -> str:
        """
        Helper method to convert a reporting period string in YYYY-MM-DD format to CY####Q# format.

        Args:
            period (str): The reporting period in 'YYYY-MM-DD' format.

        Returns:
            str: The reporting period in 'CY####Q#' format.
        """
        if not isinstance(period, str):
            raise TypeError("period must be a string.")
        try:
            date_obj = datetime.strptime(period, '%Y-%m-%d')
            if date_obj.month in [1, 2, 3]:
                return f"CY{date_obj.year}Q1"
            elif date_obj.month in [4, 5, 6]:
                return f"CY{date_obj.year}Q2"
            elif date_obj.month in [7, 8, 9]:
                return f"CY{date_obj.year}Q3"
            else:
                return f"CY{date_obj.year}Q4"
        except ValueError as e:
            raise ValueError("Invalid date format. Must be in 'YYYY-MM-DD' format.") from e
    @staticmethod
    def string_cy_validation(period: str) -> bool:
        """
        Helper method to validate if a string is in 'CY####' or 'CY####Q#' format.

        Args:
            period (str): The reporting period string to validate.

        Returns:
            bool: True if the string is in 'CY####' or 'CY####Q#' format, False otherwise.
        """
        if not isinstance(period, str):
            raise TypeError("period must be a string.")
        return bool(re.fullmatch(r'CY\d{4}(Q[1-4])?', period))
    @staticmethod
    def cik_validation(central_index_key: str) -> str:
        """
        Helper method to validate and fix the CIK (Central Index Key) format.

        Args:
            central_index_key (str): The CIK to validate.

        Returns:
            str: The validated CIK.

        Raises:
            ValueError: If the CIK is not in the correct format.
        """
        if not isinstance(central_index_key, str):
            raise TypeError("central_index_key must be a string.")
        if len(central_index_key) > 10:
            raise ValueError("CIK must be 10 digits or less.")
        if not re.fullmatch(r'\d{10}', central_index_key):
            return central_index_key.zfill(10)
        else:
            return central_index_key
    @staticmethod
    async def get_cik_async(ticker: Optional[str]=None, search_text: Optional[str] = None) -> Union[str, List[str]]:
        """
        Helper method to asynchronously get the CIK (Central Index Key) for a given ticker symbol.

        Args:
            ticker (str): The ticker symbol of the company.
            search_text (str): The name of the company to search for.

        Returns:
            str | List[str]: The CIK of the company or a list of CIKs if multiple matches are found.
        """
        if (ticker is None and search_text is None) or (ticker and search_text):
            raise ValueError("Provide exactly one of ticker or search_text.")
        async with httpx.AsyncClient() as client:
            response = await client.get(url='https://www.sec.gov/files/company_tickers.json')
            response.raise_for_status()
            data = response.json()
            if ticker:
                for item in data:
                    if item['ticker'] == ticker:
                        return item['cik_str']
                raise ValueError(f"Ticker '{ticker}' not found in the SEC EDGAR database.")
            else:
                assert search_text is not None
                for item in data:
                    if search_text.lower() in item['title'].lower():
                        return item['cik_str']
                raise ValueError(f"Search text '{search_text}' not found in the SEC EDGAR database.")
    @staticmethod
    async def get_universe_async() -> List[Company]:
        """
        Helper method to asynchronously get the universe of companies from the SEC EDGAR database.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(url='https://www.sec.gov/files/company_tickers.json')
            response.raise_for_status()
            data = response.json()
            return [await Company.to_object_async(item) for item in data]
    @staticmethod
    async def datetime_cy_conversion_async(period: datetime) -> str:
        """
        Helper method to convert a reporting period in datetime format to the 'CY####Q#' format.

        Args:
            period (datetime): The reporting period as a datetime object.

        Returns:
            str: The reporting period in 'CY####Q#' format.
        """
        return await asyncio.to_thread(EdgarHelpers.datetime_cy_conversion, period)
    @staticmethod
    async def string_cy_conversion_async(period: str) -> str:
        """
        Helper method to asynchronously convert a reporting period string in YYYY-MM-DD format to CY####Q# format.

        Args:
            period (str): The reporting period in 'YYYY-MM-DD' format.

        Returns:
            str: The reporting period in 'CY####Q#' format.
        """
        return await asyncio.to_thread(EdgarHelpers.string_cy_conversion, period)
    @staticmethod
    async def string_cy_validation_async(period: str) -> bool:
        """
        Helper method to asynchronously validate if a string is in 'CY####' or 'CY####Q#' format.

        Args:
            period (str): The reporting period string to validate.

        Returns:
            bool: True if the string is in 'CY####' or 'CY####Q#' format, False otherwise.
        """
        return await asyncio.to_thread(EdgarHelpers.string_cy_validation, period)
    @staticmethod
    async def cik_validation_async(central_index_key: str) -> str:
        """
        Helper method to asynchronously validate and fix the CIK (Central Index Key) format.

        Args:
            central_index_key (str): The CIK to validate.

        Returns:
            str: The validated CIK.

        Raises:
            ValueError: If the CIK is not in the correct format.
        """
        return await asyncio.to_thread(EdgarHelpers.cik_validation, central_index_key)
