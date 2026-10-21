# Contributing to CyberSage AI

Welcome to the CyberSage AI repository! We appreciate your interest in collaborating with us to build an AI-assisted cybersecurity detection, analysis, and remediation platform.

## Development Workflow

1. **Monorepo Layout**:
   - `apps/api`: FastAPI backend service, Pydantic schemas, scanning orchestrators, and AI agents.
   - `apps/web`: Next.js frontend console, audit trails, and interactive remediation UI.
   - `docs`: Architecture Decision Records (ADRs), threat models, and technical documentation.
   - `fixtures`: Sanitized test repositories and mock vulnerability datasets.
   - `tests`: End-to-end integration and security validation test suites.

2. **Branching & Commits**:
   - We follow [Conventional Commits](https://www.conventionalcommits.org/):
     - `feat:` for new capabilities.
     - `fix:` for bug fixes.
     - `chore:` for tooling, dependencies, or configuration changes.
     - `docs:` for documentation updates.
     - `test:` for test additions or refactoring.
   - Never force-push (`git push --force`) to shared branches.

3. **Code Quality Gates**:
   - **Backend**:
     - Linting & Formatting: `ruff check .` and `ruff format --check .`
     - Type checking: `mypy`
     - Tests: `pytest`
   - **Frontend**:
     - Linting: `npm run lint`
     - Type checking: `npm run type-check` (or `tsc --noEmit`)
     - Build: `npm run build`

4. **Security & Sandboxing Rules**:
   - Untrusted repository code must never run directly within the API host process.
   - All AI prompt inputs and scanner outputs must be treated as untrusted data.
   - Do not commit secrets, private tokens, or customer data under any circumstances.
