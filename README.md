# Equinox Partners Cogno Workspace

A collaborative workspace for Cogno Workers to manage and execute distributed tasks using GitHub, Notion, and Claude AI integration.

## Overview

The Cogno Workspace is a centralized repository that enables multiple workers to collaborate efficiently by:
- Managing tasks through GitHub issues and PRs
- Tracking work progress with Notion integration
- Automating workflows with GitHub Actions CI/CD
- Leveraging Claude AI for intelligent task processing

## Features

### 🤖 AI-Powered Automation
- Claude AI integration for intelligent task processing
- Automatic workflow optimization
- Smart PR analysis and code review

### 📋 Task Management
- GitHub Issues for task tracking
- Task-based branch naming (`task-<ID>`)
- Automated PR workflow
- Notion integration for task planning

### 🚀 CI/CD Pipeline
- Automated validation of code and documentation
- Continuous deployment to production
- Workflow monitoring and reporting
- Pre-deployment verification

### 👥 Multi-Worker Collaboration
- Parallel task execution
- Isolated worktrees per task
- Atomic PR reviews
- Concurrent branch management

### 🔒 Enterprise Security
- Branch protection rules
- Required status checks
- Code ownership enforcement
- Secret management

## Quick Start

### Prerequisites
- Git 2.38+
- GitHub account with appropriate permissions
- Claude Code / Claude API access
- Notion account (optional, for task integration)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Equinox-Partners/cogno-workspace.git
   cd cogno-workspace
   ```

2. **Create a task branch**
   ```bash
   git checkout -b task-<ID> origin/main
   ```

3. **Or use a worktree**
   ```bash
   git worktree add .cogno/agents/task-<ID> origin/main
   cd .cogno/agents/task-<ID>
   ```

4. **Make your changes**
   ```bash
   # Create or modify files
   git add .
   git commit -m "Brief description of changes"
   ```

5. **Push and create PR**
   ```bash
   git push origin task-<ID>
   # Create PR on GitHub
   ```

## Project Structure

```
cogno-workspace/
├── README.md                  # This file
├── CLAUDE.md                  # Worker instructions
├── CI_CD_GUIDE.md            # CI/CD pipeline documentation
├── QUICK_REFERENCE.md        # Quick reference for common tasks
├── .gitignore                # Git ignore rules
├── .gitattributes            # Git attributes
├── .cogno/
│   ├── .gitignore            # Cogno directory ignore rules
│   ├── app-context.md        # Integration settings and context
│   ├── repo.json             # Repository configuration
│   ├── agents/               # Worktree locations
│   │   ├── task-3408/        # Example task worktree
│   │   ├── task-3560/        # Example task worktree
│   │   ├── task-3609/        # Example task worktree
│   │   └── task-<ID>/        # New task worktrees
│   └── visual/               # Visual assets and captures
└── .github/
    ├── CODEOWNERS            # Code ownership rules
    ├── pull_request_template.md  # PR template
    ├── issue_template/       # Issue templates
    │   ├── bug_report.md
    │   ├── feature_request.md
    │   ├── documentation.md
    │   └── config.yml
    └── workflows/            # GitHub Actions workflows
        ├── ci.yml            # CI pipeline
        └── cd.yml            # CD pipeline
```

## Integration Services

### GitHub
- **Purpose**: Repository management, version control, automation
- **Features**: Workflows, API access, branch management
- **Authentication**: OAuth + SSH/HTTPS

### Notion
- **Purpose**: Task management, meeting notes
- **Features**: Database access, template processing
- **Status**: MCP Integration

### Claude API
- **Purpose**: AI processing, intelligent automation
- **Models**: Claude Opus 4.6, Sonnet 4.6, Haiku 4.5
- **Use**: Code analysis, text generation, tool calling

## Git Workflow

### Branch Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Task | `task-<ID>` | `task-3672` |
| Feature | `feature/<name>` | `feature/auth` |
| Bugfix | `fix/<name>` | `fix/login-bug` |
| Release | `release/<version>` | `release/1.0.0` |

### PR Workflow

1. Create a branch: `git checkout -b task-<ID>`
2. Make changes and commit
3. Push to origin: `git push origin task-<ID>`
4. Create PR on GitHub
5. Wait for CI pipeline to pass
6. Get PR review
7. Merge to main after approval

### Worktree Workflow

1. Create worktree: `git worktree add .cogno/agents/task-<ID> origin/main`
2. Work in isolation in the worktree
3. Commit changes as needed
4. Push branch: `git push origin task-<ID>`
5. Create PR and follow merge workflow

## CI/CD Pipelines

### CI Pipeline (.github/workflows/ci.yml)
- **Triggers**: Push to main/develop, PRs
- **Validations**:
  - YAML file validation
  - Markdown file validation
  - Documentation completeness check

### CD Pipeline (.github/workflows/cd.yml)
- **Triggers**: Push to main branch
- **Actions**:
  - Pre-deployment validation
  - Build artifacts
  - Deploy documentation
  - Post-deployment verification

**Required Files for CI/CD Success**:
- `CI_CD_GUIDE.md`
- `QUICK_REFERENCE.md`

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Worker instructions and guidelines
- **[CI_CD_GUIDE.md](CI_CD_GUIDE.md)** - Detailed CI/CD documentation
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference guide
- **[.cogno/app-context.md](.cogno/app-context.md)** - Integration configuration

## Troubleshooting

### CI Pipeline Failures

1. **YAML Validation Error**: Check `.github/workflows/*.yml` for syntax errors
2. **Markdown Validation Error**: Verify `.md` files have correct syntax
3. **Documentation Missing**: Ensure `CI_CD_GUIDE.md` and `QUICK_REFERENCE.md` exist

**Solution**: See [CI/CD Guide](CI_CD_GUIDE.md) for detailed troubleshooting

### Git Issues

1. **Merge Conflicts**: Resolve manually and commit
2. **Detached HEAD**: Create a branch with `git checkout -b branch-name`
3. **Push Rejection**: Ensure branch is up-to-date with `git pull`

**Solution**: See [Quick Reference](QUICK_REFERENCE.md) for git commands

## Security

### Best Practices
- Never commit secrets or sensitive data
- Use `.env` files for local configuration (excluded by `.gitignore`)
- Enable branch protection on `main` branch
- Require PR reviews before merge
- Use SSH keys for GitHub authentication

### Branch Protection
The `main` branch should have:
- Require CI pipeline to pass
- Require PR reviews
- Dismiss stale reviews on new commits
- Restrict who can push

## Contributing

1. Create a task branch: `git checkout -b task-<ID>`
2. Follow the [Git Workflow](#git-workflow) section
3. Reference related issues in PR description
4. Ensure CI pipeline passes
5. Request review from code owners
6. Merge after approval

## Support

- Check [CLAUDE.md](CLAUDE.md) for worker guidelines
- Review [CI_CD_GUIDE.md](CI_CD_GUIDE.md) for pipeline help
- See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for common commands
- Check [.cogno/app-context.md](.cogno/app-context.md) for integration details

## Resources

- [GitHub Repository](https://github.com/Equinox-Partners/cogno-workspace)
- [GitHub Actions](https://github.com/Equinox-Partners/cogno-workspace/actions)
- [GitHub Docs](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Project**: Equinox Partners Cogno Workspace  
**Owner**: Equinox-Partners  
**Repository**: https://github.com/Equinox-Partners/cogno-workspace  
**Last Updated**: 2026-07-27
