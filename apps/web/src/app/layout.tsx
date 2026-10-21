import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CyberSage AI — Security Detection, Analysis & Remediation",
  description:
    "AI-assisted cybersecurity platform orchestrating deterministic scanners, bounded LangGraph reasoning, and verified human-in-the-loop remediations.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-cyber-950 text-slate-100 min-h-screen selection:bg-cyan-500/30 selection:text-cyan-200">
        {children}
      </body>
    </html>
  );
}
