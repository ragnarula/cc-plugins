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

### Multi-Stage Analysis Workflow

1. **Initial Screening** (`/analyze`) - Business model, competitive position, industry analysis
2. **Deep Financial Analysis** (`/deep-dive`) - 5-10 year financial history, key metrics, trends
3. **Valuation Modeling** (`/valuation`) - DCF, comparable analysis, Graham formula with sensitivity
4. **Risk Assessment & Report** (`/report`) - Comprehensive risk analysis with clear BUY/HOLD/PASS recommendation

### Autonomous Agents

- **business-screener**: Initial research on company business model, competition, and industry
- **financial-analyzer**: Deep dive into financial statements and key value metrics (ROE, ROIC, margins)
- **valuation-modeler**: Multiple valuation approaches with documented assumptions
- **risk-assessor**: Comprehensive risk analysis across all categories
- **report-generator**: Investment memo compilation with clear recommendations

### Knowledge Skills

- **value-investing**: Buffett/Munger mental models, frameworks, and principles
- **financial-analysis**: Statement analysis, industry-specific guidance, red flags
- **risk-assessment**: Risk frameworks and red flag checklists

## Prerequisites

### Required

- Claude Code CLI
- API access to financial data services (see Configuration below)

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

Create a settings file at `.claude/value-investor.local.md` in your project:

```markdown
---
api_keys:
  sec_edgar: "your-api-key-here"  # Optional, SEC EDGAR is public
  alpha_vantage: "your-api-key-here"  # Free tier available
  yahoo_finance: ""  # No key needed for basic access

preferences:
  margin_of_safety: 0.25  # 25% margin of safety
  discount_rate: 0.10     # 10% default discount rate
  risk_tolerance: "conservative"  # conservative, moderate, aggressive

industries_to_avoid:
  - "cryptocurrency"
  - "early-stage-biotech"
---

# Value Investor Settings

This file configures your value-investor plugin preferences.
```

### Getting API Keys

- **SEC EDGAR**: Public access, no key needed for basic usage
- **Alpha Vantage**: Free tier at https://www.alphavantage.co/support/#api-key
- **Yahoo Finance**: No authentication required for basic data

## Usage

### 1. Initial Analysis

Start analyzing a company by ticker symbol:

```bash
/analyze AAPL --notes "Saw strong iPhone sales numbers in latest earnings"
```

The plugin will:
- Ask clarifying questions about your investment thesis
- Create an analysis directory: `./analysis/AAPL-2025-12-26/`
- Fetch the latest 10-K from SEC EDGAR
- Research business model, competitive position, and industry
- Save findings with clear PASS/INVESTIGATE/FAIL decision

**Output**: `./analysis/AAPL-2025-12-26/01-initial-screening.md`

### 2. Deep Financial Analysis

After reviewing initial screening and deciding to proceed:

```bash
/deep-dive
```

The plugin will:
- Continue from most recent analysis
- Analyze 5-10 years of financial history
- Calculate key metrics (ROE, ROIC, profit margins, debt levels, earnings consistency)
- Identify trends and potential red flags
- Save comprehensive financial analysis

**Output**: `./analysis/AAPL-2025-12-26/02-financial-analysis.md`

### 3. Valuation

After reviewing financials and deciding to proceed:

```bash
/valuation
```

The plugin will:
- Determine appropriate growth and discount rates with documented reasoning
- Run multiple valuation models:
  - Discounted Cash Flow (DCF)
  - Comparable company analysis
  - Benjamin Graham formula
- Perform sensitivity analysis
- Allow rerunning with different assumptions

**Output**: `./analysis/AAPL-2025-12-26/03-valuation.md`

### 4. Final Report

Generate comprehensive investment memo:

```bash
/report
```

The plugin will:
- Assess all risk categories (business, financial, competitive, management, macro)
- Run through red flag checklist
- Compile all previous analysis
- Provide clear BUY/HOLD/PASS recommendation with key supporting reasons

**Output**: `./analysis/AAPL-2025-12-26/04-investment-memo.md`

## Workflow Example

```bash
# Start analysis
/analyze BRK.B --notes "Legendary value investor's company, circular reference?"

# Review initial screening, then continue
/deep-dive

# Review financials, then run valuation
/valuation

# Generate final report
/report

# All analysis saved in ./analysis/BRK.B-2025-12-26/
```

## Analysis Output Structure

Each analysis creates a timestamped directory:

```
analysis/
└── TICKER-YYYY-MM-DD/
    ├── 01-initial-screening.md
    ├── 02-financial-analysis.md
    ├── 03-valuation.md
    └── 04-investment-memo.md
```

## Best Practices

1. **Start with screening**: Always run `/analyze` first to avoid analysis paralysis
2. **Review between stages**: Use the human approval gates to stay objective
3. **Question assumptions**: Review the reasoning behind discount rates and growth assumptions
4. **Check red flags**: Pay special attention to risk assessment and red flag sections
5. **Compare valuations**: Look at all three valuation methods for convergence/divergence
6. **Be patient**: Thorough analysis takes time; resist the urge to rush

## Commands Reference

| Command | Description | Arguments |
|---------|-------------|-----------|
| `/analyze` | Start initial screening | `TICKER --notes "optional context"` |
| `/deep-dive` | Deep financial analysis | None (continues from last analysis) |
| `/valuation` | Run valuation models | None (uses analyzed company) |
| `/report` | Generate investment memo | None (compiles all analysis) |

## Troubleshooting

**"No previous analysis found"**: Run `/analyze TICKER` first before `/deep-dive`

**"API rate limit exceeded"**: Free tier API limits reached, wait or upgrade to paid tier

**"Cannot fetch 10-K"**: Check ticker symbol is correct and company files with SEC

**"Missing settings file"**: Create `.claude/value-investor.local.md` with API keys

## Contributing

This plugin follows Claude Code plugin development best practices. See the plugin-dev documentation for contribution guidelines.

## License

MIT

## Disclaimer

This plugin provides analysis tools and frameworks but does not constitute financial advice. All investment decisions should be made with appropriate due diligence and professional consultation. Past performance does not guarantee future results.
