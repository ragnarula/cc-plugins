#!/usr/bin/env python3
"""
Inspect SEC Filing Tool

Fetch the latest 10-K filing for a ticker and save to disk for inspection.

Usage:
    python inspect_filing.py AAPL
    python inspect_filing.py MSFT --type 10-Q
    python inspect_filing.py GOOGL --output ./filings
"""

import argparse
import sys
from pathlib import Path
from sec_edgar_fetcher import SECEdgarFetcher
import json


def main():
    parser = argparse.ArgumentParser(description='Fetch and save SEC filings for inspection')
    parser.add_argument('ticker', help='Stock ticker symbol (e.g., AAPL, MSFT)')
    parser.add_argument('--type', default='10-K', help='Filing type (default: 10-K)')
    parser.add_argument('--output', default='./filings', help='Output directory (default: ./filings)')
    parser.add_argument('--metadata-only', action='store_true', help='Only fetch metadata, not content')

    args = parser.parse_args()

    ticker = args.ticker.upper()
    filing_type = args.type
    output_dir = Path(args.output)

    print(f"Fetching {filing_type} filing for {ticker}...")

    # Initialize fetcher
    fetcher = SECEdgarFetcher()

    # Fetch filings metadata
    try:
        filings = fetcher.fetch_filings(
            ticker=ticker,
            filing_types=[filing_type],
            years=5,
            limit_per_type=1  # Only get the most recent
        )
    except Exception as e:
        print(f"Error fetching filings: {e}")
        sys.exit(1)

    if not filings.get(filing_type):
        print(f"No {filing_type} filings found for {ticker}")
        sys.exit(1)

    latest_filing = filings[filing_type][0]

    print(f"\nLatest {filing_type} filing:")
    print(f"  Company: {latest_filing['companyName']}")
    print(f"  Filing Date: {latest_filing['filingDate']}")
    print(f"  Report Date: {latest_filing['reportDate']}")
    print(f"  Accession Number: {latest_filing['accessionNumber']}")
    print(f"  URL: {latest_filing['primaryDocUrl']}")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save metadata
    metadata_file = output_dir / f"{ticker}_{filing_type}_{latest_filing['filingDate']}_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(latest_filing, f, indent=2)

    print(f"\n✓ Saved metadata to: {metadata_file}")

    if args.metadata_only:
        print("\nMetadata-only mode. Skipping content download.")
        return

    # Fetch content
    print(f"\nFetching content from {latest_filing['primaryDocUrl']}...")
    print("(This may take 10-30 seconds for large filings)")

    try:
        content = fetcher.get_filing_content(latest_filing['primaryDocUrl'])
    except Exception as e:
        print(f"Error fetching content: {e}")
        sys.exit(1)

    # Save content
    content_file = output_dir / f"{ticker}_{filing_type}_{latest_filing['filingDate']}.html"
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(content)

    # Print stats
    size_bytes = len(content)
    size_mb = size_bytes / (1024 * 1024)

    print(f"\n✓ Saved content to: {content_file}")
    print(f"  Size: {size_bytes:,} bytes ({size_mb:.2f} MB)")
    print(f"  Lines: {content.count(chr(10)):,}")

    # Analyze content type
    is_xbrl = 'xbrl' in content[:5000].lower() or content.strip().startswith('<?xml')
    has_ixbrl = 'ix:' in content[:10000].lower() or 'xbrl' in content[:10000].lower()

    print(f"\nContent analysis:")
    print(f"  Format: {'XML/XBRL' if is_xbrl else 'HTML'}")
    print(f"  Has iXBRL tags: {'Yes' if has_ixbrl else 'No'}")

    # Sample content
    print(f"\nFirst 500 characters:")
    print("-" * 80)
    print(content[:500])
    print("-" * 80)

    print(f"\nYou can now inspect the full content at: {content_file}")


if __name__ == "__main__":
    main()
