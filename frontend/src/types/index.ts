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

export type TimerPhase = 'idle' | 'inspection' | 'running' | 'stopped';

export interface Solve {
  _id: string;
  time_ms: number;
  scramble: string;
  penalty: '+2' | 'DNF' | null;
  created_at: string;
}