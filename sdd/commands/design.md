---
name: design
description: Design an implementation plan from a specification. Documents the 'How' - architectural decisions, component design, API contracts, test strategy, and task breakdown. Follows SDD Phase 2 methodology to transform specifications into actionable implementation plans.
arguments:
  - FEATURE (The name of the feature)
  - DESCRIPTION (A brief description)
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "LSP", "Task", "AskUserQuestion"]
---

You must use the sdd skill.

# Design

Create a design document for a feature according to the `design.template.md` template. The design should be based on an existing specification and should explore the codebase to understand current architecture before making design decisions.

## STEP 1 - Verify specification exists
- Look for the specification document in [SDD_FOLDER]/[FEATURE]/specification.md
- If the specification doesn't exist, inform the user they need to run `/specify` first
- The specification is required as input for the design process

## STEP 2 - Check for project guidelines
- Check if [SDD_FOLDER]/project-guidelines.md exists (SDD_PROJECT_GUIDELINES)
- If it does NOT exist:
  - Use AskUserQuestion to ask the user:
    - "No project guidelines found. Project guidelines help ensure designs follow your project's conventions (error handling, logging, naming, testing). Would you like to:"
    - Option 1: "Create project guidelines now" - Create [SDD_FOLDER]/project-guidelines.md from [SDD_TEMPLATE_PROJECT_GUIDELINES] and ask user to fill it in before continuing
    - Option 2: "Skip for now" - Continue without project guidelines (designs may not follow project conventions)
  - If user chooses to create guidelines:
    - Copy [SDD_TEMPLATE_PROJECT_GUIDELINES] to [SDD_FOLDER]/project-guidelines.md
    - Inform user to edit the file with their project's conventions
    - Ask user to confirm when ready to continue
- If project guidelines exist, note the path for passing to agents as SDD_PROJECT_GUIDELINES

## STEP 3 - Create an empty design document
- The [SDD_PROJECT_FOLDER] directory should already exist from the specification phase at [SDD_FOLDER]/[FEATURE]
- Create a blank [SDD_TEMPLATE_DESIGN] document in the [SDD_PROJECT_FOLDER] directory if it doesn't already exist
- The file should be named `design.md`
- Fill the metadata in the header of the document including current date, feature name, status (Draft), version, and link to specification

## STEP 4 - Fill in the document
- Create a Task with the technical-architect agent and do the following. Pass the new design document's path as `SDD_DESIGN_DOCUMENT`, the specification document's path as `SDD_SPECIFICATION_DOCUMENT`, and if project guidelines exist, pass the path as `SDD_PROJECT_GUIDELINES`.
  - |
    The [SDD_DESIGN_DOCUMENT] file needs to be completed to the highest standard. The header has already been filled out.

    First, read the [SDD_SPECIFICATION_DOCUMENT] to understand all functional and non-functional requirements.

    If [SDD_PROJECT_GUIDELINES] exists, read it and all referenced documentation to understand project conventions for error handling, logging, naming, and testing. These conventions MUST be followed in your design decisions.

    Then, explore the codebase using Glob, Grep, and Read tools to understand the existing architecture, patterns, and conventions.

    Then, design the implementation approach by making architectural decisions and planning components, APIs, tests, and tasks. Ensure all decisions align with project guidelines if they exist.

    Write to [SDD_DESIGN_DOCUMENT] replacing all template placeholders with the completed design information.

    Ensure the document follows the [SDD_TEMPLATE_DESIGN] exactly. Do **not** add or remove any sections.

    Ensure all requirements from [SDD_SPECIFICATION_DOCUMENT] are traced to components and tasks in the Requirements Validation section.

    Ensure the document follows sdd guidelines for sdd design documents.

    CRITICAL: You MUST use the Write tool to save the completed document to [SDD_DESIGN_DOCUMENT].
    Do NOT output the document content in your response - use the Write tool instead.
    Your response text is not visible to the user. Only the file you write will be seen.
    Call Write(file_path="[SDD_DESIGN_DOCUMENT]", content="<full document>") as your final action.

## STEP 5 - Ensure design document is complete
- Read [SDD_DESIGN_DOCUMENT] to verify it contains actual design content (not just the template)
- If the file is empty or contains only template placeholders:
  1. Resume the agent from STEP 4 using its agent ID
  2. Tell it: "The design document was not saved. You MUST use the Write tool now. Call Write with file_path=[SDD_DESIGN_DOCUMENT] and the complete design content."
  3. Re-check after the agent completes
- If still not saved after retry, manually extract design from agent's response and use Write tool directly
- Ensure [SDD_DESIGN_DOCUMENT] matches the [SDD_TEMPLATE_DESIGN] template. If it deviates ask the agent from STEP 4 to fix it
- Verify that all requirements from the specification are covered in the Requirements Validation section

## STEP 6 - Review design for completeness
- Create a Task with the design-reviewer agent to validate the design. Pass `SDD_DESIGN_DOCUMENT`, `SDD_SPECIFICATION_DOCUMENT`, and if project guidelines exist, `SDD_PROJECT_GUIDELINES`.
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
