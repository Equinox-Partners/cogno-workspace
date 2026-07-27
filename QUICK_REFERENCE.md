# Quick Reference Guide

## Working with Cogno Workspace

This is a quick reference for common tasks when working with the Equinox Partners Cogno Workspace.

## Git Workflow

### Creating a Task Branch

```bash
# Fetch latest from origin
git fetch origin

# Create a new task branch
git checkout -b task-<ID> origin/main

# Or checkout a worktree
git worktree add .cogno/agents/task-<ID> origin/main
```

### Making Changes

```bash
# Stage changes
git add <file>

# Commit changes
git commit -m "Brief description of changes"

# Push to origin
git push origin task-<ID>
```

### Creating a Pull Request

1. Go to [GitHub Repository](https://github.com/Equinox-Partners/cogno-workspace)
2. Click "New Pull Request"
3. Select your branch as the source
4. Fill in PR title and description
5. Request reviewers if needed
6. Submit PR

### Merging a PR

After approval:
1. Go to PR page
2. Click "Merge pull request"
3. Confirm merge
4. Delete branch after merge

## Worktree Management

### Create a Worktree

```bash
git worktree add .cogno/agents/task-<ID> origin/main
```

### List Worktrees

```bash
git worktree list
```

### Remove a Worktree

```bash
git worktree remove .cogno/agents/task-<ID>
```

## CI/CD Pipeline

### Check Workflow Status

1. Go to [Actions Tab](https://github.com/Equinox-Partners/cogno-workspace/actions)
2. Select the workflow
3. View the latest run status

### Common Workflow Files

- ``.github/workflows/ci.yml`` - CI pipeline (YAML/Markdown validation)
- ``.github/workflows/cd.yml`` - CD pipeline (Documentation deployment)

### Required Files for CI/CD Success

- `CI_CD_GUIDE.md` - This guide
- `QUICK_REFERENCE.md` - Quick reference (this file)

Both files must exist in the repository root.

## Branch Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Task | `task-<ID>` | `task-3672` |
| Feature | `feature/<name>` | `feature/auth` |
| Bugfix | `fix/<name>` | `fix/login-bug` |
| Release | `release/<version>` | `release/1.0.0` |

## Repository Structure

```
cogno-workspace/
├── CLAUDE.md                    # Worker instructions
├── CI_CD_GUIDE.md              # CI/CD documentation (this project)
├── QUICK_REFERENCE.md          # Quick reference (this file)
├── .cogno/
│   ├── .gitignore
│   ├── app-context.md          # Integration settings
│   ├── repo.json               # Repository configuration
│   ├── agents/                 # Worktree locations
│   │   ├── task-3408/
│   │   ├── task-3560/
│   │   └── task-3672/
│   └── visual/                 # Visual assets
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI pipeline configuration
│       └── cd.yml              # CD pipeline configuration
└── [Other project files]
```

## Common Commands

### Viewing Recent Commits

```bash
# Show last 5 commits
git log --oneline -5

# Show commits on current branch
git log --oneline origin/main..HEAD

# Show specific commit details
git show <commit-hash>
```

### Checking Repository Status

```bash
# Show working tree status
git status

# Show staged changes
git diff --cached

# Show unstaged changes
git diff

# Show branch status
git branch -v
```

### Syncing with Remote

```bash
# Fetch latest changes
git fetch origin

# Fast-forward current branch
git pull origin

# Fast-forward specific branch
git pull origin main
```

## Troubleshooting

### Merge Conflicts

1. Identify conflicting files: `git status`
2. Edit files to resolve conflicts
3. Mark as resolved: `git add <file>`
4. Complete merge: `git commit`

### Detached HEAD

```bash
# Recover with new branch
git checkout -b recover-branch

# Or switch to existing branch
git checkout main
```

### Undo Recent Changes

```bash
# Undo unstaged changes
git checkout <file>

# Undo staged changes
git reset HEAD <file>

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

## Integration Services

### GitHub Integration
- **Status**: ✅ Active
- **Purpose**: Repository management, PR/Issue tracking, Actions workflows

### Notion Integration
- **Status**: ✅ Active
- **Purpose**: Task management, Meeting notes

### Claude API Integration
- **Status**: ✅ Active
- **Purpose**: AI processing, Automation

## Useful Links

- [GitHub Repository](https://github.com/Equinox-Partners/cogno-workspace)
- [GitHub Actions](https://github.com/Equinox-Partners/cogno-workspace/actions)
- [Repository Settings](https://github.com/Equinox-Partners/cogno-workspace/settings)
- [CI/CD Guide](CI_CD_GUIDE.md)
- [Project Instructions](CLAUDE.md)

## Contact & Support

For questions or issues:
1. Check the [CI/CD Guide](CI_CD_GUIDE.md)
2. Review [project instructions](CLAUDE.md)
3. Check recent commit messages
4. Review GitHub Actions logs

---

**Quick Version**: 2.0
**Last Updated**: 2026-07-27
