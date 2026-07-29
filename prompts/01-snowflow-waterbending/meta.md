# SNOWFLOW — Waterbending / snow tech demo

**Why it's here:** Best-in-class public example of AI-built *realtime graphics* with a full shared implementation brief. Persistent terrain deformation, five water spells, snow-surf wake, procedural character + cloth, atmosphere, TAA/bloom/SSR — all WebGPU, no art assets.

| Field | Value |
|-------|-------|
| Author | Maksymilian Dendura (GitHub `Noniv`, Reddit `u/Any-Reputation8118`) |
| Model | Claude Code + Opus 5 |
| Stack | WebGPU, Babylon.js, hand-written WGSL, Vite |
| Effort | ~9 hours, ~4M tokens (excl. cache) |
| Demo | https://snowflow-lilac.vercel.app/ |
| Repo | https://github.com/Noniv/snowflow_demo |
| Reddit | https://www.reddit.com/r/ClaudeAI/comments/1v94nal/people_liked_my_desert_so_heres_a_waterbending/ |
| Perf | ~3.22 ms GPU frame @ 2560×1440 on RTX 5070 Ti |

## Controls

- WASD move · mouse look · Shift sprint
- **1–5** spells · **RMB** snow-surf · **F1** / `` ` `` settings

## Prompt

See [`prompt.md`](./prompt.md) — the full *SNOWFLOW — Tech Demo · Implementation Brief* shared under Reddit spoilers. Author notes: this prompt created the base; many follow-up prompts guided milestones.

## What makes the prompt special

- Opens with a non-negotiable visual prime directive
- Specs systems at graphics-engineer depth (clipmap, multi-scale snow SSS, toroidal deformation RT, PCSS cascades, pipeline warm-up)
- Milestone gates with screenshot acceptance criteria
- Explicit GC / allocation bans for the render loop
- Authorizes cutting features that don't "pay for their pixels"
