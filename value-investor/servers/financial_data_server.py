#!/usr/bin/env python3
"""
Financial Data MCP Server

Provides SEC EDGAR filing data and financial information via Model Context Protocol.

Tools:
- fetch_sec_filings: Fetch SEC filings (10-K, 10-Q, etc.) for a company
- get_filing_content: Get full text of a specific filing
- list_filing_types: List available SEC filing types for value investing

MCP Protocol: https://spec.modelcontextprotocol.io/
"""

import sys
import json
import asyncio
from typing import Any, Dict, List, Optional
import traceback

from sec_edgar_fetcher import SECEdgarFetcher, FilingType


class MCPServer:
    """Simple MCP server implementation using stdio transport."""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.tools = {}
        self.fetcher = SECEdgarFetcher()

    def tool(self, name: str, description: str, parameters: Dict):
        """Register a tool."""
        def decorator(func):
            self.tools[name] = {
                "name": name,
                "description": description,
                "parameters": parameters,
                "func": func
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
                        "serverInfo": {
                            "name": self.name,
                            "version": self.version
                        },
                        "capabilities": {
                            "tools": {}
                        }
                    }
                }

            elif method == "tools/list":
                tools_list = []
                for tool_name, tool_info in self.tools.items():
                    tools_list.append({
                        "name": tool_info["name"],
                        "description": tool_info["description"],
                        "inputSchema": {
                            "type": "object",
                            "properties": tool_info["parameters"],
                            "required": tool_info.get("required", [])
                        }
                    })

                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": tools_list
                    }
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
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
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
                    "data": {
                        "traceback": traceback.format_exc()
                    }
                }
            }

    async def run(self):
        """Run the MCP server on stdio."""
        while True:
            try:
                # Read request from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
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
server = MCPServer(name="financial-data", version="0.1.0")


@server.tool(
    name="fetch_sec_filings",
    description="Fetch SEC filings for a company. Supports 10-K (annual), 10-Q (quarterly), 8-K (current events), DEF 14A (proxy), 13F (institutional holdings), and other filing types. Returns metadata and URLs for up to 10 years of historical filings.",
    parameters={
        "ticker": {
            "type": "string",
            "description": "Stock ticker symbol (e.g., 'AAPL', 'MSFT')"
        },
        "filing_types": {
            "type": "array",
            "description": "List of filing types to fetch. For value investing, recommended: ['10-K', '10-Q', 'DEF 14A', '8-K']",
            "items": {
                "type": "string",
                "enum": ["10-K", "10-Q", "8-K", "DEF 14A", "13F", "SC 13D", "SC 13G", "S-1", "S-3"]
            },
            "default": ["10-K", "10-Q"]
        },
        "years": {
            "type": "integer",
            "description": "Number of years of historical data to fetch (default: 10, max: 10)",
            "default": 10,
            "minimum": 1,
            "maximum": 10
        },
        "limit_per_type": {
            "type": "integer",
            "description": "Maximum number of filings per type (optional, default: all within years)",
            "default": None
        }
    }
)
async def fetch_sec_filings(
    self,
    ticker: str,
    filing_types: List[str] = None,
    years: int = 10,
    limit_per_type: Optional[int] = None
) -> Dict:
    """Fetch SEC filings for value investing analysis."""
    if filing_types is None:
        filing_types = ["10-K", "10-Q"]

    # Validate years
    if years < 1 or years > 10:
        years = 10

    try:
        filings = self.fetcher.fetch_filings(
            ticker=ticker,
            filing_types=filing_types,
            years=years,
            limit_per_type=limit_per_type
        )

        # Add summary statistics
        total_filings = sum(len(filing_list) for filing_list in filings.values())

        result = {
            "ticker": ticker.upper(),
            "filing_types_requested": filing_types,
            "years": years,
            "total_filings_found": total_filings,
            "filings": filings,
            "summary": {
                filing_type: len(filing_list)
                for filing_type, filing_list in filings.items()
            }
        }

        return result

    except Exception as e:
        return {
            "error": str(e),
            "ticker": ticker,
            "filing_types": filing_types
        }


@server.tool(
    name="get_filing_content",
    description="Fetch the full text content of a specific SEC filing. Use this after fetch_sec_filings to retrieve the actual filing document for analysis.",
    parameters={
        "url": {
            "type": "string",
            "description": "URL to the filing document (use primaryDocUrl from fetch_sec_filings result)"
        },
        "extract_text": {
            "type": "boolean",
            "description": "If true, strip ALL HTML tags and return plain text (default: false)",
            "default": False
        },
        "clean_html": {
            "type": "boolean",
            "description": "If true, return cleaned HTML with structure preserved but styling removed (recommended). Removes CSS, scripts, presentational attributes while keeping headings, tables, lists, etc. Significantly reduces file size. (default: false)",
            "default": False
        }
    }
)
async def get_filing_content(self, url: str, extract_text: bool = False, clean_html: bool = False) -> Dict:
    """Fetch full content of a SEC filing."""
    try:
        if extract_text:
            content = self.fetcher.get_filing_text(url)
            content_type = "text/plain"
        elif clean_html:
            content = self.fetcher.get_filing_content_clean(url)
            content_type = "text/html (cleaned)"
        else:
            content = self.fetcher.get_filing_content(url)
            content_type = "text/html"

        return {
            "url": url,
            "content_length": len(content),
            "content_type": content_type,
            "content": content
        }

    except Exception as e:
        return {
            "error": str(e),
            "url": url
        }


@server.tool(
    name="list_filing_types",
    description="List available SEC filing types with descriptions for value investing. Use this to understand which filings to request for different analysis scenarios.",
    parameters={}
)
async def list_filing_types(self) -> Dict:
    """List available SEC filing types for value investing."""
    return {
        "filing_types": {
            "10-K": {
                "name": "Annual Report",
                "description": "Comprehensive annual report with full financial statements, MD&A, risk factors, and business description. Essential for value investing.",
                "frequency": "Annual",
                "importance": "Critical",
                "use_cases": [
                    "Understanding business model and competitive position",
                    "Analyzing 5-10 year financial history",
                    "Identifying risk factors and contingencies",
                    "Evaluating management discussion and analysis"
                ]
            },
            "10-Q": {
                "name": "Quarterly Report",
                "description": "Quarterly financial statements and updates. Use to track recent trends and performance.",
                "frequency": "Quarterly (3 per year)",
                "importance": "High",
                "use_cases": [
                    "Tracking quarterly revenue and earnings trends",
                    "Monitoring working capital changes",
                    "Identifying recent business developments"
                ]
            },
            "8-K": {
                "name": "Current Report",
                "description": "Material events and corporate changes (acquisitions, executive changes, earnings releases, debt agreements).",
                "frequency": "As needed",
                "importance": "High",
                "use_cases": [
                    "Identifying major corporate events and changes",
                    "Tracking acquisitions and divestitures",
                    "Monitoring management changes",
                    "Understanding debt restructuring"
                ]
            },
            "DEF 14A": {
                "name": "Proxy Statement",
                "description": "Executive compensation, board composition, shareholder proposals, and governance. Critical for assessing management alignment.",
                "frequency": "Annual",
                "importance": "High",
                "use_cases": [
                    "Evaluating executive compensation structure",
                    "Assessing management incentive alignment",
                    "Understanding board composition and independence",
                    "Reviewing shareholder proposals"
                ]
            },
            "13F": {
                "name": "Institutional Holdings",
                "description": "Quarterly holdings of institutional investors ($100M+ AUM). Follow what great investors own.",
                "frequency": "Quarterly",
                "importance": "Medium",
                "use_cases": [
                    "Following Buffett, Munger, and other great investors",
                    "Identifying institutional interest in a stock",
                    "Tracking position changes by top investors"
                ]
            },
            "SC 13D": {
                "name": "Beneficial Ownership (Active)",
                "description": "5%+ ownership with intent to influence control. Indicates activist investor interest.",
                "frequency": "As needed",
                "importance": "Medium",
                "use_cases": [
                    "Identifying activist investor positions",
                    "Understanding potential catalyst events",
                    "Tracking major shareholder changes"
                ]
            },
            "SC 13G": {
                "name": "Beneficial Ownership (Passive)",
                "description": "5%+ ownership without intent to influence control. Passive institutional stakes.",
                "frequency": "As needed",
                "importance": "Medium",
                "use_cases": [
                    "Tracking large passive institutional positions",
                    "Identifying major long-term holders"
                ]
            },
            "S-1": {
                "name": "IPO Registration",
                "description": "Initial public offering registration statement. Detailed business description for newly public companies.",
                "frequency": "One-time (IPO)",
                "importance": "High (for IPOs)",
                "use_cases": [
                    "Analyzing newly public companies",
                    "Understanding business model before IPO",
                    "Evaluating IPO valuation"
                ]
            },
            "S-3": {
                "name": "Secondary Offering",
                "description": "Registration for secondary stock offerings by established public companies.",
                "frequency": "As needed",
                "importance": "Low",
                "use_cases": [
                    "Tracking dilution events",
                    "Understanding capital raising activities"
                ]
            }
        },
        "recommended_for_value_investing": [
            "10-K",
            "10-Q",
            "DEF 14A",
            "8-K"
        ],
        "recommended_workflow": {
            "initial_screening": ["10-K"],
            "deep_analysis": ["10-K", "10-Q", "DEF 14A"],
            "ongoing_monitoring": ["10-Q", "8-K"],
            "following_great_investors": ["13F"]
        }
    }


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
