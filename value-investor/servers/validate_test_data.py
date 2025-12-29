#!/usr/bin/env python3
"""
Validate Test Data Integrity

Validates that all test data fixtures exist and metadata is consistent.
Checks for missing files, validates metadata against actual files, and
reports statistics about the test dataset.

Usage:
    python validate_test_data.py
"""

import json
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path(__file__).parent / 'test_data' / 'fixtures'


def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def validate_test_data() -> bool:
    """
    Validate test data integrity.

    Returns:
        True if all validations pass, False otherwise
    """
    print("=" * 70)
    print("Validating Test Data")
    print("=" * 70)

    # Check metadata file exists
    metadata_path = BASE_DIR / 'metadata.json'

    if not metadata_path.exists():
        print(f"\n❌ ERROR: Metadata file not found: {metadata_path}")
        print("   Run download_test_data.py to generate test data.")
        return False

    # Load metadata
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n❌ ERROR: Invalid JSON in metadata file: {e}")
        return False

    print(f"\n✓ Metadata file found: {metadata_path}")
    print(f"  Version: {metadata.get('version', 'unknown')}")
    print(f"  Generated: {metadata.get('generated', 'unknown')}")

    filings = metadata.get('filings', [])

    if not filings:
        print(f"\n❌ ERROR: No filings in metadata")
        return False

    print(f"  Filings in metadata: {len(filings)}")

    # Validate each filing
    errors = []
    warnings = []

    for i, filing in enumerate(filings, 1):
        ticker = filing.get('ticker', 'UNKNOWN')
        filing_type = filing.get('filing_type', 'UNKNOWN')
        filing_date = filing.get('filing_date', 'UNKNOWN')

        print(f"\n{i}. {ticker} {filing_type} ({filing_date})")

        # Check original file
        original_path = BASE_DIR / filing.get('original_path', '')

        if not original_path.exists():
            errors.append(f"Missing original file: {original_path}")
            print(f"   ❌ Original file missing: {original_path}")
        else:
            actual_size = original_path.stat().st_size
            expected_size = filing.get('original_size', 0)

            if actual_size != expected_size:
                warnings.append(
                    f"{ticker} {filing_type}: Original size mismatch "
                    f"(expected {expected_size}, found {actual_size})"
                )
                print(f"   ⚠️  Original size mismatch: "
                      f"expected {format_size(expected_size)}, "
                      f"found {format_size(actual_size)}")
            else:
                print(f"   ✓ Original: {format_size(actual_size)}")

        # Check cleaned file
        cleaned_path = BASE_DIR / filing.get('cleaned_path', '')

        if not cleaned_path.exists():
            errors.append(f"Missing cleaned file: {cleaned_path}")
            print(f"   ❌ Cleaned file missing: {cleaned_path}")
        else:
            actual_size = cleaned_path.stat().st_size
            expected_size = filing.get('cleaned_size', 0)

            if actual_size != expected_size:
                warnings.append(
                    f"{ticker} {filing_type}: Cleaned size mismatch "
                    f"(expected {expected_size}, found {actual_size})"
                )
                print(f"   ⚠️  Cleaned size mismatch: "
                      f"expected {format_size(expected_size)}, "
                      f"found {format_size(actual_size)}")
            else:
                reduction = filing.get('reduction_percent', 0)
                print(f"   ✓ Cleaned: {format_size(actual_size)} ({reduction:.1f}% reduction)")

    # Print summary
    print("\n" + "=" * 70)
    print("Validation Summary")
    print("=" * 70)

    if errors:
        print(f"\n❌ Found {len(errors)} error(s):")
        for error in errors:
            print(f"   • {error}")

    if warnings:
        print(f"\n⚠️  Found {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"   • {warning}")

    if not errors and not warnings:
        print("\n✅ All validations passed!")

        # Print statistics
        print(f"\n📊 Dataset Statistics:")

        # By filing type
        by_type: Dict[str, int] = {}
        for filing in filings:
            filing_type = filing.get('filing_type', 'UNKNOWN')
            by_type[filing_type] = by_type.get(filing_type, 0) + 1

        print(f"\n   Filing types:")
        for filing_type, count in sorted(by_type.items()):
            print(f"      {filing_type:12} : {count} filing(s)")

        # By company
        by_ticker: Dict[str, int] = {}
        for filing in filings:
            ticker = filing.get('ticker', 'UNKNOWN')
            by_ticker[ticker] = by_ticker.get(ticker, 0) + 1

        print(f"\n   Companies:")
        for ticker, count in sorted(by_ticker.items()):
            company = next(
                (f['company_name'] for f in filings if f.get('ticker') == ticker),
                'Unknown'
            )
            print(f"      {ticker:6} ({company[:30]:30}) : {count} filing(s)")

        # Total sizes
        total_original = sum(f.get('original_size', 0) for f in filings)
        total_cleaned = sum(f.get('cleaned_size', 0) for f in filings)

        print(f"\n   Total sizes:")
        print(f"      Original: {format_size(total_original)}")
        print(f"      Cleaned:  {format_size(total_cleaned)}")

        if total_original > 0:
            total_reduction = ((total_original - total_cleaned) / total_original) * 100
            print(f"      Reduction: {format_size(total_original - total_cleaned)} ({total_reduction:.1f}%)")

        return True
    else:
        print(f"\n❌ Validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return False


if __name__ == "__main__":
    import sys

    success = validate_test_data()
    sys.exit(0 if success else 1)
