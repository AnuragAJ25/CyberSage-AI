"use client";

import React, { useEffect, useState, useCallback } from "react";
import { Activity, CheckCircle2, AlertTriangle, RefreshCw, Server } from "lucide-react";

interface HealthData {
  status: string;
  service: string;
  version: string;
  environment: string;
  timestamp: string;
}

interface ReadinessData {
  status: string;
  service: string;
  version: string;
  checks: Record<string, string>;
  timestamp: string;
}

export function StatusMonitor() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [readiness, setReadiness] = useState<ReadinessData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [lastChecked, setLastChecked] = useState<string>("");

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const fetchStatus = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [healthRes, readyRes] = await Promise.all([
        fetch(`${apiUrl}/api/v1/health`, { cache: "no-store" }),
        fetch(`${apiUrl}/api/v1/ready`, { cache: "no-store" }),
      ]);

      if (!healthRes.ok || !readyRes.ok) {
        throw new Error(`API returned HTTP ${healthRes.status}/${readyRes.status}`);
      }

      const healthData: HealthData = await healthRes.json();
      const readyData: ReadinessData = await readyRes.json();

      setHealth(healthData);
      setReadiness(readyData);
      setLastChecked(new Date().toLocaleTimeString());
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to connect to API";
      setError(`${message}. Ensure backend is running on ${apiUrl}`);
      setLastChecked(new Date().toLocaleTimeString());
    } finally {
      setLoading(false);
    }
  }, [apiUrl]);

  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  return (
    <div className="rounded-xl border border-slate-800 bg-cyber-900/60 p-6 backdrop-blur-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <Server className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-slate-100 flex items-center space-x-2">
              <span>FastAPI Backend Engine Status</span>
              {health && (
                <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              )}
            </h2>
            <p className="text-xs text-slate-400 font-mono">Target: {apiUrl}</p>
          </div>
        </div>

        <div className="flex items-center space-x-3 w-full sm:w-auto justify-between sm:justify-end">
          {lastChecked && (
            <span className="text-xs text-slate-500 font-mono">
              Checked: {lastChecked}
            </span>
          )}
          <button
            onClick={fetchStatus}
            disabled={loading}
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 disabled:opacity-50 transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-cyan-400" : ""}`} />
            <span>{loading ? "Probing..." : "Recheck"}</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        {/* Liveness Probe Card */}
        <div className="p-4 rounded-lg bg-cyber-950/70 border border-slate-800/80">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
              Liveness (/health)
            </span>
            {health?.status === "ok" ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            ) : (
              <Activity className="w-4 h-4 text-amber-400" />
            )}
          </div>
          <div className="text-lg font-bold text-slate-100 font-mono">
            {health ? health.status.toUpperCase() : error ? "UNREACHABLE" : "PROBING..."}
          </div>
          <p className="text-xs text-slate-500 mt-1">
            {health ? `Version: ${health.version} (${health.environment})` : "Awaiting response"}
          </p>
        </div>

        {/* Readiness Probe Card */}
        <div className="p-4 rounded-lg bg-cyber-950/70 border border-slate-800/80">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
              Readiness (/ready)
            </span>
            {readiness?.status === "ready" ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-amber-400" />
            )}
          </div>
          <div className="text-lg font-bold text-slate-100 font-mono">
            {readiness ? readiness.status.toUpperCase() : error ? "STANDBY" : "PROBING..."}
          </div>
          <p className="text-xs text-slate-500 mt-1">
            {readiness ? "Subsystems operational" : "Subsystem standby"}
          </p>
        </div>

        {/* Subsystem Health Checks */}
        <div className="p-4 rounded-lg bg-cyber-950/70 border border-slate-800/80">
          <div className="text-xs font-mono text-slate-400 uppercase tracking-wider mb-2">
            Subsystem Diagnostics
          </div>
          {readiness?.checks ? (
            <div className="space-y-1.5 text-xs font-mono">
              {Object.entries(readiness.checks).map(([key, val]) => (
                <div key={key} className="flex justify-between items-center text-slate-300">
                  <span className="capitalize">{key.replace("_", " ")}:</span>
                  <span
                    className={`px-1.5 py-0.5 rounded text-[10px] ${
                      val === "ready"
                        ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                        : "bg-amber-500/10 text-amber-300 border border-amber-500/20"
                    }`}
                  >
                    {val}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-500">
              {error ? "Backend offline. Run: uvicorn app.main:app" : "Reading diagnostic map..."}
            </p>
          )}
        </div>
      </div>

      {error && (
        <div className="mt-4 p-3 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs flex items-start space-x-2">
          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold">Backend Connection Notice: </span>
            <span>{error}</span>
          </div>
        </div>
      )}
    </div>
  );
}
