import React from "react";
import { AbsoluteFill, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { Scene, WordReveal } from "../components";
import { clamp, theme } from "../theme";

const Embers: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  return (
    <AbsoluteFill>
      {Array.from({ length: 70 }).map((_, i) => {
        const x = random(`x${i}`) * 1920;
        const speed = 40 + random(`s${i}`) * 90;
        const start = random(`t${i}`) * fps * 2;
        const t = Math.max(0, frame - start) / fps;
        const y = height + 40 - t * speed;
        const size = 2 + random(`r${i}`) * 5;
        const o = interpolate(frame - start, [0, fps * 0.5], [0, 0.4 + random(`o${i}`) * 0.5], clamp);
        return (
          <div
            key={i}
            style={{
              position: "absolute", left: x + Math.sin((frame + i * 10) / 18) * 12, top: y,
              width: size, height: size, borderRadius: "50%",
              background: theme.colors.accent, opacity: o,
              boxShadow: `0 0 ${size * 3}px ${theme.colors.glow}`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

export const Hook: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <Scene>
      <Embers />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "column", gap: 28 }}>
        <WordReveal
          text="Borneo burns every year."
          delay={Math.round(fps * 0.2)}
          highlight="burns"
          style={{ fontFamily: theme.fonts.display, fontWeight: 700, fontSize: 120, color: theme.colors.text }}
        />
        <WordReveal
          text="But the satellite record disagrees with itself."
          delay={Math.round(fps * 1.6)}
          per={2}
          gap={14}
          style={{ fontFamily: theme.fonts.body, fontSize: 46, color: theme.colors.textDim }}
        />
      </AbsoluteFill>
    </Scene>
  );
};
