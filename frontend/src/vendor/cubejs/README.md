# Vendored: cubejs 1.3.2

[cubejs](https://github.com/ldez/cubejs) by Petri Lehtinen and Ludovic Fernandez, MIT
licensed (see `LICENSE`). It implements Kociemba's two-phase algorithm and powers Solve
mode via `src/solver/kociembaSolver.ts`.

## Why it's vendored instead of installed from npm

The published package declares the whole `npm@6` CLI as a runtime dependency, which it
never uses. Installing it added about 460 packages and 39 `npm audit` vulnerabilities (3
critical) to every install, Render's included. The solver itself is these two files.

## Local changes

Only the module wrapper, so Vite and Vitest can load the files as ES modules. Every
change is marked with a `vendored:` comment.

- `cube.js`: `module.exports = Cube` / `this.Cube = Cube` → `export default`.
- `solve.js`: `this.Cube || require('./cube')` → `import ... from './cube.js'`.
- `index.js` (new): imports both and re-exports `Cube`, like the package's own `index.js`.
- `index.d.ts` (new): TypeScript declarations for the subset of the API the app uses.

To update: copy `lib/cube.js` and `lib/solve.js` from the new release and reapply the two
wrapper edits above.
