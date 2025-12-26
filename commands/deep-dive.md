---
name: deep-dive
description: Perform deep financial analysis of company from most recent /analyze. Analyzes 5-10 years of financial statements, calculates key metrics (ROE, ROIC, margins, FCF), and identifies trends following value investing principles.
argument-hint: (continues from last analysis)
allowed-tools: ["Read", "Write", "Bash", "Task", "Glob"]
---

# Deep Dive Financial Analysis Command

This command performs comprehensive financial analysis on the company from the most recent initial screening. Use the financial-analyzer agent to analyze historical financial statements and assess business quality.

## Execution Steps

### 1. Locate Most Recent Analysis

Find the most recent analysis directory:

```bash
ls -t ./analysis/ | head -1
```

This identifies the most recent company analysis to continue from.

Read the `01-initial-screening.md` file to understand:
- Which company is being analyzed
- Ticker symbol
- Initial screening decision (PASS/INVESTIGATE/FAIL)
- Key areas identified for deeper investigation

### 2. Verify Analysis Exists

If no prior analysis found:
- Inform user: "No previous analysis found. Please run `/analyze TICKER` first."
- Do not proceed

If initial screening decision was FAIL:
- Ask user: "Initial screening recommended passing on this investment due to [reasons]. Do you still want to proceed with deep analysis?"
- Await confirmation before continuing

### 3. Launch financial-analyzer Agent

Use the Task tool to launch the financial-analyzer agent with instructions:

**Agent prompt should include:**
- Company name and ticker from initial screening
- Instruction to perform comprehensive financial analysis:
  - Gather 5-10 years of financial statements (10-K filings)
  - Analyze income statement trends (revenue, margins, profitability)
  - Examine balance sheet strength (assets, liabilities, debt levels)
  - Evaluate cash flow generation (FCF, capital allocation)
  - Calculate key value investing metrics (ROE, ROIC, margins, debt ratios)
  - Apply financial-analysis skill frameworks
  - Identify red flags and accounting concerns
  - Assess financial quality and sustainability
  - Compare to industry peers where possible

**Analysis focus areas from initial screening:**
- Include specific areas flagged for investigation in initial screening
- Address any concerns or questions raised

**Output requirements:**
- Save findings to `./analysis/[TICKER]-[DATE]/02-financial-analysis.md`
- Include 10-year financial summary tables
- Calculate and trend key metrics
- Provide clear assessment of financial quality
- Identify concerns or red flags
- Give recommendation on proceeding to valuation

### 4. Validate Output with Investment Manager

**CRITICAL:** After financial-analyzer completes, automatically invoke investment-manager agent to validate the output.

Use the Task tool to launch investment-manager agent:

**Validation prompt should include:**
- Path to output file: `./analysis/[TICKER]-[DATE]/02-financial-analysis.md`
- Instruction to perform comprehensive validation checking:
  - All financial metrics properly calculated and sourced
  - Assumptions documented (normalized adjustments, growth rates, etc.)
  - No hallucinated financial data
  - Meets specification requirements for financial analysis
  - 10-year tables complete and accurate
  - Red flags properly identified
- Create validation report saved to: `./analysis/[TICKER]-[DATE]/validation-financial-analysis.md`

**Review validation results:**
- If status is **PASS**: Proceed to step 5 (present results)
- If status is **PASS WITH WARNINGS**: Review warnings, fix if critical, then proceed
- If status is **FAIL**: Must fix issues before proceeding

### 5. Fix Issues Until Validation Passes

**If validation identifies issues (FAIL or critical warnings):**

1. **Review validation report** to understand specific issues:
   - Missing metric calculations
   - Unsourced financial data
   - Undocumented normalization adjustments
   - Incomplete analysis sections

2. **Fix the issues** by updating the analysis file:
   - For missing calculations: Add ROE, ROIC, margin calculations with formulas
   - For unsourced data: Add "per 10-K filing FY20XX" or verify accuracy
   - For missing assumptions: Document why normalizations were made
   - For incomplete sections: Add required balance sheet, cash flow analysis

3. **Re-validate** by invoking investment-manager again on the updated file

4. **Iterate** until validation status is PASS:
   - Keep fixing and re-validating
   - Don't proceed until all critical issues resolved
   - Maximum 3 iterations (if still failing after 3, escalate to user)

**Important:** Do NOT present results to user until validation passes.

### 6. Present Results to User

After validation PASSES:

1. **Summarize financial quality:**
   - Profitability trends (margins expanding/stable/declining)
   - Returns on capital (ROE, ROIC levels and consistency)
   - Cash flow generation (FCF positive and growing?)
   - Balance sheet strength (debt levels, liquidity)

2. **Highlight key findings:**
   - Top 3 financial strengths
   - Top 3 financial concerns (if any)
   - Red flags identified (if any)

3. **Present recommendation:**
   - PROCEED: Financials support investment quality, ready for valuation
   - CAUTION: Some concerns but potentially addressable
   - STOP: Financial red flags too significant

4. **Validation status:**
   - "✅ Quality validation: PASSED"
   - "Issues found and resolved: [count]"

5. **Next steps:**
   - If PROCEED/CAUTION: "Run `/valuation` to estimate intrinsic value and margin of safety"
   - If STOP: "Financial analysis reveals significant concerns. Recommend passing. [Key reasons]"

6. **Location of detailed analysis:**
   - "Full analysis saved to: ./analysis/[TICKER]-[DATE]/02-financial-analysis.md"
   - "Validation report: ./analysis/[TICKER]-[DATE]/validation-financial-analysis.md"

## Important Guidelines

### Apply Financial Analysis Skill

Use frameworks from financial-analysis skill:
- Three financial statements analysis (Income Statement, Balance Sheet, Cash Flow)
- Key value investing metrics (ROE, ROIC, margins, FCF)
- Industry-specific considerations
- Accounting red flags and earnings quality assessment

### Focus on Normalized, Sustainable Economics

Adjust for:
- One-time items and non-recurring charges
- Economic cycles (normalize to mid-cycle)
- Accounting changes or irregularities
- Acquisitions and divestitures

The goal is to understand sustainable earning power, not just reported numbers.

### 5-10 Year Historical Analysis

Analyze sufficient history to:
- Identify trends (improving vs. deteriorating)
- Assess consistency vs. volatility
- Understand business through economic cycle
- Spot structural changes in business quality

Longer history provides better understanding, but ensure data remains relevant (don't include pre-transformation periods if business fundamentally changed).

### Compare to Peers and Industry

Benchmark company against:
- Direct competitors
- Industry averages
- Historical company performance

This context helps assess whether performance is exceptional, average, or poor.

### Create Comprehensive Output

The `02-financial-analysis.md` file should include:
- Executive summary with quality assessment
- 10-year financial summary tables
- Detailed analysis of each financial statement
- Key metrics calculated and trended
- Peer/industry comparisons
- Red flags and concerns identified
- Normalized economics estimates
- Recommendation on proceeding

Use tables, charts (described in text), and clear organization.

### Maintain High Standards

Be rigorous in analysis:
- Don't overlook warning signs
- Question aggressive accounting
- Verify cash generation matches earnings
- Check for deteriorating trends
- Apply value investing lens (quality, sustainability, conservatism)

If financials don't meet high standards, say so clearly.

## Example Usage

```
User: /deep-dive