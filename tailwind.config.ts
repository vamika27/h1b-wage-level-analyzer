import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-inter)", "Inter", "system-ui", "sans-serif"],
        serif: [
          "var(--font-libre-baskerville)",
          "Libre Baskerville",
          "Georgia",
          "serif"
        ]
      },
      colors: {
        ink: "#111318",
        charcoal: "#171a20",
        slate: "#222731",
        gold: "#d6a84f",
        amberSoft: "#f0c36a",
        parchment: "#f6efe1"
      },
      boxShadow: {
        glow: "0 0 60px rgba(214, 168, 79, 0.12)",
        card: "0 24px 80px rgba(0, 0, 0, 0.32)"
      },
      backgroundImage: {
        "radial-gold":
          "radial-gradient(circle at top right, rgba(214, 168, 79, 0.18), transparent 36rem)",
        "radial-blue":
          "radial-gradient(circle at top left, rgba(84, 110, 150, 0.16), transparent 32rem)"
      }
    }
  },
  plugins: []
};

export default config;
