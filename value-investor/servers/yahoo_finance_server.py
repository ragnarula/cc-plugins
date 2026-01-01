#!/usr/bin/env python3
"""
Yahoo Finance MCP Server

Provides financial statement data from Yahoo Finance via Model Context Protocol.

Tools:
- get_financial_statements: Fetch income statement, balance sheet, and cash flow statement for a company

MCP Protocol: https://spec.modelcontextprotocol.io/
"""

import asyncio
import json
import sys
import traceback
from typing import Any, Dict, List, Optional

from yahoo_finance_fetcher import YahooFinanceFetcher


class MCPServer:
    """Simple MCP server implementation using stdio transport."""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.tools = {}
        self.fetcher = YahooFinanceFetcher()

    def tool(self, name: str, description: str, parameters: Dict, required: Optional[List[str]] = None):
        """Register a tool."""

        def decorator(func):
            self.tools[name] = {
                "name": name,
                "description": description,
                "parameters": parameters,
                "required": required or [],
                "func": func,
            }
            return func

        return decorator

    async def handle_request(self, request: Dict) -> Dict:
        """Handle incoming MCP request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": self.name, "version": self.version},
                        "capabilities": {"tools": {}},
                    },
                }

            elif method == "tools/list":
                tools_list = []
                for tool_name, tool_info in self.tools.items():
                    tools_list.append(
                        {
                            "name": tool_info["name"],
                            "description": tool_info["description"],
                            "inputSchema": {
                                "type": "object",
                                "properties": tool_info["parameters"],
                                "required": tool_info.get("required", []),
                            },
                        }
                    )

                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools_list},
                }

            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})

                if tool_name not in self.tools:
                    raise ValueError(f"Unknown tool: {tool_name}")

                tool = self.tools[tool_name]
                result = await tool["func"](self, **tool_args)

                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": json.dumps(result, indent=2)}
                        ]
                    },
                }

            else:
                raise ValueError(f"Unknown method: {method}")

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e),
                    "data": {"traceback": traceback.format_exc()},
                },
            }

    async def run(self):
        """Run the MCP server on stdio."""
        while True:
            try:
                # Read request from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                if not line:
                    break

                request = json.loads(line)
                response = await self.handle_request(request)

                # Write response to stdout
                print(json.dumps(response), flush=True)

            except json.JSONDecodeError as e:
                sys.stderr.write(f"Invalid JSON: {e}\n")
                sys.stderr.flush()
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")
                sys.stderr.flush()


# Create server instance
server = MCPServer(name="yahoo-finance", version="0.1.0")


@server.tool(
    name="get_financial_statements",
    description="Fetch all three major financial statements (income statement, balance sheet, cash flow statement) for a given stock ticker. Returns up to 5 years of annual historical data and current fiscal year quarterly data. Data includes revenue, expenses, assets, liabilities, cash flows, and other key financial metrics. Missing data is marked with 'MISSING' string to maintain consistent schema.",
    parameters={
        "ticker": {
            "type": "string",
            "description": "Stock ticker symbol (e.g., 'AAPL', 'MSFT'). Must contain only letters, numbers, hyphens, and periods.",
        }
    },
    required=["ticker"],
)
async def get_financial_statements(self, ticker: str) -> Dict:
    """Fetch financial statements for value investing analysis."""
    try:
        result = self.fetcher.get_financial_statements(ticker)
        return result
    except Exception as e:
        return {"error": str(e), "ticker": ticker}


def main():
    """Run the MCP server."""
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        sys.stderr.write("Server stopped\n")
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Fatal error: {e}\n")
        sys.stderr.write(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
