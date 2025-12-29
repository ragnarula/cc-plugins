"""
Integration tests for filing processing workflow.

Tests HTML cleaning on real SEC filing data. Uses test fixtures
downloaded by download_test_data.py.
"""

import pytest


@pytest.mark.integration
class TestFilingCleaning:
    """Test HTML cleaning on real SEC filings."""

    def test_clean_preserves_tables(self, html_cleaner, filings_by_type):
        """Cleaned filings preserve table structure."""
        # Test on 10-K filings (annual reports have extensive tables)
        for filing in filings_by_type.get('10-K', []):
            original = filing['_original_path'].read_text(encoding='utf-8')
            cleaned = html_cleaner.clean(original)

            # Tables are critical for financial statements
            assert '<table>' in cleaned.lower() or '<TABLE>' in cleaned.lower(), \
                f"Table structure lost in {filing['ticker']} {filing['filing_type']}"

            # Should remove styling
            assert 'style=' not in cleaned.lower(), \
                f"Style attributes remain in {filing['ticker']} {filing['filing_type']}"

    def test_clean_removes_scripts(self, html_cleaner, filings_by_type):
        """Cleaned filings have no script tags."""
        for filing_list in filings_by_type.values():
            for filing in filing_list:
                cleaned_content = filing['_cleaned_path'].read_text(encoding='utf-8')

                # No scripts should remain
                assert '<script' not in cleaned_content.lower(), \
                    f"Script tags found in {filing['ticker']} {filing['filing_type']}"

    def test_clean_removes_styles(self, html_cleaner, filings_by_type):
        """Cleaned filings have no style tags."""
        for filing_list in filings_by_type.values():
            for filing in filing_list:
                cleaned_content = filing['_cleaned_path'].read_text(encoding='utf-8')

                # No style tags should remain
                assert '<style' not in cleaned_content.lower(), \
                    f"Style tags found in {filing['ticker']} {filing['filing_type']}"

    def test_clean_achieves_size_reduction(self, filings_by_type):
        """Cleaned filings are significantly smaller than originals."""
        for filing_list in filings_by_type.values():
            for filing in filing_list:
                reduction = filing['reduction_percent']

                # Should achieve at least 50% reduction
                assert reduction >= 50.0, \
                    f"Insufficient size reduction for {filing['ticker']} {filing['filing_type']}: {reduction:.1f}%"

    def test_cleaned_files_exist(self, test_data_dir, test_metadata):
        """All cleaned files exist and are non-empty."""
        for filing in test_metadata['filings']:
            cleaned_path = test_data_dir / filing['cleaned_path']

            assert cleaned_path.exists(), \
                f"Cleaned file missing: {cleaned_path}"

            size = cleaned_path.stat().st_size
            assert size > 0, \
                f"Cleaned file is empty: {cleaned_path}"


@pytest.mark.integration
class TestFilingContent:
    """Test that cleaned filings preserve important content."""

    def test_company_name_preserved(self, filings_by_type):
        """Company name is preserved in cleaned filings."""
        for filing_list in filings_by_type.values():
            for filing in filing_list:
                cleaned_content = filing['_cleaned_path'].read_text(encoding='utf-8')
                company_name = filing['company_name']

                # Company name should appear in the filing
                # (May be abbreviated or formatted differently, so check for main part)
                company_words = company_name.split()[0]  # First word of company name

                assert company_words in cleaned_content, \
                    f"Company name '{company_name}' not found in {filing['ticker']} {filing['filing_type']}"

    def test_filing_content_not_empty(self, filings_by_type):
        """Cleaned filings contain substantial text content."""
        for filing_list in filings_by_type.values():
            for filing in filing_list:
                cleaned_content = filing['_cleaned_path'].read_text(encoding='utf-8')

                # Remove HTML tags to get text content
                import re
                text_only = re.sub(r'<[^>]+>', '', cleaned_content)
                text_only = text_only.strip()

                # Should have substantial content (at least 10KB of text)
                assert len(text_only) >= 10000, \
                    f"Insufficient text content in {filing['ticker']} {filing['filing_type']}: {len(text_only)} chars"


@pytest.mark.integration
class TestFilingTypes:
    """Test cleaning across different filing types."""

    def test_10k_filings(self, filings_by_type):
        """10-K annual reports are cleaned correctly."""
        if '10-K' not in filings_by_type:
            pytest.skip("No 10-K filings in test data")

        for filing in filings_by_type['10-K']:
            cleaned_content = filing['_cleaned_path'].read_text(encoding='utf-8')

            # 10-K should have substantial content
            assert len(cleaned_content) > 100000, \
                f"10-K filing too small: {filing['ticker']}"

            # Should preserve structure
            assert '<p>' in cleaned_content.lower() or '<div>' in cleaned_content.lower()

    def test_10q_filings(self, filings_by_type):
        """10-Q quarterly reports are cleaned correctly."""
        if '10-Q' not in filings_by_type:
            pytest.skip("No 10-Q filings in test data")

        for filing in filings_by_type['10-Q']:
            cleaned_content = filing['_cleaned_path'].read_text(encoding='utf-8')

            # 10-Q is smaller than 10-K but should still be substantial
            assert len(cleaned_content) > 50000, \
                f"10-Q filing too small: {filing['ticker']}"


@pytest.mark.integration
class TestCrossCompany:
    """Test cleaning consistency across different companies."""

    def test_consistent_cleaning(self, test_metadata):
        """Cleaning achieves similar results across companies."""
        reductions = [filing['reduction_percent'] for filing in test_metadata['filings']]

        # All should achieve significant reduction
        assert all(r >= 50.0 for r in reductions), \
            f"Some filings have insufficient reduction: {reductions}"

        # Should be generally consistent (within reasonable range)
        # Most SEC filings should reduce by 70-95%
        assert min(reductions) >= 60.0, \
            f"Minimum reduction too low: {min(reductions):.1f}%"

    def test_metadata_accuracy(self, test_metadata, test_data_dir):
        """Metadata accurately reflects actual files."""
        for filing in test_metadata['filings']:
            # Check original file
            original_path = test_data_dir / filing['original_path']
            actual_original_size = original_path.stat().st_size

            # Allow small differences due to encoding
            size_diff_pct = abs(actual_original_size - filing['original_size']) / filing['original_size'] * 100

            assert size_diff_pct < 1.0, \
                f"Original file size mismatch for {filing['ticker']}: {size_diff_pct:.2f}% difference"
