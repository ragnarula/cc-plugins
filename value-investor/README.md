# Value Investor Plugin

A comprehensive investment analysis workflow for evaluating publicly traded companies using Warren Buffett and Charlie Munger's value investing principles.

## Overview

This plugin provides a systematic, professional-grade approach to analyzing potential investments in publicly traded companies. It follows a multi-stage workflow with human approval gates, ensuring thorough research while maintaining investor control.

## Philosophy

The plugin embodies value investing principles:
- **Skeptical by default**: Focused on avoiding bad investments rather than finding good ones
- **Business-first thinking**: Understanding what the company does and its competitive position
- **Margin of safety**: Conservative valuations and assumptions
- **Long-term perspective**: 5-10 year historical analysis and forward projections
- **Quality over quantity**: Thorough analysis of few companies rather than superficial screening of many

## Features

### Current Stage: Initial Screening

**Implemented:**
1. **Initial Screening** (`/analyze`) - Business model, competitive position, industry analysis using SEC filings

**Planned (Future Stages):**
2. Deep Financial Analysis - 5-10 year financial history, key metrics, trends
3. Valuation Modeling - DCF, comparable analysis, Graham formula with sensitivity
4. Risk Assessment & Final Report - Comprehensive risk analysis with BUY/HOLD/PASS recommendation

### Autonomous Agents

- **business-screener**: Initial research on company business model, competition, and industry using SEC EDGAR filings
- **investment-manager**: Quality control validation ensuring analysis follows value investing principles

### Knowledge Skills

- **value-investing**: Buffett/Munger mental models, frameworks, and principles with 10 core principles, examples, and references

## Prerequisites

### Required

- Claude Code CLI
- No API keys required (SEC EDGAR is free and public)

### Recommended

- Basic understanding of financial statements
- Familiarity with value investing concepts

## Installation

### From Local Directory

```bash
cc --plugin-dir /path/to/value-investor
```

### For Project-Specific Use

Copy the plugin to your project's `.claude-plugin/` directory:

```bash
cp -r value-investor /path/to/your/project/.claude-plugin/
```

## Configuration

(Optional) Create a settings file at `.claude/value-investor.local.md` to store preferences:

```markdown
---
preferences:
  margin_of_safety: 0.25  # 25% margin of safety (for future valuation stages)
  discount_rate: 0.10     # 10% default discount rate (for future valuation stages)
  risk_tolerance: "conservative"  # conservative, moderate, aggressive

industries_to_avoid:
  - "cryptocurrency"
  - "early-stage-biotech"
---

# Value Investor Settings

This file configures your value-investor plugin preferences.
```

**Note:** SEC EDGAR filings are free and public - no API keys required.

## Usage

### Initial Screening (Currently Implemented)

Start analyzing a company by ticker symbol:

```bash
/analyze AAPL --notes "Saw strong iPhone sales numbers in latest earnings"
```

The plugin will:
- Create an analysis directory: `./analysis/AAPL-2025-12-29/`
- Fetch the latest 10-K, 10-Q, and other SEC EDGAR filings
- Research business model, competitive position, and industry dynamics
- Apply value investing principles from the value-investing skill
- Identify economic moats and competitive advantages
- Check for red flags
- Provide clear PASS/INVESTIGATE/FAIL decision

**Output**: `./analysis/AAPL-2025-12-29/01-initial-screening.md`

The analysis is validated by the investment-manager agent to ensure quality and compliance with value investing principles.

## Workflow Example

```bash
# Analyze a company
/analyze BRK.B --notes "Legendary value investor's company"

# Review the screening results in:
# ./analysis/BRK.B-2025-12-29/01-initial-screening.md

# Decide whether to PASS, INVESTIGATE further, or FAIL based on screening
```

## Analysis Output Structure

Each analysis creates a timestamped directory:

```
analysis/
└── TICKER-YYYY-MM-DD/
    ├── 01-initial-screening.md     # Business model, competitive position, screening decision
    └── validation-*.md              # Quality control validation reports
```

## Best Practices

1. **Focus on business quality**: The screening focuses on business model and competitive advantages first
2. **Check red flags**: Pay attention to red flag warnings in the analysis
3. **Review the sources**: All analysis references specific SEC filings - review the source documents
4. **Be skeptical**: The plugin is designed to help you avoid bad investments, not find good ones
5. **Use the PASS/INVESTIGATE/FAIL framework**: Trust the screening recommendation but do your own research

## Commands Reference

| Command | Description | Arguments |
|---------|-------------|-----------|
| `/analyze` | Initial business screening | `TICKER --notes "optional context"` |

## Troubleshooting

**"Cannot fetch 10-K"**: Check that the ticker symbol is correct and the company files with the SEC (U.S. publicly traded companies)

**"SEC rate limit exceeded"**: SEC limits requests to 10 per second. The plugin respects this limit, but if you see this error, wait a few moments and try again.

**Analysis seems incomplete**: Review the validation report (`validation-*.md`) to see quality control feedback

## Contributing

This plugin follows Claude Code plugin development best practices. See the plugin-dev documentation for contribution guidelines.

## License

MIT

## Disclaimer

This plugin provides analysis tools and frameworks but does not constitute financial advice. All investment decisions should be made with appropriate due diligence and professional consultation. Past performance does not guarantee future results.
