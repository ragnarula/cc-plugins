---
name: implement-revise
description: Address feedback on an implementation. Routes feedback directly to the developer agent to fix issues or make changes. Use this when you have feedback from a code review or testing that needs to be addressed.
arguments:
  - FEATURE (The name of the feature)
  - PHASE (Optional - The phase number the feedback applies to, defaults to latest)
  - FEEDBACK (The feedback or issues to address - can be provided inline or referenced from a review)
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "LSP", "Task", "AskUserQuestion"]
---

You must use the sdd skill. Use the exact paths defined in the skill's "Project Structure and Paths" section.

# Implement Revise

Address feedback on an implementation by routing it to the developer agent who implemented the code.

## STEP 1 - Verify design exists

- Look for the design document in [SDD_FOLDER]/[FEATURE]/design.md (this is [SDD_DESIGN_DOCUMENT])
- If the design doesn't exist, inform the user they need to run `/design` first
- Read the current design to understand the implementation context
- Also locate the specification at [SDD_FOLDER]/[FEATURE]/specification.md (this is [SDD_SPECIFICATION_DOCUMENT])

## STEP 2 - Determine which phase

- If PHASE argument is provided, use that phase number
- Otherwise, determine the most recent phase that was implemented (check task completion in design document)
- Store as `SDD_CURRENT_PHASE`

## STEP 3 - Gather feedback

- If FEEDBACK argument is provided, use that feedback
- If no FEEDBACK is provided, ask the user what feedback or issues need to be addressed
- Ensure the feedback is clear and actionable
- Feedback can include:
  - Code review comments
  - Bug reports
  - Test failures
  - Style/convention issues
  - Performance concerns
  - Missing functionality

## STEP 4 - Route to developer to address feedback

**CRITICAL**: You MUST use the Task tool with `subagent_type="sdd:developer"` to address the feedback. DO NOT fix the issues yourself - launch the developer agent to do the work.

- Use the Task tool with subagent_type="sdd:developer" and the following prompt:
  - |
    You are addressing feedback on an existing implementation for Phase [SDD_CURRENT_PHASE].

    Read [SDD_DESIGN_DOCUMENT] to understand the design and tasks.
    Read [SDD_SPECIFICATION_DOCUMENT] to understand the requirements.
    Read the codebase documentation (README.md, CLAUDE.md, docs/) to understand conventions.

    Feedback to address:
    [FEEDBACK]

    For each piece of feedback:
    1. Read the referenced files to understand the current implementation
    2. If clarification is needed, use AskUserQuestion to clarify with the user
    3. Implement the fix or change following project conventions
    4. Write or update tests to cover the changes
    5. Run linters and formatters
    6. Run the test suite to ensure nothing is broken
    7. Commit the changes with a clear message describing what was fixed

    After addressing all feedback:
    - Ensure all tests pass
    - Ensure code is properly formatted and linted
    - If the changes required design alterations, update [SDD_DESIGN_DOCUMENT] with:
      - What changed from the original design
      - Why the change was necessary
      - How requirements are still met

    Report what changes were made to address the feedback.

## STEP 5 - Verify changes

- Ask the developer agent to confirm what was changed
- If there were test failures during the fix, resume the agent to address them
- Confirm to the user what changes were made

## STEP 6 - Re-review the implementation

**CRITICAL**: You MUST use the Task tool with `subagent_type="sdd:reviewer"` to review the revised implementation. DO NOT review the code yourself - launch the reviewer agent to do the work.

- Use the Task tool with subagent_type="sdd:reviewer" and the following prompt. Pass the design document's path as `SDD_DESIGN_DOCUMENT`, the specification document's path as `SDD_SPECIFICATION_DOCUMENT`, and the phase number as `SDD_CURRENT_PHASE`.
  - |
    Review the implementation of Phase [SDD_CURRENT_PHASE] for the feature.

    First, read [SDD_DESIGN_DOCUMENT] and [SDD_SPECIFICATION_DOCUMENT] to understand what was supposed to be built.

    Then, read the codebase documentation (README.md, CLAUDE.md, CONSTITUTION.md, docs/) to understand the project standards.

    Analyze the diff against the base branch to see all changes introduced.

    Perform a comprehensive review:
    1. Validate implementation matches the design document tasks
    2. Check for design alterations - if found, ensure workarounds are documented
    3. Verify tests are added for all new code
    4. Check for dead code or commented-out blocks (must be none in final phase; intermediate phase dead code must be tracked in design document)
    5. Verify code meets documented practices (error handling, logging, naming)
    6. Run all tests (unit, integration, etc.) and document any failures
    7. Run linters and quality checks, document any issues
    8. Check for compilation warnings

    Produce a review report with:
    - Status: APPROVED, NEEDS REVISION, or BLOCKED
    - Blockers: Issues that must be fixed (with file:line references)
    - Major Issues: Significant problems to address
    - Minor Issues: Small improvements or suggestions
    - Passed Checks: What was validated successfully
    - What Was Done Well: Positive feedback

    Be thorough, objective, and constructive. Reference specific files and line numbers for all issues.

- Store the review result status (APPROVED, NEEDS REVISION, or BLOCKED)

## STEP 7 - Handle review feedback

- If the review status is **APPROVED**:
  - Confirm to the user that the fixes have been reviewed and approved
  - Proceed to STEP 8
- If the review status is **NEEDS REVISION** or **BLOCKED**:
  - Present the review findings to the user
  - Use AskUserQuestion to ask if they want to:
    1. Address the new issues now (resume developer agent to fix)
    2. Proceed anyway (acknowledge risks)
    3. Discuss the feedback further
  - If addressing feedback, resume the developer agent from STEP 4 with the new review findings and re-run review
  - Loop STEP 6-7 until APPROVED or user chooses to proceed
  - If the cycle repeats more than 3 times, ask the user for guidance on how to proceed

## STEP 8 - Offer next steps

- If approved, ask the user if they want to:
  1. Provide additional feedback (`/implement-revise [FEATURE]`)
  2. Merge the changes and continue to next phase (`/implement [FEATURE]`)
- If not approved and user chose to proceed anyway, remind them of the unresolved issues

## Usage Examples

```
# Address specific feedback on latest phase
/implement-revise shopping-cart "The addItem function doesn't validate quantity is positive"

# Address feedback on a specific phase
/implement-revise shopping-cart 2 "Error handling in the checkout flow needs to follow our retry pattern"

# Address feedback from a code review
/implement-revise shopping-cart "Fix the NEEDS REVISION items from the code review"

# Address test failures
/implement-revise shopping-cart "The integration tests are failing due to database connection issues"

# Interactively provide feedback
/implement-revise shopping-cart
```
