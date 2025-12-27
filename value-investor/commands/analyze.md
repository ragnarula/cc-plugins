---
name: analyze
description: Start comprehensive investment analysis for a publicly traded company. Performs initial screening of business model, competitive position, and industry dynamics following value investing principles.
argument-hint: TICKER
allowed-tools: ["Read", "Write", "Bash", "WebSearch", "WebFetch", "Glob", "Grep", "Task"]
---

Perform initial investment screening for: $ARGUMENTS

STEP 1 - EXTRACT TICKER:
Parse the stock ticker from the first argument.

STEP 2 - CREATE ANALYSIS DIRECTORY:
Execute the following bash command

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

Save the Business Sreening report in: [ANALYSIS_DIR]

STEP 4 - AUTOMATIC VALIDATION LOOP:
1. Invoke investment-manager agent to validate the output file in [ANALYSIS_DIR]
2. If validation returns FAIL se the Task tool to invoke the business-screener agent with the following prompt:
   - Read the validation report for [TICKER] in [ANALYSIS_DIR]
   - Fix identified issues in the business screenign report
3. Re-invoke investment-manager (max 3 iterations)
4. If still FAIL after 3 iterations: present issues to user and ask how to proceed
5. If PASS: proceed to Step 5

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
