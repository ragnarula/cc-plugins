---
name: implement
description: Implement a feature from its design document. Executes Phase 3 of SDD methodology - disciplined, task-by-task coding with continuous testing, proper version control, and progress tracking in the design document.
arguments:
  - FEATURE (The name of the feature)
  - PHASE (Optional - The phase number to implement, defaults to next incomplete phase)
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "LSP", "Task"]
---

You must use the sdd skill.

# Implement

Implement a feature according to the tasks defined in its design document. Work through tasks incrementally with continuous validation, proper commits, and progress tracking.

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

## STEP 4 - Implement the phase

- Create a Task with the developer agent and do the following. Pass the design document's path as `SDD_DESIGN_DOCUMENT`, the specification document's path as `SDD_SPECIFICATION_DOCUMENT`, and the phase number as `SDD_CURRENT_PHASE`.
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
    - Report that the branch is ready for review and merge

## STEP 5 - Verify phase completion

- Read [SDD_DESIGN_DOCUMENT] to verify all tasks in Phase [SDD_CURRENT_PHASE] are marked complete
- If tasks are not marked complete:
  1. Resume the agent from STEP 4 using its agent ID
  2. Ask it to update the design document with task completion status
  3. Re-check after the agent completes
- Verify that the feature branch exists and has commits for each task
- Run the test suite to confirm all tests pass
- Inform the user that the phase is complete and the branch is ready for merge
- Remind the user to merge the branch before starting the next phase

## STEP 6 - Next steps

- If there are more phases remaining, inform the user they can run `/implement [FEATURE]` again after merging to continue with the next phase
- If all phases are complete, congratulate the user and suggest:
  - Final review of all changes
  - Integration testing
  - Updating the design document status to "Implemented"
  - Closing any related issues or tickets
