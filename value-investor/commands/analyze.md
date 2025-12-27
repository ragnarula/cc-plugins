---
name: analyze
description: Start comprehensive investment analysis for a publicly traded company. Performs initial screening of business model, competitive position, and industry dynamics following value investing principles.
argument-hint: TICKER
allowed-tools: ["Read", "Write", "Bash", "WebSearch", "WebFetch", "Glob", "Grep", "Task"]
---

Perform initial investment screening for: $ARGUMENTS

STEP 1 - EXTRACT TICKER:
Parse the stock ticker from the first argument.
If --notes flag is provided, capture the user's context.
Do NOT ask questions - proceed immediately with analysis.

STEP 2 - CREATE ANALYSIS DIRECTORY:
Execute the following bash command NOW (do not just describe it):

```bash
# Extract ticker and create timestamped analysis directory
TICKER="${1:-UNKNOWN}"
DATE=$(date +%Y-%m-%d)
ANALYSIS_DIR="./analysis/${TICKER}-${DATE}"
mkdir -p "$ANALYSIS_DIR"
echo "Created analysis directory: $ANALYSIS_DIR"
```

STEP 3 - LAUNCH BUSINESS-SCREENER AGENT:
Use the Task tool to invoke the business-screener agent with the following prompt:

"Perform initial investment screening for [TICKER].

Analysis directory: [provide the ANALYSIS_DIR path created above]

Your tasks:
- Fetch latest 10-K filing from SEC EDGAR
- Research business model and revenue sources
- Analyze competitive position and industry dynamics
- Identify economic moat (if any) using value-investing skill principles
- Apply value investing frameworks from value-investing skill
- Make clear PASS/INVESTIGATE/FAIL decision with reasoning

Output requirements:
- Save to: [ANALYSIS_DIR]/01-initial-screening.md
- Follow template from report-writing skill (business-screening-annotated.md)
- Include proper citations for all data (10-K references, etc.)
- Provide 8 required sections per template"

STEP 4 - AUTOMATIC VALIDATION LOOP:
After business-screener completes:

1. Invoke investment-manager agent to validate the output file
2. If validation returns FAIL:
   - Read the validation report
   - Fix identified issues in the screening file
   - Re-invoke investment-manager (max 3 iterations)
3. If still FAIL after 3 iterations: present issues to user and ask how to proceed
4. If PASS: proceed to Step 5

STEP 5 - PRESENT RESULTS:
After validation passes, summarize for the user:

- Business model (1-2 sentences)
- Competitive position assessment
- Economic moat (if identified)
- Key concerns or red flags
- Screening decision: PASS / INVESTIGATE / FAIL
- Validation status
- Next step: "Run `/deep-dive` to continue with financial analysis" (unless FAIL)
- Report location: ./analysis/[TICKER]-[DATE]/01-initial-screening.md
