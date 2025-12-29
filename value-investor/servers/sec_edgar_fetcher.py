"""
SEC EDGAR Filing Fetcher

Fetches SEC filings from the SEC EDGAR database for value investing analysis.
Supports 10-K, 10-Q, 8-K, DEF 14A, 13F, and other filing types.

Key Features:
- Fetch up to 10 years of historical filings
- Respect SEC rate limits (10 requests/second)
- Proper User-Agent header (SEC requirement)
- Return both metadata and filing content

SEC EDGAR API Documentation:
https://www.sec.gov/edgar/sec-api-documentation
https://www.sec.gov/developer
"""

import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Literal

from html_cleaner import HTMLCleaner

# SEC requires a User-Agent header with contact information
USER_AGENT = "Value Investor Plugin claude-code-plugin@anthropic.com"

# SEC rate limit: 10 requests per second
RATE_LIMIT_DELAY = 0.1  # 100ms between requests

FilingType = Literal["10-K", "10-Q", "8-K", "DEF 14A", "13F", "SC 13D", "SC 13G", "S-1", "S-3"]


class SECEdgarFetcher:
    """Fetches SEC filings from EDGAR database."""

    def __init__(self, user_agent: str = USER_AGENT):
        """
        Initialize the SEC EDGAR fetcher.

        Args:
            user_agent: User-Agent string (SEC requires contact info)
        """
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})
        self.last_request_time = 0
        self._cleaner = HTMLCleaner()  # HTML cleaning functionality

    def _rate_limit(self):
        """Enforce SEC rate limit of 10 requests/second."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - time_since_last)
        self.last_request_time = time.time()

    def _make_request(self, url: str) -> requests.Response:
        """Make HTTP request with rate limiting."""
        self._rate_limit()
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response

    def get_cik_from_ticker(self, ticker: str) -> Optional[str]:
        """
        Convert stock ticker to CIK (Central Index Key).

        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")

        Returns:
            CIK as zero-padded 10-digit string, or None if not found
        """
        ticker = ticker.upper().strip()

        # Use SEC's company tickers JSON file
        url = "https://www.sec.gov/files/company_tickers.json"

        try:
            response = self._make_request(url)
            data = response.json()

            # Search for ticker in the data
            for entry in data.values():
                if entry.get("ticker", "").upper() == ticker:
                    cik = str(entry["cik_str"]).zfill(10)
                    return cik

            return None
        except Exception as e:
            raise Exception(f"Failed to fetch CIK for ticker {ticker}: {str(e)}")

    def get_company_submissions(self, cik: str) -> Dict:
        """
        Get all submissions metadata for a company.

        Args:
            cik: Central Index Key (10-digit zero-padded string)

        Returns:
            Dictionary with company info and all filings metadata
        """
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"

        try:
            response = self._make_request(url)
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to fetch submissions for CIK {cik}: {str(e)}")

    def fetch_filings(
        self,
        ticker: str,
        filing_types: List[FilingType],
        years: int = 10,
        limit_per_type: Optional[int] = None
    ) -> Dict[str, List[Dict]]:
        """
        Fetch SEC filings for a company.

        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            filing_types: List of filing types to fetch (e.g., ["10-K", "10-Q"])
            years: Number of years of historical data to fetch (default: 10)
            limit_per_type: Maximum number of filings per type (default: all within years)

        Returns:
            Dictionary mapping filing type to list of filing metadata:
            {
                "10-K": [
                    {
                        "accessionNumber": "0000320193-23-000077",
                        "filingDate": "2023-11-03",
                        "reportDate": "2023-09-30",
                        "form": "10-K",
                        "fileNumber": "001-36743",
                        "primaryDocument": "aapl-20230930.htm",
                        "primaryDocUrl": "https://www.sec.gov/...",
                        "documentsUrl": "https://www.sec.gov/...",
                        "companyName": "Apple Inc.",
                        "ticker": "AAPL"
                    },
                    ...
                ],
                "10-Q": [...],
                ...
            }
        """
        # Get CIK from ticker
        cik = self.get_cik_from_ticker(ticker)
        if not cik:
            raise ValueError(f"Could not find CIK for ticker: {ticker}")

        # Get all submissions
        submissions = self.get_company_submissions(cik)

        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=years * 365)

        # Extract company name
        company_name = submissions.get("name", "Unknown Company")

        # Process filings
        result = {filing_type: [] for filing_type in filing_types}

        recent_filings = submissions.get("filings", {}).get("recent", {})

        if not recent_filings:
            return result

        # Get arrays
        forms = recent_filings.get("form", [])
        filing_dates = recent_filings.get("filingDate", [])
        accession_numbers = recent_filings.get("accessionNumber", [])
        report_dates = recent_filings.get("reportDate", [])
        primary_documents = recent_filings.get("primaryDocument", [])
        file_numbers = recent_filings.get("fileNumber", [])

        # Process each filing
        for i in range(len(forms)):
            form = forms[i]
            filing_date = filing_dates[i]

            # Check if this filing type is requested
            if form not in filing_types:
                continue

            # Check date cutoff
            try:
                filing_dt = datetime.strptime(filing_date, "%Y-%m-%d")
                if filing_dt < cutoff_date:
                    continue
            except ValueError:
                continue

            # Check limit
            if limit_per_type and len(result[form]) >= limit_per_type:
                continue

            # Build URLs
            accession_no_dashes = accession_numbers[i].replace("-", "")
            documents_url = f"https://www.sec.gov/cgi-bin/viewer?action=view&cik={cik}&accession_number={accession_numbers[i]}&xbrl_type=v"

            primary_doc_url = None
            if i < len(primary_documents) and primary_documents[i]:
                primary_doc_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_no_dashes}/{primary_documents[i]}"

            # Create filing metadata
            filing_info = {
                "accessionNumber": accession_numbers[i],
                "filingDate": filing_date,
                "reportDate": report_dates[i] if i < len(report_dates) else None,
                "form": form,
                "fileNumber": file_numbers[i] if i < len(file_numbers) else None,
                "primaryDocument": primary_documents[i] if i < len(primary_documents) else None,
                "primaryDocUrl": primary_doc_url,
                "documentsUrl": documents_url,
                "companyName": company_name,
                "ticker": ticker.upper(),
                "cik": cik
            }

            result[form].append(filing_info)

        # Sort each filing type by date (newest first)
        for filing_type in result:
            result[filing_type].sort(key=lambda x: x["filingDate"], reverse=True)

        return result

    def get_filing_content(self, url: str) -> str:
        """
        Fetch the full text content of a filing.

        Args:
            url: URL to the filing document (primaryDocUrl from fetch_filings)

        Returns:
            Full text content of the filing
        """
        try:
            response = self._make_request(url)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to fetch filing content from {url}: {str(e)}")

    def clean_html(self, html_content: str) -> str:
        """
        Clean HTML by removing styling and excess markup while preserving structure.

        This method delegates to HTMLCleaner for backward compatibility.
        For direct access to cleaning functionality, use the html_cleaner module.

        Removes:
        - All <style> and <script> tags and their contents
        - All style, class, id, and other presentational attributes
        - Font, span, and other purely presentational tags (unwrap their contents)
        - Empty tags that don't contribute to structure
        - HTML comments

        Preserves:
        - Structural tags: h1-h6, p, div, section, table, tr, td, th, ul, ol, li, br, hr
        - Links: a tags (with href attribute only)
        - Document hierarchy and text content

        Args:
            html_content: Raw HTML content

        Returns:
            Cleaned HTML with minimal markup
        """
        return self._cleaner.clean(html_content)

    def get_filing_content_clean(self, url: str) -> str:
        """
        Fetch filing content and return cleaned HTML (structure preserved, styling removed).

        This returns HTML with structure intact but significantly reduced size:
        - Removes all CSS, JavaScript, and styling
        - Removes presentational attributes and tags
        - Preserves document structure (headings, paragraphs, tables, lists)

        Args:
            url: URL to the filing document

        Returns:
            Cleaned HTML content
        """
        html_content = self.get_filing_content(url)
        return self.clean_html(html_content)

    def get_filing_text(self, url: str) -> str:
        """
        Fetch filing content and extract plain text (strip HTML).

        Uses BeautifulSoup for robust HTML parsing and text extraction.

        Args:
            url: URL to the filing document

        Returns:
            Plain text content with HTML tags removed
        """
        html_content = self.get_filing_content(url)
        return self._cleaner.extract_text(html_content)
