import type { Metadata } from "next";
import { Fraunces, Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap"
});

const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-fraunces",
  display: "swap"
});

export const metadata: Metadata = {
  title: "H-1B Wage Level Analyzer",
  description:
    "A data dashboard analyzing FY2024 H-1B wage classification patterns across major U.S. companies and tech occupations.",
  icons: {
    icon: "/logo.png",
    shortcut: "/logo.png",
    apple: "/logo.png"
  },
  openGraph: {
    title: "H-1B Wage Level Analyzer",
    description:
      "An analysis of 560,000+ federal H-1B visa records across Fortune 500 companies.",
    type: "website"
  }
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${fraunces.variable}`}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
