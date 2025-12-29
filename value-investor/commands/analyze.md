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

- Perform initial investment screening for [TICKER] and write the business screening report as a file in [ANALYSIS_DIR] in markdown format
- The output report must be saved to disk
- Always save the report

STEP 4 - AUTOMATIC VALIDATION LOOP:
1. Invoke investment-manager agent with the following prompt
  - "Validate the business screening report in [ANALYSIS_DIR] providing feedback according investment standards for citations and value principles"
2. If validation returns FAIL use the Task tool to invoke the business-screener agent with the following prompt as well as the feedback from 1 above:
   - "Fix identified issues in the business screening report in [ANALYSIS_DIR]"
   - Feedback from above
3. Re-invoke investment-manager up to 3 times until all validations are sucessful (max 3 iterations)
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
- Report file location
