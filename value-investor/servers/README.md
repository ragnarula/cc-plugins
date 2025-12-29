# Financial Data MCP Server Setup

This directory contains the MCP (Model Context Protocol) server for fetching financial data from free APIs.

## Overview

The value-investor plugin uses an MCP server to access:
- SEC EDGAR filings (10-K, 10-Q, 8-K, DEF 14A, 13F, and other filing types)

## Data Source

### SEC EDGAR API
- **URL**: https://www.sec.gov/edgar/sec-api-documentation
- **Authentication**: None required (rate limited)
- **Data**: Official SEC filings (10-K, 10-Q, 8-K, DEF 14A, 13F, etc.)
- **Rate Limit**: 10 requests/second

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

- **SEC EDGAR API**: https://www.sec.gov/edgar/sec-api-documentation
- **SEC Developer Resources**: https://www.sec.gov/developer
- **Company Tickers JSON**: https://www.sec.gov/files/company_tickers.json
- **Submissions API**: https://data.sec.gov/submissions/
- **MCP Protocol Spec**: https://spec.modelcontextprotocol.io/
- **uv (Python Package Manager)**: https://docs.astral.sh/uv/

## Architecture

**Files:**
- `sec_edgar_fetcher.py` - Core SEC EDGAR API client with rate limiting
- `financial_data_server.py` - MCP server implementation (stdio transport)
- `pyproject.toml` - Python dependencies managed by uv
- `requirements.txt` - Legacy pip requirements (use uv instead)

**Key Features:**
- Respects SEC rate limit (10 requests/second)
- Proper User-Agent header (SEC requirement)
- CIK lookup from ticker symbol
- Fetches up to 10 years of historical filings
- Returns both metadata and full filing content
- Supports all major filing types for value investing

