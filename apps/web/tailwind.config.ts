import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        cyber: {
          950: "#070b14",
          900: "#0c1322",
          850: "#111b30",
          800: "#182542",
          700: "#22355d",
          600: "#324d84",
          accent: "#00f0ff",
          success: "#10b981",
          warning: "#f59e0b",
          danger: "#ef4444",
        },
      },
    },
  },
  plugins: [],
};

export default config;
