import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Entrance, Eyebrow, Scene, WordReveal } from "../components";
import { theme } from "../theme";

const SensorBar: React.FC<{
  label: string; years: string; ratio: number; color: string; delay: number; value: string;
}> = ({ label, years, ratio, color, delay, value }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: theme.spring.smooth });
  const maxH = 520;
  return (
    <Entrance delay={delay} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 20, width: 300 }}>
      <div style={{ fontFamily: theme.fonts.display, fontSize: 64, fontWeight: 700, color, fontVariantNumeric: "tabular-nums" }}>
        {value}
      </div>
      <div style={{ height: maxH, display: "flex", alignItems: "flex-end" }}>
        <div
          style={{
            width: 160, height: maxH * ratio * p, borderRadius: 18,
            background: `linear-gradient(180deg, ${color}, ${color}55)`,
            boxShadow: `0 0 60px ${color}44`,
          }}
        />
      </div>
      <div style={{ fontFamily: theme.fonts.display, fontSize: 44, fontWeight: 700, color: theme.colors.text }}>{label}</div>
      <div style={{ fontFamily: theme.fonts.mono, fontSize: 24, color: theme.colors.textDim }}>{years}</div>
    </Entrance>
  );
};

export const Problem: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = interpolate(
    spring({ frame: frame - fps * 1.6, fps, config: theme.spring.counter }),
    [0, 1], [1, 4.2],
  );
  return (
    <Scene hue={theme.colors.cool}>
      <AbsoluteFill style={{ flexDirection: "row", alignItems: "center", padding: "0 160px", gap: 120 }}>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 30 }}>
          <Entrance delay={4}>
            <Eyebrow>Same fires · two sensors</Eyebrow>
          </Entrance>
          <WordReveal
            text="VIIRS sees 4.2× more hotspots than MODIS."
            delay={10}
            highlight="4.2×"
            style={{
              justifyContent: "flex-start", fontFamily: theme.fonts.display, fontWeight: 700,
              fontSize: 84, lineHeight: 1.05, color: theme.colors.text,
            }}
          />
          <Entrance delay={Math.round(fps * 2.4)}>
            <div style={{ fontFamily: theme.fonts.body, fontSize: 36, color: theme.colors.textDim, lineHeight: 1.4, maxWidth: 760 }}>
              Stitch them together naively and 2012 looks like the year fires exploded.
            </div>
          </Entrance>
        </div>
        <div style={{ display: "flex", gap: 40, alignItems: "flex-end" }}>
          <SensorBar label="MODIS" years="2002 →" ratio={1 / 4.2} color={theme.colors.cool} delay={Math.round(fps * 0.8)} value="1×" />
          <SensorBar
            label="VIIRS" years="2012 →" ratio={1} color={theme.colors.primary}
            delay={Math.round(fps * 1.2)} value={`${k.toFixed(1)}×`}
          />
        </div>
      </AbsoluteFill>
    </Scene>
  );
};
