#!/usr/bin/env python3
"""
Test script for MCP server

This script tests the financial data MCP server by sending JSON-RPC requests
and displaying the responses.
"""

import subprocess
import json
import sys


def send_mcp_request(method: str, params: dict = None, request_id: int = 1):
    """Send a JSON-RPC request to the MCP server."""
    request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params or {}
    }

    # Start the MCP server
    process = subprocess.Popen(
        ["uv", "run", "python", "financial_data_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send request
    request_json = json.dumps(request) + "\n"
    stdout, stderr = process.communicate(input=request_json, timeout=30)

    if stderr:
        print(f"STDERR: {stderr}", file=sys.stderr)

    # Parse response
    try:
        response = json.loads(stdout.strip())
        return response
    except json.JSONDecodeError as e:
        print(f"Failed to parse response: {e}", file=sys.stderr)
        print(f"Raw output: {stdout}", file=sys.stderr)
        return None


def test_initialize():
    """Test server initialization."""
    print("=" * 60)
    print("TEST 1: Initialize Server")
    print("=" * 60)

    response = send_mcp_request("initialize")
    if response:
        print(json.dumps(response, indent=2))
        print("✓ Server initialized successfully\n")
    else:
        print("✗ Initialization failed\n")


def test_list_tools():
    """Test listing available tools."""
    print("=" * 60)
    print("TEST 2: List Available Tools")
    print("=" * 60)

    response = send_mcp_request("tools/list")
    if response and "result" in response:
        tools = response["result"].get("tools", [])
        print(f"Found {len(tools)} tools:\n")
        for tool in tools:
            print(f"  • {tool['name']}")
            print(f"    {tool['description']}\n")
        print("✓ Tools listed successfully\n")
    else:
        print("✗ Failed to list tools\n")


def test_fetch_filings():
    """Test fetching SEC filings."""
    print("=" * 60)
    print("TEST 3: Fetch SEC Filings (AAPL, 10-K, last 3 years)")
    print("=" * 60)

    response = send_mcp_request(
        "tools/call",
        {
            "name": "fetch_sec_filings",
            "arguments": {
                "ticker": "AAPL",
                "filing_types": ["10-K"],
                "years": 3
            }
        }
    )

    if response and "result" in response:
        result_text = response["result"]["content"][0]["text"]
        result_data = json.loads(result_text)

        print(f"Ticker: {result_data.get('ticker')}")
        print(f"Total filings found: {result_data.get('total_filings_found')}")
        print(f"\nFilings:")

        for filing_type, filings in result_data.get("filings", {}).items():
            print(f"\n  {filing_type}: {len(filings)} filings")
            for filing in filings[:3]:  # Show first 3
                print(f"    - {filing['filingDate']}: {filing['primaryDocUrl'][:80]}...")

        print("\n✓ Filings fetched successfully\n")
    else:
        print("✗ Failed to fetch filings\n")


def test_list_filing_types():
    """Test listing available filing types."""
    print("=" * 60)
    print("TEST 4: List Filing Types")
    print("=" * 60)

    response = send_mcp_request(
        "tools/call",
        {
            "name": "list_filing_types",
            "arguments": {}
        }
    )

    if response and "result" in response:
        result_text = response["result"]["content"][0]["text"]
        result_data = json.loads(result_text)

        recommended = result_data.get("recommended_for_value_investing", [])
        print(f"Recommended filing types for value investing:")
        for filing_type in recommended:
            print(f"  • {filing_type}")

        print("\n✓ Filing types listed successfully\n")
    else:
        print("✗ Failed to list filing types\n")


def test_get_filing_content():
    """Test fetching actual filing content."""
    print("=" * 60)
    print("TEST 5: Get Filing Content (Latest AAPL 10-K)")
    print("=" * 60)

    # First, get the latest 10-K URL
    print("Step 1: Fetching filing metadata...")
    filings_response = send_mcp_request(
        "tools/call",
        {
            "name": "fetch_sec_filings",
            "arguments": {
                "ticker": "AAPL",
                "filing_types": ["10-K"],
                "years": 1,
                "limit_per_type": 1
            }
        },
        request_id=5
    )

    if not filings_response or "result" not in filings_response:
        print("✗ Failed to fetch filing metadata\n")
        return

    result_text = filings_response["result"]["content"][0]["text"]
    result_data = json.loads(result_text)

    if not result_data.get("filings", {}).get("10-K"):
        print("✗ No 10-K filings found\n")
        return

    filing_url = result_data["filings"]["10-K"][0]["primaryDocUrl"]
    filing_date = result_data["filings"]["10-K"][0]["filingDate"]

    print(f"Step 2: Fetching content from {filing_date}...")
    print(f"URL: {filing_url}")

    # Now fetch the actual content
    content_response = send_mcp_request(
        "tools/call",
        {
            "name": "get_filing_content",
            "arguments": {
                "url": filing_url,
                "extract_text": True  # Get plain text, not HTML
            }
        },
        request_id=6
    )

    if content_response and "result" in content_response:
        content_text = content_response["result"]["content"][0]["text"]
        content_data = json.loads(content_text)

        if "error" in content_data:
            print(f"✗ Error fetching content: {content_data['error']}\n")
            return

        content_length = content_data.get("content_length", 0)
        content_type = content_data.get("content_type", "unknown")
        content_preview = content_data.get("content", "")[:500]

        print(f"\nFiling content retrieved:")
        print(f"  Content type: {content_type}")
        print(f"  Content length: {content_length:,} characters")
        print(f"\nFirst 500 characters:")
        print("-" * 60)
        print(content_preview)
        print("-" * 60)

        print("\n✓ Filing content fetched successfully\n")
    else:
        print("✗ Failed to fetch filing content\n")


def main():
    """Run all tests."""
    print("\n🧪 Testing MCP Server for Value Investor Plugin\n")

    try:
        test_initialize()
        test_list_tools()
        test_fetch_filings()
        test_list_filing_types()
        test_get_filing_content()

        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
