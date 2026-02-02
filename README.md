# Claude Code Plugin Marketplace

A curated collection of high-quality plugins for Claude Code.

## Available Plugins

### [SDD (Spec Driven Development)](./sdd/)

**Version:** 0.1.11

A structured approach to software development that combines rigorous upfront specification with iterative implementation.

**Features:**
- **Specify** - Define requirements (FR-XXX, NFR-XXX) with clarity and precision
- **Design** - Plan architecture with test scenarios (Given/When/Then) and task breakdown
- **Implement** - Build with TDD, progress tracking in design documents
- Full traceability from requirements → components → test scenarios → tasks → code
- Validation sections to ensure no orphan requirements or scenarios

**Use Case:** For developers who want disciplined, specification-driven development with AI assistance.

[View Plugin Details →](./sdd/README.md)

---

## Installation

### Install from GitHub (Recommended)

Add this marketplace to Claude Code, then install plugins:

```bash
# Add the marketplace
/plugin marketplace add ragnarula/cc-plugins

# Install plugins
/plugin install sdd@ragnarula-cc-plugins
```

Or via the CLI:

```bash
claude plugin marketplace add ragnarula/cc-plugins --scope user
claude plugin install sdd@ragnarula-cc-plugins --scope user
```

**Scope options:**
- `user` - Install for yourself across all projects (default)
- `project` - Install for all collaborators in the repository
- `local` - Install only for yourself in this repository

### Install from Local Clone

Clone the repository and use a plugin directly:

```bash
git clone https://github.com/ragnarula/cc-plugins.git
claude --plugin-dir ./cc-plugins/sdd
```

### Project-Specific Installation

Copy a plugin into your project's `.claude-plugin/` directory:

```bash
git clone https://github.com/ragnarula/cc-plugins.git
cp -r cc-plugins/sdd /path/to/your/project/.claude-plugin/
```

## Repository Structure

```
cc-plugins/
├── README.md                       # This file
├── .claude-plugin/
│   └── marketplace.json            # Plugin registry
└── sdd/                            # Spec Driven Development plugin
    ├── .claude-plugin/
    │   └── plugin.json
    ├── skills/
    │   ├── sdd/
    │   │   ├── SKILL.md            # Core SDD methodology
    │   │   └── templates/
    │   │       ├── specification.template.md
    │   │       ├── design.template.md
    │   │       ├── index.template.md
    │   │       └── project-guidelines.template.md
    │   └── project-guidelines/
    │       └── SKILL.md            # Guidelines reading process
    └── README.md
```
