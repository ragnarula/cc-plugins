---
name: valuation
description: Run comprehensive valuation models (DCF, comparable analysis, Graham formula) with sensitivity analysis. Determines appropriate growth and discount rates with documented reasoning, calculates intrinsic value and margin of safety.
argument-hint: (continues from last analysis)
allowed-tools: ["Read", "Write", "Bash", "Task", "Glob"]
---

# Valuation Modeling Command

This command performs comprehensive valuation analysis using multiple methodologies. Use the valuation-modeler agent to build models, determine appropriate assumptions, and calculate intrinsic value with sensitivity analysis.

## Execution Steps

### 1. Locate Analysis and Verify Prerequisites

Find the most recent analysis directory and verify that both prior steps are complete:

```bash
ls -t ./analysis/ | head -1
```

Check that these files exist:
- `01-initial-screening.md` (from /analyze)
- `02-financial-analysis.md` (from /deep-dive)

If either is missing:
- Inform user which step is missing
- Request they complete prior steps first
- Do not proceed

Read both files to understand:
- Company and ticker
- Business model and competitive position
- Financial quality and normalized economics
- Concerns or red flags identified

### 2. Launch valuation-modeler Agent

Use the Task tool to launch the valuation-modeler agent with comprehensive instructions:

**Agent prompt should include:**
- Company name, ticker, and business summary from prior analysis
- Instruction to perform multi-method valuation:

  **A. Discounted Cash Flow (DCF) Analysis:**
  - Project free cash flows for 10 years
  - Determine appropriate discount rate based on business risk, considering:
    - Company's financial leverage
    - Business model stability
    - Competitive position strength
    - Earnings quality and cash conversion
  - Estimate terminal value using conservative assumptions
  - Document all assumptions and reasoning
  - Provide sensitivity table varying growth and discount rates

  **B. Comparable Company Analysis:**
  - Identify appropriate peer companies
  - Calculate relevant multiples (P/E, EV/EBITDA, P/FCF, etc.)
  - Adjust for differences in quality, growth, margins
  - Apply multiples to company's normalized metrics
  - Document comparability assessment

  **C. Benjamin Graham Formula:**
  - Calculate intrinsic value using Graham's formula:
    Value = EPS × (8.5 + 2g)
    Where g = expected growth rate
  - Use conservative growth assumptions
  - Adjust for current interest rate environment if appropriate

  **D. Sensitivity Analysis:**
  - Show how intrinsic value changes with different assumptions
  - Test range of growth rates (e.g., 0%, 3%, 5%, 7%, 10%)
  - Test range of discount rates (e.g., 8%, 10%, 12%, 15%)
  - Identify assumptions with highest impact on value

**Key requirements:**
- Document reasoning for all key assumptions (growth rates, discount rates, terminal values)
- Use conservative assumptions consistent with value investing principles
- Be explicit about uncertainties and sensitivities
- Enable easy recalculation with different inputs
- Compare all three methods for triangulation

**Output requirements:**
- Save findings to `./analysis/[TICKER]-[DATE]/03-valuation.md`
- Include clear summary of intrinsic value range
- Show all calculations and assumptions
- Provide sensitivity analysis tables
- Compare to current market price
- Calculate margin of safety

### 3. Present Results to User

After agent completes:

1. **Summarize valuation results:**
   - DCF intrinsic value: $XX - $YY range
   - Comparable companies value: $XX - $YY range
   - Graham formula value: $XX
   - Weighted or triangulated estimate: $XX

2. **Current market assessment:**
   - Current market price: $XX
   - Margin of safety: XX% (if positive)
   - Or premium to estimated value: XX% (if negative)

3. **Key assumptions:**
   - Growth rate used: X%
   - Discount rate used: X%
   - Terminal multiple: Xx
   - Reasoning for these assumptions (brief summary)

4. **Sensitivity insights:**
   - Value range under different assumptions
   - Which assumptions matter most
   - Break-even scenarios

5. **Valuation assessment:**
   - ATTRACTIVE: Significant margin of safety (>25%)
   - FAIR: Reasonable margin (10-25%)
   - EXPENSIVE: Limited margin or premium to value (<10% margin)
   - OVERVALUED: Trading above intrinsic value

6. **Next steps:**
   - "Run `/report` to complete comprehensive risk assessment and generate final investment memo"
   - Or if overvalued: "Company trading above intrinsic value. Consider adding to watchlist for better entry point."

7. **Location of detailed models:**
   - "Full valuation analysis saved to: ./analysis/[TICKER]-[DATE]/03-valuation.md"

## Important Guidelines

### Use Value Investing Valuation Principles

Apply principles from value-investing skill:
- Conservative assumptions (err on side of caution)
- Multiple valuation methods for triangulation
- Margin of safety requirement (25-50%)
- Focus on normalized, sustainable economics
- Discount rate reflects business risk

### Determine Appropriate Growth Rates

Growth assumptions should be:
- **Anchored in historical performance:** Can't sustainably grow faster than history without clear reason
- **Industry-realistic:** Consider industry growth rate, market size constraints
- **Quality-adjusted:** Higher quality businesses (wide moats, high ROIC) can sustain growth longer
- **Conservative:** Use lower end of reasonable range
- **Finite:** High growth periods should be limited (typically 5-10 years), then fade to GDP growth

Document reasoning:
- Why is X% growth rate appropriate?
- What drives this growth (market growth, share gains, pricing, new products)?
- How long can this rate be sustained?
- What's terminal growth rate assumption?

### Determine Appropriate Discount Rates

Discount rate should reflect:
- **Business risk:** More stable businesses → lower rate (8-10%)
- **Financial risk:** Higher leverage → higher rate
- **Opportunity cost:** Should exceed market return expectation (~10%)
- **Quality premium:** Higher quality → potentially lower rate

Typical ranges:
- Exceptional business, fortress balance sheet: 8-9%
- High-quality, moderate leverage: 10%
- Good business, some leverage: 11-12%
- Fair business or higher risk: 12-15%

Document reasoning for chosen rate.

### Conservative Terminal Value Assumptions

Terminal value often represents >50% of DCF value, so be conservative:
- Use modest terminal growth rate (GDP growth or less: 2-3%)
- Or use exit multiple approach (10-15x terminal FCF typical)
- Consider competitive position sustainability
- Don't assume permanent high growth or multiples

### Enable Reassessment with Different Assumptions

Structure valuation output to allow easy recalculation:
- Clear summary of all assumptions
- Sensitivity tables showing impact of changes
- Instructions for how to adjust key inputs
- Formulas and calculations documented

User may want to test different scenarios or update as new information emerges.

### Create Comprehensive Output

The `03-valuation.md` file should include:
- Executive summary with valuation range
- Detailed DCF model with all assumptions
- Comparable company analysis
- Graham formula calculation
- Sensitivity analysis tables
- Comparison to market price
- Margin of safety calculation
- Discussion of key value drivers and risks
- Recommendations

## Example Usage

```
User: /valuation