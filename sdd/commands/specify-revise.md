---
name: specify-revise
description: Address feedback on an existing specification. Routes feedback directly to the technical-analyst agent to revise the specification document. Use this when you have feedback from a review or stakeholder that needs to be incorporated.
arguments:
  - FEATURE (The name of the feature)
  - FEEDBACK (The feedback or issues to address - can be provided inline or referenced from a review)
allowed-tools: ["Read", "Write", "Bash", "WebSearch", "WebFetch", "Glob", "Grep", "Task", "AskUserQuestion"]
---

You must use the sdd skill. Use the exact paths defined in the skill's "Project Structure and Paths" section.

# Specify Revise

Address feedback on an existing specification by routing it to the technical-analyst agent who created the original document.

## STEP 1 - Verify specification exists

- Look for the specification document in [SDD_FOLDER]/[FEATURE]/specification.md (this is [SDD_SPECIFICATION_DOCUMENT])
- If the specification doesn't exist, inform the user they need to run `/specify` first
- Read the current specification to understand its state

## STEP 2 - Gather feedback

- If FEEDBACK argument is provided, use that feedback
- If no FEEDBACK is provided, ask the user what feedback or issues need to be addressed
- Ensure the feedback is clear and actionable

## STEP 3 - Route to technical-analyst to address feedback

**CRITICAL**: You MUST use the Task tool with `subagent_type="sdd:technical-analyst"` to address the feedback. DO NOT revise the specification yourself - launch the technical-analyst agent to do the work.

- Use the Task tool with subagent_type="sdd:technical-analyst" and the following prompt:
  - |
    You are revising an existing specification based on feedback.

    Read [SDD_SPECIFICATION_DOCUMENT] to understand the current specification.

    Feedback to address:
    [FEEDBACK]

    For each piece of feedback:
    1. Understand what needs to change
    2. If clarification is needed, use AskUserQuestion to clarify with the user
    3. Update the relevant sections of the specification
    4. Ensure changes maintain consistency with other sections

    After addressing all feedback:
    - Update the version number in the document header
    - Update the date to today's date
    - Ensure the document still follows the [SDD_TEMPLATE_SPECIFICATION] format
    - Use the Write tool to save the updated specification to [SDD_SPECIFICATION_DOCUMENT]

    Report what changes were made to address the feedback.

## STEP 4 - Verify changes were saved

- Read [SDD_SPECIFICATION_DOCUMENT] to verify the changes were applied
- If changes were not saved, resume the agent and ask it to use the Write tool
- Confirm to the user what changes were made

## STEP 5 - Re-review the specification

**CRITICAL**: You MUST use the Task tool with `subagent_type="sdd:spec-reviewer"` to review the revised specification. DO NOT review the specification yourself - launch the spec-reviewer agent to do the work.

- Use the Task tool with subagent_type="sdd:spec-reviewer" and the following prompt. Pass the specification document's path as `SDD_SPECIFICATION_DOCUMENT`.
  - |
    Review [SDD_SPECIFICATION_DOCUMENT] for:
    1. Achievability - Can requirements be met with current technology and codebase?
    2. Missing dependencies - Does the spec assume functionality that doesn't exist?
    3. Right abstraction level - Does the spec focus on WHAT/WHY, not HOW?
    4. Consistency - Does this conflict with existing functionality?
    5. Requirements quality - Are requirements testable and measurable?

    Explore the codebase using Glob, Grep, and Read to understand current capabilities.

    Produce a review report with status (APPROVED, NEEDS REVISION, BLOCKED) and specific, actionable feedback.

## STEP 6 - Handle review feedback

- If the spec-reviewer returns APPROVED:
  - Update the specification status to "Approved" in the document header
  - Inform the user the specification is ready for the design phase (`/design`)
- If the spec-reviewer returns NEEDS REVISION or BLOCKED:
  - Present the review findings to the user
  - Use AskUserQuestion to ask if they want to:
    1. Address the feedback now (resume technical-analyst agent to revise)
    2. Proceed anyway (acknowledge risks)
    3. Discuss the feedback further
  - If addressing feedback, resume the technical-analyst agent from STEP 3 with the review findings and re-run review after revisions
  - Loop STEP 5-6 until APPROVED or user chooses to proceed

## STEP 7 - Offer next steps

- If approved, ask the user if they want to:
  1. Continue to design phase (`/design [FEATURE]`)
  2. Provide additional feedback (`/specify-revise [FEATURE]`)
- If not approved and user chose to proceed anyway, remind them of the unresolved issues

## Usage Examples

```
# Address specific feedback
/specify-revise shopping-cart "The error handling requirements are missing edge cases for network timeouts"

# Address feedback from a review
/specify-revise shopping-cart "Address the NEEDS REVISION items from the spec review"

# Interactively provide feedback
/specify-revise shopping-cart
```
