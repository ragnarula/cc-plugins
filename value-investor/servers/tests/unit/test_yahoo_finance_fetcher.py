"""
Unit tests for YahooFinanceFetcher module.

Tests financial statement fetching functionality with mocked yfinance responses.
Fast tests with no external API calls.
"""

import pytest
from unittest.mock import Mock, patch
import pandas as pd
from datetime import datetime

from yahoo_finance_fetcher import YahooFinanceFetcher


@pytest.fixture
def fetcher():
    """YahooFinanceFetcher instance for tests."""
    return YahooFinanceFetcher(timeout=30)


@pytest.fixture
def mock_ticker():
    """Mock yfinance.Ticker object with sample financial data."""
    ticker = Mock()

    # Mock info dict with currency and fiscal year end
    ticker.info = {
        'currency': 'USD',
        'lastFiscalYearEnd': 1696118400  # 2024-09-30 timestamp
    }

    # Mock income statement annual data (pandas DataFrame)
    # DataFrame has dates as columns, financial line items as rows
    income_annual_data = {
        pd.Timestamp('2024-09-30'): {
            'Total Revenue': 385706000000,
            'Cost Of Revenue': 210352000000,
            'Gross Profit': 175354000000,
            'Operating Expense': 56055000000,
            'Operating Income': 119299000000,
            'Net Income': 93736000000
        },
        pd.Timestamp('2023-09-30'): {
            'Total Revenue': 383285000000,
            'Cost Of Revenue': 214137000000,
            'Gross Profit': 169148000000,
            'Operating Expense': 51345000000,
            'Operating Income': 117803000000,
            'Net Income': 96995000000
        },
        pd.Timestamp('2022-09-24'): {
            'Total Revenue': 394328000000,
            'Cost Of Revenue': 223546000000,
            'Gross Profit': 170782000000,
            'Operating Expense': 51226000000,
            'Operating Income': 119556000000,
            'Net Income': 99803000000
        }
    }
    ticker.financials = pd.DataFrame(income_annual_data)

    # Mock balance sheet annual data
    balance_annual_data = {
        pd.Timestamp('2024-09-30'): {
            'Total Assets': 365725000000,
            'Total Liabilities Net Minority Interest': 279414000000,
            'Stockholders Equity': 86311000000
        },
        pd.Timestamp('2023-09-30'): {
            'Total Assets': 352755000000,
            'Total Liabilities Net Minority Interest': 290437000000,
            'Stockholders Equity': 62318000000
        }
    }
    ticker.balance_sheet = pd.DataFrame(balance_annual_data)

    # Mock cash flow annual data
    cashflow_annual_data = {
        pd.Timestamp('2024-09-30'): {
            'Operating Cash Flow': 118254000000,
            'Investing Cash Flow': -9542000000,
            'Financing Cash Flow': -103184000000
        },
        pd.Timestamp('2023-09-30'): {
            'Operating Cash Flow': 110543000000,
            'Investing Cash Flow': -3705000000,
            'Financing Cash Flow': -106905000000
        }
    }
    ticker.cashflow = pd.DataFrame(cashflow_annual_data)

    # Mock quarterly data (similar structure)
    income_quarterly_data = {
        pd.Timestamp('2024-09-30'): {
            'Total Revenue': 94930000000,
            'Net Income': 22956000000
        },
        pd.Timestamp('2024-06-30'): {
            'Total Revenue': 85778000000,
            'Net Income': 21448000000
        },
        pd.Timestamp('2024-03-31'): {
            'Total Revenue': 90753000000,
            'Net Income': 23636000000
        },
        pd.Timestamp('2023-12-31'): {
            'Total Revenue': 119575000000,
            'Net Income': 33916000000
        }
    }
    ticker.quarterly_financials = pd.DataFrame(income_quarterly_data)
    ticker.quarterly_balance_sheet = pd.DataFrame({})  # Empty for simplicity
    ticker.quarterly_cashflow = pd.DataFrame({})  # Empty for simplicity

    return ticker


@pytest.fixture
def mock_ticker_with_missing_data():
    """Mock yfinance.Ticker object with NaN values for missing data."""
    ticker = Mock()

    ticker.info = {
        'currency': 'USD',
        'lastFiscalYearEnd': None
    }

    # Income statement with missing values (NaN)
    income_data = {
        pd.Timestamp('2024-09-30'): {
            'Total Revenue': 100000000,
            'Cost Of Revenue': pd.NA,  # Missing value
            'Gross Profit': pd.NA,  # Missing value
            'Net Income': 10000000
        }
    }
    ticker.financials = pd.DataFrame(income_data)
    ticker.balance_sheet = pd.DataFrame({})
    ticker.cashflow = pd.DataFrame({})
    ticker.quarterly_financials = pd.DataFrame({})
    ticker.quarterly_balance_sheet = pd.DataFrame({})
    ticker.quarterly_cashflow = pd.DataFrame({})

    return ticker


@pytest.fixture
def mock_empty_ticker():
    """Mock yfinance.Ticker object with no financial data."""
    ticker = Mock()

    ticker.info = {'currency': 'USD'}
    ticker.financials = pd.DataFrame({})
    ticker.balance_sheet = pd.DataFrame({})
    ticker.cashflow = pd.DataFrame({})
    ticker.quarterly_financials = pd.DataFrame({})
    ticker.quarterly_balance_sheet = pd.DataFrame({})
    ticker.quarterly_cashflow = pd.DataFrame({})

    return ticker
