# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in the Equinox Partners Cogno Workspace, please email security@equinox-partners.com with:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if available)

**Please do not open public GitHub issues for security vulnerabilities.**

## Security Best Practices

### Git & Repository

1. **Authentication**
   - Use SSH keys for GitHub authentication
   - Enable SSH key passphrase protection
   - Rotate keys regularly

2. **Branch Protection**
   - Main branch requires:
     - CI pipeline to pass
     - PR reviews before merge
     - Status checks to pass
     - Dismiss stale reviews on new commits

3. **Access Control**
   - Use GitHub CODEOWNERS for code ownership
   - Limit push access to main branch
   - Review team permissions regularly

### Secrets & Configuration

1. **Environment Variables**
   - Never commit `.env` files or secrets
   - Use GitHub secrets for sensitive data
   - Use `.env.example` for documentation

2. **Credentials**
   - Store credentials in system keychain/credential manager
   - Never commit API keys, tokens, or passwords
   - Rotate credentials periodically

3. **Code Review**
   - All code changes require review
   - Focus on security implications
   - Check for hardcoded secrets

### CI/CD Security

1. **Workflow Security**
   - Limit workflow permissions
   - Use specific action versions (avoid @latest)
   - Review workflow logs for sensitive data leaks

2. **Artifact Management**
   - Don't upload secrets to artifacts
   - Clean up artifacts regularly
   - Review what's being stored

### Dependency Management

1. **Updates**
   - Keep dependencies up-to-date
   - Monitor for security updates
   - Review changelog before updating

2. **Verification**
   - Verify package signatures when available
   - Check package source integrity
   - Use lock files (package-lock.json, yarn.lock)

### Documentation Security

1. **Sensitive Information**
   - Don't document API keys or secrets
   - Use `.env.example` for configuration
   - Include setup instructions without secrets

2. **Access Documentation**
   - Document access control policies
   - Maintain list of authorized personnel
   - Track access changes

## Compliance

### Data Protection
- Comply with data protection regulations (GDPR, CCPA, etc.)
- Implement data retention policies
- Secure sensitive data transmission

### Audit Logging
- Enable GitHub audit logs
- Monitor repository access
- Review security events regularly

### Incident Response
- Have an incident response plan
- Document security incidents
- Post-incident review and remediation

## Security Checklist

Before deploying to production:

- [ ] All code reviewed by authorized personnel
- [ ] No hardcoded secrets in code
- [ ] Dependencies updated and secure
- [ ] Security tests passing
- [ ] CI/CD pipeline validated
- [ ] Access controls configured correctly
- [ ] Audit logs enabled
- [ ] Monitoring and alerting active
- [ ] Incident response plan in place
- [ ] Security documentation up-to-date

## Third-Party Services

### Authorized Services
- GitHub (Repository, Actions, API)
- Notion (MCP Integration)
- Claude API (AI Processing)

### Security Requirements
- Services must have security documentation
- Authentication credentials properly secured
- API tokens rotated regularly
- Services audited for compliance

## Training & Awareness

### For All Team Members
- Understand security policies
- Follow secure coding practices
- Report security concerns
- Participate in security reviews

### For Maintainers
- Perform regular security audits
- Review and update security policies
- Manage security training
- Coordinate incident response

## Resources

- [GitHub Security Documentation](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Git Security](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)
- [Securing Secrets with GitHub](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## Security Policy Changes

This security policy is subject to change. Updates will be announced through:
- GitHub notifications
- Email to authorized team members
- Changelog updates

---

**Last Updated**: 2026-07-28  
**Maintained By**: Equinox Partners Security Team
