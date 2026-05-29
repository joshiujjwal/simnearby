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
