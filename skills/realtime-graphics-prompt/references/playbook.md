# Realtime graphics prompt playbook

Distilled from the viral demos archived in this repo (`prompts/`, `techniques/`). Use when assembling a one-shot implementation brief.

## Rule zero: the brief you emit stands alone

This file is scaffolding. It does not ship. The emitted prompt must never name this playbook, the archive, this skill, or any source demo — the receiving agent cannot open them, so a reference is dead weight at best and a hallucination hook at worst.

Consequences for everything below:

- **Techniques are conclusions, not citations.** "Use a persistent deformation buffer" must arrive in the brief as *why this concept needs one* — what the cheaper alternative cannot represent — never as "this worked in a snow demo."
- **Numbers carry derivations.** A grid size, FPS floor, substep count, or radius with no stated reason is a number the agent will change arbitrarily under pressure. Give it the reason and it changes it correctly.
- **Negative specs name the alternative and its specific failure.** "Not a heightfield" is taste. "Not a heightfield — it cannot represent a hole with a lip, so nothing can be buried" is an argument.
- **Phrases below are patterns, not text.** Re-derive each for the concept at hand (see § Steering patterns).

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
- Judgment: “this is finished, or close the tab”
- A **derived standard**, not a title — see § Deriving the standard below

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

### 2.5 Deriving the standard

Naming a game or film compresses to "make it good," because the agent cannot open the reference and the judge cannot score it. Convert the bar into **8–12 numbered, falsifiable properties.** Prefer in order:

1. **The physical referent**, when the subject exists in reality — sand, water, snow, leather, gravel, metal, skin, foliage. Anchor to macro photography of the actual substance and enumerate what such a photograph contains.
2. **The physical process**, for anything that moves — the equilibrium it returns to, how collapse looks versus the wrong-looking alternative, fast versus slow contact, what must be *perfectly still* when nothing acts on it. Motion properties are the ones nobody writes down, and where "reads as simulated" usually leaks in.
3. **A named work**, only with no physical referent (space opera, abstract, stylised-by-intent) — and then decomposed immediately into palette relationships, contrast structure, silhouette language, and what the lighting refuses to do.

Property checklist — each must be:
- verifiable from a still frame or short capture ("the interstitial gaps are the darkest value in frame" ✓ / "feels premium" ✗)
- written as a requirement, not an aspiration
- scored **individually** by the §6 judge — a numbered list produces actionable deltas, a movie title produces adjectives

Typical look axes: element scale and whether elements are individually resolvable · the light-transport term that defines the substance · hue/roughness variance within one nominal colour · where the darkest value sits · highlight size, count, roll-off · scale cues (DOF, aerial perspective, contact-shadow tightness).

Typical motion axes: rest equilibrium · failure/collapse mode · velocity-dependent response · what is exactly static · what must never jitter when idle.

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
- Screenshot at every milestone
- **Numeric acceptance harness** wherever the concept has measurable behaviour — target ranges for equilibrium, conservation, settling, stability, no-hitch — written to a file each run. A number the agent cannot argue with beats any amount of prose about quality.
- Independent harsh critic, given the screenshots and **the numbered property list only**; scores each 1–10 and names the single worst thing in frame
- Cannot relax the judge, soften the property list, or cherry-pick screenshots
- Loop: fix the lowest-scoring property, re-shoot, re-judge — until all score well **or** an honest ceiling is documented
- Browser verify end-to-end at target FPS, on the real target device
- If a non-expert human is the audience: a fresh evaluator with no knowledge of the brief must complete the core action within N seconds with no on-screen text. Fix the product, not the test.

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

## Steering patterns (re-derive — do not paste)

These reliably steer models, but each is welded to the subject it came from. Pasted verbatim into an unrelated brief they read as non-sequitur and expose the brief as assembled rather than reasoned. Keep the *move*, rewrite the *sentence*, attach the reason:

- ✗ “This single term does more for reads-as-snow than almost anything else.”
- ✓ “Of everything in this section, get this term right first: without it you have coloured plastic beads no matter what else you do.”
- ✗ “Blown-out white is the primary failure mode.”
- ✓ “Clipped white on the sparkle grains is the primary tonemapping failure mode, per §1.1 item 5. Never let a glint reach 1.0.”

The patterns:

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
- “Blind comparison against [derived property list], scored item by item”
- “You cannot mark done until the judge scores every property”

## Anti-patterns (ban these in the prompt)

- Any reference to this playbook, the archive, this skill, or a source demo
- A quality bar that is a title instead of a numbered property list
- Numbers with no stated derivation; “do not use X” with no stated failure of X
- Steering phrases still carrying their original subject (“reads as snow” in a brief that has no snow)
- “Make it cool” without a standard or a 90-second player fantasy
- Feature laundry list with no visual prime directive
- Allowing stock white PBR materials as the final look
- Particle-only versions of coherent bodies (water, snow wake, cloth)
- Average FPS only
- “Mobile + desktop + WebGL fallback” on a quality-first tech demo
- Parallel agents owning coupled lighting/tonemap without a single owner — coupled systems need sequential ownership, or each agent tunes against the others' half-finished state

## Stack defaults for this repo’s era

Prefer (unless user overrides):
- **Browser tech demo / game:** Three.js latest + WebGPU when possible, else WebGL2; Vite; procedural everything
- **Graphics-first granular/fluid sim:** Babylon.js WebGPU + hand-written WGSL compute (you need explicit control of atomics, buffer layout, and dispatch order; node-material graphs cannot express a solver)
- **FPS / multi-system game:** Three.js + custom subsystems + screenshot harness
- **Always:** no runtime asset CDN except the engine itself

## Output checklist for the assembled prompt

- [ ] 60–90s player fantasy sentence
- [ ] **8–12 numbered falsifiable properties** as the standard, with the anchor and why it was chosen
- [ ] Prime directive + defect definition
- [ ] Locked stack + FPS budget
- [ ] 1–5 systems specified at engineer depth (not buzzwords)
- [ ] Every non-obvious number states its derivation
- [ ] Every negative spec names the alternative and what it fails to deliver
- [ ] Shared state / brush path if interactive world
- [ ] Post + lighting failure modes called out, as what the user would observe
- [ ] Adversarial visual critic scoring the property list item by item + screenshot loop
- [ ] Numeric acceptance harness if behaviour is measurable
- [ ] Milestone gates, each naming the properties it must satisfy
- [ ] Perf / allocation / prewarm rules
- [ ] **Zero references to this playbook, the archive, this skill, or any source demo**
- [ ] Reads correctly to an agent with no context and no internet
- [ ] Explicit “do not stop at it works”
