import sys
sys.path.insert(0, r'c:\Users\sean\Desktop\RubiksCubeProject\RubiksCube_project')

from RubiksCube.RubiksCube import RubiksCube
from collections import Counter

# Test M' move specifically
cube = RubiksCube()

print("Testing M' move specifically:")
print("=" * 60)

print("\n1. Solved cube:")
cube_str = cube.getCubeAsString()
print(f"   String: {cube_str}")
try:
    import kociemba
    solution = kociemba.solve(cube_str)
    print(f"   Solution: {solution}")
except Exception as e:
    print(f"   Error: {e}")

print("\n2. After M' move:")
cube.moveMPrime()
cube_str = cube.getCubeAsString()
color_counts = Counter(cube_str)
print(f"   String: {cube_str}")
print(f"   Color counts: {dict(color_counts)}")
print(f"   Valid counts (all 9): {all(count == 9 for count in color_counts.values())}")

try:
    solution = kociemba.solve(cube_str)
    print(f"   Solution: {solution}")
    print(f"   Expected: M (the inverse of M')")
except Exception as e:
    print(f"   ERROR: {e}")
    print(f"   This means the cube string is invalid for kociemba")
