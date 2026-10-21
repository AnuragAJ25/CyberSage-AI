# CyberSage AI - Threat Model

This document outlines the threat model for CyberSage AI using STRIDE principles, detailing threat vectors, trust boundaries, and implemented countermeasures.

## Trust Boundaries

1. **Client / Web UI <-> API Boundary**: Authenticated API session, TLS, input validation via Pydantic schemas.
2. **API Host <-> Target Repositories / User Code**: Untrusted third-party code and manifests.
3. **API Host <-> External Scanners**: Subprocess invocation boundary; strictly no `shell=True` and isolated args.
4. **API Host <-> AI Provider (LLMs)**: External network boundary; prompt injection risks and data exfiltration.
5. **API Host <-> Verification Sandbox**: Disposable ephemeral containers with resource and network restrictions.

## STRIDE Analysis & Countermeasures

| Threat Category | Potential Attack Vector | CyberSage AI Countermeasure |
| :--- | :--- | :--- |
| **Spoofing** | Attacker impersonates an authorized developer or commits unauthorized PRs. | PR generation requires signed developer tokens and explicit UI approval. No automatic merge or commit. |
| **Tampering** | Malicious repo code modifies scanner binary or tampers with the API host environment. | Repositories are scanned in read-only mounts. Patch verification runs in disposable ephemeral sandboxes. |
| **Repudiation** | Actions taken during scanning or remediation lack audit trails. | Persistent audit logs track scan provenance, scanner raw outputs, AI prompts/responses, and developer approvals. |
| **Information Disclosure** | Leakage of private source code or secrets via AI queries or error dumps. | Stripping of detected secrets before LLM transmission; masking of sensitive strings in logs and error responses. |
| **Denial of Service** | Archive bombs (zip-bombs), infinite loops in scanners, or unbounded LLM calls. | Strict decompression size and entry limits, subprocess timeouts (e.g., 60s), CPU/memory quotas, and rate limiting. |
| **Elevation of Privilege** | Remote code execution via unsafe subprocess invocation or template injection. | Parameterized subprocess execution (`shlex`/list args, `shell=False`), minimal runtime user privileges (non-root). |

## Specific Cybersecurity Controls

### 1. Prompt Injection Defense
- Scanned repository source files, configuration manifests, and scanner logs are categorized as **Untrusted Data**.
- Prompts employ delimiter-based isolation and system instructions forbidding execution of embedded directives.
- Model responses are enforced through structured JSON Schema / Pydantic parsing rather than free-form shell evaluation.

### 2. SSRF Guardrails for Web Scanning
- Active web application scanning is disabled by default and requires explicit verified domain ownership.
- All target URLs are resolved and validated against a denylist of private, link-local, loopback, and cloud metadata IPs:
  - `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
  - `127.0.0.0/8`, `::1`
  - `169.254.169.254` (Cloud Instance Metadata Service)
  - `fc00::/7` (Unique Local Addresses)

### 3. Disposable Sandboxing
- Verification of generated patches is conducted in ephemeral containers.
- Execution parameters:
  - Read-only root filesystem where feasible.
  - No access to production database credentials or host environment variables.
  - Network isolation enabled during test suite execution.
