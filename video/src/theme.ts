import { Easing } from "remotion";
import { loadFont as loadDisplay } from "@remotion/google-fonts/SpaceGrotesk";
import { loadFont as loadBody } from "@remotion/google-fonts/Inter";
import { loadFont as loadMono } from "@remotion/google-fonts/JetBrainsMono";

const display = loadDisplay("normal", { weights: ["500", "700"], subsets: ["latin"] });
const body = loadBody("normal", { weights: ["400", "500"], subsets: ["latin"] });
const mono = loadMono("normal", { weights: ["500"], subsets: ["latin"] });

export const theme = {
  colors: {
    bg: "#0B0907",
    bgAlt: "#16110D",
    primary: "#FF6A1A",
    accent: "#FFB347",
    cool: "#4FA3FF",
    text: "#F6F1EC",
    textDim: "#A79E95",
    line: "rgba(255,255,255,0.08)",
    glow: "rgba(255, 106, 26, 0.45)",
  },
  fonts: {
    display: display.fontFamily,
    body: body.fontFamily,
    mono: mono.fontFamily,
  },
  ease: {
    out: Easing.bezier(0.16, 1, 0.3, 1),
    inOut: Easing.bezier(0.83, 0, 0.17, 1),
    in: Easing.bezier(0.7, 0, 0.84, 0),
  },
  spring: {
    snappy: { damping: 14, stiffness: 160, mass: 0.6 },
    smooth: { damping: 20, stiffness: 90, mass: 1 },
    bouncy: { damping: 11, stiffness: 170, mass: 0.7 },
    counter: { damping: 30, stiffness: 60, mass: 1 },
  },
  scenes: {
    hook: 4,
    problem: 6,
    solution: 8,
    proof: 7,
    close: 5,
  },
} as const;

export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
