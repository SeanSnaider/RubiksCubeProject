import sys
sys.path.insert(0, r'c:\Users\sean\Desktop\RubiksCubeProject\RubiksCube_project')

from RubiksCube.RubiksCube import RubiksCube
import kociemba

# Test to determine correct face orientations
cube = RubiksCube()

print("Testing face orientations for kociemba solver")
print("=" * 60)

# Test 1: Do a simple R move and see if solver gives correct inverse
print("\n1. Testing R move:")
cube.resetCube()
cube.moveR()

cube_str = cube.getCubeAsString()
print(f"   Cube string: {cube_str}")

try:
    solution = kociemba.solve(cube_str)
    print(f"   Solution: {solution}")
    print(f"   Expected: R' (or R R R)")
    if "R'" in solution or solution == "R R R":
        print("   ✓ R face orientation is CORRECT")
    else:
        print("   ✗ R face orientation might be WRONG")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Do a simple U move
print("\n2. Testing U move:")
cube.resetCube()
cube.moveU()

cube_str = cube.getCubeAsString()
try:
    solution = kociemba.solve(cube_str)
    print(f"   Solution: {solution}")
    print(f"   Expected: U'")
    if "U'" in solution or solution == "U U U":
        print("   ✓ U face orientation is CORRECT")
    else:
        print("   ✗ U face orientation might be WRONG")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Do F move
print("\n3. Testing F move:")
cube.resetCube()
cube.moveF()

cube_str = cube.getCubeAsString()
try:
    solution = kociemba.solve(cube_str)
    print(f"   Solution: {solution}")
    print(f"   Expected: F'")
    if "F'" in solution or solution == "F F F":
        print("   ✓ F face orientation is CORRECT")
    else:
        print("   ✗ F face orientation might be WRONG")
except Exception as e:
    print(f"   Error: {e}")

# Test 4: Detailed face inspection
print("\n4. Inspecting individual face after R move:")
cube.resetCube()
print("   Before R:")
print(f"   U face: {cube.U}")
print(f"   R face: {cube.R}")
print(f"   F face: {cube.F}")

cube.moveR()
print("\n   After R:")
print(f"   U face: {cube.U}")
print(f"   R face: {cube.R}")
print(f"   F face: {cube.F}")
