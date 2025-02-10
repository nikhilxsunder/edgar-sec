"""
A simple python wrapper for interacting with the US Securities and Exchange Commission API: EDGAR
"""
# Imports
import requests

class EdgarAPI:
    """
    "data.sec.gov" was created to host RESTful data Application Programming Interfaces (APIs) 
    delivering JSON-formatted data to external customers and to web pages on SEC.gov. These APIs 
    do not require any authentication or API keys to access.

    Currently included in the APIs are the submissions history by filer and the XBRL data from 
    financial statements (forms 10-Q, 10-K, 8-K, 20-F, 40-F, 6-K, and their variants).

    The JSON structures are updated throughout the day, in real time, as submissions are 
    disseminated.

    In addition, a bulk ZIP file is available to download all the JSON structures for an API. 
    This ZIP file is updated and republished nightly at approximately 3:00 a.m. ET.
    """
    # Dunder Methods
    def __init__(self):
        self.base_url = 'https://data.sec.gov'
    # Private Methods
    def __edgar_get_request(self, url_endpoint):
        headers={
            'User-Agent': 'Mozilla/5.0 (compatible; SEC-API/1.0; +https://www.sec.gov)',
            'Accept': 'application/json'
        }
        req = requests.get((self.base_url + url_endpoint), headers=headers,
                           timeout=10)
        req.raise_for_status()
        return req.text
    # Public Methods
    def get_submissions(self, central_index_key):
        """
        Each entity's current filing history is available at the following URL:

        https://data.sec.gov/submissions/CIK##########.json
        Where the ########## is the entity's 10-digit Central Index Key (CIK), including leading 
        zeros.

        This JSON data structure contains metadata such as current name, former name, and stock 
        exchanges and ticker symbols of publicly-traded companies. The object's property path 
        contains at least one year's of filing or to 1,000 (whichever is more) of the most recent 
        filings in a compact columnar data array. If the entity has additional filings, files will 
        contain an array of additional JSON files and the date range for the filings each one 
        contains.

        Parameters
        ----------
        central_index_key : str
            10-digit Central Index Key (CIK), including leading zeros. A CIK may be obtained at the 
            followwing url: https://www.sec.gov/search-filings/cik-lookup
        """
        url_endpoint = f'/submissions/CIK{central_index_key}.json'
        resp = self.__edgar_get_request(url_endpoint)
        return resp
    def get_company_concept(self, central_index_key, taxonomy, tag):
        """
        The company-concept API returns all the XBRL disclosures from a single company (CIK) and 
        concept (a taxonomy and tag) into a single JSON file, with a separate array of facts for 
        each units on measure that the company has chosen to disclose (e.g. net profits reported 
        in U.S. dollars and in Canadian dollars).

        https://data.sec.gov/api/xbrl/companyconcept/CIK##########/us-gaap/AccountsPayableCurrent.json

        Parameters
        ----------
        central_index_key : str
            10-digit Central Index Key (CIK), including leading zeros. A CIK may be obtained at the 
            followwing url: https://www.sec.gov/search-filings/cik-lookup
        taxonomy : str
            a non-custom taxonomy (e.g. 'us-gaap', 'ifrs-full', 'dei', or 'srt')
        tag : str
            e.g. 'AccountsPayableCurrent'
        """
        url_endpoint = f'/api/xbrl/companyconcept/CIK{central_index_key}/{taxonomy}/{tag}'
        resp = self.__edgar_get_request(url_endpoint)
        return resp
    def get_company_facts(self, central_index_key):
        """
        This API returns all the company concepts data for a company into a single API call:

        https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
        """
        url_endpoint = f'api/xbrl//companyfacts/CIK{central_index_key}.json'
        resp = self.__edgar_get_request(url_endpoint)
        return resp
    def get_frames(self, taxonomy, tag, unit, period):
        """
        The xbrl/frames API aggregates one fact for each reporting entity that is last filed that 
        most closely fits the calendrical period requested. This API supports for annual, quarterly 
        and instantaneous data:

        https://data.sec.gov/api/xbrl/frames/us-gaap/AccountsPayableCurrent/USD/CY2019Q1I.json
        Where the units of measure specified in the XBRL contains a numerator and a denominator, 
        these are separated by “-per-” such as “USD-per-shares”. Note that the default unit in 
        XBRL is “pure”.

        The period format is CY#### for annual data (duration 365 days +/- 30 days), CY####Q# 
        for quarterly data (duration 91 days +/- 30 days), and CY####Q#I for instantaneous data. 
        Because company financial calendars can start and end on any month or day and even change 
        in length from quarter to quarter to according to the day of the week, the frame data is 
        assembled by the dates that best align with a calendar quarter or year. Data users should 
        be mindful different reporting start and end dates for facts contained in a frame.

        Parameters
        ----------
        taxonomy : str
            a non-custom taxonomy (e.g. 'us-gaap', 'ifrs-full', 'dei', or 'srt')
        tag : str
            e.g. 'AccountsPayableCurrent'
        unit : str
            default is 'pure' denominated units are seperated by '-per-' e.g. 'USD-per-shares', 
            nondenominated e.g. 'USD'
        period : str
            annual format (duration 365 days +/- 30 days): CY#### e.g. 'CY2019'
            quarterly format (duration 91 days +/- 30 days): CY####Q# e.g. 'CY2019Q1'
            instantaneous format: CY####Q#I e.g. 'CY2019Q1I'
        """
        url_endpoint = f'/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json'
        resp = self.__edgar_get_request(url_endpoint)
        return resp