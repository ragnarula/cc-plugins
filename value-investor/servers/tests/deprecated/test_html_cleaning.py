#!/usr/bin/env python3
"""
Test HTML cleaning functionality on SEC EDGAR filings.

This script demonstrates the size reduction achieved by cleaning HTML.
"""

import sys
from sec_edgar_fetcher import SECEdgarFetcher


def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def test_html_cleaning(ticker: str = "AAPL", filing_type: str = "10-K"):
    """
    Test HTML cleaning on a real SEC filing.

    Args:
        ticker: Stock ticker symbol
        filing_type: Type of filing to test (default: 10-K)
    """
    print(f"Testing HTML cleaning for {ticker} {filing_type} filing...")
    print("=" * 70)

    fetcher = SECEdgarFetcher()

    # Fetch filings metadata
    print(f"\n1. Fetching {filing_type} filings for {ticker}...")
    filings = fetcher.fetch_filings(
        ticker=ticker,
        filing_types=[filing_type],
        years=1,
        limit_per_type=1
    )

    if not filings[filing_type]:
        print(f"No {filing_type} filings found for {ticker}")
        return

    latest = filings[filing_type][0]
    print(f"   Found: {latest['filingDate']} - {latest['companyName']}")
    print(f"   URL: {latest['primaryDocUrl']}")

    # Fetch raw HTML
    print(f"\n2. Fetching raw HTML content...")
    raw_html = fetcher.get_filing_content(latest['primaryDocUrl'])
    raw_size = len(raw_html)
    print(f"   Raw HTML size: {format_size(raw_size)}")

    # Fetch cleaned HTML
    print(f"\n3. Cleaning HTML (removing styling, excess markup)...")
    cleaned_html = fetcher.get_filing_content_clean(latest['primaryDocUrl'])
    cleaned_size = len(cleaned_html)
    print(f"   Cleaned HTML size: {format_size(cleaned_size)}")

    # Calculate reduction
    reduction_percent = ((raw_size - cleaned_size) / raw_size) * 100
    print(f"\n4. Results:")
    print(f"   Size reduction: {format_size(raw_size - cleaned_size)} ({reduction_percent:.1f}%)")
    print(f"   Compression ratio: {raw_size / cleaned_size:.2f}x")

    # Show sample of cleaned HTML
    print(f"\n5. Sample of cleaned HTML (first 1000 chars):")
    print("-" * 70)
    print(cleaned_html[:1000])
    print("-" * 70)

    print("\n✓ HTML cleaning test complete!")
    print(f"\nThe cleaned HTML preserves structure (headings, tables, paragraphs)")
    print(f"but removes all CSS, JavaScript, and presentational attributes.")


if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    filing_type = sys.argv[2] if len(sys.argv) > 2 else "10-K"

    test_html_cleaning(ticker, filing_type)
