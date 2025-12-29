"""
Agent parsing tests for business-screener.

Tests that the business-screener agent can parse and understand
different SEC filing types. Uses direct Claude API calls with the
agent's system prompt.

These tests are marked with @pytest.mark.agent and are slow/expensive
(~30 seconds each, uses Claude API credits). Run separately:
    pytest -m agent
"""

import os
import pytest
from pathlib import Path


def read_agent_prompt():
    """Read business-screener agent system prompt from agents directory."""
    # Navigate from servers/tests/agents/ to agents/
    agent_path = Path(__file__).parent.parent.parent.parent / 'agents' / 'business-screener.md'

    if not agent_path.exists():
        pytest.skip(f"Agent file not found: {agent_path}")

    return agent_path.read_text(encoding='utf-8')


@pytest.mark.agent
class TestBusinessScreenerParsing:
    """
    Test business-screener agent parsing across filing types.

    Tests require Claude API access and are slow (~30 sec each).
    Mark tests to skip: pytest -m "not agent"
    """

    def invoke_agent(self, filing_content: str, filing_type: str, ticker: str, company_name: str) -> str:
        """
        Call Claude API with business-screener system prompt.

        Args:
            filing_content: Cleaned HTML content of the filing
            filing_type: Type of filing (10-K, 10-Q, etc.)
            ticker: Stock ticker symbol
            company_name: Full company name

        Returns:
            Agent's analysis as text
        """
        import anthropic

        # Check for API key
        if not os.environ.get('ANTHROPIC_API_KEY'):
            pytest.skip("ANTHROPIC_API_KEY not set - required for agent tests")

        client = anthropic.Anthropic()
        system_prompt = read_agent_prompt()

        # Construct user message
        user_message = f"""Analyze this {filing_type} filing for {company_name} ({ticker}).

Focus on:
- Understanding the company's business model and what they do
- Key strengths or competitive advantages you observe
- Notable risks or concerns from this filing

Please provide a brief analysis (2-3 paragraphs) demonstrating your understanding of the company.

Filing content (first 50,000 characters):
{filing_content[:50000]}
"""

        # Call Claude API
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        return response.content[0].text

    def test_parse_10k_aapl(self, filings_by_type):
        """Agent demonstrates understanding of Apple 10-K."""
        filing_list = filings_by_type.get('10-K', [])

        # Find AAPL 10-K
        aapl_filing = next((f for f in filing_list if f['ticker'] == 'AAPL'), None)

        if not aapl_filing:
            pytest.skip("AAPL 10-K not in test data")

        # Load cleaned filing
        content = aapl_filing['_cleaned_path'].read_text(encoding='utf-8')

        # Invoke agent
        print(f"\nAnalyzing {aapl_filing['ticker']} 10-K from {aapl_filing['filing_date']}...")
        response = self.invoke_agent(
            content,
            '10-K',
            aapl_filing['ticker'],
            aapl_filing['company_name']
        )

        # Basic validation: agent should understand this is Apple
        ticker = aapl_filing['ticker']
        company_name = aapl_filing['company_name']

        # Should mention the company (ticker or name)
        assert ticker in response or company_name in response or 'Apple' in response, \
            f"Agent response doesn't mention Apple: {response[:200]}"

        # Should provide substantive analysis
        assert len(response) > 200, \
            f"Agent response too brief ({len(response)} chars)"

        print(f"✓ Agent analyzed {ticker} 10-K successfully")
        print(f"  Response length: {len(response)} characters")
        print(f"  Preview: {response[:300]}...")

    def test_parse_10k_msft(self, filings_by_type):
        """Agent demonstrates understanding of Microsoft 10-K."""
        filing_list = filings_by_type.get('10-K', [])

        # Find MSFT 10-K
        msft_filing = next((f for f in filing_list if f['ticker'] == 'MSFT'), None)

        if not msft_filing:
            pytest.skip("MSFT 10-K not in test data")

        # Load cleaned filing
        content = msft_filing['_cleaned_path'].read_text(encoding='utf-8')

        # Invoke agent
        print(f"\nAnalyzing {msft_filing['ticker']} 10-K from {msft_filing['filing_date']}...")
        response = self.invoke_agent(
            content,
            '10-K',
            msft_filing['ticker'],
            msft_filing['company_name']
        )

        # Basic validation
        ticker = msft_filing['ticker']
        company_name = msft_filing['company_name']

        # Should mention Microsoft
        assert ticker in response or 'Microsoft' in response or company_name in response, \
            f"Agent response doesn't mention Microsoft: {response[:200]}"

        # Should provide substantive analysis
        assert len(response) > 200, \
            f"Agent response too brief ({len(response)} chars)"

        print(f"✓ Agent analyzed {ticker} 10-K successfully")
        print(f"  Response length: {len(response)} characters")
        print(f"  Preview: {response[:300]}...")

    def test_parse_10q_quarterly(self, filings_by_type):
        """Agent demonstrates understanding of 10-Q quarterly filings."""
        filing_list = filings_by_type.get('10-Q', [])

        if not filing_list:
            pytest.skip("No 10-Q filings in test data")

        # Test first 10-Q
        filing = filing_list[0]

        # Load cleaned filing
        content = filing['_cleaned_path'].read_text(encoding='utf-8')

        # Invoke agent
        print(f"\nAnalyzing {filing['ticker']} 10-Q from {filing['filing_date']}...")
        response = self.invoke_agent(
            content,
            '10-Q',
            filing['ticker'],
            filing['company_name']
        )

        # Basic validation
        ticker = filing['ticker']

        # Should mention the company
        assert ticker in response or filing['company_name'] in response, \
            f"Agent response doesn't mention {ticker}: {response[:200]}"

        # Should provide substantive analysis
        assert len(response) > 200, \
            f"Agent response too brief ({len(response)} chars)"

        # 10-Q is quarterly, might mention "quarter" or "quarterly"
        quarterly_terms = ['quarter', 'quarterly', 'Q1', 'Q2', 'Q3', 'Q4', 'three months', 'nine months']
        has_quarterly_context = any(term in response.lower() for term in quarterly_terms)

        print(f"✓ Agent analyzed {ticker} 10-Q successfully")
        print(f"  Response length: {len(response)} characters")
        print(f"  Quarterly context detected: {has_quarterly_context}")
        print(f"  Preview: {response[:300]}...")

    def test_agent_understands_business_context(self, filings_by_type):
        """Agent provides business context beyond just data extraction."""
        # Use any available filing
        all_filings = []
        for filing_list in filings_by_type.values():
            all_filings.extend(filing_list)

        if not all_filings:
            pytest.skip("No filings in test data")

        # Use first filing
        filing = all_filings[0]

        # Load cleaned filing
        content = filing['_cleaned_path'].read_text(encoding='utf-8')

        # Invoke agent
        print(f"\nTesting business understanding with {filing['ticker']} {filing['filing_type']}...")
        response = self.invoke_agent(
            content,
            filing['filing_type'],
            filing['ticker'],
            filing['company_name']
        )

        # Agent should demonstrate understanding, not just data extraction
        # Look for business-related terms
        business_terms = [
            'business', 'product', 'service', 'customer', 'market',
            'revenue', 'compete', 'advantage', 'strategy', 'risk',
            'operation', 'segment', 'industry', 'sell', 'offer'
        ]

        terms_found = sum(1 for term in business_terms if term in response.lower())

        assert terms_found >= 3, \
            f"Agent response lacks business context (only {terms_found} business terms found)"

        print(f"✓ Agent demonstrated business understanding")
        print(f"  Business terms found: {terms_found}/{len(business_terms)}")
        print(f"  Response length: {len(response)} characters")
