import React from "react";
import { AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Entrance, Eyebrow, Scene, Spark, WordReveal } from "../components";
import { clamp, theme } from "../theme";

const MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];
const FIRST_YEAR = 2002;
const YEARS = 25;
const SEASON = [0.08, 0.06, 0.1, 0.12, 0.2, 0.35, 0.6, 0.95, 1, 0.55, 0.18, 0.1];
const BIG_YEARS = new Set([2006, 2009, 2015, 2019, 2023]);

const intensity = (year: number, month: number) => {
  const boost = BIG_YEARS.has(year) ? 1 : 0.45;
  return Math.min(1, SEASON[month] * boost * (0.7 + random(`${year}-${month}`) * 0.6));
};

const BurningCalendar: React.FC<{ delay: number }> = ({ delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cell = 22;
  const gap = 4;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      <div style={{ display: "flex", gap, marginLeft: 76 }}>
        {MONTHS.map((m, i) => (
          <div key={i} style={{ width: cell, textAlign: "center", fontFamily: theme.fonts.mono, fontSize: 16, color: theme.colors.textDim }}>
            {m}
          </div>
        ))}
      </div>
      {Array.from({ length: YEARS }).map((_, r) => {
        const year = FIRST_YEAR + r;
        const rowP = spring({ frame: frame - delay - r * 1.5, fps, config: theme.spring.snappy });
        return (
          <div key={r} style={{ display: "flex", gap, alignItems: "center", opacity: rowP }}>
            <div style={{ width: 66, marginRight: 10, textAlign: "right", fontFamily: theme.fonts.mono, fontSize: 15, color: theme.colors.textDim }}>
              {year % 4 === 2 ? year : ""}
            </div>
            {MONTHS.map((_, c) => {
              const v = intensity(year, c);
              const fill = interpolate(frame - delay - r * 1.5 - c, [0, fps * 0.4], [0, 1], { ...clamp, easing: theme.ease.out });
              return (
                <div
                  key={c}
                  style={{
                    width: cell, height: cell, borderRadius: 5,
                    background: theme.colors.bgAlt, border: `1px solid ${theme.colors.line}`,
                    position: "relative", overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      position: "absolute", inset: 0, background: theme.colors.primary,
                      opacity: v * fill, boxShadow: v > 0.7 ? `0 0 14px ${theme.colors.glow}` : undefined,
                    }}
                  />
                </div>
              );
            })}
          </div>
        );
      })}
    </div>
  );
};

export const Solution: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const shift = interpolate(frame, [fps * 2.2, fps * 3.2], [0, 1], { ...clamp, easing: theme.ease.inOut });
  return (
    <Scene>
      <AbsoluteFill style={{ flexDirection: "row", alignItems: "center", padding: "0 150px" }}>
        <div
          style={{
            display: "flex", flexDirection: "column", gap: 34,
            transform: `translateX(${interpolate(shift, [0, 1], [430, 0])}px)`,
            flex: 1,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 40 }}>
            <Spark size={150} delay={4} />
            <WordReveal
              text="IGNIS"
              delay={14}
              style={{
                fontFamily: theme.fonts.display, fontWeight: 700, fontSize: 180,
                letterSpacing: -4, color: theme.colors.text, justifyContent: "flex-start",
              }}
            />
          </div>
          <Entrance delay={26}>
            <Eyebrow>Integrated Geospatial Network for Ignition Surveillance</Eyebrow>
          </Entrance>
          <div style={{ opacity: shift }}>
            <WordReveal
              text="One harmonized fire record for Borneo, 2002 to today."
              delay={Math.round(fps * 3)}
              per={2}
              gap={14}
              style={{
                justifyContent: "flex-start", fontFamily: theme.fonts.body, fontSize: 44,
                lineHeight: 1.3, color: theme.colors.text, maxWidth: 760,
              }}
            />
          </div>
        </div>
        <div style={{ opacity: shift, transform: `translateX(${interpolate(shift, [0, 1], [80, 0])}px)` }}>
          <BurningCalendar delay={Math.round(fps * 2.6)} />
        </div>
      </AbsoluteFill>
    </Scene>
  );
};
