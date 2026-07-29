# Painterly grass world — reconstruction seed

Original prompt unknown. Seed for experiments targeting the same class of result:

```
Build a single self-contained HTML file (Three.js via CDN is fine) that is a
painterly outdoor world the player can walk or fly through.

VISUAL GOAL: Studio Ghibli / watercolor landscape energy — soft hills, layered
atmospheric fog, hand-painted color grading — but fully realtime and interactive.

NON-NEGOTIABLE FEATURE:
Instanced grass field covering the terrain. Millions of blades (or the illusion
of millions via dense instancing + LOD). Every blade reacts to a continuous
wind field simulation (gusts, direction changes, turbulence). Grass should also
react locally when the camera/player moves through it.

ALSO INCLUDE:
- Procedural terrain with rolling hills
- Trees or flowers as secondary instanced vegetation
- Soft sky + sun disk, warm rim light
- Camera: smooth free-fly or third-person walk
- 60fps target on a mid-range desktop GPU
- No external image/model assets — pure procedural geometry and shaders

When you think you're done, screenshot. If the grass doesn't feel alive in the
wind, you're not done.
```
