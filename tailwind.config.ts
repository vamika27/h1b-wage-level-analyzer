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
          "var(--font-fraunces)",
          "Fraunces",
          "Georgia",
          "serif"
        ]
      },
      colors: {
        ink: "#2B2520",
        charcoal: "#E7DED0",
        slate: "#D4C8B8",
        cream: "#F0EBE3",
        creamSoft: "#F8F3EB",
        gold: "#B98590",
        amberSoft: "#C98E96",
        sage: "#7C8C6F",
        sageSoft: "#8A9A7E",
        parchment: "#2B2520"
      },
      boxShadow: {
        glow: "0 22px 70px rgba(43, 37, 32, 0.08)",
        card: "0 22px 60px rgba(43, 37, 32, 0.1)"
      },
      backgroundImage: {
        "warm-wash":
          "linear-gradient(135deg, rgba(248, 243, 235, 0.9), rgba(240, 235, 227, 0.32))"
      }
    }
  },
  plugins: []
};

export default config;
