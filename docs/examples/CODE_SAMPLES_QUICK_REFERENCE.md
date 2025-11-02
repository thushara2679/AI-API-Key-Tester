# Code Samples & Examples - Quick Reference Guide

## 📌 TL;DR - The Process

**Adding a code sample to your repository takes 5-9 hours following this simple process:**

```
Code Selection (0.5h) → Cleanup (1h) → Document (1.5h) → Test (1h) → Integrate (1h)
```

---

## 🎯 Phase-by-Phase Overview

### Phase 1: Code Extraction & Preparation (1-2 hours)

**What to do:**
1. Find production-tested code that solves a common problem
2. Remove project-specific imports and hardcoded values  
3. Add comprehensive comments and type hints
4. Create metadata file (JSON)

**Files to create:**
- `{sample_name}.py` (clean, reusable code)
- `{sample_name}.metadata.json` (metadata file)

**Questions to answer:**
- [ ] Does this solve a common problem?
- [ ] Is it production-tested?
- [ ] Can it work independently?
- [ ] Is it 50-500 lines?

---

### Phase 2: Documentation (1-2 hours)

**What to do:**
1. Write comprehensive README
2. Add docstrings to all functions/classes
3. Create 3-5 usage examples
4. Document API and error handling

**Files to create:**
- `{sample_name}_README.md` (complete documentation)
- `{sample_name}_example.py` (working examples)

**README sections:**
- Overview
- Key Features
- When to Use / When NOT to Use
- Installation
- Usage Examples (3-5)
- API Reference
- Error Handling
- Performance Tips
- Compatibility Matrix

---

### Phase 3: Testing & Validation (1-2 hours)

**What to do:**
1. Create comprehensive test file
2. Ensure 80%+ code coverage
3. Run quality checks (pylint, black, mypy, bandit)
4. Verify no hardcoded secrets

**Files to create:**
- `{sample_name}_test.py` (unit & integration tests)

**Tests to include:**
- Unit tests (basic functionality)
- Integration tests
- Edge case tests
- Error handling tests
- Performance tests

**Quality checks:**
```bash
pytest {sample_name}_test.py -v --cov
pylint {sample_name}.py
black {sample_name}.py
mypy {sample_name}.py
bandit {sample_name}.py
```

---

### Phase 4: Integration (1 hour)

**What to do:**
1. Create directory structure
2. Copy all files
3. Update index files
4. Add to metadata registry

**Directory structure:**
```
docs/examples/code_samples/{language}/{category}/
├── {sample_name}.py
├── {sample_name}_README.md
├── {sample_name}_test.py
├── {sample_name}_example.py
└── {sample_name}.metadata.json
```

**Files to update:**
- `docs/examples/INDEX.md` (add to index)
- `docs/examples/SAMPLES_REGISTRY.json` (add metadata entry)
- `docs/examples/SEARCH_INDEX.json` (add search keywords)

---

## 📂 Directory Structure Template

```
docs/examples/
├── complete_projects/                    # Full project examples
│   ├── ai_chat_application/
│   │   ├── README.md
│   │   ├── backend/
│   │   ├── frontend/
│   │   ├── deployment/
│   │   └── docs/
│   └── ...
│
└── code_samples/                         # Reusable code snippets
    ├── python/
    │   ├── backend/
    │   ├── streaming/
    │   ├── database/
    │   └── utilities/
    ├── nodejs/
    ├── react/
    ├── mobile/
    └── desktop/
```

---

## ✅ Quality Checklist

**Before publishing, verify ALL items:**

### Code Quality
- [ ] Code runs without errors
- [ ] All tests pass (100%)
- [ ] Code coverage >= 80%
- [ ] Pylint score >= 8.0
- [ ] No type errors
- [ ] No security vulnerabilities

### Documentation
- [ ] README complete (all sections)
- [ ] All functions documented
- [ ] 3+ usage examples
- [ ] Prerequisites listed
- [ ] Dependencies listed
- [ ] Performance tips included

### Files Required
- [ ] `{sample_name}.py` (main code)
- [ ] `{sample_name}_README.md` (documentation)
- [ ] `{sample_name}_test.py` (tests)
- [ ] `{sample_name}_example.py` (examples)
- [ ] `{sample_name}.metadata.json` (metadata)

### Security
- [ ] No hardcoded credentials
- [ ] No sensitive data
- [ ] Input validation present
- [ ] Error messages safe

---

## 📄 Sample File Templates

### 1. metadata.json Template
```json
{
  "name": "Sample Name",
  "filename": "sample_name.py",
  "language": "Python",
  "category": "Backend/Feature",
  "difficulty": "intermediate",
  "lines_of_code": 150,
  "description": "What this code does",
  "use_cases": ["Use case 1", "Use case 2"],
  "prerequisites": ["Python 3.8+"],
  "dependencies": ["dependency1"],
  "tags": ["tag1", "tag2"],
  "status": "production_ready"
}
```

### 2. README Sections
```markdown
# Sample Name

## Overview
Brief explanation

## Key Features
- Feature 1
- Feature 2

## Installation
pip install dependency

## Usage
Basic and advanced examples

## API Reference
Classes, functions, parameters

## Error Handling
Common errors and solutions

## Performance
Tips and metrics
```

### 3. Test File Structure
```python
class TestSampleClass:
    def test_basic_functionality(self):
        # Basic test
        pass
    
    def test_error_handling(self):
        # Error test
        pass
    
    def test_edge_cases(self):
        # Edge case test
        pass
```

### 4. Example File Structure
```python
# EXAMPLE 1: Basic Usage
def example_basic():
    pass

# EXAMPLE 2: Advanced Usage
def example_advanced():
    pass

# EXAMPLE 3: Error Handling
def example_error_handling():
    pass
```

---

## 🔍 Metadata Registry Entry

Add to `SAMPLES_REGISTRY.json`:

```json
{
  "id": "py_sample_001",
  "name": "Sample Name",
  "path": "code_samples/python/category/sample_name.py",
  "language": "python",
  "category": "Backend",
  "difficulty": "intermediate",
  "created": "2025-01-15",
  "status": "production_ready",
  "tags": ["tag1", "tag2"]
}
```

---

## 🔗 Index Updates

### Update `INDEX.md`:
```markdown
## Python Samples

### Backend
- [Sample Name](./code_samples/python/backend/sample_name_README.md) - Description
```

### Update `SEARCH_INDEX.json`:
```json
{
  "id": "py_sample_001",
  "name": "Sample Name",
  "keywords": ["keyword1", "keyword2"],
  "language": "Python"
}
```

---

## ⏱️ Time Breakdown

| Task | Time |
|------|------|
| Code Selection & Prep | 1-2 hours |
| Documentation | 1-2 hours |
| Testing & Validation | 1-2 hours |
| Directory Setup & Integration | 1 hour |
| **TOTAL** | **5-9 hours** |

---

## 📋 Step-by-Step Checklist

### Step 1: Preparation (30 min)
- [ ] Select code from completed project
- [ ] Verify it's production-tested
- [ ] Confirm it solves a common problem
- [ ] Check it can work independently

### Step 2: Cleanup (1 hour)
- [ ] Remove project-specific imports
- [ ] Replace hardcoded values with parameters
- [ ] Add type hints
- [ ] Add comprehensive comments
- [ ] Add error handling

### Step 3: Documentation (1.5 hours)
- [ ] Write README.md (all sections)
- [ ] Add docstrings (module, class, function)
- [ ] Create examples file (3-5 examples)
- [ ] Create metadata.json file

### Step 4: Testing (1 hour)
- [ ] Create test file
- [ ] Run all tests (100% pass)
- [ ] Check code quality (pylint >= 8.0)
- [ ] Check coverage (>= 80%)
- [ ] Security scan (no issues)

### Step 5: Integration (1 hour)
- [ ] Create directory structure
- [ ] Copy all files
- [ ] Update INDEX.md
- [ ] Update SAMPLES_REGISTRY.json
- [ ] Update SEARCH_INDEX.json

### Step 6: Publication (30 min)
- [ ] Create git commit
- [ ] Push to repository
- [ ] Announce to team
- [ ] Share links

---

## 🎯 Complete Project Process

For full projects, use the same 4 phases but with additional structure:

```
docs/examples/complete_projects/{project_name}/
├── README.md (project overview)
├── requirements.md (business requirements)
├── architecture.md (system design)
├── implementation_guide.md (step-by-step)
├── backend/ (backend code)
├── frontend/ (frontend code)
├── deployment/ (deployment configs)
├── database/ (schema, migrations)
└── docs/ (API, database, troubleshooting)
```

**Timeline**: 14-24 hours (1-3 days) for complete project

---

## 📌 Key Best Practices

1. **Keep it focused** - One responsibility per sample
2. **Document everything** - Make it easy to understand
3. **Include examples** - Show real use cases
4. **Error handling** - Handle edge cases
5. **Performance tips** - Discuss trade-offs
6. **Tests** - Comprehensive test suite
7. **Comments** - Explain complex logic
8. **Security** - No hardcoded secrets
9. **Maintenance** - Keep up-to-date
10. **Community** - Listen to feedback

---

## 🚀 Quick Start (Your First Sample)

1. **Day 1 (3 hours)**
   - Identify code (30 min)
   - Cleanup code (1 hour)
   - Document code (1.5 hours)

2. **Day 2 (2-3 hours)**
   - Write tests (1 hour)
   - Run quality checks (30 min)
   - Integrate into repo (30-60 min)

3. **Day 3 (30 min)**
   - Final validation
   - Publish
   - Announce

---

## 📞 Getting Help

- **Full guide**: See `CODE_SAMPLES_EXAMPLES_GUIDE.md`
- **Detailed checklist**: See `CODE_SAMPLES_IMPLEMENTATION_CHECKLIST.md`
- **Questions**: Check troubleshooting sections in full guide

---

## 📚 All Required Files

For **each code sample**, create these 5 files:

```
1. {sample_name}.py                    # Main implementation
2. {sample_name}_README.md             # Documentation
3. {sample_name}_test.py               # Tests
4. {sample_name}_example.py            # Usage examples
5. {sample_name}.metadata.json         # Metadata
```

---

## 🔗 Links to Guides

- **Comprehensive Guide**: `CODE_SAMPLES_EXAMPLES_GUIDE.md`
- **Implementation Checklist**: `CODE_SAMPLES_IMPLEMENTATION_CHECKLIST.md`
- **This Quick Reference**: `CODE_SAMPLES_QUICK_REFERENCE.md`

---

**Status**: ✅ Ready to Use  
**Version**: 1.0  
**Last Updated**: 2025-01-15

Use these guides to add production-quality code samples and examples to your repository! 🎉
