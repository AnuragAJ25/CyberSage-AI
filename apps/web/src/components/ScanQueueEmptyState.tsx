"use client";

import React from "react";
import { Shield, Lock, FileSearch, ArrowRight } from "lucide-react";

export function ScanQueueEmptyState() {
  return (
    <div className="rounded-xl border border-slate-800 bg-cyber-900/40 p-8 backdrop-blur-sm text-center">
      <div className="mx-auto w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 flex items-center justify-center mb-4 shadow-sm shadow-cyan-500/10">
        <Shield className="w-6 h-6" />
      </div>

      <h3 className="text-lg font-semibold text-slate-100">
        Vulnerability Queue & Analysis Engine Ready
      </h3>
      <p className="max-w-xl mx-auto text-sm text-slate-400 mt-2">
        CyberSage AI enforces strict empirical integrity: no mock alerts, fabricated CVEs, or false metrics are rendered. Deterministic scanners (Semgrep, Trivy, Gitleaks) will populate this queue during Phase 2.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto mt-6 text-left">
        <div className="p-4 rounded-lg bg-cyber-950/60 border border-slate-800/80">
          <div className="flex items-center space-x-2 text-cyan-400 mb-1.5">
            <FileSearch className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Step 1: Ingestion</span>
          </div>
          <p className="text-xs text-slate-400">
            Submit repositories, manifests, or authorized web endpoints for automated triage.
          </p>
        </div>

        <div className="p-4 rounded-lg bg-cyber-950/60 border border-slate-800/80">
          <div className="flex items-center space-x-2 text-cyan-400 mb-1.5">
            <Lock className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Step 2: Scanners</span>
          </div>
          <p className="text-xs text-slate-400">
            Deterministic AST matching, secret detection, and CVE database resolution.
          </p>
        </div>

        <div className="p-4 rounded-lg bg-cyber-950/60 border border-slate-800/80">
          <div className="flex items-center space-x-2 text-cyan-400 mb-1.5">
            <ArrowRight className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Step 3: Verification</span>
          </div>
          <p className="text-xs text-slate-400">
            LangGraph synthesizes fixes verified in disposable sandboxes before human review.
          </p>
        </div>
      </div>

      <div className="mt-6 pt-6 border-t border-slate-800/60 flex items-center justify-center space-x-2 text-xs font-mono text-slate-500">
        <span>Security Boundary:</span>
        <span className="text-slate-400">Zero auto-merging permitted • Ephemeral sandbox isolated</span>
      </div>
    </div>
  );
}
