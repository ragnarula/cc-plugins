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
