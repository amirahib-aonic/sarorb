import React from "react";
import { Composition, Series } from "remotion";
import { theme } from "./theme";
import { Hook } from "./scenes/Hook";
import { Problem } from "./scenes/Problem";
import { Solution } from "./scenes/Solution";
import { Proof } from "./scenes/Proof";
import { Close } from "./scenes/Close";

const FPS = 30;
const s = theme.scenes;
const SCENES = [
  { C: Hook, sec: s.hook },
  { C: Problem, sec: s.problem },
  { C: Solution, sec: s.solution },
  { C: Proof, sec: s.proof },
  { C: Close, sec: s.close },
];

const IgnisDemo: React.FC = () => (
  <Series>
    {SCENES.map(({ C, sec }, i) => (
      <Series.Sequence key={i} durationInFrames={sec * FPS}>
        <C />
      </Series.Sequence>
    ))}
  </Series>
);

export const RemotionRoot: React.FC = () => (
  <Composition
    id="IgnisDemo"
    component={IgnisDemo}
    durationInFrames={SCENES.reduce((t, { sec }) => t + sec * FPS, 0)}
    fps={FPS}
    width={1920}
    height={1080}
  />
);
