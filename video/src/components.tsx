import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { clamp, theme } from "./theme";

export const BgMesh: React.FC<{ hue?: string }> = ({ hue = theme.colors.primary }) => {
  const frame = useCurrentFrame();
  const d1 = Math.sin(frame / 55) * 50;
  const d2 = Math.cos(frame / 70) * 40;
  return (
    <AbsoluteFill style={{ background: theme.colors.bg }}>
      <div
        style={{
          position: "absolute", width: 1300, height: 1300, borderRadius: "50%",
          top: -520, left: -320 + d1, filter: "blur(60px)",
          background: `radial-gradient(circle, ${hue}2E, transparent 62%)`,
        }}
      />
      <div
        style={{
          position: "absolute", width: 1000, height: 1000, borderRadius: "50%",
          bottom: -460, right: -260 - d2, filter: "blur(80px)",
          background: `radial-gradient(circle, ${theme.colors.accent}1A, transparent 65%)`,
        }}
      />
    </AbsoluteFill>
  );
};

export const Grade: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <AbsoluteFill style={{ backgroundColor: theme.colors.primary, mixBlendMode: "soft-light", opacity: 0.2 }} />
    <AbsoluteFill
      style={{
        background: "linear-gradient(180deg, rgba(0,0,0,0.18), transparent 28%, transparent 72%, rgba(0,0,0,0.3))",
      }}
    />
  </AbsoluteFill>
);

export const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  const noise = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E")`;
  return (
    <AbsoluteFill
      style={{
        pointerEvents: "none", backgroundImage: noise, backgroundSize: "220px",
        backgroundPosition: `${(frame * 7) % 220}px ${(frame * 13) % 220}px`,
        opacity: 0.07, mixBlendMode: "overlay",
      }}
    />
  );
};

export const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      pointerEvents: "none",
      background: "radial-gradient(ellipse at center, transparent 52%, rgba(0,0,0,0.45) 100%)",
    }}
  />
);

export const Scene: React.FC<{ children: React.ReactNode; hue?: string }> = ({ children, hue }) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();
  const exitStart = durationInFrames - Math.round(fps * 0.4);
  const exitO = interpolate(frame, [exitStart, durationInFrames - 1], [1, 0], clamp);
  const exitY = interpolate(frame, [exitStart, durationInFrames - 1], [0, -42], { ...clamp, easing: theme.ease.in });
  return (
    <AbsoluteFill>
      <BgMesh hue={hue} />
      <AbsoluteFill style={{ opacity: exitO, transform: `translateY(${exitY}px)` }}>{children}</AbsoluteFill>
      <Grade />
      <Grain />
      <Vignette />
    </AbsoluteFill>
  );
};

export const Entrance: React.FC<{ delay?: number; children: React.ReactNode; style?: React.CSSProperties }> = ({
  delay = 0, children, style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: theme.spring.smooth });
  return (
    <div
      style={{
        opacity: p,
        transform: `translateY(${interpolate(p, [0, 1], [40, 0])}px) scale(${interpolate(p, [0, 1], [0.94, 1])})`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

export const WordReveal: React.FC<{
  text: string; delay?: number; per?: number; gap?: number; style?: React.CSSProperties; highlight?: string;
}> = ({ text, delay = 0, per = 3, gap = 22, style, highlight }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap, ...style }}>
      {text.split(" ").map((word, i) => {
        const p = spring({ frame: frame - delay - i * per, fps, config: theme.spring.snappy });
        return (
          <span
            key={i}
            style={{
              display: "inline-block", opacity: p,
              color: word === highlight ? theme.colors.primary : undefined,
              transform: `translateY(${interpolate(p, [0, 1], [30, 0])}px) scale(${interpolate(p, [0, 1], [0.96, 1])})`,
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};

export const Spark: React.FC<{ size: number; delay?: number }> = ({ size, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rays = 12;
  const pop = spring({ frame: frame - delay, fps, config: theme.spring.bouncy });
  const rot = spring({ frame: frame - delay, fps, config: theme.spring.smooth });
  const breathe = 1 + Math.sin(frame / 22) * 0.015;
  return (
    <div
      style={{
        position: "relative", width: size, height: size,
        transform: `scale(${pop * breathe}) rotate(${interpolate(rot, [0, 1], [-120, 0])}deg)`,
        filter: `drop-shadow(0 0 ${size * 0.25}px ${theme.colors.glow})`,
      }}
    >
      {Array.from({ length: rays }).map((_, i) => {
        const p = spring({ frame: frame - delay - i * 1.2, fps, config: theme.spring.snappy });
        return (
          <div
            key={i}
            style={{
              position: "absolute", left: "50%", top: "50%",
              width: size * 0.085, height: size * 0.46 * p,
              background: i % 2 === 0 ? theme.colors.primary : theme.colors.accent,
              borderRadius: size, transformOrigin: "50% 0%",
              transform: `translateX(-50%) rotate(${(360 / rays) * i}deg) translateY(${size * 0.07}px)`,
            }}
          />
        );
      })}
    </div>
  );
};

export const Eyebrow: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      fontFamily: theme.fonts.mono, fontSize: 26, letterSpacing: 6, textTransform: "uppercase",
      color: theme.colors.textDim,
    }}
  >
    {children}
  </div>
);
