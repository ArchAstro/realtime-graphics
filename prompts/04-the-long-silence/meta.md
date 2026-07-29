# The Long Silence — procedural space exploration

**Why it's here:** Full space game (flight, land, scan, fold drive, star map) with photoreal aspirations, browser verification tools, and an explicit adversarial judge against Starfield. Prompt + process fully published by Anshu (`@anshuc`).

| Field | Value |
|-------|-------|
| Author | Anshu (`@anshuc` / GitHub `achimala`) |
| Model | Claude Opus 5 (+ Blender MCP skill for hard-surface assets) |
| Stack | Three.js, WebGL2, hand-written GLSL, Vite |
| Demo | https://longsilence.anshu.dev |
| Repo | https://github.com/achimala/TheLongSilence |
| X writeup | https://x.com/anshuc/status/2081801979131818412 |

## Prompts

1. [`prompt-initial.md`](./prompt-initial.md) — empty-repo first build (high effort)
2. [`prompt-visual-goal.md`](./prompt-visual-goal.md) — overnight `/goal` visual overhaul with impartial judge

## Process notes (from author)

- Adversarial subagent critique vs AAA space games (pattern from Claude of Duty)
- Blender MCP so Claude models its own assets → skill `blender-hardsurface`
- Judge never allowed to be relaxed; Claude did not finish the goal (kept iterating overnight until manually stopped)
