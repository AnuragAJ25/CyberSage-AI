"use client";

import React from "react";
import { ShieldCheck, Terminal, Cpu } from "lucide-react";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-cyber-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 shadow-sm shadow-cyan-500/20">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                CyberSage AI
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">
                Phase 1 Foundation
              </span>
            </div>
            <p className="text-xs text-slate-400">CyberForge AI & Cybersecurity Hackathon</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="hidden sm:flex items-center space-x-2 text-xs font-mono text-slate-400 border border-slate-800 px-3 py-1.5 rounded-md bg-cyber-900">
            <Cpu className="w-3.5 h-3.5 text-cyan-400" />
            <span>Team: Crazy Champions</span>
          </div>
          <a
            href="https://github.com/AnuragAJ25/CyberSage-AI"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-2 text-xs font-mono px-3 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 transition border border-slate-700"
          >
            <Terminal className="w-3.5 h-3.5 text-slate-400" />
            <span>GitHub Repository</span>
          </a>
        </div>
      </div>
    </header>
  );
}
