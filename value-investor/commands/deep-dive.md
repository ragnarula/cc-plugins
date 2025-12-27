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

**Agent prompt MUST include:**
- Company name and ticker from initial screening
- **ANALYSIS_DIR path** (same analysis directory from /analyze) - agent uses this path for output
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

**Output requirements (agent must follow):**
- **Save to:** `$ANALYSIS_DIR/02-financial-analysis.md` (use the directory path passed to agent)
- Include 10-year financial summary tables
- Calculate and trend key metrics
- Provide clear assessment of financial quality
- Identify concerns or red flags
- Give recommendation on proceeding to valuation
- **DO NOT skip this save step** - output must be written to file

### 4. Automatic Validation and Iteration Loop (Mandatory)

**This step is AUTOMATIC and MANDATORY** - runs without user intervention after financial-analyzer completes.

**First validation pass:**

Use the Task tool to launch investment-manager agent immediately after financial-analyzer finishes:

**Validation prompt must include:**
- Path to output file: `$ANALYSIS_DIR/02-financial-analysis.md`
- Instruction to perform comprehensive validation checking:
  - All financial metrics properly calculated and sourced
  - Assumptions documented (normalized adjustments, growth rates, etc.)
  - No hallucinated financial data
  - Meets specification requirements for financial analysis
  - 10-year tables complete and accurate
  - Red flags properly identified
- Create validation report saved to: `$ANALYSIS_DIR/validation-financial-analysis.md`

**Handle validation results automatically:**

**If PASS:**
- ✅ Validation successful - proceed to step 5 (present results to user)

**If FAIL or critical warnings found:**
- ⚠️ Read validation report to identify issues
- ⚠️ Fix the issues in the analysis file using Write tool:
  - For missing calculations: Add ROE, ROIC, margin calculations with formulas
  - For unsourced data: Add "per 10-K filing FY20XX" or verify accuracy
  - For missing assumptions: Document why normalizations were made
  - For incomplete sections: Add required balance sheet, cash flow analysis
- ⚠️ Re-invoke investment-manager on the updated file (automatic re-validation)
- ⚠️ Iterate: Keep fixing and re-validating until PASS (maximum 3 iterations)
- ⚠️ If still FAIL after 3 iterations: Present issue to user with explanation, ask how to proceed

**Important:** The command does NOT proceed to step 5 until validation passes. The investment-manager acts as an automatic quality gate that must be cleared before results are shown to user.

### 5. Present Results to User

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