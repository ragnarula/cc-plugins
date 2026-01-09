# SDD (Spec Driven Development) Plugin

A Claude Code plugin implementing Spec Driven Development methodology - a structured approach to software development that combines rigorous upfront specification with iterative implementation.

## Overview

SDD synthesizes best practices from waterfall (rigorous planning), agile (fast feedback), TDD (test-first discipline), and BDD (business clarity) while leveraging AI to make specifications practical and comprehensive.

**Core Principle:** Write the specification first. Design with traceability. Implement with tests.

## Workflow

### 1. Specify
Define what needs to be built with clarity and precision. The specification captures:
- Problem statement and beneficiaries
- Functional requirements (FR-XXX)
- Non-functional requirements (NFR-XXX)
- Explicit scope boundaries

### 2. Design
Plan how to implement the specification with full traceability:
- Architecture overview and technology decisions
- Component identification (Modified, Added, Used)
- Test scenarios in Given/When/Then format
- Task breakdown with requirement and scenario references

### 3. Implement
Build the system with TDD and continuous validation:
- Task-by-task implementation
- Tests written WITH implementation, not after
- Progress tracking in design document
- Requirement and scenario traceability in code comments

## Example Usage

**Note** If you really need to force use, you can prefix the exmaple prompts below with 'Use sdd to...'

### Creating a Specification
```
Create a specification for user-authentication
```
```
I need to specify a new feature for password reset functionality
```
```
Let's write a spec for adding shopping cart to the e-commerce app
```

The agent will interview you about the problem, users, and requirements before writing the specification to `.sdd/[feature-name]/specification.md`.

### Creating a Design
```
Create a design for user-authentication
```
```
Design the password-reset feature based on its specification
```
```
I'm ready to design the shopping-cart feature
```

The agent will read the specification, explore the codebase, and create a design document with components, test scenarios, and task breakdown.

### Implementing a Feature
```
Implement the user-authentication feature
```
```
Let's implement phase 1 of the password-reset design
```
```
Continue implementing shopping-cart from where we left off
```

The agent will follow the design document, implementing task-by-task with TDD.

### Reviewing Documents
```
Review the specification for user-authentication
```
```
Review the design for password-reset
```
```
Review the implementation of shopping-cart
```

### Refining Documents
```
Refine the user-authentication specification - we need to add OAuth support
```
```
Update the design for password-reset to handle rate limiting
```

### Setting Up Project Guidelines
```
Create project guidelines for this repository
```

Creates `.sdd/project-guidelines.md` to define project-specific conventions for error handling, logging, naming, and testing.

## Key Features

### Requirement Traceability
Every requirement is traced from specification through design to implementation:
```python
# Implements [user-authentication:FR-003] - Password must be hashed
def hash_password(password: str) -> str:
```

### Test Scenarios (Given/When/Then)
Component-level, integration, and E2E test scenarios with unique IDs:

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| TS-01 | Valid login | Registered user | Correct credentials submitted | Session token returned |

### Scenario Traceability
Test scenarios are traced from design to implementation:
```python
def test_valid_login():
    """Verifies [user-authentication:AuthService/TS-01]

    Given: A registered user with valid credentials
    When: User submits correct username and password
    Then: A valid session token is returned
    """
```

### Validation Sections
- **Requirements Validation**: Every requirement maps to tasks
- **Test Scenario Validation**: Every scenario maps to tasks (no orphans)

## Project Structure

```
.sdd/
  index.md                    # Feature index
  project-guidelines.md       # Project-specific conventions
  [feature-name]/
    specification.md          # What to build
    design.md                 # How to build it
```

## Plugin Structure

```
.claude-plugin/
  plugin.json                 # Plugin metadata (v0.1.11)
skills/
  sdd/
    SKILL.md                  # SDD methodology and processes
    templates/
      specification.template.md
      design.template.md
      index.template.md
      project-guidelines.template.md
  project-guidelines/
    SKILL.md                  # Guidelines reading process
```

## Key Principles

1. **Specification as Contract** - The spec defines success and guides all decisions
2. **Full Traceability** - Requirements and scenarios traced through code comments
3. **Test Scenarios First** - Define Given/When/Then before implementation
4. **Tests WITH Implementation** - No separate "add tests" phases
5. **No Orphan Scenarios** - Every scenario must be assigned to a task
6. **No Test Stubs** - All tests fully implemented (tracked if unavoidable)
7. **No Dead Code** - Track intermediate code, resolve by final phase

## ID Formats

| Type | Format | Example |
|------|--------|---------|
| Functional Requirement | `FR-XXX` | `FR-001` |
| Non-Functional Requirement | `NFR-XXX` | `NFR-001` |
| Component Test Scenario | `ComponentName/TS-XX` | `AuthService/TS-01` |
| Integration Test Scenario | `ITS-XX` | `ITS-01` |
| E2E Test Scenario | `E2E-XX` | `E2E-01` |

Fully-qualified format: `[feature-name:ID]` (e.g., `[user-authentication:FR-001]`)

## Version

0.1.11
