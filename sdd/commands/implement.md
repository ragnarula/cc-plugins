---
name: implement
description: Implement a feature from its design document. Executes Phase 3 of SDD methodology - disciplined, task-by-task coding with continuous testing, proper version control, and progress tracking in the design document. Includes automated code review after each phase.
arguments:
  - FEATURE (The name of the feature)
  - PHASE (Optional - The phase number to implement, defaults to next incomplete phase)
  - --review-and-fix (Optional flag - Skip implementation and run the review→fix→re-review cycle. Use when implementation is already done and you want to review and fix any issues.)
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "LSP", "Task"]
---

You must use the sdd skill. Use the exact paths defined in the skill's "Project Structure and Paths" section.

# Implement

Implement a feature according to the tasks defined in its design document. Work through tasks incrementally with continuous validation, proper commits, and progress tracking. After implementation, automatically review the code and fix any issues before completion.

## STEP 1 - Verify design exists and is approved

- Look for the design document in [SDD_FOLDER]/[FEATURE]/design.md
- If the design doesn't exist, inform the user they need to run `/design` first
- Check the design document status - it should be "Approved" or "Ready for Implementation"
- If status is still "Draft", ask the user to confirm the design is ready for implementation
- Read the design document to understand the phases and tasks

## STEP 2 - Determine which phase to implement

- If PHASE argument is provided, use that phase number
- Otherwise, scan the design document's Tasks section to find the first incomplete phase
- A phase is incomplete if any of its tasks are not marked as complete
- If all phases are complete, inform the user that implementation is finished
- The current phase will be stored as `SDD_CURRENT_PHASE`

## STEP 3 - Verify prerequisites for the phase

- Check if there are any prerequisite phases that must be completed first
- Verify that previous phases are complete (tasks marked done, branches merged)
- Check the Feasibility Review section for any blockers that need resolution
- If there are unresolved blockers, present them to the user and ask how to proceed

## STEP 4 - Check for review-and-fix mode

- If the `--review-and-fix` flag is present:
  - Skip STEP 5 (implementation)
  - Go directly to STEP 6 (review)
  - **IMPORTANT**: After review, automatically continue through STEP 7 to fix any issues found. Do NOT stop after the review - execute the full review→fix→re-review cycle until the code is APPROVED or the max retry limit is reached.
  - This is useful when:
    - Implementation was done manually or in a previous session
    - The user wants to re-run the review after fixing issues
    - Resuming after a partial implementation
- If `--review-and-fix` is NOT present, continue to STEP 5

## STEP 5 - Implement the phase

**CRITICAL**: You MUST use the Task tool with `subagent_type="sdd:developer"` to implement this phase. DO NOT implement the code yourself - launch the developer agent to do the work.

- Use the Task tool with subagent_type="sdd:developer" and the following prompt. Pass the design document's path as `SDD_DESIGN_DOCUMENT`, the specification document's path as `SDD_SPECIFICATION_DOCUMENT`, and the phase number as `SDD_CURRENT_PHASE`.
  - |
    Implement Phase [SDD_CURRENT_PHASE] of the feature according to the design document.

    First, read [SDD_DESIGN_DOCUMENT] and [SDD_SPECIFICATION_DOCUMENT] to understand what you're building.

    Then, read the codebase documentation (README.md, CLAUDE.md, CONSTITUTION.md, docs/) to understand conventions.

    Then, explore the codebase to understand existing patterns for error handling, logging, module structure, and tests.

    If documentation for critical patterns doesn't exist, STOP and ask the user to document them before proceeding.

    Create a feature branch for this phase (e.g., `feature/[FEATURE]-phase-[SDD_CURRENT_PHASE]`).

    Work through the tasks for Phase [SDD_CURRENT_PHASE] in order:
    1. Write tests first (TDD when appropriate)
    2. Implement the code to pass tests
    3. Run linters and formatters
    4. Run the full test suite
    5. Commit the completed task with a clear message
    6. Update the task status in [SDD_DESIGN_DOCUMENT] to mark it complete

    Do NOT skip tasks or work out of order.
    Do NOT batch multiple tasks into one commit.

    After completing all tasks in the phase:
    - Ensure all tests pass
    - Ensure code is properly formatted and linted
    - Verify all tasks are marked complete in [SDD_DESIGN_DOCUMENT]
    - Report that the phase implementation is complete and ready for review

## STEP 6 - Review the implementation

**CRITICAL**: You MUST use the Task tool with `subagent_type="sdd:reviewer"` to review the implementation. DO NOT review the code yourself - launch the reviewer agent to do the work.

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

## STEP 7 - Fix review issues (if any)

- If the review status is **APPROVED**, skip to STEP 8
- If the review status is **NEEDS REVISION** or **BLOCKED**:
  1. Present the review findings to the context
  2. **CRITICAL**: Use the Task tool with `subagent_type="sdd:developer"` to fix the issues. DO NOT fix the issues yourself - launch the developer agent:
     - |
       Fix the issues identified in the code review for Phase [SDD_CURRENT_PHASE].

       Review findings to address:
       [INSERT REVIEW FINDINGS HERE - blockers and major issues]

       Read [SDD_DESIGN_DOCUMENT] and [SDD_SPECIFICATION_DOCUMENT] for context.

       For each issue:
       1. Read the referenced file and understand the problem
       2. Implement the fix following project conventions
       3. Run tests to ensure the fix works and doesn't break anything
       4. Run linters and formatters
       5. Commit the fix with a clear message referencing what was fixed

       After fixing all issues:
       - Ensure all tests pass
       - Ensure code is properly formatted and linted
       - Report what was fixed and that the code is ready for re-review

  3. After the developer agent completes, go back to STEP 6 to re-review
  4. Repeat this cycle until the review status is **APPROVED**
  5. If the cycle repeats more than 3 times, ask the user for guidance on how to proceed

## STEP 8 - Verify phase completion

- Read [SDD_DESIGN_DOCUMENT] to verify all tasks in Phase [SDD_CURRENT_PHASE] are marked complete
- If tasks are not marked complete:
  1. Resume the developer agent to update the design document with task completion status
  2. Re-check after the agent completes
- Verify that the feature branch exists and has commits for each task
- Confirm the review status is APPROVED
- Inform the user that the phase is complete, reviewed, and the branch is ready for merge
- Remind the user to merge the branch before starting the next phase

## STEP 9 - Next steps

- If there are more phases remaining, inform the user they can run `/implement [FEATURE]` again after merging to continue with the next phase
- If all phases are complete, congratulate the user and suggest:
  - Final integration testing
  - Updating the design document status to "Implemented"
  - Closing any related issues or tickets

## Usage Examples

```
# Implement the next incomplete phase with automatic review
/implement shopping-cart

# Implement a specific phase with automatic review
/implement shopping-cart 2

# Run review and fix cycle (when implementation is already done)
/implement shopping-cart --review-and-fix

# Review and fix a specific phase that was implemented manually
/implement shopping-cart 1 --review-and-fix
```
