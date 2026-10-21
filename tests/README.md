# Integration & System Tests

This directory houses cross-cutting integration, end-to-end, and security validation test suites:

- `e2e/`: Full pipeline tests from code ingestion to developer approval.
- `security/`: SSRF guardrail tests, prompt injection resilience tests, and sandbox escape mitigation checks.

Unit tests specific to the backend reside in `apps/api/tests/`.
Unit and component tests for the frontend reside in `apps/web/__tests__/`.
