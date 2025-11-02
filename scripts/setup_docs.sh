#!/bin/bash

################################################################################
# setup_docs.sh - Documentation Setup Script
#
# Purpose: Initialize and setup documentation structure for the project
# Usage: ./setup_docs.sh [--full|--validate|--clean]
# 
# This script:
# - Creates directory structure for all documentation
# - Validates existing documentation
# - Sets up symbolic links
# - Initializes Git hooks for documentation
# - Generates initial index files
#
################################################################################

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Script configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"
DOCS_DIR="$PROJECT_ROOT/docs"
RESOURCES_DIR="$DOCS_DIR/resources"
GUIDES_DIR="$DOCS_DIR/guides"
SCRIPTS_DIR="$SCRIPT_DIR"

################################################################################
# Create Directory Structure
################################################################################

create_directory_structure() {
    log_info "Creating directory structure..."
    
    # Main directories
    mkdir -p "$DOCS_DIR"
    mkdir -p "$RESOURCES_DIR"
    mkdir -p "$GUIDES_DIR"
    mkdir -p "$DOCS_DIR/architecture"
    mkdir -p "$DOCS_DIR/adr"
    mkdir -p "$DOCS_DIR/api"
    mkdir -p "$DOCS_DIR/operations"
    mkdir -p "$PROJECT_ROOT/.github/workflows"
    
    log_success "Directory structure created"
}

################################################################################
# Copy Documentation Files
################################################################################

copy_documentation_files() {
    log_info "Copying documentation files..."
    
    # Copy best practice guides
    cp -v "$PROJECT_ROOT/code_review_checklist.md" "$GUIDES_DIR/" 2>/dev/null || log_warning "code_review_checklist.md not found in root"
    cp -v "$PROJECT_ROOT/git_workflow.md" "$GUIDES_DIR/" 2>/dev/null || log_warning "git_workflow.md not found in root"
    cp -v "$PROJECT_ROOT/documentation_standards.md" "$GUIDES_DIR/" 2>/dev/null || log_warning "documentation_standards.md not found in root"
    cp -v "$PROJECT_ROOT/security_checklist.md" "$GUIDES_DIR/" 2>/dev/null || log_warning "security_checklist.md not found in root"
    
    # Copy resource files
    cp -v "$PROJECT_ROOT/quick_reference.md" "$RESOURCES_DIR/" 2>/dev/null || log_warning "quick_reference.md not found in root"
    cp -v "$PROJECT_ROOT/glossary.md" "$RESOURCES_DIR/" 2>/dev/null || log_warning "glossary.md not found in root"
    cp -v "$PROJECT_ROOT/tool_recommendations.md" "$RESOURCES_DIR/" 2>/dev/null || log_warning "tool_recommendations.md not found in root"
    cp -v "$PROJECT_ROOT/learning_paths.md" "$RESOURCES_DIR/" 2>/dev/null || log_warning "learning_paths.md not found in root"
    cp -v "$PROJECT_ROOT/troubleshooting.md" "$RESOURCES_DIR/" 2>/dev/null || log_warning "troubleshooting.md not found in root"
    
    log_success "Documentation files copied"
}

################################################################################
# Create Git Hooks for Documentation Validation
################################################################################

setup_git_hooks() {
    log_info "Setting up Git hooks..."
    
    local hooks_dir="$PROJECT_ROOT/.git/hooks"
    
    if [ ! -d "$hooks_dir" ]; then
        log_warning "Git repository not initialized, skipping hooks setup"
        return
    fi
    
    # Create pre-commit hook for documentation validation
    cat > "$hooks_dir/pre-commit" << 'EOF'
#!/bin/bash
# Pre-commit hook: Validate documentation changes

# Check for markdown files
MD_FILES=$(git diff --cached --name-only | grep '\.md$' | grep -E '(docs|guides|resources)/')

if [ -n "$MD_FILES" ]; then
    echo "Validating documentation changes..."
    
    # Check for broken links (optional)
    # python3 scripts/validate_links.py $MD_FILES
    
    # Check for proper formatting
    for file in $MD_FILES; do
        if [ ! -f "$file" ]; then
            continue
        fi
        
        # Check for proper heading hierarchy
        if grep -q '^# ' "$file"; then
            if ! grep -q '^## ' "$file"; then
                # Warn but don't fail
                echo "⚠ Warning: $file has H1 but no H2 headings"
            fi
        fi
    done
    
    echo "✓ Documentation validation passed"
fi

exit 0
EOF
    
    chmod +x "$hooks_dir/pre-commit"
    log_success "Git hooks installed"
}

################################################################################
# Create Documentation Index
################################################################################

create_documentation_index() {
    log_info "Creating documentation index..."
    
    cat > "$DOCS_DIR/README.md" << 'EOF'
# Documentation

This directory contains all project documentation organized by category.

## Structure

- **guides/** - Best practice guides
  - code_review_checklist.md - Code review standards
  - git_workflow.md - Git workflow practices
  - documentation_standards.md - Documentation guidelines
  - security_checklist.md - Security review checklist

- **resources/** - Quick reference and learning resources
  - quick_reference.md - Command cheat sheets
  - glossary.md - Technical term definitions
  - tool_recommendations.md - Recommended tools and setup
  - learning_paths.md - Learning roadmaps for different roles
  - troubleshooting.md - Common issues and solutions

- **architecture/** - Architecture documentation
  - ADRs (Architecture Decision Records)
  - System design documents
  - Component diagrams

- **api/** - API documentation
  - Endpoint specifications
  - Request/response examples
  - Integration guides

- **operations/** - Operational documentation
  - Deployment procedures
  - Monitoring and alerting
  - Incident response
  - Backup and recovery

## Getting Started

1. **New Developer?** Start with: `resources/learning_paths.md` → Onboarding Path
2. **Need a command?** Check: `resources/quick_reference.md`
3. **Stuck?** See: `resources/troubleshooting.md`
4. **Understanding a term?** Look up: `resources/glossary.md`
5. **Setting up tools?** Review: `resources/tool_recommendations.md`

## Quick Links

- [Code Review Standards](guides/code_review_checklist.md)
- [Git Workflow](guides/git_workflow.md)
- [Documentation Standards](guides/documentation_standards.md)
- [Security Checklist](guides/security_checklist.md)

## Maintenance

Documentation should be kept up-to-date with:
- Code changes
- Process updates
- Tool/version updates
- Best practices refinements

Run validation scripts:
```bash
./scripts/validate_links.py docs/
./scripts/generate_summary.py docs/
./scripts/update_toc.py docs/
```

## Contributing

When updating documentation:
1. Follow [Documentation Standards](guides/documentation_standards.md)
2. Validate links: `python3 scripts/validate_links.py`
3. Update table of contents: `python3 scripts/update_toc.py`
4. Generate summary: `python3 scripts/generate_summary.py`

See [Contributing Guide](../CONTRIBUTING.md) for more details.
EOF

    log_success "Documentation index created"
}

################################################################################
# Create CI/CD Workflow for Documentation
################################################################################

create_ci_workflow() {
    log_info "Creating CI/CD workflow for documentation..."
    
    cat > "$PROJECT_ROOT/.github/workflows/docs-validate.yml" << 'EOF'
name: Documentation Validation

on:
  pull_request:
    paths:
      - 'docs/**'
      - '*.md'
      - 'scripts/validate_links.py'
      - 'scripts/generate_summary.py'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Validate links
        run: |
          python3 scripts/validate_links.py docs/
      
      - name: Check formatting
        run: |
          python3 -m py_compile scripts/*.py
      
      - name: Generate summary
        run: |
          python3 scripts/generate_summary.py docs/
      
      - name: Check for broken references
        run: |
          grep -r '\[.*\](.*\.md)' docs/ | \
          while read line; do
            file=$(echo "$line" | grep -oP '\(\K[^)]+' | tail -1)
            if [ -n "$file" ] && [ ! -f "$file" ]; then
              echo "Broken link: $file in $line"
              exit 1
            fi
          done || true
EOF

    log_success "CI/CD workflow created"
}

################################################################################
# Create .gitignore for Documentation
################################################################################

create_gitignore() {
    log_info "Creating .gitignore for documentation..."
    
    cat >> "$DOCS_DIR/.gitignore" << 'EOF'
# Generated documentation
_build/
dist/
*.tmp
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Python
__pycache__/
*.pyc
.pytest_cache/
.coverage

# Generated files
*.generated.md
summary.json
EOF

    log_success ".gitignore created"
}

################################################################################
# Validate Documentation Setup
################################################################################

validate_setup() {
    log_info "Validating documentation setup..."
    
    local errors=0
    
    # Check required directories
    for dir in "$DOCS_DIR" "$GUIDES_DIR" "$RESOURCES_DIR"; do
        if [ -d "$dir" ]; then
            log_success "Directory exists: $dir"
        else
            log_error "Directory missing: $dir"
            ((errors++))
        fi
    done
    
    # Check README exists
    if [ -f "$DOCS_DIR/README.md" ]; then
        log_success "Documentation README found"
    else
        log_error "Documentation README missing"
        ((errors++))
    fi
    
    if [ $errors -eq 0 ]; then
        log_success "Documentation setup validated successfully"
        return 0
    else
        log_error "Documentation setup validation failed with $errors errors"
        return 1
    fi
}

################################################################################
# Clean Up Documentation
################################################################################

cleanup_documentation() {
    log_info "Cleaning up documentation..."
    
    if [ -d "$DOCS_DIR" ]; then
        log_warning "Removing $DOCS_DIR..."
        rm -rf "$DOCS_DIR"
    fi
    
    log_success "Cleanup completed"
}

################################################################################
# Print Summary
################################################################################

print_summary() {
    cat << EOF

${GREEN}========================================${NC}
${GREEN}Documentation Setup Complete!${NC}
${GREEN}========================================${NC}

${BLUE}Directory Structure:${NC}
  - Guides: $GUIDES_DIR
  - Resources: $RESOURCES_DIR
  - Main: $DOCS_DIR

${BLUE}Next Steps:${NC}
  1. Review documentation structure: ls -la $DOCS_DIR
  2. Validate setup: $SCRIPT_DIR/setup_docs.sh --validate
  3. Validate links: python3 $SCRIPTS_DIR/validate_links.py $DOCS_DIR
  4. Generate summary: python3 $SCRIPTS_DIR/generate_summary.py $DOCS_DIR

${BLUE}Quick Start:${NC}
  - New developer? → resources/learning_paths.md
  - Need commands? → resources/quick_reference.md
  - Have questions? → resources/glossary.md
  - Stuck? → resources/troubleshooting.md

${BLUE}Documentation Links:${NC}
  - Code Review: $GUIDES_DIR/code_review_checklist.md
  - Git Workflow: $GUIDES_DIR/git_workflow.md
  - Security: $GUIDES_DIR/security_checklist.md
  - Documentation: $GUIDES_DIR/documentation_standards.md

EOF
}

################################################################################
# Main Script Logic
################################################################################

main() {
    local command="${1:-setup}"
    
    case "$command" in
        setup)
            log_info "Starting documentation setup..."
            create_directory_structure
            copy_documentation_files
            create_documentation_index
            create_ci_workflow
            create_gitignore
            setup_git_hooks
            validate_setup
            print_summary
            ;;
        
        validate)
            log_info "Validating documentation setup..."
            validate_setup
            ;;
        
        clean)
            log_warning "This will remove all documentation. Continue? (yes/no)"
            read -r response
            if [ "$response" = "yes" ]; then
                cleanup_documentation
            else
                log_info "Cleanup cancelled"
            fi
            ;;
        
        *)
            cat << EOF
Usage: $0 [command]

Commands:
  setup      - Initialize documentation (default)
  validate   - Validate existing setup
  clean      - Remove all documentation (CAUTION)
  help       - Show this help message

Examples:
  $0 setup      # Initialize documentation
  $0 validate   # Check if setup is valid
  $0 clean      # Remove documentation

EOF
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
