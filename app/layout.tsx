import type { Metadata } from "next";
import { Inter, Libre_Baskerville } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap"
});

const libreBaskerville = Libre_Baskerville({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-libre-baskerville",
  display: "swap"
});

export const metadata: Metadata = {
  title: "H-1B Wage Level Analyzer",
  description:
    "A data dashboard analyzing FY2024 H-1B wage classification patterns across major U.S. companies and tech occupations.",
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
    <html lang="en" className={`${inter.variable} ${libreBaskerville.variable}`}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
