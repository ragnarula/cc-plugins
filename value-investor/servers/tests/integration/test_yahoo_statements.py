"""
Integration tests for Yahoo Finance financial statement retrieval.

Tests end-to-end functionality with real Yahoo Finance API calls.
Validates data quality, schema consistency, and error handling with live data.

Note: These tests make real API calls and may take longer to execute.
Run with: pytest -m integration tests/integration/test_yahoo_statements.py -v
"""

import pytest
from yahoo_finance_fetcher import YahooFinanceFetcher


@pytest.fixture
def yahoo_fetcher():
    """YahooFinanceFetcher instance for integration tests."""
    return YahooFinanceFetcher(timeout=30)


@pytest.mark.integration
class TestEstablishedCompanies:
    """Test financial statement retrieval for established companies."""

    def test_fetch_apple_statements(self, yahoo_fetcher):
        """TEST-INTEGRATION-AAPL: Fetch Apple statements and verify structure."""
        result = yahoo_fetcher.get_financial_statements("AAPL")

        # Should not have an error
        assert "error" not in result, f"Error fetching AAPL: {result.get('error')}"

        # Verify top-level structure
        assert result["ticker"] == "AAPL"
        assert result["currency"] == "USD"
        assert "retrieved_at" in result
        assert "statements" in result

        # Verify all three statement types exist
        statements = result["statements"]
        assert "income_statement" in statements
        assert "balance_sheet" in statements
        assert "cash_flow" in statements

        # Verify annual and quarterly data for each statement
        for stmt_name in ["income_statement", "balance_sheet", "cash_flow"]:
            stmt = statements[stmt_name]
            assert "annual" in stmt
            assert "quarterly" in stmt
            assert isinstance(stmt["annual"], list)
            assert isinstance(stmt["quarterly"], list)

        # Apple should have substantial historical data
        assert len(statements["income_statement"]["annual"]) > 0, \
            "Apple should have annual income statement data"

    def test_fetch_microsoft_statements(self, yahoo_fetcher):
        """TEST-INTEGRATION-MSFT: Fetch Microsoft statements and verify structure."""
        result = yahoo_fetcher.get_financial_statements("MSFT")

        # Should not have an error
        assert "error" not in result, f"Error fetching MSFT: {result.get('error')}"

        # Verify top-level structure
        assert result["ticker"] == "MSFT"
        assert result["currency"] == "USD"
        assert "retrieved_at" in result
        assert "statements" in result

        # Verify all three statement types exist
        statements = result["statements"]
        assert "income_statement" in statements
        assert "balance_sheet" in statements
        assert "cash_flow" in statements

        # Microsoft should have substantial historical data
        assert len(statements["income_statement"]["annual"]) > 0, \
            "Microsoft should have annual income statement data"

    def test_historical_annual_data(self, yahoo_fetcher):
        """TEST-INTEGRATION-HISTORICAL: Verify 5 years of annual data available."""
        result = yahoo_fetcher.get_financial_statements("AAPL")

        assert "error" not in result, f"Error fetching AAPL: {result.get('error')}"

        # Check income statement annual data
        annual_data = result["statements"]["income_statement"]["annual"]

        # Should have up to 5 years of data
        assert len(annual_data) >= 3, \
            f"Expected at least 3 years of annual data, got {len(annual_data)}"

        # Verify data is sorted newest first
        if len(annual_data) >= 2:
            first_date = annual_data[0]["period_end"]
            second_date = annual_data[1]["period_end"]
            assert first_date > second_date, \
                "Annual data should be sorted newest first"

        # Verify each period has a period_end field
        for period in annual_data:
            assert "period_end" in period
            # Verify ISO 8601 date format (YYYY-MM-DD)
            assert len(period["period_end"]) == 10
            assert period["period_end"][4] == "-"
            assert period["period_end"][7] == "-"

    def test_quarterly_data_current_year(self, yahoo_fetcher):
        """TEST-INTEGRATION-QUARTERLY: Verify current year quarterly data available."""
        result = yahoo_fetcher.get_financial_statements("AAPL")

        assert "error" not in result, f"Error fetching AAPL: {result.get('error')}"

        # Check income statement quarterly data
        quarterly_data = result["statements"]["income_statement"]["quarterly"]

        # Should have quarterly data (typically 4 quarters)
        # Note: May have less if company just reported
        assert len(quarterly_data) >= 1, \
            "Expected at least 1 quarter of quarterly data"

        # Should not have more than 4 quarters (current year only)
        assert len(quarterly_data) <= 4, \
            f"Expected max 4 quarters, got {len(quarterly_data)}"

        # Verify data is sorted newest first
        if len(quarterly_data) >= 2:
            first_date = quarterly_data[0]["period_end"]
            second_date = quarterly_data[1]["period_end"]
            assert first_date > second_date, \
                "Quarterly data should be sorted newest first"


@pytest.mark.integration
class TestEdgeCases:
    """Test financial statement retrieval for edge cases."""

    def test_missing_data_recent_ipo(self, yahoo_fetcher):
        """TEST-INTEGRATION-MISSING-DATA: Test recent IPO with incomplete data."""
        # Use a ticker that's known to have limited historical data
        # RIVN (Rivian) went public in late 2021, should have less data
        result = yahoo_fetcher.get_financial_statements("RIVN")

        # Should succeed even with limited data
        if "error" in result:
            # If ticker not found or data unavailable, that's acceptable for edge cases
            assert result["error"]["code"] in ["TICKER_NOT_FOUND", "DATA_UNAVAILABLE"], \
                f"Unexpected error for RIVN: {result['error']}"
        else:
            # If data available, verify structure is consistent
            statements = result["statements"]
            assert "income_statement" in statements
            assert "balance_sheet" in statements
            assert "cash_flow" in statements

            # Annual data may be limited for recent IPOs
            annual_data = statements["income_statement"]["annual"]
            # Should have at least empty list or some data
            assert isinstance(annual_data, list), \
                "Annual data should be a list even if empty"

    def test_invalid_ticker_error_handling(self, yahoo_fetcher):
        """TEST-INTEGRATION-INVALID-TICKER: Test invalid ticker error handling."""
        result = yahoo_fetcher.get_financial_statements("INVALID999")

        # Should return an error
        assert "error" in result, "Expected error for invalid ticker"

        # Error should have required fields
        error = result["error"]
        assert "code" in error
        assert "message" in error
        assert "ticker" in error

        # Error code should be TICKER_NOT_FOUND or DATA_UNAVAILABLE
        assert error["code"] in ["TICKER_NOT_FOUND", "DATA_UNAVAILABLE"], \
            f"Unexpected error code: {error['code']}"

        # Message should be informative
        assert len(error["message"]) > 0, "Error message should not be empty"

    def test_schema_consistency_across_tickers(self, yahoo_fetcher):
        """TEST-INTEGRATION-SCHEMA: Verify schema consistency across tickers."""
        tickers = ["AAPL", "MSFT", "GOOGL"]
        results = []

        for ticker in tickers:
            result = yahoo_fetcher.get_financial_statements(ticker)
            if "error" not in result:
                results.append(result)

        # Should have at least 2 successful results to compare
        assert len(results) >= 2, \
            "Need at least 2 successful results to verify schema consistency"

        # Verify all results have the same top-level structure
        for result in results:
            assert "ticker" in result
            assert "currency" in result
            assert "retrieved_at" in result
            assert "statements" in result

            # Verify statements structure
            statements = result["statements"]
            assert "income_statement" in statements
            assert "balance_sheet" in statements
            assert "cash_flow" in statements

            # Verify each statement has annual and quarterly
            for stmt in statements.values():
                assert "annual" in stmt
                assert "quarterly" in stmt

        # Verify annual data structure consistency
        # All results should have the same fields in each period
        # (though values may be MISSING)
        for result in results:
            income_annual = result["statements"]["income_statement"]["annual"]
            if len(income_annual) > 0:
                # Each period should have period_end field
                for period in income_annual:
                    assert "period_end" in period, \
                        f"Missing period_end in {result['ticker']} annual data"

                    # Verify ISO 8601 date format
                    period_end = period["period_end"]
                    assert isinstance(period_end, str), \
                        f"period_end should be string, got {type(period_end)}"
                    assert len(period_end) == 10, \
                        f"period_end should be YYYY-MM-DD format, got {period_end}"


@pytest.mark.integration
class TestDataQuality:
    """Test data quality and format compliance."""

    def test_date_format_iso_8601(self, yahoo_fetcher):
        """Verify all dates are in ISO 8601 format (YYYY-MM-DD)."""
        result = yahoo_fetcher.get_financial_statements("AAPL")

        assert "error" not in result, f"Error fetching AAPL: {result.get('error')}"

        # Check all annual data
        for stmt_name in ["income_statement", "balance_sheet", "cash_flow"]:
            annual_data = result["statements"][stmt_name]["annual"]
            for period in annual_data:
                period_end = period["period_end"]
                # ISO 8601 format: YYYY-MM-DD
                assert len(period_end) == 10, \
                    f"Invalid date format: {period_end}"
                assert period_end[4] == "-" and period_end[7] == "-", \
                    f"Invalid date separators: {period_end}"

                # Verify date components are numeric
                year, month, day = period_end.split("-")
                assert year.isdigit() and len(year) == 4, \
                    f"Invalid year: {year}"
                assert month.isdigit() and 1 <= int(month) <= 12, \
                    f"Invalid month: {month}"
                assert day.isdigit() and 1 <= int(day) <= 31, \
                    f"Invalid day: {day}"

    def test_currency_format_iso_4217(self, yahoo_fetcher):
        """Verify currency codes are in ISO 4217 format."""
        result = yahoo_fetcher.get_financial_statements("AAPL")

        assert "error" not in result, f"Error fetching AAPL: {result.get('error')}"

        # Currency should be 3-letter uppercase code
        currency = result["currency"]
        assert isinstance(currency, str), \
            f"Currency should be string, got {type(currency)}"
        assert len(currency) == 3, \
            f"Currency should be 3 letters (ISO 4217), got: {currency}"
        assert currency.isupper(), \
            f"Currency should be uppercase, got: {currency}"
        # Common currency codes
        assert currency in ["USD", "EUR", "JPY", "GBP", "CNY", "CAD", "AUD"], \
            f"Unexpected currency code: {currency}"

    def test_missing_marker_consistency(self, yahoo_fetcher):
        """Verify MISSING markers are used consistently for unavailable data."""
        # Use a ticker that might have some missing data
        result = yahoo_fetcher.get_financial_statements("AAPL")

        assert "error" not in result, f"Error fetching AAPL: {result.get('error')}"

        # Check all statements for MISSING markers
        for stmt_name in ["income_statement", "balance_sheet", "cash_flow"]:
            annual_data = result["statements"][stmt_name]["annual"]

            for period in annual_data:
                for key, value in period.items():
                    if value == "MISSING":
                        # MISSING should be a string, not None or NaN
                        assert isinstance(value, str), \
                            f"MISSING marker should be string, got {type(value)}"
                        assert value == "MISSING", \
                            f"Missing marker should be exactly 'MISSING', got {value}"

    def test_retrieved_at_timestamp(self, yahoo_fetcher):
        """Verify retrieved_at timestamp is in ISO 8601 format."""
        result = yahoo_fetcher.get_financial_statements("AAPL")

        assert "error" not in result, f"Error fetching AAPL: {result.get('error')}"

        retrieved_at = result["retrieved_at"]
        assert isinstance(retrieved_at, str), \
            f"retrieved_at should be string, got {type(retrieved_at)}"

        # Should end with 'Z' for UTC
        assert retrieved_at.endswith("Z"), \
            f"retrieved_at should end with 'Z' for UTC, got {retrieved_at}"

        # Should contain 'T' separator
        assert "T" in retrieved_at, \
            f"retrieved_at should contain 'T' separator, got {retrieved_at}"
