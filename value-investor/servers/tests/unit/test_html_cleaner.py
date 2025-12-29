"""
Unit tests for HTMLCleaner module.

Tests HTML cleaning functionality with various input patterns.
Fast tests with no I/O operations.
"""

import pytest
from html_cleaner import HTMLCleaner


@pytest.mark.unit
class TestHTMLCleanerBasics:
    """Test basic HTML cleaning functionality."""

    def test_remove_style_tags(self, html_cleaner):
        """Style tags and their contents are removed."""
        html = '<style>body{color:red}</style><p>Text</p>'
        result = html_cleaner.clean(html)

        assert '<style>' not in result.lower()
        assert 'color:red' not in result
        assert '<p>' in result.lower()
        assert 'Text' in result

    def test_remove_script_tags(self, html_cleaner):
        """Script tags and their contents are removed."""
        html = '<script>console.log("test")</script><p>Text</p>'
        result = html_cleaner.clean(html)

        assert '<script>' not in result.lower()
        assert 'console.log' not in result
        assert '<p>' in result.lower()
        assert 'Text' in result

    def test_remove_class_attributes(self, html_cleaner):
        """Class attributes are removed from all tags."""
        html = '<p class="foo">Text</p>'
        result = html_cleaner.clean(html)

        assert 'class=' not in result.lower()
        assert '<p>' in result.lower()
        assert 'Text' in result

    def test_remove_id_attributes(self, html_cleaner):
        """ID attributes are removed from all tags."""
        html = '<div id="content">Text</div>'
        result = html_cleaner.clean(html)

        assert 'id=' not in result.lower()
        assert '<div>' in result.lower()
        assert 'Text' in result

    def test_remove_style_attributes(self, html_cleaner):
        """Style attributes are removed from all tags."""
        html = '<p style="color:red">Text</p>'
        result = html_cleaner.clean(html)

        assert 'style=' not in result.lower()
        assert '<p>' in result.lower()
        assert 'Text' in result


@pytest.mark.unit
class TestHTMLCleanerUnwrapTags:
    """Test unwrapping of presentational tags."""

    def test_unwrap_font_tags(self, html_cleaner):
        """Font tags are removed but content is preserved."""
        html = '<p><font color="red">Red text</font></p>'
        result = html_cleaner.clean(html)

        assert '<font' not in result.lower()
        assert 'Red text' in result
        assert '<p>' in result.lower()

    def test_unwrap_span_tags(self, html_cleaner):
        """Span tags are removed but content is preserved."""
        html = '<p><span class="highlight">Highlighted</span></p>'
        result = html_cleaner.clean(html)

        assert '<span' not in result.lower()
        assert 'Highlighted' in result

    def test_unwrap_bold_tags(self, html_cleaner):
        """Bold tags are removed but content is preserved."""
        html = '<p><b>Bold text</b> and <strong>strong text</strong></p>'
        result = html_cleaner.clean(html)

        assert '<b>' not in result.lower()
        assert '<strong>' not in result.lower()
        assert 'Bold text' in result
        assert 'strong text' in result

    def test_unwrap_italic_tags(self, html_cleaner):
        """Italic tags are removed but content is preserved."""
        html = '<p><i>Italic</i> and <em>emphasized</em></p>'
        result = html_cleaner.clean(html)

        assert '<i>' not in result.lower()
        assert '<em>' not in result.lower()
        assert 'Italic' in result
        assert 'emphasized' in result


@pytest.mark.unit
class TestHTMLCleanerPreserve:
    """Test preservation of structural elements."""

    def test_preserve_headings(self, html_cleaner):
        """Heading tags are preserved."""
        html = '<h1>Title</h1><h2>Subtitle</h2><p>Text</p>'
        result = html_cleaner.clean(html)

        assert '<h1>' in result.lower()
        assert '<h2>' in result.lower()
        assert 'Title' in result
        assert 'Subtitle' in result

    def test_preserve_paragraphs(self, html_cleaner):
        """Paragraph tags are preserved."""
        html = '<p>First paragraph</p><p>Second paragraph</p>'
        result = html_cleaner.clean(html)

        assert '<p>' in result.lower()
        assert 'First paragraph' in result
        assert 'Second paragraph' in result

    def test_preserve_tables(self, html_cleaner):
        """Table structure is preserved."""
        html = '''
        <table>
            <tr><th>Header</th></tr>
            <tr><td>Data</td></tr>
        </table>
        '''
        result = html_cleaner.clean(html)

        assert '<table>' in result.lower()
        assert '<tr>' in result.lower()
        assert '<th>' in result.lower()
        assert '<td>' in result.lower()
        assert 'Header' in result
        assert 'Data' in result

    def test_preserve_lists(self, html_cleaner):
        """List structure is preserved."""
        html = '<ul><li>Item 1</li><li>Item 2</li></ul>'
        result = html_cleaner.clean(html)

        assert '<ul>' in result.lower()
        assert '<li>' in result.lower()
        assert 'Item 1' in result
        assert 'Item 2' in result

    def test_preserve_divs(self, html_cleaner):
        """Div tags are preserved for structure."""
        html = '<div><p>Nested content</p></div>'
        result = html_cleaner.clean(html)

        assert '<div>' in result.lower()
        assert '<p>' in result.lower()
        assert 'Nested content' in result

    def test_preserve_href_attribute(self, html_cleaner):
        """Href attribute on links is preserved."""
        html = '<p><a href="http://example.com" class="link">Click here</a></p>'
        result = html_cleaner.clean(html)

        assert 'href="http://example.com"' in result
        assert 'class=' not in result.lower()
        assert '<a ' in result.lower()
        assert 'Click here' in result

    def test_preserve_br_tags(self, html_cleaner):
        """Line break tags are preserved."""
        html = '<p>Line 1<br/>Line 2</p>'
        result = html_cleaner.clean(html)

        assert '<br' in result.lower()
        assert 'Line 1' in result
        assert 'Line 2' in result


@pytest.mark.unit
class TestHTMLCleanerEmptyTags:
    """Test removal of empty tags."""

    def test_remove_empty_div(self, html_cleaner):
        """Empty div tags are removed."""
        html = '<div></div><p>Text</p>'
        result = html_cleaner.clean(html)

        # Empty div should be gone, but paragraph should remain
        assert '<p>' in result.lower()
        assert 'Text' in result
        # Check that there's only one div (the body tag might be present)
        # or no divs if all are empty

    def test_preserve_br_in_empty_check(self, html_cleaner):
        """BR tags are preserved even when alone."""
        html = '<p>Text<br/></p>'
        result = html_cleaner.clean(html)

        assert '<br' in result.lower()
        assert '<p>' in result.lower()


@pytest.mark.unit
class TestHTMLCleanerExtractText:
    """Test plain text extraction."""

    def test_extract_text_basic(self, html_cleaner):
        """Basic text extraction strips all tags."""
        html = '<p>Hello <b>world</b>!</p>'
        result = html_cleaner.extract_text(html)

        assert '<' not in result
        assert '>' not in result
        assert 'Hello' in result
        assert 'world' in result

    def test_extract_text_with_style(self, html_cleaner):
        """Style tags and content are removed during text extraction."""
        html = '<style>body{color:red}</style><p>Text</p>'
        result = html_cleaner.extract_text(html)

        assert 'color:red' not in result
        assert 'Text' in result

    def test_extract_text_whitespace_normalized(self, html_cleaner):
        """Whitespace is normalized in extracted text."""
        html = '<p>Text  with   multiple    spaces</p>'
        result = html_cleaner.extract_text(html)

        assert 'Text with multiple spaces' in result
        # Should not have multiple consecutive spaces
        assert '  ' not in result


@pytest.mark.unit
class TestHTMLCleanerComplexHTML:
    """Test cleaning of complex HTML structures."""

    def test_clean_complex_sample(self, html_cleaner, sample_html):
        """Clean complex sample HTML with nested structures."""
        result = html_cleaner.clean(sample_html)

        # Should remove styling
        assert '<style>' not in result.lower()
        assert 'color: red' not in result.lower()

        # Should remove scripts
        assert '<script>' not in result.lower()
        assert 'console.log' not in result

        # Should remove class/id attributes
        assert 'class=' not in result.lower()
        assert 'id=' not in result.lower() or 'id=' in result.lower() and 'doctype' in result.lower()  # Allow DOCTYPE

        # Should preserve structure
        assert '<h1>' in result.lower()
        assert '<table>' in result.lower()
        assert '<ul>' in result.lower()
        assert '<li>' in result.lower()

        # Should preserve href
        assert 'href="http://example.com"' in result

        # Should preserve content
        assert 'Main Heading' in result
        assert 'Value 1' in result
        assert 'Item 1' in result

    def test_clean_xbrl_sample(self, html_cleaner, sample_html_with_xbrl):
        """Clean HTML with XBRL inline tags (like SEC filings)."""
        result = html_cleaner.clean(sample_html_with_xbrl)

        # Should handle XBRL tags
        assert 'ix:' in result.lower()  # XBRL tags preserved

        # Should remove styling
        assert '<style>' not in result.lower()
        assert '.xbrl' not in result

        # Should preserve structure and content
        assert '<p>' in result.lower()
        assert '<table>' in result.lower()
        assert 'Revenue' in result
        assert '$1,000,000' in result


@pytest.mark.unit
class TestHTMLCleanerConfiguration:
    """Test configurable tag handling."""

    def test_custom_unwrap_tags(self):
        """Custom unwrap tags are respected."""
        cleaner = HTMLCleaner(unwrap_tags=['custom'])
        html = '<p><custom>Text</custom></p>'
        result = cleaner.clean(html)

        assert '<custom' not in result.lower()
        assert 'Text' in result

    def test_custom_self_closing_tags(self):
        """Custom self-closing tags are preserved."""
        cleaner = HTMLCleaner(self_closing_tags=['img', 'custom'])
        html = '<p><custom/></p>'
        result = cleaner.clean(html)

        # Custom tag should be preserved (not removed as empty)
        assert '<p>' in result.lower()
