# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- Hardened secret configuration in `apps/api/app/core/config.py`: rejects known placeholders and weak secrets in production/staging.
- Implemented honest readiness probe in `/api/v1/ready` distinguishing operational core API from planned roadmap capabilities (Semgrep, OSV-Scanner, Gitleaks, AI agents, sandbox).
- Removed hardcoded credentials in `infra/docker-compose.yml` using strict Compose variable validation `${POSTGRES_PASSWORD:?}`.
- Refined initial scanner MVP definition to Semgrep (SAST), OSV-Scanner (SCA), and Gitleaks (Secrets), marking DAST as optional/future scope.
- Added comprehensive unit tests in `apps/api/tests/test_health.py` covering honest readiness, unconfigured fallbacks, and secret validation.

## [0.1.0] - 2026-10-21
### Added
- Phase 1: Established CyberSage AI engineering foundation and monorepo structure.
- Monorepo directory layout for `apps/api`, `apps/web`, `tests`, `fixtures`, `docs`, `scripts`, `infra`, and `.github/workflows`.
- FastAPI backend application in `apps/api` with typed Pydantic settings, structured logging, centralized error handling, and versioned health/readiness endpoints (`/api/v1/health`, `/api/v1/ready`).
- Next.js 14+ TypeScript/Tailwind CSS frontend console in `apps/web` with clean dark-mode shell, interactive status panel, and transparent empty states distinguishing implemented vs. planned features.
- Root configuration files: `.gitignore`, `.editorconfig`, `.env.example`, `.pre-commit-config.yaml`, `CONTRIBUTING.md`, `SECURITY.md`.
- Documentation: `docs/architecture.md`, `docs/threat-model.md`, and initial Architecture Decision Record `docs/adr/0001-monorepo-and-core-stack.md`.
- GitHub Actions CI workflow in `.github/workflows/ci.yml` running backend linting, type-checking, pytest suites, and frontend linting, type-checking, and build validation.
