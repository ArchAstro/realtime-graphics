# Claude of Duty — browser FPS

**Why it's here:** Extreme end of "single orchestrator prompt → multi-agent fleet builds a full FPS." ~55k lines, 11 subsystems, zero art assets, adversarial visual critics comparing to Call of Duty. Honest about not hitting the AAA bar (critics ~5/10) while still being one of the strongest autonomous game-engineering demos.

| Field | Value |
|-------|-------|
| Author | Matt Shumer (`@mattshumer_`) |
| Model | Claude Opus 5 + multi-agent orchestration |
| Stack | Three.js r180, WebGL2, Vite; custom physics (no Rapier) |
| Demo | https://pages.workbench.md/p/pg_lzr8fzlTfUfh |
| Repo | https://github.com/mshumer/Claude-of-Duty |
| Prompt file in repo | `prompt.md` (copied here) |

## Prompt

See [`prompt.md`](./prompt.md).

## Pattern

Short **quality-obsessed** orchestrator prompt: fan out sub-agents, `/loop`, harsh visual critic that does blind side-by-side vs real CoD, don't stop until critic is wowed. The architecture contract lived separately in `ARCHITECTURE.md` during the build.
