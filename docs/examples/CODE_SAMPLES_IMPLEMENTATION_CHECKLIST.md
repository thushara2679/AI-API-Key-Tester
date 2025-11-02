# Code Samples & Examples - Implementation Checklist

## 📋 Quick Start Checklist

Use this checklist when adding any code sample or complete project.

---

## Phase 1: Code Extraction (1-2 hours)

### Step 1: Identify & Select Code
- [ ] Code solves a common problem
- [ ] Code is production-tested
- [ ] Code is 50-500 lines (for samples)
- [ ] Code can work independently
- [ ] Code follows best practices

**Questions to Ask**:
1. Is this code used in multiple projects?
2. Does this implement a reusable pattern?
3. Would other developers benefit from this?
4. Is the code well-tested?
5. Is the code well-understood by the team?

### Step 2: Prepare Code for Publishing
- [ ] Remove project-specific imports
- [ ] Replace hardcoded values with parameters
- [ ] Remove debug/commented code
- [ ] Add comprehensive docstrings
- [ ] Add type hints
- [ ] Add error handling
- [ ] Verify code runs independently
- [ ] Add license header

**Conversion Template**:
```python
# BEFORE (Project-specific)
import config  # From project
from logging_setup import get_logger  # From project

logger = get_logger("payment_processor")
db = config.DATABASE_URL

# AFTER (Generic, reusable)
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def process_payment(db_url: str, payment_data: Dict[str, Any]) -> bool:
    """Process payment with provided configuration."""
    # Implementation
```

---

## Phase 2: Documentation (1-2 hours)

### Step 1: Create Code Comments
- [ ] Module docstring (50-100 words)
- [ ] Class docstrings for all classes
- [ ] Function docstrings for all functions
- [ ] Inline comments for complex logic
- [ ] Type hints on all parameters
- [ ] Examples in docstrings

**Docstring Template**:
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief one-line description.
    
    Longer description explaining what this function does,
    why it's useful, and when to use it.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        ValueError: If param1 is empty
        TypeError: If param2 is not an integer
    
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    
    Note:
        This function is async-safe for concurrent use.
        Thread-safe implementation.
    
    See Also:
        - related_function()
        - another_function()
    """
```

### Step 2: Create Metadata File
**File**: `{sample_name}.metadata.json`

```json
{
  "name": "Sample Name",
  "filename": "sample_name.py",
  "language": "Python",
  "category": "Backend/Feature",
  "difficulty": "intermediate",
  "complexity_score": 3.5,
  "lines_of_code": 150,
  "estimated_read_time_minutes": 10,
  "estimated_implementation_time_minutes": 30,
  "description": "Clear description of what this code does",
  "use_cases": ["Use case 1", "Use case 2"],
  "prerequisites": ["Requirement 1"],
  "dependencies": ["dependency1", "dependency2"],
  "learning_outcomes": ["Learn X", "Learn Y"],
  "tags": ["tag1", "tag2"],
  "status": "production_ready"
}
```

### Step 3: Create README
**File**: `{sample_name}_README.md`

- [ ] Overview section (2-3 paragraphs)
- [ ] Key features (bullet list)
- [ ] When to use (1 paragraph)
- [ ] When NOT to use (1 paragraph)
- [ ] Installation section
- [ ] Usage section (3-5 examples)
- [ ] API reference
- [ ] Error handling
- [ ] Performance tips
- [ ] Related samples
- [ ] Compatibility matrix

**Section Template**:
```markdown
# Sample Name

## Overview
Brief explanation of what this code does and why it's useful.

## Key Features
- Feature 1
- Feature 2
- Feature 3

## When to Use
Use this when you need to...

## When NOT to Use
Don't use this when...

## Installation
```bash
pip install dependency
```

## Usage

### Basic Example
```python
code_example_here()
```

### Advanced Example
```python
advanced_example()
```

## API Reference

### Class/Function Name
Description of what it does.

**Parameters**:
- param1 (type): Description

**Returns**: Description

**Raises**: Exceptions it can raise

## Error Handling
Common errors and how to handle them.

## Performance Tips
- Tip 1
- Tip 2

## Related Samples
- [Sample A](link)
- [Sample B](link)

## Compatibility Matrix
| Version | Support |
|---------|---------|
| 3.8     | ✅      |
| 3.9     | ✅      |

## License
MIT License
```

### Step 4: Create Usage Examples
**File**: `{sample_name}_example.py`

```python
"""
Complete working examples for {Sample Name}.

This file demonstrates various use cases and patterns.
Run individual examples to see how the code works.
"""

# ============================================================================
# EXAMPLE 1: Basic Usage
# ============================================================================

def example_basic():
    """Basic usage example."""
    from sample_name import SampleClass
    
    obj = SampleClass()
    result = obj.method()
    print(f"Result: {result}")


# ============================================================================
# EXAMPLE 2: Advanced Usage
# ============================================================================

def example_advanced():
    """Advanced usage with options."""
    from sample_name import SampleClass, Config
    
    config = Config(option1=True, option2=False)
    obj = SampleClass(config)
    result = obj.complex_method()
    print(f"Result: {result}")


# ============================================================================
# EXAMPLE 3: Error Handling
# ============================================================================

def example_error_handling():
    """How to handle errors."""
    from sample_name import SampleClass, CustomError
    
    try:
        obj = SampleClass()
        result = obj.method()
    except CustomError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Run examples
    example_basic()
    example_advanced()
    example_error_handling()
```

---

## Phase 3: Testing (1-2 hours)

### Step 1: Create Test File
**File**: `{sample_name}_test.py`

```python
"""
Tests for {Sample Name}

Run with: pytest {sample_name}_test.py -v
"""

import pytest
from sample_name import SampleClass, CustomError


class TestSampleClass:
    """Test cases for SampleClass."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.obj = SampleClass()
    
    def test_basic_functionality(self):
        """Test basic method functionality."""
        result = self.obj.method()
        assert result is not None
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(CustomError):
            self.obj.method_that_fails()
    
    def test_edge_cases(self):
        """Test edge cases."""
        assert self.obj.method(None) == expected_value
        assert self.obj.method("") == expected_value
    
    def test_performance(self):
        """Test performance metrics."""
        import time
        start = time.time()
        self.obj.method()
        duration = time.time() - start
        assert duration < 1.0  # Should complete in < 1 second


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_object():
    """Provide a sample object for testing."""
    return SampleClass()


@pytest.fixture
def sample_data():
    """Provide test data."""
    return {
        "key1": "value1",
        "key2": "value2"
    }
```

### Step 2: Run Tests
```bash
# Run all tests
pytest {sample_name}_test.py -v

# Check coverage
pytest {sample_name}_test.py --cov

# Run specific test
pytest {sample_name}_test.py::TestClass::test_method -v
```

- [ ] All tests pass
- [ ] Coverage >= 80%
- [ ] No warnings

### Step 3: Code Quality Checks
```bash
# Lint code
pylint {sample_name}.py

# Format code
black {sample_name}.py

# Type check
mypy {sample_name}.py

# Security check
bandit {sample_name}.py
```

- [ ] Pylint score >= 8.0
- [ ] No formatting issues
- [ ] Type checking passes
- [ ] No security issues

---

## Phase 4: Directory Setup (30 minutes)

### Step 1: Create Directory Structure

**For Python Sample**:
```bash
mkdir -p docs/examples/code_samples/python/{category}/
```

**For Complete Project**:
```bash
mkdir -p docs/examples/complete_projects/{project_name}/
mkdir -p docs/examples/complete_projects/{project_name}/{backend,frontend,deployment,docs}
```

### Step 2: Copy Files

```bash
# Copy sample files
cp sample_name.py docs/examples/code_samples/python/category/
cp sample_name_test.py docs/examples/code_samples/python/category/
cp sample_name_example.py docs/examples/code_samples/python/category/
cp sample_name_README.md docs/examples/code_samples/python/category/
cp sample_name.metadata.json docs/examples/code_samples/python/category/

# Verify structure
tree docs/examples/code_samples/python/category/
```

### Step 3: Update Index Files

**Update Master Index**: `docs/examples/INDEX.md`
```markdown
## Python Samples

### [Category Name]
- [Sample Name](./code_samples/python/category/sample_name_README.md) - Description
```

**Update Category Index**: `docs/examples/code_samples/python/PYTHON_INDEX.md`
```markdown
## Python Code Samples

### [Category]
| Sample | Difficulty | Tags | Status |
|--------|-----------|------|--------|
| [Sample Name](./category/sample_name_README.md) | Intermediate | tag1, tag2 | ✅ |
```

---

## Phase 5: Validation (1 hour)

### Pre-Publication Checklist

**Code Quality** ✅
- [ ] Code runs without errors
- [ ] All tests pass (100% pass rate)
- [ ] Code coverage >= 80%
- [ ] Pylint/linter score >= 8.0
- [ ] No type errors
- [ ] No security issues

**Documentation** ✅
- [ ] README is complete and clear
- [ ] All functions have docstrings
- [ ] All classes have docstrings
- [ ] Module has docstring
- [ ] 3+ usage examples provided
- [ ] Prerequisites listed
- [ ] Dependencies listed
- [ ] Performance tips provided

**Usability** ✅
- [ ] Can be used independently
- [ ] Clear use cases
- [ ] Easy to understand
- [ ] Well-organized
- [ ] No external project dependencies

**Testing** ✅
- [ ] Unit tests provided
- [ ] Integration tests provided
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] Performance tested

**Metadata** ✅
- [ ] metadata.json is complete
- [ ] All fields filled accurately
- [ ] Tags are relevant
- [ ] Compatibility matrix included
- [ ] Performance metrics included

**Security** ✅
- [ ] No hardcoded credentials
- [ ] No sensitive data
- [ ] Follows security best practices
- [ ] Input validation present
- [ ] Error messages safe

---

## Phase 6: Integration (1 hour)

### Step 1: Add to Metadata Registry

**File**: `docs/examples/SAMPLES_REGISTRY.json`

```json
{
  "samples": [
    {
      "id": "py_streaming_001",
      "name": "Streaming Response Handler",
      "path": "code_samples/python/streaming/streaming_response.py",
      "language": "python",
      "category": "Backend/Streaming",
      "difficulty": "intermediate",
      "created": "2025-01-15",
      "last_updated": "2025-01-15",
      "status": "production_ready",
      "tags": ["streaming", "async", "production"],
      "rating": 4.8,
      "downloads": 0
    }
  ]
}
```

- [ ] Entry added to registry
- [ ] All fields accurate
- [ ] Tags are relevant
- [ ] Path is correct

### Step 2: Update Search Index

**File**: `docs/examples/SEARCH_INDEX.json`

```json
{
  "indexes": [
    {
      "id": "py_streaming_001",
      "name": "Streaming Response Handler",
      "keywords": ["streaming", "async", "response", "handler", "python"],
      "category": "Backend",
      "language": "Python"
    }
  ]
}
```

- [ ] Search index updated
- [ ] Keywords comprehensive
- [ ] Category correct

### Step 3: Update Related Files

**Update main docs**:
```markdown
## Related Code Samples
See [Code Samples Index](./examples/INDEX.md) for:
- Python: streaming, async, database
- Node.js: middleware, queues, websocket
- React: hooks, state management, streaming
```

**Update agent documentation**:
```markdown
## Recommended Code Samples
For implementing this feature:
1. [Streaming Response Handler](../examples/code_samples/python/...)
2. [Error Handling](../examples/code_samples/python/...)
```

- [ ] Main docs updated
- [ ] Agent docs updated
- [ ] All links working
- [ ] Navigation clear

---

## Phase 7: Commit & Publish (30 minutes)

### Step 1: Create Git Commit

```bash
# Add files
git add docs/examples/code_samples/python/category/
git add docs/examples/INDEX.md
git add docs/examples/SAMPLES_REGISTRY.json

# Create commit message
git commit -m "feat: add streaming response handler sample

- Add complete Python streaming response implementation
- Include comprehensive tests and documentation
- Add usage examples and metadata
- Update index and search registry

Related: #123"
```

- [ ] Commit message is clear
- [ ] All files included
- [ ] References issue

### Step 2: Create GitHub Release

```bash
# Create tag
git tag -a v1.0.0 -m "Release Code Samples Collection v1.0.0"

# Push tag
git push origin v1.0.0
```

- [ ] Tag created
- [ ] Release notes written
- [ ] Downloads available

### Step 3: Publish & Announce

**Announcement Template**:
```markdown
# 📢 New Code Samples Released!

## What's New
- Streaming Response Handler (Python) ✅
- Error Handling Patterns (Python) ✅
- WebSocket Implementation (Node.js) ✅

## Quick Links
- [View Samples](./docs/examples/)
- [Browse by Language](./docs/examples/INDEX.md)
- [Download](./releases)

## Contributing
Want to add your code sample? See CONTRIBUTING.md
```

- [ ] Announcement posted
- [ ] Team notified
- [ ] Links verified

---

## Complete Project Checklist

For adding complete project examples:

### Structure Setup
- [ ] Backend directory with code
- [ ] Frontend directory with code
- [ ] Database schema and migrations
- [ ] Deployment configurations
- [ ] Documentation folder
- [ ] Tests for all components
- [ ] Docker setup
- [ ] Environment examples

### Documentation
- [ ] Comprehensive README
- [ ] Architecture documentation
- [ ] API documentation
- [ ] Database documentation
- [ ] Deployment guide
- [ ] Troubleshooting guide
- [ ] Contributing guide

### Testing
- [ ] Backend unit tests
- [ ] Backend integration tests
- [ ] Frontend component tests
- [ ] E2E tests
- [ ] Performance tests
- [ ] Security tests

### Deployment
- [ ] Docker Compose setup
- [ ] Kubernetes manifests
- [ ] Terraform/IaC
- [ ] CI/CD pipelines
- [ ] Monitoring setup
- [ ] Logging configuration

### Quality Assurance
- [ ] Code review completed
- [ ] Security audit passed
- [ ] Performance tested
- [ ] Deployment tested
- [ ] Documentation complete
- [ ] All tests passing

---

## Sample Submission Form

**To Add a Code Sample**:

```markdown
## Code Sample Submission

### Basic Information
- Sample Name: 
- Language: 
- Category: 
- Difficulty: 

### Code Details
- Total Lines: 
- Dependencies: 
- Requirements: 

### Documentation
- README Complete: [ ]
- Examples Provided: [ ]
- Tests Included: [ ]
- Metadata File: [ ]

### Testing Status
- All Tests Pass: [ ]
- Coverage: [ ]%
- Code Quality: [ ]

### Validation
- Code Review: [ ]
- Security Check: [ ]
- Performance Check: [ ]

### Location
Path where sample will be stored:
```

---

## Troubleshooting

### Issue: Code has external project dependencies
**Solution**: Refactor to remove dependencies or document as "requires project context"

### Issue: Tests are failing
**Solution**: 
1. Run tests locally
2. Check for environment-specific issues
3. Add proper mocks/fixtures
4. Document test requirements

### Issue: Documentation is incomplete
**Solution**:
1. Add all required sections
2. Review README template
3. Ask for feedback
4. Iterate until complete

### Issue: Performance concerns
**Solution**:
1. Profile the code
2. Document performance characteristics
3. Add benchmarks
4. Provide optimization tips

### Issue: Security vulnerabilities
**Solution**:
1. Run security scan (bandit, etc.)
2. Fix identified issues
3. Add secure coding comments
4. Include security considerations

---

## Quick Reference

### Essential Files for Each Sample
```
sample_name.py                    # Main implementation
sample_name_test.py               # Tests
sample_name_example.py            # Usage examples
sample_name_README.md             # Documentation
sample_name.metadata.json         # Metadata
```

### Directory Structure
```
docs/examples/
├── complete_projects/            # Full project examples
└── code_samples/                 # Reusable code snippets
    ├── python/                   # By language
    ├── nodejs/
    ├── react/
    ├── mobile/
    └── desktop/
```

### Tools to Use
- **Testing**: pytest (Python), Jest (JS)
- **Linting**: pylint (Python), ESLint (JS)
- **Formatting**: black (Python), prettier (JS)
- **Type Checking**: mypy (Python), TypeScript
- **Security**: bandit (Python), snyk (all)

---

## Timeline Estimates

| Phase | Duration | Effort |
|-------|----------|--------|
| Code Extraction | 1-2 hours | Low |
| Documentation | 1-2 hours | Medium |
| Testing | 1-2 hours | Medium |
| Directory Setup | 30 min | Low |
| Validation | 1 hour | Medium |
| Integration | 1 hour | Low |
| Commit & Publish | 30 min | Low |
| **TOTAL** | **6-9 hours** | **Medium** |

---

## Next Steps

1. **Select Code**: Choose code from completed projects
2. **Prepare**: Clean and document
3. **Test**: Ensure tests pass
4. **Validate**: Run all checks
5. **Integrate**: Add to repository
6. **Publish**: Release and announce
7. **Maintain**: Keep up-to-date

---

**Version**: 1.0  
**Last Updated**: 2025-01-15  
**Created**: Development Team
