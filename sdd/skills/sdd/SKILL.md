---
name: sdd (Spec Driven Development)
description: This skill outlines how to follow the spec driven development workflow. The workflow is non-negotiable and must be followed for sdd or Spec Driven Development. Use this for writing, refining and reviewing specs, specifications, designs, tasks, test and implementations.
version: 0.1.26
---

# Spec Driven Development (SDD)

## Practical Guidelines

### Project Structure and Paths

All SDD artifacts live in the `.sdd/` folder at the repository root. Use these exact paths:

| Variable | Path |
|----------|------|
| `SDD_FOLDER` | `.sdd/` |
| `SDD_INDEX` | `.sdd/index.md` |
| `SDD_PROJECT_FOLDER` | `.sdd/[FEATURE]/` |
| `SDD_SPECIFICATION_DOCUMENT` | `.sdd/[FEATURE]/specification.md` |
| `SDD_DESIGN_DOCUMENT` | `.sdd/[FEATURE]/design.md` |
| `SDD_PROJECT_GUIDELINES` | `.sdd/project-guidelines.md` |

Where `[FEATURE]` is the kebab-case name of the feature (e.g., `user-authentication`, `shopping-cart`).

### Templates

- `SDD_TEMPLATE_INDEX` located in `templates/index.template.md` used for feature index
- `SDD_TEMPLATE_SPECIFICATION` located in `templates/specification.template.md` used for initial requirements gathering
- `SDD_TEMPLATE_DESIGN` located in `templates/design.template.md` used for design documents
- `SDD_TEMPLATE_PROJECT_GUIDELINES` located in `templates/project-guidelines.template.md` used for project-specific conventions

### Project Guidelines

The `SDD_PROJECT_GUIDELINES` file (`.sdd/project-guidelines.md`) contains project-specific conventions that agents MUST follow in all phases. This file can:

1. **Reference existing documentation** - List paths to docs, READMEs, or other files containing conventions
2. **Define inline guidelines** - Specify conventions directly in the file

You MUST read this file during exploration and apply these conventions to architectural decisions.

### Domain Skills

After exploring the codebase and understanding the task, identify which domain skills apply:

- **distributed-systems**: Multiple services, network coordination, eventual consistency
- **low-level-systems**: Memory management, performance-critical, OS interfaces
- **security**: Auth, untrusted input, sensitive data, compliance
- **infrastructure**: Cloud resources, IaC, networking, disaster recovery
- **devops-sre**: CI/CD, deployment, observability, SLOs
- **data-engineering**: Pipelines, ETL, schema evolution, data quality
- **api-design**: Public/internal APIs, versioning, contracts

Load relevant skills and apply their mindset and practices throughout specification, design, and review phases.

## Processes

You **MUST** explore the code base using tools like Read, Glob etc before doing **ANY** of the below.
You **MUST** understand project guidelines starting with the file [SDD_PROJECT_GUIDELINES]

### Creating

Do this when a user asks to create a specification or design

You MUST create the required document in the relevant feature specific folder in the `.sdd/` folder at the root of the project

**Maintain the index:**
1. If `.sdd/index.md` doesn't exist, create it from `templates/index.template.md`
2. Add a row for the new feature (newest entries at top, ordered by date)
3. Update the status as the feature progresses through Draft → Approved → Implemented

**Examples**

**If** the user asks to create a **specification** for user authentication **then** copy `templates/specification.template.md` to `.sdd/user-authentication/specification.md` if it doesn't already exist.

**If** the user asks to create a **design** for user authentication **then** copy `templates/design.template.md` to `.sdd/user-authentication/design.md` if it doesn't already exist.

### Specifying

Your **GOAL** is to complete all parts of the specification template for the feature.

**Scope:** A single specification should represent approximately 1 day of implementation work. If the feature is larger, break it into multiple specifications. During the discovery interview, sense check the scope and suggest splitting if necessary.

**Template guidance:**
- Follow the template structure as defined in [SDD_TEMPLATE_SPECIFICATION]
- Sections marked "optional" or "if needed" can be omitted entirely if not applicable
- Do NOT add new sections that aren't in the template

#### Process

**Phase 1: Discovery Interview**

Interview the user about their idea or brief. Keep asking questions until you can unambiguously fill out every section of the template. Don't ask about template sections directly - ask about their problem, users, and goals.

- What problem are they solving? Why does it matter?
- Who experiences this problem? How do they cope today?
- What does success look like? How will they know it's working?
- What are the boundaries? What's explicitly not included?
- What could go wrong? What are the edge cases?
- How will they validate the feature works? What steps will they take?
- What would they do in the UI/CLI to verify each requirement is met?

**Probe vague answers relentlessly** - Don't accept "fast", "secure", or "user-friendly" without measurable criteria. Keep questioning until requirements are specific and testable.

**NFRs are optional** - Only include non-functional requirements when there are genuine, measurable quality constraints (e.g., specific latency targets, compliance requirements). Most features don't need them.

**Phase 2: Write the Specification**

Once you have enough information to fill out every section unambiguously, write the complete specification in one pass. Do not ask further questions during this phase.

You **MUST** complete [SDD_SPECIFICATION_DOCUMENT] **FULLY** for the feature

### Designing

Your **GOAL** is to complete all parts of the design template for the feature.

**Purpose:** The design document is a complete handover document. Anyone on the team should be able to pick it up and carry out the implementation without needing to ask clarifying questions.

**Level of detail:** Include enough detail to enable handover to another team member, but not so much that you replicate the implementation in the document. Describe *what* and *why*, not *how* at the code level.

**Template guidance:**
- Follow the template structure as defined in [SDD_TEMPLATE_DESIGN]
- Sections marked "optional" or "if needed" can be omitted entirely if not applicable
- Do NOT add new sections that aren't in the template

#### Process

**Phase 1: Research**

Read and understand before designing:
- Read the specification thoroughly
- **Extract and list ALL functional and non-functional requirements by ID** - create a working checklist
- Explore the existing codebase for patterns, conventions, and integration points
- Read project guidelines if they exist

**Phase 2: Design**

Once you understand the requirements and codebase:

1. **Requirements Enumeration Checkpoint** (MANDATORY before writing components)
   - Create a checklist of every FR and NFR from the specification
   - For each requirement, identify which component(s) will address it
   - If a requirement cannot be mapped to a component, you must either:
     a. Add a new component to address it
     b. Document it in Feasibility Review with justification why it cannot be addressed
   - **Do NOT proceed until every requirement has a component assignment**

2. **Write the design document**
   - Work through components systematically
   - As you define each component, verify its Requirements References are complete
   - Cross-check against your requirements checklist as you go
   - Do NOT proceed to Task Breakdown until all requirements are mapped to components

3. **Verify requirements coverage BEFORE finalizing**
   - Cross-check every requirement from the specification has task coverage
   - If any requirement is missing task coverage, add tasks to cover it
   - **A design with unmapped requirements is incomplete and must not be submitted**

4. **QA Feasibility Analysis**
   For each QA scenario in the specification:
   - Can the user complete all steps with functionality in this design?
   - If not, document **white-box setup** required:
     - What manual manipulation is needed (e.g., insert DB records, call internal APIs)
     - Why it's needed (what functionality is missing/out of scope)
     - Is this acceptable or should scope change?
   - White-box setup should be planned, not discovered during QA

You **MUST** identify components required to implement the feature in the specification

#### Component Identification

For each component, document:
- **Modified**: Current behavior, what changes, dependencies, test scenarios (Given/When/Then)
- **Added**: Single responsibility, consumers, location, requirements satisfied, test scenarios (Given/When/Then)
- **Used**: Existing components required as-is for implementation (document what it provides and why it's needed)

Keep components focused (single responsibility, minimal coupling, explicit dependencies). Define public interfaces and error handling. Avoid over-engineering for future needs.

#### API Design (When Needed)

**Design documents describe contracts, not code.**
API designs should:
- Describe operations conceptually (what they do, inputs, outputs, errors)
- Define data shapes and validation rules in prose or simple schemas
- Specify error conditions and expected behaviors
- Document constraints and invariants
- Show Interfaces

API designs should NOT include:
- Code of function implementations
- Language-specific syntax (unless illustrating a non-functional requirement)
- Internal implementation logic

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

#### Test Scenarios

**Tests verify acceptance criteria from requirements.**

Each test must trace to an acceptance criterion defined in a requirement (FR-XXX). No acceptance criterion = no test.

**Scenario format:** Given/When/Then
- **Given**: Initial state
- **When**: Action performed
- **Then**: Expected outcome (the acceptance criterion)


#### Instrumentation (optional)

Only needed if NFRs require observability. Skip for typical features.

#### Task Breakdown

- Group into logical phases ordered by dependencies
- Each task must have clear completion criteria
- Each task must specify which requirements it fulfills using `[feature:REQ-ID]` format
- Each task must reference which test scenarios (TS-IDs, ITS-IDs, E2E-IDs) it implements
- Testing happens WITH implementation, not after
- Every requirement must map to tasks (and vice versa)

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
- Every requirement must map to one or more tasks
- Verify complete coverage by cross-checking against specification
- No requirement should be left unaddressed in the design
- If a requirement cannot be addressed, document it in Feasibility Review

#### Design Quality Standards

A complete design document must have:
- ✅ **Link to specification** via the Linked Specification field
- ✅ **Architecture overview** explaining current context and proposed changes
- ✅ **Components defined** (Modified/Added) with requirements references and test scenarios
- ✅ **Tasks organized** into logical phases referencing requirements and test scenarios
- ✅ **Risks identified** with mitigation strategies
- ✅ **No TBDs or ambiguities** in the final design
- ✅ **QA feasibility analyzed** - white-box setup documented for each scenario

Optional sections (include only if applicable):
- Integration Test Scenarios (if multi-component interactions)
- E2E Test Scenarios (if complete user workflows need testing)
- Instrumentation (if NFRs require observability)

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

#### Code Comments

- Only add comments where the logic isn't self-evident
- Prefer self-documenting code over comments
- **NEVER add SDD artifact references in code or tests** - no FR-XXX, TS-XX, requirement IDs, or scenario IDs in comments, docstrings, or test names

**BAD - Do NOT do this:**
```python
# Implements FR-001
def add_to_cart(): ...

def test_add_item():
    """Verifies TS-01"""
```

**GOOD - Clean code without SDD references:**
```python
def add_to_cart(): ...

def test_add_item_increases_quantity(): ...
```

#### Dead Code

- Any dead code introduced in intermediate phases **MUST** be tracked in the design document
- All dead code **MUST** be used by the end of the final phase

#### Stubs

- Any stub implementations **MUST** be tracked in the design document
- All stubs **MUST** be implemented or removed by the end of the final phase

### Auto-Implement

Use this process when asked to auto-implement a design. Each phase is implemented as a stacked PR.

**CRITICAL**: You MUST use the Task tool to launch subagents for implementation and review. Do NOT implement or review directly - always delegate to subagents.

#### Process

For each phase in the design (in order):

1. **Create phase branch**
   - Branch from previous phase branch (or main for phase 1)
   - Name: `feature/<feature-name>-phase-<N>`

2. **Implementation subagent** (MUST use Task tool)
   - Launch Task tool with implementation prompt for this phase
   - Subagent implements all tasks in the phase
   - Subagent commits after each task

3. **Create/update stacked PR**
   - Create PR from phase branch to previous phase branch (or main for phase 1)
   - PR description includes phase number, goal, and requirements covered
   - On subsequent rounds, push commits to update the existing PR

4. **Review subagent** (MUST use Task tool)
   - Launch Task tool with review prompt for this phase
   - Subagent reviews the implementation against the design
   - Returns list of issues (P0, P1, P2)
   - Add review report as PR comment

5. **Fix loop**
   - If P0 or P1 issues exist:
     a. Launch Task tool with implementation subagent to fix issues
     b. Push fixes to PR
     c. Launch Task tool with review subagent again
     d. Add new review report as PR comment
     e. Repeat until no P0/P1 issues remain

6. **Next phase**
   - Move to next phase, branching from current phase branch
   - Repeat steps 1-5

#### Subagent Prompts

**Implementation subagent prompt:**
> Use SDD to implement phase [N] of [design-path].

**Review subagent prompt:**
> Use SDD to review the implementation of phase [N] for [design-path].

### Reviewing

The user can ask to review a specification, design or implementation. Follow the process below and produce a report for the user at the end.

**CRITICAL**: You MUST use the Task tool to create a subagent for the review.

#### Common Review Steps

1. Read specification, design, and project guidelines (if exists)
2. Load relevant domain skills based on the feature (e.g., security, api-design, distributed-systems) and apply their review criteria
3. Verify requirements traceability and coverage
4. Check for edge cases and architectural fit
5. Validate against project conventions (error handling, logging, naming, testing)

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
- No implementation leakage (describe contracts conceptually, not code)
- Tests included WITH tasks, not deferred to later phases
- Architectural decisions fit existing codebase patterns
- Only check for optional sections (Integration Tests, E2E Tests, Instrumentation) if they're applicable to the feature

**QA feasibility validation:**
- Every QA scenario from spec has feasibility analysis
- White-box setup is explicitly documented (not discovered during QA)
- All white-box setup is either:
  a. Acceptable (functionality intentionally out of scope)
  b. Covered by tasks (will be implemented)
  c. Flagged as gap requiring scope change

**Requirements validation (perform during review):**
- Every requirement from the specification maps to at least one task
- Every task references the requirements it fulfills
- No orphan requirements (defined but never addressed)

**Test scenario validation (perform during review):**
- Every test scenario maps to at least one task
- Each task has a "Test Scenarios:" field referencing specific scenario IDs (TS-XX, ITS-XX, E2E-XX)
- No separate "add tests" tasks or testing phases
- No orphan scenarios (defined but never assigned to tasks)

**Example of GOOD task structure:**
```
**Task 1: Implement CartService.addItem()**
- Status: Backlog
- Requirements: [shopping-cart:FR-001], [shopping-cart:FR-002]
- Test Scenarios: [shopping-cart:CartService/TS-01], [shopping-cart:ITS-01]
- Details:
  fn addItem(productId: string, quantity: int) -> Cart
    throws: ProductNotFound, InvalidQuantity
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
- Test scenarios missing Given/When/Then structure

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

**Test verification (read the actual test code):**
- For each test scenario defined in the design, find and read its implementation
- Verify the test actually exercises the acceptance criterion (not just asserting trivial values)
- Check that tests would actually fail if the requirement was not implemented
- Every test scenario from the design must have a corresponding test in the code

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
- Run all tests
- Run linters and formatters
- Build/compile the project

**Red flags:**
- Test scenarios from design missing in code
- Tests that wouldn't fail if the requirement was removed
- Implementation doesn't match design
- Undocumented deviations from design
- Untracked stubs or dead code (in final phase)
- Security vulnerabilities

#### Quality Standards (All Reviews)

A thorough review must verify:
- ✅ Every test scenario from the design is implemented (verified by reading the test code)
- ✅ Tests actually exercise acceptance criteria (would fail if requirement not implemented)
- ✅ No TBDs or ambiguities
- ✅ Project guidelines followed
- ✅ Risks identified with mitigations
- ✅ All stubs and dead code tracked (intermediate) or resolved (final)

#### Review Severity Levels

All review findings MUST be categorized by severity. Reports must list findings grouped by severity, with P0 issues first.

**P0 - Blocking (must fix before approval):**
- Test scenario from design not implemented
- Test that doesn't actually verify its acceptance criterion (trivial or fake)
- Failing tests
- Security vulnerabilities
- Requirements not covered by implementation

**P1 - High (should fix before approval):**
- Undocumented deviations from design
- Untracked stubs or dead code in final phase
- QA scenario has no feasibility analysis
- Undocumented white-box setup discovered

**P2 - Medium (fix recommended):**
- Minor architectural inconsistencies
- Missing risk mitigations

**P3 - Low (nice to have):**
- Style inconsistencies not caught by linter
- Documentation improvements
- Minor naming convention deviations

**Report format:**
Reviews MUST present findings in severity order:
```
## P0 - Blocking
- [Finding description and location]

## P1 - High
- [Finding description and location]

## P2 - Medium
- [Finding description and location]

## P3 - Low
- [Finding description and location]
```

A review with any P0 findings MUST recommend rejection until resolved.
