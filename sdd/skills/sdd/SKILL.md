---
name: sdd (Spec Driven Development)
description: This skill outlines how to follow the spec driven development workflow. The workflow is non-negotiable and must be followed for sdd or Spec Driven Development.
version: 0.1.0
---

# Spec Driven Development (SDD)

## Practical Guidelines

### Project Structure and Paths

All SDD artifacts live in the `.sdd/` folder at the repository root. Use these exact paths:

| Variable | Path |
|----------|------|
| `SDD_FOLDER` | `.sdd/` |
| `SDD_PROJECT_FOLDER` | `.sdd/[FEATURE]/` |
| `SDD_SPECIFICATION_DOCUMENT` | `.sdd/[FEATURE]/specification.md` |
| `SDD_DESIGN_DOCUMENT` | `.sdd/[FEATURE]/design.md` |
| `SDD_PROJECT_GUIDELINES` | `.sdd/project-guidelines.md` |

Where `[FEATURE]` is the kebab-case name of the feature (e.g., `user-authentication`, `shopping-cart`).

### Templates

- `SDD_TEMPLATE_SPECIFICATION` located in `templates/specification.template.md` used for initial requirements gathering
- `SDD_TEMPLATE_DESIGN` located in `templates/design.template.md` used for design documents
- `SDD_TEMPLATE_PROJECT_GUIDELINES` located in `templates/project-guidelines.template.md` used for project-specific conventions

### Project Guidelines

The `SDD_PROJECT_GUIDELINES` file (`.sdd/project-guidelines.md`) contains project-specific conventions that agents MUST follow in all phases. This file can:

1. **Reference existing documentation** - List paths to docs, READMEs, or other files containing conventions
2. **Define inline guidelines** - Specify conventions directly in the file

You MUST read this file during exploration and apply these conventions to architectural decisions.

## Processes

You **MUST** explore the code base using tools like Read, Glob etc before doing **ANY** of the below.
You **MUST** understand project guidelines starting with the file [SDD_PROJECT_GUIDELINES]

### Creating

Do this when a user asks to create a specification or design

You MUST create the required document in the relevant feature specific folder in the `.sdd/` folder at the root of the project

**Examples**

**If** the user asks to create a **specification** for user authentication **then** copy `templates/specificationtemplate.md` to `.sdd/user-authentication/specification.md` if it doesn't already exist.

**If** the user asks to create a **design** for user authentication **then** copy `templates/design.template.md` to `.sdd/user-authentication/specification.md` if it doesn't already exist.

### Specifying

Your **GOAL** is to complete all parts of the specification template for the feature.
You **MUST** ask the user questions about the feature they are trying to implement

**Probe vague answers relentlessly** - Ask for specific metrics, edge cases, and priorities. Challenge assumptions and explore alternatives. Don't accept "fast", "secure", or "user-friendly" without measurable criteria.

You **MUST** complete [SDD_SPECIFICATION_DOCUMENT] **FULLY** for the feature

### Designing

Your **GOAL** is to complete all parts of the design template for the feature

You **MUST** read the relevant [SDD_SPECIFICATION_DOCUMENT] for the feature

You **MUST** identify components required to implement the feature in the specification

#### Component Identification

For each component, document:
- **Modified**: Current behavior, what changes, dependencies, how to test
- **Added**: Single responsibility, consumers, location, requirements satisfied, tests

Keep components focused (single responsibility, minimal coupling, explicit dependencies). Define public interfaces and error handling. Avoid over-engineering for future needs.

#### API Design (When Needed)

**Design documents describe contracts, not code.**
API designs should:
- Describe operations conceptually (what they do, inputs, outputs, errors)
- Define data shapes and validation rules in prose or simple schemas
- Specify error conditions and expected behaviors
- Document constraints and invariants

API designs should NOT include:
- Code samples or function implementations
- Language-specific syntax (unless illustrating a non-functional requirement)
- Internal implementation logic
- Concrete class/function signatures beyond naming

**Exception:** Include code samples ONLY when they illustrate specific non-functional requirements:
- Serialization formats (JSON structure, protocol buffers)
- Concurrency patterns (mutex usage, async boundaries)
- Performance-critical algorithms (when the algorithm IS the requirement)
- Protocol specifics (wire format, handshake sequences)

**Example - GOOD (conceptual):**
> The `addToCart` operation accepts a product identifier and quantity. It validates the product exists and quantity is positive. On success, returns the updated cart. On failure, returns an error indicating whether the product was not found or quantity was invalid.

**Example - BAD (implementation leakage):**
```python
def add_to_cart(product_id: str, quantity: int) -> Cart:
    product = self.product_repo.get(product_id)
    if not product:
        raise ProductNotFoundError(product_id)
    ...
```

#### Test Strategy

Plan system-level testing beyond component tests: integration paths, E2E user journeys, performance/security testing needs, and required test data/infrastructure.

#### Task Breakdown

- Group into logical phases ordered by dependencies
- Each task must have clear completion criteria
- Testing happens WITH implementation, not after
- Every requirement must map to tasks

#### Write the design

**Fill the design template**
- You will be given the path to the new design file
- Reference the **sdd** skill for the standard design template structure [SDD_TEMPLATE_DESIGN]
- Follow the template structure exactly
- Ensure every section is complete and detailed
- Link requirements to components to tasks for full traceability
- Always save the document once you've finished designing. **Never** skip this step

**Ensure requirement coverage**
- Every functional requirement must map to one or more components
- Every non-functional requirement must map to implementation decisions
- Every requirement must map to one or more tasks
- Use the Requirements Validation section to verify complete coverage
- No requirement should be left unaddressed in the design
- If a requirement cannot be addressed, document it in Feasibility Review

#### Design Quality Standards

A complete design document must have:
- ✅ **Link to specification** via the Linked Specification field
- ✅ **Architecture overview** explaining current context and proposed changes
- ✅ **All requirements traced** to components via Requirements References
- ✅ **All components defined** with clear descriptions and locations
- ✅ **Test strategy documented** beyond component-level tests
- ✅ **Risks identified** with mitigation strategies
- ✅ **Tasks organized** into logical phases with dependencies
- ✅ **Requirements validation** showing every requirement maps to tasks
- ✅ **No TBDs or ambiguities** in the final design
- ✅ **Standard structure** following [SDD_TEMPLATE_DESIGN] exactly
- ✅ **Project guidelines compliance** if SDD_PROJECT_GUIDELINES exists

### Refining

When asked to refine a specification or design:
1. Read existing documents and linked specification thoroughly
2. Identify gaps, inconsistencies, or new requirements
3. Explore codebase for changed context or new patterns
4. Ask stakeholder about changed priorities or constraints
5. Update documents while maintaining template structure
6. Verify all requirements still map to components and tasks

### Implementing

**CRITICAL:** You must read the design document, specification, and project guidelines before starting any implementation.

#### Before Writing Any Code

Read the design, specification, existing code, and documentation thoroughly. If anything is unclear or ambiguous, ask before guessing.

#### When implementing a feature:

1. **Read and understand the design**
   - Read the design document and linked specification
   - Understand all tasks and which phase you are implementing
   - Identify prerequisites or dependencies

2. **Read project guidelines**
   - Check for `.sdd/project-guidelines.md` (SDD_PROJECT_GUIDELINES)
   - Read all referenced documentation files
   - Note error handling, logging, naming, and testing conventions
   - **CRITICAL** These conventions MUST inform your implementation decisions

3. **Set up the feature branch**
   - Create a feature branch for the current phase
   - Use a descriptive branch name (e.g., `feature/auth-phase-1`)

4. **Implement task by task**
   - Work through tasks in order as specified in the design
   - For each task:
     a. Write tests first (TDD when appropriate)
     b. Implement the code to pass tests
     c. Run linters and formatters
     d. Run the full test suite
     e. Commit the completed task with a clear message
     f. Update the task status in the design document
   - Do NOT skip ahead or batch multiple tasks into one commit

5. **Validate continuously** - Build, lint, and test after each task. Fix issues immediately.

6. **Track progress** - Mark tasks complete in design document. Document deviations and issues.

7. **Complete the phase** - All tasks done, tests passing, code linted. Wait for merge before next phase.

#### Dead Code

- Any dead code introduced in intermediate phases **MUST** be tracked in the design document
- All dead code **MUST** be used by the end of the final phase

#### Stubs

- Any stub implementations **MUST** be tracked in the design document
- All stubs **MUST** be implemented or removed by the end of the final phase

### Reviewing

The user can ask to review a specification, design or implementation. Follow the process below and produce a report for the user at the end.

**CRITICAL**: You MUST use the Task tool to create a subagent for the review.

#### Common Review Steps

1. Read specification, design, and project guidelines (if exists)
2. Verify requirements traceability and coverage
3. Check for edge cases and architectural fit
4. Validate against project conventions (error handling, logging, naming, testing)

#### Specification Review

**Focus areas:**
- Verify achievability and dependencies
- Ensure requirements are testable and measurable (not implementation details)
- Check for conflicts with existing functionality
- Validate scope is appropriate for single iteration

**Abstraction level check:**

GOOD (stays at specification level):
- "Users must be able to search products by name"
- "Search results must return within 500ms for 95th percentile"

BAD (contains implementation details):
- "Use Elasticsearch for product search"
- "Create a ProductSearchService class"

**Red flags:**
- Implementation details masquerading as requirements
- Vague/untestable requirements
- Unrealistic performance expectations
- Dependencies on unavailable services
- Requirements that assume non-existent functionality

#### Design Review

**Focus areas:**
- All requirements traced to components and tasks
- No implementation leakage (describe contracts conceptually, not code)
- Tests included WITH tasks, not deferred to later phases
- Architectural decisions fit existing codebase patterns
- Project guidelines compliance (if SDD_PROJECT_GUIDELINES exists)

**Task-level test verification:**
- Each task must have a "Tests:" field referencing specific test cases
- No separate "add tests" tasks or testing phases
- All component test cases must be assigned to tasks

**Example of GOOD task structure:**
```
- Task 1: Implement CartService.addItem()
  - Status: Backlog
  - Add item to cart with quantity validation
  - Tests: TEST-CART-ADD-VALID, TEST-CART-ADD-INVALID-QTY
```

**Example of BAD task structure:**
```
Phase 1: Implement CartService
Phase 2: Add unit tests for CartService  ← VIOLATION
```

**Red flags:**
- Requirements not traced to components/tasks
- Code samples in API design sections
- Separate "add tests" phases
- TBDs or ambiguities
- Architectural decisions conflicting with existing patterns
- Missing risk assessment

#### Implementation Review

**Diff analysis:**
- Run `git diff main...HEAD` to understand scope
- Verify all design tasks are represented
- Check for changes that don't correspond to any task

**Design validation:**
- Verify implementation matches design tasks
- Check that APIs and interfaces match design contracts
- Flag any undocumented deviations
- If design was altered, verify workarounds are documented

**Check for stubs:**
- Search for: `skip`, `todo`, `pending`, `@pytest.mark.skip`, `pass` in test functions, placeholder assertions
- **Intermediate phases**: Stubs acceptable only if tracked in design document
- **Final phase**: No stubs allowed

**Check for dead code:**
- Unused imports, variables, or functions
- Commented-out code
- **Intermediate phases**: Dead code acceptable only if tracked in design document
- **Final phase**: No dead code allowed

**Quality gates:**
- Run all tests (unit, integration, e2e)
- Run linters and formatters
- Build/compile the project
- Verify code follows documented practices

**Red flags:**
- Implementation doesn't match design
- Requirements removed without justification
- New code without tests
- Untracked stubs or dead code (in final phase)
- Failing tests or linting errors
- Undocumented deviations from design
- Security vulnerabilities

#### Quality Standards (All Reviews)

A thorough review must verify:
- ✅ Requirements coverage complete
- ✅ Tests adequate and passing
- ✅ No TBDs or ambiguities
- ✅ Project guidelines followed
- ✅ Risks identified with mitigations
- ✅ All stubs and dead code tracked (intermediate) or resolved (final)
