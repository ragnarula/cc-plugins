---
name: Report Writing Templates
description: This skill should be used when the user asks about "report format", "report template", "how to structure analysis", "screening report template", "investment memo template", or when guidance is needed on structuring investment analysis outputs. Provides standardized templates for business screening, financial analysis, valuation, and investment memo reports.
version: 0.1.0
---

# Report Writing Templates

## Purpose

This skill provides standardized templates for investment analysis reports generated throughout the value investing workflow. These templates ensure consistency, completeness, and adherence to quality standards across all analyses.

## When to Use This Skill

**Invoke this skill when:**
- Creating a new investment analysis report
- Seeking guidance on report structure and required sections
- Understanding what content belongs in each section
- Learning proper citation and source attribution formats
- Validating that a report includes all necessary components
- Training on report writing standards for value investing analysis

**Agents should reference this skill when:**
- business-screener creates initial screening reports (01-initial-screening.md)
- financial-analyzer creates financial analysis reports (02-financial-analysis.md)
- valuation-modeler creates valuation reports (03-valuation.md)
- report-generator creates investment memos (04-investment-memo.md)
- investment-manager validates report structure and completeness

## Available Templates

### Currently Available

#### Business Screening Report Template
- **Purpose**: Initial investment screening and business quality assessment
- **Used by**: business-screener agent via `/analyze` command
- **Output file**: `01-initial-screening.md`
- **Decision types**: PASS / INVESTIGATE / FAIL
- **Versions**:
  - **Annotated**: Complete template with detailed guidance, examples, and requirements for each section
  - **Clean**: Minimal scaffold with placeholders for quick reference and scaffolding

### Future Templates (Roadmap)

#### Financial Analysis Report Template
- **Purpose**: Deep dive into 5-10 year financial history and metrics
- **Used by**: financial-analyzer agent via `/deep-dive` command
- **Output file**: `02-financial-analysis.md`

#### Valuation Report Template
- **Purpose**: Multiple valuation approaches with sensitivity analysis
- **Used by**: valuation-modeler agent via `/valuation` command
- **Output file**: `03-valuation.md`

#### Investment Memo Template
- **Purpose**: Comprehensive investment recommendation with risk assessment
- **Used by**: report-generator agent via `/report` command
- **Output file**: `04-investment-memo.md`

## Template Types

### Annotated Templates

**Purpose**: Learning, reference, and comprehensive guidance

**Characteristics**:
- Detailed instructions for each section
- Examples of properly formatted content
- Citation format demonstrations
- Evidence requirements clearly stated
- Anti-examples (what NOT to do)
- Cross-references to value investing principles

**Use annotated templates when:**
- Learning how to structure analysis
- Understanding content requirements for each section
- Seeking examples of proper formatting and citations
- Training new agents or analysts
- Clarifying quality standards

### Clean Templates

**Purpose**: Quick reference and report scaffolding

**Characteristics**:
- Section headers and structure only
- Minimal placeholders ([Company Name], _____, etc.)
- No instructional text
- Ready for copy-paste scaffolding
- Streamlined for rapid use

**Use clean templates when:**
- Creating a new report quickly
- Need just the structure without guidance
- Already familiar with content requirements
- Scaffolding a report for completion

## How to Use These Templates

### For Agents

1. **Reference annotated template** to understand section requirements
2. **Use structure from clean template** as report scaffold
3. **Follow content guidance** from annotated template for each section
4. **Apply value investing principles** from value-investing skill
5. **Ensure all citations meet standards** described in templates
6. **Save completed report** to specified analysis directory

### For Users

1. **Review annotated template** to understand report expectations
2. **Use clean template** as checklist to verify completeness
3. **Reference examples** to see proper formatting
4. **Check citation requirements** before finalizing reports
5. **Invoke skill directly** for questions about structure or content

## Quality Standards

All reports generated using these templates must meet rigorous quality standards:

### Source Citation Requirements

**CRITICAL**: Every factual claim, metric, and data point must include a source citation.

**Primary sources** (preferred):
- SEC filings (10-K, 10-Q, 8-K) with specific page numbers
- Company earnings releases and presentations
- Proxy statements (DEF 14A)
- Company investor relations materials

**Secondary sources** (acceptable):
- Industry research reports (Gartner, IDC, etc.) with dates
- Financial data providers (Bloomberg, FactSet, S&P)
- Earnings call transcripts from reputable sources
- Financial publications (WSJ, Bloomberg, Reuters)

**Unacceptable**:
- Unsourced claims or "common knowledge"
- Estimates without methodology
- Social media content
- Wikipedia (except for basic historical facts)
- Promotional materials

**Citation format**:
```
Revenue: $416.2B (Apple Inc. 10-K FY2025, Income Statement, p.28)
ROE: 160% (NI $112B / Equity $70B avg, per 10-K FY2025)
Market share: 23% smartphone market (IDC Smartphone Tracker Q4 2024)
```

### Evidence Requirements

**Economic moat assessments** require specific, quantified evidence:
- Brand power → Pricing premium %, NPS scores, brand rankings (all with sources)
- Network effects → User count, value metrics per user, growth dynamics (all with sources)
- Switching costs → Retention rates, switching cost estimates, tenure data (all with sources)
- Cost advantages → Unit cost comparisons, margin analysis, scale metrics (all with sources)
- Regulatory barriers → Required licenses, approval timelines, barrier documentation (all with sources)

**Financial observations** require:
- Specific values with context (not approximations)
- Year-over-year or multi-year trends
- Peer comparisons where relevant
- Calculation methodologies shown for derived metrics (ROE, ROIC, margins)

### Completeness Requirements

**All required sections must be present**:
- Executive Summary with clear decision
- Business model analysis
- Competitive position and moat assessment
- Industry dynamics
- Financial observations
- Red flags and concerns
- Decision and rationale
- Comprehensive sources section

**Decision alignment**:
- Decision (PASS/INVESTIGATE/FAIL) must align with evidence presented
- Rationale must reference specific findings from analysis
- Next steps must logically follow from decision

## Integration with Plugin Workflow

### Workflow Context

The report-writing skill integrates into the four-stage investment analysis workflow:

1. **Stage 1: Initial Screening** (`/analyze`)
   - Command: analyze.md
   - Agent: business-screener.md
   - Template: business-screening-annotated.md / business-screening-clean.md
   - Output: 01-initial-screening.md

2. **Stage 2: Financial Analysis** (`/deep-dive`)
   - Command: deep-dive.md
   - Agent: financial-analyzer.md
   - Template: [Future] financial-analysis-annotated.md / financial-analysis-clean.md
   - Output: 02-financial-analysis.md

3. **Stage 3: Valuation** (`/valuation`)
   - Command: valuation.md
   - Agent: valuation-modeler.md
   - Template: [Future] valuation-annotated.md / valuation-clean.md
   - Output: 03-valuation.md

4. **Stage 4: Investment Memo** (`/report`)
   - Command: report.md
   - Agent: report-generator.md
   - Template: [Future] investment-memo-annotated.md / investment-memo-clean.md
   - Output: 04-investment-memo.md

### Validation Integration

The investment-manager agent uses these templates to validate report quality:
- Checks all required sections are present
- Verifies citations meet standards
- Ensures moat assessments include required evidence
- Confirms decision aligns with analysis
- Validates completeness against template specifications

## Cross-References to Other Skills

### value-investing Skill

Templates reference and apply frameworks from the value-investing skill:
- **The Four Essential Questions** - Structure business screening analysis
- **Economic Moat Types** - Guide competitive advantage assessment
- **Investment Checklist** - Ensure comprehensive evaluation
- **Decision Framework** - Inform PASS/INVESTIGATE/FAIL criteria

**Specific references**:
- `value-investing/SKILL.md` - Core principles and decision criteria
- `value-investing/principles/03-competitive-advantages.md` - Moat assessment frameworks
- `value-investing/examples/moat-analysis-checklist.md` - Evidence requirements for moats

### financial-analysis Skill

Templates incorporate financial analysis standards:
- **10-K Reading Framework** - Source for financial data extraction
- **Metric Calculation Standards** - ROE, ROIC, margin analysis approaches
- **Quality Assessment Criteria** - Earnings quality, cash flow analysis

**Specific references**:
- `financial-analysis/SKILL.md` - Financial statement analysis techniques
- `financial-analysis/examples/10-year-financial-model.md` - Financial data presentation format

### risk-assessment Skill

Templates include risk identification and assessment:
- **Risk Categories** - Business, financial, competitive, management, macro
- **Red Flag Checklists** - Warning signs and concerns
- **Severity Assessment** - Critical vs. serious vs. warning level risks

**Specific references**:
- `risk-assessment/SKILL.md` - Risk evaluation frameworks
- `risk-assessment/examples/risk-matrix-template.md` - Risk categorization approach

## Template Files

### Business Screening Templates

**Annotated version**: `templates/business-screening-annotated.md`
- Comprehensive guidance for each section
- Examples using real companies (Apple, See's Candy, etc.)
- Citation format demonstrations
- Evidence requirements for moat assessments
- Anti-examples showing what to avoid
- ~500 lines with detailed instructions

**Clean version**: `templates/business-screening-clean.md`
- Minimal structure with placeholders
- Section headers only
- Ready for scaffolding
- Quick reference
- ~150 lines streamlined

## Best Practices

### For Report Creation

1. **Start with structure** - Use clean template to scaffold report
2. **Reference guidance** - Consult annotated template for section requirements
3. **Cite as you write** - Add sources immediately, don't leave for later
4. **Show your work** - Include calculation methodologies for derived metrics
5. **Be specific** - Use precise figures with context, not approximations
6. **Stay objective** - Let evidence drive conclusions, not biases
7. **Check completeness** - Verify all sections present before finalizing

### For Citation

1. **Primary sources first** - Always prefer SEC filings and company reports
2. **Be specific** - Include page numbers, section names, fiscal years
3. **Show calculations** - Display formula and source data for derived metrics
4. **Date everything** - Indicate when data was accessed or published
5. **Link when possible** - Include URLs for digital sources
6. **Avoid approximations** - Use exact figures as stated in sources
7. **Distinguish facts from judgments** - Label opinions clearly

### For Moat Assessment

1. **Identify moat type(s)** - Match to five standard types
2. **Quantify evidence** - Provide specific metrics, not vague claims
3. **Cite all evidence** - Source every data point used
4. **Assess sustainability** - Project 10-year durability with reasoning
5. **Consider erosion risks** - Identify threats to moat longevity
6. **Compare to peers** - Show relative competitive position
7. **Avoid wishful thinking** - Require hard evidence, not hopes

## Future Enhancements

### Planned Template Additions

- **Financial Analysis Template** - For deep-dive financial statement analysis
- **Valuation Template** - For DCF, comparable, and other valuation methods
- **Investment Memo Template** - For final comprehensive investment recommendations

### Potential Expansions

- **Example excerpts** in examples/ directory showing real analysis snippets
- **Common mistakes** section with anti-patterns to avoid
- **Quick reference guides** for citation formats and evidence requirements
- **Template variations** for different company types (asset-light vs. capital-intensive, etc.)

## Summary

The report-writing skill provides the structural foundation for consistent, high-quality investment analysis reports. By standardizing format, enforcing citation requirements, and clearly defining content expectations, these templates ensure that all analyses meet value investing standards for rigor, completeness, and verifiability.

**Key principles**:
- **Consistency** - All reports follow standardized structure
- **Completeness** - All required sections and content present
- **Citability** - Every claim backed by specific sources
- **Clarity** - Decisions align clearly with evidence
- **Quality** - Reports meet investment-grade standards

Success is measured not by clever insights, but by systematic application of these templates to produce thorough, well-documented, verifiable investment analysis.
