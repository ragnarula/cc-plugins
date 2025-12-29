#!/usr/bin/env python3
"""
Download Test Data for SEC Filing Analysis

Downloads diverse SEC filings for testing HTML cleaning and agent parsing.
Creates test fixtures in test_data/fixtures/ directory with both original
and cleaned versions of each filing.

Test Coverage:
- 8-10 filings across 5-6 filing types
- Multiple companies (AAPL, MSFT, BRK.B)
- Critical types: 10-K, 10-Q, DEF 14A, 8-K
- Institutional holdings: 13F

Usage:
    python download_test_data.py
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from sec_edgar_fetcher import SECEdgarFetcher
from html_cleaner import HTMLCleaner


# Test filings to download: (ticker, filing_type, years, limit_per_type)
TEST_FILINGS: List[Tuple[str, str, int, int]] = [
    # Apple - Core annual and quarterly
    ('AAPL', '10-K', 1, 1),
    ('AAPL', '10-Q', 1, 1),

    # Microsoft - Annual, quarterly, proxy, current events
    ('MSFT', '10-K', 1, 1),
    ('MSFT', '10-Q', 1, 1),
    ('MSFT', 'DEF 14A', 1, 1),
    ('MSFT', '8-K', 1, 1),

    # Berkshire Hathaway - Follow Buffett!
    ('BRK.B', '10-K', 1, 1),
    ('BRK.B', '13F', 1, 1),
]

# Output directory
BASE_DIR = Path(__file__).parent / 'test_data' / 'fixtures'


def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def sanitize_filename(filing_type: str, filing_date: str) -> str:
    """Create safe filename from filing type and date."""
    safe_type = filing_type.replace(' ', '_').replace('/', '-')
    return f"{safe_type}_{filing_date}.html"


def download_test_data():
    """Download test filings and create cleaned versions."""
    print("=" * 70)
    print("Downloading SEC Filing Test Data")
    print("=" * 70)

    # Initialize
    fetcher = SECEdgarFetcher()
    cleaner = HTMLCleaner()
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    metadata = {
        'version': '1.0',
        'generated': datetime.now().isoformat(),
        'filings': []
    }

    total_filings = 0
    total_original_size = 0
    total_cleaned_size = 0

    # Download each filing
    for ticker, filing_type, years, limit in TEST_FILINGS:
        print(f"\n📄 Fetching {ticker} {filing_type}...")

        try:
            # Fetch filing metadata
            filings = fetcher.fetch_filings(
                ticker=ticker,
                filing_types=[filing_type],
                years=years,
                limit_per_type=limit
            )

            filing_list = filings.get(filing_type, [])

            if not filing_list:
                print(f"   ⚠️  No {filing_type} filings found for {ticker}")
                continue

            # Process each filing
            for filing in filing_list:
                filing_date = filing['filingDate']
                company_name = filing['companyName']

                print(f"   • {filing_date} - {company_name}")

                # Create ticker directory
                ticker_dir = BASE_DIR / ticker
                ticker_dir.mkdir(exist_ok=True)

                # Generate filenames
                filename = sanitize_filename(filing_type, filing_date)
                original_path = ticker_dir / filename
                cleaned_filename = filename.replace('.html', '_cleaned.html')
                cleaned_path = ticker_dir / cleaned_filename

                # Download original
                print(f"     Downloading original...", end=" ", flush=True)
                original_content = fetcher.get_filing_content(filing['primaryDocUrl'])
                original_path.write_text(original_content, encoding='utf-8')
                original_size = len(original_content)
                print(f"{format_size(original_size)}")

                # Clean and save
                print(f"     Cleaning HTML...", end=" ", flush=True)
                stats = cleaner.clean_file(original_path, cleaned_path)
                cleaned_size = stats['cleaned_size']
                reduction = stats['reduction_percent']
                print(f"{format_size(cleaned_size)} ({reduction:.1f}% reduction)")

                # Add to metadata
                metadata['filings'].append({
                    'ticker': ticker,
                    'filing_type': filing_type,
                    'filing_date': filing_date,
                    'report_date': filing.get('reportDate'),
                    'company_name': company_name,
                    'cik': filing['cik'],
                    'original_path': f"{ticker}/{filename}",
                    'cleaned_path': f"{ticker}/{cleaned_filename}",
                    'original_size': original_size,
                    'cleaned_size': cleaned_size,
                    'reduction_bytes': stats['reduction_bytes'],
                    'reduction_percent': reduction,
                    'compression_ratio': stats['compression_ratio'],
                    'url': filing['primaryDocUrl']
                })

                total_filings += 1
                total_original_size += original_size
                total_cleaned_size += cleaned_size

        except Exception as e:
            print(f"   ❌ Error downloading {ticker} {filing_type}: {e}")
            continue

    # Save metadata
    metadata_path = BASE_DIR / 'metadata.json'
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

    # Print summary
    print("\n" + "=" * 70)
    print("Download Complete!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"   Filings downloaded:    {total_filings}")
    print(f"   Original total size:   {format_size(total_original_size)}")
    print(f"   Cleaned total size:    {format_size(total_cleaned_size)}")

    if total_original_size > 0:
        total_reduction = ((total_original_size - total_cleaned_size) / total_original_size) * 100
        print(f"   Total reduction:       {format_size(total_original_size - total_cleaned_size)} ({total_reduction:.1f}%)")

    print(f"\n📁 Files saved to: {BASE_DIR}")
    print(f"📋 Metadata saved to: {metadata_path}")

    # Group by filing type
    by_type = {}
    for filing in metadata['filings']:
        filing_type = filing['filing_type']
        by_type[filing_type] = by_type.get(filing_type, 0) + 1

    print(f"\n📈 Coverage by filing type:")
    for filing_type, count in sorted(by_type.items()):
        print(f"   {filing_type:12} : {count} filing(s)")


if __name__ == "__main__":
    download_test_data()
