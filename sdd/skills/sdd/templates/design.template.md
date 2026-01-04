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

> **CRITICAL: Tests are written WITH implementation, not after.**
> Each task that adds or modifies functionality MUST include writing tests as part of that task.
> Do NOT create separate "Add tests" tasks or defer testing to later phases.
> TDD approach: Write failing test → Implement → Verify test passes → Refactor.

### Phase [1] [Goal of this phase]
- Task [1]: [Short description of the task]
  - Status: [Backlog | In Progress | Done]
  - [More detailed description if necessary]
  - Tests: [Which test cases from component definitions are written in this task]
- Task [2]: [Short description of the task]
  - Status: [Backlog | In Progress | Done]
  - [More detailed description if necessary]
  - Tests: [Which test cases from component definitions are written in this task]

### Phase [2] [Goal of this phase]
- Task [1]: [Short description of the task]
  - Status: [Backlog | In Progress | Done]
  - [More detailed description if necessary]
  - Tests: [Which test cases from component definitions are written in this task]
- Task [2]: [Short description of the task]
  - Status: [Backlog | In Progress | Done]
  - [More detailed description if necessary]
  - Tests: [Which test cases from component definitions are written in this task]

---

## Intermediate Dead Code Tracking

> Code introduced in earlier phases that will be used in later phases must be tracked here.
> All entries must be resolved (code used or removed) by the final phase.

| Phase Introduced | Description | Used In Phase | Status |
|------------------|-------------|---------------|--------|
| [Example: Phase 1] | [Example: Helper functions for data transformation] | [Example: Phase 3] | [Pending/Resolved] |

---

## Intermediate Stub Tracking

> **CRITICAL: Stubs are NOT acceptable without explicit tracking.**
> All stubs MUST be fully implemented as part of the task that introduces the code they test.
> If a stub is absolutely necessary (e.g., external dependency not yet available), it MUST be tracked here.
> All entries must be resolved (stub implemented or removed) by the final phase.
> A "stub" includes: `skip`, `todo`, `pass`, `pytest.mark.skip`, `@unittest.skip`, `it.skip`, `xit`, `pending`, empty test bodies, or `assert True` placeholders.

| Phase Introduced | Test Name | Reason for Stub | Implemented In Phase | Status |
|------------------|-----------|-----------------|----------------------|--------|
| [Example: Phase 1] | [Example: test_external_api_integration] | [Example: External API not yet configured in CI] | [Example: Phase 3] | [Pending/Resolved] |

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
