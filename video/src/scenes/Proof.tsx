import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Entrance, Eyebrow, Scene, WordReveal } from "../components";
import { theme } from "../theme";

const Stat: React.FC<{
  target: number; decimals: number; prefix?: string; suffix?: string; label: string; delay: number; hero?: boolean;
}> = ({ target, decimals, prefix = "", suffix = "", label, delay, hero }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const value = interpolate(spring({ frame: frame - delay, fps, config: theme.spring.counter }), [0, 1], [0, target]);
  const float = Math.sin((frame + delay * 3) / 30) * 3;
  return (
    <Entrance delay={delay} style={{ flex: 1 }}>
      <div
        style={{
          transform: `translateY(${float}px)`,
          padding: "48px 44px", borderRadius: 32, background: `${theme.colors.bgAlt}CC`,
          border: `1px solid ${theme.colors.line}`, boxShadow: "0 40px 80px -20px rgba(0,0,0,0.6)",
          display: "flex", flexDirection: "column", gap: 18,
        }}
      >
        <div
          style={{
            fontFamily: theme.fonts.display, fontWeight: 700, fontSize: 104, lineHeight: 1, whiteSpace: "nowrap",
            color: hero ? theme.colors.primary : theme.colors.text, fontVariantNumeric: "tabular-nums",
          }}
        >
          {prefix}
          {value.toFixed(decimals)}
          {suffix}
        </div>
        <div style={{ fontFamily: theme.fonts.body, fontSize: 30, lineHeight: 1.35, color: theme.colors.textDim }}>{label}</div>
      </div>
    </Entrance>
  );
};

export const Proof: React.FC = () => {
  const { fps } = useVideoConfig();
  const at = (s: number) => Math.round(fps * s);
  return (
    <Scene>
      <AbsoluteFill style={{ justifyContent: "center", padding: "0 150px", gap: 70 }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 22 }}>
          <Entrance delay={4}>
            <Eyebrow>Validated on West Kalimantan · 2012–2026 overlap</Eyebrow>
          </Entrance>
          <WordReveal
            text="Calibrated month by month. Checked year by year."
            delay={10}
            style={{ justifyContent: "flex-start", fontFamily: theme.fonts.display, fontWeight: 700, fontSize: 64, color: theme.colors.text }}
          />
        </div>
        <div style={{ display: "flex", gap: 40 }}>
          <Stat target={0.978} decimals={3} prefix="r = " label="MODIS and VIIRS move together on monthly counts" delay={at(1.2)} />
          <Stat target={12} decimals={0} label="per-month scaling factors keep the fire season's shape" delay={at(1.4)} />
          <Stat target={7.1} decimals={1} suffix="%" label="median error predicting a held-out year" delay={at(1.6)} hero />
        </div>
      </AbsoluteFill>
    </Scene>
  );
};
