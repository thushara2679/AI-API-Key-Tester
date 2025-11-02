# Automation Scripts

This directory contains automation scripts for managing, validating, and maintaining the Advanced AI Agent System documentation and configuration.

## Overview

Five powerful automation scripts designed to streamline documentation management and system configuration:

| Script | Purpose | Type | Lines |
|--------|---------|------|-------|
| `setup_docs.sh` | Initialize documentation structure | Bash | 471 |
| `validate_links.py` | Validate markdown links | Python | 317 |
| `generate_summary.py` | Generate documentation statistics | Python | 349 |
| `update_toc.py` | Auto-update table of contents | Python | 287 |
| `agent_config.py` | Manage agent configurations | Python | 484 |
| **TOTAL** | | | **1,908** |

---

## Scripts

### 1. setup_docs.sh
**Documentation Setup Script**

Initialize and setup documentation structure for the project.

**Usage:**
```bash
./setup_docs.sh [command]

Commands:
  setup      - Initialize documentation (default)
  validate   - Validate existing setup
  clean      - Remove all documentation
  help       - Show help message
```

**Features:**
- ✓ Creates directory structure for guides and resources
- ✓ Copies documentation files
- ✓ Sets up Git hooks for validation
- ✓ Creates CI/CD workflows
- ✓ Generates index files
- ✓ Validates setup completeness

**Examples:**
```bash
# Initialize documentation
./setup_docs.sh setup

# Validate existing setup
./setup_docs.sh validate

# Clean up (caution!)
./setup_docs.sh clean
```

**Directory Structure Created:**
```
docs/
├── guides/                 # Best practice guides
│   ├── code_review_checklist.md
│   ├── git_workflow.md
│   ├── documentation_standards.md
│   └── security_checklist.md
├── resources/              # Quick references and resources
│   ├── quick_reference.md
│   ├── glossary.md
│   ├── tool_recommendations.md
│   ├── learning_paths.md
│   └── troubleshooting.md
├── architecture/           # Architecture docs
├── api/                   # API documentation
├── operations/            # Operational docs
└── README.md              # Documentation index
```

---

### 2. validate_links.py
**Markdown Link Validation Script**

Validate all links in markdown documentation files.

**Usage:**
```bash
python3 validate_links.py [path] [--strict] [--fix]

Arguments:
  path      - Path to markdown file or directory
  --strict  - Check external URLs (slower)
  --fix     - Attempt to auto-fix issues
```

**Features:**
- ✓ Finds and validates all markdown links
- ✓ Checks internal file references
- ✓ Validates external URLs (optional)
- ✓ Reports issues with line numbers
- ✓ Generates comprehensive report
- ✓ Exit codes for CI/CD integration

**Examples:**
```bash
# Validate single file
python3 validate_links.py README.md

# Validate directory
python3 validate_links.py docs/

# Check external links too (slow)
python3 validate_links.py docs/ --strict

# Validate multiple files
python3 validate_links.py docs/*.md
```

**Output Example:**
```
ℹ Validating: docs/guides/git_workflow.md
ℹ Validating: docs/resources/quick_reference.md

======================================================================
Link Validation Report
======================================================================

✓ git_workflow.md

✗ quick_reference.md:
  ✗ Line 45: File not found: docs/missing.md
    Link: [Missing File](docs/missing.md)

======================================================================
Summary
======================================================================
Files validated: 10
Errors found: 1
Warnings: 0
Issues fixed: 0

✗ Found 1 broken link
```

---

### 3. generate_summary.py
**Documentation Summary Generator**

Generate comprehensive summary and statistics for documentation.

**Usage:**
```bash
python3 generate_summary.py [path] [--output file.json] [--format json|md|txt]

Arguments:
  path        - Path to documentation directory
  --output    - Export to JSON file
  --format    - Output format (default: txt)
```

**Features:**
- ✓ Counts files, lines, sections
- ✓ Generates detailed statistics
- ✓ Analyzes content structure
- ✓ Creates comprehensive index
- ✓ Exports in multiple formats (JSON, Markdown, Text)
- ✓ Groups by category

**Examples:**
```bash
# Generate text summary
python3 generate_summary.py docs/

# Export to JSON
python3 generate_summary.py docs/ --output summary.json

# Generate markdown
python3 generate_summary.py docs/ --format md > summary.md

# Export and format
python3 generate_summary.py docs/ --format json --output stats.json
```

**Output Example:**
```
======================================================================
                    Documentation Summary
======================================================================

OVERALL STATISTICS
  Total Files:    15
  Total Lines:    4,325
  Total Words:    52,180
  Total Size:     236.5KB

BY CATEGORY

  Guides:
    Files:  4
    Lines:  3,735
    Words:  45,000
    Size:   163KB

  Resources:
    Files:  5
    Lines:  3,902
    Words:  48,000
    Size:   86KB

  API:
    Files:  2
    Lines:  450
    Words:  5,000
    Size:   18KB
```

---

### 4. update_toc.py
**Table of Contents Update Script**

Automatically generate and update table of contents in markdown files.

**Usage:**
```bash
python3 update_toc.py [path] [--in-place] [--max-depth N]

Arguments:
  path       - Path to markdown file or directory
  --in-place - Update files in-place
  --max-depth - Maximum heading depth (default: 3)
```

**Features:**
- ✓ Generates TOC from markdown headings
- ✓ Updates existing TOC automatically
- ✓ Handles nested heading levels
- ✓ Generates proper anchor links
- ✓ Processes multiple files
- ✓ Can write in-place or to stdout

**Examples:**
```bash
# Generate TOC for file (print to stdout)
python3 update_toc.py docs/README.md

# Update file in-place
python3 update_toc.py docs/README.md --in-place

# Update all files in directory
python3 update_toc.py docs/ --in-place

# Update with max depth of 2
python3 update_toc.py docs/ --in-place --max-depth 2
```

**Generated TOC Format:**
```markdown
## Table of Contents

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
```

---

### 5. agent_config.py
**Agent Configuration Utility**

Manage and configure agents in the Advanced AI Agent System.

**Usage:**
```bash
python3 agent_config.py [command] [options]

Commands:
  init       - Initialize new agent
  list       - List all agents
  create     - Create agent with options
  validate   - Validate agent configuration
  info       - Show agent information
  export     - Export all configurations
  import     - Import configurations
  docs       - Generate documentation
```

**Features:**
- ✓ Create and manage agent configurations
- ✓ Validate agent specifications
- ✓ Generate documentation
- ✓ Export/import configurations
- ✓ Support for multiple agent types
- ✓ Environment-specific configuration

**Agent Types:**
- `worker` - Process data
- `coordinator` - Orchestrate other agents
- `validator` - Validate data/results
- `transformer` - Transform data
- `aggregator` - Combine/aggregate results

**Examples:**
```bash
# Initialize new agent
python3 agent_config.py init my-agent

# List all agents
python3 agent_config.py list

# Create agent with options
python3 agent_config.py create worker-1 \
  --type worker \
  --description "Main data processor"

# Validate agent configuration
python3 agent_config.py validate my-agent

# Show agent info
python3 agent_config.py info my-agent

# Export all configurations
python3 agent_config.py export --output agents.json

# Import configurations
python3 agent_config.py import agents.json

# Generate documentation
python3 agent_config.py docs my-agent > my-agent.md
```

**Generated Agent Configuration (YAML):**
```yaml
name: my-agent
version: 1.0.0
type: worker
description: Agent description
created: 2025-10-26T12:00:00
updated: 2025-10-26T12:00:00

capabilities:
  - data-processing
  - validation

dependencies:
  - database-service
  - message-queue

configuration:
  timeout: 30
  retries: 3
  max_workers: 5
  logging:
    level: INFO
    format: structured

environment:
  development:
    db_host: localhost
  staging:
    db_host: staging-db.example.com
  production:
    db_host: prod-db.example.com

interfaces:
  input:
    - data
    - config
  output:
    - result
    - status
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Bash shell (for setup_docs.sh)
- YAML support: `pip install pyyaml`

### Setup
```bash
# Install required packages
pip install pyyaml requests

# Make scripts executable
chmod +x setup_docs.sh
chmod +x validate_links.py
chmod +x generate_summary.py
chmod +x update_toc.py
chmod +x agent_config.py

# Or all at once
chmod +x *.sh *.py
```

---

## Usage Examples

### Complete Documentation Setup

```bash
# 1. Initialize documentation
./setup_docs.sh setup

# 2. Validate links
python3 validate_links.py docs/

# 3. Generate summary
python3 generate_summary.py docs/ --format md > SUMMARY.md

# 4. Update all table of contents
python3 update_toc.py docs/ --in-place

# 5. Commit changes
git add docs/
git commit -m "docs: regenerated documentation"
```

### Agent Configuration Management

```bash
# 1. Create agents
python3 agent_config.py init processor-1
python3 agent_config.py init validator-1 --type validator
python3 agent_config.py init coordinator-1 --type coordinator

# 2. List agents
python3 agent_config.py list

# 3. Validate configurations
python3 agent_config.py validate processor-1
python3 agent_config.py validate validator-1

# 4. Export for deployment
python3 agent_config.py export --output agents.json

# 5. Generate documentation
python3 agent_config.py docs processor-1 > AGENTS.md
```

### CI/CD Integration

```bash
# In CI/CD pipeline:
set -e

# Validate documentation
./setup_docs.sh validate
python3 validate_links.py docs/ --strict

# Validate agents
python3 agent_config.py validate my-agent

# Generate reports
python3 generate_summary.py docs/ --output summary.json

echo "✓ All validation passed"
```

---

## CI/CD Workflows

### GitHub Actions Example

```yaml
name: Documentation Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install pyyaml requests
      
      - name: Setup documentation
        run: ./setup_docs.sh validate
      
      - name: Validate links
        run: python3 validate_links.py docs/ --strict
      
      - name: Generate summary
        run: python3 generate_summary.py docs/
      
      - name: Validate agents
        run: python3 agent_config.py validate my-agent
```

---

## Error Handling

### Common Issues

**Python not found:**
```bash
# Use python3 explicitly
python3 validate_links.py docs/

# Or add shebang to PATH
which python3
```

**Permission denied:**
```bash
# Make scripts executable
chmod +x *.sh *.py
```

**YAML module not found:**
```bash
pip install pyyaml
```

**Broken links not found:**
```bash
# Check link format
# - Correct: [text](path/to/file.md)
# - Wrong: [text](path to file.md)
```

---

## Troubleshooting

### Script Troubleshooting

**setup_docs.sh issues:**
- Git repository not initialized: Initialize with `git init`
- Directory permission denied: Check directory permissions
- CI/CD workflow error: Ensure YAML syntax is correct

**validate_links.py issues:**
- Links checked too slowly: Use `--strict` flag only when needed
- False positives on anchor links: Check anchor format matches headings
- External links timeout: Increase timeout or skip with `--no-external`

**generate_summary.py issues:**
- JSON export fails: Check file write permissions
- Word counts seem off: Some punctuation counted as words

**update_toc.py issues:**
- TOC not updating: Check for `<!-- toc -->` markers
- Anchor links broken: Verify heading text matches
- Depth not respected: Use `--max-depth N` option

**agent_config.py issues:**
- YAML syntax error: Check indentation and format
- Validation fails: Review error messages for specific issues
- Import fails: Ensure JSON format is correct

---

## Performance

### Script Performance

| Script | Files | Time | Notes |
|--------|-------|------|-------|
| setup_docs.sh | 1 | <1s | Directory creation only |
| validate_links.py | 20 | 2-3s | Local links only |
| validate_links.py | 20 | 30s+ | With --strict (external URLs) |
| generate_summary.py | 20 | 1-2s | Full analysis |
| update_toc.py | 20 | 1-2s | In-place update |
| agent_config.py | All | <1s | YAML operations |

---

## Contributing

When adding new scripts:
1. Add shebang line for language
2. Include comprehensive docstring
3. Add color-coded output messages
4. Support --help flag
5. Use proper exit codes
6. Add examples to README

---

## License

These automation scripts are part of the Advanced AI Agent System documentation and are provided as-is.

---

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review script help: `./script.sh --help` or `python3 script.py --help`
3. Check documentation in guides/ and resources/
4. Contact project maintainers

---

## Quick Reference

```bash
# Documentation management
./setup_docs.sh setup              # Initialize docs
python3 validate_links.py docs/    # Check links
python3 generate_summary.py docs/  # Generate stats
python3 update_toc.py docs/ --in-place  # Update TOC

# Agent management
python3 agent_config.py init agent-name        # Create agent
python3 agent_config.py list                   # List agents
python3 agent_config.py validate agent-name    # Validate
python3 agent_config.py export --output agents.json  # Export
python3 agent_config.py docs agent-name        # Generate docs
```

---

**Total Lines of Automation:** 1,908 lines
**Coverage:** Documentation management, validation, and agent configuration
**Ready to use:** ✅ Production-ready

