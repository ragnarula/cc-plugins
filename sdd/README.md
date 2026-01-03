# SDD (Spec Driven Development) Plugin

A Claude Code plugin implementing Spec Driven Development methodology - a structured approach to software development that combines the rigor of upfront specification with the flexibility of iterative implementation.

## Overview

SDD synthesizes best practices from waterfall (rigorous planning), agile (fast feedback), TDD (test-first discipline), and BDD (business clarity) while leveraging AI to make specifications practical and comprehensive.

**Core Principle:** Write the specification first. Make it executable. Keep it living.

## Features

- **Specification Phase** (`/specify`): Define what needs to be built with clarity and precision
- **Design Phase** (`/design`): Plan how to implement the specification with architectural decisions
- **Implementation Phase** (`/implement`): Build the system with TDD, automated reviews, and progress tracking

## Structure

```
.claude-plugin/
  plugin.json           # Plugin metadata
agents/
  technical-analyst.md  # Requirements engineering specialist
  spec-reviewer.md      # Specification validator
  technical-architect.md # Design and architecture specialist
  design-reviewer.md    # Design validator
  developer.md          # Implementation specialist (TDD)
  reviewer.md           # Code review specialist
commands/
  specify.md            # /specify command
  design.md             # /design command
  implement.md          # /implement command
skills/
  sdd/
    SKILL.md            # SDD methodology documentation
    templates/          # Document templates
```

## Usage

### 1. Specify a Feature
```
/specify user-authentication "Allow users to log in with email and password"
```
Creates a specification document through stakeholder interviews, then validates feasibility.

### 2. Design the Implementation
```
/design user-authentication
```
Creates an architectural design with components, APIs, test strategy, and task breakdown.

### 3. Implement the Feature
```
/implement user-authentication
```
Implements the feature phase-by-phase with TDD, continuous validation, and automated code reviews.

## Key Principles

1. **Specification as Contract** - The spec defines success and guides all decisions
2. **Executable Specifications** - If you can't verify it, you can't specify it
3. **Living Documentation** - Specifications evolve with understanding
4. **Test-First Implementation** - Tests are written WITH implementation, not after
5. **No Test Stubs** - All tests must be fully implemented (tracked if unavoidable)
6. **No Dead Code** - Clean up unused code, track intermediate code in design docs

## Installation

Add this plugin to your Claude Code plugins directory or install from the marketplace.

## Version

0.1.2
