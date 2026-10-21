# ADR 0001: Monorepo Architecture and Core Technology Stack

## Status
Accepted

## Context
CyberSage AI requires tightly coupled coordination between:
- A high-performance Python API backend managing security scanners, SARIF normalization, and LangGraph-based AI workflows.
- A modern, responsive developer dashboard for inspecting vulnerabilities, reviewing explanations, and accepting/rejecting remediation pull requests.
- Shared fixtures, end-to-end security test suites, and infrastructure definitions.

A fragmented multi-repository structure would introduce synchronization overhead, version drift between backend schemas and frontend types, and friction during local testing.

## Decision
1. **Repository Structure**:
   Adopt a monorepo architecture:
   - `apps/api`: Python 3.12+ / FastAPI application with Pydantic v2 schemas and SQLAlchemy.
   - `apps/web`: Next.js 14+ (App Router), TypeScript (strict mode), and Tailwind CSS.
   - `docs`: System documentation, ADRs, threat models.
   - `fixtures`: Sanitized test repositories and mock datasets.
   - `infra`: Container definitions and local orchestrations.
   - `scripts`: Developer automation and CI helper scripts.
   - `tests`: End-to-end integration and security validation test suites.

2. **Backend Engineering**:
   - Framework: **FastAPI** for asynchronous throughput and native OpenAPI documentation.
   - Settings & Validation: **Pydantic v2** and **pydantic-settings** for strictly typed environment configurations.
   - Tooling & Linting: **Ruff** for fast linting/formatting; **mypy** for static type analysis; **pytest** for testing.

3. **Frontend Engineering**:
   - Framework: **Next.js** with TypeScript for type safety and fast server-side / static rendering.
   - Styling: **Tailwind CSS** for maintainable design tokens and responsive states.

4. **AI Orchestration**:
   - Framework: **LangGraph** for resilient state-machine coordination and human-in-the-loop cycles; **LangChain** for model-agnostic integrations.

## Consequences
- **Positive**: Single pull-request workflow for schema updates; shared CI workflows; unified documentation and threat models.
- **Negative**: Monorepo CI must maintain selective execution paths to avoid redundant builds when only backend or frontend files change.
