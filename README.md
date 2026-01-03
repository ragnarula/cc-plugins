# Claude Code Plugin Marketplace

A curated collection of high-quality plugins for Claude Code.

## Available Plugins

### [SDD (Spec Driven Development)](./sdd/)

**Version:** 0.1.2

A structured approach to software development that combines the rigor of upfront specification with the flexibility of iterative implementation.

**Features:**
- Specification phase (`/specify`) - Define requirements with clarity and precision
- Design phase (`/design`) - Plan architecture and implementation strategy
- Implementation phase (`/implement`) - Build with TDD and automated reviews
- Specialized agents for analysis, design, implementation, and review
- Living documentation and requirements traceability

**Use Case:** For developers who want disciplined, specification-driven development with AI assistance.

[View Plugin Details →](./sdd/README.md)

---

### [Value Investor](./value-investor/)

**Version:** 0.1.0

A comprehensive investment analysis workflow for evaluating publicly traded companies using Warren Buffett and Charlie Munger's value investing principles.

**Features:**
- Multi-stage analysis workflow (screening → deep dive → valuation → report)
- Autonomous agents for business analysis, financial modeling, and risk assessment
- Built-in value investing frameworks and mental models
- Human approval gates at each stage
- Systematic 10-year financial analysis

**Use Case:** For investors who want to apply disciplined value investing principles to evaluate public companies.

[View Plugin Details →](./value-investor/README.md)

## Installation

### Installing a Plugin

To use any plugin from this marketplace:

```bash
# Clone the marketplace repository
git clone <repository-url> cc-plugins

# Navigate to the marketplace directory
cd cc-plugins

# Use the plugin with Claude Code
cc --plugin-dir ./value-investor
```

### Project-Specific Installation

To install a plugin for a specific project:

```bash
# Copy the desired plugin to your project
cp -r cc-plugins/value-investor /path/to/your/project/.claude-plugin/
```

## Plugin Development

Want to contribute a plugin? Check out the [Claude Code plugin development documentation](https://docs.anthropic.com/claude-code) for guidelines and best practices.

### Submission Guidelines

1. Follow Claude Code plugin structure conventions
2. Include comprehensive README with examples
3. Provide clear installation and configuration instructions
4. Test thoroughly before submission
5. Include appropriate error handling and user feedback

## Repository Structure

```
cc-plugins/
├── README.md                    # This file
├── .claude-plugin/
│   └── marketplace.json         # Plugin registry
├── sdd/                         # Spec Driven Development plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/
│   ├── commands/
│   ├── skills/
│   └── README.md
├── value-investor/              # Value Investor plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/
│   ├── commands/
│   ├── skills/
│   └── README.md
└── [future-plugin]/             # Additional plugins...
```

## License

Individual plugins may have their own licenses. Check each plugin's directory for license information.

## Support

For issues with specific plugins, please check the plugin's README for troubleshooting guidance.

For general Claude Code questions, visit: https://docs.anthropic.com/claude-code
