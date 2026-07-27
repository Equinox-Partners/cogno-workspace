# CI/CD Pipeline Guide

## Overview

This document describes the continuous integration and continuous deployment (CI/CD) pipeline for the Equinox Partners Cogno Workspace project.

## Pipeline Architecture

### Continuous Integration (CI) Pipeline

The CI pipeline (``.github/workflows/ci.yml``) is triggered on:
- Push events to `main` or `develop` branches
- Pull requests targeting `main` or `develop` branches

**Pipeline Steps:**
1. **Code Checkout** - Clones the repository
2. **YAML Validation** - Validates all YAML files in `.github/workflows/`
3. **Markdown Validation** - Validates Markdown files for syntax and structure
4. **Documentation Completeness Check** - Verifies required documentation files exist
5. **Summary** - Reports validation status

**Required Files:**
- `CI_CD_GUIDE.md` - This file
- `QUICK_REFERENCE.md` - Quick reference guide

### Continuous Deployment (CD) Pipeline

The CD pipeline (``.github/workflows/cd.yml``) is triggered on:
- Push events to the `main` branch only

**Pipeline Steps:**
1. **Code Checkout** - Clones the repository
2. **Build Environment Setup** - Initializes deployment environment
3. **Deployment Prerequisites Validation** - Verifies required files and configuration
4. **Build Artifacts** - Creates deployment artifacts (documentation)
5. **Deploy to Production** - Deploys the built artifacts
6. **Post-Deployment Verification** - Verifies deployment success
7. **Deployment Summary** - Reports deployment status

**Deployment Artifacts:**
- Documentation files from `CI_CD_GUIDE.md` and `QUICK_REFERENCE.md`
- Deployed to production documentation endpoint

## Branch Strategy

### Main Branch (`main`)
- Production-ready code
- PR reviews required before merge
- Both CI and CD pipelines run on push

### Develop Branch (`develop`)
- Integration branch for feature development
- CI pipeline runs on push and PR
- CD pipeline does not run

### Feature Branches (`task-<ID>` or `feature/*`)
- Individual feature or task development
- Create from `develop` or `main`
- CI pipeline runs on PR to `develop` or `main`

## Workflow Status

### Current Status: ✅ Active

- **CI Pipeline**: Active and passing
- **CD Pipeline**: Active and configured
- **Required Documentation**: Present and validated

## Running Workflows

### Automatic Triggers

Workflows run automatically on:
1. Push to `main` or `develop`
2. Pull requests to `main` or `develop`

### Manual Trigger

To manually trigger workflows:
1. Go to GitHub Actions tab
2. Select the workflow
3. Click "Run workflow"
4. Select the branch
5. Click "Run workflow"

## Troubleshooting

### CI Pipeline Failures

**YAML Validation Errors:**
- Check syntax in `.github/workflows/*.yml` files
- Ensure proper indentation (2 spaces)
- Use YAML validator tools

**Markdown Validation Errors:**
- Check `.md` files for syntax errors
- Ensure code blocks are properly closed with backticks

**Documentation Completeness Errors:**
- Verify `CI_CD_GUIDE.md` exists in repository root
- Verify `QUICK_REFERENCE.md` exists in repository root

### CD Pipeline Failures

**Deployment Prerequisites Not Met:**
- Verify `CI_CD_GUIDE.md` and `QUICK_REFERENCE.md` exist
- Ensure files have correct content

**Build Failures:**
- Check `build/docs/` directory creation
- Verify file permissions
- Check documentation file content

**Deployment Errors:**
- Verify deployment endpoint is accessible
- Check deployment credentials/permissions
- Review deployment logs

## Environment Variables

Currently, the pipelines do not require environment variables. Configuration is read from:
- Repository structure (`.cogno/`, `.github/`)
- Documentation files in repository root

## Security Considerations

### Workflow Permissions
- Workflows run with minimal required permissions
- Token scopes limited to repository scope

### Secrets Management
- No secrets currently required in workflows
- Configuration files stored in repository

### Branch Protection
- Main branch should have:
  - Require status checks before merge
  - Require CI pipeline to pass
  - Require PR reviews before merge
  - Dismiss stale PR approvals on new commits

## Maintenance

### Regular Tasks
- Monitor workflow execution
- Review workflow logs for errors
- Update documentation as needed
- Keep dependencies current

### Performance Monitoring
- Review workflow execution times
- Optimize slow steps if needed
- Archive old workflow runs

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub CLI Documentation](https://cli.github.com/manual/)

---

**Last Updated**: 2026-07-27
**Maintained By**: Cogno Workers
