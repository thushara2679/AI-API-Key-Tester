# Git Workflow Best Practices

## Overview

This guide establishes standardized Git workflow practices for the Advanced AI Agent System development team. It ensures consistent code management, effective collaboration, and maintainable repository history.

---

## 1. Repository Structure

### 1.1 Branch Organization

```
main/master
├── Production code
├── Tags for releases
└── Protected branch (requires PR, all tests pass)

develop
├── Integration branch
├── Pre-release code
└── Staging environment deploys

feature/
├── feature/PROJ-123-user-authentication
├── feature/PROJ-456-data-pipeline
└── feature/[ISSUE-NUMBER]-[DESCRIPTION]

bugfix/
├── bugfix/PROJ-789-memory-leak
└── bugfix/[ISSUE-NUMBER]-[DESCRIPTION]

hotfix/
├── hotfix/PROD-001-critical-crash
└── hotfix/[ISSUE-NUMBER]-[CRITICAL-DESC]

release/
├── release/v1.0.0
└── release/v[VERSION]

experiment/
├── experiment/new-algorithm
└── experiment/[DESCRIPTION]
```

### 1.2 Branch Naming Convention

**Format:** `[type]/[ISSUE-ID]-[description]`

**Types:**
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `release/` - Release preparation
- `experiment/` - Experimental work
- `docs/` - Documentation only
- `refactor/` - Code refactoring
- `perf/` - Performance improvements

**Examples:**
```
✅ GOOD
- feature/PROJ-123-user-authentication
- bugfix/PROJ-456-fix-null-pointer-exception
- hotfix/CRITICAL-001-database-connection-pool
- docs/PROJ-789-api-documentation
- refactor/PROJ-234-extract-shared-logic

❌ BAD
- feature123
- fix-something
- mywork
- test
- wip
- john-changes
```

---

## 2. Commit Best Practices

### 2.1 Commit Message Format

**Format:** `[TYPE] [ISSUE-ID] - [Description]`

**Types:**
- `FEAT` - New feature
- `FIX` - Bug fix
- `REFACTOR` - Code refactoring
- `PERF` - Performance improvement
- `TEST` - Test changes
- `DOCS` - Documentation
- `STYLE` - Code style/formatting
- `CHORE` - Maintenance tasks
- `CI` - CI/CD configuration
- `HOTFIX` - Critical production fix

**Format Details:**
```
[TYPE] [ISSUE-ID] - [Brief description (50 chars max)]

[Optional detailed explanation if needed]
- Bullet point 1
- Bullet point 2
- Bullet point 3

[Optional footer]
Closes #123
Relates to #456
BREAKING CHANGE: description
```

### 2.2 Commit Message Examples

**Good Examples:**
```
FEAT PROJ-123 - Add user authentication service

- Implement JWT token generation
- Add login endpoint with rate limiting
- Add password hashing with bcrypt
- Add session management

Closes #123
Relates to PROJ-124, PROJ-125
```

```
FIX PROJ-456 - Fix null pointer exception in data processor

The processor was not validating input data before processing,
causing crashes when null values were passed.

- Add input validation at service entry point
- Add unit tests for null input scenarios
- Update error message to be more descriptive

Closes #456
```

```
REFACTOR PROJ-789 - Extract common validation logic

- Create ValidationService singleton
- Replace duplicate validation code with service calls
- Improve error handling consistency

No functional changes, improves maintainability.
```

**Poor Examples:**
```
❌ "fix stuff"
❌ "update code"
❌ "asdf"
❌ "work in progress"
❌ "WIP: don't merge yet"
```

### 2.3 Commit Size Guidelines

**Ideal Commit Size:**
- One logical change per commit
- Between 50-300 lines changed
- Related files grouped together
- Can be described in one sentence

**What to Include:**
```
✅ Closely related changes
✅ Complete feature or fix
✅ Tests for the changes
✅ Documentation updates
✅ Config changes if related
```

**What NOT to Include:**
```
❌ Unrelated bug fixes
❌ Partial features
❌ Formatting changes in unrelated files
❌ Debugging code
❌ Commented-out code
```

### 2.4 Commit Frequency

**Best Practice:**
- Commit frequently (every 15-30 minutes)
- One logical change per commit
- Never go more than 1 hour without committing
- Before taking breaks or switching tasks
- Before pulling latest changes

**Example Commit Sequence:**
```
1. [FEAT] Create user service
2. [TEST] Add unit tests for user service
3. [FEAT] Add authentication middleware
4. [DOCS] Update API documentation
5. [REFACTOR] Extract validation logic
```

---

## 3. Pull Request Process

### 3.1 Creating Pull Requests

**Before Creating PR:**
- [ ] Branch is up-to-date with base branch
- [ ] All tests pass locally
- [ ] Code is linted and formatted
- [ ] No debug code or console.log statements
- [ ] Commit messages are clear
- [ ] Changes are logically grouped

**PR Naming:**
```
Format: [TYPE] [ISSUE-ID] - [Description]

Examples:
- FEAT PROJ-123 - Add user authentication service
- FIX PROJ-456 - Fix memory leak in cache
- REFACTOR PROJ-789 - Extract validation logic
```

### 3.2 PR Description Template

```markdown
## Description
Brief summary of the changes.

## Related Issues
Fixes #123
Relates to #456

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Changes Made
- Item 1
- Item 2
- Item 3

## How Has This Been Tested?
Describe the test process:
- [ ] Unit tests added
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases tested

## Checklist
- [ ] Code follows style guide
- [ ] Self-review completed
- [ ] Comments added for complex areas
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No breaking changes (or documented)

## Performance Impact
- [ ] No performance impact
- [ ] Improved performance
- [ ] Potential performance impact (details below)

Performance analysis:
- Details here

## Screenshots (if applicable)
Include screenshots for UI changes.

## Additional Notes
Any other relevant information.
```

### 3.3 PR Review Workflow

```
Feature Branch Created
        ↓
Local Development & Testing
        ↓
Push to Remote
        ↓
Create Pull Request
        ↓
Code Review
        ├─→ Request Changes? ──→ Update PR ──→ Re-review
        ├─→ Approve
        └─→ Comment (non-blocking)
        ↓
All Checks Pass
        ↓
Approval from 1-2 Reviewers
        ↓
Merge to Base Branch
        ↓
Delete Feature Branch
        ↓
Deploy (automated or manual)
```

---

## 4. Code Review Standards

### 4.1 Review Process

**Reviewer Responsibilities:**
- [ ] Review code within 24 hours
- [ ] Check functionality and logic
- [ ] Verify security implications
- [ ] Ensure tests are adequate
- [ ] Check documentation
- [ ] Verify performance impact

**Required Approvals:**
- Minimum 1 approval for bugfixes
- Minimum 2 approvals for features
- Minimum 1 approval for documentation
- Architecture review for major changes
- Security review for security-related changes

### 4.2 Review Timeline

| Change Type | Review Time | Approvals |
|------------|-------------|-----------|
| Bugfix | 2-4 hours | 1 |
| Feature | 4-8 hours | 2 |
| Hotfix | Immediate | 1 |
| Refactor | 24 hours | 1-2 |
| Documentation | 24 hours | 1 |
| Release | 24 hours | 2 |

### 4.3 Addressing Review Comments

**When Reviewer Requests Changes:**

1. Create a new commit for each change
2. Don't force push (preserves review history)
3. Reply to each review comment
4. Re-request review when done
5. Be respectful and collaborative

**Example Response:**
```
"Good catch! I've added the validation check in commit abc1234.
This handles the edge case you mentioned."
```

---

## 5. Merging and Integration

### 5.1 Merge Strategy

**Preferred Strategy:** Squash and Merge for feature branches

```
Before Merge:
  Feature Branch: commit1, commit2, commit3, commit4, commit5

After Squash:
  Main Branch: single commit with all changes
```

**When to Squash:**
- Feature branches with multiple commits
- Cleanup commits (formatting, fixes)
- WIP commits during development

**When to Keep History:**
- Release branches
- Important milestone commits
- Complex multi-part features

### 5.2 Merge Checklist

Before merging, verify:
- [ ] All tests pass
- [ ] All reviews approved
- [ ] CI/CD pipeline succeeds
- [ ] No merge conflicts (or resolved cleanly)
- [ ] Branch is up-to-date with base
- [ ] Performance impact assessed
- [ ] Security review passed (if needed)
- [ ] Documentation updated
- [ ] Changelog updated (if needed)

### 5.3 Conflict Resolution

**Preventing Conflicts:**
- Keep branches short-lived (< 1 week)
- Sync frequently with main branch
- Communicate about shared files
- Review main branch changes regularly

**Resolving Conflicts:**

1. Fetch latest from main
```bash
git fetch origin main
```

2. Rebase on main
```bash
git rebase origin/main
```

3. Fix conflicts in editor
```
<<<<<<< HEAD
Your change
=======
Other change
>>>>>>> origin/main
```

4. Keep correct version, remove markers
5. Stage and continue
```bash
git add .
git rebase --continue
```

6. Force push to feature branch
```bash
git push --force-with-lease origin feature-branch
```

---

## 6. Branching Patterns

### 6.1 Git Flow Pattern

```
main ───────┬─────────────────────
            │ (tagged v1.0.0)
            │
develop ────┼───────────┬─────────
            │           │
feature ────┼──────┐    └──┬────┐
            │      │       │    │
            └─────merge───merge─┘
                   │
release ──────────merge────────
                   │
                   └─ Hotfix
```

### 6.2 GitHub Flow Pattern

```
main ──────┬──────┬──────┬──────
           │      │      │
feature ───┼─merge┤─merge┤─merge
           │      │      │
develop ───┴──────┴──────┴──────
```

### 6.3 Trunk-Based Development

```
main ──┬─┬─┬─┬─┬─ (rapid, small merges)
       │ │ │ │ │
feat1  ┤ │ │ │ │
feat2  ├─┤ │ │ │
feat3  ├─┼─┤ │ │
feat4  ├─┼─┼─┤ │
feat5  ├─┼─┼─┼─┤
```

---

## 7. Tag Management

### 7.1 Version Tags

**Format:** Semantic Versioning `v[MAJOR].[MINOR].[PATCH]`

```
v1.0.0    - Initial release
v1.0.1    - Patch (bug fixes)
v1.1.0    - Minor (new features)
v2.0.0    - Major (breaking changes)
v1.0.0-rc.1    - Release candidate
v1.0.0-beta.1  - Beta release
```

### 7.2 Creating Tags

**Annotated Tag (Recommended):**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

**Lightweight Tag:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

### 7.3 Release Workflow

```
Feature Development (develop)
        ↓
Release Branch Created (release/v1.0.0)
        ↓
Final Testing & Bugfixes
        ↓
Merge to Main & Tag (v1.0.0)
        ↓
Merge Back to Develop
        ↓
Delete Release Branch
```

---

## 8. Rebasing and History

### 8.1 Rebasing Guidelines

**Interactive Rebase (Local Only):**
```bash
# Rebase last 3 commits
git rebase -i HEAD~3

# Options in editor:
# pick - use commit
# reword - use commit, but edit message
# squash - use commit, but meld with previous
# fixup - like squash, but discard commit message
# drop - remove commit
```

**Rebase vs Merge:**

| Operation | Use Case |
|-----------|----------|
| Rebase | Local branches, keep linear history |
| Merge | Shared branches, preserve history |
| Squash | Feature branches before merge |

### 8.2 Rewriting History Rules

```
✅ OK to Rewrite:
- Local commits not yet pushed
- Force push with --force-with-lease
- Brief feature branches

❌ Never Rewrite:
- Shared/main branches
- Published commits
- Release tags
```

---

## 9. Stashing and Temporary Changes

### 9.1 Stash Usage

**Save work temporarily:**
```bash
# Stash with message
git stash save "Working on feature X"

# Apply stash
git stash apply

# Apply and remove
git stash pop

# List stashes
git stash list

# Clear stashes
git stash clear
```

**Good Uses:**
- Quick switch to fix a bug
- Temporary storage during development
- Clean up before pull/rebase

---

## 10. Synchronization

### 10.1 Keeping Branches Updated

**Before Starting Work:**
```bash
git checkout main
git pull origin main
git checkout feature-branch
git rebase origin/main
```

**During Development:**
```bash
# Daily sync
git fetch origin
git rebase origin/main

# Or merge if preferred
git merge origin/main
```

**After Branch Update:**
```bash
git pull origin main
git rebase origin/main
git push --force-with-lease origin feature-branch
```

### 10.2 Remote Tracking

```bash
# Set tracking branch
git branch -u origin/feature-branch

# Push with tracking
git push -u origin feature-branch

# List tracking branches
git branch -vv
```

---

## 11. Troubleshooting Common Issues

### 11.1 Accidental Commits

**Undo Last Commit (Keep Changes):**
```bash
git reset HEAD~1
```

**Undo Last Commit (Discard Changes):**
```bash
git reset --hard HEAD~1
```

**Undo Published Commit:**
```bash
git revert HEAD
```

### 11.2 Lost Commits

**Find Lost Commits:**
```bash
git reflog
git checkout <commit-hash>
```

**Recover Lost Branch:**
```bash
git reflog
git checkout -b recovered-branch <commit-hash>
```

### 11.3 Wrong Branch

**Move Commit to Different Branch:**
```bash
# On wrong branch
git log --oneline (note commit hash)
git reset HEAD~1

# Switch to correct branch
git checkout correct-branch
git cherry-pick <commit-hash>
```

### 11.4 Merge Conflicts

**View Conflicts:**
```bash
git status
```

**Abort Merge:**
```bash
git merge --abort
```

**Use Specific Version:**
```bash
git checkout --ours file.txt    # Our version
git checkout --theirs file.txt  # Their version
```

---

## 12. Repository Maintenance

### 12.1 Cleanup

**Delete Local Branches:**
```bash
# Delete merged branches
git branch -d branch-name

# Delete all local branches except main/develop
git branch | grep -v "main\|develop" | xargs git branch -d
```

**Delete Remote Branches:**
```bash
git push origin --delete branch-name
```

**Prune Remote Branches:**
```bash
git remote prune origin
git fetch --prune
```

### 12.2 Repository Health

**Check Repository Size:**
```bash
du -sh .git/
git count-objects -v
```

**Optimize Repository:**
```bash
git gc --aggressive
```

**Clean Large Files:**
```bash
# Find large files
git rev-list --all --objects | sed -n $(git rev-list --objects --all | cut -f1 | sort -u | while read hash; do du -b "$(git cat-file -p $hash | head -1)"; done | sort -rn | head -10 | while read bytes hash; do echo -n "-e s/$hash/$bytes /"; done) | head
```

---

## 13. Team Policies

### 13.1 Required Checks

Before Merge, Ensure:
- [ ] All tests pass
- [ ] Linting passes
- [ ] Build succeeds
- [ ] Code review approved
- [ ] Security scan passed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

### 13.2 Branch Protection Rules

**Main/Develop Branches:**
- Require status checks to pass
- Require code reviews (1-2 approvals)
- Require branches to be up-to-date
- Dismiss stale pull request approvals
- Require conversation resolution
- Restrict who can push to branch

**Configuration:**
```
Repository Settings → Branches → Branch Protection Rules
```

### 13.3 CI/CD Integration

**Automated Checks:**
- [ ] Unit tests run
- [ ] Integration tests run
- [ ] Linting checks
- [ ] Security scanning
- [ ] Build verification
- [ ] Performance benchmarks
- [ ] Dependency checks

---

## 14. Best Practices Summary

### Daily Workflow
1. Pull latest changes
2. Create feature branch
3. Make changes with clear commits
4. Push branch frequently
5. Create PR when ready
6. Address review comments
7. Merge when approved
8. Delete branch after merge

### Commit Discipline
- Commit frequently (every 15-30 min)
- Write clear messages
- Keep commits focused
- Test before committing
- Never commit broken code
- Never commit secrets

### Collaboration
- Keep branches short-lived (< 1 week)
- Communicate about work
- Review promptly
- Be respectful in reviews
- Help others with conflicts
- Share knowledge

### History Cleanliness
- Squash trivial commits
- Keep linear history when possible
- Use meaningful branch names
- Tag releases
- Clean up old branches
- Maintain readable log

---

## 15. Common Commands Reference

```bash
# Branching
git branch                          # List local branches
git branch -a                       # List all branches
git branch -d feature-name          # Delete branch
git checkout -b feature-name        # Create and switch branch
git switch feature-name             # Switch branch (newer syntax)

# Committing
git add .                           # Stage all changes
git commit -m "message"             # Commit staged changes
git commit --amend                  # Modify last commit
git commit --amend --no-edit        # Add to last commit

# Pulling/Pushing
git pull origin develop             # Pull latest changes
git push origin feature-name        # Push branch
git push --force-with-lease         # Force push safely
git fetch origin                    # Fetch remote changes

# Rebasing
git rebase origin/main              # Rebase on main
git rebase -i HEAD~3                # Interactive rebase
git rebase --abort                  # Cancel rebase

# History
git log --oneline                   # Concise commit history
git log --graph --all --decorate    # Visual history
git log -p                          # Show changes
git show commit-hash                # Show specific commit
git diff branch1 branch2            # Compare branches

# Stashing
git stash                           # Stash changes
git stash list                      # List stashes
git stash pop                       # Apply and remove stash
git stash drop                      # Delete stash

# Tags
git tag v1.0.0                      # Create tag
git push origin v1.0.0              # Push tag
git tag -d v1.0.0                   # Delete tag
```

---

## 16. Git Configuration

### 16.1 Setup

```bash
# Global configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "vim"

# Project-specific
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 16.2 Useful Aliases

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.log-pretty "log --graph --all --decorate --oneline"
git config --global alias.sync "!git fetch origin && git rebase origin/main"
```

---

## Conclusion

This Git workflow establishes clear practices for effective team collaboration. Following these guidelines ensures:
- Clean, readable repository history
- Efficient code review process
- Easy collaboration and knowledge sharing
- Quick problem resolution
- Professional development practices

**Remember:** Good Git practices are an investment in team productivity and code quality! 🚀

