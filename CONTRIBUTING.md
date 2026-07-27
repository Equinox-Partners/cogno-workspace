# Contributing to Cogno Workspace

Thank you for your interest in contributing to the Equinox Partners Cogno Workspace! This document provides guidelines and instructions for contributing.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing opinions and experiences
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites
- Git 2.38+
- GitHub account with appropriate permissions
- Familiarity with the [CLAUDE.md](CLAUDE.md) worker instructions
- Understanding of the [CI/CD pipeline](CI_CD_GUIDE.md)

### Setting Up Your Environment

1. **Fork the repository** (if not a team member)
   ```bash
   # Navigate to https://github.com/Equinox-Partners/cogno-workspace
   # Click "Fork" button
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/cogno-workspace.git
   cd cogno-workspace
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/Equinox-Partners/cogno-workspace.git
   ```

4. **Create a task branch**
   ```bash
   git fetch origin main
   git checkout -b task-<ID> origin/main
   ```

## Making Changes

### Workflow

1. **Create a task branch**
   ```bash
   git checkout -b task-<ID> origin/main
   ```

2. **Make your changes**
   - Follow the code style guidelines
   - Write clear commit messages
   - Keep commits atomic and logical

3. **Commit your changes**
   ```bash
   git add <files>
   git commit -m "Brief description of changes"
   ```

4. **Push to your fork**
   ```bash
   git push origin task-<ID>
   ```

5. **Create a Pull Request**
   - Go to GitHub and create a new PR
   - Use the PR template provided
   - Reference related issues
   - Ensure CI/CD passes

### Branch Naming

Follow the naming convention:

| Type | Pattern | Example |
|------|---------|---------|
| Task | `task-<ID>` | `task-3672` |
| Feature | `feature/<name>` | `feature/new-dashboard` |
| Bugfix | `fix/<name>` | `fix/auth-timeout` |
| Chore | `chore/<name>` | `chore/update-deps` |

### Commit Messages

Write clear, descriptive commit messages:

```
[TYPE] Brief description (50 chars or less)

More detailed explanation if needed, wrapped at 72 characters.
Explain what and why, not how.

Fixes #123
```

**Commit Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (no logic change)
- `refactor:` Code refactoring (no feature change)
- `perf:` Performance improvement
- `test:` Test changes
- `chore:` Build, dependency, or tooling changes

## Pull Request Process

### Before Submitting

- [ ] Your code follows the project's code style
- [ ] You've tested your changes locally
- [ ] You've updated documentation if needed
- [ ] CI/CD pipeline passes
- [ ] You've filled out the PR template completely

### PR Template

The PR template includes:
- Description of changes
- Type of change (bug fix, feature, etc.)
- Testing performed
- Documentation updates
- Checklist completion

### PR Review Process

1. **CI Pipeline Validation**
   - YAML syntax validation
   - Markdown validation
   - Documentation completeness check

2. **Code Review**
   - At least one approval required
   - Code owners must review
   - Address review comments
   - Re-request review after changes

3. **Merge**
   - Squash and merge recommended for clarity
   - Delete branch after merge
   - Close related issues if applicable

## Documentation

### Updating Documentation

If your changes affect documentation:
1. Update relevant `.md` files
2. Update `CI_CD_GUIDE.md` if CI/CD changes
3. Update `QUICK_REFERENCE.md` for common commands
4. Update README if structure changes

### Documentation Format

- Use Markdown format
- Include code examples where helpful
- Add table of contents for long documents
- Include links to related resources
- Update "Last Updated" dates

## Testing

### Required Tests

All changes must pass:
- ✅ CI pipeline validation
- ✅ Markdown validation
- ✅ YAML syntax validation
- ✅ Documentation completeness

### Running Tests Locally

1. **Validate YAML**
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"
   ```

2. **Validate Markdown**
   - Check for proper syntax
   - Verify links work
   - Check code block formatting

3. **Verify Documentation**
   ```bash
   ls -la CI_CD_GUIDE.md QUICK_REFERENCE.md
   ```

## Reporting Issues

### Bug Reports

Create a bug report using the bug template:
1. Go to GitHub Issues
2. Click "New issue"
3. Select "Bug Report"
4. Fill in template details
5. Submit issue

**Include:**
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Relevant logs/errors

### Feature Requests

Create a feature request using the feature template:
1. Go to GitHub Issues
2. Click "New issue"
3. Select "Feature Request"
4. Fill in template details
5. Submit issue

**Include:**
- Clear problem statement
- Proposed solution
- Use case/benefit
- Alternative approaches

### Documentation Requests

Create a documentation request using the docs template:
1. Go to GitHub Issues
2. Click "New issue"
3. Select "Documentation"
4. Fill in template details
5. Submit issue

**Include:**
- What documentation is needed
- Current gaps
- Affected areas
- Suggested content

## Security

### Reporting Security Issues

**Do not** open public issues for security vulnerabilities.

See [SECURITY.md](SECURITY.md) for instructions on reporting security issues responsibly.

### Security Practices

- Never commit secrets or credentials
- Use `.env.example` for configuration
- Follow secure coding practices
- Review code for security issues

## Getting Help

### Questions?

- Review [CLAUDE.md](CLAUDE.md) for worker guidelines
- Check [CI_CD_GUIDE.md](CI_CD_GUIDE.md) for pipeline help
- See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for common commands
- Review existing issues and PRs

### Discussions

- Use GitHub Discussions for general questions
- Reference relevant issues/PRs
- Follow community guidelines

## Recognition

Contributors will be recognized:
- In commit messages and PR descriptions
- In release notes for major contributions
- In a CONTRIBUTORS.md file
- Through GitHub contribution graph

## License

By contributing to this project, you agree that your contributions will be licensed under its MIT License.

## Additional Resources

- [GitHub Docs](https://docs.github.com)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Markdown Guide](https://www.markdownguide.org/)
- [YAML Syntax](https://yaml.org/spec/)

---

**Thank you for contributing!** 🎉

Questions? Feel free to reach out to the team at Equinox Partners.

**Last Updated**: 2026-07-28
