---
name: design
description: Design an implementation plan from a specification. Documents the 'How' - architectural decisions, component design, API contracts, test strategy, and task breakdown. Follows SDD Phase 2 methodology to transform specifications into actionable implementation plans.
arguments:
  - FEATURE (The name of the feature)
  - DESCRIPTION (A brief description)
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "LSP", "Task"]
---

You must use the sdd skill.

# Design

Create a design document for a feature according to the `design.template.md` template. The design should be based on an existing specification and should explore the codebase to understand current architecture before making design decisions.

## STEP 1 - Verify specification exists
- Look for the specification document in [SDD_FOLDER]/[FEATURE]/specification.md
- If the specification doesn't exist, inform the user they need to run `/specify` first
- The specification is required as input for the design process

## STEP 2 - Create an empty design document
- The [SDD_PROJECT_FOLDER] directory should already exist from the specification phase at [SDD_FOLDER]/[FEATURE]
- Create a blank [SDD_TEMPLATE_DESIGN] document in the [SDD_PROJECT_FOLDER] directory if it doesn't already exist
- The file should be named `design.md`
- Fill the metadata in the header of the document including current date, feature name, status (Draft), version, and link to specification

## STEP 3 - Fill in the document
- Create a Task with the technical-architect agent and do the following. Pass the new design document's path to it's context as `SDD_DESIGN_DOCUMENT` and the specification document's path as `SDD_SPECIFICATION_DOCUMENT`.
  - |
    The [SDD_DESIGN_DOCUMENT] file needs to be completed to the highest standard. The header has already been filled out.

    First, read the [SDD_SPECIFICATION_DOCUMENT] to understand all functional and non-functional requirements.

    Then, explore the codebase using Glob, Grep, and Read tools to understand the existing architecture, patterns, and conventions.

    Then, design the implementation approach by making architectural decisions and planning components, APIs, tests, and tasks.

    Write to [SDD_DESIGN_DOCUMENT] replacing all template placeholders with the completed design information.

    Ensure the document follows the [SDD_TEMPLATE_DESIGN] exactly. Do **not** add or remove any sections.

    Ensure all requirements from [SDD_SPECIFICATION_DOCUMENT] are traced to components and tasks in the Requirements Validation section.

    Ensure the document follows sdd guidelines for sdd design documents.

    Do **not** forget to actually save the document to disk. Don't just present it to the user.

## STEP 4 - Ensure design document is complete
- Ensure [SDD_DESIGN_DOCUMENT] is completed and saved to disk and all placeholders from the template have been replaced with actual design information
- If the document is not saved to disk, ask the agent from STEP 3 to write it to disk and re-check
- Ensure [SDD_DESIGN_DOCUMENT] matches the [SDD_TEMPLATE_DESIGN] template. If it deviates ask the agent from STEP 3 to fix it
- Verify that all requirements from the specification are covered in the Requirements Validation section
