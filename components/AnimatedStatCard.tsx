"use client";

import { useEffect, useRef, useState } from "react";

type AnimatedStatCardProps = {
  value: number;
  prefix?: string;
  suffix?: string;
  label: string;
  detail: string;
  decimals?: number;
};

const easeOutCubic = (progress: number) => 1 - Math.pow(1 - progress, 3);

export function AnimatedStatCard({
  value,
  prefix = "",
  suffix = "",
  label,
  detail,
  decimals = 0
}: AnimatedStatCardProps) {
  const cardRef = useRef<HTMLDivElement | null>(null);
  const [hasEntered, setHasEntered] = useState(false);
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    const card = cardRef.current;
    if (!card) {
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setHasEntered(true);
          observer.disconnect();
        }
      },
      { threshold: 0.35 }
    );

    observer.observe(card);

    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!hasEntered) {
      return;
    }

    let animationFrame = 0;
    const duration = 1300;
    const start = performance.now();

    const tick = (now: number) => {
      const progress = Math.min((now - start) / duration, 1);
      setDisplayValue(value * easeOutCubic(progress));

      if (progress < 1) {
        animationFrame = requestAnimationFrame(tick);
      }
    };

    animationFrame = requestAnimationFrame(tick);

    return () => cancelAnimationFrame(animationFrame);
  }, [hasEntered, value]);

  const formattedValue = displayValue.toLocaleString("en-US", {
    maximumFractionDigits: decimals,
    minimumFractionDigits: decimals
  });

  return (
    <div
      ref={cardRef}
      className={`group rounded-3xl border border-white/10 bg-white/[0.045] p-6 shadow-card backdrop-blur transition duration-700 hover:-translate-y-1 hover:border-gold/45 hover:bg-white/[0.07] ${
        hasEntered ? "translate-y-0 opacity-100" : "translate-y-6 opacity-0"
      }`}
    >
      <div className="mb-5 h-px w-16 bg-gold/70 transition group-hover:w-24" />
      <p className="font-serif text-4xl leading-none tracking-tight text-parchment md:text-5xl">
        {prefix}
        {formattedValue}
        {suffix}
      </p>
      <p className="mt-4 text-sm font-semibold uppercase tracking-[0.24em] text-gold">
        {label}
      </p>
      <p className="mt-3 text-sm leading-6 text-zinc-300">{detail}</p>
    </div>
  );
}
