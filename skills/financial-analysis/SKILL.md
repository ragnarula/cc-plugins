---
name: Financial Statement Analysis
description: This skill should be used when the user asks to "analyze financials", "read 10-K", "evaluate financial statements", "assess financial health", "calculate financial ratios", "analyze balance sheet", "review income statement", "examine cash flow", "identify accounting red flags", or when performing detailed financial analysis of a company's historical performance and financial position.
version: 0.1.0
---

# Financial Statement Analysis

## Purpose

This skill provides frameworks for analyzing financial statements to assess business quality, identify trends, spot red flags, and calculate key metrics essential for value investing. Apply these techniques to evaluate historical performance and financial health when analyzing investment opportunities.

## Core Principles

Financial analysis aims to answer three questions:

1. **How profitable is the business?** (Income Statement)
2. **What does the company own and owe?** (Balance Sheet)
3. **Does the business generate real cash?** (Cash Flow Statement)

Always focus on normalized, sustainable economics rather than reported accounting figures. Look for consistency, quality of earnings, and alignment between accounting profits and cash generation.

## The Three Financial Statements

### Income Statement Analysis

**Purpose:** Measure profitability and operating performance

**Key Line Items:**

**Revenue** - Top line
- Analyze growth rate (5-10 year CAGR)
- Look for consistency vs. volatility
- Understand revenue composition (products, segments, geography)
- Check for one-time items inflating revenue

**Gross Profit** - Revenue minus Cost of Goods Sold
- Calculate Gross Margin % (Gross Profit / Revenue)
- Track trend over 5-10 years
- Compare to competitors and industry
- Stable or expanding margins indicate pricing power

**Operating Expenses** - SG&A, R&D, etc.
- Analyze as % of revenue
- Look for operating leverage (expenses growing slower than revenue)
- Distinguish growth vs. maintenance spending

**Operating Income** - Gross Profit minus Operating Expenses
- Calculate Operating Margin % (Operating Income / Revenue)
- Core measure of business profitability
- Remove one-time items for normalized figure

**Net Income** - Bottom line after all expenses, interest, taxes
- Calculate Net Margin % (Net Income / Revenue)
- Analyze trend over time
- Adjust for one-time items to get normalized earnings

**Critical Adjustments:**
- Add back non-cash charges (depreciation, amortization)
- Remove one-time items (restructuring, impairments)
- Normalize for unusual tax benefits/charges
- Calculate Owner Earnings (Net Income + D&A - Maintenance CapEx - Working Capital needs)

### Balance Sheet Analysis

**Purpose:** Assess financial strength and asset quality

**Assets Side:**

**Current Assets:**
- Cash & Equivalents - Real dry powder or trapped overseas?
- Accounts Receivable - Growing faster than sales? (Red flag)
- Inventory - Growing faster than sales? (Red flag)
- Calculate Days Sales Outstanding (DSO) = (Receivables / Revenue) × 365
- Calculate Days Inventory Outstanding (DIO) = (Inventory / COGS) × 365

**Long-term Assets:**
- Property, Plant & Equipment (PP&E) - Capital intensity indicator
- Intangible Assets/Goodwill - From acquisitions, potential impairment risk
- Goodwill >30% of assets = red flag for serial acquirer

**Liabilities Side:**

**Current Liabilities:**
- Accounts Payable - Company stretching payments?
- Short-term Debt - Refinancing risk?
- Calculate Days Payable Outstanding (DPO) = (Payables / COGS) × 365

**Long-term Liabilities:**
- Long-term Debt - Analyze debt/equity ratio, debt/EBITDA
- Pension & Other Post-retirement Benefits - Unfunded obligations
- Deferred Tax Liabilities - Timing differences

**Equity:**
- Shareholders' Equity - Book value
- Retained Earnings - Cumulative profits reinvested
- Treasury Stock - Share buyback activity

**Critical Ratios:**
- Current Ratio = Current Assets / Current Liabilities (>1.5 healthy)
- Quick Ratio = (Current Assets - Inventory) / Current Liabilities (>1.0 healthy)
- Debt/Equity = Total Debt / Shareholders' Equity (<0.5 conservative)
- Interest Coverage = EBIT / Interest Expense (>5x comfortable)

### Cash Flow Statement Analysis

**Purpose:** Verify cash generation and capital allocation

**Operating Cash Flow:**
- Cash from core business operations
- Should exceed Net Income over time
- If OCF < Net Income consistently = earnings quality concern

**Investing Cash Flow:**
- Capital Expenditures (CapEx) - Most important line
  - Maintenance CapEx - Required to maintain business
  - Growth CapEx - For expansion
- Acquisitions - Cash spent on M&A
- Asset sales - Proceeds from divestitures

**Financing Cash Flow:**
- Debt issuance/repayment
- Dividends paid
- Share buybacks/issuance

**Free Cash Flow Calculation:**
FCF = Operating Cash Flow - Capital Expenditures

Alternatively:
Owner Earnings = Net Income + D&A - Maintenance CapEx - Working Capital increases

**Critical Analysis:**
- FCF should be positive and growing
- FCF Margin = FCF / Revenue (track trend)
- FCF Conversion = FCF / Net Income (>80% healthy)
- Capital Intensity = CapEx / Revenue (<5% excellent, >15% concern)

## Key Value Investing Metrics

### Return on Equity (ROE)

**Formula:** ROE = Net Income / Shareholders' Equity

**Interpretation:**
- >20% = Excellent
- 15-20% = Good
- 10-15% = Fair
- <10% = Poor

**Deep Dive:**
Use DuPont Analysis to decompose ROE:
ROE = (Net Margin) × (Asset Turnover) × (Equity Multiplier)
= (NI/Sales) × (Sales/Assets) × (Assets/Equity)

Understand if high ROE from:
- High profitability (good)
- Efficient asset use (good)
- High leverage (risky)

### Return on Invested Capital (ROIC)

**Formula:** ROIC = NOPAT / Invested Capital

Where:
- NOPAT = Net Operating Profit After Tax = EBIT × (1 - Tax Rate)
- Invested Capital = Total Debt + Equity - Excess Cash

**Interpretation:**
- >15% = Excellent
- 12-15% = Good
- 8-12% = Fair
- <8% = Poor

**Why ROIC Matters:**
- Better than ROE for leveraged companies
- Measures return on all capital, not just equity
- Companies earning >12% ROIC create value when they grow
- Companies earning <8% ROIC destroy value when they grow

### Profit Margins

**Gross Margin** = (Revenue - COGS) / Revenue
- Indicates pricing power and unit economics
- Should be stable or expanding
- Compare to competitors

**Operating Margin** = Operating Income / Revenue
- Measures core business profitability
- Shows operating leverage
- Industry-specific benchmarks

**Net Margin** = Net Income / Revenue
- Bottom-line profitability
- Affected by financing and tax strategies

**FCF Margin** = Free Cash Flow / Revenue
- Ultimate measure of cash profitability
- Should track or exceed net margin

### Debt Analysis

**Total Debt / EBITDA**
- <1x = Very conservative
- 1-2x = Moderate
- 2-3x = Aggressive
- >3x = High risk

**Interest Coverage** = EBIT / Interest Expense
- >8x = Very safe
- 5-8x = Comfortable
- 3-5x = Adequate
- <3x = Risk of distress

**Debt Maturity Profile:**
- Review debt maturities in 10-K
- Refinancing risk if large maturities in next 2-3 years
- Preferable: Laddered maturities, long duration

## Industry-Specific Considerations

### Technology / Software

**Key Metrics:**
- Recurring revenue % (80%+ excellent for SaaS)
- Net revenue retention (>100% shows expansion)
- Customer acquisition cost (CAC) vs. Lifetime value (LTV)
- Rule of 40: Growth Rate + FCF Margin >40%
- Gross margins (70-90% for pure software)

**Red Flags:**
- Declining retention rates
- Rising CAC
- Revenue concentration in few customers

### Retail

**Key Metrics:**
- Same-store sales growth
- Inventory turnover = COGS / Average Inventory
- Sales per square foot
- Gross margin per product category

**Red Flags:**
- Negative comps
- Rising inventory levels
- Increasing promotional activity
- Store traffic declining

### Manufacturing

**Key Metrics:**
- Capacity utilization
- Gross margin trend
- Working capital efficiency
- Return on assets

**Red Flags:**
- Low utilization (<75%)
- Margin compression
- Rising inventories
- Commodity cost pressure

### Financial Services (Banks)

**Key Metrics:**
- Net interest margin (NIM)
- Return on assets (ROA)
- Efficiency ratio (expenses/revenue, lower better)
- Tier 1 capital ratio (>10% strong)
- Loan loss provisions / Total loans

**Red Flags:**
- Narrowing NIM
- Rising loan losses
- Declining capital ratios
- Concentration in risky loans

### Insurance

**Key Metrics:**
- Combined ratio (<100% profitable, <95% excellent)
- Float growth
- Investment return on float
- Underwriting profit

**Red Flags:**
- Combined ratio >100%
- Catastrophe exposure
- Reserve deficiencies

## Accounting Red Flags

### Earnings Quality Red Flags

1. **Net Income > Operating Cash Flow consistently**
   - Indicates accrual inflation
   - Check working capital build

2. **Frequent "one-time" charges**
   - If quarterly, they're not one-time
   - Add back to see true economics

3. **Revenue recognition changes**
   - Moving to more aggressive policies
   - Indicates pressure to meet targets

4. **Capitalizing vs. expensing**
   - Capitalizing normal operating costs
   - Inflates earnings and assets

5. **Related-party transactions**
   - Transactions with entities controlled by insiders
   - Potential self-dealing

### Cash Flow Red Flags

1. **Rising DSO (Days Sales Outstanding)**
   - Customers taking longer to pay
   - Possible channel stuffing or weak demand

2. **Rising DIO (Days Inventory Outstanding)**
   - Inventory building faster than sales
   - Obsolescence risk

3. **Negative Free Cash Flow**
   - Business consumes rather than generates cash
   - Check if temporary (growth investment) or structural

4. **Operating cash flow manipulations**
   - Stretching payables (rising DPO)
   - Delaying capital expenditures
   - Securitizing receivables

## Financial Analysis Process

### Step 1: Gather 10 Years of Data

Obtain from 10-K filings:
- Income statements (10 years)
- Balance sheets (10 years)
- Cash flow statements (10 years)
- Management discussion & analysis (MD&A)

### Step 2: Calculate Key Metrics

For each year, calculate:
- Revenue growth %
- Gross, Operating, Net, FCF margins
- ROE, ROIC
- Debt/EBITDA, Interest Coverage
- FCF and FCF growth
- DSO, DIO, DPO
- Working capital needs

### Step 3: Analyze Trends

Chart metrics over 10 years:
- Look for consistency vs. volatility
- Identify improving vs. deteriorating trends
- Spot cyclicality or structural changes

### Step 4: Compare to Peers

Benchmark against:
- Direct competitors
- Industry averages
- Historical company performance

### Step 5: Adjust for Abnormalities

Normalize for:
- Economic cycles
- One-time events
- Accounting changes
- Acquisitions/divestitures

### Step 6: Project Normalized Economics

Estimate sustainable:
- Revenue growth rate
- Profit margins
- Capital requirements
- Free cash flow generation

## Working Capital Analysis

**Working Capital** = Current Assets - Current Liabilities

**Changes in Working Capital:**
- Increase in WC = Uses cash (negative for FCF)
- Decrease in WC = Sources cash (positive for FCF)

**Cash Conversion Cycle:**
CCC = DSO + DIO - DPO

- Lower CCC = Better (cash generated faster)
- Negative CCC = Excellent (gets paid before paying suppliers)

**Examples:**
- Amazon: Negative CCC (collects before paying suppliers)
- Retailers: Long CCC (must hold inventory, slow collections)

## Using Financial Analysis in Investment Process

**Initial Screening:**
- Quick check: Positive FCF? ROE >12%? Reasonable debt?
- Pass if fundamentals clearly weak
- Proceed if worth deeper analysis

**Deep Dive:**
- Full 10-year analysis
- Calculate all key metrics
- Industry-specific assessment
- Identify red flags

**Valuation Inputs:**
- Normalized earnings power
- Sustainable margin estimates
- Growth rate justification
- Capital intensity requirements

**Ongoing Monitoring:**
- Track quarterly metrics
- Watch for deteriorating trends
- Reassess if material changes

## Additional Resources

### Reference Files

For detailed analysis techniques:
- **`references/financial-statement-checklists.md`** - Systematic line-by-line analysis guides
- **`references/industry-benchmarks.md`** - Metrics and norms by industry

### Example Files

Templates and calculations:
- **`examples/10-year-financial-model.md`** - Spreadsheet template for historical analysis
- **`examples/ratio-calculation-guide.md`** - Step-by-step ratio calculations with examples

## Summary

Financial analysis transforms raw accounting data into actionable insights about business quality. Focus on:

1. Consistent, growing profitability across all margin types
2. High and stable returns on capital (ROE >15%, ROIC >12%)
3. Strong, positive free cash flow generation
4. Conservative balance sheet with manageable debt
5. Quality earnings that convert to cash
6. Industry-appropriate metrics showing competitive strength

Use financial analysis to answer: "Does this business generate attractive returns on invested capital sustainably over time?" If yes, proceed to valuation. If no, pass regardless of current price.
