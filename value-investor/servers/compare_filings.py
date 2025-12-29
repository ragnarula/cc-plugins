#!/usr/bin/env python3
"""
Compare Original and Cleaned SEC Filings

Inspection tool for comparing original SEC filings with cleaned versions.
Supports multiple comparison modes:
- stats: Show size reduction metrics
- diff: Show unified diff of changes
- preview: Open cleaned HTML in browser

Usage:
    python compare_filings.py <filing_path> --mode stats
    python compare_filings.py <filing_path> --mode diff
    python compare_filings.py <filing_path> --mode preview
"""

import argparse
import difflib
import webbrowser
import tempfile
from pathlib import Path

from html_cleaner import HTMLCleaner


def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def show_stats(original: str, cleaned: str, filepath: Path):
    """Show size reduction statistics."""
    original_size = len(original)
    cleaned_size = len(cleaned)
    reduction_bytes = original_size - cleaned_size
    reduction_percent = (reduction_bytes / original_size) * 100 if original_size > 0 else 0
    compression_ratio = original_size / cleaned_size if cleaned_size > 0 else 0

    print("=" * 70)
    print(f"Filing Comparison: {filepath.name}")
    print("=" * 70)
    print(f"\n📊 Size Statistics:")
    print(f"   Original size:     {format_size(original_size):>12}")
    print(f"   Cleaned size:      {format_size(cleaned_size):>12}")
    print(f"   Size reduction:    {format_size(reduction_bytes):>12} ({reduction_percent:.1f}%)")
    print(f"   Compression ratio: {compression_ratio:>12.2f}x")

    # Count tags
    import re
    original_tag_count = len(re.findall(r'<[^>]+>', original))
    cleaned_tag_count = len(re.findall(r'<[^>]+>', cleaned))

    print(f"\n🏷️  HTML Tags:")
    print(f"   Original tags:     {original_tag_count:>12,}")
    print(f"   Cleaned tags:      {cleaned_tag_count:>12,}")
    print(f"   Tags removed:      {original_tag_count - cleaned_tag_count:>12,}")

    # Check for specific removals
    print(f"\n🗑️  Removed Elements:")
    print(f"   <style> tags:      {'Yes' if '<style' in original.lower() and '<style' not in cleaned.lower() else 'No':>12}")
    print(f"   <script> tags:     {'Yes' if '<script' in original.lower() and '<script' not in cleaned.lower() else 'No':>12}")
    print(f"   class attributes:  {'Yes' if 'class=' in original.lower() and 'class=' not in cleaned.lower() else 'No':>12}")
    print(f"   style attributes:  {'Yes' if 'style=' in original.lower() and 'style=' not in cleaned.lower() else 'No':>12}")

    # Preserved elements
    print(f"\n✅ Preserved Elements:")
    print(f"   <table> tags:      {'Yes' if '<table' in cleaned.lower() else 'No':>12}")
    print(f"   <p> tags:          {'Yes' if '<p>' in cleaned.lower() else 'No':>12}")
    print(f"   <a> tags:          {'Yes' if '<a ' in cleaned.lower() else 'No':>12}")
    print(f"   href attributes:   {'Yes' if 'href=' in cleaned.lower() else 'No':>12}")


def show_diff(original: str, cleaned: str, context_lines: int = 3):
    """Show unified diff between original and cleaned."""
    print("=" * 70)
    print("Unified Diff (showing differences)")
    print("=" * 70)
    print(f"Context lines: {context_lines}")
    print()

    original_lines = original.splitlines(keepends=True)
    cleaned_lines = cleaned.splitlines(keepends=True)

    diff = difflib.unified_diff(
        original_lines,
        cleaned_lines,
        fromfile='original.html',
        tofile='cleaned.html',
        n=context_lines
    )

    diff_lines = list(diff)

    if not diff_lines:
        print("No differences found (files are identical)")
        return

    # Show first 100 lines of diff
    max_lines = 100
    for i, line in enumerate(diff_lines):
        if i >= max_lines:
            print(f"\n... (showing first {max_lines} lines of {len(diff_lines)} total)")
            break
        print(line, end='')


def show_preview(cleaned: str, filepath: Path):
    """Open cleaned HTML in default browser."""
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        temp_path = Path(f.name)
        f.write(cleaned)

    print("=" * 70)
    print("HTML Preview")
    print("=" * 70)
    print(f"\nOpening cleaned HTML in browser...")
    print(f"Original file: {filepath}")
    print(f"Preview file: {temp_path}")
    print(f"\nNote: Preview file will be deleted when you close this program.")

    # Open in browser
    webbrowser.open(temp_path.as_uri())

    print("\n✓ Browser opened. Press Ctrl+C to exit and delete preview file.")

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nCleaning up...")
        if temp_path.exists():
            temp_path.unlink()
        print("✓ Preview file deleted")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Compare original and cleaned SEC filings',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show size statistics
  python compare_filings.py test_data/fixtures/AAPL/10-K_2025-10-31.html --mode stats

  # Show diff (first 100 lines)
  python compare_filings.py test_data/fixtures/AAPL/10-K_2025-10-31.html --mode diff

  # Open cleaned version in browser
  python compare_filings.py test_data/fixtures/AAPL/10-K_2025-10-31.html --mode preview
        """
    )

    parser.add_argument(
        'filing_path',
        type=Path,
        help='Path to original HTML filing'
    )

    parser.add_argument(
        '--mode',
        choices=['stats', 'diff', 'preview'],
        default='stats',
        help='Comparison mode (default: stats)'
    )

    parser.add_argument(
        '--context',
        type=int,
        default=3,
        help='Number of context lines for diff mode (default: 3)'
    )

    args = parser.parse_args()

    # Check file exists
    if not args.filing_path.exists():
        print(f"Error: File not found: {args.filing_path}")
        return 1

    # Read original
    print(f"Reading {args.filing_path}...")
    original = args.filing_path.read_text(encoding='utf-8')

    # Clean
    print("Cleaning HTML...")
    cleaner = HTMLCleaner()
    cleaned = cleaner.clean(original)

    # Execute mode
    print()
    if args.mode == 'stats':
        show_stats(original, cleaned, args.filing_path)
    elif args.mode == 'diff':
        show_diff(original, cleaned, args.context)
    elif args.mode == 'preview':
        show_preview(cleaned, args.filing_path)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
