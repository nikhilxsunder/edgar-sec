# filepath: /src/edgar_sec/clients.py
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
A feature-rich python-package for interacting with the US Securities and Exchange Commission API: EDGAR
"""
# Imports
from collections import deque
from typing import Optional, Dict, Any, Tuple, Union, cast
import asyncio
import time
from datetime import datetime
from tenacity import retry, wait_fixed, stop_after_attempt
from cachetools import FIFOCache, cached
from asyncache import cached as async_cached
import httpx
from edgar_sec.objects import CompanyConcept, SubmissionHistory, CompanyFacts, Frame
from edgar_sec.helpers import EdgarHelpers
from edgar_sec.__about__ import __title__, __version__, __author__, __license__, __copyright__, __description__, __url__

class EdgarAPI:
    """Interact with the US Securities and Exchange Commission EDGAR API.

    This class provides methods to access the SEC's EDGAR database through their
    RESTful API endpoints. The data.sec.gov service delivers JSON-formatted data
    without requiring authentication or API keys. The API provides access to: Filing
    entity submission history and XBRL financial statement data (forms 10-Q, 10-K,
    8-K, 20-F, 40-F, 6-K).
    """
    # Dunder Methods
    def __init__(self, cache_mode: bool=False, cache_size: int=256) -> None:
        """
        Initialize the EdgarAPI class the provide functions for accessing SEC EDGAR data.

        Args:
            cache_mode (bool): Whether to enable caching for API responses. Defaults to False.
            cache_size (int): The maximum number of items to store in the cache if caching is enabled. Defaults to 256.

        Returns:
            EdgarAPI: An instance of the EdgarAPI class.

        Raises:
            ValueError: If the cache_size parameter is not a positive integer.

        Example:
            >>> import edgar_sec as ed
            >>> api = ed.EdgarAPI(cache_mode=True)

        Note:
            Unlike many APIs, the SEC EDGAR API doesn't require an API key, but it does enforce a
            rate limit of 10 requests per second which this implementation automatically respects.
        """
        self.base_url: str = 'https://data.sec.gov'
        self.headers: Dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (compatible; SEC-API/1.0; +https://www.sec.gov)',
            'Accept': 'application/json'
        }
        self.cache_mode: bool = cache_mode
        self.cache_size: int = cache_size
        self.cache: FIFOCache = FIFOCache(maxsize=cache_size)
        self.max_requests_per_second = 10
        self.request_times: deque = deque()
        self.lock: asyncio.Lock = asyncio.Lock()
        self.semaphore: asyncio.Semaphore = asyncio.Semaphore(self.max_requests_per_second)
        self.Async: EdgarAPI.AsyncAPI = self.AsyncAPI(self)
    def __repr__(self) -> str:
        """
        string representation of the EdgarAPI class.

        Returns:
            str: A string representation of the EdgarAPI class.
        """
        return f"EdgarAPI(cache_mode={self.cache_mode}, cache_size={self.cache_size})"
    def __str__(self) -> str:
        """
        string representation of the EdgarAPI class.

        Returns:
            str: A string representation of the EdgarAPI class.
        """
        return (
            f"EdgarAPI Instance:\n"
            f"Base URL: {self.base_url}\n"
            f"Cache Mode: {'Enabled' if self.cache_mode else 'Disabled'}\n"
            f"Cache Size: {self.cache_size}\n"
            f"Max Requests per Second: {self.max_requests_per_second}\n"
        )
    def __eq__(self, other: object) -> bool:
        """
        Equality comparison for the EdgarAPI class.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(other, EdgarAPI):
            return NotImplemented
        return (
            self.cache_mode == other.cache_mode and
            self.cache_size == other.cache_size
        )
    def __hash__(self) -> int:
        """
        Hash function for the EdgarAPI class.

        Returns:
            int: A hash value for the EdgarAPI instance.
        """
        return hash((self.cache_mode, self.cache_size))
    def __del__(self) -> None:
        """
        Destructor for the EdgarAPI class. Clears the cache when the instance is deleted.
        """
        if hasattr(self, "cache"):
            self.cache.clear()
    def __getitem__(self, key: str) -> Any:
        """
        Get a specific item from the cache.

        Args:
            key (str): The name of the attribute to get.

        Returns:
            Any: The value of the attribute.

        Raises:
            AttributeError: If the key does not exist.
        """
        if key in self.cache.keys():
            return self.cache[key]
        else:
            raise AttributeError(f"'{key}' not found in cache.")
    def __len__(self) -> int:
        """
        Get the number of cached items in the EdgarAPI class.

        Returns:
            int: The number of cached items in the EdgarAPI instance.
        """
        return len(self.cache)
    def __contains__(self, key: str) -> bool:
        """
        Check if a specific item exists in the cache.

        Args:
            key (str): The name of the attribute to check.

        Returns:
            bool: True if the attribute exists, False otherwise.
        """
        return key in self.cache.keys() if self.cache_mode else False
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a specific item in the cache.

        Args:
            key (str): The name of the attribute to set.
            value (Any): The value to set.
        """
        self.cache[key] = value
    def __delitem__(self, key: str) -> None:
        """
        Delete a specific item from the cache.

        Args:
            key (str): The name of the attribute to delete.

        Raises:
            AttributeError: If the key does not exist in the cache.
        """
        if key in self.cache.keys():
            del self.cache[key]
        else:
            raise AttributeError(f"'{key}' not found in cache.")
    def __call__(self) -> str:
        """
        Call the EdgarAPI instance to get a summary of its configuration.

        Returns:
            str: A string representation of the EdgarAPI instance's configuration.
        """
        return (
            f"EdgarAPI Instance:\n"
            f"  Base URL: {self.base_url}\n"
            f"  Cache Mode: {'Enabled' if self.cache_mode else 'Disabled'}\n"
            f"  Cache Size: {self.cache_size}\n"
        )
    # Private Methods
    @retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
    def __rate_limited(self) -> None:
        """
        Ensures synchronous requests comply with rate limits.
        """
        now = time.time()
        self.request_times.append(now)
        while self.request_times and self.request_times[0] < now - 1:
            self.request_times.popleft()
        if len(self.request_times) >= self.max_requests_per_second:
            time.sleep(1 - (now - self.request_times[0]))
    @retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
    def __edgar_get_request(self, url_endpoint: str) -> Dict[Any, Any]:
        """
        Helper method to perform a synchronous GET request to the EDGAR API.
        """
        def __get_request(url_endpoint: str) -> Dict[Any, Any]:
            """
            Helper method to perform a synchronous GET request to the EDGAR API.
            """
            self.__rate_limited()
            with httpx.Client() as client:
                response = client.get((self.base_url + url_endpoint), headers=self.headers, timeout=10)
                response.raise_for_status()
                response_json = response.json()
                return response_json
        @cached(cache=self.cache)
        def __cached_get_request(url_endpoint: str) -> Dict[Any, Any]:
            """
            Helper method to perform a synchronous GET request to the EDGAR API with caching.
            """
            return __get_request(url_endpoint)
        if self.cache_mode:
            return __cached_get_request(url_endpoint)
        else:
            return __get_request(url_endpoint)
    # Public Methods
    def get_submissions(self, ticker: Optional[str]=None, central_index_key: Optional[str]=None) -> SubmissionHistory:
        """Get a submission history.

        Retrieve a company's submission history from the SEC EDGAR database.

        Args:
            ticker (str, optional): The ticker symbol of the company. If provided, the CIK will be derived from the ticker.
            central_index_key (str, optional): 10-digit Central Index Key (CIK) of the entity, including leading zeros. A CIK may be obtained at the SEC's CIK lookup: https://www.sec.gov/search-filings/cik-lookup

        Returns:
            SubmissionHistory: An object containing the entity's filing history, including company information and recent filings.

        Raises:
            ValueError: If the request fails or the response is not valid JSON format.

        Example:
            >>> import edgar_sec as ed
            >>> api = ed.EdgarAPI()
            >>> apple_history = api.get_submissions("AAPL")
            >>> print(apple_history.name)
            'Apple Inc.'

        Note:
            This endpoint returns the most recent 1,000 filings or at least one year's worth, whichever is more. For entities with additional filings, the response includes references to additional JSON files and their date ranges.
        """
        if ticker and central_index_key:
            raise ValueError("Provide either ticker or central_index_key, not both.")
        if central_index_key is None and ticker is None:
            raise ValueError("Provide either ticker or central_index_key.")
        if ticker:
            central_index_key = cast(str, EdgarHelpers.get_cik(ticker=ticker))
        assert central_index_key is not None
        central_index_key = EdgarHelpers.cik_validation(central_index_key)
        url_endpoint = f'/submissions/CIK{central_index_key}.json'
        response = self.__edgar_get_request(url_endpoint)
        return SubmissionHistory.to_object(response)
    def get_company_concept(self, taxonomy: str, tag: str, ticker: Optional[str]=None, central_index_key: Optional[str]=None) -> CompanyConcept:
        """Get a company concept.

        Retrieve XBRL disclosures for a specific concept from a company.

        Args:
            ticker (str, optional): The ticker symbol of the company. If provided, the CIK will be derived from the ticker.
            central_index_key (str, optional): 10-digit Central Index Key (CIK) of the entity, including leading zeros. A CIK may be obtained at the SEC's CIK lookup: https://www.sec.gov/search-filings/cik-lookup
            taxonomy (str): A non-custom taxonomy identifier (e.g. 'us-gaap', 'ifrs-full', 'dei', or 'srt').
            tag (str): The specific disclosure concept tag to retrieve, such as 'AccountsPayableCurrent' or 'Assets'.

        Returns:
            CompanyConcept: An object containing all disclosures related to the specified concept, organized by units of measure.

        Raises:
            ValueError: If the request fails or the response is not valid JSON format.

        Example:
            >>> import edgar_sec as ed
            >>> api = ed.EdgarAPI()
            >>> concept = api.get_company_concept("us-gaap", "AccountsPayableCurrent", "AAPL")
            >>> for unit in concept.units:
            >>>     print(f"Value: {unit.val}, Period: {unit.end}")

        Note:
            This endpoint returns separate arrays of facts for each unit of measure that the company has disclosed (e.g., values reported in both USD and EUR).
        """
        if ticker and central_index_key:
            raise ValueError("Provide either ticker or central_index_key, not both.")
        if central_index_key is None and ticker is None:
            raise ValueError("Provide either ticker or central_index_key.")
        if ticker:
            central_index_key = cast(str, EdgarHelpers.get_cik(ticker=ticker))
        assert central_index_key is not None
        central_index_key = EdgarHelpers.cik_validation(central_index_key)
        url_endpoint = f'/api/xbrl/companyconcept/CIK{central_index_key}/{taxonomy}/{tag}.json'
        response = self.__edgar_get_request(url_endpoint)
        return CompanyConcept.to_object(response)
    def get_company_facts(self, ticker: Optional[str]=None, central_index_key: Optional[str]=None) -> CompanyFacts:
        """Get all company facts.

        Retrieve all XBRL disclosures for a company in a single request.

        Args:
            ticker (str, optional): The ticker symbol of the company. If provided, the CIK will be derived from the ticker.
            central_index_key (str, optional): 10-digit Central Index Key (CIK) of the entity, including leading zeros. A CIK may be obtained at the SEC's CIK lookup: https://www.sec.gov/search-filings/cik-lookup

        Returns:
            CompanyFact: An object containing all facts and disclosures for the company, organized by taxonomy and concept.

        Raises:
            ValueError: If the request fails or the response is not valid JSON format.

        Example:
            >>> import edgar_sec as ed
            >>> api = ed.EdgarAPI()
            >>> facts = api.get_company_facts("AAPL")
            >>> revenue = facts.facts["us-gaap"].disclosures.get("RevenueFromContractWithCustomerExcludingAssessedTax")
            >>> if revenue and "USD" in revenue.units:
            >>>     print(f"Latest revenue: ${revenue.units['USD'][0].val}")

        Note:
            This is the most comprehensive endpoint, returning all concepts across all taxonomies for a company. The response can be quite large for companies with extensive filing histories.
        """
        if ticker and central_index_key:
            raise ValueError("Provide either ticker or central_index_key, not both.")
        if central_index_key is None and ticker is None:
            raise ValueError("Provide either ticker or central_index_key.")
        if ticker:
            central_index_key = cast(str, EdgarHelpers.get_cik(ticker=ticker))
        assert central_index_key is not None
        central_index_key = EdgarHelpers.cik_validation(central_index_key)
        url_endpoint = f'/api/xbrl/companyfacts/CIK{central_index_key}.json'
        response = self.__edgar_get_request(url_endpoint)
        return CompanyFacts.to_object(response)
    def get_frames(self, taxonomy: str, tag: str, unit: str, period: Union[str, datetime], instantaneous: bool) -> Frame:
        """

        Retrieve aggregated XBRL facts across multiple companies for a specific period.

        Args:
            taxonomy (str): A non-custom taxonomy identifier (e.g. 'us-gaap', 'ifrs-full', 'dei', or 'srt').
            tag (str): The specific disclosure concept tag to retrieve (e.g. 'AccountsPayableCurrent', 'Assets').
            unit (str): Unit of measurement for the requested data. Default is 'pure'. Denominated units are separated by '-per-' (e.g. 'USD-per-shares'), non-denominated units are specified directly (e.g. 'USD').
            period (str | datetime): The reporting period as a datetime object or a string in the formats: "YYYY-MM-DD" or Annual (365 days ±30 days): CY#### (e.g. 'CY2019'), Quarterly (91 days ±30 days): CY####Q# (e.g. 'CY2019Q1'), Instantaneous: CY####Q#I (e.g. 'CY2019Q1I').
            instantaneous (bool): Whether the period is instantaneous (e.g. 'CY2019Q1I').

        Returns:
            Frame: An object containing facts from multiple companies for the specified concept and period.

        Example:
            >>> import edgar_sec as ed
            >>> api = ed.EdgarAPI()
            >>> frame = api.get_frames("us-gaap", "AccountsPayableCurrent", "USD", "2019-01-01", instantaneous=True)
            >>> for i, disclosure in enumerate(frame.data[:3]):
            >>>     print(f"{disclosure.entity_name}: ${disclosure.val}")

        Note:
            Due to varying company fiscal calendars, the frame data is assembled using the dates that best align with calendar periods. Be mindful that facts in a frame may have different exact reporting start and end dates.
        """
        if not isinstance(period, (str, datetime)):
            raise TypeError("period must be a string or datetime object.")
        if isinstance(period, datetime):
            period = EdgarHelpers.datetime_cy_conversion(period)
        elif isinstance(period, str):
            if not EdgarHelpers.string_cy_validation(period):
                period = EdgarHelpers.string_cy_conversion(period)
        if instantaneous and not period.endswith("I"):
            period += "I"
        url_endpoint = f'/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json'
        response = self.__edgar_get_request(url_endpoint)
        return Frame.to_object(response)
    class AsyncAPI:
        """
        The Async sub-class contains methods for interacting with the SEC EDGAR API asynchronously.
        """
        # Dunder Methods
        def __init__(self, parent: 'EdgarAPI') -> None:
            """
            Initialize with a reference to the parent EdgarAPI instance.
            """
            self._parent: EdgarAPI = parent
            self.cache_mode: bool = parent.cache_mode
            self.cache: FIFOCache = parent.cache
            self.base_url: str = parent.base_url
            self.headers: Dict[str, str] = parent.headers
        def __repr__(self) -> str:
            """
            String representation of the AsyncAPI Instance.

            Returns:
                str: A string representation of the AsyncAPI class.
            """
            return f"{self._parent.__repr__()}.AsyncAPI"
        def __str__(self) -> str:
            """
            String representation of the AsyncAPI Instance.

            Returns:
                str: A string representation of the AsyncAPI class.
            """
            return (
                f"{self._parent.__str__()}\n"
                f"  AsyncAPI Instance:\n"
                f"    Base URL: {self.base_url}\n"
            )
        def __eq__(self, other: object) -> bool:
            """
            Equality comparison for the AsyncAPI class.

            Args:
                other (object): The object to compare with.

            Returns:
                bool: True if the objects are equal, False otherwise.
            """
            if not isinstance(other, EdgarAPI.AsyncAPI):
                return NotImplemented
            return (
                self._parent.cache_mode == other._parent.cache_mode and
                self._parent.cache_size == other._parent.cache_size
            )
        def __hash__(self) -> int:
            """
            Hash function for the AsyncAPI instance.

            Returns:
                int: A hash value for the AsyncAPI instance.
            """
            return hash((self._parent.cache_mode, self._parent.cache_size, self.base_url))
        def __del__(self) -> None:
            """
            Destructor for the AsyncAPI class. Clears the cache when the instance is deleted.
            """
            if hasattr(self, "cache"):
                self.cache.clear()
        def __getitem__(self, key: str) -> Any:
            """
            Get a specific item from the cache.

            Args:
                key (str): The name of the attribute to get.

            Returns:
                Any: The value of the attribute.

            Raises:
                AttributeError: If the key does not exist.
            """
            if key in self.cache.keys():
                return self.cache[key]
            else:
                raise AttributeError(f"'{key}' not found in cache.")
        def __len__(self) -> int:
            """
            Get the length of the cache.

            Returns:
                int: The number of items in the cache.
            """
            return len(self.cache)
        def __contains__(self, key: str) -> bool:
            """
            Check if a specific item exists in the cache.

            Args:
                key (str): The name of the attribute to check.

            Returns:
                bool: True if the attribute exists, False otherwise.
            """
            return key in self.cache.keys()
        def __setitem__(self, key: str, value: Any) -> None:
            """
            Set a specific item in the cache.

            Args:
                key (str): The name of the attribute to set.
                value (Any): The value to set.
            """
            self.cache[key] = value
        def __delitem__(self, key: str) -> None:
            """
            Delete a specific item from the cache.

            Args:
                key (str): The name of the attribute to delete.

            Raises:
                AttributeError: If the key does not exist in the cache.
            """
            if key in self.cache.keys():
                del self.cache[key]
            else:
                raise AttributeError(f"'{key}' not found in cache.")
        def __call__(self) -> str:
            """
            Call the AsyncAPI instance to get a summary of its configuration.

            Returns:
                str: A string representation of the AsyncAPI instance's configuration.
            """
            return (
                f"EdgarAPI Instance\n"
                f"  AsyncAPI Instance:\n"
                f"    Base URL: {self.base_url}\n"
                f"    Cache Mode: {'Enabled' if self.cache_mode else 'Disabled'}\n"
                f"    Cache Size: {len(self.cache)} items\n"
            )
        # Private Methods
        async def __update_semaphore(self) -> Tuple[int, float]:
            """
            Dynamically adjusts the semaphore based on requests left in the second.
            """
            async with self._parent.lock:
                now = time.time()
                while self._parent.request_times and self._parent.request_times[0] < now - 1:
                    self._parent.request_times.popleft()
                requests_made = len(self._parent.request_times)
                requests_left = max(0, self._parent.max_requests_per_second - requests_made)
                time_left = max(0, 1 - (now - (self._parent.request_times[0] if self._parent.request_times else now)))
                new_limit = max(1, requests_left)
                self._parent.semaphore = asyncio.Semaphore(new_limit)
                return requests_left, time_left
        @retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
        async def __rate_limited(self) -> None:
            """
            Enforces the rate limit dynamically based on requests left in the current second.
            """
            async with self._parent.semaphore:
                requests_left, time_left = await self.__update_semaphore()
                if requests_left > 0:
                    sleep_time = time_left / max(1, requests_left)
                    await asyncio.sleep(sleep_time)
                else:
                    await asyncio.sleep(time_left)
                async with self._parent.lock:
                    self._parent.request_times.append(time.time())
        @retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
        async def __edgar_get_request(self, url_endpoint: str) -> Dict[Any, Any]:
            """
            Helper method to perform an asynchronous GET request to the EDGAR API.
            """
            async def __get_request(url_endpoint: str) -> Dict[Any, Any]:
                """
                Helper method to perform an asynchronous GET request to the EDGAR API.
                """
                await self.__rate_limited()
                async with httpx.AsyncClient() as client:
                    response = await client.get((self.base_url + url_endpoint), headers=self.headers, timeout=10)
                    response.raise_for_status()
                    response_json = response.json()
                    return response_json
            @async_cached(cache=self.cache)
            async def __cached_get_request(url_endpoint: str) -> Dict[Any, Any]:
                return await __get_request(url_endpoint)
            if self.cache_mode:
                return await __cached_get_request(url_endpoint)
            else:
                return await __get_request(url_endpoint)
        # Public Methods
        async def get_submissions(self, ticker: Optional[str]=None, central_index_key: Optional[str]=None) -> SubmissionHistory:
            """Get a submission history.

            Retrieve a company's submission history from the SEC EDGAR database.

            Args:
                ticker (str, optional): The ticker symbol of the company. If provided, the CIK will be derived from the ticker.
                central_index_key (str, optional): 10-digit Central Index Key (CIK) of the entity, including leading zeros. A CIK may be obtained at the SEC's CIK lookup: https://www.sec.gov/search-filings/cik-lookup

            Returns:
                SubmissionHistory: An object containing the entity's filing history, including company information and recent filings.

            Raises:
                ValueError: If the request fails or the response is not valid JSON format.

            Example:
                >>> import edgar_sec as ed
                >>> import asyncio
                >>> async def main():
                >>>     api = ed.EdgarAPI().Async
                >>>     apple_history = await api.get_submissions("AAPL")
                >>>     print(apple_history.name)
                >>> asyncio.run(main())
                'Apple Inc.'

            Note:
                This endpoint returns the most recent 1,000 filings or at least one year's worth, whichever is more. For entities with additional filings, the response includes references to additional JSON files and their date ranges.
            """
            if ticker and central_index_key:
                raise ValueError("Provide either ticker or central_index_key, not both.")
            if central_index_key is None and ticker is None:
                raise ValueError("Provide either ticker or central_index_key.")
            if ticker:
                central_index_key = cast(str, await EdgarHelpers.get_cik_async(ticker=ticker))
            assert central_index_key is not None
            central_index_key = await EdgarHelpers.cik_validation_async(central_index_key)
            url_endpoint = f'/submissions/CIK{central_index_key}.json'
            response = await self.__edgar_get_request(url_endpoint)
            return await SubmissionHistory.to_object_async(response)
        async def get_company_concept(self, taxonomy: str, tag: str, ticker: Optional[str]=None, central_index_key: Optional[str]=None) -> CompanyConcept:
            """Get a company concept.

            Retrieve XBRL disclosures for a specific concept from a company.

            Args:
                ticker (str, optional): The ticker symbol of the company. If provided, the CIK will be derived from the ticker.
                central_index_key (str, optional): 10-digit Central Index Key (CIK) of the entity, including leading zeros. A CIK may be obtained at the SEC's CIK lookup: https://www.sec.gov/search-filings/cik-lookup
                taxonomy (str): A non-custom taxonomy identifier (e.g. 'us-gaap', 'ifrs-full', 'dei', or 'srt').
                tag (str): The specific disclosure concept tag to retrieve, such as 'AccountsPayableCurrent' or 'Assets'.

            Returns:
                CompanyConcept: An object containing all disclosures related to the specified concept, organized by units of measure.

            Raises:
                ValueError: If the request fails or the response is not valid JSON format.

            Example:
                >>> import edgar_sec as ed
                >>> import asyncio
                >>> async def main():
                >>>     api = ed.EdgarAPI()
                >>>     # Get Apple Inc's Accounts Payable disclosure asynchronously
                >>>     concept = await api.Async.get_company_concept("us-gaap", "AccountsPayableCurrent", "AAPL")
                >>>     for unit in concept.units:
                >>>         print(f"Value: {unit.val}, Period: {unit.end}")
                >>> asyncio.run(main())

            Note:
                This endpoint returns separate arrays of facts for each unit of measure that the company has disclosed (e.g., values reported in both USD and EUR).
            """
            if ticker and central_index_key:
                raise ValueError("Provide either ticker or central_index_key, not both.")
            if central_index_key is None and ticker is None:
                raise ValueError("Provide either ticker or central_index_key.")
            if ticker:
                central_index_key = cast(str, await EdgarHelpers.get_cik_async(ticker=ticker))
            assert central_index_key is not None
            central_index_key = await EdgarHelpers.cik_validation_async(central_index_key)
            url_endpoint = f'/api/xbrl/companyconcept/CIK{central_index_key}/{taxonomy}/{tag}.json'
            response = await self.__edgar_get_request(url_endpoint)
            return await CompanyConcept.to_object_async(response)
        async def get_company_facts(self, ticker: Optional[str]=None, central_index_key: Optional[str]=None) -> CompanyFacts:
            """Get all company facts.

            Retrieve all XBRL disclosures for a company in a single request.

            Args:
                ticker (str, optional): The ticker symbol of the company. If provided, the CIK will be derived from the ticker.
                central_index_key (str): 10-digit Central Index Key (CIK) of the entity, including leading zeros. A CIK may be obtained at the SEC's CIK lookup: https://www.sec.gov/search-filings/cik-lookup

            Returns:
                CompanyFact: An object containing all facts and disclosures for the company, organized by taxonomy and concept.

            Raises:
                ValueError: If the request fails or the response is not valid JSON format.

            Example:
                >>> import edgar_sec as ed
                >>> import asyncio
                >>> async def main():
                >>>     api = ed.EdgarAPI()
                >>>     facts = await api.Async.get_company_facts("AAPL")
                >>>     revenue = facts.facts["us-gaap"].disclosures.get("RevenueFromContractWithCustomerExcludingAssessedTax")
                >>>     if revenue and "USD" in revenue.units:
                >>>         print(f"Latest revenue: ${revenue.units['USD'][0].val}")
                >>> asyncio.run(main())

            Note:
                This is the most comprehensive endpoint, returning all concepts across all taxonomies for a company. The response can be quite large for companies with extensive filing histories.
            """
            if ticker and central_index_key:
                raise ValueError("Provide either ticker or central_index_key, not both.")
            if central_index_key is None and ticker is None:
                raise ValueError("Provide either ticker or central_index_key.")
            if ticker:
                central_index_key = cast(str, await EdgarHelpers.get_cik_async(ticker=ticker))
            assert central_index_key is not None
            central_index_key = await EdgarHelpers.cik_validation_async(central_index_key)
            url_endpoint = f'/api/xbrl/companyfacts/CIK{central_index_key}.json'
            response = await self.__edgar_get_request(url_endpoint)
            return await CompanyFacts.to_object_async(response)
        async def get_frames(self, taxonomy: str, tag: str, unit: str, period: Union[str, datetime], instantaneous: bool) -> Frame:
            """Get frames for a period.

            Retrieve aggregated XBRL facts across multiple companies for a specific period.

            Args:
                taxonomy (str): A non-custom taxonomy identifier (e.g. 'us-gaap', 'ifrs-full', 'dei', or 'srt').
                tag (str): The specific disclosure concept tag to retrieve (e.g. 'AccountsPayableCurrent', 'Assets').
                unit (str): Unit of measurement for the requested data. Default is 'pure'. Denominated units are separated by '-per-' (e.g. 'USD-per-shares'), non-denominated units are specified directly (e.g. 'USD').
                period (str | datetime): The reporting period as a datetime object or a string in the formats: "YYYY-MM-DD" or Annual (365 days ±30 days): CY#### (e.g. 'CY2019'), Quarterly (91 days ±30 days): CY####Q# (e.g. 'CY2019Q1'), Instantaneous: CY####Q#I (e.g. 'CY2019Q1I').
                instantaneous (bool): Whether the period is instantaneous (e.g. 'CY2019Q1I').
            Returns:
                Frame: An object containing facts from multiple companies for the specified concept and period.

            Raises:
                ValueError: If the request fails or the response is not valid JSON format.

            Example:
                >>> from edgar_sec import EdgarAPI
                >>> import asyncio
                >>> async def main():
                >>>     api = EdgarAPI()
                >>>     frame = await api.Async.get_frames("us-gaap", "AccountsPayableCurrent", "USD", "CY2019Q1I")
                >>>     for i, disclosure in enumerate(frame.data[:3]):
                >>>         print(f"{disclosure.entity_name}: ${disclosure.val}")
                >>> asyncio.run(main())

            Note:
                Due to varying company fiscal calendars, the frame data is assembled using the dates that best align with calendar periods. Be mindful that facts in a frame may have different exact reporting start and end dates.
            """
            if not isinstance(period, (str, datetime)):
                raise TypeError("period must be a string or datetime object.")
            if isinstance(period, datetime):
                period = await EdgarHelpers.datetime_cy_conversion_async(period)
            elif isinstance(period, str):
                if not await EdgarHelpers.string_cy_validation_async(period):
                    period = await EdgarHelpers.string_cy_conversion_async(period)
            if instantaneous and not period.endswith("I"):
                period += "I"
            url_endpoint = f'/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json'
            response = await self.__edgar_get_request(url_endpoint)
            return await Frame.to_object_async(response)
