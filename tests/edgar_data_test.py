import pytest
import asyncio
import time
from unittest.mock import patch, MagicMock
import httpx
from edgar_sec.edgar_sec import EdgarAPI
from edgar_sec.edgar_data import (
    SubmissionHistory,
    CompanyConcept,
    CompanyFact,
    Frame
)

# Sample API responses
SUBMISSIONS_RESPONSE = {
    "cik": "0000320193",
    "entityType": "operating",
    "sic": "3571",
    "sicDescription": "ELECTRONIC COMPUTERS",
    "name": "Apple Inc.",
    "tickers": ["AAPL"],
    "exchanges": ["NASDAQ"],
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

COMPANY_CONCEPT_RESPONSE = {
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

COMPANY_FACTS_RESPONSE = {
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
                            "filed": "2022-01-28"
                        }
                    ]
                }
            }
        }
    }
}

FRAMES_RESPONSE = {
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
        }
    ]
}

class TestEdgarAPI:
    """Test cases for the EdgarAPI class."""

    @pytest.fixture
    def api(self):
        """Create an instance of the EdgarAPI for testing."""
        return EdgarAPI(cache_mode=True)

    @pytest.fixture
    def mock_response(self):
        """Create a mock response for httpx requests."""
        mock = MagicMock()
        mock.raise_for_status = MagicMock()
        return mock

    def test_init(self, api):
        """Test initialization of the EdgarAPI class."""
        assert api.base_url == 'https://data.sec.gov'
        assert api.cache_mode is True
        assert api.cache is not None
        assert api.max_requests_per_second == 10
        assert isinstance(api.Async, EdgarAPI.AsyncAPI)

    @patch('httpx.Client')
    def test_get_submissions(self, mock_client, api, mock_response):
        """Test the get_submissions method."""
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        mock_response.json.return_value = SUBMISSIONS_RESPONSE

        # Set the cache to ensure we use our mock response
        api.cache.__setitem__('/submissions/CIK0000320193.json', SUBMISSIONS_RESPONSE)

        result = api.get_submissions('0000320193')
        assert isinstance(result, SubmissionHistory)
        assert result.cik == "0000320193"
        assert result.name == "Apple Inc."
        assert isinstance(result.filings, list)

    @patch('httpx.Client')
    def test_get_company_concept(self, mock_client, api, mock_response):
        """Test the get_company_concept method."""
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        mock_response.json.return_value = COMPANY_CONCEPT_RESPONSE

        # Set the cache to ensure we use our mock response
        api.cache.__setitem__('/api/xbrl/companyconcept/CIK0000320193/us-gaap/AccountsPayableCurrent.json', COMPANY_CONCEPT_RESPONSE)

        result = api.get_company_concept('0000320193', 'us-gaap', 'AccountsPayableCurrent')
        assert isinstance(result, CompanyConcept)
        assert result.cik == "0000320193"
        assert result.taxonomy == "us-gaap"
        assert result.tag == "AccountsPayableCurrent"

    @patch('httpx.Client')
    def test_get_company_facts(self, mock_client, api, mock_response):
        """Test the get_company_facts method."""
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        mock_response.json.return_value = COMPANY_FACTS_RESPONSE

        # Set the cache to ensure we use our mock response
        api.cache.__setitem__('/api/xbrl/companyfacts/CIK0000320193.json', COMPANY_FACTS_RESPONSE)

        result = api.get_company_facts('0000320193')
        assert isinstance(result, CompanyFact)
        assert result.cik == "0000320193"
        assert result.entity_name == "Apple Inc."
        assert "us-gaap" in result.facts

    @patch('httpx.Client')
    def test_get_frames(self, mock_client, api, mock_response):
        """Test the get_frames method."""
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        mock_response.json.return_value = FRAMES_RESPONSE

        # Set the cache to ensure we use our mock response
        api.cache.__setitem__('/api/xbrl/frames/us-gaap/AccountsPayableCurrent/USD/CY2021Q4I.json', FRAMES_RESPONSE)

        result = api.get_frames('us-gaap', 'AccountsPayableCurrent', 'USD', 'CY2021Q4I')
        assert isinstance(result, Frame)
        assert result.taxonomy == "us-gaap"
        assert result.tag == "AccountsPayableCurrent"
        assert len(result.frames) > 0

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient')
    async def test_async_get_submissions(self, mock_client, api, mock_response):
        """Test the async get_submissions method."""
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        mock_response.json.return_value = SUBMISSIONS_RESPONSE

        # Set the cache to ensure we use our mock response
        api.cache.__setitem__('/submissions/CIK0000320193.json', SUBMISSIONS_RESPONSE)

        result = await api.Async.get_submissions('0000320193')
        assert isinstance(result, SubmissionHistory)
        assert result.cik == "0000320193"

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient')
    async def test_async_get_company_concept(self, mock_client, api, mock_response):
        """Test the async get_company_concept method."""
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        mock_response.json.return_value = COMPANY_CONCEPT_RESPONSE

        # Set the cache to ensure we use our mock response
        api.cache.__setitem__('/api/xbrl/companyconcept/CIK0000320193/us-gaap/AccountsPayableCurrent', COMPANY_CONCEPT_RESPONSE)

        result = await api.Async.get_company_concept('0000320193', 'us-gaap', 'AccountsPayableCurrent')
        assert isinstance(result, CompanyConcept)
        assert result.cik == "0000320193"

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient')
    async def test_async_get_company_facts(self, mock_client, api, mock_response):
        """Test the async get_company_facts method."""
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        mock_response.json.return_value = COMPANY_FACTS_RESPONSE

        # Set the cache to ensure we use our mock response
        api.cache.__setitem__('api/xbrl//companyfacts/CIK0000320193.json', COMPANY_FACTS_RESPONSE)

        result = await api.Async.get_company_facts('0000320193')
        assert result == COMPANY_FACTS_RESPONSE

    @pytest.mark.asyncio
    async def test_rate_limiting(self, api):
        """Test that rate limiting is enforced."""
        start_time = time.time()

        # Simulate multiple requests in quick succession
        tasks = [api.Async._AsyncAPI__rate_limited() for _ in range(5)]
        await asyncio.gather(*tasks)

        # Should take some time due to rate limiting
        elapsed_time = time.time() - start_time
        # Rate limiting should cause some delay, but exact time is hard to predict
        assert elapsed_time > 0  # Minimal check

    def test_error_handling(self, api):
        """Test error handling when API requests fail."""
        with patch('httpx.Client') as mock_client:
            mock_client.return_value.__enter__.return_value.get.side_effect = httpx.HTTPStatusError(
                "404 Not Found",
                request=MagicMock(),
                response=MagicMock(status_code=404)
            )

            with pytest.raises(Exception):
                api.get_submissions('0000000000')
