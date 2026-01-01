# Design: [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Status:** Draft | Under Review | Approved | Implemented
**Linked Specification** `.sdd/<feature>/specification.md`

---

# Design Document

---

## Architecture Overview

### Current Architecture Context
- [How does this fit into existing system?]

### Proposed Architecture
- [Diagram or description]
- [Key patterns and rationale]
- [Sequence diagram if necessary]

### Technology Decisions
- [Choices and justification]

### Quality Attributes
- [Scalability approach]
- [Maintainability considerations]

---

## API Design [Optional if there are public interfaces needed]
- [Public interface definitions]
- [Data models and schemas]
- [Error handling strategy]
- [Versioning approach]

---

## Modified Components

### [Modified Component 1]
**Change Description** [Short description of what it currently does and what it needs to do. Describe the delta]

**Dependants** [Any dependants that need to be modified as a result]

**Kind** [Function | Class | Module | Crate etc]

**Requirements References**
- REQ-FN/NFN-?: [1st Example requirement that necessitates this change]
- REQ-FN/NFN-?: [2nd Example requirement that necessitates this change]

**Test Cases**
- TEST-NAME-1: [Short description of the test]
- TEST-NAME-2: [Short description of the test]

### [Modified Component 2]
**Change Description** [Short description of what it currently does and what it needs to do. Describe the delta]

**Dependants** [Any dependants that need to be modified as a result]

**Kind** [Function | Class | Module | Crate etc]

**Requirements References**
- REQ-FN/NFN-?: [1st Example requirement that necessitates this change]
- REQ-FN/NFN-?: [2nd Example requirement that necessitates this change]

**Test Cases**
- TEST-NAME-1: [Short description of the test]
- TEST-NAME-2: [Short description of the test]

---

## Added Components

### [Added Component 1]
**Description** [Short description of what the new component should do]

**Users** [Who/what will call/use this component?]

**Kind** [Function | Class | Module | Crate etc]

**Location** [Which file/class/module/crate will this new component be located in?]

**Requirements References**
- REQ-FN/NFN-?: [1st Example requirement that necessitates this change]
- REQ-FN/NFN-?: [2nd Example requirement that necessitates this change]

**Test Cases**
- TEST-NAME-1: [Short description of the test]
- TEST-NAME-2: [Short description of the test]

### [Added Component 2]
**Description** [Short description of what the new component should do]

**Users** [Who/what will call/use this component?]

**Kind** [Function | Class | Module | Crate etc]

**Location** [Which file/class/module/crate will this new component be located in?]

**Requirements References**
- REQ-FN/NFN-?: [1st Example requirement that necessitates this change]
- REQ-FN/NFN-?: [2nd Example requirement that necessitates this change]

**Test Cases**
- TEST-NAME-1: [Short description of the test]
- TEST-NAME-2: [Short description of the test]

---

## Documentation Considerations
- [Developer docs that need to be created/updated]
- [API docs that need to be created/updated]
- [Readme's docs that need to be created/updated]
- [Any other documentation considerations?]

---

## Test Strategy

### Test Pyramid
- Unit: [What to unit test in addition to components above]
- Integration: [What to integration test]
- E2E: [What to test end-to-end]

### Coverage Strategy
- Critical paths: [...]
- Performance tests: [...]
- Security tests: [...]

### Test Data
- [Requirements and sources]

### Test Feasibility
- [Missing test infrastructure that should be built first]
- [Missing test data that should be acquired first]

---

## Risks and Dependencies
- [Technical risks and mitigation]
- [External dependencies]
- [Assumptions and constraints]

---

## Feasability Review
- [Large missing feature that needs to be built first as separate iteration]
- [Large missing infrastructure that needs to be available first as separate iteration]

---


## Task Breakdown

### Phase [1] [Goal of this phase]
- Task [1]: [Short description of the task]
  - Status: [Backlog | In Progress | Done]
  - [More detailed description if necessary]
- Task [2]: [Short description of the task]
  - Status: [Backlog | In Progress | Done]
  - [More detailed description if necessary]
  
### Phase [2] [Goal of this phase]
- Task [1]: [Short description of the task]
  - Status: [Backlog | In Progress | Done]
  - [More detailed description if necessary]
- Task [2]: [Short description of the task]
  - Status: [Backlog | In Progress | Done]
  - [More detailed description if necessary]

---

## Requirements Validation

Ensure all requirements have matching tasks

- REQ-FN-[1]
  - Phase [X] Task [Y]
  - Phase [Y] Task [Z]
- REQ-FN-[2]
  - Phase [X] Task [Y]
  - Phase [Y] Task [Z]

- REQ-NFN-[1]
  - Phase [X] Task [Y]
  - Phase [Y] Task [Z]
- REQ-NFN-[2]
  - Phase [X] Task [Y]
  - Phase [Y] Task [Z]

---

## Appendix

### Glossary
- **Term 1:** Definition
- **Term 2:** Definition

### References
- [Link to related documents, research, or external specifications]

### Change History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | [Name] | Initial design |

---
