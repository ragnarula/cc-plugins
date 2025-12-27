---
name: report
description: Generate comprehensive investment memo with final BUY/HOLD/PASS recommendation. Performs risk assessment across all categories, compiles all prior analysis, and provides clear decision with supporting reasons.
argument-hint: (continues from last analysis)
allowed-tools: ["Read", "Write", "Bash", "Task", "Glob", "Grep"]
---

Generate final investment memo with comprehensive risk assessment and recommendation.

STEP 1 - FIND ANALYSIS AND VERIFY ALL PREREQUISITES:
Execute bash to locate analysis directory:

```bash
LATEST=$(ls -t ./analysis/ 2>/dev/null | head -1)
if [ -z "$LATEST" ]; then
  echo "ERROR: No analysis found. Run /analyze first."
  exit 1
fi
ANALYSIS_DIR="./analysis/$LATEST"
echo "Generating report for: $ANALYSIS_DIR"
```

STEP 2 - VERIFY ALL PRIOR STEPS COMPLETE:
Check that all three files exist:
- Read $ANALYSIS_DIR/01-initial-screening.md
- Read $ANALYSIS_DIR/02-financial-analysis.md
- Read $ANALYSIS_DIR/03-valuation.md

If any missing: inform user which steps to complete first and stop.

Extract company name, ticker, and key findings from all prior analysis.

STEP 3 - LAUNCH RISK-ASSESSOR AGENT:
Use the Task tool to invoke the risk-assessor agent:

"Perform comprehensive risk assessment for [COMPANY/TICKER from prior analysis].

Analysis directory: [provide ANALYSIS_DIR path]

Read prior analysis files (01, 02, 03) to understand the company.

Your tasks:
Assess risks across five categories:
1. Business risks (product, customer, operational)
2. Financial risks (leverage, liquidity, capital allocation)
3. Competitive risks (moat erosion, disruption, market share)
4. Management risks (capability, integrity, governance)
5. Macro risks (economic cycle, regulatory, interest rates)

For each risk: assess severity and probability.

Run red flag checklist from risk-assessment skill.

Perform downside scenario analysis:
- Base case
- Downside case
- Severe downside case
- Probability-weighted expected value

This risk assessment will be used by report-generator agent."

STEP 4 - LAUNCH REPORT-GENERATOR AGENT:
After risk-assessor completes, use the Task tool to invoke the report-generator agent:

"Generate comprehensive investment memo for [COMPANY/TICKER].

Analysis directory: [provide ANALYSIS_DIR path]

Read all prior analysis:
- 01-initial-screening.md (business model, moat)
- 02-financial-analysis.md (historical performance, metrics)
- 03-valuation.md (intrinsic value, margin of safety)
- Risk assessment from risk-assessor agent

Compile final investment memo with:
- Executive summary
- Investment thesis (why invest or why pass)
- Business quality assessment
- Financial quality summary
- Valuation summary with margin of safety
- Risk assessment
- Clear recommendation: BUY / HOLD / PASS
- Supporting reasons for recommendation

Output requirements:
- Save to: [ANALYSIS_DIR]/04-investment-memo.md
- Follow investment memo template from report-writing skill
- Provide clear, actionable recommendation
- Include key supporting evidence"

STEP 5 - AUTOMATIC VALIDATION:
After report-generator completes:

1. Invoke investment-manager agent to validate output
2. If FAIL: fix issues and re-validate (max 3 iterations)
3. If still FAIL after 3 iterations: present to user
4. If PASS: proceed to Step 6

STEP 6 - PRESENT FINAL RECOMMENDATION:
Present the investment decision:

- Clear recommendation: BUY / HOLD / PASS
- Key supporting reasons (top 3)
- Primary risks identified
- Margin of safety (if BUY)
- Validation status: "✅ Quality validation: PASSED"
- Report location: [ANALYSIS_DIR]/04-investment-memo.md
- Analysis complete message

Congratulate user on completing thorough analysis!
