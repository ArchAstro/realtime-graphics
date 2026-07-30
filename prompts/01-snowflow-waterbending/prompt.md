> Source: Reddit r/ClaudeAI — [People liked my desert, so here's a waterbending demo!](https://www.reddit.com/r/ClaudeAI/comments/1v94nal/people_liked_my_desert_so_heres_a_waterbending/) by u/Any-Reputation8118.
> Extracted from the post's spoiler block (implementation brief). Author notes this created the base; further milestone prompts guided Opus.

# SNOWFLOW — Tech Demo · Implementation Brief

You are the sole engineer and technical artist on a real-time graphics tech demo. Build it end to end. This document is the spec, the art direction, and the acceptance criteria.
## 0. Prime directive

Visual quality is the product. There is no gameplay loop, no progression, no UI to design around. A player will load this, walk around a snow field for ninety seconds, cast a few spells, surf across a dune, and either think "this is AAA" or close the tab. Everything below serves that single judgment.
Two rules that override everything else in this document:
If a requirement in this brief conflicts with making the demo more beautiful, break the requirement. Note the deviation in `DECISIONS.md` with a one-line rationale. You have full authority to change scope, swap techniques, or drop a feature that isn't paying for its pixels.
Anything that reads as low-poly, flat-shaded, untextured, placeholder, or "indie prototype" is a defect, not a stepping stone. If you can't make a thing look finished, cut it from the frame rather than ship it looking rough.
Do not stop at "it works." Stop when every captured frame looks polished, cohesive, and production-ready.
## 1. Stack and hard constraints

- **Language:** Modern JavaScript (ES2023 modules). JSDoc types encouraged, no TypeScript build step required.
- **Engine:** Babylon.js latest stable, WebGPU only
- **Bundler:** Vite
- **Target:** Chrome stable on Windows 11, RTX 5070 Ti, 2560×1440
- **Frame target:** 90 FPS sustained. 60 FPS floor.
- **Frame time:** No frame exceeding median + 4 ms after the loading screen dismisses

No fallbacks. No WebGL path, no mobile path, no feature detection branches. If navigator.gpu is absent, show a single line of text and stop. Do not spend a minute on compatibility.
Assets. Generate procedurally where it produces a better or more controllable result, including terrain, noise, and most masks. Use free CC0 assets where hand-authored data wins, such as Poly Haven HDRIs and snow or ice PBR material scans, or ambientCG detail textures. Vendor everything into the repository; no runtime CDN fetches. Document every third-party asset and its licence in ASSETS.md.
## 2. Systems
### 2.1 Terrain

A flat plane will kill this demo. The snow field needs real form.
Build a geometry clipmap or nested-ring LOD centred on the player, so triangle density is high near the camera and falls off with distance. Aim for roughly sub-10 cm vertex spacing in the inner ring at default zoom.
Height comes from layered procedural noise composited on the GPU: broad dune forms measured in tens of metres, medium drifts and wind lobes measured in metres, and sastrugi ridges and ripples measured in decimetres. Do not use a single fBm octave stack and call it done. The terrain needs directional structure carved by a prevailing wind. Encode a wind direction and let the medium and fine layers stretch and shear along it.
Include a small number of exposed rock outcrops or ice shelves so there is silhouette and scale in the mid-distance, with snow accumulation blending onto their upward faces. Keep them sparse. The brief is "just snow and the player," and these exist only to give the horizon something to say.
The far field needs mountains and heavy aerial perspective. A distant matte-projected ridgeline or a low-cost impostor ring is acceptable as long as it never reads as flat.
### 2.2 Snow shading

This shader is the most important code in the project. Budget accordingly.
Build a custom material using Babylon ShaderMaterial, a PBRCustomMaterial plugin, or an equivalent approach. Use WGSL through NodeMaterial or raw shader code, not a stock PBR material with a white albedo.
Required behaviours:
- Multi-scale normals. Detail normal maps at three tiling scales, blended by distance and slope, plus normals derived analytically from the deformation heightfield (§2.3). Use triplanar mapping on steep slopes.
- Subsurface scattering. Snow is translucent. Use wrapped diffuse plus a back-scatter term. Shadowed and grazing areas should pick up a soft blue-white internal glow rather than going flat dark. This single term does more for "reads as snow" than almost anything else.
- View-dependent glinting. Create procedural sparkle from a high-frequency normal perturbation, gated hard on a narrow specular lobe and grazing view angle, with a stable hash so glints do not crawl or shimmer under TAA. Keep it subtle. If it looks like glitter, halve it, then halve it again.
- Compression, wetness, and ice as separate surface states. Trodden and spell-affected snow is denser, with darker albedo, tighter specular response, and less scatter. Refrozen ice is smoother and more reflective. Read this from the terrain state buffer (§2.3) so it is shared by movement and spells.
- Contact detail. Trail edges need micro-occlusion and a hint of chunky displaced granularity, not a clean bevel.
### 2.3 Terrain state and deformation

This is the core interactive system. Everything writes here; the snow shader reads it.
Maintain a player-following render target covering roughly 60–100 m, with resolution high enough for approximately 2 cm texels in the deformation area. A 4096² R16F target scrolled toroidally as the player moves is a reasonable starting point. Snap movement to texel boundaries to avoid swimming.
Suggested channels, packed across one or two targets as appropriate:
- Depression depth — how far the surface is pushed down.
- Displaced mass — snow pushed out of a depression, forming berms at trail edges. Do not skip this.
- Compression, wetness, and ice — persistent surface states used by shading.
Rules:
Deformation is persistent and additive, accumulated by writing brush splats into the target each frame. Never rebuild it from a list of past events.
Apply slow refill over time through a gentle diffusion and decay pass, so trails soften and eventually heal. Tune it so a trail remains clearly visible after 60 seconds.
Terrain vertex displacement samples the depression and displaced-mass channels. Recompute normals from the same data so lighting and shadowing respond correctly. A trail that does not self-shadow is a failure.
Player feet, the snow-surf wake, and every spell write into this buffer. That shared write path is what makes the spells feel embedded in the snow rather than like effects floating above it.
### 2.4 Atmosphere and lighting

Use a low, warm sun that creates long shadows. Use cascaded shadow maps with PCSS-style soft filtering. Tune cascade splits so near-field trail shadows stay crisp.
Use a high-quality HDRI or a physically based sky model if it gives better control over sun angle. Ambient light must be strongly blue-shifted. The cool-shadow and warm-light contrast is essential to the snow rendering.
Add fog and aerial perspective with height falloff. Distance should compress contrast noticeably.
Add ground blow or spindrift: low, wind-driven surface snow streaming across the field. It should make the environment feel alive without obscuring the terrain.
Add volumetric light shafts only where they materially improve the image. Keep them restrained.
Spells emit light. Budget 4–6 dynamic lights maximum, with tight radii. Ensure the snow shader's subsurface-scattering term responds to them so a spell visibly illuminates the snow from within the drift it touches.
### 2.5 Post-processing

Order matters. Suggested chain:
TAA → SSAO → screen-space reflections on wet and icy surfaces only → very restrained depth of field → restrained bloom → ACES or AgX tonemapping → subtle film grain → post-TAA sharpening.
TAA is essential for stabilising glinting and thin geometry. Every post-process should be individually toggleable from the settings overlay for A/B comparison. Blown-out white is the primary failure mode for snow renders, so monitor highlight roll-off constantly.
### 2.6 Character and robe

The character will be seen from behind at mid-distance almost the entire time. Spend the budget on silhouette, cloth, and shading; spend almost nothing on the face.
Create a hooded, layered robe with a deep cowl, long sleeves, an over-mantle, and a trailing hem. Use shell-based fur at the hood and cuffs, with roughly 20–40 shells and alpha-tested strands.
Add cloth simulation to the hem, sleeves, and mantle. A GPU or CPU Verlet simulation with distance and bending constraints is acceptable. Drive it with locomotion velocity, acceleration, and the wind field. During snow-surf, the cloth should whip backwards sharply.
Cloth shading needs sheen or fuzz and an anisotropic response for a woven appearance, plus subsurface scattering on thin regions. Do not use a plain PBR dielectric.
Keep the face in shadow beneath the hood. Do not model detailed facial features that cannot be finished to the same standard.
If a rig and locomotion animation cannot be brought to a high standard, prefer a fully cloth- and procedurally driven figure over a stiff or poorly animated one. Feet must plant rather than slide.
Feet displace snow and kick up spray on each step. This must be frame-accurate with each footfall.
### 2.7 Camera and controls

Use third-person, action-MMO framing. Position the camera over the shoulder with a slight offset rather than directly behind the character.
WASD movement is relative to camera facing. The mouse orbits. The scroll wheel zooms across a smooth, eased range.
Use a spring-arm camera with collision-free but velocity-aware behaviour. It should lag slightly under acceleration, widen the FOV under speed, and tighten on stopping. All transitions must ease, with no snapping.
Add subtle camera shake to heavy spells and hard surf carves. Keep it subtle.
### 2.8 Spells: keys 1–5

All five spells share one bending grammar: continuous, momentum-carrying, unbroken flow. No instant spawns and no instant despawns. Everything eases in from the snow and settles back into it. Every spell reads and writes the terrain state buffer.
Suggested set, adjustable where a different implementation produces a stronger result:
- Sweep — A crescent wave of slush and water rises from the ground ahead and travels outward, ploughing a channel and throwing berms to either side.
- Ribbon — A held, continuous stream of water tracks the player's hand and the camera aim, describing arcs and figure-eight paths in the air and scoring thin curved lines in the snow beneath it.
- Bloom — A targeted eruption sends a column of powder and water upwards, blows a crater with a raised rim, then falls back as a slow, glittering curtain of fallout.
- Crystallize — Water rapidly freezes. Refractive crystal formations grow out of the drift with visible subsurface scattering and internal light transport, permanently altering the surface state to glossy ice. This effect should encourage the player to stop and inspect it.
- Vortex — A swirling column of airborne snow forms around the player, visibly stripping surface snow from the ground. The deformation buffer thins in a ring, holds the removed snow aloft, and lets it settle back.
Implementation direction: use swept procedural ribbon or tube meshes updated on the GPU from a spline or particle spine for the coherent water body, GPU compute particles for spray, mist, and droplets, and a refraction pass for translucency. Full screen-space fluid rendering is probably too expensive for the frame target, but use it if it remains within budget and materially improves the result.
Water shading needs:
Refraction with restrained chromatic dispersion.
Depth-based absorption tint.
Animated flow-map normals.
Foam and slush at the leading edge.
Shed droplets with correct motion-blur streaking.
### 2.9 Snow-surf: hold RMB

This will be used more than everything else combined. It receives the most polish.
Holding RMB raises a crest of compressed snow under the player's feet. The player accelerates. Mouse movement steers carving turns with visible body lean and a banked camera.
The wake is the centrepiece: a curling, breaking wave of displaced snow trails behind and towards the outside of the turn, throwing a spray plume that catches sunlight and casts a shadow. It should combine the physical character of a snowboard carve and a boat wake.
Snow-surf carves a deep, persistent groove into the terrain buffer with high berms. A completed run should remain visible from across the field.
Entering and exiting use eased transitions, never snaps. The robe whips backwards, the FOV widens, and wind streaks appear in screen space. There is no audio, so every visual cue must contribute to the sensation of speed.
Turning at speed should feel weighty and analogue. Tune it by hand until it feels good, not merely until it compiles.
## 3. Performance engineering

Garbage collection is your primary enemy. A 12 ms garbage-collection pause is a visible hitch and instantly destroys the AAA impression.
Zero allocations in the render loop. Do not use new inside per-frame code. Pre-allocate scratch Vector3, Matrix, and Quaternion instances at module scope and reuse them.
Do not use map, filter, reduce, spread syntax, or destructuring that creates new objects in hot paths. Use plain indexed for loops.
Do not construct strings each frame, including for the performance overlay. Update the overlay on a throttled interval and reuse buffers.
Use object pools for every transient effect, particle burst, and decal.
Use pre-allocated typed arrays for all GPU buffer uploads. Write into them rather than rebuilding them.
Use scene.freezeActiveMeshes(), mesh.freezeWorldMatrix(), material.freeze(), and scene.blockMaterialDirtyMechanism aggressively for static content.
Use thin instances for all repeated geometry.
Profile with the Chrome performance panel and Babylon's inspector. Ship a frame-time graph in the overlay showing the 1% low, not merely an FPS counter. Average FPS will hide the exact hitching problem that matters most.
Set a frame budget and hold to it. At 90 FPS, the total budget is 11.1 ms. Allocate it explicitly across terrain, snow shading, shadows, VFX, cloth, and post-processing. Record actual measured cost per system in PERF.md.
## 4. Loading and pipeline warm-up

WebGPU pipeline compilation stutter is a real and severe risk. A shader that first compiles when the player casts spell 4 will produce a multi-hundred-millisecond freeze.
Before the loading screen dismisses:
Load and decode every texture, HDRI, mesh, and buffer.
Force-compile every material and particle-system pipeline, including every spell, post-process, and shader permutation, by rendering them once to a tiny offscreen target.
Warm every render target and run several frames of every compute pass.
Only then fade in.
A four-second load with a clean first minute is better than an instant load that hitches. Present a tasteful loading screen. This is the first thing anyone sees, so it must not resemble an unstyled browser default.
## 5. UI

Provide only a settings and performance overlay, toggled with a key such as F1 or backtick and hidden by default.
Contents:
Frame-time graph with 1% low.
Draw-call and triangle counts.
Individual toggles for every post-process and major system.
Quality presets.
Sliders for the art parameters most likely to need live tuning, including sun angle, fog density, glint intensity, deformation depth, and refill rate.
Build this early. It will save hours.
No HUD. No crosshair. No spell bar. Nothing else on screen, ever.
## 6. Project structure

Suggested structure; adapt as needed:

```
/src
  /core        engine bootstrap, render loop, resource manager, pooling
  /terrain     clipmap, procedural heightfield, deformation buffers
  /shaders     WGSL
  /character   controller, robe cloth, shell fur
  /spells      one module per spell + shared bending primitives
  /vfx         particle systems, decals, spray
  /post        post-process chain
  /ui          settings overlay
/assets        vendored, with ASSETS.md
DECISIONS.md   every deviation from this brief + rationale
PERF.md        measured frame budget per system
```

## 7. Milestones

Take a 1440p screenshot at every milestone, inspect it critically, and commit the screenshots.
- Foundation — WebGPU boot, Vite, render loop, settings overlay with frame graph, camera, and WASD movement on a placeholder plane.
- Terrain and snow shading — Clipmap, procedural heightfield, full snow material with subsurface scattering and glinting, sun, cascaded shadows, sky IBL, and fog. Gate: a static screenshot with no character already looks polished, atmospheric, and production-ready. Do not proceed until this is true.
- Deformation — Full terrain state buffer, footfall displacement with berms, refill, correct normals, and self-shadowing. Gate: footprints and trails visibly displace mass, form raised edges, and integrate correctly with lighting.
- Character — Robe, cloth simulation, shell fur, locomotion, foot planting, and spray on footfall.
- Snow-surf — The centrepiece. Spend disproportionate time here.
- Spells — All five spells, each writing into the terrain.
- Post-processing and polish pass — Full chain, tonemapping calibration, spindrift, and restrained light shafts.
- Performance hardening — Profile, eliminate every allocation in the loop, verify 90 FPS with clean 1% lows, and verify that warm-up covers every pipeline.
## 8. Visual acceptance criteria

Before declaring the demo complete, verify each item against a fresh 1440p screenshot and in motion:
No visible faceting, hard polygon edges, or flat-shaded surfaces anywhere in frame.
Snow highlights are not clipped to pure white; shadows are blue rather than grey or black.
Distant terrain shows clear aerial perspective and contrast compression.
Surface detail is legible at three distinct scales simultaneously: dunes, ripples, and grain.
Trails have raised berms, self-shadow correctly, and soften over time.
Sparkle appears only at grazing angles and does not crawl or shimmer in motion.
The robe reads as layered fabric with real cloth motion, and the fur trim reads as fur.
Spell water is translucent and refractive, with visible internal light scatter.
Spell light visibly illuminates the snow it touches, including through-scatter.
Every spell leaves a mark on the terrain that persists after the effect ends.
The snow-surf wake looks like displaced mass with momentum, not merely particle spray.
The demo sustains 90 FPS with 1% lows above 60 FPS.
No hitch occurs on the first cast of any spell.
## 9. Working agreement

Build, don't test-loop. Playwright is available for capturing screenshots at milestones and catching hard regressions. Use it for those purposes. Do not build a test suite; time spent on tests is time not spent on the snow shader.
Look at your own output constantly. Capture screenshots, inspect them critically, and iterate on values. Most of the quality gap between "prototype" and "AAA" is parameter tuning, and you can only close it by looking.
Do not move on from an ugly milestone. Milestone 2 in particular is a hard gate.
When a technique is not working, replace it rather than patching it. You have full latitude over the approach.
Record every deviation in `DECISIONS.md`, briefly. One line is sufficient.
Ship something worth screenshotting.