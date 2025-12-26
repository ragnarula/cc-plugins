---
name: analyze
description: Start comprehensive investment analysis for a publicly traded company. Performs initial screening of business model, competitive position, and industry dynamics following value investing principles.
argument-hint: TICKER [--notes "optional context"]
allowed-tools: ["Read", "Write", "Bash", "WebSearch", "WebFetch", "Glob", "Grep", "Task"]
---

# Investment Analysis Command

This command initiates a comprehensive investment analysis workflow for a publicly traded company. Use the business-screener agent to perform systematic research and create an analysis directory with findings.

## Execution Steps

### 1. Parse Arguments and Gather Context

Extract the ticker symbol from user input:
- Required: Stock ticker (e.g., AAPL, MSFT, BRK.B)
- Optional: --notes flag with user's initial thesis or context

If user provides notes about why they're interested in the company, capture this context. If not provided, ask:
- "What attracted you to [COMPANY]?"
- "What's your initial investment thesis or reason for looking at this company?"
- "Any specific concerns or areas you'd like me to focus on?"

This helps understand the user's perspective and ensures analysis addresses their specific interests.

### 2. Create Analysis Directory Structure

Create a timestamped directory for this analysis:

```bash
mkdir -p ./analysis/[TICKER]-[YYYY-MM-DD]
```

Example: `./analysis/AAPL-2025-12-26/`

This directory will contain all analysis outputs:
- 01-initial-screening.md
- 02-financial-analysis.md (from deep-dive command)
- 03-valuation.md (from valuation command)
- 04-investment-memo.md (from report command)

### 3. Launch business-screener Agent

Use the Task tool to launch the business-screener agent with clear instructions:

**Agent prompt should include:**
- Stock ticker and company name
- User's initial thesis/notes (if provided)
- Instruction to perform comprehensive initial screening:
  - Fetch latest 10-K from SEC EDGAR
  - Research business model and how company makes money
  - Analyze competitive position and market dynamics
  - Identify economic moat (if any)
  - Assess industry structure and trends
  - Apply value investing principles from value-investing skill
  - Give clear PASS/INVESTIGATE/FAIL decision with reasoning

**Output requirements:**
- Save findings to `./analysis/[TICKER]-[DATE]/01-initial-screening.md`
- Structure report with clear sections
- Provide decision and reasoning
- Identify specific areas for deep dive if INVESTIGATE

### 4. Validate Output with Investment Manager

**CRITICAL:** After business-screener completes, automatically invoke investment-manager agent to validate the output.

Use the Task tool to launch investment-manager agent:

**Validation prompt should include:**
- Path to output file: `./analysis/[TICKER]-[DATE]/01-initial-screening.md`
- Instruction to perform comprehensive validation checking:
  - All assumptions documented with reasoning
  - All values have clear justification or sources
  - No hallucinations (unsupported claims, made-up data)
  - Meets specification requirements for initial screening
  - Reasoning is sound and logical
  - Sources are cited where needed
- Create validation report saved to: `./analysis/[TICKER]-[DATE]/validation-initial-screening.md`

**Review validation results:**
- If status is **PASS**: Proceed to step 5 (present results)
- If status is **PASS WITH WARNINGS**: Review warnings, fix if critical, then proceed
- If status is **FAIL**: Must fix issues before proceeding

### 5. Fix Issues Until Validation Passes

**If validation identifies issues (FAIL or critical warnings):**

1. **Review validation report** to understand specific issues:
   - Read the detailed validation report
   - Identify critical and major issues
   - Understand what needs to be fixed

2. **Fix the issues** by updating the analysis file:
   - For missing assumptions: Add reasoning (e.g., "5% growth based on historical 3-year average")
   - For unsourced values: Add citations (e.g., "per 10-K filing") or verify/remove
   - For hallucinations: Remove unsupported claims or find proper sources
   - For missing sections: Add required content per specification

3. **Re-validate** by invoking investment-manager again on the updated file

4. **Iterate** until validation status is PASS:
   - Keep fixing and re-validating
   - Don't proceed until all critical issues resolved
   - Maximum 3 iterations (if still failing after 3, escalate to user)

**Important:** Do NOT present results to user until validation passes. The investment-manager acts as a quality gate that must be cleared.

### 6. Present Results to User

After validation PASSES:

1. **Summarize key findings:**
   - Company business model (1-2 sentences)
   - Competitive position assessment
   - Economic moat identified (if any)
   - Key concerns or red flags

2. **Present decision:**
   - PASS: Business quality sufficient to proceed to deep analysis
   - INVESTIGATE: Mixed signals, need deeper investigation
   - FAIL: Fundamental issues, recommend passing on investment

3. **Validation status:**
   - "✅ Quality validation: PASSED"
   - "Issues found and resolved: [count] (see validation report for details)"

4. **Next steps:**
   - If PASS/INVESTIGATE: "Run `/deep-dive` to continue with detailed financial analysis"
   - If FAIL: "Based on initial screening, I recommend passing on this opportunity. [Key reasons]"

5. **Location of detailed report:**
   - "Full analysis saved to: ./analysis/[TICKER]-[DATE]/01-initial-screening.md"
   - "Validation report: ./analysis/[TICKER]-[DATE]/validation-initial-screening.md"

## Important Guidelines

### Use Value Investing Principles

The analysis should apply principles from the value-investing skill:
- Circle of competence check (can the business be understood?)
- Economic moat identification
- Business quality over price
- Skeptical, conservative approach

Reference the value-investing skill for frameworks on:
- Four essential questions
- Economic moat types
- Business quality assessment
- Common value traps to avoid

### Be Thorough But Focused

Initial screening should be comprehensive but not get lost in details:
- Understand what the business does and how it makes money
- Identify key competitive advantages (or lack thereof)
- Spot major red flags early
- Reserve detailed financial analysis for deep-dive phase

### Create Detailed, Well-Structured Output

The `01-initial-screening.md` file should include:
- Executive summary with clear decision
- Business model description
- Industry and competitive analysis
- Economic moat assessment
- Initial observations and concerns
- Recommended next steps
- Sources and references

Use markdown formatting with clear headers, bullet points, and tables where appropriate.

### Maintain Objectivity

Analysis should be:
- Fact-based and data-driven
- Skeptical, not promotional
- Balanced, noting both positives and concerns
- Explicit about assumptions and uncertainties

Avoid confirmation bias - don't just look for reasons to invest based on user's initial thesis.

## Example Usage

```
User: /analyze AAPL --notes "Saw strong iPhone sales in latest earnings"