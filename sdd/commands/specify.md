---
name: specify
description: Write a specification for a feature. Documents the 'What' and 'Why' for approval by stakeholders, without deciding implementation details yet. Captures functional and non-functional requirements for later use in architecture planning. Follows standard process for capturing requirements according to templates.
arguments:
  - FEATURE (The name of the feature)
  - DESCRIPTON (A brief description)
allowed-tools: ["Read", "Write", "Bash", "WebSearch", "WebFetch", "Glob", "Grep", "Task"]
---

You must use the sdd skill.

# Specify

Create a specification document for a feature according to the `specification.template.md` template. Iterate on the document until all open questions are answered and no further clarifications are necessary.

## STEP 1 - Create an empty specification document
- Create an empty folder in the [SDD_FOLDER] directory from the sdd skill named after the feature if it doesn't already exist. This directory will be the `SDD_PROJECT_FOLDER`
- Create a blank [SSD_TEMPlATE_SPECIFICATION] document in the [SDD_PROJECT_FOLDER] directory if it doesn't already exist
- Fill the metadata in the header of the document including current date, feature name, status (Draft), version etc.

## STEP 2 - Fill in the document
- Create a Task with the technical-analyst agent and do the following. Pass the new specification document's path to it's context as `SDD_SPECIFICATION_DOCUMENT`.
  - |
    The [SDD_SPECIFICATION_DOCUMENT] file needs to be completed to the highest standard. The header has already been filled out.
    Interview the user to understand the rest of the specifications and requirements
    Write to [SDD_SPECIFICATION_DOCUMENT] replacing all tempalte placeholders with the completed information
    Ensure the document follows the [SDD_TEMPLATE_SPECIFICATION] exactly. Do **not** add or remove any sections.
    Ensure the document follows sdd guidelies for sdd specifications
    Do **not** forget to actually save the document to disk. Don't just present it to the user
  
## STEP 3 - Ensure specification document is complete
- Ensure [SDD_SPECIFICATION_DOCUMENT] is completed and saved to disk and all placeholders from the template have been replaced with actual information
- If the document is not saved to disk, ask the agent from STEP 2 to write it to disk and re check
- Ensure [SDD_SPECIFICATION_DOCUMENT] matches the [SDD_TEMPLATE_SPECIFICATION] template. If it deviates ask the agent from STEP 2 to fix it
