# SIMNearby 🌆

> **Record a city. Reimagine it.**

[![Status](https://img.shields.io/badge/status-🚧_Early_Development-orange)](.)
[![Stack](https://img.shields.io/badge/stack-TypeScript_·_React_·_Three.js_·_Node.js_·_Python-blue)](.)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

SIMNearby lets you record video of any city street or location and generate interactive 3D "what-if" worlds — visualize what that street looks like with different buildings, green spaces, transit options, or urban planning changes using VR/3D simulation.

---

## ✨ Core Features

| Feature | Description |
|---|---|
| 📹 **Video Ingest** | Upload city footage; extract frames & geo-metadata |
| 🏗️ **3D Reconstruction** | ML pipeline (NeRF / photogrammetry) builds a 3D scene mesh |
| 🎨 **What-If Editor** | Drag-drop urban elements: buildings, parks, roads, density |
| 🥽 **VR Viewer** | Immersive Three.js WebXR scene; desktop + headset modes |
| 💾 **Scenario Sharing** | Save, fork, and share scenarios via URL |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | TypeScript · React 18 · Three.js · React Three Fiber · Zustand |
| Backend | Node.js · Express · TypeScript |
| Reconstruction | Python 3.11 · OpenCV · Open3D · PyTorch (NeRF/Gaussian Splatting) |
| Storage | PostgreSQL · S3-compatible object store |
| VR | WebXR · Three.js XRSession |
| Testing | Vitest (client) · Jest (server) · pytest (Python) |
| CI | GitHub Actions |

---

## 🚀 Getting Started

```bash
# Clone
git clone https://github.com/joshiujjwal/simnearby.git
cd simnearby

# Install JS dependencies
npm install

# Install Python dependencies
cd src/reconstruction && pip install -r requirements.txt && cd ../..

# Copy env config
cp .env.example .env

# Start dev servers (client + server)
npm run dev

# Run 3D reconstruction worker
npm run worker:reconstruction
```

### Running Tests

```bash
# All JS/TS tests
npm test

# Python reconstruction tests
pytest tests/reconstruction/

# E2E (TODO — Playwright setup in Phase 2)
npm run test:e2e
```

---

## 📁 Project Structure

```
simnearby/
├── src/
│   ├── client/               # React + Three.js frontend
│   │   ├── components/       # UI components (panels, controls, overlays)
│   │   ├── hooks/            # Custom React hooks
│   │   ├── scenes/           # Three.js scene graphs and XR setup
│   │   ├── store/            # Zustand state slices
│   │   └── utils/            # Geo helpers, mesh loaders, etc.
│   ├── server/               # Node.js / Express API
│   │   ├── routes/           # REST endpoints
│   │   ├── services/         # Business logic (job queue, scenario CRUD)
│   │   └── middleware/       # Auth, validation, error handling
│   └── reconstruction/       # Python ML pipeline
│       ├── pipeline/         # Orchestration (ingest → reconstruct → export)
│       ├── models/           # NeRF / Gaussian Splatting wrappers
│       └── utils/            # Frame extraction, GPS parsing, mesh utils
├── tests/                    # Mirrors src/ structure
├── docs/
│   ├── spec.md               # Full feature specification
│   └── adr/                  # Architecture Decision Records
├── .github/
│   ├── copilot-instructions.md
│   ├── workflows/            # CI/CD pipelines
│   └── skills/               # Agent skills
├── README.md
├── TODO.md                   # Evidence-gated task breakdown
├── CLAUDE.md                 # Claude/Anthropic context
└── AGENTS.md                 # OpenAI Codex agent instructions
```

---

## 🤝 Contributing

1. **Write tests first** (red phase) before implementing anything
2. Make tests pass (green phase)
3. Review your own diff — would you approve this in a PR?
4. Commit with a descriptive message referencing the TODO item
5. Open a PR with **evidence**: screenshots, passing test output, or a short video
6. Small, focused PRs only — one concern per PR

> No evidence = no merge. This keeps the feedback loop tight and the codebase honest.

## 🚀 Improvement Proposals

### First-Principles Analysis
- **NeRF/Gaussian Splatting is compute-intensive by nature**: Reconstructing a 3D scene from video frames is an inverse rendering problem that takes minutes-to-hours on GPU hardware; the architecture must treat reconstruction as an async background job, not a synchronous API call — the current worker design is correct but must be made failure-tolerant.
- **Urban planning as the primary use case creates a paradox**: Meaningful "what-if" scenarios require accurate base geometry, but accurate geometry requires high-quality input video with controlled overlap, lighting, and GPS; casual city walkers won't produce reconstruction-grade footage without guidance.
- **Three.js WebXR is the right layer, but 3D model file size is the critical bottleneck**: A street-level NeRF scene can produce meshes in the hundreds of megabytes; streaming and progressive loading strategy determines whether VR mode is usable on commodity hardware or only on high-end rigs.
- **"Scenario sharing via URL" implies a content delivery problem**: Shareable scenarios require the 3D assets to be hosted, versioned, and served globally at acceptable latency — S3 alone is not a CDN strategy.

### Key Risks & Assumptions
- **Assumes users have reconstruction-quality video**: Handheld smartphone video with motion blur, occlusion, and inconsistent frame overlap frequently fails NeRF pipelines outright; without guided capture (overlay, checklist), the tool will produce poor 3D models for most users.
- **GPU dependency for reconstruction is a cost and latency cliff**: Every reconstruction job requires GPU compute; this is expensive at scale and creates queue depth problems during peak usage without a cost-control mechanism.
- **Urban planning regulations vary by jurisdiction**: A "what-if" showing a new high-rise may be useful for public discourse but legally ambiguous for professional planning submissions — the use case scope needs boundaries.
- **WebXR adoption remains low**: Most users accessing via a browser will not have a VR headset; the desktop 3D viewer must be excellent as the primary experience, not a fallback.

### Concrete Improvement Ideas
- **Build a guided video capture mode** — an in-browser or mobile UI that overlays coverage indicators, optimal walking paths, and frame-quality feedback during capture; this is the single highest-leverage improvement because it directly determines reconstruction quality.
- **Implement progressive mesh streaming** — export scenes as tiled 3D (3D Tiles / glTF LOD) and stream detail progressively based on camera proximity; this makes large scenes feasible on consumer hardware and in mobile browsers.
- **Add a pre-reconstruction quality gate** — analyze uploaded frames for blur, coverage gaps, and GPS consistency before queuing GPU work; reject or warn on low-quality inputs to avoid wasted compute and user frustration.
- **Create scenario diff visualization** — a split-view or overlay mode comparing original reconstruction to modified scenario; this is the "before/after" that makes what-if planning genuinely legible to non-technical stakeholders.
- **Integrate OSM (OpenStreetMap) data as default base layer** — pre-populate building footprints, road layouts, and zoning data from OSM for known locations; users can then focus on modifying specific elements rather than building scenes from scratch.
- **Define a cost-control policy for GPU jobs** — implement per-user job quotas, estimated cost display before queuing, and automatic downsampling for free tier users; without this, a viral spike produces unbounded infrastructure cost.
