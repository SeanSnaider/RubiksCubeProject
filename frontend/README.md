# Frontend

React 19 + TypeScript + Vite. See the [root README](../README.md) for what the app does and
how the pieces fit together.

## Commands

```bash
npm install
cp .env.example .env   # only needed if the API isn't at http://localhost:8000/api
npm run dev            # http://localhost:5173
npm test               # Vitest unit tests (move engine, validation, solver, formatting)
npm run lint
npm run build          # type-check, then build to dist/
```

The app runs entirely in the browser. Moves, scrambles, stats, history (localStorage) and
the Solve mode solver need no backend.

## Layout

| Path | What's there |
|---|---|
| `src/App.tsx` | Root component, mode switching, Cube mode |
| `src/components/` | One component per file, each with a CSS module |
| `src/utils/cubeMoves.ts` | Move engine, a port of `backend/app/services/cube_service.py` |
| `src/utils/cubeValidation.ts` | Facelet serialization and the solvability checks for entered cubes |
| `src/solver/` | Kociemba two-phase solver, run in a Web Worker |
| `src/vendor/cubejs/` | Vendored cubejs solver (MIT) |
| `src/utils/*.test.ts`, `src/solver/*.test.ts` | Unit tests |

## Dependencies worth knowing about

- **cubejs** (vendored in `src/vendor/cubejs/`): the Kociemba two-phase solver used by
  Solve mode. It's vendored rather than installed because the npm package drags in the
  whole `npm@6` CLI as a runtime dependency; that directory's README has the details and
  how to update it. It does not validate its input, so always run `findCubeProblems()`
  first, which `solveCube()` does for you.
- **vitest** (dev): unit test runner; shares Vite's config.
