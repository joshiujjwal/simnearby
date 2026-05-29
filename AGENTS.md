# AGENTS.md — SIMNearby

Agent instructions for automated coding tools (Codex, Copilot Workspace, etc.).

---

## Setup

```bash
# 1. Install Node dependencies
npm install

# 2. Install Python dependencies
pip install -r src/reconstruction/requirements.txt

# 3. Copy environment config
cp .env.example .env

# 4. Start backing services (requires Docker)
docker compose up -d postgres minio

# 5. Verify everything works
npm test && pytest tests/reconstruction/ -v
```

---

## Repository Layout

| Path | Purpose |
|---|---|
| `src/client/` | React + Three.js SPA |
| `src/server/` | Express REST API (TypeScript) |
| `src/reconstruction/` | Python ML pipeline |
| `tests/` | All tests — mirrors `src/` |
| `docs/spec.md` | Authoritative feature specification |
| `TODO.md` | Prioritised task list with evidence gates |
| `CLAUDE.md` | Detailed context, commands, gotchas |

---

## Code Style

### TypeScript (client + server)

- **Strict mode** (`"strict": true` in tsconfig)
- No `any` — use `unknown` + type guards if the shape is genuinely unknown
- Prefer `const` over `let`; never `var`
- Named exports only — no default exports (makes refactoring predictable)
- Zod for all external input validation (API request bodies, env vars)
- ESLint + Prettier enforced in CI — run `npm run lint` before committing
- Import order: node built-ins → external packages → internal (`@/...`) → relative

### React / Three.js

- React Three Fiber for Three.js integration; use `@react-three/drei` helpers
- Three.js objects instantiated in `scenes/` or inside `useRef`/`useMemo` — never bare in JSX
- Clean up Three.js resources in `useEffect` return function (`.dispose()`)
- Zustand for global state; React `useState` for purely local UI state

### Python

- Python 3.11+, type hints on all public functions
- `black` formatter, `ruff` linter, `mypy` for type checking
- `pathlib.Path` for all paths — never `os.path` string concatenation
- Functions < 50 lines; if longer, split into helpers
- `pytest` for all tests; `pytest-asyncio` for async pipeline tests

---

## Testing Instructions

### The Rule: Red Before Green

Every implementation task MUST have a failing test committed **before** the implementation:

```bash
# 1. Write test → confirm it fails
npm run test:client -- --reporter=verbose    # or
npm run test:server                          # or
pytest tests/reconstruction/ -v

# 2. Implement
# 3. Confirm tests pass
npm test && pytest tests/reconstruction/
```

### Test locations

| Code | Test |
|---|---|
| `src/client/components/Foo.tsx` | `tests/client/components/Foo.test.tsx` |
| `src/server/routes/ingest.ts` | `tests/server/routes/ingest.test.ts` |
| `src/reconstruction/pipeline/ingest.py` | `tests/reconstruction/pipeline/test_ingest.py` |

### Mocking

- HTTP: `msw` (Mock Service Worker) for client; `supertest` for server
- S3/object store: `moto` for Python; `@aws-sdk/client-s3` mock for Node
- Three.js: use `@react-three/test-renderer` for scene tests

---

## PR Instructions

Every PR must include **evidence** before it can be merged:

| Change type | Required evidence |
|---|---|
| New feature | Passing test output + screenshot or short video |
| Bug fix | Failing test that demonstrates the bug + fix that passes |
| Refactor | Before/after test run output showing no regressions |
| Performance | FPS or latency measurement before and after |

### PR checklist

- [ ] Tests written first (red commit exists before green commit)
- [ ] `npm test && pytest` passes locally
- [ ] `npm run lint && npm run typecheck` passes
- [ ] No `console.log` left in production code paths
- [ ] `CLAUDE.md` updated if a non-obvious gotcha was discovered
- [ ] `TODO.md` items checked off
- [ ] Evidence attached (screenshot / video / test output)

---

## What NOT to Do

- Do not refactor code that isn't directly related to the task at hand
- Do not remove or skip tests to make CI pass
- Do not add dependencies without updating `package.json` and noting the reason in the PR
- Do not commit `.env` files or any secrets
- Do not use `any` in TypeScript
- Do not create files outside the established structure without updating this file
