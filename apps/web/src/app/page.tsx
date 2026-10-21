import React from "react";
import { Navbar } from "@/components/Navbar";
import { StatusMonitor } from "@/components/StatusMonitor";
import { FeatureRoadmap } from "@/components/FeatureRoadmap";
import { ScanQueueEmptyState } from "@/components/ScanQueueEmptyState";

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col bg-cyber-950">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Hero Section */}
        <div className="relative overflow-hidden rounded-2xl border border-slate-800 bg-gradient-to-b from-cyber-900 to-cyber-950 p-8">
          <div className="absolute top-0 right-0 -mt-8 -mr-8 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="relative z-10 max-w-3xl">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-mono bg-cyan-500/10 border border-cyan-500/20 text-cyan-300 mb-4">
              <span className="w-2 h-2 rounded-full bg-cyan-400" />
              <span>CyberForge AI & Cybersecurity Hackathon</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-100">
              Autonomous Detection. Bounded Reasoning.{" "}
              <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                Human-Approved Remediation.
              </span>
            </h1>
            <p className="mt-3 text-sm sm:text-base text-slate-400 leading-relaxed">
              CyberSage AI orchestrates deterministic static/dynamic security scanners with LangGraph stateful AI agents to find vulnerabilities, explain exploitability, and produce verified pull requests with mandatory developer sign-off.
            </p>
          </div>
        </div>

        {/* Live Backend Health & Subsystem Status */}
        <StatusMonitor />

        {/* Vulnerability Queue Empty State */}
        <ScanQueueEmptyState />

        {/* Capabilities Matrix / Roadmap */}
        <FeatureRoadmap />
      </main>

      <footer className="border-t border-slate-800/80 bg-cyber-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>CyberSage AI &copy; 2026 — Team Crazy Champions</span>
          <span className="font-mono text-slate-600">Phase 1 Foundation • Target Branch: main</span>
        </div>
      </footer>
    </div>
  );
}
