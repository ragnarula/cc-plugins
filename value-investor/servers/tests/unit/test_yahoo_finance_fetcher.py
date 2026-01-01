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


@pytest.mark.unit
class TestSuccessfulDataRetrieval:
    """Test successful financial statement retrieval with mocked responses."""

    def test_valid_ticker_returns_correct_structure(self, fetcher, mock_ticker):
        """TEST-UNIT-VALID-TICKER: Mock successful response, verify JSON structure."""
        with patch('yahoo_finance_fetcher.yf.Ticker', return_value=mock_ticker):
            result = fetcher.get_financial_statements('AAPL')

        # Verify top-level structure
        assert 'error' not in result
        assert 'ticker' in result
        assert result['ticker'] == 'AAPL'
        assert 'currency' in result
        assert result['currency'] == 'USD'
        assert 'fiscal_year_end' in result
        assert 'retrieved_at' in result
        assert 'statements' in result

        # Verify statements structure
        statements = result['statements']
        assert 'income_statement' in statements
        assert 'balance_sheet' in statements
        assert 'cash_flow' in statements

        # Verify each statement has annual and quarterly sections
        assert 'annual' in statements['income_statement']
        assert 'quarterly' in statements['income_statement']
        assert 'annual' in statements['balance_sheet']
        assert 'quarterly' in statements['balance_sheet']
        assert 'annual' in statements['cash_flow']
        assert 'quarterly' in statements['cash_flow']

        # Verify annual data contains period_end field
        income_annual = statements['income_statement']['annual']
        assert len(income_annual) > 0
        assert 'period_end' in income_annual[0]
        assert 'Total Revenue' in income_annual[0]

    def test_date_transformation_to_iso8601(self, fetcher, mock_ticker):
        """TEST-UNIT-DATE-TRANSFORMATION: Verify ISO 8601 date format."""
        with patch('yahoo_finance_fetcher.yf.Ticker', return_value=mock_ticker):
            result = fetcher.get_financial_statements('AAPL')

        # Check annual income statement dates
        income_annual = result['statements']['income_statement']['annual']
        for period in income_annual:
            period_end = period['period_end']
            # Verify ISO 8601 format (YYYY-MM-DD)
            assert isinstance(period_end, str)
            assert len(period_end) == 10
            assert period_end[4] == '-'
            assert period_end[7] == '-'
            # Verify it's a valid date format
            datetime.strptime(period_end, '%Y-%m-%d')

        # Check quarterly data dates
        income_quarterly = result['statements']['income_statement']['quarterly']
        for period in income_quarterly:
            period_end = period['period_end']
            assert isinstance(period_end, str)
            datetime.strptime(period_end, '%Y-%m-%d')

    def test_currency_extraction_iso4217(self, fetcher, mock_ticker):
        """TEST-UNIT-CURRENCY-EXTRACTION: Verify ISO 4217 currency code."""
        with patch('yahoo_finance_fetcher.yf.Ticker', return_value=mock_ticker):
            result = fetcher.get_financial_statements('AAPL')

        # Verify currency is uppercase ISO 4217 code
        assert result['currency'] == 'USD'
        assert result['currency'].isupper()
        assert len(result['currency']) == 3

    def test_data_sorting_newest_first(self, fetcher, mock_ticker):
        """TEST-UNIT-DATA-SORTING: Verify newest-first ordering."""
        with patch('yahoo_finance_fetcher.yf.Ticker', return_value=mock_ticker):
            result = fetcher.get_financial_statements('AAPL')

        # Check annual income statement is sorted newest first
        income_annual = result['statements']['income_statement']['annual']
        assert len(income_annual) >= 2

        # Convert period_end strings to dates for comparison
        dates = [datetime.strptime(p['period_end'], '%Y-%m-%d') for p in income_annual]

        # Verify dates are in descending order (newest first)
        for i in range(len(dates) - 1):
            assert dates[i] >= dates[i + 1], f"Dates not sorted newest first: {dates}"

        # Check quarterly data is also sorted newest first
        income_quarterly = result['statements']['income_statement']['quarterly']
        if len(income_quarterly) >= 2:
            quarterly_dates = [datetime.strptime(p['period_end'], '%Y-%m-%d') for p in income_quarterly]
            for i in range(len(quarterly_dates) - 1):
                assert quarterly_dates[i] >= quarterly_dates[i + 1]
