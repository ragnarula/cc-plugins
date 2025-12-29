"""
Shared pytest fixtures for all tests.

Provides common fixtures for accessing test data, HTML cleaner, and
SEC Edgar fetcher instances.
"""

import json
import pytest
from pathlib import Path

from html_cleaner import HTMLCleaner
from sec_edgar_fetcher import SECEdgarFetcher


@pytest.fixture
def test_data_dir():
    """Path to test data fixtures directory."""
    return Path(__file__).parent.parent / 'test_data' / 'fixtures'


@pytest.fixture
def test_metadata(test_data_dir):
    """
    Load test data metadata.

    Returns:
        dict: Metadata containing all filing information
    """
    metadata_path = test_data_dir / 'metadata.json'

    if not metadata_path.exists():
        pytest.skip("Test data not found. Run download_test_data.py first.")

    with open(metadata_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def filings_by_type(test_metadata, test_data_dir):
    """
    Group filings by type with full file paths.

    Returns:
        dict: Filing type -> list of filing metadata dicts

    Each filing dict includes:
        - All metadata from metadata.json
        - _original_path: Path to original filing
        - _cleaned_path: Path to cleaned filing
    """
    by_type = {}

    for filing in test_metadata['filings']:
        filing_type = filing['filing_type']

        if filing_type not in by_type:
            by_type[filing_type] = []

        # Add full paths to filing metadata
        filing['_original_path'] = test_data_dir / filing['original_path']
        filing['_cleaned_path'] = test_data_dir / filing['cleaned_path']

        by_type[filing_type].append(filing)

    return by_type


@pytest.fixture
def html_cleaner():
    """HTMLCleaner instance for tests."""
    return HTMLCleaner()


@pytest.fixture
def sec_fetcher():
    """SECEdgarFetcher instance for tests."""
    return SECEdgarFetcher()


@pytest.fixture
def sample_html():
    """Sample HTML for unit testing."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Document</title>
        <style>
            body { color: red; }
            .foo { background: blue; }
        </style>
        <script>
            console.log('test');
        </script>
    </head>
    <body>
        <h1 class="header" id="title" style="color: green;">Main Heading</h1>
        <div class="content">
            <p><font color="red">Red text in </font><b>bold</b> and <i>italic</i>.</p>
            <table class="data" border="1">
                <tr>
                    <th>Column 1</th>
                    <th>Column 2</th>
                </tr>
                <tr>
                    <td>Value 1</td>
                    <td>Value 2</td>
                </tr>
            </table>
            <ul>
                <li>Item 1</li>
                <li><span class="highlight">Item 2</span></li>
                <li>Item 3</li>
            </ul>
            <p>Link: <a href="http://example.com" class="link" id="link1">Example</a></p>
            <div class="empty"></div>
            <p><br/></p>
        </div>
        <!-- This is a comment -->
    </body>
    </html>
    """


@pytest.fixture
def sample_html_with_xbrl():
    """Sample HTML with XBRL inline tags (like SEC filings)."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SEC Filing</title>
        <style>
            .xbrl { font-weight: bold; }
        </style>
    </head>
    <body>
        <div>
            <ix:header>
                <ix:hidden>
                    <ix:nonnumeric>false</ix:nonnumeric>
                    <ix:nonnumeric>2025</ix:nonnumeric>
                </ix:hidden>
            </ix:header>
            <p>Revenue: <ix:nonnumeric>$1,000,000</ix:nonnumeric></p>
            <table>
                <tr>
                    <td>Net Income</td>
                    <td><ix:nonnumeric>$250,000</ix:nonnumeric></td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
