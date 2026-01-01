"""
End-to-end tests for Yahoo Finance MCP server protocol compliance.

Tests the full MCP server lifecycle including:
- Server initialization via subprocess
- JSON-RPC protocol compliance
- Tool registration and discovery
- Tool execution with real data
- Error handling and responses

These tests launch the server as a subprocess and communicate via stdin/stdout
to verify real-world MCP protocol behavior.

Run with: pytest -m e2e tests/e2e/test_yahoo_finance_mcp.py -v
"""

import json
import subprocess
import sys
from pathlib import Path
import pytest


@pytest.fixture
def server_path():
    """Path to the Yahoo Finance MCP server script."""
    return Path(__file__).parent.parent.parent / "yahoo_finance_server.py"


@pytest.fixture
def server_process(server_path):
    """
    Launch Yahoo Finance MCP server as subprocess.

    Yields a process with stdin/stdout pipes for communication.
    Automatically cleans up the process after the test.
    """
    process = subprocess.Popen(
        [sys.executable, str(server_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    yield process

    # Cleanup: close stdin to signal EOF and wait for server to exit
    try:
        process.stdin.close()
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def send_request(process, method, params=None, request_id=1):
    """
    Send a JSON-RPC request to the MCP server.

    Args:
        process: subprocess.Popen instance
        method: JSON-RPC method name
        params: Optional parameters dict
        request_id: Request ID (default: 1)

    Returns:
        dict: Parsed JSON-RPC response
    """
    request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
    }
    if params is not None:
        request["params"] = params

    # Send request
    request_line = json.dumps(request) + "\n"
    process.stdin.write(request_line)
    process.stdin.flush()

    # Read response
    response_line = process.stdout.readline()
    if not response_line:
        raise RuntimeError("Server closed stdout without sending response")

    return json.loads(response_line)


@pytest.mark.e2e
class TestMCPInitialize:
    """Test MCP initialize protocol."""

    def test_initialize_response_structure(self, server_process):
        """TEST-MCP-INITIALIZE: Send initialize request, verify server info response."""
        response = send_request(
            server_process,
            method="initialize",
            params={"protocolVersion": "2024-11-05", "capabilities": {}}
        )

        # Verify JSON-RPC structure
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response
        assert "error" not in response

        result = response["result"]

        # Verify protocolVersion field present
        assert "protocolVersion" in result, "Missing protocolVersion in initialize response"
        assert isinstance(result["protocolVersion"], str)
        assert len(result["protocolVersion"]) > 0

        # Verify serverInfo contains name and version
        assert "serverInfo" in result, "Missing serverInfo in initialize response"
        server_info = result["serverInfo"]

        assert "name" in server_info, "Missing name in serverInfo"
        assert server_info["name"] == "yahoo-finance"

        assert "version" in server_info, "Missing version in serverInfo"
        assert isinstance(server_info["version"], str)
        assert len(server_info["version"]) > 0

        # Verify capabilities present
        assert "capabilities" in result


@pytest.mark.e2e
class TestMCPToolsList:
    """Test MCP tools/list protocol."""

    def test_tools_list_response_structure(self, server_process):
        """TEST-MCP-TOOLS-LIST: Send tools/list request, verify get_financial_statements tool."""
        # Initialize server first
        send_request(
            server_process,
            method="initialize",
            params={"protocolVersion": "2024-11-05", "capabilities": {}}
        )

        # Send tools/list request
        response = send_request(
            server_process,
            method="tools/list",
            request_id=2
        )

        # Verify JSON-RPC structure
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert "result" in response
        assert "error" not in response

        result = response["result"]

        # Verify tools array present
        assert "tools" in result, "Missing tools array in tools/list response"
        tools = result["tools"]
        assert isinstance(tools, list), "tools should be an array"
        assert len(tools) > 0, "tools array should not be empty"

        # Verify get_financial_statements tool is in response
        tool_names = [tool["name"] for tool in tools]
        assert "get_financial_statements" in tool_names, \
            "get_financial_statements tool not found in tools/list"

        # Find the get_financial_statements tool
        financial_tool = next(
            (tool for tool in tools if tool["name"] == "get_financial_statements"),
            None
        )
        assert financial_tool is not None

        # Verify tool has name, description, inputSchema
        assert "name" in financial_tool, "Tool missing name field"
        assert financial_tool["name"] == "get_financial_statements"

        assert "description" in financial_tool, "Tool missing description field"
        assert isinstance(financial_tool["description"], str)
        assert len(financial_tool["description"]) > 0, "Tool description should not be empty"

        assert "inputSchema" in financial_tool, "Tool missing inputSchema field"
        input_schema = financial_tool["inputSchema"]

        # Verify inputSchema structure
        assert "type" in input_schema
        assert input_schema["type"] == "object"

        assert "properties" in input_schema
        properties = input_schema["properties"]

        # Verify ticker parameter exists
        assert "ticker" in properties, "Missing ticker parameter in inputSchema"
        ticker_param = properties["ticker"]
        assert "type" in ticker_param
        assert ticker_param["type"] == "string"
        assert "description" in ticker_param

        # Verify required parameters
        assert "required" in input_schema
        assert "ticker" in input_schema["required"]


@pytest.mark.e2e
class TestMCPToolCall:
    """Test MCP tools/call protocol."""

    def test_tool_call_success(self, server_process):
        """TEST-MCP-TOOL-CALL: Send tools/call request with ticker=AAPL, verify response."""
        # Initialize server first
        send_request(
            server_process,
            method="initialize",
            params={"protocolVersion": "2024-11-05", "capabilities": {}}
        )

        # Send tools/call request for AAPL
        response = send_request(
            server_process,
            method="tools/call",
            params={
                "name": "get_financial_statements",
                "arguments": {"ticker": "AAPL"}
            },
            request_id=2
        )

        # Verify JSON-RPC structure
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert "result" in response, f"Expected result, got: {response}"
        assert "error" not in response

        result = response["result"]

        # Verify response format: {content: [{type: "text", text: JSON}]}
        assert "content" in result, "Missing content field in tools/call response"
        content = result["content"]
        assert isinstance(content, list), "content should be an array"
        assert len(content) > 0, "content array should not be empty"

        # Verify first content item
        content_item = content[0]
        assert "type" in content_item
        assert content_item["type"] == "text"

        assert "text" in content_item
        text = content_item["text"]
        assert isinstance(text, str), "text should be a string"

        # Parse the JSON from the text field
        data = json.loads(text)

        # Verify financial data structure
        assert "ticker" in data or "error" not in data, \
            "Response should contain financial data or no error"

        # If no error, verify it's financial data for AAPL
        if "error" not in data:
            assert data["ticker"] == "AAPL"
            assert "currency" in data
            assert "statements" in data

            statements = data["statements"]
            assert "income_statement" in statements
            assert "balance_sheet" in statements
            assert "cash_flow" in statements


@pytest.mark.e2e
class TestMCPErrorHandling:
    """Test MCP error handling for invalid inputs."""

    def test_invalid_ticker_error_response(self, server_process):
        """TEST-MCP-ERROR-HANDLING: Send tools/call with invalid ticker, verify error response."""
        # Initialize server first
        send_request(
            server_process,
            method="initialize",
            params={"protocolVersion": "2024-11-05", "capabilities": {}}
        )

        # Send tools/call request with invalid ticker
        response = send_request(
            server_process,
            method="tools/call",
            params={
                "name": "get_financial_statements",
                "arguments": {"ticker": "INVALID999"}
            },
            request_id=2
        )

        # Verify JSON-RPC structure
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2

        # The design says errors can be in two formats:
        # 1. JSON-RPC error: {error: {code, message, data}}
        # 2. Content with error: {content: [{type: "text", text: JSON with error field}]}

        # Check if it's a JSON-RPC error response
        if "error" in response:
            # Format: {error: {code, message, data}}
            error = response["error"]
            assert "code" in error, "Error missing code field"
            assert "message" in error, "Error missing message field"

            # Verify error code is -32603 (internal error per JSON-RPC spec)
            assert error["code"] == -32603, \
                f"Expected error code -32603, got {error['code']}"

            # Message should be informative
            assert len(error["message"]) > 0, "Error message should not be empty"

        # Otherwise, check if error is in content
        elif "result" in response:
            result = response["result"]
            assert "content" in result
            content = result["content"]
            assert len(content) > 0

            content_item = content[0]
            assert content_item["type"] == "text"

            # Parse the JSON from text
            data = json.loads(content_item["text"])

            # Should have error field
            assert "error" in data, "Expected error field in response data"
            error = data["error"]

            # Verify error has required fields
            assert "code" in error, "Error missing code field"
            assert "message" in error, "Error missing message field"
            assert "ticker" in error or "ticker" in data, \
                "Error should include ticker information"

            # Message should be informative
            assert len(error["message"]) > 0, "Error message should not be empty"

            # Error code should indicate the problem
            assert error["code"] in [
                "TICKER_NOT_FOUND",
                "DATA_UNAVAILABLE",
                "INVALID_TICKER_FORMAT"
            ], f"Unexpected error code: {error['code']}"
