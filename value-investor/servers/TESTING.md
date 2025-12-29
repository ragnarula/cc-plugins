# Testing Guide

Comprehensive testing documentation for the Value Investor MCP Server.

## Quick Start

```bash
# Install dependencies
uv sync --extra dev

# Run all tests
uv run pytest

# Run only fast tests (skip agent tests)
uv run pytest -m "not agent"

# Run specific test categories
uv run pytest -m unit           # Unit tests only (0.05s)
uv run pytest -m integration    # Integration tests only (1.7s)
uv run pytest -m agent          # Agent tests only (slow, requires API key)
```

## Test Structure

```
servers/
├── tests/
│   ├── conftest.py                   # Shared fixtures
│   ├── unit/
│   │   └── test_html_cleaner.py      # HTMLCleaner unit tests (25 tests)
│   ├── integration/
│   │   └── test_filing_processing.py # Filing processing tests (11 tests)
│   └── agents/
│       └── test_business_screener.py # Agent parsing tests (4 tests)
├── test_data/
│   └── fixtures/                     # Downloaded SEC filings
│       ├── metadata.json             # Filing index
│       ├── AAPL/
│       │   ├── 10-K_2025-10-31.html
│       │   ├── 10-K_2025-10-31_cleaned.html
│       │   └── ...
│       └── MSFT/
│           └── ...
└── tests/deprecated/                  # Archived old scripts
    ├── test_mcp.py
    ├── test_html_cleaning.py
    └── test_mcp_server.sh
```

## Test Categories

### Unit Tests (25 tests, ~0.05s)
Fast, isolated tests with no I/O or external dependencies.

**What they test:**
- HTML tag removal (style, script, class, id attributes)
- Tag unwrapping (font, span, bold, italic)
- Structure preservation (headings, tables, lists)
- Empty tag removal
- Text extraction
- Configuration options

**Run:**
```bash
uv run pytest -m unit -v
```

### Integration Tests (11 tests, ~1.7s)
Tests using real SEC filing test data.

**What they test:**
- Cleaning preserves table structure
- Scripts and styles are removed
- Significant size reduction achieved (50%+)
- Company names preserved
- Content not empty
- Different filing types (10-K, 10-Q)
- Cross-company consistency

**Run:**
```bash
uv run pytest -m integration -v
```

### Agent Tests (4 tests, ~30s each, requires API key)
Tests business-screener agent parsing capabilities.

**What they test:**
- Agent understands Apple 10-K
- Agent understands Microsoft 10-K
- Agent handles quarterly 10-Q filings
- Agent provides business context

**Requirements:**
- `ANTHROPIC_API_KEY` environment variable set
- Claude API credits (uses Sonnet 4.5)

**Run:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
uv run pytest -m agent -v
```

**Skip agent tests:**
```bash
uv run pytest -m "not agent"
```

## Test Data Management

### Download Test Data

Initial download of SEC filings:

```bash
uv run python download_test_data.py
```

This downloads:
- AAPL 10-K, 10-Q
- MSFT 10-K, 10-Q
- Additional filings as configured

**Output:**
- `test_data/fixtures/` directory created
- Original HTML files saved
- Cleaned HTML files generated
- `metadata.json` index file

### Validate Test Data

Check integrity of test data:

```bash
uv run python validate_test_data.py
```

Validates:
- All files exist
- File sizes match metadata
- Cleaned versions present
- Provides statistics

### Add New Test Filings

Edit `download_test_data.py`:

```python
TEST_FILINGS = [
    # Add new entry: (ticker, filing_type, years, limit)
    ('GOOGL', '10-K', 1, 1),
]
```

Then run:
```bash
uv run python download_test_data.py
uv run python validate_test_data.py
```

## Inspection Tools

### Compare Filings

Compare original vs cleaned HTML:

```bash
# Show statistics
uv run python compare_filings.py test_data/fixtures/AAPL/10-K_2025-10-31.html --mode stats

# Show diff (first 100 lines)
uv run python compare_filings.py test_data/fixtures/AAPL/10-K_2025-10-31.html --mode diff

# Open in browser
uv run python compare_filings.py test_data/fixtures/AAPL/10-K_2025-10-31.html --mode preview
```

**Stats mode output:**
- Original vs cleaned size
- Size reduction percentage
- Compression ratio
- Tag counts
- Removed/preserved elements

## Continuous Integration

### Recommended CI Workflow

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync --extra dev

      - name: Run unit tests
        run: uv run pytest -m unit

      - name: Run integration tests
        run: uv run pytest -m integration

      # Skip agent tests in CI (require API key)
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running fast tests..."
uv run pytest -m "unit or integration" --tb=short

if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

## Debugging Test Failures

### Verbose Output

```bash
uv run pytest -vv                    # Very verbose
uv run pytest --tb=long              # Full tracebacks
uv run pytest -s                     # Show print statements
uv run pytest -x                     # Stop on first failure
```

### Run Specific Tests

```bash
# By file
uv run pytest tests/unit/test_html_cleaner.py

# By class
uv run pytest tests/unit/test_html_cleaner.py::TestHTMLCleanerBasics

# By test name
uv run pytest tests/unit/test_html_cleaner.py::TestHTMLCleanerBasics::test_remove_style_tags

# By pattern
uv run pytest -k "style"             # Run tests matching "style"
```

### Common Issues

**Test data not found:**
```
SKIPPED: Test data not found. Run download_test_data.py first.
```
Solution: Run `uv run python download_test_data.py`

**ANTHROPIC_API_KEY not set:**
```
SKIPPED: ANTHROPIC_API_KEY not set - required for agent tests
```
Solution: Export API key or skip agent tests with `-m "not agent"`

**File size mismatches:**
Minor size differences (<1%) are normal due to encoding. Re-download if needed.

## Test Coverage

### Current Coverage

| Category | Tests | Runtime | Status |
|----------|-------|---------|--------|
| Unit | 25 | 0.05s | ✅ Passing |
| Integration | 11 | 1.73s | ✅ Passing |
| Agent | 4 | ~120s | ⚠️ Requires API key |
| **Total** | **40** | **~122s** | **36 passing** |

### Coverage Goals

- [x] HTML cleaning functionality
- [x] Real filing processing
- [x] Cross-company consistency
- [x] Agent parsing validation
- [ ] MCP protocol compliance (future)
- [ ] Error handling edge cases (future)

## Best Practices

### Writing New Tests

1. **Choose the right marker:**
   - `@pytest.mark.unit` - Fast, no I/O
   - `@pytest.mark.integration` - Uses test data
   - `@pytest.mark.agent` - Uses Claude API

2. **Use fixtures from conftest.py:**
   ```python
   def test_example(html_cleaner, filings_by_type):
       # html_cleaner: HTMLCleaner instance
       # filings_by_type: Dict of filings grouped by type
   ```

3. **Add descriptive docstrings:**
   ```python
   def test_clean_preserves_tables(self, html_cleaner):
       """Tables are critical for financial statements."""
   ```

4. **Use clear assertions:**
   ```python
   assert '<table>' in cleaned, \
       f"Table structure lost in {filing['ticker']}"
   ```

### Maintaining Test Data

- Keep test data small (< 10 filings)
- Cover diverse filing types (10-K, 10-Q, DEF 14A)
- Use recent filings (< 1 year old)
- Refresh annually or when format changes

## Performance Benchmarks

| Operation | Time | Notes |
|-----------|------|-------|
| Clean 1.5MB filing | ~0.3s | AAPL 10-K |
| Clean 7.8MB filing | ~1.2s | MSFT 10-K |
| Unit test suite | 0.05s | 25 tests |
| Integration suite | 1.73s | 11 tests |
| Agent test (1 filing) | ~30s | Includes API latency |

## Troubleshooting

### Tests run but skip agent tests

**Expected behavior.** Agent tests require `ANTHROPIC_API_KEY` environment variable.

### Integration tests fail with "Test data not found"

Run `download_test_data.py` to create test fixtures.

### Download script fails with timeout errors

SEC EDGAR API can be slow. Script respects rate limits (10 req/sec). Retry or reduce number of filings.

### Agent tests timeout

Increase timeout in test or reduce filing content size (currently limited to 50K chars).

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [SEC EDGAR API](https://www.sec.gov/edgar/sec-api-documentation)
- [BeautifulSoup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Anthropic API documentation](https://docs.anthropic.com/)

## Support

For issues or questions:
1. Check test output with `-vv` flag
2. Verify test data exists
3. Check environment variables
4. Review test logs

Old test scripts archived in `tests/deprecated/` for reference.
