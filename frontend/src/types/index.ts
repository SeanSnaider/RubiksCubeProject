/**
 * Shared data shapes: the cube model, the app's modes, and recorded solves.
 *
 * The cube model mirrors the backend's (`backend/app/models/cube.py`): six 3x3
 * faces, each sticker named by the face it belongs to when solved.
 */

// Color represents a sticker - named after the face it belongs to when solved
export type Color = 'U' | 'D' | 'L' | 'R' | 'F' | 'B';

// A face is a 3x3 grid of colors
export type Face = Color[][];

// The complete cube state - all 6 faces
export interface CubeState {
  U: Face;  // Up (white)
  D: Face;  // Down (yellow)
  L: Face;  // Left (orange)
  R: Face;  // Right (red)
  F: Face;  // Front (green)
  B: Face;  // Back (blue)
}

/** The name of one of the six faces. */
export type FaceName = keyof CubeState;

/** A sticker on a cube being entered by hand: a color, or null while still blank. */
export type Sticker = Color | null;

/** A cube that may still have blank stickers, as built in Solve mode. */
export type EditableCube = Record<FaceName, Sticker[][]>;

/** The app's top-level tabs. */
export type AppMode = 'cube' | 'timer' | 'learn' | 'solve';

/** A recorded solve, as stored in localStorage (and by the backend API). */
export interface Solve {
  _id: string;
  time_ms: number;
  scramble: string;
  penalty: '+2' | 'DNF' | null;
  mode: 'cube' | 'timer';
  created_at: string;
}