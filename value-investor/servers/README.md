# Financial Data MCP Server Setup

This directory contains the MCP (Model Context Protocol) server for fetching financial data from free APIs.

## Overview

The value-investor plugin uses MCP servers to access:
- SEC EDGAR filings (10-K, 10-Q, 8-K, DEF 14A, 13F, and other filing types)
- Yahoo Finance financial statements (income statement, balance sheet, cash flow statement)

## Data Sources

### SEC EDGAR API
- **URL**: https://www.sec.gov/edgar/sec-api-documentation
- **Authentication**: None required (rate limited)
- **Data**: Official SEC filings (10-K, 10-Q, 8-K, DEF 14A, 13F, etc.)
- **Rate Limit**: 10 requests/second

### Yahoo Finance API
- **Library**: yfinance Python library (https://github.com/ranaroussi/yfinance)
- **Authentication**: None required (free data access)
- **Data**: Financial statements (income statement, balance sheet, cash flow statement)
- **Historical Data**: Up to 5 years annual data + current year quarterly data
- **Rate Limit**: No explicit limit (handled internally by yfinance)

## Installation

The MCP server uses `uv` for dependency management - no manual installation needed. Dependencies are automatically managed when the server starts.

## MCP Server Implementation

The MCP server provides these tools:

### Available Tools

**1. `fetch_sec_filings`**
- Fetches SEC filings for a company with up to 10 years of historical data
- Parameters:
  - `ticker` (required): Stock ticker symbol (e.g., "AAPL", "MSFT")
  - `filing_types` (optional): List of filing types, defaults to ["10-K", "10-Q"]
  - `years` (optional): Number of years of history (1-10, default: 10)
  - `limit_per_type` (optional): Maximum filings per type
- Returns: Metadata and URLs for all matching filings

**2. `get_filing_content`**
- Retrieves the full text content of a specific SEC filing
- Parameters:
  - `url` (required): URL to the filing document (from fetch_sec_filings result)
  - `extract_text` (optional): Strip HTML and return plain text (default: false)
  - `clean_html` (optional): Return cleaned HTML with styling removed (default: false)
- Returns: Filing content with metadata

**3. `list_filing_types`**
- Lists all available SEC filing types with descriptions for value investing
- Parameters: None
- Returns: Comprehensive information about each filing type including use cases and importance

### Yahoo Finance MCP Server

The Yahoo Finance MCP server provides quantitative financial data to complement the qualitative narrative data from SEC EDGAR filings.

**Tool: `get_financial_statements`**
- Fetches all three major financial statements for value investing analysis
- Parameters:
  - `ticker` (required): Stock ticker symbol (e.g., "AAPL", "MSFT")
- Returns: Complete financial statement data with consistent JSON schema

**Response Structure:**
```json
{
  "ticker": "AAPL",
  "currency": "USD",
  "fiscal_year_end": "September",
  "retrieved_at": "2025-12-31T15:30:00Z",
  "statements": {
    "income_statement": {
      "annual": [/* up to 5 years */],
      "quarterly": [/* current fiscal year */]
    },
    "balance_sheet": {
      "annual": [/* up to 5 years */],
      "quarterly": [/* current fiscal year */]
    },
    "cash_flow": {
      "annual": [/* up to 5 years */],
      "quarterly": [/* current fiscal year */]
    }
  }
}
```

**Data Features:**
- **ISO 8601 Dates**: All period dates in YYYY-MM-DD format
- **ISO 4217 Currency**: Currency codes (USD, EUR, JPY, etc.)
- **Missing Data Handling**: Fields with unavailable data marked as "MISSING" string (not null)
- **Schema Consistency**: Same fields present regardless of data availability
- **30-Second Timeout**: All requests timeout after 30 seconds
- **Input Sanitization**: Ticker validation prevents injection attacks

**Error Handling:**

The tool returns clear error codes for different failure scenarios:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "ticker": "TICKER"
  }
}
```

**Error Codes:**
- `INVALID_TICKER_FORMAT`: Ticker contains invalid characters (only alphanumeric, hyphens, periods allowed)
- `TICKER_NOT_FOUND`: Ticker symbol not found in Yahoo Finance database
- `DATA_UNAVAILABLE`: Ticker exists but has no financial statement data (e.g., ETFs, non-public companies)
- `API_TIMEOUT`: Request exceeded 30-second timeout
- `API_ERROR`: Unexpected error from Yahoo Finance API

**Usage Examples:**

```python
# Basic usage - fetch Apple's financial statements
result = get_financial_statements(ticker="AAPL")

# Access income statement data
annual_income = result["statements"]["income_statement"]["annual"]
latest_year = annual_income[0]  # Most recent year
revenue = latest_year["Total Revenue"]
net_income = latest_year["Net Income"]

# Access balance sheet data
annual_balance = result["statements"]["balance_sheet"]["annual"]
latest_balance = annual_balance[0]
total_assets = latest_balance["Total Assets"]
total_liabilities = latest_balance["Total Liabilities Net Minority Interest"]

# Access cash flow data
annual_cashflow = result["statements"]["cash_flow"]["annual"]
latest_cashflow = annual_cashflow[0]
operating_cashflow = latest_cashflow["Operating Cash Flow"]
free_cashflow = latest_cashflow["Free Cash Flow"]

# Handle missing data
if revenue == "MISSING":
    # Data not available for this period
    pass
```

**Integration with SEC EDGAR Server:**

The Yahoo Finance and SEC EDGAR servers are designed to complement each other:

```python
# Combined workflow example
# 1. Get quantitative financial data from Yahoo Finance
financials = get_financial_statements(ticker="AAPL")
revenue_5yr = [period["Total Revenue"] for period in financials["statements"]["income_statement"]["annual"]]

# 2. Get qualitative narrative from SEC EDGAR 10-K
filings = fetch_sec_filings(ticker="AAPL", filing_types=["10-K"], years=5)
latest_10k = get_filing_content(url=filings["filings"]["10-K"][0]["primaryDocUrl"], clean_html=True)

# 3. Combine for comprehensive analysis
# - Yahoo Finance: Revenue trend showing 15% CAGR over 5 years
# - SEC EDGAR 10-K: Management explains revenue growth drivers
# - Value investing decision: Assess business quality + financial performance
```

**Installation and Testing:**

The Yahoo Finance server is automatically configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "yahoo-finance": {
      "command": "uv",
      "args": ["run", "--directory", "${CLAUDE_PLUGIN_ROOT}/servers", "python", "yahoo_finance_server.py"]
    }
  }
}
```

To test the server standalone:

```bash
# Navigate to servers directory
cd value-investor/servers

# Run the server (reads JSON-RPC from stdin, writes to stdout)
uv run python yahoo_finance_server.py

# Send test request (in another terminal):
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | uv run python yahoo_finance_server.py

# Run integration tests
uv run pytest tests/integration/test_yahoo_statements.py -v

# Run all Yahoo Finance tests (unit + integration + e2e)
uv run pytest -k yahoo -v
```

## Usage in Plugin

The agents (business-screener, financial-analyzer, etc.) automatically use these MCP tools when needed:

```python
# Example: Agent fetches 10-K and 10-Q filings
filings = fetch_sec_filings(
    ticker="AAPL",
    filing_types=["10-K", "10-Q", "DEF 14A"],
    years=10
)

# Example: Agent gets full content of a specific filing
content = get_filing_content(
    url=filings["filings"]["10-K"][0]["primaryDocUrl"],
    clean_html=True  # Remove styling for smaller size
)
```

## Development Status

**Current Status**: ✅ **Python MCP Server Implemented**

The financial data MCP server is now fully implemented in Python with SEC EDGAR filing fetching capabilities.

**Completed**:
- ✅ Python MCP server (`financial_data_server.py`)
- ✅ SEC EDGAR fetcher utility (`sec_edgar_fetcher.py`)
- ✅ MCP protocol handlers with stdio transport
- ✅ SEC EDGAR API integration with rate limiting
- ✅ Support for 10-K, 10-Q, 8-K, DEF 14A, 13F, and other filing types
- ✅ Fetch up to 10 years of historical filings
- ✅ uv integration with pyproject.toml

**Available Now**:
- `fetch_sec_filings`: Fetch multiple filing types for a company
- `get_filing_content`: Retrieve full filing document content
- `list_filing_types`: View all available filing types with descriptions

**Still To Do** (future enhancements):
- Add stock price fetching (Alpha Vantage/Yahoo Finance integration)
- Add financial statements extraction
- Add caching layer
- Add company search functionality

## Quick Start

### Installation

The MCP server uses `uv` for dependency management (no installation needed - uv handles everything automatically):

```bash
cd servers

# Test the SEC EDGAR fetcher standalone
uv run python sec_edgar_fetcher.py

# The MCP server runs automatically via .mcp.json when using the plugin
```

### Using the MCP Tools

Once the plugin is installed, agents automatically have access to these tools:

**1. Fetch SEC Filings**
```python
# Fetch 10-K and 10-Q filings for Apple
result = fetch_sec_filings(
    ticker="AAPL",
    filing_types=["10-K", "10-Q", "DEF 14A"],
    years=10
)
# Returns metadata with URLs for all filings
```

**2. Get Filing Content**
```python
# Retrieve full text of a specific filing
content = get_filing_content(
    url="https://www.sec.gov/Archives/edgar/data/320193/...",
    extract_text=True  # Strip HTML for plain text
)
```

**3. List Available Filing Types**
```python
# See all supported filing types with descriptions
filing_info = list_filing_types()
# Returns detailed info about each filing type for value investing
```

### Example Workflow

```python
# 1. Fetch Apple's filings from last 10 years
filings = fetch_sec_filings(
    ticker="AAPL",
    filing_types=["10-K", "10-Q", "DEF 14A", "8-K"],
    years=10
)

# 2. Get the most recent 10-K
latest_10k = filings["filings"]["10-K"][0]
print(f"Latest 10-K: {latest_10k['filingDate']}")
print(f"URL: {latest_10k['primaryDocUrl']}")

# 3. Retrieve the full filing content
content = get_filing_content(
    url=latest_10k['primaryDocUrl'],
    extract_text=True
)

# 4. Analyze the filing content for value investing insights
# (agents can now read and analyze the full 10-K)
```

## Testing

Comprehensive test suite with unit, integration, and agent parsing tests.

### Quick Start

```bash
# Install test dependencies
cd servers
uv sync --extra dev

# Run all tests (fast tests only)
uv run pytest -m "not agent"

# Run all tests including agent tests (requires API key)
export ANTHROPIC_API_KEY="your-key-here"
uv run pytest
```

### Test Categories

**Unit Tests** (25 tests, ~0.05s)
- HTML cleaning functionality
- Tag removal and preservation
- Text extraction
- Configuration options

**Integration Tests** (11 tests, ~1.7s)
- Real SEC filing processing
- Size reduction validation
- Content preservation
- Cross-company consistency

**Agent Tests** (4 tests, ~120s, requires API key)
- business-screener parsing validation
- Filing type understanding
- Business context extraction

### Test Coverage

```
Unit tests:        25 passed ✅
Integration tests: 11 passed ✅
Agent tests:        4 tests (requires ANTHROPIC_API_KEY)
Total:             36 passing tests
```

### Common Commands

```bash
# Fast tests only
uv run pytest -m unit                    # Unit tests (0.05s)
uv run pytest -m integration             # Integration tests (1.7s)
uv run pytest -m "not agent"             # Skip agent tests

# Specific tests
uv run pytest tests/unit/                # Run all unit tests
uv run pytest -k "clean"                 # Run tests matching "clean"
uv run pytest -v                         # Verbose output

# Test data management
uv run python download_test_data.py      # Download SEC filings
uv run python validate_test_data.py      # Validate test data

# Inspection tools
uv run python compare_filings.py test_data/fixtures/AAPL/10-K_2025-10-31.html --mode stats
```

### Test Data

Test data includes real SEC filings:
- **AAPL**: 10-K, 10-Q
- **MSFT**: 10-K, 10-Q
- Total: 4 filings (15.4 MB original → 1.5 MB cleaned, 90.5% reduction)

Located in `test_data/fixtures/` with metadata index.

### Documentation

See [TESTING.md](./TESTING.md) for comprehensive testing guide including:
- Test structure and organization
- Running specific test categories
- Adding new test data
- Debugging test failures
- CI/CD integration
- Performance benchmarks

## Resources

**SEC EDGAR:**
- **SEC EDGAR API**: https://www.sec.gov/edgar/sec-api-documentation
- **SEC Developer Resources**: https://www.sec.gov/developer
- **Company Tickers JSON**: https://www.sec.gov/files/company_tickers.json
- **Submissions API**: https://data.sec.gov/submissions/

**Yahoo Finance:**
- **yfinance Library**: https://github.com/ranaroussi/yfinance
- **Yahoo Finance**: https://finance.yahoo.com/
- **yfinance Documentation**: https://pypi.org/project/yfinance/

**Protocols and Tools:**
- **MCP Protocol Spec**: https://spec.modelcontextprotocol.io/
- **uv (Python Package Manager)**: https://docs.astral.sh/uv/
- **JSON-RPC 2.0 Specification**: https://www.jsonrpc.org/specification

## Architecture

**MCP Server Files:**
- `financial_data_server.py` - SEC EDGAR MCP server (stdio transport)
- `yahoo_finance_server.py` - Yahoo Finance MCP server (stdio transport)
- `sec_edgar_fetcher.py` - SEC EDGAR API client with rate limiting
- `yahoo_finance_fetcher.py` - Yahoo Finance data fetcher using yfinance library
- `html_cleaner.py` - HTML cleaning utilities (shared)
- `pyproject.toml` - Python dependencies managed by uv
- `requirements.txt` - Legacy pip requirements (use uv instead)

**SEC EDGAR Server Features:**
- Respects SEC rate limit (10 requests/second)
- Proper User-Agent header (SEC requirement)
- CIK lookup from ticker symbol
- Fetches up to 10 years of historical filings
- Returns both metadata and full filing content
- Supports all major filing types for value investing

**Yahoo Finance Server Features:**
- 30-second timeout on all HTTP requests
- Ticker sanitization prevents injection attacks
- Consistent JSON schema with MISSING markers
- ISO 8601 date format (YYYY-MM-DD)
- ISO 4217 currency codes (USD, EUR, JPY)
- Clear error codes for all failure scenarios
- Up to 5 years annual + current year quarterly data

