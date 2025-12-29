#!/bin/bash
# Test script for MCP server

cd "$(dirname "$0")"

echo "Testing MCP Server..."
echo ""

# Test 1: Initialize
echo "=== Test 1: Initialize ==="
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | uv run python financial_data_server.py
echo ""

# Test 2: List tools
echo "=== Test 2: List Tools ==="
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | uv run python financial_data_server.py
echo ""

# Test 3: Fetch SEC filings for AAPL
echo "=== Test 3: Fetch SEC Filings (AAPL, 10-K only, last 3 years) ==="
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"fetch_sec_filings","arguments":{"ticker":"AAPL","filing_types":["10-K"],"years":3}}}' | uv run python financial_data_server.py
echo ""

# Test 4: List filing types
echo "=== Test 4: List Filing Types ==="
echo '{"jsonrpc":"2.0","id":4,"method":"tools/list_filing_types","params":{"name":"list_filing_types","arguments":{}}}' | uv run python financial_data_server.py
echo ""

echo "Tests complete!"
