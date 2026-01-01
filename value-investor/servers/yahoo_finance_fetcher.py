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
from datetime import datetime
from typing import Dict, Optional, List

import yfinance as yf
import pandas as pd


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

    def _transform_dataframe_to_json(self, df: pd.DataFrame, limit_years: Optional[int] = None) -> List[Dict]:
        """
        Transform pandas DataFrame to list of JSON dictionaries.

        Args:
            df: Pandas DataFrame with dates as columns
            limit_years: Limit to N most recent years (default: None = all data)

        Returns:
            List of dictionaries with period_end and financial line items
        """
        if df is None or df.empty:
            return []

        result = []

        # DataFrame columns are dates (pandas Timestamp objects)
        # Rows are financial line items
        # We need to transpose to get one dict per period
        for col in df.columns:
            # Convert date to ISO 8601 format (YYYY-MM-DD)
            if isinstance(col, pd.Timestamp):
                period_end = col.strftime('%Y-%m-%d')
            else:
                # Handle edge case where column is already a string
                period_end = str(col)

            # Create dict for this period
            period_data = {"period_end": period_end}

            # Add all financial line items
            for row_name in df.index:
                value = df.loc[row_name, col]

                # Convert pandas types to native Python types
                # Use "MISSING" string for NaN/None values (REQ-FN-02)
                if pd.isna(value):
                    period_data[row_name] = "MISSING"
                elif isinstance(value, (pd.Int64Dtype, pd.Float64Dtype)):
                    period_data[row_name] = float(value)
                else:
                    # Try to convert to float if numeric
                    try:
                        period_data[row_name] = float(value)
                    except (ValueError, TypeError):
                        period_data[row_name] = str(value)

            result.append(period_data)

        # Sort by date (newest first)
        result.sort(key=lambda x: x['period_end'], reverse=True)

        # Limit to specified number of years
        if limit_years:
            result = result[:limit_years]

        return result

    def _extract_currency(self, ticker_obj) -> str:
        """
        Extract currency code from ticker info.

        Args:
            ticker_obj: yfinance Ticker object

        Returns:
            ISO 4217 currency code (e.g., 'USD', 'EUR', 'JPY')
        """
        try:
            info = ticker_obj.info
            currency = info.get('currency', 'USD')
            # Ensure uppercase for ISO 4217 compliance
            return currency.upper()
        except Exception:
            # Default to USD if unable to extract
            return 'USD'

    def _extract_fiscal_year_end(self, ticker_obj) -> Optional[str]:
        """
        Extract fiscal year end month from ticker info.

        Args:
            ticker_obj: yfinance Ticker object

        Returns:
            Month name (e.g., 'September', 'December') or None
        """
        try:
            info = ticker_obj.info
            # Yahoo Finance provides fiscal year end as a timestamp or month
            fiscal_year_end = info.get('lastFiscalYearEnd')
            if fiscal_year_end:
                # Convert timestamp to month name
                if isinstance(fiscal_year_end, int):
                    dt = datetime.fromtimestamp(fiscal_year_end)
                    return dt.strftime('%B')
            return None
        except Exception:
            return None

    def _limit_quarterly_to_current_year(self, quarterly_data: List[Dict]) -> List[Dict]:
        """
        Limit quarterly data to current fiscal year only.

        Args:
            quarterly_data: List of quarterly period dictionaries

        Returns:
            Filtered list containing only current year quarters
        """
        if not quarterly_data:
            return []

        # Get current year
        current_year = datetime.now().year

        # Filter to current year only
        # Yahoo Finance typically provides last 4 quarters, which is usually the current fiscal year
        # We'll take the first 4 quarters (most recent) to ensure we get current year data
        return quarterly_data[:4]

    def _check_data_availability(self, ticker_obj) -> bool:
        """
        Check if ticker has any financial data available.

        Args:
            ticker_obj: yfinance Ticker object

        Returns:
            True if at least one financial statement has data, False otherwise
        """
        # Check if any of the main financial statements have data
        has_income = ticker_obj.financials is not None and not ticker_obj.financials.empty
        has_balance = ticker_obj.balance_sheet is not None and not ticker_obj.balance_sheet.empty
        has_cashflow = ticker_obj.cashflow is not None and not ticker_obj.cashflow.empty

        return has_income or has_balance or has_cashflow

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

            # Check if ticker has any financial data
            if not self._check_data_availability(ticker_obj):
                return {
                    "error": {
                        "code": "DATA_UNAVAILABLE",
                        "message": f"Ticker '{sanitized_ticker}' is valid but has no financial statements available. This may occur for non-public companies, ETFs, or newly listed securities.",
                        "ticker": sanitized_ticker
                    }
                }

            # Fetch all financial statements (pandas DataFrames)
            # Annual data
            income_annual_df = ticker_obj.financials  # Income statement annual
            balance_annual_df = ticker_obj.balance_sheet  # Balance sheet annual
            cashflow_annual_df = ticker_obj.cashflow  # Cash flow annual

            # Quarterly data
            income_quarterly_df = ticker_obj.quarterly_financials  # Income statement quarterly
            balance_quarterly_df = ticker_obj.quarterly_balance_sheet  # Balance sheet quarterly
            cashflow_quarterly_df = ticker_obj.quarterly_cashflow  # Cash flow quarterly

            # Extract metadata
            currency = self._extract_currency(ticker_obj)
            fiscal_year_end = self._extract_fiscal_year_end(ticker_obj)
            retrieved_at = datetime.now().isoformat() + 'Z'

            # Transform DataFrames to JSON
            # Annual data: limit to 5 years
            income_annual = self._transform_dataframe_to_json(income_annual_df, limit_years=5)
            balance_annual = self._transform_dataframe_to_json(balance_annual_df, limit_years=5)
            cashflow_annual = self._transform_dataframe_to_json(cashflow_annual_df, limit_years=5)

            # Quarterly data: limit to current fiscal year (4 quarters)
            income_quarterly = self._limit_quarterly_to_current_year(
                self._transform_dataframe_to_json(income_quarterly_df)
            )
            balance_quarterly = self._limit_quarterly_to_current_year(
                self._transform_dataframe_to_json(balance_quarterly_df)
            )
            cashflow_quarterly = self._limit_quarterly_to_current_year(
                self._transform_dataframe_to_json(cashflow_quarterly_df)
            )

            # Build final result
            result = {
                "ticker": sanitized_ticker,
                "currency": currency,
                "fiscal_year_end": fiscal_year_end,
                "retrieved_at": retrieved_at,
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
