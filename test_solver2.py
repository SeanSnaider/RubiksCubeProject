import sys
sys.path.insert(0, r'c:\Users\sean\Desktop\RubiksCubeProject\RubiksCube_project')

from RubiksCube.RubiksCube import RubiksCube
import kociemba

# Create a cube and try different scenarios
cube = RubiksCube()

print("Testing solver with various scenarios:")
print("=" * 60)

# Test 1: Solved cube
print("\n1. Solved cube:")
cube_str = cube.getCubeAsString()
print(f"   String: {cube_str}")
try:
    solution = kociemba.solve(cube_str)
    print(f"   [OK] Solution found: {solution}")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test 2: Single U move
print("\n2. After U move:")
cube.moveU()
cube_str = cube.getCubeAsString()
print(f"   String: {cube_str}")
try:
    solution = kociemba.solve(cube_str)
    print(f"   [OK] Solution found: {solution}")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test 3: Multiple moves
print("\n3. After U R F:")
cube.resetCube()
cube.moveU()
cube.moveR()
cube.moveF()
cube_str = cube.getCubeAsString()
print(f"   String: {cube_str}")
try:
    solution = kociemba.solve(cube_str)
    print(f"   [OK] Solution found: {solution}")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test 4: Scramble
print("\n4. After scramble:")
cube.resetCube()
cube.scrambleCube()
cube_str = cube.getCubeAsString()
print(f"   String: {cube_str}")
try:
    solution = kociemba.solve(cube_str)
    print(f"   [OK] Solution found: {solution}")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test 5: Check if cube state is valid after moves
print("\n5. Validating cube state:")
cube.resetCube()
print(f"   Initial: U={cube.U[1][1]} R={cube.R[1][1]} F={cube.F[1][1]} D={cube.D[1][1]} L={cube.L[1][1]} B={cube.B[1][1]}")

# Count each color
from collections import Counter
cube_str = cube.getCubeAsString()
color_counts = Counter(cube_str)
print(f"   Color counts: {dict(color_counts)}")
print(f"   Each should be 9: {all(count == 9 for count in color_counts.values())}")
