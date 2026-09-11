"""
Tests for the solver integration in cube_service.

These cover the boundary between our cube model and the RubikTwoPhase solver:
orientation normalization and the notation the solver speaks. They deliberately
do not test the move engine itself, only that a solution we hand back actually
solves the cube it was asked about.

Regression context: the facelet string Kociemba expects identifies faces by
their centers, so it only accepts a cube in the standard orientation. Any slice
move, wide move or whole-cube rotation moves centers and made the solver reject
a perfectly legal cube with "Wrong edge and corner parity". See
normalize_orientation() in cube_service.
"""
import pytest

from app.services import cube_service as cs


# Moves that displace centers, which is what used to break the solver.
CENTER_MOVING_MOVES = ["M", "M'", "E", "E'", "S", "S'",
                       "Rw", "Lw'", "Uw", "Dw'",
                       "x", "x'", "y", "y'", "z", "z'", "x2 y", "z' x"]


def solved():
    """Return a fresh solved cube."""
    return cs.get_solved_state()


def test_solution_solves_a_plain_scramble():
    state = cs.apply_moves(solved(), "R U R' U' F2 D B' L2")
    assert cs.apply_moves(state, cs.get_solution(state)) == solved()


@pytest.mark.parametrize("move", CENTER_MOVING_MOVES)
def test_solution_solves_a_cube_whose_centers_moved(move):
    """A rotated cube is legal, and its solution must return it to solved."""
    state = cs.apply_moves(solved(), move)
    assert cs.apply_moves(state, cs.get_solution(state)) == solved()


def test_solution_uses_standard_notation():
    """The solver emits U1/U2/U3; our own parser has to be able to read it back."""
    state = cs.apply_moves(solved(), "M' x Rw U R'")
    solution = cs.get_solution(state)
    assert ' '.join(cs.parse_moves(solution)) == solution


def test_normalize_orientation_reports_the_rotations_it_applied():
    rotated = cs.apply_moves(solved(), "x")
    oriented, rotations = cs.normalize_orientation(rotated)
    assert oriented['U'][1][1] == 'U' and oriented['F'][1][1] == 'F'
    assert cs.apply_moves(rotated, rotations) == oriented


def test_normalize_orientation_leaves_an_oriented_cube_alone():
    state = cs.apply_moves(solved(), "R U R'")
    oriented, rotations = cs.normalize_orientation(state)
    assert rotations == ""
    assert oriented == state


def test_to_standard_notation_converts_quarter_turn_counts():
    assert cs.to_standard_notation("U1 R2 F3 (3f)") == "U R2 F'"


def test_to_standard_notation_rejects_unknown_tokens():
    with pytest.raises(ValueError):
        cs.to_standard_notation("U4")


def test_rotated_cube_is_considered_valid():
    """Turning the whole cube doesn't make it unsolvable."""
    assert cs.validate_state(cs.apply_moves(solved(), "x M"))


def test_impossible_cube_is_rejected():
    broken = solved()
    broken['U'] = [['D'] * 3 for _ in range(3)]
    assert not cs.validate_state(broken)
