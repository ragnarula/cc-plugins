---
name: deep-dive
description: Perform deep financial analysis of company from most recent /analyze. Analyzes 5-10 years of financial statements, calculates key metrics (ROE, ROIC, margins, FCF), and identifies trends following value investing principles.
argument-hint: (continues from last analysis)
allowed-tools: ["Read", "Write", "Bash", "Task", "Glob", "Grep", "WebSearch", "WebFetch"]
---

Continue with deep financial analysis from most recent screening.

STEP 1 - FIND MOST RECENT ANALYSIS:
Execute bash command to locate the latest analysis directory:

```bash
LATEST=$(ls -t ./analysis/ 2>/dev/null | head -1)
if [ -z "$LATEST" ]; then
  echo "ERROR: No analysis directory found. Run /analyze first."
  exit 1
fi
ANALYSIS_DIR="./analysis/$LATEST"
echo "Continuing analysis in: $ANALYSIS_DIR"
```

STEP 2 - VERIFY PREREQUISITES:
Read $ANALYSIS_DIR/01-initial-screening.md to:
- Extract the ticker symbol and company name
- Check the screening decision (PASS/INVESTIGATE/FAIL)
- If screening was FAIL: ask user "The initial screening was FAIL. Do you still want to proceed with deep-dive?"

STEP 3 - LAUNCH FINANCIAL-ANALYZER AGENT:
Use the Task tool to invoke the financial-analyzer agent:

"Perform deep financial analysis for [COMPANY/TICKER from screening].

Analysis directory: [provide ANALYSIS_DIR path]

Your tasks:
- Fetch 5-10 years of financial statements (10-K filings)
- Calculate key value investing metrics:
  - Return on Equity (ROE) trend
  - Return on Invested Capital (ROIC) trend
  - Profit margins (gross, operating, net)
  - Free cash flow generation and consistency
  - Debt levels and coverage ratios
  - Earnings quality and consistency
- Identify trends (improving, stable, deteriorating)
- Flag accounting red flags or concerns
- Apply frameworks from financial-analysis skill

Output requirements:
- Save to: [ANALYSIS_DIR]/02-financial-analysis.md
- Follow financial analysis template from report-writing skill
- Include proper citations (10-K year, page numbers)
- Show calculations with sources for all metrics"

STEP 4 - AUTOMATIC VALIDATION:
After financial-analyzer completes:

1. Invoke investment-manager agent to validate output
2. If FAIL: fix issues and re-validate (max 3 iterations)
3. If still FAIL after 3 iterations: present to user
4. If PASS: proceed to Step 5

STEP 5 - PRESENT RESULTS:
Summarize financial analysis:

- Financial quality assessment (strong/moderate/weak)
- Key metrics summary (ROE, ROIC, margins, FCF)
- Trends identified (positive/negative)
- Red flags or concerns
- Validation status: "✅ Quality validation: PASSED"
- Next step: "Run `/valuation` to estimate intrinsic value"
- Report location: [ANALYSIS_DIR]/02-financial-analysis.md
