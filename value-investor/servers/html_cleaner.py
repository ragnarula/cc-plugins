"""
HTML Cleaner for SEC EDGAR Filings

Provides HTML cleaning functionality to remove styling and excess markup
while preserving document structure. Optimized for SEC filings which often
contain inline XBRL tags and heavy CSS/JavaScript.

Key Features:
- Remove all styling (CSS, style attributes, presentational tags)
- Preserve structural elements (headings, tables, lists, paragraphs)
- Handle XBRL inline tags gracefully
- Significant file size reduction (typically 70-80%)
"""

import re
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup, NavigableString, XMLParsedAsHTMLWarning


# Default tags to unwrap (remove tag but keep contents)
DEFAULT_UNWRAP_TAGS = [
    'font', 'span', 'b', 'i', 'u', 'strong', 'em',
    'small', 'big', 'center', 'strike', 's'
]

# Default self-closing tags to preserve
DEFAULT_SELF_CLOSING_TAGS = ['br', 'hr', 'img']


class HTMLCleaner:
    """
    Stateless HTML cleaning for SEC filings.

    Removes styling and presentational markup while preserving document
    structure and content. Configurable tag handling allows customization
    for different use cases.

    Example:
        cleaner = HTMLCleaner()
        cleaned_html = cleaner.clean(raw_html)

        # Or clean a file directly
        stats = cleaner.clean_file('input.html', 'output.html')
        print(f"Reduced size by {stats['reduction_percent']:.1f}%")
    """

    def __init__(
        self,
        unwrap_tags: Optional[List[str]] = None,
        self_closing_tags: Optional[List[str]] = None
    ):
        """
        Initialize HTMLCleaner with configurable tag handling.

        Args:
            unwrap_tags: Tags to remove while keeping their contents.
                        Defaults to common presentational tags (font, span, etc.)
            self_closing_tags: Self-closing tags to preserve during empty tag removal.
                              Defaults to ['br', 'hr', 'img']
        """
        self.unwrap_tags = unwrap_tags or DEFAULT_UNWRAP_TAGS
        self.self_closing_tags = self_closing_tags or DEFAULT_SELF_CLOSING_TAGS

    def clean(self, html_content: str) -> str:
        """
        Clean HTML by removing styling and excess markup while preserving structure.

        Removes:
        - All <style> and <script> tags and their contents
        - All style, class, id, and other presentational attributes
        - Font, span, and other purely presentational tags (unwrap their contents)
        - Empty tags that don't contribute to structure
        - HTML comments

        Preserves:
        - Structural tags: h1-h6, p, div, section, table, tr, td, th, ul, ol, li, br, hr
        - Links: a tags (with href attribute only)
        - Document hierarchy and text content

        Args:
            html_content: Raw HTML content as string

        Returns:
            Cleaned HTML with minimal markup as string
        """
        # Suppress XBRL/XML parsing warning (SEC filings often contain inline XBRL)
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

        soup = BeautifulSoup(html_content, 'lxml')

        # Remove script and style elements entirely
        for element in soup(['script', 'style', 'link', 'meta']):
            element.decompose()

        # Remove HTML comments
        for comment in soup.find_all(string=lambda text: isinstance(text, NavigableString) and text.strip().startswith('<!--')):
            comment.extract()

        # Tags to unwrap (remove tag but keep contents)
        for tag_name in self.unwrap_tags:
            for tag in soup.find_all(tag_name):
                tag.unwrap()

        # Remove all attributes except href on <a> tags
        for tag in soup.find_all(True):
            if tag.name == 'a':
                # Keep only href attribute
                attrs = dict(tag.attrs)
                tag.attrs = {}
                if 'href' in attrs:
                    tag['href'] = attrs['href']
            else:
                # Remove all attributes
                tag.attrs = {}

        # Remove empty tags (except self-closing ones like br, hr)
        changed = True
        while changed:
            changed = False
            for tag in soup.find_all(True):
                if tag.name in self.self_closing_tags:
                    continue
                # Check if tag is empty (no text and no children, or only whitespace)
                if not tag.get_text(strip=True) and not tag.find_all(True):
                    tag.decompose()
                    changed = True

        # Get the cleaned HTML
        # Use body content only if present, otherwise use all
        body = soup.find('body')
        if body:
            cleaned = str(body)
        else:
            cleaned = str(soup)

        # Remove excessive whitespace while preserving some structure
        cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)  # Max 2 consecutive newlines
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)  # Collapse spaces/tabs

        return cleaned

    def extract_text(self, html_content: str) -> str:
        """
        Extract plain text from HTML using BeautifulSoup.

        More sophisticated than regex-based approaches - properly handles
        nested tags and preserves text content from complex HTML structures.

        Args:
            html_content: Raw HTML content as string

        Returns:
            Plain text content with all HTML tags removed
        """
        # Suppress XBRL/XML parsing warning
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

        soup = BeautifulSoup(html_content, 'lxml')

        # Extract text with space separators
        text = soup.get_text(separator=' ', strip=True)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text

    def clean_file(
        self,
        input_path: Path,
        output_path: Path
    ) -> Dict[str, Any]:
        """
        Clean HTML file and save to output path, returning size reduction stats.

        Args:
            input_path: Path to input HTML file
            output_path: Path where cleaned HTML should be saved

        Returns:
            Dictionary with statistics:
            - original_size: Original file size in bytes
            - cleaned_size: Cleaned file size in bytes
            - reduction_bytes: Bytes saved
            - reduction_percent: Percentage reduction
            - compression_ratio: Original size / cleaned size

        Example:
            cleaner = HTMLCleaner()
            stats = cleaner.clean_file(
                Path('input.html'),
                Path('output.html')
            )
            print(f"Saved {stats['reduction_bytes']:,} bytes "
                  f"({stats['reduction_percent']:.1f}% reduction)")
        """
        # Read original
        original = input_path.read_text(encoding='utf-8')
        original_size = len(original)

        # Clean
        cleaned = self.clean(original)
        cleaned_size = len(cleaned)

        # Save cleaned
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(cleaned, encoding='utf-8')

        # Calculate stats
        reduction_bytes = original_size - cleaned_size
        reduction_percent = (reduction_bytes / original_size) * 100 if original_size > 0 else 0
        compression_ratio = original_size / cleaned_size if cleaned_size > 0 else 0

        return {
            'original_size': original_size,
            'cleaned_size': cleaned_size,
            'reduction_bytes': reduction_bytes,
            'reduction_percent': reduction_percent,
            'compression_ratio': compression_ratio
        }


def main():
    """Example usage of HTMLCleaner."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python html_cleaner.py <input_file> [output_file]")
        print("\nExample:")
        print("  python html_cleaner.py filing.html")
        print("  python html_cleaner.py filing.html cleaned_filing.html")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.with_stem(f"{input_path.stem}_cleaned")

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    print(f"Cleaning {input_path}...")

    cleaner = HTMLCleaner()
    stats = cleaner.clean_file(input_path, output_path)

    print(f"\nResults:")
    print(f"  Original size: {stats['original_size']:,} bytes")
    print(f"  Cleaned size:  {stats['cleaned_size']:,} bytes")
    print(f"  Reduction:     {stats['reduction_bytes']:,} bytes ({stats['reduction_percent']:.1f}%)")
    print(f"  Ratio:         {stats['compression_ratio']:.2f}x")
    print(f"\nCleaned file saved to: {output_path}")


if __name__ == "__main__":
    main()
