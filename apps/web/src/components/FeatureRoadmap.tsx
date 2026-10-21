"use client";

import React from "react";
import { CheckCircle2, Clock, ShieldAlert, GitPullRequest, Search, FileCode2, Terminal } from "lucide-react";

interface FeatureItem {
  name: string;
  category: string;
  status: "implemented" | "planned" | "in-progress";
  description: string;
  icon: React.ComponentType<{ className?: string }>;
}

const features: FeatureItem[] = [
  {
    name: "Engineering Foundation & Monorepo",
    category: "Foundation",
    status: "implemented",
    description: "Monorepo layout, FastAPI backend, Next.js web shell, Ruff, Mypy, Pytest, and GitHub Actions CI.",
    icon: Terminal,
  },
  {
    name: "Versioned Health & Readiness Probes",
    category: "Foundation",
    status: "implemented",
    description: "/api/v1/health and /api/v1/ready endpoints with typed Pydantic responses and structured logging.",
    icon: CheckCircle2,
  },
  {
    name: "Static Application Security Testing (SAST)",
    category: "Scanners",
    status: "planned",
    description: "Deterministic Semgrep scanner integration for AST-based rule analysis across Python, JS/TS, Go.",
    icon: Search,
  },
  {
    name: "Software Composition Analysis (SCA)",
    category: "Scanners",
    status: "planned",
    description: "Trivy scanner pipeline resolving CVEs and dependency vulnerability graphs from manifests.",
    icon: ShieldAlert,
  },
  {
    name: "SARIF Normalization & Risk Correlation",
    category: "Engine",
    status: "planned",
    description: "Canonical data modeling, vulnerability deduplication, and CVSS v3.1 prioritization.",
    icon: FileCode2,
  },
  {
    name: "LangGraph Triage & Fix Synthesis",
    category: "AI Reasoning",
    status: "planned",
    description: "Stateful agent coordination explaining root causes and synthesizing precise unified patch diffs.",
    icon: Clock,
  },
  {
    name: "Ephemeral Sandbox Patch Verification",
    category: "Verification",
    status: "planned",
    description: "Isolated disposable container execution running test suites to guarantee zero regression before review.",
    icon: Terminal,
  },
  {
    name: "Human-in-the-Loop PR Generation",
    category: "Delivery",
    status: "planned",
    description: "Developer console sign-off: Accept, Edit, or Reject. Creates Git branch and PR only upon approval.",
    icon: GitPullRequest,
  },
];

export function FeatureRoadmap() {
  return (
    <div className="rounded-xl border border-slate-800 bg-cyber-900/60 p-6 backdrop-blur-sm">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-base font-semibold text-slate-100">
            Platform Capabilities & Engineering Roadmap
          </h2>
          <p className="text-xs text-slate-400">
            Phase 1 Foundation active — Unimplemented modules are marked as Planned (no simulated or fake metrics).
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
        {features.map((feat) => {
          const Icon = feat.icon;
          const isDone = feat.status === "implemented";
          return (
            <div
              key={feat.name}
              className={`p-4 rounded-lg border flex flex-col justify-between ${
                isDone
                  ? "bg-cyan-950/20 border-cyan-800/40 text-slate-200"
                  : "bg-cyber-950/40 border-slate-800/60 text-slate-400"
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div
                    className={`p-1.5 rounded-md ${
                      isDone
                        ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20"
                        : "bg-slate-800 text-slate-400 border border-slate-700"
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                  </div>
                  <span
                    className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded-full border ${
                      isDone
                        ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/20"
                        : "bg-slate-800 text-slate-400 border-slate-700"
                    }`}
                  >
                    {feat.status}
                  </span>
                </div>
                <h3 className="text-sm font-medium text-slate-100 mb-1">{feat.name}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{feat.description}</p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between text-[11px] font-mono text-slate-500">
                <span>Domain</span>
                <span className="text-slate-400">{feat.category}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
