# SIMNearby — Feature Specification

_Last updated: Phase 0 (pre-implementation)_

---

## 1. Overview

**Problem:** Urban planners, architects, community groups, and curious citizens have no easy way to visualize "what-if" changes to real city streets. Existing tools require specialist software, expensive licences, or manually-built 3D models.

**Solution:** SIMNearby allows anyone to:
1. Record a short video of a real location (street, plaza, park)
2. Automatically reconstruct a 3D scene from that footage
3. Layer urban planning changes onto the scene via a drag-and-drop editor
4. Explore the result in an immersive VR/3D viewer

**Primary users:** urban planners, architecture students, civic tech communities, city councils.

---

## 2. Functional Requirements

### 2.1 Video Ingest

- [ ] Accept video uploads: MP4, MOV, WebM; max 500 MB
- [ ] Extract frames at configurable FPS (default: 2 fps)
- [ ] Parse GPS metadata from video EXIF / sidecar file if available
- [ ] Persist frames to object store (S3-compatible)
- [ ] Return a `jobId` immediately; status polled via `GET /api/ingest/:jobId/status`
- [ ] Job states: `queued → extracting → reconstructing → complete | failed`
- [ ] Failed jobs expose an error message and partial artifact URL if available

### 2.2 3D Reconstruction

- [ ] Structure-from-Motion (SfM) via COLMAP or Open3D to produce a sparse point cloud
- [ ] Dense reconstruction to mesh (MVS or Gaussian Splatting bake-to-mesh)
- [ ] Export as `.glb` (binary glTF 2.0) for web compatibility
- [ ] Reconstruction time target: < 5 min for a 30-second, 60-frame video on GPU
- [ ] Mesh simplification step: target < 200k triangles for real-time rendering
- [ ] Store asset in object store; signed URL valid for 24h

### 2.3 What-If Scenario Editor

- [ ] Load reconstructed scene into Three.js viewer
- [ ] Urban element palette: buildings (low/mid/high-rise), trees, benches, parks, cycle lanes, bus stops
- [ ] Drag element from palette → ray-cast onto scene surface → place at hit point
- [ ] Selected elements: translate (XYZ), rotate (Y), scale (uniform)
- [ ] Delete selected element (Delete / Backspace key)
- [ ] Undo / redo (Ctrl+Z / Ctrl+Y), minimum 20-step history
- [ ] Scenario serialised as JSON: `{ sceneId, elements: [{ type, position, rotation, scale }] }`
- [ ] `POST /api/scenarios` creates a scenario; `GET /api/scenarios/:id` retrieves it
- [ ] Scenario URL: `simnearby.app/scene/:sceneId?scenario=:scenarioId`
- [ ] Fork scenario: create a copy owned by the current user

### 2.4 3D / VR Viewer

- [ ] Orbit camera (mouse / touch) in desktop mode
- [ ] WebXR immersive-vr session with `<VRButton />`
- [ ] In VR: controller ray-cast for element interaction, teleport locomotion
- [ ] Environment: HDRI sky dome, dynamic sun position (time of day slider)
- [ ] Shadows: directional light + shadow map (configurable quality)
- [ ] Performance target: ≥ 60 FPS desktop, ≥ 72 FPS in VR headset

### 2.5 User Accounts

- [ ] Email/password registration and login
- [ ] JWT access token (15 min) + refresh token (7 days)
- [ ] User owns their scenes and scenarios
- [ ] Public / private scenario visibility toggle
- [ ] Anonymous access: view public scenarios without logging in

---

## 3. Non-Functional Requirements

- [ ] API response time p95 < 200ms (excluding file upload and job status)
- [ ] Video upload progress streamed to client (not a single blocking request)
- [ ] Scene `.glb` delivered via CDN; signed URL redirect
- [ ] No PII stored beyond email + hashed password
- [ ] OWASP Top 10 mitigations applied at API layer
- [ ] Accessible: WCAG 2.1 AA for all 2D UI panels

---

## 4. Data Model

### Scene

```ts
type Scene = {
  id: string;           // UUID
  ownerId: string;
  videoKey: string;     // object store key for source video
  status: 'queued' | 'extracting' | 'reconstructing' | 'complete' | 'failed';
  assetUrl: string | null;   // signed URL to .glb
  frameCount: number;
  gpsOrigin: { lat: number; lng: number } | null;
  createdAt: Date;
  updatedAt: Date;
};
```

### Scenario

```ts
type ScenarioElement = {
  id: string;           // UUID
  type: UrbanElementType;
  position: [number, number, number];
  rotation: [number, number, number];   // Euler XYZ radians
  scale: number;
};

type Scenario = {
  id: string;
  sceneId: string;
  ownerId: string;
  title: string;
  isPublic: boolean;
  elements: ScenarioElement[];
  createdAt: Date;
  updatedAt: Date;
};

type UrbanElementType =
  | 'building_low' | 'building_mid' | 'building_high'
  | 'tree_oak' | 'tree_birch'
  | 'park_grass' | 'bench' | 'bus_stop' | 'cycle_lane';
```

### User

```ts
type User = {
  id: string;
  email: string;
  passwordHash: string;
  createdAt: Date;
};
```

---

## 5. API Design

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register` | — | Create account |
| POST | `/api/auth/login` | — | Issue JWT |
| POST | `/api/auth/refresh` | refresh token | Rotate tokens |
| POST | `/api/ingest` | JWT | Upload video, returns `{ jobId }` |
| GET | `/api/ingest/:jobId/status` | JWT | Poll job state |
| GET | `/api/scenes/:sceneId` | optional JWT | Get scene metadata |
| GET | `/api/scenes/:sceneId/asset` | JWT | Get signed URL to `.glb` |
| GET | `/api/scenes` | JWT | List user's scenes |
| POST | `/api/scenarios` | JWT | Create scenario |
| GET | `/api/scenarios/:id` | optional JWT | Get scenario |
| PUT | `/api/scenarios/:id` | JWT | Update scenario |
| POST | `/api/scenarios/:id/fork` | JWT | Fork scenario |
| DELETE | `/api/scenarios/:id` | JWT | Delete scenario |

---

## 6. Test Plan

### Unit Tests

- Frame extraction: given a 10-frame synthetic video, `extract_frames` returns exactly 10 frames
- GPS parser: EXIF with known coordinates returns matching `gpsOrigin`
- `scenarioStore`: each action (add, remove, update, undo, redo) produces correct state
- `SceneLoader`: resolves with a `THREE.Group` given a mock `.glb` URL
- JWT utilities: token generation, validation, expiry

### Integration Tests

- `POST /api/ingest` → job enqueued → frames in object store (mock S3)
- `POST /api/scenarios` → `GET /api/scenarios/:id` round-trip preserves all fields
- Auth flow: register → login → protected route → token refresh

### Edge Cases

- Video with no GPS metadata: scene created without `gpsOrigin`, no error
- Video too short (< 5 frames): job fails with `insufficient_frames` error code
- Reconstruction failure (COLMAP exits non-zero): job status → `failed`, error message set
- Scenario with 0 elements: valid, serialises to `{ elements: [] }`
- Concurrent edits to same scenario: last-write-wins (document in spec; CRDTs in parking lot)

---

## 7. Open Questions

- [ ] **Reconstruction quality vs. speed trade-off**: should we offer a "fast draft" mode (2–3 min) and "high quality" mode (15+ min)?
- [ ] **Asset licensing**: what CC0 GLB libraries to bundle? (Sketchfab, Poly Haven, KenShape)
- [ ] **GPS alignment**: how to align the reconstructed mesh with real-world coordinates? (COLMAP GPS priors vs. manual alignment UI)
- [ ] **Mobile upload**: do we support recording directly in-browser via `getUserMedia`? Or upload-only to start?
- [ ] **Gaussian Splatting**: `.splat` files are not natively renderable by Three.js — use `three-gaussian-splat` lib or bake to mesh?
- [ ] **Collaboration**: is real-time multi-user editing in scope for v1?
