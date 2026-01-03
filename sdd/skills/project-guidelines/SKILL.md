---
name: project-guidelines
description: This skill documents the standard process for reading and applying project-specific guidelines during SDD workflow phases. Use this when an agent needs to understand and follow project conventions for error handling, logging, naming, and testing.
version: 0.1.0
---

# Project Guidelines Reading

This skill defines the standard process for reading and applying project-specific guidelines. Multiple SDD agents (technical-architect, design-reviewer, developer) must follow this process to ensure consistency with project conventions.

## When to Use This Skill

Use this skill when:
- Starting the design phase (technical-architect)
- Reviewing a design for compliance (design-reviewer)
- Beginning implementation (developer)
- Validating that work follows project conventions

## The Project Guidelines File

Project guidelines are stored at `.sdd/project-guidelines.md` (referenced as `SDD_PROJECT_GUIDELINES`).

This file can:
1. **Reference existing documentation** - List paths to docs, READMEs, or other files containing conventions
2. **Define inline guidelines** - Specify conventions directly in the file

## Standard Reading Process

### Step 1: Check for Project Guidelines

```
Check if `.sdd/project-guidelines.md` exists
```

If the file does not exist:
- Note that no project-specific guidelines are defined
- Proceed with general best practices
- Consider recommending that guidelines be created

### Step 2: Read the Guidelines File

If the file exists, read it thoroughly using the Read tool.

### Step 3: Read All Referenced Documentation

The guidelines file may contain a "Referenced Documentation" section listing paths to other files. **You MUST read ALL referenced files.**

Common referenced files include:
- Error handling documentation
- Logging standards
- Coding style guides
- Architecture decision records (ADRs)
- README sections on conventions
- CLAUDE.md or CONSTITUTION.md files

### Step 4: Extract Key Conventions

From the guidelines and referenced documentation, identify conventions in these categories:

**Error Handling:**
- Error types/classes to use
- Error propagation patterns
- What information errors should contain
- How to categorize errors

**Logging:**
- Logging framework/approach
- Log levels and when to use them
- Required context in logs
- Structured logging requirements

**Naming Conventions:**
- File naming patterns
- Class/module naming patterns
- Function/method naming patterns
- Variable naming patterns

**Testing Conventions:**
- Test file locations and naming
- Test framework and assertion style
- Mocking/stubbing patterns
- Test data management

### Step 5: Apply Conventions to Decisions

**For Technical Architects (Design Phase):**
- Ensure component designs follow naming conventions
- Specify error handling approaches that match project patterns
- Plan logging consistent with project standards
- Design test strategies aligned with testing conventions

**For Design Reviewers (Review Phase):**
- Validate that designs comply with each convention category
- Flag any design decisions that conflict with documented guidelines
- Reference specific guidelines when noting violations

**For Developers (Implementation Phase):**
- Follow error handling patterns exactly
- Use logging consistent with project standards
- Apply naming conventions to all new code
- Structure tests according to testing conventions

## Validation Checklist

When applying project guidelines, verify:

- [ ] Project guidelines file was read (if it exists)
- [ ] All referenced documentation files were read
- [ ] Error handling approach matches project conventions
- [ ] Logging approach matches project conventions
- [ ] Naming conventions are followed
- [ ] Testing approach aligns with project conventions

## What to Do When Guidelines Are Missing

If `.sdd/project-guidelines.md` does not exist but the project has established patterns:

1. **Explore the codebase** to discover implicit conventions
2. **Document discovered patterns** in your output
3. **Consider recommending** that guidelines be formalized

If guidelines are incomplete or ambiguous:

1. **Use AskUserQuestion** to clarify conventions
2. **Document assumptions** you're making
3. **Note gaps** that should be filled in the guidelines

## Example Usage

### In Technical Architect Agent

```
Agent: "Let me first check for project guidelines..."
*Reads .sdd/project-guidelines.md*
Agent: "I found project guidelines referencing docs/error-handling.md and docs/logging.md. Let me read those..."
*Reads docs/error-handling.md*
*Reads docs/logging.md*
Agent: "I see the project uses custom AppError classes with error codes, and structured JSON logging. I'll ensure my design follows these patterns..."
```

### In Design Reviewer Agent

```
Agent: "Checking design compliance with project guidelines..."
*Reads .sdd/project-guidelines.md and referenced docs*
Agent: "The design specifies throwing generic Error objects, but project guidelines require using AppError with error codes. This is a CONCERN that needs to be addressed."
```

### In Developer Agent

```
Agent: "Before implementing, let me understand project conventions..."
*Reads .sdd/project-guidelines.md*
Agent: "The project uses snake_case for file names and PascalCase for classes. I'll follow these patterns in my implementation..."
```

## Integration with SDD Workflow

This skill integrates with the broader SDD workflow:

- **Phase 2 (Design):** Technical architect reads guidelines before designing
- **Phase 2 Review:** Design reviewer validates guidelines compliance
- **Phase 3 (Implement):** Developer follows guidelines during coding
- **Phase 4 (Review):** Reviewer verifies implementation follows guidelines

Project guidelines ensure consistency across all phases and all agents working on a project.
