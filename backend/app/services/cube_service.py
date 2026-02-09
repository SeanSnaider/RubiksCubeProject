"""
Cube Service - Business Logic Layer

This service contains all the cube manipulation logic extracted from
the original Pygame implementation. It's now stateless - instead of
modifying a class instance, each function takes a state dict and
returns a new state dict.

Key concepts:
- Stateless functions (no class, just functions that transform data)
- Deep copy to avoid mutating input (immutability)
- Pure functions: same input always produces same output
"""
import copy
import random

# Available moves for scramble generation
BASIC_MOVES = ['U', "U'", 'U2', 'R', "R'", 'R2', 'F', "F'", 'F2',
               'D', "D'", 'D2', 'L', "L'", 'L2', 'B', "B'", 'B2']


def get_solved_state() -> dict:
    """
    Return a solved cube state.

    Each face is a 3x3 grid where every cell contains
    the letter of that face (representing its color).
    """
    return {
        'U': [['U'] * 3 for _ in range(3)],  # White (Up)
        'D': [['D'] * 3 for _ in range(3)],  # Yellow (Down)
        'L': [['L'] * 3 for _ in range(3)],  # Orange (Left)
        'R': [['R'] * 3 for _ in range(3)],  # Red (Right)
        'F': [['F'] * 3 for _ in range(3)],  # Green (Front)
        'B': [['B'] * 3 for _ in range(3)],  # Blue (Back)
    }


def rotate_face_cw(face: list) -> list:
    """
    Rotate a 3x3 face 90 degrees clockwise.

    The pattern: new[row][col] = old[2-col][row]
    """
    return [
        [face[2][0], face[1][0], face[0][0]],
        [face[2][1], face[1][1], face[0][1]],
        [face[2][2], face[1][2], face[0][2]],
    ]


def rotate_face_ccw(face: list) -> list:
    """
    Rotate a 3x3 face 90 degrees counter-clockwise.
    This is simply three clockwise rotations.
    """
    result = face
    for _ in range(3):
        result = rotate_face_cw(result)
    return result


# =============================================================================
# BASIC FACE MOVES (U, D, L, R, F, B and their primes)
# =============================================================================

def move_u(state: dict) -> dict:
    """
    U move: Rotate the Up (white) face clockwise.
    Also cycles the top row of F → L → B → R → F
    """
    state = copy.deepcopy(state)

    # Rotate the U face itself
    state['U'] = rotate_face_cw(state['U'])

    # Cycle the adjacent edges (top rows of surrounding faces)
    # The top row of Front goes to Left, Left to Back, Back to Right, Right to Front
    temp = state['F'][0][:]
    state['F'][0] = state['R'][0][:]
    state['R'][0] = state['B'][0][:]
    state['B'][0] = state['L'][0][:]
    state['L'][0] = temp

    return state


def move_u_prime(state: dict) -> dict:
    """U' move: Three U moves equals U'"""
    for _ in range(3):
        state = move_u(state)
    return state


def move_d(state: dict) -> dict:
    """
    D move: Rotate the Down (yellow) face clockwise.
    Cycles the bottom row of F → R → B → L → F
    """
    state = copy.deepcopy(state)

    state['D'] = rotate_face_cw(state['D'])

    # Bottom rows cycle in opposite direction to U
    temp = state['F'][2][:]
    state['F'][2] = state['L'][2][:]
    state['L'][2] = state['B'][2][:]
    state['B'][2] = state['R'][2][:]
    state['R'][2] = temp

    return state


def move_d_prime(state: dict) -> dict:
    """D' move"""
    for _ in range(3):
        state = move_d(state)
    return state


def move_r(state: dict) -> dict:
    """
    R move: Rotate the Right (red) face clockwise.
    Cycles the right column of U → F → D → B (B is mirrored)
    """
    state = copy.deepcopy(state)

    state['R'] = rotate_face_cw(state['R'])

    # The right column cycles through U, F, D, B
    # Note: B face is "upside down" relative to others
    temp = [state['U'][0][2], state['U'][1][2], state['U'][2][2]]

    # U right col <- F right col
    state['U'][0][2] = state['F'][0][2]
    state['U'][1][2] = state['F'][1][2]
    state['U'][2][2] = state['F'][2][2]

    # F right col <- D right col
    state['F'][0][2] = state['D'][0][2]
    state['F'][1][2] = state['D'][1][2]
    state['F'][2][2] = state['D'][2][2]

    # D right col <- B left col (reversed!)
    state['D'][0][2] = state['B'][2][0]
    state['D'][1][2] = state['B'][1][0]
    state['D'][2][2] = state['B'][0][0]

    # B left col <- temp (reversed!)
    state['B'][0][0] = temp[2]
    state['B'][1][0] = temp[1]
    state['B'][2][0] = temp[0]

    return state


def move_r_prime(state: dict) -> dict:
    """R' move"""
    for _ in range(3):
        state = move_r(state)
    return state


def move_l(state: dict) -> dict:
    """
    L move: Rotate the Left (orange) face clockwise.
    """
    state = copy.deepcopy(state)

    state['L'] = rotate_face_cw(state['L'])

    # Left column cycles through U, B, D, F
    temp = [state['U'][0][0], state['U'][1][0], state['U'][2][0]]

    # U left col <- B right col (reversed!)
    state['U'][0][0] = state['B'][2][2]
    state['U'][1][0] = state['B'][1][2]
    state['U'][2][0] = state['B'][0][2]

    # B right col <- D left col (reversed!)
    state['B'][0][2] = state['D'][2][0]
    state['B'][1][2] = state['D'][1][0]
    state['B'][2][2] = state['D'][0][0]

    # D left col <- F left col
    state['D'][0][0] = state['F'][0][0]
    state['D'][1][0] = state['F'][1][0]
    state['D'][2][0] = state['F'][2][0]

    # F left col <- temp
    state['F'][0][0] = temp[0]
    state['F'][1][0] = temp[1]
    state['F'][2][0] = temp[2]

    return state


def move_l_prime(state: dict) -> dict:
    """L' move"""
    for _ in range(3):
        state = move_l(state)
    return state


def move_f(state: dict) -> dict:
    """
    F move: Rotate the Front (green) face clockwise.
    """
    state = copy.deepcopy(state)

    state['F'] = rotate_face_cw(state['F'])

    # The bottom row of U, right col of L, top row of D, left col of R cycle
    temp = [state['U'][2][0], state['U'][2][1], state['U'][2][2]]

    # U bottom row <- L right col (rotated)
    state['U'][2][0] = state['L'][2][2]
    state['U'][2][1] = state['L'][1][2]
    state['U'][2][2] = state['L'][0][2]

    # L right col <- D top row
    state['L'][0][2] = state['D'][0][0]
    state['L'][1][2] = state['D'][0][1]
    state['L'][2][2] = state['D'][0][2]

    # D top row <- R left col (rotated)
    state['D'][0][0] = state['R'][2][0]
    state['D'][0][1] = state['R'][1][0]
    state['D'][0][2] = state['R'][0][0]

    # R left col <- temp
    state['R'][0][0] = temp[0]
    state['R'][1][0] = temp[1]
    state['R'][2][0] = temp[2]

    return state


def move_f_prime(state: dict) -> dict:
    """F' move"""
    for _ in range(3):
        state = move_f(state)
    return state


def move_b(state: dict) -> dict:
    """
    B move: Rotate the Back (blue) face clockwise.
    """
    state = copy.deepcopy(state)

    state['B'] = rotate_face_cw(state['B'])

    # Cycles U top row, R right col, D bottom row, L left col
    temp = [state['U'][0][0], state['U'][0][1], state['U'][0][2]]

    # U top row <- R right col
    state['U'][0][0] = state['R'][0][2]
    state['U'][0][1] = state['R'][1][2]
    state['U'][0][2] = state['R'][2][2]

    # R right col <- D bottom row (reversed)
    state['R'][0][2] = state['D'][2][2]
    state['R'][1][2] = state['D'][2][1]
    state['R'][2][2] = state['D'][2][0]

    # D bottom row <- L left col
    state['D'][2][0] = state['L'][0][0]
    state['D'][2][1] = state['L'][1][0]
    state['D'][2][2] = state['L'][2][0]

    # L left col <- temp (reversed)
    state['L'][0][0] = temp[2]
    state['L'][1][0] = temp[1]
    state['L'][2][0] = temp[0]

    return state


def move_b_prime(state: dict) -> dict:
    """B' move"""
    for _ in range(3):
        state = move_b(state)
    return state


# =============================================================================
# SLICE MOVES (M, E, S)
# =============================================================================

def move_m(state: dict) -> dict:
    """
    M move: Middle slice, turns like L.
    The middle column (between L and R) rotates in the same direction as L.
    """
    state = copy.deepcopy(state)

    # Middle column (col 1) cycles: U → F → D → B (with B reversed)
    temp = [state['U'][0][1], state['U'][1][1], state['U'][2][1]]

    # U middle col <- B middle col (reversed)
    state['U'][0][1] = state['B'][2][1]
    state['U'][1][1] = state['B'][1][1]
    state['U'][2][1] = state['B'][0][1]

    # B middle col <- D middle col (reversed)
    state['B'][0][1] = state['D'][2][1]
    state['B'][1][1] = state['D'][1][1]
    state['B'][2][1] = state['D'][0][1]

    # D middle col <- F middle col
    state['D'][0][1] = state['F'][0][1]
    state['D'][1][1] = state['F'][1][1]
    state['D'][2][1] = state['F'][2][1]

    # F middle col <- temp (from U)
    state['F'][0][1] = temp[0]
    state['F'][1][1] = temp[1]
    state['F'][2][1] = temp[2]

    return state


def move_m_prime(state: dict) -> dict:
    """M' move: opposite of M"""
    for _ in range(3):
        state = move_m(state)
    return state


def move_e(state: dict) -> dict:
    """
    E move: Equator slice, turns like D.
    The middle row (between U and D) rotates in same direction as D.
    """
    state = copy.deepcopy(state)

    # Middle row (row 1) cycles: F → L → B → R → F
    temp = state['F'][1][:]
    state['F'][1] = state['L'][1][:]
    state['L'][1] = state['B'][1][:]
    state['B'][1] = state['R'][1][:]
    state['R'][1] = temp

    return state


def move_e_prime(state: dict) -> dict:
    """E' move"""
    for _ in range(3):
        state = move_e(state)
    return state


def move_s(state: dict) -> dict:
    """
    S move: Standing slice, turns like F.
    The middle layer (between F and B) rotates in same direction as F.
    """
    state = copy.deepcopy(state)

    # Middle row of U, middle col of L, middle row of D, middle col of R cycle
    temp = [state['U'][1][0], state['U'][1][1], state['U'][1][2]]

    # U middle row <- L middle col (rotated)
    state['U'][1][0] = state['L'][2][1]
    state['U'][1][1] = state['L'][1][1]
    state['U'][1][2] = state['L'][0][1]

    # L middle col <- D middle row
    state['L'][0][1] = state['D'][1][0]
    state['L'][1][1] = state['D'][1][1]
    state['L'][2][1] = state['D'][1][2]

    # D middle row <- R middle col (rotated)
    state['D'][1][0] = state['R'][2][1]
    state['D'][1][1] = state['R'][1][1]
    state['D'][1][2] = state['R'][0][1]

    # R middle col <- temp
    state['R'][0][1] = temp[0]
    state['R'][1][1] = temp[1]
    state['R'][2][1] = temp[2]

    return state


def move_s_prime(state: dict) -> dict:
    """S' move"""
    for _ in range(3):
        state = move_s(state)
    return state


# =============================================================================
# MOVE DISPATCHER
# =============================================================================

# Maps move notation to functions
MOVE_MAP = {
    'U': move_u, "U'": move_u_prime, 'U2': lambda s: move_u(move_u(s)),
    'D': move_d, "D'": move_d_prime, 'D2': lambda s: move_d(move_d(s)),
    'R': move_r, "R'": move_r_prime, 'R2': lambda s: move_r(move_r(s)),
    'L': move_l, "L'": move_l_prime, 'L2': lambda s: move_l(move_l(s)),
    'F': move_f, "F'": move_f_prime, 'F2': lambda s: move_f(move_f(s)),
    'B': move_b, "B'": move_b_prime, 'B2': lambda s: move_b(move_b(s)),
    'M': move_m, "M'": move_m_prime, 'M2': lambda s: move_m(move_m(s)),
    'E': move_e, "E'": move_e_prime, 'E2': lambda s: move_e(move_e(s)),
    'S': move_s, "S'": move_s_prime, 'S2': lambda s: move_s(move_s(s)),
}


def parse_moves(moves: str) -> list:
    """
    Parse a move string like "R U R' U'" into individual moves.

    Handles:
    - Single moves: R, U, F, etc.
    - Prime moves: R', U', F', etc.
    - Double moves: R2, U2, F2, etc.
    """
    result = []
    i = 0
    moves = moves.strip()

    while i < len(moves):
        # Skip whitespace
        if moves[i].isspace():
            i += 1
            continue

        # Get the base move letter
        if moves[i].upper() in 'URFDLBMES':
            move = moves[i].upper()
            i += 1

            # Check for modifier
            if i < len(moves):
                if moves[i] == "'":
                    move += "'"
                    i += 1
                elif moves[i] == "2":
                    move += "2"
                    i += 1

            result.append(move)
        else:
            i += 1  # Skip unknown characters

    return result


def apply_move(state: dict, move: str) -> dict:
    """Apply a single move to the cube state."""
    if move in MOVE_MAP:
        return MOVE_MAP[move](state)
    raise ValueError(f"Unknown move: {move}")


def apply_moves(state: dict, moves: str) -> dict:
    """Apply a sequence of moves to the cube state."""
    move_list = parse_moves(moves)
    for move in move_list:
        state = apply_move(state, move)
    return state


def generate_scramble(length: int = 21) -> str:
    """
    Generate a random scramble sequence.

    Rules:
    - Uses standard WCA-style moves (no slice moves)
    - Avoids consecutive moves on the same face (R R' is pointless)
    - Avoids moves on opposite faces in sequence if the first was repeated
    """
    scramble = []
    last_face = None
    second_last_face = None

    # Opposite faces
    opposites = {'U': 'D', 'D': 'U', 'R': 'L', 'L': 'R', 'F': 'B', 'B': 'F'}

    for _ in range(length):
        move = random.choice(BASIC_MOVES)
        face = move[0]

        # Avoid same face consecutively
        while face == last_face:
            move = random.choice(BASIC_MOVES)
            face = move[0]

        # Avoid patterns like "R L R" (same face with opposite in between)
        if second_last_face == face and last_face == opposites.get(face):
            while face == second_last_face or face == last_face:
                move = random.choice(BASIC_MOVES)
                face = move[0]

        scramble.append(move)
        second_last_face = last_face
        last_face = face

    return ' '.join(scramble)


# =============================================================================
# KOCIEMBA SOLVER INTEGRATION
# =============================================================================

def state_to_kociemba_string(state: dict) -> str:
    """
    Convert cube state to Kociemba solver format.

    Kociemba expects a 54-character string in URFDLB order:
    - First 9 chars: U face (row by row, left to right)
    - Next 9 chars: R face
    - Next 9 chars: F face
    - Next 9 chars: D face
    - Next 9 chars: L face
    - Last 9 chars: B face
    """
    face_order = ['U', 'R', 'F', 'D', 'L', 'B']
    result = ''

    for face_name in face_order:
        face = state[face_name]
        for row in face:
            for cell in row:
                result += cell

    return result


def get_solution(state: dict) -> str:
    """
    Get optimal solution using Kociemba two-phase algorithm.

    Returns a move sequence that solves the cube.
    Raises ValueError if the cube state is invalid/unsolvable.
    """
    import kociemba

    cube_string = state_to_kociemba_string(state)
    try:
        solution = kociemba.solve(cube_string)
        return solution
    except ValueError as e:
        raise ValueError(f"Invalid cube state: {e}")


def validate_state(state: dict) -> bool:
    """
    Validate that a cube state is solvable.

    Checks:
    1. Each color appears exactly 9 times
    2. The Kociemba solver can find a solution (proves it's a valid permutation)
    """
    # Count colors
    counts = {'U': 0, 'D': 0, 'L': 0, 'R': 0, 'F': 0, 'B': 0}
    for face in state.values():
        for row in face:
            for cell in row:
                if cell in counts:
                    counts[cell] += 1

    # Each color must appear exactly 9 times
    for count in counts.values():
        if count != 9:
            return False

    # Try to solve - if successful, state is valid
    try:
        get_solution(state)
        return True
    except:
        return False
