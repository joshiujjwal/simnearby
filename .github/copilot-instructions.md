# GitHub Copilot Instructions — SIMNearby

## Project Summary

SIMNearby records city video, reconstructs a 3D scene via ML, and lets users apply urban planning
"what-if" changes (buildings, parks, roads) in an interactive Three.js / WebXR viewer.

Stack: **TypeScript · React 18 · Three.js / React Three Fiber · Node.js · Express · Python 3.11**

---

## TypeScript Conventions

- Strict mode always on; no `any`, no implicit `any`
- Named exports only — no `export default`
- Zod schemas for all API input validation
- Colocate schema next to the route it validates
- Services (`src/server/services/`) must not import Express types
- Types live in `src/client/types/` (shared) or colocated with the module they describe

## React Conventions

- Functional components only; no class components
- Hooks in `src/client/hooks/`; one hook per concept
- Three.js scene logic in `src/client/scenes/`; never instantiate Three.js objects in JSX bodies
- Use `@react-three/drei` helpers (OrbitControls, Environment, useGLTF) before rolling your own
- Clean up Three.js objects in `useEffect` cleanup via `.dispose()`
- State: Zustand (`src/client/store/`) for cross-component state; `useState` for local UI state only

## Python Conventions

- Type hints on every public function (enforced by `mypy`)
- `pathlib.Path` for file paths everywhere
- `black` formatting, `ruff` linting
- Async pipeline steps use `asyncio`; sync utilities in `utils/`
- COLMAP is invoked as a subprocess; capture stdout/stderr and log on failure

## Testing Conventions

- **Write the failing test first** — Copilot suggestions for tests should always precede implementation suggestions
- Client tests: Vitest + `@testing-library/react` + `@react-three/test-renderer`
- Server tests: Jest + Supertest
- Python tests: pytest + pytest-asyncio
- Mock S3 with `moto` (Python) and AWS SDK mocks (Node)
- Test file mirrors source file path: `src/X` → `tests/X`

## Three.js / WebXR Conventions

- Use `useFrame` for per-frame logic; avoid `setInterval`/`setTimeout` in render paths
- Enable shadows only on the primary directional light
- All async asset loads (GLTFLoader, TextureLoader) go inside `useEffect` or `useMemo` with Suspense
- WebXR entry via `@react-three/xr`; always provide a fallback for non-XR browsers
- Dispose geometry and material when a component unmounts

## Boundaries

- Do not refactor files unrelated to the current task
- Do not delete or weaken existing tests
- Do not add new npm/pip packages without a clear need; prefer stdlib or already-listed deps
- Do not generate placeholder `// TODO` comments — if something isn't implemented, write a failing test instead
- Do not use `console.log` in production code paths (use a proper logger)
- Do not hardcode secrets; use `process.env` variables defined in `.env.example`
