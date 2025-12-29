# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Claude Code plugin that implements an initial investment screening workflow based on Warren Buffett and Charlie Munger's value investing principles. The plugin uses autonomous agents, validation checkpoints, and structured output generation.

**Current Status**: Stage 1 (Initial Screening) is fully implemented. Stages 2-4 (Financial Analysis, Valuation, Final Report) are planned for future development.

## Plugin Architecture

### Multi-Agent Workflow System

The plugin implements a **sequential workflow with quality gates** between stages:

1. **Commands** (user-facing entry points) → orchestrate agents
2. **Agents** (autonomous workers) → perform analysis and create outputs
3. **investment-manager** (quality control) → validates outputs automatically
4. **Skills** (knowledge bases) → provide principles and frameworks

**Critical Pattern**: Each command follows a three-step execution model:
1. Create analysis directory structure upfront
2. Launch specialized agent with directory path
3. **Automatically** invoke investment-manager for validation (no user intervention)
4. Fix issues and re-validate in loop until PASS (max 3 iterations)

This validation loop is **mandatory and automatic** - users never see invalid outputs.

### Directory Structure

```
.claude-plugin/
  plugin.json           # Plugin metadata
.mcp.json              # MCP server configuration (SEC EDGAR filing access)
agents/                # Autonomous analysis agents (2 implemented)
  business-screener.md  # Initial business screening
  investment-manager.md # Quality control (special role)
commands/              # User-invocable slash commands (1 implemented)
  analyze.md           # /analyze - initial screening
skills/                # Knowledge bases (1 domain)
  value-investing/     # Buffett/Munger principles (10 principles + examples + references)
servers/               # MCP server implementations
  financial_data_server.py  # Python MCP server for SEC EDGAR filings
  sec_edgar_fetcher.py      # SEC API client
  html_cleaner.py           # HTML cleaning utilities
analysis/              # Generated output directory
  [TICKER]-YYYY-MM-DD/ # One directory per analysis
    01-initial-screening.md  # Business screening output
    validation-*.md          # Quality control reports
```

### Analysis Workflow

**Current Implementation** (Stage 1 only):

1. `/analyze TICKER` → business-screener → 01-initial-screening.md ✅ **IMPLEMENTED**

**Planned Future Stages**:

2. `/deep-dive` → financial-analyzer → 02-financial-analysis.md ⏳ PLANNED
3. `/valuation` → valuation-modeler → 03-valuation.md ⏳ PLANNED
4. `/report` → risk-assessor + report-generator → 04-investment-memo.md ⏳ PLANNED

**State management**: When future stages are implemented, workflow state will be tracked via file existence in analysis directories.

### Agent System Design

**All agents follow standardized frontmatter structure:**

```yaml
---
identifier: agent-name
description: One-sentence capability description
whenToUse: |
  Detailed triggering conditions with examples
tools: [Read, Write, WebSearch, ...]
model: sonnet
color: orange
---
```

**Agent coordination pattern:**
- Commands create analysis directories FIRST (mkdir -p)
- Commands pass `$ANALYSIS_DIR` path to agents in prompt
- Agents write outputs to exact paths specified
- Commands invoke investment-manager immediately after agent completes
- investment-manager validates, commands fix issues in loop

### Quality Control System

**investment-manager agent** is special - it validates other agents' outputs:

**Validation checklist:**
- All assumptions documented with reasoning
- All values have clear justification or sources
- No hallucinations (unsupported claims, made-up data)
- Specification compliance (required sections present)
- Reasoning is sound and logical
- Sources cited where needed

**Automatic iteration loop** (implemented in ALL commands):
1. Agent produces output → file written
2. investment-manager validates → validation report created
3. If FAIL: Read validation report, fix issues in output file, re-validate
4. Repeat until PASS (max 3 iterations)
5. If still FAIL after 3: Surface to user with explanation

This ensures users NEVER see unvalidated analysis.

### Skills System Architecture

Skills provide **domain knowledge and frameworks** that agents reference:

**Structure pattern:**
```
skills/[domain]/
  SKILL.md              # Main skill file with frontmatter
  principles/           # Core concepts (10 principles)
  references/           # Supporting materials (quotes, moats, red flags)
  examples/             # Templates and checklists
```

**Skills are invoked by:**
- Agents (via skill references in their system prompts)
- Commands (by instructing agents to "apply value-investing principles")
- Users (via skill-based slash commands like /value-investing)

**Critical**: Skills contain the intellectual framework (Buffett/Munger methodology). Agents execute the framework systematically.

## Key Implementation Patterns

### Pattern 1: Analysis Directory Creation

**Always create directory BEFORE launching agents:**

```bash
ANALYSIS_DIR="./analysis/[TICKER]-[YYYY-MM-DD]"
mkdir -p "$ANALYSIS_DIR"
```

Then pass `$ANALYSIS_DIR` to agent prompt so agent knows exact save location.

### Pattern 2: Agent Prompt Construction

**Agent prompts must include:**
- Context (ticker, company name, user notes if provided)
- **Analysis directory path** (where to save output)
- Specific instructions (what to research, what sections to include)
- Output requirements (file path, format, required sections)
- Skill references ("apply value-investing principles from value-investing skill")

### Pattern 3: Automatic Validation Loop

**Template for all commands:**

```markdown
1. Launch [agent] to create output
2. Automatically launch investment-manager to validate
3. If PASS: proceed to present results
4. If FAIL:
   - Read validation report
   - Fix issues in output file using Write tool
   - Re-invoke investment-manager
   - Iterate max 3 times
5. If still FAIL after 3: ask user how to proceed
```

**This is MANDATORY** - never skip validation step.

### Pattern 4: Referencing Requirements

**All outputs must include references to source files:**

When agents cite principles, frameworks, or analysis from skills/references:
- Include file path in citation: `(value-investing/principles/02-good-business-criteria.md)`
- Use specific line numbers when quoting: `(02-good-business-criteria.md:45-50)`
- Link to examples: `See moat-analysis-checklist.md for framework`

This ensures analysis is **traceable and verifiable**.

## Configuration

### Plugin Settings

Users configure API keys and preferences in `.claude/value-investor.local.md`:

```markdown
---
api_keys:
  sec_edgar: "key"
  alpha_vantage: "key"
preferences:
  margin_of_safety: 0.25
  discount_rate: 0.10
  risk_tolerance: "conservative"
industries_to_avoid:
  - "cryptocurrency"
---
```

**Pattern**: Commands read this file for user preferences but provide sensible defaults.

### MCP Server Integration

`.mcp.json` configures SEC EDGAR filing data access:

```json
{
  "mcpServers": {
    "financial-data": {
      "command": "uv",
      "args": ["run", "--directory", "${CLAUDE_PLUGIN_ROOT}/servers", "python", "financial_data_server.py"]
    }
  }
}
```

Agents use MCP tools to fetch SEC filings (10-K, 10-Q, 8-K, DEF 14A, 13F, etc.) from the SEC EDGAR database.

## Development Guidelines

### When Adding New Commands

1. Create `commands/[name].md` with proper frontmatter
2. Include ticker/argument parsing logic
3. **Create analysis directory first** (mkdir -p)
4. Define agent prompt with output path
5. **Implement automatic validation loop** with investment-manager
6. Define clear output file path and format
7. Update README.md with command documentation

### When Adding New Agents

1. Create `agents/[name].md` with proper frontmatter
2. Define clear `whenToUse` with examples
3. Specify required tools in frontmatter
4. Include comprehensive system prompt with:
   - Expertise description
   - Core responsibilities
   - Output format requirements
   - Skill references (which frameworks to apply)
5. Agents MUST save outputs to paths passed in prompts
6. Test validation by investment-manager agent

### When Modifying Skills

1. Skills are **knowledge bases** not executables
2. Structure: principles/ + references/ + examples/
3. Use markdown format with clear sections
4. Include specific examples and frameworks
5. Skills are referenced by agents via skill system
6. Changes to skills affect ALL agents that reference them

### When Working with Analysis Outputs

**Never modify user analysis files directly** - validation loop handles corrections.

**Reading analysis outputs:**
- Use Read tool with full paths
- Check file existence before reading
- Parse sections systematically

**Fixing validation failures:**
- Read validation report to identify specific issues
- Use Write tool (not Edit) to fix output files
- Add missing reasoning, sources, or sections
- Re-validate after fixes

## Common Development Tasks

**Test the implemented workflow:**
```bash
cc
/analyze AAPL --notes "test analysis"
# Review output in ./analysis/AAPL-YYYY-MM-DD/01-initial-screening.md
# Check validation report in ./analysis/AAPL-YYYY-MM-DD/validation-initial-screening.md
```

**Check validation reports:**
```bash
cat analysis/[TICKER]-[DATE]/validation-*.md
```

**Verify agent outputs:**
Validation reports show whether outputs meet specifications.

## Philosophy and Principles

This plugin embodies **value investing discipline**:

- **Skeptical by default** - focused on avoiding bad investments
- **Business-first thinking** - understand the company deeply
- **Margin of safety** - conservative assumptions and valuations
- **Long-term perspective** - 5-10 year analysis horizon
- **Quality over quantity** - thorough analysis of few companies

**Agent behavior reflects this:**
- Agents challenge assumptions, not confirm biases
- Unsupported claims flagged as hallucinations
- Conservative valuations preferred over aggressive
- Red flags highlighted prominently
- Clear PASS/FAIL decisions (no wishy-washy recommendations)

The investment-manager enforces these standards rigorously.
