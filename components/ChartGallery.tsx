"use client";

import Image from "next/image";
import { useEffect, useState } from "react";

export type Chart = {
  title: string;
  caption: string;
  src: string;
};

type ChartGalleryProps = {
  charts: Chart[];
};

export function ChartGallery({ charts }: ChartGalleryProps) {
  const [activeChart, setActiveChart] = useState<Chart | null>(null);

  useEffect(() => {
    if (!activeChart) {
      return;
    }

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setActiveChart(null);
      }
    };

    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", onKeyDown);

    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [activeChart]);

  return (
    <>
      <div className="grid gap-6 lg:grid-cols-2">
        {charts.map((chart) => (
          <button
            key={chart.src}
            type="button"
            onClick={() => setActiveChart(chart)}
            className="chart-frame group overflow-hidden rounded-3xl border border-white/10 text-left shadow-card transition duration-300 hover:-translate-y-1 hover:border-gold/50 focus:outline-none focus:ring-2 focus:ring-gold/70"
            aria-label={`Open ${chart.title} chart at full size`}
          >
            <div className="border-b border-white/10 bg-ink/45 p-5">
              <h3 className="font-serif text-2xl text-parchment">{chart.title}</h3>
              <p className="mt-2 text-sm leading-6 text-zinc-300">{chart.caption}</p>
            </div>
            <div className="bg-[#f5f0e8] p-3">
              <Image
                src={chart.src}
                alt={chart.caption}
                width={1400}
                height={875}
                className="aspect-[16/10] w-full rounded-2xl object-contain transition duration-300 group-hover:scale-[1.015]"
              />
            </div>
          </button>
        ))}
      </div>

      {activeChart ? (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-ink/90 p-4 backdrop-blur-md"
          role="dialog"
          aria-modal="true"
          aria-label={`${activeChart.title} full-size chart`}
          onClick={() => setActiveChart(null)}
        >
          <div
            className="max-h-[92vh] w-full max-w-7xl overflow-hidden rounded-3xl border border-gold/30 bg-charcoal shadow-2xl"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="flex items-start justify-between gap-4 border-b border-white/10 p-4 md:p-5">
              <div>
                <h3 className="font-serif text-2xl text-parchment">
                  {activeChart.title}
                </h3>
                <p className="mt-1 text-sm text-zinc-300">{activeChart.caption}</p>
              </div>
              <button
                type="button"
                onClick={() => setActiveChart(null)}
                className="rounded-full border border-white/15 px-4 py-2 text-sm text-zinc-200 transition hover:border-gold/70 hover:text-gold focus:outline-none focus:ring-2 focus:ring-gold/70"
              >
                Close
              </button>
            </div>
            <div className="max-h-[76vh] overflow-auto bg-[#f5f0e8] p-4">
              <Image
                src={activeChart.src}
                alt={activeChart.caption}
                width={1800}
                height={1125}
                className="mx-auto h-auto w-full max-w-none rounded-2xl object-contain"
              />
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
