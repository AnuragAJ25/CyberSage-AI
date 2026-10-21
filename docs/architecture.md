# CyberSage AI - System Architecture

CyberSage AI is an AI-assisted cybersecurity detection, analysis, and remediation platform. It combines deterministic static and dynamic security scanners with bounded LLM orchestration to detect vulnerabilities, explain their operational impact, synthesize verified remediations, and present pull-request-ready changes for human review.

## High-Level Architecture Diagram

```mermaid
flowchart TD
    subgraph Inputs ["1. Input Sources & Ingestion"]
        Repo["Source Repositories (Git/Zip)"]
        Manifests["Dependency Manifests (npm, pip, maven)"]
        Configs["IaC & Configs (Docker, K8s, Terraform)"]
        Logs["Security Logs (WAF, SIEM)"]
        WebApps["Authorized Web Apps (SSRF-Guarded)"]
    end

    subgraph Scanners ["2. Deterministic Scanners"]
        SAST["SAST (Semgrep, Bandit)"]
        SCA["SCA (Trivy, pip-audit)"]
        SecretScan["Secret Detection (Gitleaks)"]
        DAST["DAST (OWASP ZAP / Custom HTTP)"]
    end

    subgraph Engine ["3. Core Orchestration & Normalization"]
        IngestService["Ingestion & Validation Gateway"]
        Normalizer["SARIF / Unified Schema Normalizer"]
        Correlator["Vulnerability De-duplicator & Risk Scorer"]
        DB[(PostgreSQL Store)]
    end

    subgraph AIOrchestration ["4. AI Reasoning (LangGraph & LangChain)"]
        TriageAgent["Triage & Impact Explainer Agent"]
        FixGenAgent["Remediation Synthesis Agent"]
        LangGraph["LangGraph Stateful Workflow Coordinator"]
    end

    subgraph Sandbox ["5. Verification Sandbox (Isolated)"]
        EphemeralEnv["Disposable Sandbox Container"]
        PatchApply["Apply Diff / Patch"]
        RegressionTest["Run Scanners & Test Suite"]
    end

    subgraph DeveloperApproval ["6. Human-in-the-Loop & Delivery"]
        UI["CyberSage Developer Console"]
        ApprovalGate{"Developer Sign-Off"}
        PR["GitHub / GitLab Pull Request"]
        Audit["Audit Trail & Event Log"]
    end

    %% Ingestion to Scanners
    Repo --> IngestService
    Manifests --> IngestService
    Configs --> IngestService
    Logs --> IngestService
    WebApps --> IngestService

    IngestService --> SAST
    IngestService --> SCA
    IngestService --> SecretScan
    IngestService --> DAST

    %% Scanners to Normalizer
    SAST --> Normalizer
    SCA --> Normalizer
    SecretScan --> Normalizer
    DAST --> Normalizer

    Normalizer --> Correlator
    Correlator --> DB
    Correlator --> LangGraph

    %% LangGraph Agents
    LangGraph --> TriageAgent
    LangGraph --> FixGenAgent

    %% Remediation to Sandbox
    FixGenAgent --> EphemeralEnv
    EphemeralEnv --> PatchApply
    PatchApply --> RegressionTest
    RegressionTest -->|Feedback Loop on Failure| FixGenAgent
    RegressionTest -->|Verified Fix Diff| LangGraph

    %% Delivery to Human
    LangGraph --> UI
    UI --> ApprovalGate
    ApprovalGate -->|Accepted| PR
    ApprovalGate -->|Rejected / Edited| Audit
    ApprovalGate -->|Audit Record| DB
```

## System Components

### 1. Ingestion Layer
- Accepts code repositories, dependency manifests, configuration files, and authorized web URLs.
- Applies strict size limits, archive unpack quotas (zip-slip defense), and SSRF validation for web targets.

### 2. Deterministic Scanner Tier
- Runs isolated scanners (Semgrep, Trivy, Gitleaks, etc.) emitting standard machine-readable outputs (SARIF, JSON).
- Scanner outputs represent empirical ground truth; LLMs are never used as substitute scanners.

### 3. Normalization & Correlation
- Standardizes diverse scanner payloads into a canonical `Finding` schema with CVE, CWE, CVSS v3.1, file coordinates, and contextual code snippets.
- Deduplicates identical findings across scanner tools and correlates related security issues.

### 4. AI Orchestration (LangGraph + LangChain)
- Coordinates bounded reasoning workflows using state machines.
- **Triage Agent**: Explains vulnerability mechanics, attack vectors, and exploitability.
- **Remediation Agent**: Produces unified diffs tailored to the codebase without introducing regressions or hallucinated dependencies.
- Enforces strict Pydantic output schemas and treats inputs as untrusted data to mitigate prompt injection.

### 5. Verification Sandbox
- Executes in an isolated disposable sandbox with resource and timeout bounds.
- Applies the proposed patch, runs linters, unit tests, and rescans the target to verify that the vulnerability is neutralized without breaking existing functionality.

### 6. Human-in-the-Loop Approval & PR Engine
- Surfaces findings, AI explanations, verified diffs, and test results in the developer console.
- Grants final authority to human developers: Accept, Edit, or Reject.
- Automated merging or unapproved deployment is strictly prohibited.
