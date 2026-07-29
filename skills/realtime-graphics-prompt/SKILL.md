---
name: realtime-graphics-prompt
description: >
  Generate a one-shot implementation prompt for an amazing-looking browser game
  or realtime graphics simulation, synthesizing best practices from researched
  demos (SNOWFLOW, Claude of Duty, Long Silence, Solebound, etc.) and techniques
  (clipmap, deformation buffers, SSS, post stack, adversarial critics). Use when
  the user wants a vibe-code / one-shot game prompt, a graphics tech-demo brief,
  “prompt for Claude/Codex to build a game”, /realtime-graphics-prompt, or to
  distill the archive into a new prompt.
---

# Realtime graphics one-shot prompt generator

Your job is to **emit a ready-to-paste implementation brief** that maximizes
the chance a coding agent one-shots something that looks and plays like the
viral AI realtime demos (SNOWFLOW, Claude of Duty, Long Silence…)—not a grey
box MVP.

This skill ships with a self-contained playbook. When the user is also inside
the **realtime-graphics-prompts** archive repo, optionally deepen from local
sources (see below).

## When invoked

1. **Read the playbook (required)** — path relative to this skill:
   ```
   references/playbook.md
   ```
   (Installed copy lives next to this `SKILL.md`.)

2. **If** the working tree is the archive repo (has `prompts/` + `techniques/catalog.json`),
   optionally skim concept-relevant sources (do not dump them into chat):
   - `techniques/catalog.json` — technique ↔ prompt map
   - `prompts/*/meta.md` — stack, why it worked
   - `prompts/01-snowflow-waterbending/prompt.md` — gold-standard brief
   - `prompts/03-claude-of-duty/prompt.md` — adversarial critic
   - `prompts/04-the-long-silence/prompt-initial.md` + `prompt-visual-goal.md`

3. Gather intent (ask only what’s missing; default aggressively):
   - **Concept** — what is it? (required)
   - **Fantasy** — what does the player do for 60–90 seconds?
   - **Reference bar** — AAA/game/photo to beat (default from concept)
   - **Stack** — default Three.js + WebGPU if available else WebGL2 + Vite; procedural only
   - **Form** — tech demo vs full game loop
   - **Effort** — `brief` (systems-heavy, SNOWFLOW-class) vs `loop` (shorter + adversarial) vs `hybrid` (default)

If the user only gives a one-liner (“waterbending desert”, “space freighter”,
“destructible city”), invent a sharp fantasy + reference and proceed. Do not
interview them for ten turns.

## How to design the prompt

### A. Choose the spine

| User wants… | Spine |
|-------------|--------|
| Graphics tech demo, one place, interactive world | SNOWFLOW **implementation brief** |
| Full game loop, AAA look | Long Silence **empty-repo AAA** + CoD **critic loop** |
| Weird polished sim / toy | Solebound **max effort** + brief systems for the hero mechanic |
| Default | **Hybrid**: prime directive + locked stack + deep systems for 2–4 hero features + adversarial critic + milestones |

### B. Select techniques

From the concept, pick **only** techniques that pay for pixels. Spec them at
**engineer depth** (buffers, failure modes, shared includes)—not buzzword lists.

Use the playbook tables. Always include unless the concept forbids them:

1. Prime directive + placeholder = defect  
2. Frame budget + zero alloc + pipeline prewarm  
3. Analytic or coherent lighting + post/tonemap discipline  
4. Adversarial screenshot critic vs named reference  
5. Milestone hard gates  

### C. Write the prompt in this exact section order

Emit **one fenced markdown block** the user can copy into Claude Code / Codex / Cursor.

```markdown
# <TITLE> — Implementation Brief

You are the sole engineer and technical artist on a realtime <game|tech demo>.
Build it end to end. This document is the spec, the art direction, and the acceptance criteria.

## 0. Player fantasy (60–90 seconds)
<What they do. What they feel. What “close the tab” looks like if it fails.>

## 1. Prime directive
Visual quality is the product. …
- Beauty overrides conflicting requirements; log deviations in DECISIONS.md
- Low-poly / flat / untextured / placeholder / “indie prototype” = defect
- Do not stop at “it works.” Stop when every captured frame looks polished and cohesive.
- Named bar: <AAA or photo reference>. Side-by-side blind comparison required.

## 2. Stack and hard constraints
- Language / engine / bundler
- Target machine, resolution, 60 FPS floor / 90 target / report 1% lows
- No external art (except engine). Procedural meshes, materials, audio.
- Zero allocations in the render loop. Pipeline prewarm before dismiss loading.
- If navigator.gpu missing: <one line and stop | WebGL2 path — pick one>

## 3. Systems
### 3.1 Environment
<clipmap / bake / floating origin / wind noise — only if needed, with failure modes>

### 3.2 Hero interactive system
<deformation buffer / combat / flight / repair — shared world state if applicable>

### 3.3 Materials and lighting
<multi-scale, SSS, analytic sky, PCSS, etc.>

### 3.4 Character / props (if any)
<procedural / SDF blend-shell / cloth-hide cheap body>

### 3.5 Post-processing
Order: … Tonemap: AgX or ACES. Failure mode: clipped whites / plastic PBR.

## 4. Gameplay / interaction
<controls, core loop if any; show-don’t-tell; no tutorial spam>

## 5. Performance
Budget table, GC ban, pools, overlay with per-system toggles and 1% lows.

## 6. Milestones (hard gates — screenshot each)
1. …
Do not advance while ugly. Milestone 2 (environment only) is a hard visual gate.

## 7. Adversarial verification
- Independent judge subagent (or second pass) compares screenshots to <reference>
- Cannot relax the judge prompt
- /loop (or equivalent) until judge is wowed or scores honestly and you keep improving the lowest categories
- Verify in real browser at target FPS; first use of every ability must not hitch

## 8. Working agreement
Build. Screenshot. Look. Tune. Replace failing techniques. Ship something worth recording.
```

Fill every section with **concrete** numbers and failure modes. Steal phrasing
from the playbook’s “prompt match phrases” where it fits.

### D. Length guidance

- **Hybrid / brief:** ~1.5–4k words is fine (SNOWFLOW-class). Prefer depth on
  hero systems over listing 20 features.
- **Loop-only:** 400–800 words if user wants something short like CoD’s
  orchestrator—but still include prime directive, stack, critic, FPS.

## Deliverable format (your response to the user)

1. **One-line thesis** — what you’re aiming at and which archive patterns you fused  
2. **Assumptions** — stack, reference, form (bullet list, short)  
3. **The prompt** — single copy-paste fenced block (complete; no “TBD”)  
4. **How to run it** — e.g. empty repo + Claude Code / Codex, ultrathink/ultracode if relevant, screenshot loop  
5. **Optional follow-ups** — 2–4 milestone feedback prompts if the one-shot stalls  
6. **Technique map** — which techniques to study (playbook names; if in archive repo, link `techniques/demos/…`)

Do **not** implement the game unless asked. Do **not** only link to archive
pages—emit the actual prompt text.

## Quality bar for your output

Reject your own prompt if it:

- Lacks a 60–90s fantasy or named quality bar  
- Says “cool shaders” without buffer/failure-mode detail on the hero system  
- Omits FPS / allocation / prewarm  
- Omits adversarial or screenshot verification  
- Allows placeholder art to ship  

Before sending, re-read against `references/playbook.md` checklist at the bottom.

## Examples of good fusion

**User:** “sand mage that digs dunes”

→ Hybrid of desert + SNOWFLOW: clipmap + wind noise + deformation with berms +
wrap sand SSS + 5 sand abilities writing one buffer + critic vs Journey/Dune
stills + 90 FPS brief.

**User:** “one shot a CoD-like”

→ CoD orchestrator critic loop + architecture ownership note + procedural
materials + post stack + honest 1% lows + Three.js.

**User:** “cozy shoe shop”

→ Solebound max-effort tone + procedural PBR leather + world-space tools +
GPU mask state + short fantasy “12 days, 12 pairs”.
