# Test Fixtures

This directory contains sanitized repositories, sample manifests, and mock scanner outputs used for integration testing:

- `samples/`: Example code snippets containing known vulnerabilities (SQLi, XSS, insecure deserialization) for scanner verification.
- `manifests/`: Example dependency manifests (e.g., `requirements.txt`, `package.json`, `pom.xml`) with known vulnerable dependency versions.
- `scanner-outputs/`: Canonical SARIF and JSON scanner mock responses (Semgrep, Trivy, Gitleaks).
