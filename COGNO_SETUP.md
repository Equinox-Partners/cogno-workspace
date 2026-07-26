# Cogno Workspace CI/CD Setup Guide

## Overview

This guide explains how to configure and use the Cogno integration with GitHub Actions CI/CD pipelines in the `cogno-workspace` repository.

## Prerequisites

- Access to the Cogno platform and API
- GitHub repository access with permissions to manage secrets
- Basic understanding of GitHub Actions and workflows

## Step 1: Configure GitHub Secrets

You must add the following secrets to your GitHub repository settings:

### Required Secrets

1. **COGNO_API_TOKEN** (Required)
   - Description: Bearer token for authentication with Cogno API
      - How to obtain: Contact your Cogno administrator
         - Location: Repository → Settings → Secrets and variables → Actions
            - Value format: `Bearer <your-api-token>`

            2. **COGNO_API_ENDPOINT** (Required)
               - Description: Base URL for the Cogno API
                  - Example: `https://cogno-api.example.com`
                     - How to obtain: Provided by Cogno platform administrator

                     3. **COGNO_WORKSPACE_ID** (Required)
                        - Description: Unique identifier for your Cogno workspace
                           - Example: `cogno-workspace-001`
                              - How to obtain: Check `.cogno/repo.json` configuration

                              ### How to Add Secrets

                              1. Go to your repository → **Settings**
                              2. Click **Secrets and variables** → **Actions**
                              3. Click **New repository secret**
                              4. Enter the secret name (e.g., `COGNO_API_TOKEN`)
                              5. Paste the secret value
                              6. Click **Add secret**

                              Repeat for all three required secrets.

                              ## Step 2: Understand the CI/CD Workflows

                              ### CI Workflow (.github/workflows/ci.yml)

                              Triggers on:
                              - Push to `main` and `develop` branches
                              - Pull requests to `main` and `develop` branches

                              Runs:
                              - Cogno task structure validation (checks branch naming conventions)
                              - Dependency installation
                              - Linting and tests
                              - Cogno integration validation

                              ### CD Workflow (.github/workflows/cd.yml)

                              Triggers on:
                              - Push to `main` branch only

                              Runs:
                              - Deployment readiness validation
                              - Application build
                              - Deployment to production
                              - Cogno notification of deployment status

                              ## Step 3: Create Task Branches

                              When creating a new Cogno task:

                              1. Create a branch with the naming convention: `task-<TASK_ID>`
                                 ```bash
                                    git checkout -b task-12345
                                       ```

                                       2. Create a worktree for isolated work:
                                          ```bash
                                             git worktree add .cogno/agents/task-12345 task-12345
                                                ```

                                                3. Make your changes in the worktree

                                                4. Commit and push your changes
                                                   ```bash
                                                      git push origin task-12345
                                                         ```

                                                         ## Step 4: Monitor Workflow Execution

                                                         ### View Workflow Results

                                                         1. Go to **Actions** tab in your repository
                                                         2. Select the specific workflow (CI or CD)
                                                         3. View logs and details for each step

                                                         ### Checking Cogno Integration Status

                                                         - CI workflow will log when Cogno integration steps execute
                                                         - Check for `COGNO_API_TOKEN` environment variable availability
                                                         - Look for webhook notification logs in the deployment section

                                                         ## Step 5: Pull Request and Merge Process

                                                         1. Create a pull request from your task branch to `develop` or `main`
                                                         2. CI workflow will automatically run validation
                                                         3. Review the workflow results in the PR
                                                         4. Once approved, merge the PR
                                                         5. CD workflow will run on merge to `main`

                                                         ## Troubleshooting

                                                         ### Workflow Fails with "Token Not Found"

                                                         **Problem**: CI/CD workflow shows errors about missing `COGNO_API_TOKEN`

                                                         **Solution**:
                                                         - Verify the secret is added to GitHub repository settings
                                                         - Ensure the secret name exactly matches `COGNO_API_TOKEN`
                                                         - Check that the secret has a value
                                                         - Secrets added after workflow failure require re-running the workflow

                                                         ### Branch Naming Validation Fails

                                                         **Problem**: CI workflow fails at "Validate Cogno task structure"

                                                         **Solution**:
                                                         - Ensure branch name follows pattern: `task-<ID>` (e.g., `task-12345`)
                                                         - Acceptable branches: `main`, `develop`, or `task-*`
                                                         - Rename the branch if needed:
                                                           ```bash
                                                             git branch -m old-name task-12345
                                                               git push origin :old-name task-12345
                                                                 ```

                                                                 ### Cogno Integration Not Triggering

                                                                 **Problem**: Cogno integration steps show "Integration will be enabled when COGNO_API_TOKEN is configured"

                                                                 **Solution**:
                                                                 - This is normal behavior when secrets are not configured
                                                                 - Add the required GitHub secrets (see Step 1)
                                                                 - Re-run the workflow or create a new commit

                                                                 ### Webhook Notifications Failing

                                                                 **Problem**: Deployment status notifications not reaching Cogno

                                                                 **Solution**:
                                                                 - Verify `COGNO_API_ENDPOINT` is correct and accessible
                                                                 - Ensure firewall/network allows GitHub to reach the endpoint
                                                                 - Check Cogno API logs for incoming webhook requests
                                                                 - Verify webhook signature validation in Cogno platform

                                                                 ## API Token Management

                                                                 ### Rotating Tokens

                                                                 1. Generate a new token from Cogno admin panel
                                                                 2. Update the `COGNO_API_TOKEN` secret in GitHub
                                                                 3. Test with a new workflow run
                                                                 4. Revoke the old token from Cogno admin panel

                                                                 ### Token Expiration

                                                                 - Tokens may expire based on your Cogno configuration
                                                                 - Set calendar reminders to rotate tokens before expiration
                                                                 - Monitor workflow failures that might indicate token expiration

                                                                 ## Best Practices

                                                                 1. **Never commit secrets** to version control
                                                                 2. **Rotate API tokens** regularly (quarterly recommended)
                                                                 3. **Review workflow logs** after each deployment
                                                                 4. **Test branches** with sample commits before production use
                                                                 5. **Monitor Cogno integration** logs for early issue detection
                                                                 6. **Document task metadata** in `.cogno/task.json` when available
                                                                 7. **Use PR reviews** even if auto-merge is not enabled
                                                                 8. **Backup configurations** of your Cogno workspace settings

                                                                 ## Advanced Configuration

                                                                 ### Custom Cogno API Endpoints

                                                                 To use a custom Cogno API endpoint:

                                                                 1. Update `COGNO_API_ENDPOINT` secret with your endpoint URL
                                                                 2. Ensure the endpoint matches `.cogno/repo.json` configuration
                                                                 3. Test connectivity with a test workflow run

                                                                 ### Slack Notifications

                                                                 To enable Slack notifications (future feature):

                                                                 1. Add `SLACK_WEBHOOK_URL` secret
                                                                 2. Update CI/CD workflows to include Slack steps
                                                                 3. Configure notification preferences in `.cogno/repo.json`

                                                                 ## Support and Debugging

                                                                 ### Enabling Debug Logging

                                                                 Add this to workflow files for verbose output:
                                                                 ```yaml
                                                                 env:
                                                                   ACTIONS_STEP_DEBUG: true
                                                                     COGNO_DEBUG_MODE: true
                                                                     ```

                                                                     ### Collecting Diagnostic Information

                                                                     When troubleshooting, gather:
                                                                     - Workflow run logs (Actions tab)
                                                                     - GitHub secret names and status (not values)
                                                                     - `.cogno/repo.json` configuration
                                                                     - Error messages and timestamps

                                                                     ### Getting Help

                                                                     - Check GitHub Issues for known problems
                                                                     - Review Cogno platform documentation
                                                                     - Contact your Cogno administrator
                                                                     - Review workflow logs line by line for specific errors

                                                                     ## Additional Resources

                                                                     - [Cogno Workspace README](./README.md)
                                                                     - [Cogno Worker Instructions](./CLAUDE.md)
                                                                     - [Cogno Repository Configuration](./.cogno/repo.json)
                                                                     - [GitHub Actions Documentation](https://docs.github.com/en/actions)
                                                                     - [GitHub Secrets Management](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

                                                                     ## Version History

                                                                     - v1.0.0 (2026-07-26) - Initial setup guide for Cogno integration
                                                                     
