# Desert explorer / sand mage (precursor to SNOWFLOW)

**Why it's here:** Same author as SNOWFLOW; the viral desert demo that preceded the snow/waterbending work. GPU clipmap dunes, permanent sand deformation, cloth robe, six sand spells, physically based sky. Direct lineage for the snow brief.

| Field | Value |
|-------|-------|
| Author | `u/Any-Reputation8118` / Noniv |
| Model | Claude Code + Opus 5 |
| Stack | WebGPU, Three.js, TSL shaders, compute kernels |
| Effort | ~14 hours, ~5M tokens (per OP comments) |
| Demo | https://desert-dusky.vercel.app/ |
| Reddit | https://www.reddit.com/r/ClaudeAI/comments/1v7h5e3/i_built_a_procedural_desert_explorer_with_claude/ |
| Perf | ~160 FPS @ 1440p on RTX 5070 Ti |

## Controls

WASD · 1–5 + RMB cast · F3 perf · F1 settings

## Prompt status

**Author did not save the original prompt** (stated in comments: "Sadly I did not save it… original prompt was like 20% of the result, then I was working with Claude incrementally").

See [`notes.md`](./notes.md) for process reconstruction and a **prompt seed** inferred from OP's public description + the later SNOWFLOW brief (which *is* fully preserved).

## Workflow that mattered

> "giving Claude its own instruments: a headless-Chrome harness that boots the app, screenshots it and reports per-subsystem GPU cost, so changes were made against measured numbers."
