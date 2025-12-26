# Financial Data MCP Server Setup

This directory contains the MCP (Model Context Protocol) server for fetching financial data from free APIs.

## Overview

The value-investor plugin uses an MCP server to access:
- SEC EDGAR filings (10-K, 10-Q, 8-K)
- Stock prices and historical data
- Financial metrics and ratios
- Company information

## Free Data Sources

### 1. SEC EDGAR API
- **URL**: https://www.sec.gov/edgar/sec-api-documentation
- **Authentication**: None required (rate limited)
- **Data**: Official SEC filings (10-K, 10-Q, 8-K, etc.)
- **Rate Limit**: 10 requests/second

### 2. Alpha Vantage API
- **URL**: https://www.alphavantage.co/
- **Authentication**: Free API key required
- **Data**: Stock prices, financial metrics, company overview
- **Rate Limit**: 25 requests/day (free tier)
- **Get Key**: https://www.alphavantage.co/support/#api-key

### 3. Yahoo Finance (via yfinance Python library)
- **Library**: yfinance
- **Authentication**: None required
- **Data**: Stock prices, financial statements, company info
- **Rate Limit**: Reasonable use

## Installation

### Prerequisites

```bash
# Install Node.js (if not installed)
# macOS:
brew install node

# Install Python 3 (if not installed)
# macOS:
brew install python3

# Install required Python libraries
pip3 install yfinance requests pandas
```

### Configuration

1. **Get API Keys** (optional but recommended):
   - Alpha Vantage: https://www.alphavantage.co/support/#api-key
   - No key needed for SEC EDGAR or Yahoo Finance

2. **Set Environment Variables**:
   ```bash
   export ALPHA_VANTAGE_API_KEY="your-key-here"
   ```

   Or add to your `.claude/value-investor.local.md` settings file.

3. **Update .mcp.json**:
   The plugin's `.mcp.json` is pre-configured to use the financial data server.

## MCP Server Implementation

The MCP server provides these tools:

### Available Tools

**1. `get_sec_filing`**
- Fetches SEC filings (10-K, 10-Q, etc.) for a company
- Parameters: ticker, filing_type, year (optional)
- Returns: Filing content or URL

**2. `get_stock_price`**
- Gets current or historical stock prices
- Parameters: ticker, start_date (optional), end_date (optional)
- Returns: Price data

**3. `get_financials`**
- Retrieves financial statements
- Parameters: ticker, statement_type (income, balance, cash_flow)
- Returns: Financial data as JSON

**4. `get_company_info`**
- Gets company overview and metrics
- Parameters: ticker
- Returns: Company description, sector, metrics

**5. `search_company`**
- Searches for company by name
- Parameters: company_name
- Returns: Ticker symbol and basic info

## Usage in Plugin

The agents (business-screener, financial-analyzer, etc.) automatically use these MCP tools when needed:

```python
# Example: Agent fetches 10-K
result = use_tool("get_sec_filing", {
    "ticker": "AAPL",
    "filing_type": "10-K"
})

# Example: Agent gets historical financials
financials = use_tool("get_financials", {
    "ticker": "AAPL",
    "statement_type": "income"
})
```

## Development Status

**Current Status**: Documentation and placeholder

**To Complete**:
1. Implement `servers/financial-data-server.js` or `.py`
2. Implement MCP protocol handlers
3. Add data fetching logic for each tool
4. Add error handling and rate limiting
5. Test with Claude Code

**Alternative**: Until MCP server is fully implemented, agents can use WebSearch and WebFetch tools to access SEC EDGAR and financial data websites directly.

## Quick Start for Development

### Option 1: Node.js Implementation

```javascript
// servers/financial-data-server.js
const { MCPServer } = require('@anthropic/mcp-sdk');

const server = new MCPServer({
  name: 'financial-data',
  version: '0.1.0'
});

// Register tools
server.tool('get_sec_filing', async ({ ticker, filing_type }) => {
  // Fetch from SEC EDGAR
  // Implementation here
});

server.tool('get_stock_price', async ({ ticker, start_date, end_date }) => {
  // Fetch from Yahoo Finance or Alpha Vantage
  // Implementation here
});

// More tools...

server.start();
```

### Option 2: Python Implementation

```python
# servers/financial-data-server.py
from mcp.server import MCPServer
import yfinance as yf
import requests

server = MCPServer(name="financial-data", version="0.1.0")

@server.tool("get_sec_filing")
async def get_sec_filing(ticker: str, filing_type: str):
    # Fetch from SEC EDGAR API
    pass

@server.tool("get_stock_price")
async def get_stock_price(ticker: str, start_date: str = None, end_date: str = None):
    # Use yfinance
    stock = yf.Ticker(ticker)
    return stock.history(start=start_date, end=end_date)

# More tools...

if __name__ == "__main__":
    server.run()
```

## Fallback: Direct API Access

Until MCP server is implemented, agents use WebSearch/WebFetch:

```markdown
To get SEC 10-K:
- Search: "SEC EDGAR [ticker] 10-K"
- Or visit: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=[ticker]&type=10-K

To get stock price:
- Search: "Yahoo Finance [ticker]"
- Or use yfinance library via Bash tool

To get financials:
- Use Alpha Vantage API via WebFetch
- Or parse from SEC filings
```

## Testing

```bash
# Test SEC EDGAR access
curl "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=AAPL&type=10-K&dateb=&owner=exclude&count=10&output=atom"

# Test Alpha Vantage (replace YOUR_API_KEY)
curl "https://www.alphavantage.co/query?function=OVERVIEW&symbol=AAPL&apikey=YOUR_API_KEY"

# Test yfinance
python3 -c "import yfinance as yf; print(yf.Ticker('AAPL').info)"
```

## Resources

- MCP SDK Documentation: https://github.com/anthropics/anthropic-sdk-typescript
- SEC EDGAR API: https://www.sec.gov/edgar/sec-api-documentation
- Alpha Vantage: https://www.alphavantage.co/documentation/
- yfinance: https://github.com/ranaroussi/yfinance

## Future Enhancements

- Implement full MCP server
- Add caching to reduce API calls
- Add rate limiting and retry logic
- Support additional data sources (Financial Modeling Prep, Polygon.io)
- Add company financials database for offline access
- Implement data normalization and cleaning
