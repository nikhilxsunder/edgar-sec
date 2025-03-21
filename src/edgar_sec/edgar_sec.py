"""
A feature-rich python wrapper for interacting with the US Securities and Exchange Commission API: EDGAR
"""
# Imports
from collections import deque
import asyncio
import time
from tenacity import retry, wait_fixed, stop_after_attempt
from cachetools import TTLCache
import httpx
from edgar_sec.edgar_data import CompanyConcept, SubmissionHistory, CompanyFact, Frame

class EdgarAPI:
    """Interact with the US Securities and Exchange Commission EDGAR API.

    This class provides methods to access the SEC's EDGAR database through their
    RESTful API endpoints. The data.sec.gov service delivers JSON-formatted data
    without requiring authentication or API keys. The API provides access to: Filing
    entity submission history and XBRL financial statement data (forms 10-Q, 10-K,
    8-K, 20-F, 40-F, 6-K).

    Examples:
        >>> api = EdgarAPI(cache_mode=True)
        >>> apple_data = api.get_submissions("0000320193")
        >>> company_concept = api.get_company_concept("0000320193", "us-gaap", "AccountsPayable")

    Note:
        The SEC imposes a request rate limit which this implementation respects
        through built-in rate limiting mechanisms. The rate limit is 10 requests
        per second. If the rate limit is exceeded, the API will raise a
        `ValueError` with an appropriate message.
    """
    # Dunder Methods
    def __init__(self, cache_mode=False):
        """Initialize the EdgarAPI class for accessing SEC EDGAR data.

        Args:
            cache_mode (bool): Whether to cache API responses locally. Default is False.
                When True, responses are stored in memory for up to 1 hour.

        Returns:
            EdgarAPI: An instance of the EdgarAPI class.

        Example:
            >>> from edgar_sec import EdgarAPI
            >>> api = EdgarAPI(cache_mode=True)
            >>> # Subsequent identical requests will use cached data
            >>> apple_data = api.get_submissions("0000320193")

        Note:
            Unlike many APIs, the SEC EDGAR API doesn't require an API key, but it
            does enforce a rate limit of 10 requests per second which this
            implementation automatically respects.
        """
        self.base_url = 'https://data.sec.gov'
        self.cache_mode = cache_mode
        self.cache = TTLCache(maxsize=256, ttl=3600) if cache_mode else None
        self.max_requests_per_second = 10
        self.request_times = deque()
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(self.max_requests_per_second)
        self.Async = self.AsyncAPI(self)
    # Private Methods
    @retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
    def __rate_limited(self):
        """
        Ensures synchronous requests comply with rate limits (requests per second).
        """
        now = time.time()
        self.request_times.append(now)
        while self.request_times and self.request_times[0] < now - 1:
            self.request_times.popleft()
        if len(self.request_times) >= self.max_requests_per_second:
            time.sleep(1 - (now - self.request_times[0]))
    @retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
    def __edgar_get_request(self, url_endpoint):
        """
        Helper method to perform a synchronous GET request to the EDGAR API.
        """
        key = url_endpoint if self.cache_mode else None
        if self.cache_mode and key and key in self.cache.keys():
            return self.cache.get(key)
        self.__rate_limited()
        headers={
            'User-Agent': 'Mozilla/5.0 (compatible; SEC-API/1.0; +https://www.sec.gov)',
            'Accept': 'application/json'
        }
        with httpx.Client() as client:
            response = client.get((self.base_url + url_endpoint), headers=headers, timeout=10)
            response.raise_for_status()
            response_json = response.json()
        if self.cache_mode and key:
            self.cache.__setitem__(key, response_json)
        return response_json
    # Public Methods
    def get_submissions(self, central_index_key):
        """Retrieve a company's submission history from the SEC EDGAR database.

        Args:
            central_index_key (str): 10-digit Central Index Key (CIK) of the entity,
                including leading zeros. A CIK may be obtained at the SEC's CIK lookup:
                https://www.sec.gov/search-filings/cik-lookup

        Returns:
            SubmissionHistory: An object containing the entity's filing history,
                including company information and recent filings.

        Example:
            >>> from edgar_sec import EdgarAPI
            >>> api = EdgarAPI()
            >>> # Get Apple Inc's submission history
            >>> apple_history = api.get_submissions("0000320193")
            >>> print(apple_history.name)
            'Apple Inc.'

        Note:
            This endpoint returns the most recent 1,000 filings or at least one year's
            worth, whichever is more. For entities with additional filings, the response
            includes references to additional JSON files and their date ranges.
        """
        url_endpoint = f'/submissions/CIK{central_index_key}.json'
        response = self.__edgar_get_request(url_endpoint)
        return SubmissionHistory.from_api_response(response)
    def get_company_concept(self, central_index_key, taxonomy, tag):
        """Retrieve XBRL disclosures for a specific concept from a company.

        Args:
            central_index_key (str): 10-digit Central Index Key (CIK) of the entity, including leading zeros. A CIK may be obtained at the SEC's CIK lookup: https://www.sec.gov/search-filings/cik-lookup
            taxonomy (str): A non-custom taxonomy identifier (e.g. 'us-gaap', 'ifrs-full', 'dei', or 'srt').
            tag (str): The specific disclosure concept tag to retrieve, such as 'AccountsPayableCurrent' or 'Assets'.

        Returns:
            CompanyConcept: An object containing all disclosures related to the specified concept, organized by units of measure.

        Example:
            >>> from edgar_sec import EdgarAPI
            >>> api = EdgarAPI()
            >>> # Get Apple Inc's Accounts Payable disclosure
            >>> concept = api.get_company_concept("0000320193", "us-gaap", "AccountsPayableCurrent")
            >>> for unit in concept.units:
            >>>     print(f"Value: {unit.val}, Period: {unit.end}")

        Note:
            This endpoint returns separate arrays of facts for each unit of measure that
            the company has disclosed (e.g., values reported in both USD and EUR).
        """
        url_endpoint = f'/api/xbrl/companyconcept/CIK{central_index_key}/{taxonomy}/{tag}.json'
        response = self.__edgar_get_request(url_endpoint)
        return CompanyConcept.from_api_response(response)
    def get_company_facts(self, central_index_key):
        """Retrieve all XBRL disclosures for a company in a single request.

        Args:
            central_index_key (str): 10-digit Central Index Key (CIK) of the entity, including leading zeros. A CIK may be obtained at the SEC's CIK lookup: https://www.sec.gov/search-filings/cik-lookup

        Returns:
            CompanyFact: An object containing all facts and disclosures for the company, organized by taxonomy and concept.

        Example:
            >>> from edgar_sec import EdgarAPI
            >>> api = EdgarAPI()
            >>> # Get all Apple Inc's financial disclosures
            >>> facts = api.get_company_facts("0000320193")
            >>> # Access a specific concept in the US GAAP taxonomy
            >>> revenue = facts.facts["us-gaap"].disclosures.get("RevenueFromContractWithCustomerExcludingAssessedTax")
            >>> if revenue and "USD" in revenue.units:
            >>>     print(f"Latest revenue: ${revenue.units['USD'][0].val}")

        Note:
            This is the most comprehensive endpoint, returning all concepts across all
            taxonomies for a company. The response can be quite large for companies
            with extensive filing histories.
        """
        url_endpoint = f'/api/xbrl/companyfacts/CIK{central_index_key}.json'
        response = self.__edgar_get_request(url_endpoint)
        return CompanyFact.from_api_response(response)
    def get_frames(self, taxonomy, tag, unit, period):
        """Retrieve aggregated XBRL facts across multiple companies for a specific period.

        Args:
            taxonomy (str): A non-custom taxonomy identifier (e.g. 'us-gaap', 'ifrs-full', 'dei', or 'srt').
            tag (str): The specific disclosure concept tag to retrieve (e.g. 'AccountsPayableCurrent', 'Assets').
            unit (str): Unit of measurement for the requested data. Default is 'pure'. Denominated units are separated by '-per-' (e.g. 'USD-per-shares'), non-denominated units are specified directly (e.g. 'USD').
            period (str): The reporting period in the format: Annual (365 days ±30 days): CY#### (e.g. 'CY2019'), Quarterly (91 days ±30 days): CY####Q# (e.g. 'CY2019Q1'), Instantaneous: CY####Q#I (e.g. 'CY2019Q1I').

        Returns:
            Frame: An object containing facts from multiple companies for the specified concept and period.

        Example:
            >>> from edgar_sec import EdgarAPI
            >>> api = EdgarAPI()
            >>> # Get all companies' Q1 2019 Accounts Payable data in USD
            >>> frame = api.get_frames("us-gaap", "AccountsPayableCurrent", "USD", "CY2019Q1I")
            >>> # Print the first few results
            >>> for i, disclosure in enumerate(frame.data[:3]):
            >>>     print(f"{disclosure.entity_name}: ${disclosure.val}")

        Note:
            Due to varying company fiscal calendars, the frame data is assembled using
            the dates that best align with calendar periods. Be mindful that facts in a
            frame may have different exact reporting start and end dates.
        """
        url_endpoint = f'/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json'
        response = self.__edgar_get_request(url_endpoint)
        return Frame.from_api_response(response)
    class AsyncAPI:
        """Asynchronous version of the EdgarAPI methods.

        Args:
            parent: The parent EdgarAPI instance that created this AsyncAPI instance.
                This provides access to configuration and resources of the parent.

        Returns:
            AsyncAPI: An instance of the AsyncAPI class that provides async methods
                for all EdgarAPI functionality.

        Example:
            >>> from edgar_sec import EdgarAPI
            >>> import asyncio
            >>> async def get_apple_data():
            >>>     api = EdgarAPI(cache_mode=True)
            >>>     # Get Apple Inc's submission history asynchronously
            >>>     apple_history = await api.Async.get_submissions("0000320193")
            >>>     print(apple_history.name)
            >>> asyncio.run(get_apple_data())
            'Apple Inc.'

        Note:
            All methods in this class are coroutines that must be awaited. They follow
            the same rate limiting as the synchronous methods but are more efficient
            when making multiple concurrent requests.
        """
        # Dunder Methods
        def __init__(self, parent):
            """Initialize the AsyncAPI class for accessing SEC EDGAR data asynchronously.

            Args:
                parent (EdgarAPI): The parent EdgarAPI instance that created this AsyncAPI instance.
                    This provides access to configuration and resources of the parent.

            Returns:
                AsyncAPI: An instance of the AsyncAPI class.

            Example:
                >>> from edgar_sec import EdgarAPI
                >>> api = EdgarAPI(cache_mode=True)
                >>> # The AsyncAPI instance is automatically created and accessible
                >>> async_api = api.Async

            Note:
                This class should not be instantiated directly. Instead, use the
                `Async` attribute of an EdgarAPI instance which is automatically
                created during EdgarAPI initialization.
            """
            self._parent = parent
            self.cache_mode = parent.cache_mode
            self.cache = parent.cache
            self.base_url = parent.base_url
        # Private Methods
        async def __update_semaphore(self):
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
        async def __rate_limited(self):
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
        async def __edgar_get_request(self, url_endpoint):
            """
            Helper method to perform an asynchronous GET request to the EDGAR API.
            """
            cache_key = url_endpoint if self.cache_mode else None
            if self.cache_mode and cache_key:
                cached_response = await asyncio.to_thread(self.cache.get, cache_key)
                if cached_response:
                    return cached_response
            await self.__rate_limited()
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; SEC-API/1.0; +https://www.sec.gov)',
                'Accept': 'application/json'
            }
            async with httpx.AsyncClient() as client:
                try:
                    response = client.get((self.base_url + url_endpoint), headers=headers, timeout=10)
                    response.raise_for_status()
                    response_json = response.json()
                    if self.cache_mode:
                        await asyncio.to_thread(self.cache.__setitem__, cache_key, response_json)
                    return response_json
                except httpx.HTTPStatusError as e:
                    raise ValueError(f"HTTP Error occurred: {e}") from e
                except httpx.RequestError as e:
                    raise ValueError(f"Request Error occurred: {e}") from e
        # Public Methods
        async def get_submissions(self, central_index_key):
            """Asynchronously retrieve a company's submission history from the SEC EDGAR database.

            Args:
                central_index_key (str): 10-digit Central Index Key (CIK) of the entity,
                    including leading zeros. A CIK may be obtained at the SEC's CIK lookup:
                    https://www.sec.gov/search-filings/cik-lookup

            Returns:
                SubmissionHistory: An object containing the entity's filing history,
                    including company information and recent filings.

            Example:
                >>> from edgar_sec import EdgarAPI
                >>> import asyncio
                >>> async def main():
                >>>     api = EdgarAPI()
                >>>     # Get Apple Inc's submission history asynchronously
                >>>     apple_history = await api.Async.get_submissions("0000320193")
                >>>     print(apple_history.name)
                >>> asyncio.run(main())
                'Apple Inc.'

            Note:
                This endpoint returns the most recent 1,000 filings or at least one year's
                worth, whichever is more. For entities with additional filings, the response
                includes references to additional JSON files and their date ranges.
            """
            url_endpoint = f'/submissions/CIK{central_index_key}.json'
            response = await self.__edgar_get_request(url_endpoint)
            return SubmissionHistory.from_api_response(response)
        async def get_company_concept(self, central_index_key, taxonomy, tag):
            """Asynchronously retrieve XBRL disclosures for a specific concept from a company.

            Args:
                central_index_key (str): 10-digit Central Index Key (CIK) of the entity, including leading zeros. A CIK may be obtained at the SEC's CIK lookup: https://www.sec.gov/search-filings/cik-lookup
                taxonomy (str): A non-custom taxonomy identifier (e.g. 'us-gaap', 'ifrs-full', 'dei', or 'srt').
                tag (str): The specific disclosure concept tag to retrieve, such as 'AccountsPayableCurrent' or 'Assets'.

            Returns:
                CompanyConcept: An object containing all disclosures related to the specified concept, organized by units of measure.

            Example:
                >>> from edgar_sec import EdgarAPI
                >>> import asyncio
                >>> async def main():
                >>>     api = EdgarAPI()
                >>>     # Get Apple Inc's Accounts Payable disclosure asynchronously
                >>>     concept = await api.Async.get_company_concept("0000320193", "us-gaap", "AccountsPayableCurrent")
                >>>     for unit in concept.units:
                >>>         print(f"Value: {unit.val}, Period: {unit.end}")
                >>> asyncio.run(main())

            Note:
                This endpoint returns separate arrays of facts for each unit of measure that
                the company has disclosed (e.g., values reported in both USD and EUR).
            """
            url_endpoint = f'/api/xbrl/companyconcept/CIK{central_index_key}/{taxonomy}/{tag}'
            response = await self.__edgar_get_request(url_endpoint)
            return CompanyConcept.from_api_response(response)
        async def get_company_facts(self, central_index_key):
            """Asynchronously retrieve all XBRL disclosures for a company in a single request.

            Args:
                central_index_key (str): 10-digit Central Index Key (CIK) of the entity, including leading zeros. A CIK may be obtained at the SEC's CIK lookup: https://www.sec.gov/search-filings/cik-lookup

            Returns:
                CompanyFact: An object containing all facts and disclosures for the company, organized by taxonomy and concept.

            Example:
                >>> from edgar_sec import EdgarAPI
                >>> import asyncio
                >>> async def main():
                >>>     api = EdgarAPI()
                >>>     # Get all Apple Inc's financial disclosures asynchronously
                >>>     facts = await api.Async.get_company_facts("0000320193")
                >>>     # Access a specific concept in the US GAAP taxonomy
                >>>     revenue = facts.facts["us-gaap"].disclosures.get("RevenueFromContractWithCustomerExcludingAssessedTax")
                >>>     if revenue and "USD" in revenue.units:
                >>>         print(f"Latest revenue: ${revenue.units['USD'][0].val}")
                >>> asyncio.run(main())

            Note:
                This is the most comprehensive endpoint, returning all concepts across all
                taxonomies for a company. The response can be quite large for companies
                with extensive filing histories.
            """
            url_endpoint = f'api/xbrl//companyfacts/CIK{central_index_key}.json'
            response = await self.__edgar_get_request(url_endpoint)
            return response
        async def get_frames(self, taxonomy, tag, unit, period):
            """Asynchronously retrieve aggregated XBRL facts across multiple companies for a specific period.

            Args:
                taxonomy (str): A non-custom taxonomy identifier (e.g. 'us-gaap', 'ifrs-full', 'dei', or 'srt').
                tag (str): The specific disclosure concept tag to retrieve (e.g. 'AccountsPayableCurrent', 'Assets').
                unit (str): Unit of measurement for the requested data. Default is 'pure'. Denominated units are separated by '-per-' (e.g. 'USD-per-shares'), non-denominated units are specified directly (e.g. 'USD').
                period (str): The reporting period in the format: Annual (365 days ±30 days): CY#### (e.g. 'CY2019'), Quarterly (91 days ±30 days): CY####Q# (e.g. 'CY2019Q1'), Instantaneous: CY####Q#I (e.g. 'CY2019Q1I')

            Returns:
                Frame: An object containing facts from multiple companies for the specified concept and period.

            Example:
                >>> from edgar_sec import EdgarAPI
                >>> import asyncio
                >>> async def main():
                >>>     api = EdgarAPI()
                >>>     # Get all companies' Q1 2019 Accounts Payable data in USD asynchronously
                >>>     frame = await api.Async.get_frames("us-gaap", "AccountsPayableCurrent", "USD", "CY2019Q1I")
                >>>     # Print the first few results
                >>>     for i, disclosure in enumerate(frame.data[:3]):
                >>>         print(f"{disclosure.entity_name}: ${disclosure.val}")
                >>> asyncio.run(main())

            Note:
                Due to varying company fiscal calendars, the frame data is assembled using
                the dates that best align with calendar periods. Be mindful that facts in a
                frame may have different exact reporting start and end dates.
            """
            url_endpoint = f'/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json'
            response = await self.__edgar_get_request(url_endpoint)
            return Frame.from_api_response(response)
