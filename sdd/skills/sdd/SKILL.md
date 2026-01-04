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

**Probe vague answers relentlessly:**
- User: "It should be fast"
- You: "What response time would meet your needs? Under what load? What happens if it's slower?"

- User: "It needs to be secure"
- You: "What are the specific security requirements? Authentication? Authorization? Data encryption? Compliance needs?"

- User: "Make it user-friendly"
- You: "What does user-friendly mean for this feature? What would make it frustrating? Who is the user and what's their technical skill level?"

**Challenge assumptions:**
- "You mentioned X must happen before Y - is that a hard requirement or could we support both orders?"
- "Why do we need this field? What would break if we didn't have it?"
- "Is this requirement really needed for MVP or could it come later?"

**Explore alternatives and tradeoffs:**
- "Have you considered approach A vs approach B? What are the tradeoffs?"
- "Would it be acceptable if we [simpler alternative] instead?"
- "What's more important - feature richness or time to market?"

**Dig into edge cases:**
- "What happens when [boundary condition]?"
- "How should the system behave if [error occurs]?"
- "What if the user tries to [unexpected action]?"

You **MUST** complete [SDD_SPECIFICATION_DOCUMENT] **FULLY** for the feature

### Designing

Your **GOAL** is to complete all parts of the design template for the feature

You **MUST** read the relevant [SDD_SPECIFICATION_DOCUMENT] for the feature

You **MUST** identify components required to implement the feature in the specification

#### Component Identification

**Modified Components:**
- What does this component do today?
- What needs to change and why?
- What requirements drive this change?
- What other components depend on this?
- How do we test the changes?

**Added Components:**
- What is the single responsibility of this new component?
- Who/what will call or use this component?
- Where should it live in the codebase?
- What requirements does it satisfy?
- How do we test it?

**Keep components focused:**
- Single responsibility principle
- Clear boundaries and interfaces
- Minimal coupling
- Document dependencies explicitly

**Define public interfaces:**
- What operations are exposed?
- What data models are used?
- What are the inputs and outputs?
- How are errors communicated?

**Establish conventions:**
- Error handling and validation patterns
- Request/response formats
- Authentication and authorization
- Versioning strategy

**Plan for evolution:**
- How can this API evolve without breaking clients?
- What backward compatibility is needed?
- How will deprecation work?

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

**Component-level tests are already defined in component sections. Here, plan system-level testing:**

**Test Pyramid:**
- Unit tests: What additional unit testing beyond components? Utilities? Helpers?
- Integration tests: What are the critical integration paths?
- E2E tests: What user journeys must work end-to-end?

**Coverage Strategy:**
- What are the critical paths that must have coverage?
- What performance testing is needed?
- What security testing is required?
- Are there accessibility requirements to test?

**Test Data:**
- What test data is required?
- Where will it come from?
- How do we maintain it?

**Test Feasibility:**
- What test infrastructure is missing and needs to be built first?
- What test data needs to be acquired or created?
- Are there blockers to testing that must be resolved?
 
 #### Task Breakdown

**Group into logical phases:**
- Phase 1 might be: Infrastructure setup and prerequisite work
- Phase 2 might be: Core components and their tests
- Phase 3 might be: Dependant components and their tests
- Each phase should have a clear goal
- Testing should be done along with implementation, **not** left to later

**Order by dependencies:**
- What must be done before other work can start?
- What can be parallelized?
- What are the checkpoints for validation?

**Keep tasks focused:**
- Each task should be clear and achievable
- Tasks should have clear completion criteria
- Avoid tasks that are too large or vague

**Map to requirements:**
- Ensure every requirement has tasks that implement it
- Use the Requirements Validation section to verify this

#### Write the design

**Fill the design template**
- You will be given the path to the new design file
- Reference the **sdd** skill for the standard design template structure [SDD_TEMPLATE_DESIGN]
- Follow the template structure exactly
- Ensure every section is complete and detailed
- Link requirements to components to tasks for full traceability
- Always save the document once you've finished designing. **Never** skip this step`

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

**Red flags in designs:**
- ❌ Components without requirement references
- ❌ Requirements without components or tasks implementing them
- ❌ Vague technology choices without justification
- ❌ Missing or incomplete test strategy
- ❌ No risk assessment or "no risks identified" without analysis
- ❌ Tasks without clear deliverables or completion criteria
- ❌ Designs that specify implementation details instead of architecture
- ❌ Incomplete requirements validation matrix
- ❌ "TBD" or "To be determined" anywhere
- ❌ Designs that don't explore the existing codebase first
- ❌ Designs that ignore project guidelines (error handling, logging, naming conventions)

### Refining

The user can ask to refine a specification, design or implementation

1. **Read the existing documents thoroughly**
   - Use Read tool to load the current specification and design if they exist
   - Understand what's already documented

2. **Read the linked specification**
   - Ensure you understand the requirements
   - Check for specification updates since design was created

3. **Identify gaps and inconsistencies**
   - Are there requirements not addressed in the design?
   - Are there new requirements since the original design?
   - Is the design inconsistent with the template [SDD_TEMPLATE_DESIGN]?
   - Are there missing risk assessments?

4. **Explore codebase for new context**
   - Has the codebase changed since the design was created?
   - Are there new patterns to follow?
   - Are there new constraints to consider?

5. **Ask stakeholder about preferences**
   - Use AskUserQuestion for architectural tradeoffs
   - Clarify if priorities or constraints have changed
   - Understand if the implementation revealed new information

6. **Update documents**
   - Use Write tool to update the specification or design file as required
   - Add missing sections or details
   - Update components, tasks, or requirements validation
   - Always stick to [SDD_TEMPLATE_DESIGN] [SDD_TEMPLATE_SPECIFICATION] structure

7. **Verify requirement coverage**
   - Check Requirements Validation section
   - Ensure all requirements still map to components and tasks

### Implementing

**CRITICAL:** You must read the design document and specification before starting any implementation. You must also read the codebase documentation before writing any code.

#### Before Writing Any Code

**Read extensively first:**
- Design document: Understand what you're building and why
- Specification: Understand the requirements you're satisfying
- Existing code: Understand patterns you must follow
- Documentation: Understand conventions and standards

**Ask if unclear:**
- If the design is ambiguous, ask before guessing
- If a pattern isn't documented, request documentation
- If you encounter a blocker, surface it immediately

#### When implementing a feature:

1. **Read and understand the design**
   - Read the design document thoroughly using the Read tool
   - Read the linked specification to understand the requirements
   - Understand all tasks in the Tasks section
   - Note which phase you are implementing
   - Identify any prerequisites or dependencies

2. **Read project guidelines**
   - Check for `.sdd/project-guidelines.md` (SDD_PROJECT_GUIDELINES)
   - If it exists, read it to understand project-specific conventions
   - Read all referenced documentation files listed in the guidelines
   - Note error handling, logging, naming, and testing conventions
   - **CRITICAL** These conventions MUST inform your implementation decisions

3. **Understand established patterns**
   - How are errors propagated and handled?
   - How is logging done?
   - How are modules structured?
   - How are tests structured?
   - What naming conventions are used?
   - What code style is expected?
   - **If you don't see clear guidelines for these patterns, insist that they be documented before proceeding**

4. **Set up the feature branch**
   - Create a feature branch for the current phase
   - Use a descriptive branch name (e.g., `feature/auth-phase-1`, `feature/cart-implementation`)
   - Ensure you're starting from the correct base branch

5. **Implement task by task**
   - Work through tasks in order as specified in the design
   - For each task:
     a. Write tests first (TDD when appropriate)
     b. Implement the code to pass tests
     c. Run linters and formatters
     d. Run the full test suite
     e. Commit the completed task with a clear message
     f. Update the task status in the design document
   - Do NOT skip ahead or work out of order
   - Do NOT batch multiple tasks into one commit

6. **Validate continuously**
   - Compile/build after every significant change
   - Run linters and formatters frequently
   - Run tests after every task completion
   - Fix issues immediately before moving on
   - Never leave the codebase in a broken state

7. **Track progress**
   - Mark tasks as complete in the design document
   - Record any implementation notes or deviations
   - Document any issues encountered and how they were resolved
   - Add a note in the design if implementation reveals necessary changes or follow up tasks, but do NOT erase

8. **Complete the phase**
   - Ensure all tasks in the phase are complete
   - Ensure all tests pass
   - Ensure code is properly formatted and linted
   - Create a final commit summarizing the phase if needed
   - Wait for the branch to be merged before starting the next phase

#### Dead Code

- Any dead code introduced in intermediate phases **MUST** be tracked in the design document
- All dead code **MUST** be used by the end of the final phase
- You **MUST** ensure all tracked dead code in the design document is eventually removed

#### Stubs

- Any stub implementations of functions or test **MUST** be tracked in the design document
- All stubs **MUST** be implemented or removed by the end of the final phase
- You **MUT** ensure all tracked stubs in the design document are eventually implemented

### Reviewing

The user can ask to review a specification, design or implementation. Follow the process below and produce a report for the user at the end.

**CRITICAL**: You MUST use the Task tool to create a subagent for the review. The subagent should follow the process below

#### Review Strategy
You **MUST** use the sdd skill.

**Read and understand both specification and design**
- Read the specification document first to understand requirements
- Read the design document thoroughly
- Note the linked specification reference
- Understand what was supposed to be designed

**Read project guidelines if they exist**
- Check for `.sdd/project-guidelines.md` (SDD_PROJECT_GUIDELINES)
- If it exists, read it to understand project-specific conventions
- Read all referenced documentation files listed in the guidelines
- Note error handling, logging, naming, and testing conventions
- These conventions will be used to validate design decisions

##### Specification Review
###### Feasibility Analysis

**Assess technical achievability:**
- Can each requirement be implemented with current capabilities?
- What new functionality would need to be built?
- Are there hard technical constraints that block requirements?

**Check dependency chain:**
- What must exist before this can be built?
- Are those dependencies available or planned?
- Should missing dependencies be called out as risks?

###### Specification Quality Check

**Validate the right abstraction level:**

GOOD (stays at specification level):
- "Users must be able to search products by name"
- "Search results must return within 500ms for 95th percentile"
- "The system must support filtering by category"

BAD (contains implementation details):
- "Use Elasticsearch for product search"
- "Create a ProductSearchService class"
- "Store search indices in Redis"

**Check requirement clarity:**
- Can each requirement be verified as met or not met?
- Are edge cases clear without prescribing solutions?
- Are non-functional requirements measurable?

###### Consistency Analysis

**Check against existing functionality:**
- Search for similar features in the codebase
- Identify potential conflicts or overlaps
- Note integration considerations

**Validate assumptions:**
- Are implicit assumptions about the system correct?
- Does the spec author understand current capabilities?

###### Review Quality Standards

A thorough specification review must verify:
- **Achievability** - Requirements can be met with available resources
- **Dependencies identified** - No hidden prerequisites
- **Right abstraction** - Spec focuses on what/why, not how
- **Testable requirements** - Each requirement can be verified
- **Measurable NFRs** - Non-functional requirements have thresholds
- **Clear scope** - Boundaries are well-defined
- **No conflicts** - Doesn't break existing functionality
- **Completeness** - No obvious gaps in requirements

**Red flags to catch:**
- Requirements that assume non-existent functionality
- Implementation details masquerading as requirements
- Vague requirements that can't be tested
- Scope that's too large for single iteration
- Missing edge cases at the requirements level
- Conflicts with existing features
- Unrealistic performance expectations
- Dependencies on unavailable external services

**What NOT to flag:**
- Absence of API designs (those belong in design phase)
- Absence of technical approach (that's for design)
- Lack of code examples (specs shouldn't have these)
- Missing architecture decisions (design phase concern)

##### Design Review

###### Project Guidelines Compliance

**If `.sdd/project-guidelines.md` exists:**

1. Read the project guidelines file
2. Read all referenced documentation files
3. For each convention category, verify the design complies:

**Error Handling:**
- Does the design's error handling approach match project conventions?
- Are error types/classes consistent with project standards?
- Is error propagation handled according to guidelines?

**Logging:**
- Does the design specify logging consistent with project patterns?
- Are log levels used appropriately per guidelines?
- Is structured logging followed if required?

**Naming:**
- Do component names follow project naming conventions?
- Do file locations follow project structure patterns?
- Are API names consistent with project style?

**Testing:**
- Does the test strategy align with project testing conventions?
- Are test file locations following project patterns?
- Is the testing framework/approach consistent?

**When violations found:** Flag as a Concern with specific reference to which guideline is violated and recommendation for how to align.

###### Requirements Traceability

**For each requirement in the specification:**
1. Find it in the design's Requirements Validation section
2. Verify it maps to specific components (Modified or Added)
3. Verify it maps to specific tasks
4. Check that the component/task actually addresses the requirement
5. Flag any broken or missing traces

**Common gaps:**
- Requirement listed but component doesn't actually address it
- Requirement mapped to task that's too vague
- Non-functional requirements with no concrete implementation approach
- Edge cases from spec examples not reflected in design

###### Edge Case Analysis

**For each functional requirement:**
- What happens with empty/null input?
- What happens at boundary values?
- What happens with invalid input?
- What happens with concurrent access?
- What happens when dependencies fail?
- What happens with maximum load?

**For each non-functional requirement:**
- How is the threshold actually achieved?
- What happens when threshold is exceeded?
- Is degradation handled gracefully?

###### Architectural Validation

**Verify against codebase:**
- Do proposed file locations follow project conventions?
- Do proposed patterns match existing code?
- Are referenced existing components accurate?
- Would modifications to existing components break anything?

**Check consistency:**
- Do component names follow conventions?
- Is error handling consistent with project patterns?
- Is logging consistent with project patterns?

###### Implementation Leakage Detection

**Designs should describe WHAT and WHY, not HOW at code level.**

**Check API Design section:**
- Are operations described conceptually or with code samples?
- Could a developer choose different implementation approaches?
- Is the design language-agnostic where possible?

**Acceptable code/specifics:**
- Serialization format examples (JSON structure, protobuf schemas)
- Concurrency patterns when mandated by non-functional requirements
- Wire protocols or format specifications
- Algorithm pseudocode when the algorithm IS the requirement

**Red flags:**
- Function signatures with full type annotations
- Class implementations or method bodies
- Language-specific idioms that aren't required by NFRs
- "Implementation" sections describing code logic

**When found:** Flag as a Concern with recommendation to describe the contract conceptually instead, preserving developer flexibility during implementation.

###### Task-Level Test Verification

**CRITICAL: Tests must be written WITH implementation, not after.**

**For each task in the Task Breakdown:**
1. Check that the task has a "Tests:" field
2. Verify the Tests field references specific test cases from component definitions
3. Ensure the task is NOT just "implement X" without tests

**Red flags for deferred testing:**
- Tasks like "Add unit tests for X" as separate tasks
- A phase dedicated to "Testing" or "Add tests"
- Tasks without any "Tests:" field
- Component test cases not assigned to any task

**Verify complete test assignment:**
1. List all test cases defined in Modified Components and Added Components
2. For each test case, find which task will write it
3. Flag any test case not assigned to a task
4. Flag any task that modifies/adds code without associated tests

**Example of GOOD task structure:**
```
- Task 1: Implement CartService.addItem()
  - Status: Backlog
  - Add item to cart with quantity validation
  - Tests: TEST-CART-ADD-VALID, TEST-CART-ADD-INVALID-QTY, TEST-CART-ADD-DUPLICATE
```

**Example of BAD task structure (deferred testing):**
```
Phase 1:
- Task 1: Implement CartService
- Task 2: Implement CartRepository

Phase 2:
- Task 1: Add unit tests for CartService  ← VIOLATION
- Task 2: Add integration tests           ← VIOLATION
```

###### Review Quality Standards

A thorough design review must verify:
- **Requirements coverage** - Every spec requirement has design coverage
- **Edge case coverage** - Common edge cases are addressed
- **Architectural fit** - Design fits existing codebase patterns
- **Project guidelines compliance** - Design follows documented conventions (if SDD_PROJECT_GUIDELINES exists)
- **Component completeness** - All components fully specified
- **Test adequacy** - Test strategy covers requirements and edge cases
- **Tests with tasks** - Each task includes its tests, no deferred testing phases
- **Task completeness** - Tasks would actually deliver the feature
- **Risk identification** - Technical risks called out with mitigations

**Red flags to catch:**
- Requirements in spec not traced in design
- Edge cases from spec examples missing from design
- Components without clear test cases
- Vague tasks like "implement feature" without specifics
- Modified components without dependant analysis
- New components without clear locations
- Test strategy missing integration or edge case tests
- Assumptions that contradict the codebase
- Architectural decisions that conflict with existing patterns
- **Separate "add tests" tasks** - Tests must be written WITH implementation
- **Testing phases** - Phases dedicated to testing violate TDD principles
- **Tasks missing "Tests:" field** - Every task that adds/modifies code needs tests
- **Unassigned test cases** - Component test cases not mapped to any task
- **Code samples in API design** - APIs should describe contracts conceptually, not show implementation code
- **Implementation leakage** - Designs prescribing specific implementation details that should be left to the developer
- **Project guidelines violations** - Design decisions that conflict with documented project conventions (error handling, logging, naming, testing)

##### Implementation Review

###### Diff Analysis

**Start with the big picture:**
- Run `git diff main...HEAD` (or appropriate base branch)
- Understand all changes being introduced
- Identify files added, modified, and deleted
- What is the overall scope of changes?
- Which components are affected?
- Are the changes focused or scattered?

**Then examine details:**
- Read through each changed file
- Understand the purpose of each change
- Look for patterns and anti-patterns

**Check for completeness:**
- Are all design tasks represented in the diff?
- Are there changes that don't correspond to any task?
- Is anything missing that should be there?

###### Design Validation
**Validate implementation matches design**
- Compare the diff against design document tasks
- Ensure each design task has corresponding implementation
- Verify the architecture matches what was designed
- Check that APIs and interfaces match the design contracts
**Check for design alterations and workarounds**
- If the design was altered during implementation, verify:
  - Changes are documented in the design document
  - Workarounds are documented explaining how requirements will still be met
  - Requirements are NOT simply removed without justification
   - Flag any undocumented deviations from the design

**Trace requirements to code:**
- Each functional requirement should have implementation
- Each non-functional requirement should have appropriate handling
- Use the Requirements Validation section of the design as your checklist

**Verify architectural decisions:**
- Are the right patterns being used?
- Are components in the right locations?
- Do interfaces match the design?

**Check for scope creep:**
- Are there changes beyond what was designed?
- Is extra functionality being added without approval?
- Are design decisions being overridden silently?


**Check for stubs**
- Search for stub patterns: `skip`, `todo`, `pending`, `@pytest.mark.skip`, `@unittest.skip`, `it.skip`, `xit`
- Search for empty test bodies or `pass` statements in test functions
- Search for placeholder assertions: `assert True`, `expect(true).toBe(true)`, `assertTrue(true)`
- Search for TODO/FIXME comments in test files
- **Intermediate phases**: Test stubs are acceptable ONLY if tracked in the design document's "Test Stub Tracking" section with a clear plan for implementation
- **Final phase**: When reviewing the final phase of a design, there must be NO test stubs - all tests must be fully implemented. Verify any previously tracked test stubs have been resolved

**Check for dead code**
- Identify unused imports, variables, or functions introduced by this design
- Flag commented-out code that should be removed
- Check for code that will never be executed
- **Intermediate phases**: Dead code related to this design's work is acceptable if it will be used in a subsequent phase of the same design. Such code must be tracked in the design document (e.g., "Task X.Y introduces helper functions used in Phase Z")
- **Final phase**: When reviewing the final phase of a design, there must be NO dead code related to this design's work - all code introduced by the design should be used. Verify any previously tracked dead code markers have been resolved
   
**Verify code meets documented practices**
- Check error handling matches documented patterns
- Verify logging follows project standards
- Ensure naming conventions are followed
- Check module structure matches project organization
- Verify code style is consistent

**Run all tests**
- Execute unit tests
- Execute integration tests
- Execute any other test types (e2e, performance, etc.)
- Document any test failures

**Run linters and quality checks**
- Run project linters (ruff, eslint, clippy, etc.)
- Run formatters in check mode
- Run static analysis tools if configured
- Document any linting issues

**Check for compilation warnings**
- Build/compile the project
- Document any new warnings introduced
- Warnings in new code should be addressed

###### Test Verification

**Check test existence:**
- Every new function/method should have tests
- Every new module should have a test file
- Edge cases identified in design should be tested

**Check test quality:**
- Do tests actually validate the requirements?
- Are tests using appropriate assertions?
- Are tests following the existing test patterns?

**Check test execution:**
- Do all tests pass?
- Are there flaky tests?
- Is test coverage acceptable?

###### Quality Gate Enforcement

**Linting and formatting:**
- No linting errors in new code
- Code is properly formatted
- No style violations

**Compilation and build:**
- Project compiles without errors
- No new warnings introduced
- Build artifacts are correct

**Documentation:**
- Code is appropriately commented
- Public APIs are documented
- README updated if needed

###### Review Quality Standards

A thorough review must verify:
- ✅ **Design alignment** - Implementation matches the design document
- ✅ **Requirement coverage** - All requirements are implemented
- ✅ **Test coverage** - All new code has tests
- ✅ **Tests fully implemented** - No test stubs (skip, pass, todo, placeholder assertions) in final phase; intermediate phase stubs tracked in design document
- ✅ **Test execution** - All tests pass
- ✅ **Linting** - No linting errors or warnings
- ✅ **Compilation** - No build errors or new warnings
- ✅ **Code standards** - Follows documented practices
- ✅ **No dead code** - No unused or commented-out code in final phase; intermediate phase dead code tracked in design document
- ✅ **Documentation** - Changes are properly documented
- ✅ **Workarounds documented** - If design was altered, workarounds exist

**Red flags to catch:**
- ❌ Implementation that doesn't match the design
- ❌ Requirements removed without justification
- ❌ New code without corresponding tests
- ❌ Test stubs (skip, pass, todo, placeholder assertions) - in final phase, or untracked in intermediate phases
- ❌ Tests deferred to "later phase" without tracking in design document
- ❌ Failing tests
- ❌ Linting errors or warnings ignored
- ❌ Undocumented deviations from design
- ❌ Dead code or commented-out blocks (in final phase, or untracked in intermediate phases)
- ❌ Violations of documented coding standards
- ❌ Missing error handling or logging
- ❌ Security vulnerabilities
