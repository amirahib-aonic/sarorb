import React from "react";
import { AbsoluteFill, useVideoConfig } from "remotion";
import { Entrance, Eyebrow, Scene, Spark, WordReveal } from "../components";
import { theme } from "../theme";

export const Close: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <Scene>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "column", gap: 36 }}>
        <Spark size={190} delay={2} />
        <WordReveal
          text="IGNIS"
          delay={12}
          style={{ fontFamily: theme.fonts.display, fontWeight: 700, fontSize: 150, letterSpacing: -3, color: theme.colors.text }}
        />
        <WordReveal
          text="See when and where Borneo burns."
          delay={Math.round(fps * 0.9)}
          per={2}
          gap={14}
          style={{ fontFamily: theme.fonts.body, fontSize: 48, color: theme.colors.textDim }}
        />
        <Entrance delay={Math.round(fps * 1.6)}>
          <Eyebrow>Sarawak Orbiters · NASA Space Apps 2026</Eyebrow>
        </Entrance>
      </AbsoluteFill>
    </Scene>
  );
};
