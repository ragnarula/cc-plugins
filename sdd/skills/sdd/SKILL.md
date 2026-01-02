---
name: sdd (Spec Driven Development)
description: This skill outlines how to follow the spec driven development workflow. The workflow is non-negotiable and must be followed for sdd or Spec Driven Development.
version: 0.1.0
---

# Spec Driven Development (SDD)

## Overview

Spec-Driven Development is a modern software development methodology that synthesizes the best practices from decades of software engineering evolution—from waterfall's rigorous planning to agile's adaptability, TDD's test-first discipline, and BDD's business clarity—while leveraging AI to make specifications both powerful and practical.

## Core Principle

**Write the specification first. Make it executable. Keep it living.**

In SDD, the specification is not just documentation—it is the single source of truth that drives design, implementation, testing, and validation. With AI assistance, specifications become easy to write, comprehensive to cover edge cases, and practical to maintain.

## The Evolution: What We Kept, What We Left Behind

### From Waterfall (1970s-1990s)
**Kept:**
- Upfront planning and clear requirements gathering
- Comprehensive documentation as a contract
- Structured phases with clear deliverables
- Specification as the foundation for design

**Left Behind:**
- Inflexibility to changing requirements
- Long feedback cycles (months/years)
- Late integration and testing
- Assumption that requirements are frozen

### From Agile (2000s-2010s)
**Kept:**
- Iterative and incremental development
- Fast feedback loops (days/weeks)
- Adaptability to changing requirements
- Continuous collaboration with stakeholders
- Working software as the measure of progress

**Left Behind:**
- "No documentation" extremism
- "Just start coding" without design
- Scope creep masked as flexibility
- Over-reliance on tacit knowledge

### From TDD (2000s-2020s)
**Kept:**
- Write tests before implementation
- Tests as executable specifications
- Confidence in refactoring
- Design emerges from test constraints
- Red-Green-Refactor cycle

**Left Behind:**
- Excessive focus on unit tests over integration
- Brittle tests coupled to implementation details
- Slow initial velocity
- Tests as separate from specifications

### From BDD (2010s-2020s)
**Kept:**
- Business-readable specifications (Given-When-Then)
- Focus on behavior, not implementation
- Bridge between business and technical teams
- Specifications as living documentation
- Outside-in development approach

**Left Behind:**
- Verbose Gherkin overhead
- Tool complexity (Cucumber, SpecFlow, etc.)
- Specifications that duplicate test code
- Over-specification of UI details

## The SDD Workflow

### Phase 1: Specify

**Purpose:** Define what needs to be built with clarity and precision.

**Process:**
1. **Capture Requirements**
   - Define the problem to be solved
   - Identify the functional requirements
   - Identify the non-functional requirements
   - Explicity exclude anything out of scope
   - Document open questions

2. **Write the Specification**
   - Use natural language with precision
   - Structure: according to [SDD_TEMPLATE_SPECIFICATION] (See below)
   - Make it business-readable but technically complete
   - Include examples and counter-examples
   - Leverage AI to explore edge cases and ensure completeness

3. **Define Requirements**
   - Clear, testable conditions for "done"
   - Both positive and negative cases
   - Performance and quality attributes
   - Security and compliance requirements

4. **Review and Refine**
   - Stakeholder validation
   - Technical feasibility check
   - Completeness audit (use AI to identify gaps)
   - Risk assessment

**Deliverable:** A comprehensive specification document that answers:
- What problem are we solving and why?
- Who is it for and how will they use it?
- What are the functional requirements?
- What are the non-functional requirements?
- How will we know it's correct?

**AVOID**
- Showing APIs even as examples
- Requirements that users can never experience e.g. coding standards, testing styles/frameworks to use, architectural hints. These will be defined later.

### Phase 2: Design

**Purpose:** Plan how to implement the specification.

**Process:**
1. **Architectural Design**
   - Identify components and their responsibilities
   - Define interfaces and contracts
   - Choose patterns and technologies
   - Consider scalability and maintainability

2. **API Design**
   - Define public interfaces from the specification
   - Design data models and schemas
   - Establish error handling strategies
   - Plan for versioning and evolution

3. **Test Strategy**
   - Determine test pyramid (unit/integration/e2e)
   - Identify critical paths requiring coverage
   - Plan for performance and security testing
   - Define test data requirements

4. **Implementation Plan**
   - Break down into incremental deliverables
   - Identify dependencies and risks
   - Establish checkpoints and validation gates
   - Plan for iterative refinement
   - explicitly ensure **all** requirements from the specification have a solution in the plan

**Deliverable:** A clear implementation roadmap that connects the specification to concrete technical decisions.

### Phase 3: Implement

**Purpose:** Build the system according to the specification.

**Process:**
1. **Write Executable Specifications**
   - Convert acceptance criteria into tests
   - Start with integration/behavior tests
   - Use specification language in test names and assertions
   - Ensure tests fail initially (Red)

2. **Implement to Pass Tests**
   - Write minimal code to satisfy specification
   - Follow the design from Phase 2
   - Keep implementation simple and clear
   - Make tests pass (Green)

3. **Refactor for Quality**
   - Improve code structure without changing behavior
   - Apply design patterns where beneficial
   - Optimize for readability and maintainability
   - Ensure all tests still pass (Refactor)

4. **Validate Against Specification**
   - Ensure all acceptance criteria are met
   - Check edge cases and error conditions
   - Verify performance and quality attributes
   - Conduct specification review

**Deliverable:** Working software that demonstrably satisfies the specification, with executable tests proving correctness.

### Phase 4: Evolve

**Purpose:** Maintain alignment between specification, implementation, and reality.

**Process:**
1. **Monitor and Learn**
   - Gather usage data and feedback
   - Identify gaps between specification and needs
   - Track technical debt and improvement opportunities
   - Measure against success criteria

2. **Update Specification**
   - Refine based on learnings
   - Add new requirements incrementally
   - Remove obsolete requirements
   - Keep specification as living documentation

3. **Refactor Implementation**
   - Align code with updated specification
   - Improve design as understanding deepens
   - Update tests to reflect new specifications
   - Maintain test coverage and quality

4. **Communicate Changes**
   - Update stakeholders on evolution
   - Document decisions and rationale
   - Maintain changelog and version history
   - Ensure team alignment

**Deliverable:** An evolving system where specification, implementation, and tests remain synchronized and reflect current reality.

## Key Principles

### 1. Specification as Contract
The specification is a binding contract between stakeholders and developers. It defines success and guides all decisions.

### 2. Executable Specifications
Specifications must be testable. If you can't verify it, you can't specify it.

### 3. Living Documentation
Specifications evolve with understanding. Dead documentation is waste; living documentation is essential.

### 4. AI-Assisted Completeness
Use AI to explore edge cases, identify gaps, generate test scenarios, and ensure specifications are comprehensive.

### 5. Iterative Refinement
Specifications don't need to be perfect upfront, but they must exist before implementation. Refine iteratively based on feedback.

### 6. Behavior Over Implementation
Specify what the system should do, not how it should do it. Preserve implementation flexibility.

### 7. Fail Fast on Specification
If the specification is unclear, ambiguous, or incomplete, stop. Don't start implementation hoping to figure it out later.

### 8. Test at the Right Level
Write tests at the level of the specification. Integration and behavior tests verify specifications; unit tests verify implementation details.

### 9. Minimum Viable Specification
Start with the core behavior and essential constraints. Add complexity only when needed.

### 10. One Source of Truth
The specification is the single source of truth. Code implements it. Tests verify it. Documentation derives from it.

## Common Anti-Patterns to Avoid

### Specification Anti-Patterns
- **Analysis Paralysis:** Spending weeks perfecting specifications before any code
- **Vague Specs:** "The system should be fast" without measurable criteria
- **Implementation Leakage:** Specifying internal implementation details
- **Unchanging Stone Tablets:** Refusing to update specifications as understanding evolves
- **Specification Theater:** Writing specs no one reads or validates against

### Implementation Anti-Patterns
- **Code-First:** Starting implementation before specification exists
- **Specification Ignorance:** Implementing without reading or understanding the spec
- **Test-After:** Writing tests after implementation instead of from specifications
- **Gold Plating:** Adding features not in the specification
- **Specification Drift:** Allowing implementation to diverge from specification without updating either

### Process Anti-Patterns
- **Waterfall Regression:** Treating SDD phases as sequential and inflexible
- **Agile Chaos:** Using "agile" as an excuse to skip specification
- **Test Obsession:** Focusing on test coverage metrics over specification coverage
- **Documentation Debt:** Letting specifications become stale and untrusted

## Practical Guidelines

### Project Structure

- **`.sdd` folder** All artifacts created during Spec-Driven Development live in a `.sdd` folder also referenced as `SDD_FOLDER`. **Notice** the '.' before the folder name. The folder should be prefixed with a '.'.
- **Folder-per-feature** Within the `SDD_FOLDER` create a sub folder for each features's specification, plan, and task documents to live together

### Templates

- `SDD_TEMPLATE_SPECIFICATION` located in `templates/specification.template.md` used for initial requirements gathering
- `SDD_TEMPLATE_DESIGN` located in `templates/design.template.md` used for design documents
- `SDD_TEMPLATE_PROJECT_GUIDELINES` located in `templates/project-guidelines.template.md` used for project-specific conventions

### Project Guidelines

The `SDD_PROJECT_GUIDELINES` file (`.sdd/project-guidelines.md`) contains project-specific conventions that agents must follow during the design phase. This file can:

1. **Reference existing documentation** - List paths to docs, READMEs, or other files containing conventions
2. **Define inline guidelines** - Specify conventions directly in the file

Agents read this file during exploration and apply these conventions to architectural decisions. The design-reviewer validates that designs comply with project guidelines.

### Leveraging AI in SDD

1. **Specification Generation:** Use AI to draft initial specifications from requirements
2. **Edge Case Discovery:** Ask AI to identify edge cases and failure scenarios
3. **Completeness Checking:** Have AI review specifications for gaps and ambiguities
4. **Test Generation:** Use AI to generate test scenarios from specifications
5. **Implementation Validation:** Ask AI to verify implementation matches specification
6. **Specification Refinement:** Use AI to improve clarity and precision
7. **Documentation Sync:** Leverage AI to keep specs, tests, and docs aligned

### Measuring SDD Success

**Specification Quality:**
- All requirements have acceptance criteria
- No ambiguous or untestable requirements
- Edge cases are documented
- Specifications are reviewed and approved

**Implementation Quality:**
- All acceptance criteria have passing tests
- No untested code paths
- Implementation aligns with design decisions
- Code is readable and maintainable

**Process Quality:**
- Specification exists before implementation starts
- Tests are written before production code
- Specifications are kept up-to-date
- Changes go through specification update process

**Outcome Quality:**
- Delivered system meets all acceptance criteria
- Few bugs in production (specification was complete)
- Easy to understand and modify (specification is clear)
- Stakeholder satisfaction (specification matched needs)


## Conclusion

Spec-Driven Development takes the wisdom of five decades of software methodology evolution and combines it with modern AI capabilities to create a pragmatic, powerful approach to building software:

- **Rigorous like Waterfall:** Clear specifications and planning upfront
- **Adaptive like Agile:** Iterative refinement and fast feedback
- **Confident like TDD:** Tests verify correctness automatically
- **Clear like BDD:** Business-readable specifications bridge stakeholders
- **Enhanced by AI:** Comprehensive, complete, and maintainable at scale

The result is software that is correct, maintainable, and aligned with stakeholder needs—delivered with the speed and flexibility modern development demands.

**Remember:** The specification is not overhead. It is the foundation. Write it first. Make it executable. Keep it living.
