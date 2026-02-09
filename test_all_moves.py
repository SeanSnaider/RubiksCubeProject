import sys
sys.path.insert(0, r'c:\Users\sean\Desktop\RubiksCubeProject\RubiksCube_project')

from RubiksCube.RubiksCube import RubiksCube
import kociemba

moves = [
    ('U', lambda c: c.moveU()),
    ('R', lambda c: c.moveR()),
    ('F', lambda c: c.moveF()),
    ('D', lambda c: c.moveD()),
    ('L', lambda c: c.moveL()),
    ('B', lambda c: c.moveB()),
    ("M'", lambda c: c.moveMPrime()),
    ("E'", lambda c: c.moveEPrime()),
    ("S'", lambda c: c.moveSPrime()),
]

print("Testing all moves to see which ones create invalid states:")
print("=" * 70)

for move_name, move_func in moves:
    cube = RubiksCube()
    cube.resetCube()
    move_func(cube)

    cube_str = cube.getCubeAsString()

    try:
        solution = kociemba.solve(cube_str)
        print(f"{move_name:3s}: OK - Solution: {solution}")
    except Exception as e:
        print(f"{move_name:3s}: FAIL - {e}")
