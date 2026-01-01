"""
Yahoo Finance Financial Statements Fetcher

Fetches financial statement data from Yahoo Finance using the yfinance library.
Provides structured access to income statements, balance sheets, and cash flow statements
with historical annual and quarterly data.

Key Features:
- Fetch all three major financial statements (income, balance sheet, cash flow)
- Retrieve up to 5 years of annual historical data
- Retrieve current fiscal year quarterly data
- 30-second timeout on all HTTP requests
- Consistent JSON schema with MISSING markers for unavailable data
- Clear error codes for different failure scenarios

Yahoo Finance Data Access:
https://github.com/ranaroussi/yfinance
"""

import re
from typing import Dict, Optional

import yfinance as yf


class YahooFinanceFetcher:
    """Fetches financial statement data from Yahoo Finance."""

    def __init__(self, timeout: int = 30):
        """
        Initialize the Yahoo Finance fetcher.

        Args:
            timeout: HTTP request timeout in seconds (default: 30)
        """
        self.timeout = timeout

    def _sanitize_ticker(self, ticker: str) -> str:
        """
        Sanitize ticker symbol to prevent injection attacks.

        Args:
            ticker: Raw ticker symbol input

        Returns:
            Sanitized ticker symbol (uppercase, alphanumeric + hyphen/period only)

        Raises:
            ValueError: If ticker contains invalid characters
        """
        # Remove whitespace
        ticker = ticker.strip().upper()

        # Validate: alphanumeric, hyphen, and period only
        if not re.match(r'^[A-Z0-9.-]+$', ticker):
            raise ValueError(
                f"Invalid ticker format: '{ticker}'. "
                "Ticker must contain only letters, numbers, hyphens, and periods."
            )

        return ticker

    def _fetch_ticker_data(self, ticker: str):
        """
        Fetch ticker object from yfinance with timeout.

        Args:
            ticker: Sanitized ticker symbol

        Returns:
            yfinance Ticker object

        Raises:
            TimeoutError: If request exceeds timeout
            Exception: For other API errors
        """
        # Configure yfinance to use our timeout
        # yfinance uses requests internally, and we can configure timeout via session
        import requests

        # Create a session with timeout
        session = requests.Session()
        session.request = lambda *args, **kwargs: requests.Session.request(
            session, *args, **{**kwargs, 'timeout': self.timeout}
        )

        # Create ticker with custom session
        ticker_obj = yf.Ticker(ticker, session=session)

        return ticker_obj

    def get_financial_statements(self, ticker: str) -> Dict:
        """
        Fetch all three major financial statements for a given ticker.

        Retrieves:
        - Income statement (annual and quarterly)
        - Balance sheet (annual and quarterly)
        - Cash flow statement (annual and quarterly)

        Annual data: up to 5 years of historical data
        Quarterly data: current fiscal year only

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')

        Returns:
            Dictionary containing financial statements with consistent JSON schema.
            Missing data is marked with string "MISSING".

            Success response format:
            {
                "ticker": "AAPL",
                "currency": "USD",
                "fiscal_year_end": "September",
                "retrieved_at": "2025-12-31T15:30:00Z",
                "statements": {
                    "income_statement": {
                        "annual": [...],
                        "quarterly": [...]
                    },
                    "balance_sheet": {
                        "annual": [...],
                        "quarterly": [...]
                    },
                    "cash_flow": {
                        "annual": [...],
                        "quarterly": [...]
                    }
                }
            }

            Error response format:
            {
                "error": {
                    "code": "ERROR_CODE",
                    "message": "Human-readable error message",
                    "ticker": "TICKER"
                }
            }

            Error codes:
            - INVALID_TICKER_FORMAT: Ticker fails sanitization regex
            - TICKER_NOT_FOUND: Ticker not found in Yahoo Finance
            - DATA_UNAVAILABLE: Ticker valid but no financial statements
            - API_TIMEOUT: Request timeout after 30s
            - API_ERROR: Unexpected yfinance error
        """
        try:
            # Sanitize ticker input
            sanitized_ticker = self._sanitize_ticker(ticker)

            # Fetch ticker data with timeout
            ticker_obj = self._fetch_ticker_data(sanitized_ticker)

            # Fetch all financial statements
            # Annual data
            income_annual = ticker_obj.financials  # Income statement annual
            balance_annual = ticker_obj.balance_sheet  # Balance sheet annual
            cashflow_annual = ticker_obj.cashflow  # Cash flow annual

            # Quarterly data
            income_quarterly = ticker_obj.quarterly_financials  # Income statement quarterly
            balance_quarterly = ticker_obj.quarterly_balance_sheet  # Balance sheet quarterly
            cashflow_quarterly = ticker_obj.quarterly_cashflow  # Cash flow quarterly

            # This is a placeholder - data transformation will be implemented in Task 2.3
            # For now, just return the raw data to verify fetching works
            result = {
                "ticker": sanitized_ticker,
                "statements": {
                    "income_statement": {
                        "annual": income_annual,
                        "quarterly": income_quarterly
                    },
                    "balance_sheet": {
                        "annual": balance_annual,
                        "quarterly": balance_quarterly
                    },
                    "cash_flow": {
                        "annual": cashflow_annual,
                        "quarterly": cashflow_quarterly
                    }
                }
            }

            return result

        except ValueError as e:
            # Ticker sanitization failed
            return {
                "error": {
                    "code": "INVALID_TICKER_FORMAT",
                    "message": str(e),
                    "ticker": ticker
                }
            }
        except TimeoutError:
            return {
                "error": {
                    "code": "API_TIMEOUT",
                    "message": f"Request timeout after {self.timeout} seconds",
                    "ticker": ticker
                }
            }
        except Exception as e:
            # Generic error handling - will be refined in Task 2.5
            return {
                "error": {
                    "code": "API_ERROR",
                    "message": str(e),
                    "ticker": ticker
                }
            }
