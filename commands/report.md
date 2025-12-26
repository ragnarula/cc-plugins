---
name: report
description: Generate comprehensive investment memo with final BUY/HOLD/PASS recommendation. Performs risk assessment across all categories, compiles all prior analysis, and provides clear decision with supporting reasons.
argument-hint: (continues from last analysis)
allowed-tools: ["Read", "Write", "Bash", "Task", "Glob"]
---

# Investment Report Generation Command

This command completes the investment analysis workflow by performing comprehensive risk assessment and generating a final investment memo with clear recommendation. Uses risk-assessor and report-generator agents to compile findings and make final decision.

## Execution Steps

### 1. Locate Analysis and Verify All Prerequisites

Find the most recent analysis directory and verify all prior steps are complete:

```bash
ls -t ./analysis/ | head -1
```

Check that these files exist:
- `01-initial-screening.md` (from /analyze)
- `02-financial-analysis.md` (from /deep-dive)
- `03-valuation.md` (from /valuation)

If any are missing:
- Inform user which steps are missing
- Request they complete prior steps first
- Do not proceed

Read all three files to understand:
- Business model and competitive position
- Financial quality and historical performance
- Valuation analysis and margin of safety
- Concerns identified at each stage

### 2. Launch risk-assessor Agent

Use the Task tool to launch the risk-assessor agent to perform comprehensive risk analysis:

**Agent prompt should include:**
- Company name, ticker, and analysis summary
- Instruction to perform systematic risk assessment using risk-assessment skill:

  **Identify and assess risks across five categories:**

  1. **Business Risks:** Product, customer, supplier, operational, revenue model risks
  2. **Financial Risks:** Leverage, liquidity, capital allocation, accounting risks
  3. **Competitive Risks:** Market share, moat erosion, disruption, industry changes
  4. **Management Risks:** Capability, integrity, compensation, governance concerns
  5. **Macro Risks:** Economic cycle, regulatory, interest rate, geopolitical exposure

  **For each risk:**
  - Assess severity (High/Medium/Low impact on value)
  - Estimate probability (High/Medium/Low likelihood)
  - Prioritize critical risks requiring attention

  **Run red flag checklist:**
  - Automatic disqualifiers (fraud, no moat, bankruptcy risk)
  - Serious concerns (high debt + declining FCF, market share losses, etc.)
  - Warning signs (customer concentration, rising DSO, etc.)

  **Perform downside scenario analysis:**
  - Base case (most likely outcome)
  - Downside case (things go poorly)
  - Severe downside (worst realistic scenario)
  - Probability-weighted expected value
  - Maximum potential loss estimate

  **Stress testing:**
  - Revenue decline scenarios
  - Margin compression scenarios
  - Financial stress tests (rates, recession, refinancing)
  - Competitive response scenarios

**Output requirements:**
- Identify all material risks
- Assess severity and probability
- Flag any automatic disqualifiers
- Model downside scenarios
- Calculate probability-weighted value
- Provide risk assessment summary

This information will feed into the final investment memo.

### 3. Launch report-generator Agent

Use the Task tool to launch the report-generator agent to compile comprehensive investment memo:

**Agent prompt should include:**
- Company name, ticker
- Access to all prior analysis files (01, 02, 03)
- Risk assessment from risk-assessor agent
- Instruction to create comprehensive investment memo:

  **Investment Memo Structure:**

  **I. Executive Summary (1 page)**
  - Company overview (1-2 sentences)
  - Investment thesis (2-3 sentences)
  - Clear recommendation: BUY / HOLD / PASS
  - Key supporting reasons (3-5 bullets)
  - Margin of safety and expected return

  **II. Business Analysis**
  - Business model and revenue streams
  - Competitive position and economic moat
  - Industry dynamics and trends
  - Key strengths and weaknesses

  **III. Financial Analysis**
  - Historical performance summary (5-10 years)
  - Profitability trends and margins
  - Returns on capital (ROE, ROIC)
  - Cash flow generation and quality
  - Balance sheet strength
  - Peer comparison

  **IV. Valuation**
  - Intrinsic value estimate and methodology
  - Current market price
  - Margin of safety
  - Key assumptions and sensitivities
  - Valuation risks and opportunities

  **V. Risk Assessment**
  - Critical risks identified
  - Downside scenarios
  - Mitigating factors
  - Maximum loss potential
  - Risk/reward assessment

  **VI. Investment Decision**
  - Final recommendation with rationale
  - Position sizing suggestion
  - Monitoring plan
  - Exit criteria

  **Recommendation Criteria:**

  **BUY if:**
  - Business quality good (moat, ROIC >12%, consistent performance)
  - Management able and trustworthy
  - Adequate margin of safety (25-50% depending on quality)
  - Favorable risk/reward (2:1 or better upside/downside)
  - No automatic disqualifiers
  - Better opportunity than alternatives

  **HOLD/WATCH if:**
  - Business quality excellent but price too high (insufficient margin)
  - Minor concerns need monitoring
  - Waiting for better entry point
  - Keep on watchlist for future opportunity

  **PASS if:**
  - Any automatic disqualifiers present
  - Business quality insufficient (no moat, poor returns, declining)
  - Management concerns
  - Insufficient margin of safety
  - Risk/reward unfavorable
  - Better opportunities available

**Output requirements:**
- Save to `./analysis/[TICKER]-[DATE]/04-investment-memo.md`
- Clear, well-structured markdown
- Include all relevant data and analysis
- Professional format suitable for reference
- Clear recommendation with supporting evidence

### 4. Present Results to User

After report generation completes:

1. **Headline Recommendation:**
   - **BUY** / **HOLD** / **PASS**: [Company Name] ([TICKER])

2. **Key Supporting Reasons (3-5 bullets):**
   - Most important factors driving recommendation
   - E.g., "Wide moat from network effects and brand", "Trading at 35% discount to intrinsic value", "Consistent 20% ROE over 10 years"

3. **Valuation Summary:**
   - Intrinsic value estimate: $XX - $YY
   - Current price: $XX
   - Margin of safety: XX%
   - Expected annual return: XX%

4. **Key Risks:**
   - Top 3 risks to thesis
   - Mitigating factors

5. **If BUY:**
   - Position sizing suggestion
   - Monitoring plan summary
   - Entry price target (if current price not ideal)

6. **If HOLD:**
   - What would make it a BUY (e.g., "Would buy at $XX for 30% margin of safety")
   - Monitoring plan

7. **If PASS:**
   - Primary reasons for passing
   - What would need to change for reconsideration (if anything)

8. **Location of full memo:**
   - "Complete investment memo saved to: ./analysis/[TICKER]-[DATE]/04-investment-memo.md"

## Important Guidelines

### Apply Rigorous Value Investing Standards

Use value-investing skill principles for decision:
- Four essential questions must be answered satisfactorily
- Require clear competitive advantage
- Demand adequate margin of safety
- Focus on avoiding losses, not chasing gains

Don't compromise standards - passing on good companies at high prices is good discipline.

### Be Decisive and Clear

The recommendation should be unambiguous:
- Not "could be interesting if..." → Pick BUY, HOLD, or PASS
- Not "depends on your risk tolerance" → Make a call based on value principles
- Not hedging with excessive caveats → Clear stance with clear reasoning

Clarity is more valuable than hedging.

### Provide Actionable Recommendations

If BUY:
- Suggest position size (% of portfolio) based on conviction and risk
- Provide price target or entry range
- Outline what to monitor

If HOLD:
- Specify price at which it becomes BUY
- Explain what you're watching for

If PASS:
- Explain why clearly
- State what would need to change (if anything)

### Maintain Intellectual Honesty

The memo should:
- Acknowledge uncertainties and what you don't know
- Present balanced view (not just bullish or bearish)
- Address counterarguments to thesis
- Note where judgment calls were made
- Be honest about confidence level

Overconfidence is dangerous - be realistic about limitations of analysis.

### Create Professional, Referenceable Document

The investment memo should be:
- Comprehensive enough to stand alone
- Well-organized with clear sections
- Suitable for review months later
- Professional in tone and structure
- Factual and data-driven

This is a document you'll reference when monitoring the investment and when reviewing decisions later.

## Example Usage

```
User: /report