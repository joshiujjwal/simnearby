# SIMNearby — Claude Context

> Keep this file under 200 lines. Update it when you discover something non-obvious.

---

## What This Project Does

Record a city video → ML 3D reconstruction → interactive Three.js what-if editor → WebXR viewer.  
See `docs/spec.md` for the full feature spec.

---

## Commands

```bash
# Install all JS/TS dependencies (monorepo workspaces)
npm install

# Run all TS tests
npm test

# Run only client tests (Vitest)
npm run test:client

# Run only server tests (Jest)
npm run test:server

# Run Python reconstruction tests
pytest tests/reconstruction/ -v

# Lint (ESLint + Prettier check)
npm run lint

# Type-check (tsc --noEmit across all workspaces)
npm run typecheck

# Start dev environment (client HMR + server watch)
npm run dev

# Start Python reconstruction worker
cd src/reconstruction && python -m pipeline.worker

# Build for production
npm run build

# Docker Compose (Postgres + MinIO + services)
docker compose up
```

> ⚠️ TODO: Commands above are forward-declared. Update as you set up each workspace.

---

## Directory Map

```
src/client/            React + Three.js SPA
  components/          Pure UI (panels, buttons, overlays)
  hooks/               Custom hooks (useScene, useScenario, useXR)
  scenes/              Three.js scene graphs, loaders, XR setup
  store/               Zustand slices (scenarioStore, uiStore, authStore)
  utils/               Geo helpers, mesh utils, debounce, etc.

src/server/            Express REST API
  routes/              Thin handlers — validate input, call service, return response
  services/            Business logic — no Express types leak here
  middleware/          Auth (JWT), error handling, rate limiting, multipart

src/reconstruction/    Python ML pipeline (run as a separate worker process)
  pipeline/            Orchestration: ingest → SfM → dense → export
  models/              COLMAP wrapper, Gaussian Splatting wrapper
  utils/               Frame extraction (OpenCV), GPS parsing, mesh simplification

tests/                 Mirrors src/ — unit and integration tests
docs/                  spec.md, ADRs, perf baselines, VR compat notes
.github/               CI workflows, Copilot instructions
```

---

## Non-Obvious Conventions

### TypeScript
- Zod schemas live next to the type they validate (`routes/ingest.schema.ts` beside `routes/ingest.ts`)
- Never import Express types in `services/` — services take plain objects, return plain objects
- Three.js objects are created in `scenes/`, **never** in React component bodies (causes re-creation on render)

### Python
- All pipeline functions are **pure or explicitly async** — no global mutable state
- Use `pathlib.Path` everywhere, never raw strings for paths
- Type hints required on all public functions; run `mypy` before committing

### Three.js / React Three Fiber
- Use `useFrame` for per-frame updates, never `setInterval`
- Dispose geometry/materials in `useEffect` cleanup to avoid GPU memory leaks
- Shadows are expensive — only enable on the main directional light

### Testing
- **Red before green**: the failing test must exist in a commit before the implementation
- Mock S3 with `moto` in Python; use `msw` (Mock Service Worker) in client tests
- Never use `any` in tests — if you need it, the type is wrong

### State
- `scenarioStore` is the single source of truth for what's in the 3D scene
- Server is authoritative after save; optimistic updates are fine, but handle failures

---

## Workflow

1. **Read `TODO.md`** — find the next unchecked task in the current phase
2. **Run existing tests** — `npm test && pytest tests/reconstruction/` must be green before you start
3. **Write the failing test** — commit it with message `test: <description> (red)`
4. **Implement** — minimal code to make the test pass; no gold-plating
5. **Commit** — `feat/fix: <description> (green)`
6. **Update this file** — if you learned something non-obvious, add it to "Non-Obvious Conventions"
7. **Check the evidence gate** — if this was the last task in a phase, confirm all evidence is in place before moving on

---

## Known Gotchas

- COLMAP requires CUDA for GPU acceleration; fallback to CPU is 10–20× slower
- `.glb` files from Open3D may have flipped normals — apply `mesh.fix_normals()` after export
- Three.js `GLTFLoader` is async; wrap in a `Suspense` boundary in React
- WebXR requires HTTPS even on localhost — use `vite --https` or a local cert
- `moto` S3 mock must be started before imports that initialise boto3 clients

---

## Environment Variables

See `.env.example` (TODO: create this file in Phase 0).

Key vars:
```
DATABASE_URL=postgres://...
S3_BUCKET=simnearby-assets
S3_ENDPOINT=...
JWT_SECRET=...
RECONSTRUCTION_WORKER_QUEUE=...
```
