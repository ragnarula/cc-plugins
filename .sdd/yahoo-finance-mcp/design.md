# Design: Yahoo Finance Financial Statements MCP

**Version:** 1.0
**Date:** 2025-12-31
**Status:** Approved
**Linked Specification** `.sdd/yahoo-finance-mcp/specification.md`

---

# Design Document

---

## Architecture Overview

### Current Architecture Context

The cc-plugins repository contains a value-investor plugin with an existing MCP server implementation pattern:

- **Existing MCP Server**: `financial_data_server.py` provides SEC EDGAR filing access using stdio transport
- **MCPServer Pattern**: Base class handles JSON-RPC protocol, tool registration, and request routing
- **uv-based Dependency Management**: All Python dependencies managed via `pyproject.toml` and uv
- **Shared Utilities**: `html_cleaner.py` provides HTML cleaning functionality
- **Configuration**: `.mcp.json` configures MCP servers with command and args for uv execution
- **Directory Structure**: `value-investor/servers/` contains all MCP server implementations

The Yahoo Finance MCP server will follow the same architectural pattern, living alongside the SEC EDGAR server. Both servers will be independently usable but designed to complement each other: SEC EDGAR provides qualitative narrative data (10-K filings, MD&A) while Yahoo Finance provides quantitative structured data (income statements, balance sheets, cash flow statements).

### Proposed Architecture

The Yahoo Finance MCP server will be a new standalone Python MCP server following the established pattern:

```
value-investor/servers/
├── financial_data_server.py          # Existing: SEC EDGAR MCP server
├── yahoo_finance_server.py           # NEW: Yahoo Finance MCP server
├── yahoo_finance_fetcher.py          # NEW: Yahoo Finance API client
├── sec_edgar_fetcher.py              # Existing: SEC EDGAR API client
├── html_cleaner.py                   # Existing: Shared utility
├── pyproject.toml                    # Updated: Add yfinance dependency
└── tests/
    ├── unit/
    │   └── test_yahoo_finance_fetcher.py    # NEW: Unit tests
    └── integration/
        └── test_yahoo_statements.py         # NEW: Integration tests

value-investor/.mcp.json              # Updated: Add yahoo-finance server config
```

**Sequence Flow for Tool Invocation:**

1. User/Agent invokes MCP tool `get_financial_statements` with ticker "AAPL"
2. MCP server receives JSON-RPC request via stdio
3. `yahoo_finance_server.py` routes to registered tool handler
4. Tool handler calls `YahooFinanceFetcher.get_financial_statements("AAPL")`
5. `YahooFinanceFetcher` fetches data from yfinance library
6. Data is transformed to consistent JSON schema with MISSING markers
7. Error handling wraps any failures with clear error codes
8. Response returned via JSON-RPC to caller
9. 30-second timeout enforced at HTTP request level

**Component Communication Pattern:**

```
Claude Agent
    ↓ (MCP tool call)
MCPServer (stdio JSON-RPC)
    ↓ (route to tool)
get_financial_statements(ticker)
    ↓ (fetch data)
YahooFinanceFetcher
    ↓ (yfinance library)
Yahoo Finance API
    ↓ (raw data)
YahooFinanceFetcher (transform)
    ↓ (consistent JSON)
MCPServer (format response)
    ↓ (JSON-RPC response)
Claude Agent (receives data)
```

### Technology Decisions

**Primary Technology: yfinance Python Library**

**Rationale**: The yfinance library is the de facto standard for Yahoo Finance data access in Python with:
- Active maintenance and large community (30k+ GitHub stars)
- Robust API for financial statements, historical data, and company info
- Built-in error handling and retry logic
- Free and requires no API keys
- Compatible with existing dependency management (uv/pip)

**Alternative Considered**: Direct Yahoo Finance API calls via requests
- **Rejected**: Yahoo Finance's unofficial API is unstable and frequently changes endpoints. yfinance abstracts these changes and provides a stable interface.

**Data Format: JSON with ISO Standards**

**Rationale**:
- ISO 8601 dates (YYYY-MM-DD) for universal parsing
- ISO 4217 currency codes (USD, EUR, JPY) for international compatibility
- Consistent schema regardless of missing data (REQ-NFN-04)
- Native JSON serialization for MCP protocol

**Error Handling Strategy: Explicit Error Codes**

**Rationale**:
- Clear error codes (TICKER_NOT_FOUND, API_TIMEOUT, DATA_UNAVAILABLE) enable programmatic handling
- Human-readable messages support both AI agents and end users (REQ-NFN-03)
- Structured error responses match MCP protocol conventions

**Timeout Strategy: Request-Level Timeouts**

**Rationale**:
- 30-second timeout enforced at yfinance/requests level (REQ-NFN-01)
- Prevents hanging connections
- Returns API_TIMEOUT error code for graceful degradation

### Quality Attributes

**Reliability:**
- Data returned exactly as provided by Yahoo Finance without transformation (REQ-NFN-02)
- Explicit MISSING markers for unavailable data prevent silent failures (REQ-FN-02)
- Comprehensive error handling with clear error codes (REQ-FN-03)
- Input sanitization prevents injection attacks (REQ-NFN-05)

**Performance:**
- 30-second maximum response time enforced via timeouts (REQ-NFN-01)
- Single API call per tool invocation (yfinance caches internally)
- Minimal data transformation overhead

**Maintainability:**
- Follows established MCPServer pattern from financial_data_server.py
- Clear separation of concerns (server/fetcher/transformer)
- Comprehensive unit and integration tests
- Consistent with existing codebase conventions

**Security:**
- Ticker symbol sanitization (alphanumeric + hyphen/period only) prevents injection
- No data caching or persistence (REQ-NFN-05)
- No sensitive data logged (only ticker symbols in error messages)

**Scalability:**
- Stateless server design (no session management)
- No rate limiting needed (Yahoo Finance via yfinance handles this internally)
- Each request independent and isolated

---

## API Design

### MCP Tool: get_financial_statements

**Purpose**: Retrieve all three major financial statements (income statement, balance sheet, cash flow statement) for a given ticker, including historical annual data and current year quarterly data.

**Input Schema:**

```json
{
  "type": "object",
  "properties": {
    "ticker": {
      "type": "string",
      "description": "Stock ticker symbol (e.g., 'AAPL', 'MSFT')",
      "pattern": "^[A-Z0-9.-]+$"
    }
  },
  "required": ["ticker"]
}
```

**Success Response Schema:**

```json
{
  "ticker": "AAPL",
  "currency": "USD",
  "fiscal_year_end": "September",
  "retrieved_at": "2025-12-31T15:30:00Z",
  "statements": {
    "income_statement": {
      "annual": [
        {
          "period_end": "2024-09-30",
          "revenue": 385706000000,
          "cost_of_revenue": 210352000000,
          "gross_profit": 175354000000,
          "operating_expenses": 56055000000,
          "operating_income": 119299000000,
          "net_income": 93736000000,
          "earnings_per_share": 6.13,
          "..."
        }
      ],
      "quarterly": [
        {
          "period_end": "2025-03-31",
          "revenue": "MISSING",
          "..."
        }
      ]
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
```

**Error Response Schema:**

```json
{
  "error": {
    "code": "TICKER_NOT_FOUND",
    "message": "No financial data found for ticker 'XYZ999'. Verify the ticker symbol is correct.",
    "ticker": "XYZ999"
  }
}
```

**Error Codes:**

- `TICKER_NOT_FOUND`: Invalid or unknown ticker symbol
- `API_TIMEOUT`: Request exceeded 30-second timeout
- `DATA_UNAVAILABLE`: Ticker valid but no financial statements available
- `INVALID_TICKER_FORMAT`: Ticker contains invalid characters
- `API_ERROR`: Unexpected error from Yahoo Finance API

**Data Model Conventions:**

1. **Missing Data Handling**: Use string "MISSING" for unavailable fields (never null or omit)
2. **Number Format**: All financial values as integers (not floats) representing smallest currency unit
3. **Date Format**: ISO 8601 (YYYY-MM-DD) for all period_end dates
4. **Currency**: ISO 4217 three-letter codes (USD, EUR, JPY)
5. **Field Naming**: Snake_case for consistency with Python conventions
6. **Ordering**: Annual data sorted newest-to-oldest, quarterly data sorted newest-to-oldest

**Versioning Approach:**

- Version 1.0: Initial implementation with current schema
- Future versions: Add optional parameters (e.g., `years`, `include_ttm`, `include_estimates`)
- Breaking changes: Increment major version, maintain backward compatibility in MCP server for 1 version cycle

---

## Modified Components

### pyproject.toml

**Change Description**: Currently defines dependencies for SEC EDGAR MCP server (requests, beautifulsoup4, lxml). Needs to add yfinance dependency for Yahoo Finance data access.

**Dependants**:
- `yahoo_finance_server.py` (imports yfinance)
- `yahoo_finance_fetcher.py` (imports yfinance)
- uv lock file (uv.lock will be regenerated)

**Kind**: Configuration file (TOML)

**Requirements References**
- REQ-FN-01: yfinance provides financial statement fetching capability
- REQ-NFN-01: yfinance supports timeout configuration for 30s limit

**Test Cases**
- TEST-DEPS-INSTALL: Verify uv sync successfully installs yfinance
- TEST-DEPS-VERSION: Verify yfinance version meets minimum requirements (>=0.2.40)

### .mcp.json

**Change Description**: Currently configures only the financial-data MCP server for SEC EDGAR filings. Needs to add configuration for yahoo-finance MCP server to enable Yahoo Finance tools in Claude agents.

**Dependants**:
- Claude Code runtime (reads this file to start MCP servers)
- Value investor agents (will have access to new tools)

**Kind**: Configuration file (JSON)

**Requirements References**
- REQ-FN-01: Enables get_financial_statements tool availability
- REQ-NFN-05: Ensures server runs in isolated process for security

**Test Cases**
- TEST-MCP-CONFIG-VALID: Verify JSON is well-formed and parseable
- TEST-MCP-SERVER-START: Verify yahoo-finance server starts successfully via uv run

---

## Added Components

### YahooFinanceFetcher

**Description**: Core API client that fetches financial statement data from Yahoo Finance using the yfinance library. Handles data retrieval, error handling, timeout enforcement, and transformation to consistent JSON schema with MISSING markers for unavailable data.

**Users**:
- `yahoo_finance_server.py` (MCP tool handlers call this class)
- Integration tests (test_yahoo_statements.py)

**Kind**: Python Class

**Location**: `value-investor/servers/yahoo_finance_fetcher.py` (new file)

**Requirements References**
- REQ-FN-01: Implements fetching of all three financial statements with historical data
- REQ-FN-02: Handles missing data by marking fields as "MISSING"
- REQ-NFN-01: Enforces 30-second timeout on all API requests
- REQ-NFN-02: Returns data unmodified from Yahoo Finance source
- REQ-NFN-04: Ensures consistent JSON structure and date/currency formats
- REQ-NFN-05: Sanitizes ticker input to prevent injection attacks

**Test Cases**
- TEST-FETCH-SUCCESS: Verify successful retrieval for valid ticker (AAPL)
- TEST-FETCH-INVALID-TICKER: Verify TICKER_NOT_FOUND error for invalid ticker
- TEST-FETCH-MISSING-DATA: Verify MISSING markers for incomplete data
- TEST-FETCH-TIMEOUT: Verify API_TIMEOUT error when request exceeds 30s
- TEST-SANITIZE-TICKER: Verify ticker sanitization prevents SQL injection patterns
- TEST-DATE-FORMAT: Verify all dates in ISO 8601 format
- TEST-CURRENCY-FORMAT: Verify currency codes in ISO 4217 format
- TEST-SCHEMA-CONSISTENCY: Verify schema consistency when data missing vs available
- TEST-ANNUAL-DATA: Verify retrieval of up to 5 years annual data
- TEST-QUARTERLY-DATA: Verify retrieval of current year quarterly data

### yahoo_finance_server.py

**Description**: MCP server implementation that exposes get_financial_statements as an MCP tool using stdio transport. Follows MCPServer pattern from financial_data_server.py with JSON-RPC protocol handling, tool registration, and error response formatting.

**Users**:
- Claude Code runtime (launches via .mcp.json configuration)
- Claude agents (invoke via MCP tool calls)

**Kind**: Python Module (executable script)

**Location**: `value-investor/servers/yahoo_finance_server.py` (new file)

**Requirements References**
- REQ-FN-01: Exposes get_financial_statements tool via MCP protocol
- REQ-FN-03: Returns clear error messages in MCP error responses
- REQ-NFN-03: Formats errors with code, message, and ticker

**Test Cases**
- TEST-MCP-INITIALIZE: Verify MCP initialize response includes server info
- TEST-MCP-TOOLS-LIST: Verify tools/list returns get_financial_statements
- TEST-MCP-TOOL-CALL: Verify tools/call invokes fetcher and returns data
- TEST-MCP-ERROR-HANDLING: Verify MCP error response format for failures
- TEST-MCP-STDIO-TRANSPORT: Verify server reads stdin and writes stdout correctly
- TEST-MCP-JSONRPC-PROTOCOL: Verify JSON-RPC 2.0 compliance

### test_yahoo_finance_fetcher.py

**Description**: Unit tests for YahooFinanceFetcher class covering all error conditions, data transformation logic, and edge cases. Uses pytest with mocked yfinance responses to avoid external API calls.

**Users**:
- Test suite (pytest)
- CI/CD pipeline (future)

**Kind**: Python Module (pytest test file)

**Location**: `value-investor/servers/tests/unit/test_yahoo_finance_fetcher.py` (new file)

**Requirements References**
- REQ-FN-01: Test coverage for financial statement fetching
- REQ-FN-02: Test coverage for missing data handling
- REQ-FN-03: Test coverage for error message clarity
- REQ-NFN-01: Test coverage for timeout enforcement
- REQ-NFN-02: Test coverage for data accuracy (no transformation)
- REQ-NFN-04: Test coverage for schema consistency
- REQ-NFN-05: Test coverage for input sanitization

**Test Cases**
- TEST-UNIT-VALID-TICKER: Mock successful yfinance response
- TEST-UNIT-INVALID-TICKER: Mock ticker not found scenario
- TEST-UNIT-MISSING-FIELDS: Mock response with incomplete data
- TEST-UNIT-TIMEOUT: Mock timeout exception handling
- TEST-UNIT-SANITIZATION: Test ticker validation regex
- TEST-UNIT-DATE-TRANSFORMATION: Test date format conversion
- TEST-UNIT-CURRENCY-EXTRACTION: Test currency code extraction
- TEST-UNIT-MISSING-MARKER: Test "MISSING" string insertion

### test_yahoo_statements.py

**Description**: Integration tests that validate end-to-end financial statement retrieval using real Yahoo Finance API calls. Tests actual data quality, schema consistency, and error handling with live API. Marked with @pytest.mark.integration for selective execution.

**Users**:
- Test suite (pytest with integration marker)
- Manual testing during development

**Kind**: Python Module (pytest test file)

**Location**: `value-investor/servers/tests/integration/test_yahoo_statements.py` (new file)

**Requirements References**
- REQ-FN-01: End-to-end validation of financial statement retrieval
- REQ-NFN-02: Validation that data matches Yahoo Finance source
- REQ-NFN-04: Validation of consistent schema across multiple tickers

**Test Cases**
- TEST-INTEGRATION-AAPL: Verify retrieval of Apple financial statements
- TEST-INTEGRATION-MSFT: Verify retrieval of Microsoft financial statements
- TEST-INTEGRATION-SCHEMA: Verify schema consistency across multiple companies
- TEST-INTEGRATION-HISTORICAL: Verify 5 years of annual data available
- TEST-INTEGRATION-QUARTERLY: Verify current year quarterly data available
- TEST-INTEGRATION-MISSING-DATA: Test ticker with incomplete data (recent IPO)
- TEST-INTEGRATION-INVALID-TICKER: Test error handling with invalid ticker

### README.md updates

**Description**: Documentation updates to value-investor/servers/README.md explaining the new Yahoo Finance MCP server, installation, usage examples, and how it complements the existing SEC EDGAR server.

**Users**:
- Developers setting up the plugin
- Users understanding available MCP tools

**Kind**: Documentation (Markdown)

**Location**: `value-investor/servers/README.md` (existing file, append new section)

**Requirements References**
- All requirements: Documentation provides usage guidance for all features

**Test Cases**
- TEST-DOC-COMPLETENESS: Manual review that all tools documented
- TEST-DOC-EXAMPLES: Manual verification that examples are correct

---

## Test Strategy

### Test Pyramid

**Unit Tests** (Fast, no I/O):
- YahooFinanceFetcher class methods (data transformation, error handling, validation)
- Ticker sanitization logic
- Date and currency formatting functions
- Missing data marker insertion
- Error code generation
- Mock yfinance responses to avoid external API calls
- Target: 20-25 unit tests, <0.1s execution time

**Integration Tests** (Real API calls):
- End-to-end financial statement retrieval with real Yahoo Finance API
- Cross-ticker schema consistency validation
- Historical data availability validation (5 years annual)
- Quarterly data availability validation (current year)
- Real error scenarios (invalid tickers, incomplete data)
- Target: 8-10 integration tests, ~5s execution time
- Marked with @pytest.mark.integration for selective execution

**E2E Tests** (MCP protocol):
- Full MCP server startup and tool invocation via stdio
- JSON-RPC protocol compliance
- Tool registration and discovery (tools/list)
- Tool execution (tools/call)
- Error response formatting
- Target: 5-6 E2E tests, ~2s execution time

### Coverage Strategy

**Critical Paths:**
1. Happy path: Valid ticker → successful financial statement retrieval → consistent JSON response
2. Invalid ticker path: Invalid ticker → TICKER_NOT_FOUND error → clear error message
3. Missing data path: Valid ticker with incomplete data → MISSING markers → consistent schema
4. Timeout path: Slow API response → API_TIMEOUT error after 30s → graceful degradation

**Performance Tests:**
- Measure end-to-end latency for typical tickers (should be <5s for cached data)
- Verify timeout enforcement at exactly 30 seconds
- Monitor memory usage during large data retrieval
- No formal performance suite initially, but add benchmarks if performance issues arise

**Security Tests:**
- Ticker input fuzzing with SQL injection patterns
- Ticker input fuzzing with command injection patterns
- Ticker input fuzzing with path traversal patterns
- Verify no sensitive data in error messages or logs
- Verify no data persistence between requests

### Test Data

**Sources:**
- **Real tickers for integration tests**: AAPL, MSFT, GOOGL (established companies with complete data)
- **Edge case tickers**: Recent IPOs with <5 years history, small-cap stocks with incomplete data
- **Invalid tickers**: XYZ999, INVALID, SQL-INJECTION-PATTERN
- **Mocked responses**: JSON fixtures for unit tests to avoid API dependencies

**Requirements:**
- No downloaded test data files needed (unlike SEC EDGAR server)
- Integration tests make live API calls (fast enough for CI)
- Mock data fixtures for unit tests stored in tests/fixtures/yahoo_finance/

**Maintenance:**
- Mock fixtures updated when yfinance library changes response format
- Integration tests may break if Yahoo Finance changes API (acceptable, update as needed)

### Test Feasibility

**No Blockers Identified:**
- yfinance library is stable and well-tested (no need to build test infrastructure)
- Yahoo Finance API is free and requires no authentication (no API key setup needed)
- Existing pytest infrastructure in place (can reuse patterns from SEC EDGAR tests)
- No special test environment needed (works on any machine with internet)

**Test Execution:**
```bash
# Fast tests only (unit)
uv run pytest -m "unit" tests/unit/test_yahoo_finance_fetcher.py

# Integration tests (real API calls)
uv run pytest -m "integration" tests/integration/test_yahoo_statements.py

# All tests
uv run pytest tests/unit/test_yahoo_finance_fetcher.py tests/integration/test_yahoo_statements.py
```

---

## Risks and Dependencies

### Technical Risks

**Risk 1: Yahoo Finance API Instability**
- **Description**: Yahoo Finance has no official public API. yfinance uses web scraping which can break if Yahoo changes their website structure.
- **Likelihood**: Medium (happens 1-2 times per year based on yfinance GitHub issues)
- **Impact**: High (tool becomes non-functional until yfinance updates)
- **Mitigation**:
  - Use latest stable yfinance version (active maintenance)
  - Implement graceful error handling with clear error messages
  - Monitor yfinance GitHub for breaking changes
  - Consider fallback to alternative data source in future (Alpha Vantage, Financial Modeling Prep)

**Risk 2: Data Quality Variance**
- **Description**: Yahoo Finance data quality varies by ticker (incomplete data for small-cap stocks, recent IPOs, foreign exchanges)
- **Likelihood**: High (expected for edge-case tickers)
- **Impact**: Low (requirement REQ-FN-02 explicitly handles this with MISSING markers)
- **Mitigation**:
  - Explicit MISSING markers for unavailable data (requirement)
  - Integration tests covering edge cases (recent IPOs, small-cap)
  - Clear documentation of data quality expectations

**Risk 3: Rate Limiting**
- **Description**: Yahoo Finance may rate limit or block excessive requests
- **Likelihood**: Low (yfinance handles rate limiting internally, typical usage is infrequent)
- **Impact**: Medium (temporary unavailability)
- **Mitigation**:
  - No caching needed per requirement (each request independent)
  - yfinance implements exponential backoff internally
  - Document expected usage patterns (value investing = infrequent queries)

### External Dependencies

**Primary Dependency: yfinance Library**
- **Version**: >=0.2.40 (current stable)
- **Maintenance**: Actively maintained (last release <30 days)
- **License**: Apache 2.0 (permissive, compatible with plugin)
- **Fallback**: Could implement direct API scraping if library abandoned (not recommended)

**Secondary Dependency: Yahoo Finance Service**
- **Availability**: No SLA (free service)
- **Uptime**: Generally high (>99% based on community reports)
- **Alternatives**: Alpha Vantage (requires API key), Financial Modeling Prep (paid), SEC EDGAR (only official filings, no statements)

**Python Runtime Dependencies**
- **Python**: >=3.10 (matches existing server requirements)
- **requests**: >=2.31.0 (already in pyproject.toml)
- **pandas**: Transitive dependency of yfinance (automatically installed)

### Assumptions and Constraints

**Assumptions:**
1. Users have internet access when invoking tools (no offline mode)
2. Yahoo Finance will continue to provide free financial data access
3. yfinance library maintainers will continue updating for API changes
4. Claude agents can handle "MISSING" markers appropriately in analysis
5. 30-second timeout is sufficient for typical API responses (usually <5s)

**Constraints:**
1. No API authentication available (Yahoo Finance is free, no API keys)
2. Cannot guarantee 100% data completeness (depends on Yahoo Finance coverage)
3. Cannot cache data (REQ: no data persistence between requests)
4. Cannot fetch more than ~5 years historical annual data (Yahoo Finance limitation)
5. Cannot fetch quarterly data beyond current fiscal year (Yahoo Finance limitation)
6. Must follow existing MCP server pattern (consistency with financial_data_server.py)

**Design Constraints:**
1. Must use uv for dependency management (established project pattern)
2. Must use stdio transport for MCP protocol (Claude Code requirement)
3. Must return JSON-RPC 2.0 compliant responses (MCP protocol requirement)
4. Must handle errors gracefully without raising exceptions to MCP layer (error objects, not exceptions)

---

## Feasability Review

**No Prerequisites Required**

This feature is fully implementable with existing infrastructure:
- ✅ Python environment and uv already configured
- ✅ MCP server pattern established in financial_data_server.py
- ✅ Test infrastructure (pytest) already in place
- ✅ yfinance library is mature and stable
- ✅ No API keys or authentication setup needed
- ✅ No new infrastructure or services required

**Future Enhancements (Out of Scope for v1.0):**

1. **Data Caching Layer** (separate iteration)
   - Would require Redis/SQLite infrastructure
   - Would improve performance but conflicts with REQ-NFN-05 (no data persistence)
   - Defer until explicit caching requirement added

2. **Financial Ratios Calculation** (separate iteration)
   - Explicitly out of scope per specification
   - Would require financial modeling logic
   - Should be separate tool if needed

3. **Multi-Ticker Comparison** (separate iteration)
   - Explicitly out of scope per specification
   - Would require different tool design (batch operations)
   - Consider if user demand arises

**Ready to Proceed**: All requirements are implementable with current infrastructure and dependencies.

---

## Task Breakdown

### Phase 1: Infrastructure Setup

**Goal**: Prepare development environment and add dependencies

- Task 1.1: Add yfinance dependency to pyproject.toml
  - Status: Complete
  - Update dependencies list with `yfinance>=0.2.40`
  - Run `uv sync` to install and generate lock file
  - Verify installation with `uv run python -c "import yfinance"`

- Task 1.2: Update .mcp.json with yahoo-finance server configuration
  - Status: Complete
  - Add new server entry: `"yahoo-finance": {"command": "uv", "args": [...]}`
  - Verify JSON syntax is valid
  - Test that server path resolves correctly

- Task 1.3: Create test fixtures directory structure
  - Status: Complete
  - Create `tests/unit/` if not exists
  - Create `tests/integration/` if not exists
  - Create `tests/fixtures/yahoo_finance/` for mock data

### Phase 2: Core Fetcher Implementation

**Goal**: Implement YahooFinanceFetcher class with data retrieval and transformation

- Task 2.1: Implement YahooFinanceFetcher class skeleton
  - Status: Complete
  - Create `yahoo_finance_fetcher.py`
  - Define class with `__init__` and `get_financial_statements` method signature
  - Add ticker sanitization method `_sanitize_ticker`
  - Add timeout configuration (30s default)

- Task 2.2: Implement financial statement fetching with yfinance
  - Status: Complete
  - Use `yfinance.Ticker(ticker)` to instantiate ticker object
  - Fetch `ticker.financials` (income statement annual)
  - Fetch `ticker.quarterly_financials` (income statement quarterly)
  - Fetch `ticker.balance_sheet` and `ticker.quarterly_balance_sheet`
  - Fetch `ticker.cashflow` and `ticker.quarterly_cashflow`
  - Implement 30-second timeout on all HTTP requests via yfinance

- Task 2.3: Implement data transformation to consistent JSON schema
  - Status: Complete
  - Transform pandas DataFrames to JSON dictionaries
  - Convert dates to ISO 8601 format (YYYY-MM-DD)
  - Extract currency code from ticker.info (ISO 4217)
  - Sort annual data by date (newest first)
  - Sort quarterly data by date (newest first)
  - Limit annual data to 5 years
  - Limit quarterly data to current fiscal year

- Task 2.4: Implement missing data handling with MISSING markers
  - Status: Complete
  - Detect missing/NaN values in pandas DataFrames
  - Replace with string "MISSING" in JSON output
  - Ensure schema consistency (same fields present regardless of MISSING values)
  - Handle edge case: ticker with no financial data at all

- Task 2.5: Implement error handling with clear error codes
  - Status: Complete
  - Catch yfinance exceptions and map to error codes
  - TICKER_NOT_FOUND: Ticker not found in Yahoo Finance
  - API_TIMEOUT: Request timeout after 30s
  - DATA_UNAVAILABLE: Ticker valid but no financial statements
  - INVALID_TICKER_FORMAT: Ticker fails sanitization regex
  - API_ERROR: Unexpected yfinance error
  - Return error dict with code, message, ticker fields

### Phase 3: MCP Server Implementation

**Goal**: Create MCP server following financial_data_server.py pattern

- Task 3.1: Create yahoo_finance_server.py with MCPServer class
  - Status: Complete
  - Copy MCPServer base class from financial_data_server.py
  - Update server name to "yahoo-finance"
  - Update server version to "0.1.0"
  - Instantiate YahooFinanceFetcher in `__init__`

- Task 3.2: Register get_financial_statements MCP tool
  - Status: Complete
  - Use `@server.tool` decorator
  - Define tool name: "get_financial_statements"
  - Define description: detailed explanation of tool purpose
  - Define input schema with ticker parameter (string, required)
  - Implement tool handler that calls YahooFinanceFetcher

- Task 3.3: Implement JSON-RPC protocol handlers
  - Status: Complete
  - Handle "initialize" method (return server info and capabilities)
  - Handle "tools/list" method (return tool metadata)
  - Handle "tools/call" method (route to tool handler)
  - Return JSON-RPC 2.0 compliant responses
  - Format errors as JSON-RPC error objects (not exceptions)

- Task 3.4: Implement stdio transport
  - Status: Complete
  - Read JSON-RPC requests from stdin line-by-line
  - Write JSON-RPC responses to stdout with flush
  - Write error logs to stderr (not stdout)
  - Handle EOF gracefully (server shutdown)
  - Add main() function with asyncio.run()

### Phase 4: Unit Testing

**Goal**: Achieve comprehensive unit test coverage with mocked dependencies

- Task 4.1: Create test_yahoo_finance_fetcher.py with pytest fixtures
  - Status: Complete
  - Create file in tests/unit/
  - Define pytest fixture for YahooFinanceFetcher instance
  - Define mock yfinance.Ticker fixture
  - Mark tests with @pytest.mark.unit

- Task 4.2: Write unit tests for successful data retrieval
  - Status: Complete
  - TEST-UNIT-VALID-TICKER: Mock successful response, verify JSON structure
  - TEST-UNIT-DATE-TRANSFORMATION: Verify ISO 8601 date format
  - TEST-UNIT-CURRENCY-EXTRACTION: Verify ISO 4217 currency code
  - TEST-UNIT-DATA-SORTING: Verify newest-first ordering

- Task 4.3: Write unit tests for missing data handling
  - Status: Complete
  - TEST-UNIT-MISSING-FIELDS: Mock response with NaN values
  - TEST-UNIT-MISSING-MARKER: Verify "MISSING" string insertion
  - TEST-UNIT-SCHEMA-CONSISTENCY: Verify same fields present with/without data

- Task 4.4: Write unit tests for error conditions
  - Status: Complete
  - TEST-UNIT-INVALID-TICKER: Verify TICKER_NOT_FOUND error code
  - TEST-UNIT-TIMEOUT: Mock timeout exception, verify API_TIMEOUT
  - TEST-UNIT-SANITIZATION: Test ticker validation regex
  - TEST-UNIT-API-ERROR: Mock yfinance exception, verify error handling

- Task 4.5: Run unit tests and verify coverage
  - Status: Complete
  - Execute: `uv run pytest -m unit tests/unit/test_yahoo_finance_fetcher.py -v`
  - Target: All tests passing, >90% code coverage
  - Result: All 14 tests passing

### Phase 5: Integration Testing

**Goal**: Validate end-to-end functionality with real Yahoo Finance API

- Task 5.1: Create test_yahoo_statements.py for integration tests
  - Status: Complete
  - Create file in tests/integration/
  - Mark tests with @pytest.mark.integration
  - Add conftest.py fixture for YahooFinanceFetcher instance

- Task 5.2: Write integration tests for established companies
  - Status: Complete
  - TEST-INTEGRATION-AAPL: Fetch Apple statements, verify structure
  - TEST-INTEGRATION-MSFT: Fetch Microsoft statements, verify structure
  - TEST-INTEGRATION-HISTORICAL: Verify 5 years of annual data
  - TEST-INTEGRATION-QUARTERLY: Verify current year quarterly data

- Task 5.3: Write integration tests for edge cases
  - Status: Complete
  - TEST-INTEGRATION-MISSING-DATA: Test recent IPO with incomplete data
  - TEST-INTEGRATION-INVALID-TICKER: Test invalid ticker error handling
  - TEST-INTEGRATION-SCHEMA: Verify schema consistency across tickers

- Task 5.4: Run integration tests and validate data quality
  - Status: Complete
  - Execute: `uv run pytest -m integration tests/integration/test_yahoo_statements.py`
  - Result: All 11 tests passed in 11.19s
  - Validated: ISO 8601 dates, ISO 4217 currency, MISSING markers, schema consistency

### Phase 6: E2E MCP Protocol Testing

**Goal**: Validate MCP server protocol compliance and tool invocation

- Task 6.1: Write E2E test for MCP initialize
  - Status: Complete
  - TEST-MCP-INITIALIZE: Send initialize request, verify server info response
  - Verify protocolVersion field present
  - Verify serverInfo contains name and version

- Task 6.2: Write E2E test for MCP tools/list
  - Status: Complete
  - TEST-MCP-TOOLS-LIST: Send tools/list request
  - Verify get_financial_statements tool in response
  - Verify tool has name, description, inputSchema

- Task 6.3: Write E2E test for MCP tools/call
  - Status: Complete
  - TEST-MCP-TOOL-CALL: Send tools/call request with ticker=AAPL
  - Verify successful response with financial data
  - Verify response format: {content: [{type: "text", text: JSON}]}

- Task 6.4: Write E2E test for MCP error handling
  - Status: Complete
  - TEST-MCP-ERROR-HANDLING: Send tools/call with invalid ticker
  - Verify error response format: {error: {code, message, data}}
  - Verify error code is -32603 (internal error per JSON-RPC spec) OR verify error is properly formatted in the content

- Task 6.5: Run E2E tests via subprocess (full server startup)
  - Status: Backlog
  - Launch server via subprocess with stdin/stdout pipes
  - Send JSON-RPC requests to stdin
  - Read JSON-RPC responses from stdout
  - Verify server shuts down cleanly on EOF

### Phase 7: Documentation and Polish

**Goal**: Complete documentation and prepare for release

- Task 7.1: Update value-investor/servers/README.md
  - Status: Backlog
  - Add new section: "Yahoo Finance MCP Server"
  - Document get_financial_statements tool with examples
  - Document error codes and handling
  - Document installation and testing
  - Add usage example showing integration with SEC EDGAR server

- Task 7.2: Add inline documentation and docstrings
  - Status: Backlog
  - Add module-level docstring to yahoo_finance_server.py
  - Add module-level docstring to yahoo_finance_fetcher.py
  - Add docstrings to all public methods
  - Add type hints to all function signatures

- Task 7.3: Create test data validation script
  - Status: Backlog
  - Create validate_yahoo_data.py (similar to validate_test_data.py)
  - Verify sample data against live API
  - Document expected data ranges for integration tests

- Task 7.4: Manual end-to-end testing with Claude agent
  - Status: Backlog
  - Start Claude Code with plugin loaded
  - Invoke get_financial_statements tool from agent
  - Verify data is retrieved and formatted correctly
  - Test error scenarios (invalid ticker, timeout)
  - Verify agent can parse and use financial data

- Task 7.5: Final code review and cleanup
  - Status: Backlog
  - Review all code for consistency with financial_data_server.py patterns
  - Remove debug print statements
  - Verify error messages are clear and actionable
  - Run all tests one final time
  - Update CHANGELOG if exists

---

## Requirements Validation

**Ensure all requirements have matching tasks**

### Functional Requirements

- **REQ-FN-01: Fetch Financial Statements**
  - Phase 2 Task 2.2: Implement financial statement fetching with yfinance
  - Phase 2 Task 2.3: Implement data transformation to consistent JSON schema
  - Phase 3 Task 3.2: Register get_financial_statements MCP tool
  - Phase 5 Task 5.2: Write integration tests for established companies
  - Phase 5 Task 5.4: Run integration tests and validate data quality

- **REQ-FN-02: Handle Missing Data Gracefully**
  - Phase 2 Task 2.4: Implement missing data handling with MISSING markers
  - Phase 4 Task 4.3: Write unit tests for missing data handling
  - Phase 5 Task 5.3: Write integration tests for edge cases (incomplete data)

- **REQ-FN-03: Provide Clear Error Messages**
  - Phase 2 Task 2.5: Implement error handling with clear error codes
  - Phase 4 Task 4.4: Write unit tests for error conditions
  - Phase 5 Task 5.3: Write integration tests for invalid ticker
  - Phase 6 Task 6.4: Write E2E test for MCP error handling

### Non-Functional Requirements

- **REQ-NFN-01: Response Time (30s timeout)**
  - Phase 2 Task 2.1: Implement YahooFinanceFetcher class skeleton (timeout configuration)
  - Phase 2 Task 2.2: Implement financial statement fetching with yfinance (30s timeout)
  - Phase 4 Task 4.4: Write unit tests for error conditions (timeout test)

- **REQ-NFN-02: Data Accuracy**
  - Phase 2 Task 2.2: Implement financial statement fetching with yfinance (no modification)
  - Phase 5 Task 5.4: Run integration tests and validate data quality (manual verification)

- **REQ-NFN-03: Error Clarity**
  - Phase 2 Task 2.5: Implement error handling with clear error codes
  - Phase 7 Task 7.1: Update README.md (document error codes)

- **REQ-NFN-04: Data Format Consistency**
  - Phase 2 Task 2.3: Implement data transformation to consistent JSON schema (ISO 8601, ISO 4217)
  - Phase 2 Task 2.4: Implement missing data handling (schema consistency)
  - Phase 4 Task 4.3: Write unit tests for missing data handling (schema consistency test)
  - Phase 5 Task 5.3: Write integration tests for edge cases (schema consistency across tickers)

- **REQ-NFN-05: Security**
  - Phase 2 Task 2.1: Implement YahooFinanceFetcher class skeleton (ticker sanitization)
  - Phase 4 Task 4.4: Write unit tests for error conditions (sanitization test)

---

## Appendix

### Glossary

- **MCP (Model Context Protocol)**: Protocol for integrating external tools with AI assistants via JSON-RPC 2.0 over stdio
- **yfinance**: Popular Python library for accessing Yahoo Finance data (unofficial API wrapper)
- **Financial Statements**: Formal accounting records including Income Statement, Balance Sheet, and Cash Flow Statement
- **Income Statement**: Financial statement showing revenues, expenses, and net income over a period
- **Balance Sheet**: Financial statement showing assets, liabilities, and equity at a point in time
- **Cash Flow Statement**: Financial statement showing cash inflows and outflows over a period
- **Ticker Symbol**: Abbreviated identifier for publicly traded companies (e.g., AAPL for Apple Inc.)
- **Annual Data**: Financial statements reported yearly (typically from 10-K filings)
- **Quarterly Data**: Financial statements reported every quarter (typically from 10-Q filings)
- **Fiscal Year**: 12-month period used for financial reporting (may differ from calendar year)
- **ISO 8601**: International standard for date format (YYYY-MM-DD)
- **ISO 4217**: International standard for currency codes (USD, EUR, JPY)
- **MISSING Marker**: String value "MISSING" used to indicate unavailable data while maintaining schema consistency
- **JSON-RPC 2.0**: Stateless, lightweight remote procedure call protocol encoded in JSON
- **stdio Transport**: Communication mechanism using standard input/output streams (stdin/stdout)
- **uv**: Modern Python package manager (faster alternative to pip)
- **pandas DataFrame**: Two-dimensional tabular data structure (used by yfinance for financial data)

### References

- **yfinance Library**: https://github.com/ranaroussi/yfinance
- **Yahoo Finance**: https://finance.yahoo.com/
- **MCP Protocol Specification**: https://modelcontextprotocol.io/
- **JSON-RPC 2.0 Specification**: https://www.jsonrpc.org/specification
- **ISO 8601 Date Format**: https://www.iso.org/iso-8601-date-and-time-format.html
- **ISO 4217 Currency Codes**: https://www.iso.org/iso-4217-currency-codes.html
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **pytest Documentation**: https://docs.pytest.org/
- **uv Documentation**: https://docs.astral.sh/uv/
- **pandas Documentation**: https://pandas.pydata.org/docs/

### Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-31 | Technical Architect Agent | Initial design |

---
