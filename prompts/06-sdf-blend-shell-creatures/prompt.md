# SDF blend-shell creatures — initial prompt

Source: Reddit r/aigamedev comment by OP on [Fable 5 procedural creatures](https://www.reddit.com/r/aigamedev/comments/1umiurs/fable_5_just_oneshot_crazy_cool_procedural/)

```
Build with Three.js and explore a new procedurally generated 3D character style — ragdoll-like characters composed of primitive shapes that look like one seamless body via a custom, mobile-performant tech-art/shader solution, with toon styling, plus a procedural animation system that works for 2-legged, any-legged, no-legged (hopping) and flying characters with arms. Goal: a unique, easily AI-generatable style with heavy juice and polish — "HOLY SH** THIS WAS DONE WITH AI?" quality, "for the next billion dollar game."
```

## What Fable invented (OP summary)

- Capsule/cone primitives merged to one draw call
- Vertex shader snaps verts onto **smooth-min SDF surface of all shapes** → seams vanish
- Normals from SDF gradient; colors blend by proximity
- Outlines on SDF *offset* surface; thin parts cap blend radius
- Procedural animation: reactive IK feet (2/4/6 legs), hop state machine, flyer bank, physics rope tails that are also SDF primitives
- Character definition ≈ 15 lines of JSON
