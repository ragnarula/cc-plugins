---
name: analyze
description: Start comprehensive investment analysis for a publicly traded company. Performs initial screening of business model, competitive position, and industry dynamics following value investing principles.
argument-hint: TICKER [--notes "optional context"]
allowed-tools: ["Read", "Write", "Bash", "WebSearch", "WebFetch", "Glob", "Grep", "Task"]
---

# Investment Analysis Command

This command initiates a comprehensive investment analysis workflow for a publicly traded company. Use the business-screener agent to perform systematic research and create an analysis directory with findings.

## Execution Steps

### 1. Parse Arguments and Extract Ticker

Extract the ticker symbol from user input:
- Required: Stock ticker (e.g., AAPL, MSFT, BRK.B)
- Optional: --notes flag with user's initial thesis or context (captured if provided, but NOT requested if missing)

Begin analysis immediately without asking questions. The analysis will proceed from first principles, researching the company systematically without bias from user's initial expectations. Optional notes (if provided) are captured but analysis doesn't depend on them.

### 2. Create Analysis Directory and Prepare for Output

**IMMEDIATELY create** a timestamped directory for this analysis:

```bash
ANALYSIS_DIR="./analysis/[TICKER]-[YYYY-MM-DD]"
mkdir -p "$ANALYSIS_DIR"
```

Example: `./analysis/AAPL-2025-12-26/`

**This step happens first**, before launching agents. The directory path is then **passed to all agents** to ensure they save outputs correctly.

This directory will contain all analysis outputs across the workflow:
- 01-initial-screening.md (from /analyze)
- 02-financial-analysis.md (from /deep-dive)
- 03-valuation.md (from /valuation)
- 04-investment-memo.md (from /report)
- validation-*.md files (from investment-manager validation)

### 3. Launch business-screener Agent

Use the Task tool to launch the business-screener agent with clear instructions:

**Agent prompt MUST include:**
- Stock ticker and company name
- **ANALYSIS_DIR path** (the directory created in step 2) - agent uses this path for output
- User's initial thesis/notes (if provided)
- Instruction to perform comprehensive initial screening:
  - Fetch latest 10-K from SEC EDGAR
  - Research business model and how company makes money
  - Analyze competitive position and market dynamics
  - Identify economic moat (if any)
  - Assess industry structure and trends
  - Apply value investing principles from value-investing skill
  - Give clear PASS/INVESTIGATE/FAIL decision with reasoning

**Output requirements (agent must follow):**
- **Save to:** `$ANALYSIS_DIR/01-initial-screening.md` (use the directory path passed to agent)
- Structure report with clear sections
- Provide decision and reasoning
- Identify specific areas for deep dive if INVESTIGATE
- **DO NOT skip this save step** - output must be written to file

### 4. Automatic Validation and Iteration Loop (Mandatory)

**This step is AUTOMATIC and MANDATORY** - runs without user intervention after business-screener completes.

**First validation pass:**

Use the Task tool to launch investment-manager agent immediately after business-screener finishes:

**Validation prompt must include:**
- Path to output file: `$ANALYSIS_DIR/01-initial-screening.md`
- Instruction to perform comprehensive validation checking:
  - All assumptions documented with reasoning
  - All values have clear justification or sources
  - No hallucinations (unsupported claims, made-up data)
  - Meets specification requirements for initial screening
  - Reasoning is sound and logical
  - Sources are cited where needed
- Create validation report saved to: `$ANALYSIS_DIR/validation-initial-screening.md`

**Handle validation results automatically:**

**If PASS:**
- ✅ Validation successful - proceed to step 5 (present results to user)

**If FAIL or critical warnings found:**
- ⚠️ Read validation report to identify issues
- ⚠️ Fix the issues in the analysis file using Write tool:
  - For missing assumptions: Add reasoning (e.g., "5% growth based on historical 3-year average")
  - For unsourced values: Add citations (e.g., "per 10-K filing") or verify/remove
  - For hallucinations: Remove unsupported claims or find proper sources
  - For missing sections: Add required content per specification
- ⚠️ Re-invoke investment-manager on the updated file (automatic re-validation)
- ⚠️ Iterate: Keep fixing and re-validating until PASS (maximum 3 iterations)
- ⚠️ If still FAIL after 3 iterations: Present issue to user with explanation, ask how to proceed

**Important:** The command does NOT proceed to step 5 until validation passes. The investment-manager acts as an automatic quality gate that must be cleared before results are shown to user.

### 5. Present Results to User

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