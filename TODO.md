# SIMNearby — Task Breakdown

## How to Use This File

Each task follows this loop:
1. **Red** — write the test(s) for the task; confirm they fail
2. **Green** — implement until tests pass
3. **Review** — manually inspect the diff; does it do exactly what the task says?
4. **Commit** — descriptive message, reference the TODO item (e.g. `feat(ingest): frame extraction #3`)
5. **Update context** — if you learned something surprising, add it to `CLAUDE.md` or `AGENTS.md`
6. **Gate** — do not start the next phase until all tasks in this phase are ✅ and reviewed

---

## Phase 0: Foundation ⬜

> Goal: a running repo with CI, linting, testing, and a "hello world" render.

- [ ] **0.1** Init `package.json` with workspaces: `src/client`, `src/server`
- [ ] **0.2** Add TypeScript (`tsconfig.json` per workspace), ESLint + Prettier configs
- [ ] **0.3** Set up Vitest for `src/client` with a smoke test (`renders without crashing`)
- [ ] **0.4** Set up Jest for `src/server` with a smoke test (health-check route returns 200)
- [ ] **0.5** Set up pytest for `src/reconstruction` with a smoke test (`import pipeline` succeeds)
- [ ] **0.6** GitHub Actions CI: install → lint → test on push to `main` and all PRs
- [ ] **0.7** Render a bare Three.js canvas (`<SceneCanvas />`) in the client with no errors
- [ ] **0.8** Review all AI config files (this file, CLAUDE.md, AGENTS.md, copilot-instructions.md) — edit anything that doesn't fit

**Evidence gate:** CI is green on `main`. `npm test && pytest` both pass locally.

---

## Phase 1: Video Ingest Pipeline ⬜

> Goal: upload a video file → extract frames → store frames + metadata in DB/object store.

- [ ] **1.1** Define `VideoIngestJob` TypeScript type and Zod schema (server)
- [ ] **1.2** Write tests: POST `/api/ingest` with a mock video returns a job ID (unit + integration)
- [ ] **1.3** Implement `POST /api/ingest` route — accepts `multipart/form-data`, enqueues job
- [ ] **1.4** Write tests: Python `extract_frames(video_path) → List[Frame]` extracts correct frame count
- [ ] **1.5** Implement `reconstruction/pipeline/ingest.py` — OpenCV frame extraction, GPS EXIF parsing
- [ ] **1.6** Write tests: frames are uploaded to object store (mock S3 with `moto`)
- [ ] **1.7** Implement S3 upload step in ingest pipeline
- [ ] **1.8** Expose `GET /api/ingest/:jobId/status` endpoint with tests
- [ ] **1.9** Build `<UploadPanel />` React component — drag-drop video + progress indicator
- [ ] **1.10** Write Vitest tests for `<UploadPanel />` upload states (idle, uploading, error, done)
- [ ] **1.11** Manual test: upload a short city clip end-to-end; confirm frames land in object store

**Evidence gate:** integration test passes with a real (small) test video. Screenshot of frames in object store.

---

## Phase 2: 3D Reconstruction ⬜

> Goal: frames in → 3D scene mesh (.glb/.ply) out, available via API.

- [ ] **2.1** Write spec for reconstruction pipeline in `docs/spec.md` (update "Reconstruction" section)
- [ ] **2.2** Write tests: `run_reconstruction(frames_dir) → SceneAsset` returns a valid asset path
- [ ] **2.3** Implement thin wrapper around **COLMAP** (or Open3D) for SfM point cloud
- [ ] **2.4** Implement NeRF/Gaussian-Splatting export step (initial: bake to mesh .glb)
- [ ] **2.5** Write tests: exported `.glb` is valid (non-zero file size, parses with `trimesh`)
- [ ] **2.6** Store result in object store; update job status to `complete` with asset URL
- [ ] **2.7** Expose `GET /api/scenes/:sceneId/asset` to return signed URL
- [ ] **2.8** Write integration test for the full reconstruct → fetch asset flow
- [ ] **2.9** Manual test: reconstruct from a 10-second clip; inspect mesh in Blender

**Evidence gate:** A real reconstructed `.glb` is committed to `tests/fixtures/` (small clip). CI passes.

---

## Phase 3: Three.js Scene Viewer ⬜

> Goal: load a reconstructed scene in Three.js and navigate it in the browser.

- [ ] **3.1** Write tests: `SceneLoader.load(url)` resolves to a `THREE.Group` with at least one mesh
- [ ] **3.2** Implement `src/client/scenes/SceneLoader.ts` — loads `.glb`, sets up lighting + shadows
- [ ] **3.3** Write tests: `<SceneViewer sceneUrl={...} />` mounts without throwing
- [ ] **3.4** Implement `<SceneViewer />` with orbit controls (React Three Fiber + `@react-three/drei`)
- [ ] **3.5** Add `<SceneViewer />` to main app routing; wire to scene asset URL from API
- [ ] **3.6** Performance baseline: measure FPS on a reference device; document in `docs/perf-baseline.md`
- [ ] **3.7** Manual test: navigate the loaded scene; confirm mesh renders correctly

**Evidence gate:** Screenshot of reconstructed scene rendered in browser. FPS > 30 on target device.

---

## Phase 4: What-If Editor ⬜

> Goal: users can add/remove/swap urban elements (buildings, parks, roads) on the 3D scene.

- [ ] **4.1** Define `ScenarioElement` and `Scenario` types; write serialization tests
- [ ] **4.2** Build Zustand `scenarioStore` with actions: `addElement`, `removeElement`, `updateElement`
- [ ] **4.3** Write tests for all store actions (pure unit tests, no DOM)
- [ ] **4.4** Implement `<ElementPalette />` — draggable tile list of urban asset types
- [ ] **4.5** Implement `<SceneDrop />` — Three.js ray-cast plane to place elements on scene surface
- [ ] **4.6** Write tests: placing an element updates `scenarioStore` and re-renders scene
- [ ] **4.7** Bundle a small asset library (CC0 GLB models: tree, bench, building shell, park)
- [ ] **4.8** Implement `POST /api/scenarios` and `GET /api/scenarios/:id` (CRUD with tests)
- [ ] **4.9** Save/load scenario to/from API; URL param `?scenario=<id>` restores state
- [ ] **4.10** Manual test: build a "what-if green space" scenario on a real reconstructed scene

**Evidence gate:** Screen recording of a full what-if edit session saved and reloaded via URL.

---

## Phase 5: WebXR / VR Mode ⬜

> Goal: the scene viewer works in an immersive WebXR session (headset or cardboard).

- [ ] **5.1** Write tests: `<XRButton />` renders; `navigator.xr` mock returns supported session types
- [ ] **5.2** Integrate `@react-three/xr` — add `<VRButton />` and `<XR>` wrapper
- [ ] **5.3** Implement basic controller ray-cast for element placement in VR
- [ ] **5.4** Add teleport locomotion (point + click to move)
- [ ] **5.5** Test on Meta Quest browser via ngrok tunnel; document issues in `docs/vr-compat.md`
- [ ] **5.6** Fallback to 3D orbit mode when WebXR not supported

**Evidence gate:** Video recording of VR mode working on at least one headset.

---

## Phase 6: Polish & Harden ⬜

- [ ] **6.1** Auth: JWT login/register (server tests first)
- [ ] **6.2** Rate limiting on ingest endpoint
- [ ] **6.3** Lighthouse score ≥ 90 on desktop (performance, accessibility)
- [ ] **6.4** Error boundaries in React; server-side error logging (Sentry or similar)
- [ ] **6.5** Docker Compose for local dev (Postgres + MinIO + Node + Python worker)
- [ ] **6.6** README accuracy pass — every command must work on a clean machine

---

## Phase 7: Ship ⬜

- [ ] **7.1** Deploy backend to Railway / Fly.io; document in `docs/deploy.md`
- [ ] **7.2** Deploy frontend to Vercel
- [ ] **7.3** Deploy Python worker to Modal / Replicate
- [ ] **7.4** Set up production object store (Cloudflare R2 or AWS S3)
- [ ] **7.5** Smoke-test production URL end-to-end
- [ ] **7.6** Tag `v0.1.0` release

---

## Parking Lot 🅿️

> Ideas to revisit — not blocking any phase.

- Real-time collaborative editing (CRDTs)
- AI-generated urban suggestions ("add bike lanes here")
- Time-of-day lighting simulation
- Procedural building generation from floor plans
- Mobile AR overlay (map scenario onto live camera)
- City comparison mode (two scenarios side-by-side)

---

## Lessons Learned 📝

> Fill this in as you go. Each entry = one thing that surprised you or saved you time.

<!-- Example:
- **2024-01-15** — COLMAP crashes on videos < 20 frames. Minimum: extract 30+ frames. -->
