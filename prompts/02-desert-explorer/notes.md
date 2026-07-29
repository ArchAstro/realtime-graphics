# Desert explorer — process notes + reconstructed seed

## What OP publicly described

> a browser desert you walk around in third person. The terrain is a procedural dune field on a GPU clipmap — no meshes, no textures, no downloaded assets; every surface is generated in shader code. Sand deforms permanently where you walk and slowly erodes back. There's a hooded robe simulated as GPU cloth, a physically-based sky marched per pixel, and six aimed sand spells (1–5 and right mouse) that dig real craters into the terrain and raise real dunes you can ride.

## Reconstructed seed (NOT original — for experimentation)

Use this as a starting point, then iterate with screenshot + GPU-cost feedback like OP did. Prefer the full SNOWFLOW brief in `../01-snowflow-waterbending/prompt.md` for the mature version of the same design language.

```
You are the sole engineer and technical artist on a real-time graphics tech demo.
Build a third-person desert sand-mage tech demo end to end.

PRIME DIRECTIVE: Visual quality is the product. No gameplay loop, no progression UI.
A player walks dunes for 90 seconds, casts sand spells, and either thinks "this is AAA" or closes the tab.

STACK: Modern JS (ES modules), Three.js latest with WebGPURenderer + TSL, Vite.
TARGET: Chrome desktop, discrete GPU, 1440p, 90 FPS sustained / 60 FPS floor.
NO WebGL fallback. If navigator.gpu is missing, show one line and stop.
NO downloaded meshes/textures/HDRIs if procedural can win. Everything in shader code where possible.

SYSTEMS (must ship):
1. Geometry clipmap dune field, wind-anisotropic layered noise height, far ridge impostors.
2. Custom sand material: multi-scale normals, sparkle, wet/compressed states, triplanar on steep faces.
3. Persistent player-following deformation render target (depression + berm mass + compression). Feet, surf, and spells all write the same buffer. Trails refill slowly and self-shadow.
4. Physically based sky (per-pixel march or high-quality analytic) with long low sun and soft cascaded shadows (PCSS).
5. Procedural hooded-robe character, GPU cloth on hem/sleeves, foot planting IK, footfall spray.
6. Six aimed sand abilities (keys 1–5 + RMB) that dig real craters / raise rideable dunes — displacement is geometry, not decals.
7. Post: TAA, restrained bloom, tonemap (AgX/ACES), grain. Every effect toggleable from F1 overlay with frame-time graph + 1% lows.

PERFORMANCE: Zero allocations in the render loop. Prewarm every pipeline before the loading screen dismisses. Instrument with a headless Chrome harness that screenshots and reports per-subsystem GPU cost.

MILESTONES (hard gates — screenshot each, do not proceed if ugly):
Foundation → Terrain+sand look → Deformation → Character/cloth → Spells → Polish+perf.

Do not stop when it works. Stop when every captured frame looks polished and cohesive.
```

## Follow-up loop OP used

1. Build milestone
2. Human playtests + Claude screenshots
3. Feed bugs / "looks wrong" / GPU ms back into next prompt
4. Character model was weak → redesigned as fully robed so cloth hides cheap geometry
