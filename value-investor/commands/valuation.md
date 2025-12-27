---
name: valuation
description: Run comprehensive valuation models (DCF, comparable analysis, Graham formula) with sensitivity analysis. Determines appropriate growth and discount rates with documented reasoning, calculates intrinsic value and margin of safety.
argument-hint: (continues from last analysis)
allowed-tools: ["Read", "Write", "Bash", "Task", "Glob", "Grep", "WebSearch", "WebFetch"]
---

Perform valuation analysis using multiple methodologies.

STEP 1 - FIND ANALYSIS AND VERIFY PREREQUISITES:
Execute bash to locate analysis directory:

```bash
LATEST=$(ls -t ./analysis/ 2>/dev/null | head -1)
if [ -z "$LATEST" ]; then
  echo "ERROR: No analysis found. Run /analyze first."
  exit 1
fi
ANALYSIS_DIR="./analysis/$LATEST"
echo "Found analysis: $ANALYSIS_DIR"
```

STEP 2 - VERIFY PRIOR STEPS COMPLETE:
Check that both files exist:
- Read $ANALYSIS_DIR/01-initial-screening.md (verify exists)
- Read $ANALYSIS_DIR/02-financial-analysis.md (verify exists)

If either missing: inform user which step to complete first and stop.

Extract company name, ticker, and key context from prior analysis.

STEP 3 - LAUNCH VALUATION-MODELER AGENT:
Use the Task tool to invoke the valuation-modeler agent:

"Perform comprehensive valuation for [COMPANY/TICKER from prior analysis].

Analysis directory: [provide ANALYSIS_DIR path]

Your tasks:
Build three valuation models:

A. Discounted Cash Flow (DCF):
   - Project 10-year free cash flows
   - Determine discount rate (document reasoning based on business risk)
   - Calculate terminal value conservatively
   - Provide sensitivity analysis (varying growth and discount rates)

B. Comparable Company Analysis:
   - Identify peer companies
   - Calculate multiples (P/E, EV/EBITDA, P/FCF)
   - Adjust for quality differences
   - Apply to normalized metrics

C. Benjamin Graham Formula:
   - Value = EPS × (8.5 + 2g)
   - Use conservative growth assumptions

All assumptions must be:
- Documented with clear reasoning
- Conservative per value investing principles
- Supported by prior financial analysis

Output requirements:
- Save to: [ANALYSIS_DIR]/03-valuation.md
- Show all calculations and assumptions
- Include sensitivity analysis tables
- Compare to current market price
- Calculate margin of safety
- Triangulate across all three methods"

STEP 4 - AUTOMATIC VALIDATION:
After valuation-modeler completes:

1. Invoke investment-manager agent to validate output
2. If FAIL: fix issues and re-validate (max 3 iterations)
3. If still FAIL after 3 iterations: present to user
4. If PASS: proceed to Step 5

STEP 5 - PRESENT RESULTS:
Summarize valuation analysis:

- Intrinsic value range (from three methods)
- Current market price vs. intrinsic value
- Margin of safety percentage
- Key assumptions and their impact
- Validation status: "✅ Quality validation: PASSED"
- Next step: "Run `/report` for final investment memo"
- Report location: [ANALYSIS_DIR]/03-valuation.md
