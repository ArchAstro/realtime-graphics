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

## Output hygiene: the emitted prompt must stand alone

The archive, this playbook, and the demos it was distilled from are **your**
research material. They are invisible in the deliverable. Non-negotiable:

- **Never name** the archive, this skill, the playbook, SNOWFLOW, Claude of Duty,
  Long Silence, Solebound, or any other source prompt/demo **inside the emitted
  prompt.** Not as attribution, not as "in the style of", not in a comment. The
  receiving agent has no access to any of it, so a reference is dead weight at
  best and a hallucination hook at worst.
- **Every assertion carries its own reason.** The brief must be derivable from
  physics, perception, hardware, and the concept — never from "this worked for
  someone else." If you cannot state why a technique/number/prohibition is right,
  either derive it or cut it.
- **Every non-obvious number carries its derivation inline** — grid size, FPS
  floor, substep count, radius, threshold. `h = 6 mm` is noise; `h = 6 mm, chosen
  so one sim particle equals one 2.35 mm pellet` is a spec the agent can reason
  against when it needs to change it.
- **Every negative spec says why not the cheap alternative.** "Not a heightfield"
  is a taste claim; "not a heightfield — it cannot represent a hole with a lip,
  so nothing can be buried" is an argument that survives contact with a tired
  agent looking for a shortcut.

Provenance belongs in your chat response to the user (§ Deliverable format), not
in the block they paste.

## When invoked

1. **Read the playbook (required)** — path relative to this skill:
   ```
   references/playbook.md
   ```
   (Installed copy lives next to this `SKILL.md`.)

2. **If** the working tree is the archive repo (has `prompts/` + `techniques/catalog.json`),
   optionally skim concept-relevant sources — **internal research only; none of
   these names may appear in the emitted prompt** (do not dump them into chat):
   - `techniques/catalog.json` — technique ↔ prompt map
   - `prompts/*/meta.md` — stack, why it worked
   - `prompts/01-snowflow-waterbending/prompt.md` — gold-standard brief
   - `prompts/03-claude-of-duty/prompt.md` — adversarial critic
   - `prompts/04-the-long-silence/prompt-initial.md` + `prompt-visual-goal.md`

3. Gather intent (ask only what’s missing; default aggressively):
   - **Concept** — what is it? (required)
   - **Fantasy** — what does the player do for 60–90 seconds?
   - **Quality standard** — what the frame must match, expressed as checkable
     properties (see §B; default derived from the concept)
   - **Stack** — default Three.js + WebGPU if available else WebGL2 + Vite; procedural only
   - **Form** — tech demo vs full game loop
   - **Effort** — `brief` (systems-heavy, SNOWFLOW-class) vs `loop` (shorter + adversarial) vs `hybrid` (default)

If the user only gives a one-liner (“waterbending desert”, “space freighter”,
“destructible city”), invent a sharp fantasy + standard and proceed. Do not
interview them for ten turns.

## How to design the prompt

### A. Choose the spine

| User wants… | Spine |
|-------------|--------|
| Graphics tech demo, one place, interactive world | SNOWFLOW **implementation brief** |
| Full game loop, AAA look | Long Silence **empty-repo AAA** + CoD **critic loop** |
| Weird polished sim / toy | Solebound **max effort** + brief systems for the hero mechanic |
| Default | **Hybrid**: prime directive + locked stack + deep systems for 2–4 hero features + adversarial critic + milestones |

### B. Derive the quality standard (do not just name one)

A bare title — “make it look like Journey” — is not a spec. The receiving agent
cannot open the reference, so the title compresses to “make it good,” and it
gives the adversarial judge in §7 nothing to score.

**Convert the bar into a numbered list of checkable properties** the agent can
verify against its own screenshot. Prefer, in order:

1. **The physical referent, when the subject exists in reality** (sand, water,
   litter, leather, snow, metal, skin, foliage, gravel). This is the strongest
   option: the properties are objectively true, the agent already knows them, and
   every one is falsifiable. Anchor to *macro/close photography of the actual
   substance*, then enumerate what such a photograph contains — grain scale,
   translucency, hue variance, where the darkest value sits, highlight size and
   roll-off, depth-of-field behavior.
2. **The physical process, for anything that moves** — how the material actually
   behaves: maximum stable slope, how a wall fails, what fast vs. slow contact
   produces, what is *perfectly still* when nothing is acting on it. Motion
   properties are where "reads as simulated" usually leaks in, and they are
   almost always the ones nobody wrote down.
3. **A named work, only when there is no physical referent** (space opera,
   abstract, stylized-by-intent). Even then, immediately decompose it into
   properties — palette relationships, contrast structure, silhouette language,
   what the lighting refuses to do — so the judge scores properties, not vibes.

Rules:

- Aim for **8–12 numbered properties**, split into look and motion.
- Each must be verifiable from a still frame or a short capture. “Feels premium”
  is not a property. “The interstitial gaps are the darkest value in frame,
  darker than any lit surface” is.
- Write them as **requirements, not aspirations**, and make §7’s judge score them
  one by one. This is the mechanism that makes the loop converge instead of
  thrash: a critic given a numbered list produces actionable deltas, a critic
  given a movie title produces adjectives.
- Say plainly in the brief *why* a physical anchor was chosen: a violation is then
  wrong for a nameable reason, which is the whole point.

### C. Select techniques

From the concept, pick **only** techniques that pay for pixels. Spec them at
**engineer depth** (buffers, failure modes, shared includes)—not buzzword lists.
State each one's justification from the concept's physics, not from precedent.

Use the playbook tables. Always include unless the concept forbids them:

1. Prime directive + placeholder = defect  
2. Frame budget + zero alloc + pipeline prewarm  
3. Analytic or coherent lighting + post/tonemap discipline  
4. Adversarial screenshot critic vs named reference  
5. Milestone hard gates  

### D. Write the prompt in this exact section order

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
- Low-poly / flat / untextured / placeholder / “prototype” = defect
- Do not stop at “it works.” Stop when every captured frame looks polished and cohesive.
- <If the concept has measurable behaviour: "X that looks about right is also a
  defect — §7 defines numeric acceptance tests. You do not get to declare it good;
  the harness does.">

### 1.1 The standard, derived from <the real material | the real process | first principles>
<The bar is not "good for a browser demo." State the anchor and why it was chosen.>
Then 8–12 numbered, falsifiable properties the agent checks against its own frame:
1. <grain/element scale — is it individually resolvable, and at what size>
2. <light transport that defines the substance: translucency / absorption / anisotropy>
3. <hue + roughness variance within a nominal single colour>
4. <where the darkest value in frame must sit, and why>
5. <highlight size, count, and roll-off; what must never clip>
6. <scale cues: DOF, aerial perspective, contact shadow tightness>
…and for motion:
7. <the equilibrium the material always returns to>
8. <how failure/collapse looks — and the wrong-looking alternative it must not be>
9. <fast contact vs slow contact produce visibly different results>
10. <what must be perfectly, absolutely still when nothing acts on it>

<Close with: "If a frame or a motion violates one of these, it is wrong for a
reason you can name. That nameability is the entire reason to anchor to a physical
standard rather than an aesthetic one.">


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
<Open with "why this and not something cheaper": name each cheaper alternative and
the specific §1.1 property it cannot deliver. Then the numbers, each with its
derivation. Then the failure modes, each with what the user would actually see.>

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
<Each gate states which §1.1 properties it must satisfy.>

## 7. Adversarial verification
<If the concept has measurable behaviour, include a numbered automated acceptance
harness with target ranges — angle of repose, conservation, settling depth, no
residual creep, no hitch on first use — writing results to a file each run. A
number the agent cannot argue with is worth more than any amount of prose.>
- Independent judge subagent (or genuinely uncontaminated second pass) is given the
  screenshots and **the numbered §1.1 property list only**, scores each 1–10, and
  names the single worst thing in frame
- Cannot relax the judge prompt, soften §1.1, or cherry-pick screenshots
- /loop (or equivalent): fix the lowest-scoring property, re-shoot, re-judge —
  until every property scores well, or an honest ceiling is documented
- Verify in real browser at target FPS; first use of every ability must not hitch
- <If a human non-expert is the audience: a fresh evaluator with no knowledge of
  this brief must accomplish the core action within N seconds, with no text on
  screen. "Fix the toy, not the test.">


## 8. Working agreement
Build. Screenshot. Look. Tune. Replace failing techniques. Ship something worth recording.
```

Fill every section with **concrete** numbers and failure modes.

The playbook’s steering patterns are **patterns, not text to paste.** A borrowed
line that still carries its original subject (“reads as snow”, “the wake is a swept
mesh”) is a tell that the brief was assembled rather than reasoned, and it reads as
non-sequitur to the agent receiving it. Re-derive each one for *this* concept and
attach its reason:

- ✗ “This single term does more than almost anything else.”
- ✓ “Of everything in this section, get this term right first: without it you have
  coloured plastic beads no matter what else you do.”
- ✗ “Blown-out white is the primary failure mode.”
- ✓ “Clipped white on the sparkle grains is the primary tonemapping failure mode,
  per §1.1 item 5. Never let a glint reach 1.0.”

Same rule for the section skeleton: rename, merge, split, and renumber sections to
fit the concept. The order above is a checklist of what must be covered, not a form
to fill in.

### E. Length guidance

- **Hybrid / brief:** ~1.5–4k words is fine. Prefer depth on hero systems over
  listing 20 features.
- **Loop-only:** 400–800 words if the user wants something short—but still include
  prime directive, stack, critic, FPS.

Length is bought with derivations, not with more features. If a section grew and
nothing in it is falsifiable, it got longer and weaker.

## Deliverable format (your response to the user)

Everything here is **your chat response**, outside the fenced block. This is the
only place provenance is allowed to appear.

1. **One-line thesis** — what you’re aiming at, and what makes this brief specific
   to the ask rather than generic  
2. **Assumptions** — stack, standard, form (bullet list, short)  
3. **The prompt** — single copy-paste fenced block (complete; no “TBD”; no
   reference to the archive, this skill, or any source demo). Use a 4-backtick
   outer fence so inner code/tables survive.  
4. **How to run it** — empty repo + Claude Code / Codex, ultrathink/ultracode if
   relevant, screenshot loop, plus any real-device gotcha (HTTPS for WebGPU on
   tablets, etc.)  
5. **Where this will actually go wrong** — 3–4 ranked failure predictions with the
   symptom the user will observe. More useful than a technique list, because it
   tells them what to poke at when the one-shot half-works.  
6. **Optional follow-ups** — 2–4 milestone feedback prompts if the one-shot stalls  
7. **Optional technique map** — playbook names to study; link `techniques/demos/…`
   only if the user is in the archive repo. Skip it if §5 already earned its space.

Do **not** implement the game unless asked. Do **not** only link to archive
pages—emit the actual prompt text.

## Quality bar for your output

Reject your own prompt if it:

- Lacks a 60–90s fantasy, or has a quality bar that is a title instead of 8–12
  falsifiable properties  
- **Names the archive, this skill, the playbook, or any source demo anywhere inside
  the block**  
- Contains a number whose derivation isn’t stated, or a “do not use X” without the
  specific thing X fails to deliver  
- Reuses a steering phrase still attached to its original subject matter  
- Says “cool shaders” without buffer/failure-mode detail on the hero system  
- Omits FPS / allocation / prewarm  
- Omits adversarial or screenshot verification, or has a judge scoring vibes rather
  than the §1.1 list  
- Has measurable physical behaviour but no numeric acceptance harness  
- Allows placeholder art to ship  

Final pass before sending: read the block as if you were the receiving agent with
no context and no internet. Anything you couldn’t act on, or couldn’t look up, is a
defect. Then re-check `references/playbook.md`’s bottom checklist.

## Examples of good fusion

Shorthand below is **internal planning notation.** None of these names reach the
emitted prompt; each becomes derived prose there.

**User:** “sand mage that digs dunes”

→ Hybrid desert + granular spine: clipmap + wind-anisotropic noise + deformation
with displaced mass + wrap SSS + 5 abilities writing one shared buffer + 90 FPS.
Standard derived from macro dune photography and real sand behaviour: lee-face
asymmetry, ripple wavelength, repose angle, how a slipface avalanches, grazing
glint that must not crawl. Judge scores those, not “does it look like Journey.”

**User:** “one shot a shooter”

→ Critic loop + single-owner architecture note (coupled lighting/tonemap must not
be split across parallel agents) + procedural materials + post stack + honest 1%
lows. Standard derived from what real interiors do: bounce colour, contact shadow
tightness, muzzle-flash light that actually reaches walls, no ambient-lit flats.

**User:** “cozy shoe shop”

→ Max-effort tone + procedural PBR leather + world-space tools + GPU mask state +
short fantasy “12 days, 12 pairs”. Standard derived from real leather: grain scale,
anisotropic sheen, edge burnishing, how wax builds in creases, thread that sits
*in* a channel rather than on top.

## What good output looks like

A brief that passes: a derived numbered standard instead of a title; every number
carrying its reason; negative specs that name the alternative and what it fails to
deliver; a numeric acceptance harness wherever behaviour is measurable, sitting
alongside the visual judge; failure modes written as what the user would observe;
and not one reference to anything outside the block itself.
