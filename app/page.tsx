import Image from "next/image";
import { AnimatedStatCard } from "@/components/AnimatedStatCard";
import { ChartGallery, type Chart } from "@/components/ChartGallery";

const githubUrl = "https://github.com/vamika27/h1b-wage-level-analyzer";

const charts: Chart[] = [
  {
    title: "Figure 1: Top Companies by H-1B Tech Filings",
    caption: "Top 15 companies ranked by total H-1B tech filings in FY2024.",
    src: "/figures/fig1_top_companies.png"
  },
  {
    title: "Figure 2: Wage Level Distribution",
    caption:
      "Prevailing wage level distribution (I-IV) as a percentage of each company's filings.",
    src: "/figures/fig2_wage_level_dist.png"
  },
  {
    title: "Figure 3: Level I & II Wage Share",
    caption:
      "Companies ranked by share of Level I & II wage classifications - higher means more entry-level wage filings.",
    src: "/figures/fig3_level1_share.png"
  },
  {
    title: "Figure 4: Company Wage Gap vs BLS Median",
    caption: "Average offered wage gap vs BLS occupational median by company.",
    src: "/figures/fig4_wage_gap_company.png"
  },
  {
    title: "Figure 5: Offered Wages vs BLS Median",
    caption:
      "Scatterplot of offered wages vs BLS median - points below the line are below the national median.",
    src: "/figures/fig5_scatter_offered_vs_bls.png"
  },
  {
    title: "Figure 6: Wage Gap Heatmap by Occupation",
    caption: "Heatmap of average wage gap by company and occupation.",
    src: "/figures/fig6_heatmap_gap_by_soc.png"
  }
];

const techStack = ["Python", "pandas", "DuckDB", "SQL", "matplotlib", "seaborn"];

const pipelineSteps = [
  "DOL Excel",
  "Python Cleaning",
  "DuckDB SQL",
  "BLS Join",
  "Wage Gap Calc",
  "Visualization"
];

export default function Home() {
  return (
    <main className="min-h-screen overflow-hidden bg-cream text-ink">
      <div className="sticky top-0 z-50 px-4 pt-4 sm:px-6">
        <div className="mx-auto flex max-w-7xl items-center justify-between rounded-full border border-gold/20 bg-gold/[0.09] px-4 py-3 text-xs font-semibold uppercase tracking-[0.22em] text-ink/70 shadow-card backdrop-blur-md transition-shadow duration-300 md:px-5 md:text-sm">
          <a
            href="#top"
            className="flex items-center gap-3 text-gold transition hover:text-amberSoft"
          >
            <span className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate/60 bg-creamSoft p-1 shadow-card">
              <Image
                src="/logo.png"
                alt="H-1B Analyzer logo"
                width={32}
                height={32}
                className="h-8 w-8 rounded-lg object-cover"
                priority
              />
            </span>
            <span>H-1B Analyzer</span>
          </a>
          <nav className="hidden items-center gap-6 md:flex">
            <a className="transition hover:text-gold" href="#findings">
              Findings
            </a>
            <a className="transition hover:text-gold" href="#charts">
              Charts
            </a>
            <a className="transition hover:text-gold" href="#methodology">
              Methodology
            </a>
            <a className="transition hover:text-gold" href="#data">
              Data
            </a>
            <a
              className="rounded-full border border-gold/30 bg-creamSoft/70 px-4 py-2 text-gold transition hover:border-gold/60 hover:text-amberSoft"
              href={githubUrl}
              target="_blank"
              rel="noreferrer"
            >
              Source Code
            </a>
          </nav>
        </div>
      </div>
      <section
        id="top"
        className="relative isolate flex min-h-[calc(100vh-5rem)] items-center px-5 py-10 sm:px-8"
      >
        <div className="absolute inset-0 -z-10 bg-warm-wash" />

        <div className="mx-auto grid w-full max-w-7xl items-center gap-12 lg:grid-cols-[1.12fr_0.88fr]">
          <div>
            <p className="mb-5 inline-flex rounded-full border border-gold/30 bg-gold/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.28em] text-gold">
              FY2024 Federal Visa Records
            </p>
            <h1 className="font-serif text-5xl font-bold leading-[1.03] tracking-tight text-ink sm:text-6xl lg:text-7xl">
              H-1B Wage Level Analyzer
            </h1>
            <p className="mt-7 max-w-3xl text-lg leading-8 text-ink/70 sm:text-xl">
              Do Fortune 500 companies systematically classify tech roles at
              suppressed wage levels? We analyzed 560,000+ federal visa records
              to find out.
            </p>

            <div className="mt-10 flex flex-wrap gap-3 rounded-3xl border border-slate/60 bg-creamSoft/75 p-4 text-sm font-semibold uppercase tracking-[0.16em] text-ink/75 shadow-card backdrop-blur">
              <span className="text-gold">560K+ Records</span>
              <span className="text-sage/70">/</span>
              <span>20+ Companies</span>
              <span className="text-sage/70">/</span>
              <span>8 Tech Occupations</span>
              <span className="text-sage/70">/</span>
              <span>6 SQL Queries</span>
              <span className="text-sage/70">/</span>
              <span>FY2024 DOL Data</span>
            </div>

            <div className="mt-6 flex flex-wrap gap-2">
              {techStack.map((tool) => (
                <span
                  key={tool}
                  className="rounded-full border border-sage/30 bg-sage/10 px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.16em] text-sage"
                >
                  {tool}
                </span>
              ))}
            </div>

            <div className="mt-10 flex flex-wrap gap-4">
              <a
                href="#charts"
                className="rounded-full bg-gold px-6 py-3 text-sm font-bold uppercase tracking-[0.18em] text-creamSoft transition hover:bg-amberSoft"
              >
                View Charts
              </a>
              <a
                href="#methodology"
                className="rounded-full border border-slate/70 px-6 py-3 text-sm font-bold uppercase tracking-[0.18em] text-ink transition hover:border-gold hover:text-gold"
              >
                Methodology
              </a>
              <a
                href={githubUrl}
                target="_blank"
                rel="noreferrer"
                className="rounded-full border border-gold/40 bg-creamSoft/80 px-6 py-3 text-sm font-bold uppercase tracking-[0.18em] text-gold transition hover:border-gold hover:text-amberSoft"
              >
                View Source Code
              </a>
            </div>
          </div>

          <div className="relative">
            <div className="absolute -inset-6 rounded-[2rem] bg-slate/25 blur-2xl" />
            <div className="relative rounded-[2rem] border border-slate/60 bg-creamSoft/85 p-6 shadow-card backdrop-blur">
              <div className="mb-8 flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.24em] text-gold">
                    Analysis Focus
                  </p>
                  <h2 className="mt-2 font-serif text-3xl">Wage Classification</h2>
                </div>
                <div className="h-12 w-12 rounded-full border border-sage/35 bg-sage/10" />
              </div>
              <div className="space-y-5">
                {[
                  ["Applications", "560K+", "Federal LCA records screened"],
                  ["SQL Queries", "6", "Analytical outputs produced with DuckDB"],
                  ["Employers", "20+", "Major company sponsors compared"],
                  ["Occupations", "SOC 15", "Computer & mathematical roles"],
                  ["Benchmarks", "BLS OEWS", "National medians joined by SOC"]
                ].map(([label, value, detail]) => (
                  <div
                    key={label}
                    className="rounded-2xl border border-slate/60 bg-cream/70 p-5"
                  >
                    <div className="flex items-baseline justify-between gap-4">
                      <span className="text-sm uppercase tracking-[0.2em] text-ink/55">
                        {label}
                      </span>
                      <span className="font-serif text-3xl text-sage">{value}</span>
                    </div>
                    <p className="mt-2 text-sm text-ink/70">{detail}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="findings" className="px-5 py-20 sm:px-8">
        <div className="mx-auto max-w-7xl">
          <SectionEyebrow>Key Findings</SectionEyebrow>
          <div className="mt-4 grid gap-6 lg:grid-cols-[0.9fr_1.1fr] lg:items-end">
            <h2 className="font-serif text-4xl font-bold tracking-tight md:text-5xl">
              Four signals from the wage-level analysis.
            </h2>
            <p className="text-lg leading-8 text-ink/70">
              The dashboard highlights filing concentration, entry-level wage
              classification patterns, and how offered wages compare with BLS
              occupational medians for matched tech roles.
            </p>
          </div>
          <div className="mt-12 grid gap-6 sm:grid-cols-2 xl:grid-cols-4">
            <AnimatedStatCard
              value={4188}
              label="Amazon"
              detail="Amazon's H-1B tech filings, most of any company in the FY2024 sample."
            />
            <AnimatedStatCard
              value={93}
              suffix="%"
              label="Wipro"
              detail="Share of Wipro filings classified at Level I or II prevailing wages."
            />
            <AnimatedStatCard
              value={22}
              suffix="% above BLS median"
              label="JPMorgan"
              detail="Offered wages exceeded the BLS occupational median in the matched sample."
            />
            <AnimatedStatCard
              value={560}
              suffix="K+"
              label="Records"
              detail="Total DOL LCA records analyzed before company and occupation cuts."
            />
          </div>
        </div>
      </section>

      <section id="charts" className="px-5 py-20 sm:px-8">
        <div className="mx-auto max-w-7xl">
          <SectionEyebrow>Charts Gallery</SectionEyebrow>
          <div className="mt-4 grid gap-6 lg:grid-cols-[0.95fr_1.05fr] lg:items-end">
            <h2 className="font-serif text-4xl font-bold tracking-tight md:text-5xl">
              Six exported figures from the analysis pipeline.
            </h2>
            <p className="text-lg leading-8 text-ink/70">
              Click any chart to inspect the full-size PNG. The figures are
              served as static assets from the public folder for zero-backend
              deployment.
            </p>
          </div>
          <div className="mt-12">
            <ChartGallery charts={charts} />
          </div>
        </div>
      </section>

      <section id="methodology" className="px-5 py-20 sm:px-8">
        <div className="mx-auto max-w-7xl rounded-[2rem] border border-slate/60 bg-creamSoft/75 p-6 shadow-card backdrop-blur md:p-10">
          <SectionEyebrow>Methodology</SectionEyebrow>
          <div className="mt-4 grid gap-10 lg:grid-cols-[0.85fr_1.15fr]">
            <div>
              <h2 className="font-serif text-4xl font-bold tracking-tight md:text-5xl">
                From federal disclosure files to company-level wage gaps.
              </h2>
              <p className="mt-6 text-lg leading-8 text-ink/70">
                The pipeline begins with DOL LCA disclosure data, cleans the
                records in Python, analyzes employer and wage-level patterns in
                DuckDB SQL, joins BLS OEWS occupational benchmarks, and computes
                offered wage gaps against national medians.
              </p>
              <div className="mt-8 rounded-2xl border border-gold/25 bg-gold/10 p-5">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                  Formula
                </p>
                <code className="mt-3 block overflow-x-auto whitespace-nowrap font-mono text-sm text-ink md:text-base">
                  wage_gap_pct = (offered_wage - bls_median) / bls_median &times; 100
                </code>
              </div>
              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                <div className="rounded-2xl border border-slate/60 bg-cream/75 p-4">
                  <p className="font-serif text-3xl text-sage">560K+</p>
                  <p className="mt-1 text-xs font-semibold uppercase tracking-[0.18em] text-ink/55">
                    Records Processed
                  </p>
                </div>
                <div className="rounded-2xl border border-slate/60 bg-cream/75 p-4">
                  <p className="font-serif text-3xl text-sage">6</p>
                  <p className="mt-1 text-xs font-semibold uppercase tracking-[0.18em] text-ink/55">
                    SQL Query Outputs
                  </p>
                </div>
              </div>
            </div>

            <div className="flex flex-col justify-center">
              {pipelineSteps.map((step, index) => (
                <div key={step} className="relative">
                  <div className="rounded-2xl border border-slate/60 bg-cream/75 p-5">
                    <div className="flex items-center gap-4">
                      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-sage/40 bg-sage/10 font-serif text-lg text-sage">
                        {index + 1}
                      </div>
                      <div>
                        <p className="font-serif text-xl text-ink">{step}</p>
                        <p className="mt-1 text-sm text-ink/65">
                          {getPipelineDetail(step)}
                        </p>
                      </div>
                    </div>
                  </div>
                  {index < pipelineSteps.length - 1 ? (
                    <div className="flex h-7 items-center pl-5 text-sage" aria-hidden="true">
                      &darr;
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section id="data" className="px-5 py-20 sm:px-8">
        <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-2">
          <div className="rounded-[2rem] border border-slate/60 bg-creamSoft/75 p-6 shadow-card md:p-8">
            <SectionEyebrow>Data Sources</SectionEyebrow>
            <h2 className="mt-4 font-serif text-4xl font-bold tracking-tight">
              Public data, reproducible pipeline.
            </h2>
            <div className="mt-8 space-y-4">
              <SourceLink
                href="https://www.dol.gov/agencies/eta/foreign-labor/performance"
                title="DOL OFLC Performance Data"
                description="FY2024 LCA disclosure records with employer, role, wage, and wage-level fields."
              />
              <SourceLink
                href="https://www.bls.gov/oes/special.requests/oesm24nat.zip"
                title="BLS OEWS National Data"
                description="National occupational employment and wage statistics used for median wage benchmarks."
              />
              <SourceLink
                href={githubUrl}
                title="GitHub Repository"
                description="Analysis code, SQL, outputs, and documentation for the H-1B Wage Level Analyzer."
              />
            </div>
            <div className="mt-6 rounded-2xl border border-sage/25 bg-sage/10 p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-sage">
                Wage Gap Formula
              </p>
              <code className="mt-3 block overflow-x-auto whitespace-nowrap font-mono text-sm text-ink md:text-base">
                wage_gap_pct = (offered_wage - bls_median) / bls_median &times; 100
              </code>
            </div>
          </div>

          <div className="rounded-[2rem] border border-gold/25 bg-gold/10 p-6 shadow-card md:p-8">
            <SectionEyebrow>Disclaimer</SectionEyebrow>
            <p className="mt-5 font-serif text-3xl leading-snug text-ink">
              Wage level classifications are lawful.
            </p>
            <p className="mt-6 text-lg leading-8 text-ink/75">
              This analysis is descriptive and does not imply wrongdoing by any
              company. Level I wages are appropriate for genuinely entry-level
              roles.
            </p>
            <div className="gold-rule mt-10 h-px" />
            <p className="mt-8 text-sm uppercase tracking-[0.2em] text-ink/55">
              Scope: 560,000+ FY2024 DOL records, 20+ companies, 8 tech
              occupations
            </p>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate/60 px-5 py-10 sm:px-8">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 text-sm text-ink/60 md:flex-row md:items-center md:justify-between">
          <p>
            Built by <span className="text-ink">Vamika Negi</span> · Data:
            DOL FY2024 · Tools: Python, DuckDB, pandas, matplotlib
          </p>
          <a
            href={githubUrl}
            target="_blank"
            rel="noreferrer"
            className="text-gold transition hover:text-amberSoft"
          >
            GitHub
          </a>
        </div>
      </footer>
    </main>
  );
}

function SectionEyebrow({ children }: { children: React.ReactNode }) {
  return (
    <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">
      {children}
    </p>
  );
}

function SourceLink({
  href,
  title,
  description
}: {
  href: string;
  title: string;
  description: string;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      className="block rounded-2xl border border-slate/60 bg-cream/75 p-5 transition hover:border-gold/45 hover:bg-creamSoft"
    >
      <span className="font-serif text-xl text-ink">{title}</span>
      <span className="mt-2 block text-sm leading-6 text-ink/65">
        {description}
      </span>
    </a>
  );
}

function getPipelineDetail(step: string) {
  const details: Record<string, string> = {
    "DOL Excel": "Raw FY2024 LCA disclosure records from OFLC.",
    "Python Cleaning": "Normalize employer names, SOC codes, wages, and levels.",
    "DuckDB SQL": "Aggregate filings, wage-level shares, and company metrics.",
    "BLS Join": "Attach OEWS national medians by matched occupation.",
    "Wage Gap Calc": "Compare offered wages to occupational median benchmarks.",
    Visualization: "Export six polished figures for the static web gallery."
  };

  return details[step];
}
