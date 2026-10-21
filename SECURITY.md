# Security Policy

## Reporting Security Vulnerabilities

We take the security of CyberSage AI seriously. If you identify a security issue, vulnerability, or potential leak within CyberSage AI:

1. **Do not create a public issue** on GitHub.
2. Email the maintainers directly or use GitHub Private Vulnerability Reporting:
   - Anurag Jaiswal ([GitHub @AnuragAJ25](https://github.com/AnuragAJ25))
   - Dhanya Charni
3. Include detailed steps to reproduce the vulnerability, including sample requests, environment settings, and affected components.

## Security Architecture Principles

- **No Arbitrary Code Execution**: Untrusted code scanned by CyberSage AI is isolated within dedicated sandboxes with memory, process, network, and execution time limits.
- **Strict Human-in-the-Loop**: Remediations and patches proposed by AI models require explicit developer review and sign-off. CyberSage AI will never merge or deploy code automatically.
- **SSRF Prevention & Explicit Web Scanning Authorization**: Active web scanning is disabled by default and requires explicit verification and ownership checks. Internal network addresses (RFC 1918, RFC 4193, loopbacks, link-local, cloud metadata) are blocked.
- **Prompt Injection Defense**: Scanner outputs and user code are treated as untrusted data. AI agents operate under bounded structured schemas with defensive guardrails.
- **Zero Secrets in Commits**: All keys, passwords, and tokens are injected via environment variables and never logged or serialized to disk.
