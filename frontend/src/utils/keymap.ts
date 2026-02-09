// Keyboard key → move notation mapping
// Ported from original Pygame handleKeyPress keybindings

export const KEY_MAP: Record<string, string> = {
  // Basic moves
  'j': 'U',
  'f': "U'",
  'i': 'R',
  'k': "R'",
  'h': 'F',
  'g': "F'",
  's': 'D',
  'l': "D'",
  'd': 'L',
  'e': "L'",
  'w': 'B',
  'o': "B'",

  // Slice moves
  'x': "M'",
  '.': "M'",
  '5': 'M',
  '6': 'M',
  '2': 'E',
  '9': "E'",
  '1': "S'",
  '0': 'S',

  // Wide moves
  'u': 'Rw',
  'm': "Rw'",
  'r': "Lw'",
  'v': 'Lw',
  ',': 'Uw',
  'c': "Uw'",
  'z': 'Dw',
  '/': "Dw'",

  // Cube rotations
  't': 'x',
  'y': 'x',
  'b': "x'",
  'n': "x'",
  ';': 'y',
  'a': "y'",
  'p': 'z',
  'q': "z'",
};
