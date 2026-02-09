import sys
sys.path.insert(0, r'c:\Users\sean\Desktop\RubiksCubeProject\RubiksCube_project')

from RubiksCube.RubiksCube import RubiksCube
import kociemba

# Create solved cube
cube = RubiksCube()

print("Analyzing cube state representation:")
print("=" * 70)

print("\nYour internal representation (solved cube):")
print(f"U face: {cube.U}")
print(f"R face: {cube.R}")
print(f"F face: {cube.F}")
print(f"D face: {cube.D}")
print(f"L face: {cube.L}")
print(f"B face: {cube.B}")

print("\nYour getCubeAsString output:")
cube_str = cube.getCubeAsString()
print(cube_str)
print(f"Length: {len(cube_str)}")

print("\nKociemba expects for a SOLVED cube:")
print("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")

print("\nComparison:")
expected = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
if cube_str == expected:
    print("[OK] MATCH! Your solved cube string is correct.")
else:
    print("[ERROR] MISMATCH!")
    print("\nDifferences:")
    for i, (yours, exp) in enumerate(zip(cube_str, expected)):
        if yours != exp:
            face_idx = i // 9
            pos_in_face = i % 9
            faces = ['U', 'R', 'F', 'D', 'L', 'B']
            print(f"  Position {i} ({faces[face_idx]}{pos_in_face+1}): yours='{yours}', expected='{exp}'")

# Now test with a single R move
print("\n" + "=" * 70)
print("\nTesting R move:")
cube.resetCube()
cube.moveR()

print("\nAfter R move, your internal state:")
print(f"U face: {cube.U}")
print(f"R face: {cube.R}")
print(f"F face: {cube.F}")
print(f"D face: {cube.D}")
print(f"B face: {cube.B}")

cube_str_after_r = cube.getCubeAsString()
print(f"\nYour string after R: {cube_str_after_r}")

try:
    solution = kociemba.solve(cube_str_after_r)
    print(f"[OK] Kociemba can solve it! Solution: {solution}")
    if solution in ["R'", "R R R"]:
        print("  And the solution is correct!")
except Exception as e:
    print(f"[ERROR] Kociemba error: {e}")
    print("\nThis means the R move is changing the cube state incorrectly")
    print("for kociemba's expected format.")
