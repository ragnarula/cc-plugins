---
name: design-revise
description: Address feedback on an existing design document. Routes feedback directly to the technical-architect agent to revise the design. Use this when you have feedback from a review or stakeholder that needs to be incorporated.
arguments:
  - FEATURE (The name of the feature)
  - FEEDBACK (The feedback or issues to address - can be provided inline or referenced from a review)
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "LSP", "Task", "AskUserQuestion"]
---

You must use the sdd skill. Use the exact paths defined in the skill's "Project Structure and Paths" section.

# Design Revise

Address feedback on an existing design document by routing it to the technical-architect agent who created the original document.

## STEP 1 - Verify design exists

- Look for the design document in [SDD_FOLDER]/[FEATURE]/design.md (this is [SDD_DESIGN_DOCUMENT])
- If the design doesn't exist, inform the user they need to run `/design` first
- Read the current design to understand its state
- Also locate the specification at [SDD_FOLDER]/[FEATURE]/specification.md (this is [SDD_SPECIFICATION_DOCUMENT])

## STEP 2 - Check for project guidelines

- Check if [SDD_FOLDER]/project-guidelines.md exists (SDD_PROJECT_GUIDELINES)
- If it exists, note the path for passing to the agent
- Guidelines help ensure revisions maintain consistency with project conventions

## STEP 3 - Gather feedback

- If FEEDBACK argument is provided, use that feedback
- If no FEEDBACK is provided, ask the user what feedback or issues need to be addressed
- Ensure the feedback is clear and actionable

## STEP 4 - Route to technical-architect to address feedback

**CRITICAL**: You MUST use the Task tool with `subagent_type="sdd:technical-architect"` to address the feedback. DO NOT revise the design yourself - launch the technical-architect agent to do the work.

- Use the Task tool with subagent_type="sdd:technical-architect" and the following prompt:
  - |
    You are revising an existing design document based on feedback.

    Read [SDD_DESIGN_DOCUMENT] to understand the current design.
    Read [SDD_SPECIFICATION_DOCUMENT] to ensure changes remain aligned with requirements.
    If [SDD_PROJECT_GUIDELINES] exists, read it to ensure changes follow project conventions.

    Feedback to address:
    [FEEDBACK]

    For each piece of feedback:
    1. Understand what needs to change
    2. If the feedback affects architectural decisions, explore the codebase to validate feasibility
    3. If clarification is needed, use AskUserQuestion to clarify with the user
    4. Update the relevant sections of the design document
    5. Ensure changes maintain traceability to specification requirements
    6. Update the Requirements Validation section if affected

    After addressing all feedback:
    - Update the version number in the document header
    - Update the date to today's date
    - Ensure the document still follows the [SDD_TEMPLATE_DESIGN] format
    - Verify all specification requirements are still covered
    - CRITICAL: Use the Write tool to save the updated design to [SDD_DESIGN_DOCUMENT]

    Report what changes were made to address the feedback.

## STEP 5 - Verify changes were saved

- Read [SDD_DESIGN_DOCUMENT] to verify the changes were applied
- If changes were not saved, resume the agent and ask it to use the Write tool
- Confirm to the user what changes were made

## STEP 6 - Re-review the design

**CRITICAL**: You MUST use the Task tool with `subagent_type="sdd:design-reviewer"` to review the revised design. DO NOT review the design yourself - launch the design-reviewer agent to do the work.

- Use the Task tool with subagent_type="sdd:design-reviewer" and the following prompt. Pass `SDD_DESIGN_DOCUMENT`, `SDD_SPECIFICATION_DOCUMENT`, and if project guidelines exist, `SDD_PROJECT_GUIDELINES`.
  - |
    Review [SDD_DESIGN_DOCUMENT] against [SDD_SPECIFICATION_DOCUMENT] for:
    1. Requirements coverage - Does every requirement have clear design coverage?
    2. Edge case coverage - Are edge cases from specification examples addressed?
    3. Corner cases - Are boundary conditions, error scenarios, and concurrent access handled?
    4. Architectural feasibility - Does the design fit existing codebase patterns?
    5. Component completeness - Are all components fully specified with locations and tests?
    6. Test strategy adequacy - Does test strategy cover requirements and edge cases?
    7. Task completeness - Would completing all tasks actually deliver the feature?
    8. Project guidelines compliance - If [SDD_PROJECT_GUIDELINES] exists, does the design follow documented conventions for error handling, logging, naming, and testing?

    Explore the codebase using Glob, Grep, Read, and LSP to validate architectural decisions.

    Produce a review report with status (APPROVED, NEEDS REVISION, BLOCKED) and specific, actionable feedback referencing requirements and design sections.

## STEP 7 - Handle review feedback

- If the design-reviewer returns APPROVED:
  - Update the design status to "Approved" in the document header
  - Inform the user the design is ready for implementation (`/implement`)
- If the design-reviewer returns NEEDS REVISION or BLOCKED:
  - Present the review findings to the user
  - Use AskUserQuestion to ask if they want to:
    1. Address the feedback now (resume technical-architect agent to revise)
    2. Proceed anyway (acknowledge risks and gaps)
    3. Discuss the feedback further
  - If addressing feedback, resume the technical-architect agent from STEP 4 with the review findings and re-run review after revisions
  - Loop STEP 6-7 until APPROVED or user chooses to proceed

## STEP 8 - Offer next steps

- If approved, ask the user if they want to:
  1. Continue to implementation phase (`/implement [FEATURE]`)
  2. Provide additional feedback (`/design-revise [FEATURE]`)
- If not approved and user chose to proceed anyway, remind them of the unresolved issues

## Usage Examples

```
# Address specific feedback
/design-revise shopping-cart "The error handling strategy doesn't align with our existing patterns"

# Address feedback from a review
/design-revise shopping-cart "Address the NEEDS REVISION items from the design review"

# Address feedback about task breakdown
/design-revise shopping-cart "Phase 2 tasks are too large, break them down further"

# Interactively provide feedback
/design-revise shopping-cart
```
