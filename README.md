# Realtime Graphics Prompts

A research archive and toolkit for **AI-built realtime graphics**: viral browser games and simulations (Three.js / WebGPU / Babylon), the **prompts that produced them**, the **GPU techniques** they rely on, and an **installable agent skill** that turns those lessons into a new one-shot prompt.

This is not a game engine. It is:

1. **Prompt archive** — original (or reconstructed) prompts + metadata for demos that look and feel high quality  
2. **Technique curriculum** — interactive WebGL teaching demos for the systems those prompts force models to build  
3. **Agent skill** — `realtime-graphics-prompt`, installable via [`npx skills`](https://github.com/vercel-labs/skills)

---

## Live site (GitHub Pages)

**https://archastro.github.io/realtime-graphics/**

- Repo is **private** (`ArchAstro/realtime-graphics`); source code stays private.
- The **Pages site is public** (anyone with the URL). GitHub only offers access-controlled private Pages on Enterprise Cloud.
- Deploy: push to `main` → `.github/workflows/pages.yml` builds with base path `/realtime-graphics` and deploys.

## Quick start (local)

```bash
# Browse the archive in your browser (builds prompt HTML pages, then serves)
npm run dev
```

Opens `http://127.0.0.1:8000/` by default.

```bash
npm run dev -- 3000       # custom port
npm run dev -- --no-open  # serve without opening a browser
npm run build             # only regenerate prompts/*/index.html from markdown
npm run build:pages       # build .pages-dist/ with GH Pages base path
```

Requires **Python 3** (for the static server and HTML rebuild). No `npm install` of app dependencies is required for the site.

---

## What’s in here

### 1. Prompt archive (`prompts/`)

Twelve high-signal demos scraped from Reddit / X, each with:

| File | Purpose |
|------|---------|
| `meta.md` | Why it made the cut, author, stack, demo/repo links |
| `prompt.md` (or `prompt-*.md`) | The actual prompt text when published |
| `notes.md` | Process notes / reconstruction when the original prompt was lost |
| `index.html` | Generated readable page (hero, facts, prompt panel, related techniques) |

Browse at **`/prompts/`** after `npm run dev`.

Examples:

| # | Demo | Why it matters |
|---|------|----------------|
| 01 | [SNOWFLOW](prompts/01-snowflow-waterbending/) | Full WebGPU snow/waterbending brief (~19k chars) |
| 02 | [Desert explorer](prompts/02-desert-explorer/) | Clipmap dunes + sand spells; process notes |
| 03 | [Claude of Duty](prompts/03-claude-of-duty/) | Adversarial AAA critic loop → ~55k LOC FPS |
| 04 | [The Long Silence](prompts/04-the-long-silence/) | Space game + Starfield judge `/goal` |
| 05 | [SOLEBOUND](prompts/05-solebound-shoe-repair/) | Short max-effort → full shoe-repair game |
| 06 | [SDF blend-shell creatures](prompts/06-sdf-blend-shell-creatures/) | Novel seamless procedural characters |
| 07–12 | City, COD zombies, crane, canal locks, grass, mansion | One-shots and bake-offs |

Each folder’s `meta.md` cites original posts and licenses of *those* projects.

### 2. Techniques (`techniques/`)

GPU / rendering ideas reverse-engineered from the archive, with **live demos**:

| # | Technique | Demo |
|---|-----------|------|
| 01 | Geometry clipmap | [`demos/01-geometry-clipmap.html`](techniques/demos/01-geometry-clipmap.html) |
| 02 | Layered wind-anisotropic noise | [`demos/02-layered-wind-noise.html`](techniques/demos/02-layered-wind-noise.html) |
| 03 | Persistent deformation buffer | [`demos/03-deformation-buffer.html`](techniques/demos/03-deformation-buffer.html) |
| 04 | Multi-scale surface shading | [`demos/04-multi-scale-shading.html`](techniques/demos/04-multi-scale-shading.html) |
| 05 | Wrapped diffuse + cheap SSS | [`demos/05-wrap-sss.html`](techniques/demos/05-wrap-sss.html) |
| 06 | SDF blend-shell | [`demos/06-sdf-blend-shell.html`](techniques/demos/06-sdf-blend-shell.html) |
| 07 | Floating origin | [`demos/07-floating-origin.html`](techniques/demos/07-floating-origin.html) |
| 08 | Bake vs evaluate | [`demos/08-bake-vs-evaluate.html`](techniques/demos/08-bake-vs-evaluate.html) |
| 09 | Analytic sky | [`demos/09-atmosphere-sky.html`](techniques/demos/09-atmosphere-sky.html) |
| 10 | Post stack + tonemap | [`demos/10-post-stack.html`](techniques/demos/10-post-stack.html) |
| 11 | Swept-mesh wake | [`demos/11-swept-mesh.html`](techniques/demos/11-swept-mesh.html) |
| 12 | Procedural PBR forge | [`demos/12-procedural-pbr.html`](techniques/demos/12-procedural-pbr.html) |

- Curriculum hub: **`/techniques/`**
- Demo index: **`/techniques/demos/`**
- Cross-links: `techniques/catalog.json` maps techniques ↔ source prompts

Teaching demos are simplified WebGL/Three.js sketches, not production ports of the viral projects.

### 3. Agent skill (`skills/realtime-graphics-prompt/`)

Installable with the [skills CLI](https://github.com/vercel-labs/skills). When you run `/realtime-graphics-prompt` (or ask for a one-shot game prompt), the agent:

1. Loads the distilled **playbook** (`skills/.../references/playbook.md`)
2. Optionally skims this archive if you’re in the repo
3. Emits a **copy-paste implementation brief** (SNOWFLOW-style systems + CoD-style critic + FPS/perf rules)

#### Install the skill

From this checkout:

```bash
# See what this package ships
npx skills add . --list
# or
npm run skills:list

# Install into agents for the current project
npx skills add . --skill realtime-graphics-prompt -y
# or
npm run skills:install

# Install for your user (all projects)
npx skills add . --skill realtime-graphics-prompt -g -y
# or
npm run skills:install:global
```

From GitHub:

```bash
npx skills add ArchAstro/realtime-graphics --skill realtime-graphics-prompt -y
npx skills add ArchAstro/realtime-graphics --skill realtime-graphics-prompt -g -y
```

#### Use the skill

```
/realtime-graphics-prompt
```

Or natural language: *“write a one-shot prompt for a sand-mage desert tech demo.”*

---

## Site map

| URL | What |
|-----|------|
| `/` | Home — entry points to demos, curriculum, prompts |
| `/techniques/` | Technique curriculum (HTML) |
| `/techniques/demos/` | Interactive technique demos |
| `/prompts/` | Prompt archive index |
| `/prompts/<id>/` | Single prompt (overview, facts, full text, related techniques) |

Subtle WebGL backdrop: `techniques/site-bg.js` (content sits on solid frosted panels for readability).

---

## Repo layout

```
realtime-graphics-prompts/
├── index.html                 # site home
├── package.json               # npm run dev / build / skills:*
├── scripts/
│   ├── dev.sh                 # build prompts + serve (used by npm run dev)
│   ├── serve.sh               # alias → dev.sh
│   └── build-prompt-pages.py  # markdown → prompts/*/index.html
├── prompts/                   # archive (md sources + generated HTML)
├── techniques/                # curriculum, demos, catalog, shared CSS/JS
├── skills/
│   └── realtime-graphics-prompt/   # npx skills package
│       ├── SKILL.md
│       └── references/playbook.md
├── skills.sh.json             # skills.sh grouping metadata
└── README.md
```

Grok also discovers the skill via `.grok/skills/realtime-graphics-prompt` → symlink into `skills/`.

---

## Patterns that produce quality

Across the best demos, working prompts share these moves:

1. **Visual quality is the product** — prime directive that can override scope  
2. **Adversarial visual critics** — screenshot loops vs a named AAA bar (CoD, Starfield, …)  
3. **Hard frame budgets** — 60/90 FPS, **1% lows**, not average FPS alone  
4. **Procedural art** — no asset pipeline thrash; coherent style from code  
5. **Milestone gates** — don’t advance while a still looks like a prototype  
6. **Shared world state** — feet / spells / tools write one deformation buffer so FX feel *in* the world  
7. **Pipeline prewarm** — first ability cast must not compile mid-frame  

Full checklist: `skills/realtime-graphics-prompt/references/playbook.md`.

---

## npm scripts

| Script | What it does |
|--------|----------------|
| `npm run dev` | Rebuild prompt HTML + serve site + open browser |
| `npm run build` | Only rebuild `prompts/*/index.html` from markdown |
| `npm run skills:list` | `npx skills add . --list` |
| `npm run skills:install` | Install skill into project agents |
| `npm run skills:install:global` | Install skill globally |

---

## Editing the archive

1. Edit or add markdown under `prompts/<id>/` (`meta.md`, `prompt.md`, …).  
2. If you add a technique link, update `techniques/catalog.json` (and optionally the demos).  
3. Run `npm run build` or `npm run dev` to regenerate HTML pages.  
4. For skill wording/playbook changes, edit `skills/realtime-graphics-prompt/` and reinstall if needed (`npm run skills:install`).

---

## Sources

Collected from public Reddit and X posts (ClaudeAI, aigamedev, singularity, threejs, and related threads). Individual `meta.md` files cite authors, posts, and upstream repos.

---

## License

- **This collection** (site, curriculum, skill packaging, organization) is for research and learning.  
- **Upstream prompts and demos** remain attributed to their authors; respect each project’s license before reuse or redistribution of *their* code/assets.
