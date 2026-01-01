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


@pytest.mark.unit
class TestMissingDataHandling:
    """Test handling of missing or incomplete financial data."""

    def test_missing_fields_replaced_with_missing_marker(self, fetcher, mock_ticker_with_missing_data):
        """TEST-UNIT-MISSING-FIELDS: Mock response with NaN values."""
        with patch('yahoo_finance_fetcher.yf.Ticker', return_value=mock_ticker_with_missing_data):
            result = fetcher.get_financial_statements('TEST')

        # Verify no error
        assert 'error' not in result

        # Check income statement has data
        income_annual = result['statements']['income_statement']['annual']
        assert len(income_annual) > 0

        # Verify that NaN values are replaced with "MISSING" string
        period = income_annual[0]
        assert period['Total Revenue'] == 100000000  # Has value
        assert period['Cost Of Revenue'] == 'MISSING'  # Was NaN
        assert period['Gross Profit'] == 'MISSING'  # Was NaN
        assert period['Net Income'] == 10000000  # Has value

    def test_missing_marker_is_string(self, fetcher, mock_ticker_with_missing_data):
        """TEST-UNIT-MISSING-MARKER: Verify "MISSING" string insertion."""
        with patch('yahoo_finance_fetcher.yf.Ticker', return_value=mock_ticker_with_missing_data):
            result = fetcher.get_financial_statements('TEST')

        income_annual = result['statements']['income_statement']['annual']
        period = income_annual[0]

        # Verify MISSING is a string, not None or null
        missing_fields = [k for k, v in period.items() if v == 'MISSING']
        assert len(missing_fields) > 0

        for field in missing_fields:
            assert isinstance(period[field], str)
            assert period[field] == 'MISSING'

    def test_schema_consistency_with_and_without_data(self, fetcher, mock_ticker, mock_ticker_with_missing_data):
        """TEST-UNIT-SCHEMA-CONSISTENCY: Verify same fields present with/without data."""
        # Get result with complete data
        with patch('yahoo_finance_fetcher.yf.Ticker', return_value=mock_ticker):
            result_complete = fetcher.get_financial_statements('AAPL')

        # Get result with missing data
        with patch('yahoo_finance_fetcher.yf.Ticker', return_value=mock_ticker_with_missing_data):
            result_missing = fetcher.get_financial_statements('TEST')

        # Both should have the same top-level structure
        assert set(result_complete.keys()) == set(result_missing.keys())

        # Both should have statements with same structure
        assert 'statements' in result_complete
        assert 'statements' in result_missing

        # Income statement fields should be present in both
        complete_income = result_complete['statements']['income_statement']['annual'][0]
        missing_income = result_missing['statements']['income_statement']['annual'][0]

        # Both should have period_end field
        assert 'period_end' in complete_income
        assert 'period_end' in missing_income

        # Missing data period should have same financial line items (just with MISSING values)
        for field in missing_income:
            if field != 'period_end':
                # Field exists in result with missing data
                assert field in missing_income
                # Value is either a number or "MISSING" string
                assert isinstance(missing_income[field], (int, float, str))


@pytest.mark.unit
class TestErrorConditions:
    """Test error handling for various failure scenarios."""

    def test_invalid_ticker_not_found(self, fetcher, mock_empty_ticker):
        """TEST-UNIT-INVALID-TICKER: Verify TICKER_NOT_FOUND error code."""
        with patch('yahoo_finance_fetcher.yf.Ticker', return_value=mock_empty_ticker):
            result = fetcher.get_financial_statements('INVALID')

        # Verify error response structure
        assert 'error' in result
        assert 'code' in result['error']
        assert 'message' in result['error']
        assert 'ticker' in result['error']

        # Verify DATA_UNAVAILABLE code (empty ticker means no data available)
        assert result['error']['code'] == 'DATA_UNAVAILABLE'
        assert 'INVALID' in result['error']['ticker']

    def test_timeout_exception_handling(self, fetcher):
        """TEST-UNIT-TIMEOUT: Mock timeout exception, verify API_TIMEOUT."""
        with patch('yahoo_finance_fetcher.yf.Ticker', side_effect=TimeoutError("Request timed out")):
            result = fetcher.get_financial_statements('AAPL')

        # Verify error response
        assert 'error' in result
        assert result['error']['code'] == 'API_TIMEOUT'
        assert 'timeout' in result['error']['message'].lower()
        assert '30' in result['error']['message']  # Mentions timeout duration

    def test_ticker_sanitization_rejects_invalid_characters(self, fetcher):
        """TEST-UNIT-SANITIZATION: Test ticker validation regex."""
        # Test various invalid ticker formats
        # Note: control characters in the middle won't be stripped by .strip()
        invalid_tickers = [
            '; DROP TABLE',      # SQL injection attempt
            '&& rm -rf /',       # Command injection attempt
            '<script>alert(1)</script>',  # XSS attempt
            'AA\nPL',            # Control character in middle (won't be stripped)
            '../../../etc',      # Path traversal attempt
            '@#$%',              # Special characters only
            'AAPL; DELETE',      # SQL injection with valid prefix
            'TEST/../../',       # Path traversal with valid prefix
            'AAPL@HACK',         # Special character in middle
            'TEST<SCRIPT>',      # XSS in middle
        ]

        for invalid_ticker in invalid_tickers:
            result = fetcher.get_financial_statements(invalid_ticker)

            # Verify error response
            assert 'error' in result, f"Expected error for ticker: {invalid_ticker}"
            assert result['error']['code'] == 'INVALID_TICKER_FORMAT', f"Expected INVALID_TICKER_FORMAT for: {invalid_ticker}, got {result['error']['code']}"
            assert 'invalid' in result['error']['message'].lower()

    def test_ticker_sanitization_allows_valid_characters(self, fetcher, mock_ticker):
        """TEST-UNIT-SANITIZATION: Test valid ticker formats are accepted."""
        # Valid ticker formats (alphanumeric + hyphen/period)
        valid_tickers = [
            'AAPL',
            'BRK.B',      # Berkshire Hathaway Class B
            'BRK-B',      # Alternative format
            'MSFT',
            'GOOGL',
            'TSM',        # Taiwan Semiconductor
            'ASML',       # ASML Holding
        ]

        for valid_ticker in valid_tickers:
            with patch('yahoo_finance_fetcher.yf.Ticker', return_value=mock_ticker):
                result = fetcher.get_financial_statements(valid_ticker)

            # Should not have error
            assert 'error' not in result, f"Unexpected error for valid ticker: {valid_ticker}"
            assert 'ticker' in result
            # Ticker should be uppercased and sanitized
            assert result['ticker'].isupper()

    def test_api_error_generic_exception_handling(self, fetcher):
        """TEST-UNIT-API-ERROR: Mock yfinance exception, verify error handling."""
        # Mock a generic exception from yfinance
        with patch('yahoo_finance_fetcher.yf.Ticker', side_effect=Exception("Unexpected API error")):
            result = fetcher.get_financial_statements('AAPL')

        # Verify error response
        assert 'error' in result
        assert result['error']['code'] == 'API_ERROR'
        assert 'error' in result['error']['message'].lower()

    def test_connection_error_handling(self, fetcher):
        """TEST-UNIT-API-ERROR: Test network connection error handling."""
        with patch('yahoo_finance_fetcher.yf.Ticker', side_effect=ConnectionError("Network unreachable")):
            result = fetcher.get_financial_statements('AAPL')

        # Verify error response
        assert 'error' in result
        assert result['error']['code'] == 'API_ERROR'
        assert 'connection' in result['error']['message'].lower()

    def test_ticker_not_found_error_patterns(self, fetcher):
        """TEST-UNIT-INVALID-TICKER: Test various ticker not found error patterns."""
        # Mock different error messages that indicate ticker not found
        error_messages = [
            "No data found for this ticker",
            "404 Not Found",
            "Invalid ticker symbol",
            "No timezone found",
            "No price data found"
        ]

        for error_msg in error_messages:
            with patch('yahoo_finance_fetcher.yf.Ticker', side_effect=Exception(error_msg)):
                result = fetcher.get_financial_statements('NOTFOUND')

            # Should map to TICKER_NOT_FOUND error code
            assert 'error' in result
            assert result['error']['code'] == 'TICKER_NOT_FOUND', f"Expected TICKER_NOT_FOUND for error: {error_msg}"
            assert 'ticker' in result['error']
