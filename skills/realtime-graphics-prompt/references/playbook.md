# Realtime graphics prompt playbook

Distilled from the viral demos archived in this repo (`prompts/`, `techniques/`). Use when assembling a one-shot implementation brief.

## Prompt archetypes that actually shipped quality

| Archetype | Source | Strength | Weakness |
|-----------|--------|----------|----------|
| **Implementation brief** | SNOWFLOW | Systems-depth graphics + milestones + perf | Long; needs follow-ups for polish |
| **Adversarial quality loop** | Claude of Duty, Long Silence `/goal` | Forces visual iteration with harsh critic | Can thrash without architecture ownership |
| **AAA bar + empty repo** | Long Silence initial | Strong aesthetic non-negotiables + verify in browser | Underspecifies systems |
| **Short max-effort** | Solebound | Surprising depth from “show me your best” | Unpredictable scope |
| **Domain process sim** | Tower crane, Panama locks | Clear agent + process + deliverable | Not a full game |
| **Novel tech-art style** | SDF blend-shell creatures | One crisp aesthetic thesis | Narrow |

Best one-shots **combine**: brief-level systems for the 1–3 features that sell the shot + adversarial critic + hard FPS budget + procedural art.

## Non-negotiable prompt sections (ordered)

### 0. Role + product definition
- “Sole engineer and technical artist”
- One sentence: what the player does for 60–90 seconds
- Judgment: “AAA or close the tab” / named reference (CoD, Starfield, Journey…)

### 1. Prime directive
Copy the SNOWFLOW pattern:
- Visual quality is the product
- Beauty overrides conflicting requirements (log deviations)
- Placeholder / low-poly / flat / untextured = **defect**, not MVP
- Stop when frames look finished, not when features compile

### 2. Stack + hard constraints
Always lock:
- Language + engine (Three.js WebGPU/TSL, Babylon WebGPU, raw WebGL2…)
- “No external art assets” (or list allowed CDN: three only)
- Target device + resolution + **frame budget** (e.g. 60 FPS floor, 90 target, 1% lows)
- No mobile / no fallback if that matches the reference demos
- Zero allocations in the render loop

### 3. Systems that sell the screenshot
Pick only systems that **pay for pixels** for this concept:

| If the concept needs… | Spec this (from techniques) |
|----------------------|------------------------------|
| Endless / large ground | Geometry clipmap, VS displacement, wind-layered noise |
| Player leaves marks | Persistent deformation RT + depression **and** berm mass + shared `brush()` |
| Material “reads as substance” | Multi-scale normals, wrap+SSS, surface state channels |
| Fluid / spell / wake body | Swept mesh along spine, not particle mush |
| Characters from AI | SDF blend-shell or fully procedural cloth-hidden body |
| Planetary / huge scale | Floating origin + log depth; bake planets |
| Atmosphere / time of day | Analytic sky tied to sun elevation |
| AAA polish pass | Post chain + tonemap discipline (no clipped white) |
| Zero art budget | Procedural PBR forge |

### 4. Shared world state
When interactive FX exist: **one** terrain/state buffer that feet, tools, and abilities all write. “Effects floating above the world” is an explicit failure.

### 5. Performance engineering
- Pre-allocate; ban `new` / map / filter in hot loops
- **Pipeline prewarm** before first interaction
- Measure **1% low / p99**, not average FPS alone
- Budget ms per system; ship overlay with toggles

### 6. Verification / adversarial loop
From Claude of Duty + Long Silence:
- Screenshot at every milestone
- Independent harsh critic compares to **named AAA reference**
- Blind A/B preference; cannot relax the judge
- Loop until critic is wowed **or** you hit an honest score ceiling and document it
- Browser verify end-to-end at target FPS

### 7. Milestones with hard gates
Example gates (adapt):
1. Boot + camera + frame graph
2. Environment still looks production-ready **with no character**
3. Interaction / deformation integrates with lighting/shadows
4. Hero mechanic (surf, shoot, fold, repair…)
5. Post + tonemap calibration
6. Perf hardening + prewarm

Do not advance past an ugly milestone.

### 8. Working agreement
- Build, screenshot, look, iterate (parameter tuning is most of the quality gap)
- Replace techniques that fail; don’t patch forever
- `DECISIONS.md` / `PERF.md` for deviations and budgets

## Prompt match phrases (paste into systems)

These phrases from the archive reliably steer models:

- “Visual quality is the product”
- “Anything that reads as low-poly, flat-shaded, untextured, or placeholder is a defect”
- “If a requirement conflicts with beauty, break the requirement”
- “One static mesh, one draw call” (clipmap)
- “Do not use a single fBm stack”
- “Displaced mass — do not skip this”
- “A trail that does not self-shadow is a failure”
- “This single term does more for reads-as-snow than almost anything else” (SSS)
- “Wake is a swept mesh, not a particle effect”
- “Planets are baked, not evaluated”
- “Blown-out white is the primary failure mode”
- “Zero allocations in the render loop”
- “First cast of any ability must not compile a pipeline mid-frame”
- “Side-by-side blind comparison with [AAA reference]”
- “You cannot mark done until the judge says it looks as good”

## Anti-patterns (ban these in the prompt)

- “Make it cool” without a named bar or 90-second player fantasy
- Feature laundry list with no visual prime directive
- Allowing stock white PBR materials as the final look
- Particle-only versions of coherent bodies (water, snow wake, cloth)
- Average FPS only
- “Mobile + desktop + WebGL fallback” on a quality-first tech demo
- Parallel agents owning coupled lighting/tonemap without a single owner (CoD lesson: sequential ownership of coupled systems wins)

## Stack defaults for this repo’s era

Prefer (unless user overrides):
- **Browser tech demo / game:** Three.js latest + WebGPU when possible, else WebGL2; Vite; procedural everything
- **Graphics-first snow/sand/water:** Babylon.js WebGPU + hand WGSL (SNOWFLOW class)
- **FPS / multi-system game:** Three.js + custom subsystems + screenshot harness
- **Always:** no runtime asset CDN except the engine itself

## Output checklist for the assembled prompt

- [ ] 60–90s player fantasy sentence
- [ ] Named AAA / photo quality bar
- [ ] Prime directive + defect definition
- [ ] Locked stack + FPS budget
- [ ] 1–5 systems specified at engineer depth (not buzzwords)
- [ ] Shared state / brush path if interactive world
- [ ] Post + lighting failure modes called out
- [ ] Adversarial visual critic + screenshot loop
- [ ] Milestone gates
- [ ] Perf / allocation / prewarm rules
- [ ] Explicit “do not stop at it works”
