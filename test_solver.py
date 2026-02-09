import sys
sys.path.insert(0, r'c:\Users\sean\Desktop\RubiksCubeProject\RubiksCube_project')

from RubiksCube.RubiksCube import RubiksCube

# Create a solved cube
cube = RubiksCube()
cube_string = cube.getCubeAsString()

print(f"Cube string length: {len(cube_string)}")
print(f"Cube string: {cube_string}")
print(f"Expected length: 54 (6 faces x 9 stickers)")

# Check what kociemba expects
print("\nKociemba expects a 54-character string with:")
print("- Order: U R F D L B")
print("- Each face: 9 stickers (row by row)")
print("- Valid characters: U, R, F, D, L, B")

# Try to solve it
try:
    import kociemba
    solution = kociemba.solve(cube_string)
    print(f"\nSolved cube solution: {solution}")
except Exception as e:
    print(f"\nError solving: {e}")

# Test with a scrambled cube
print("\n--- Testing with one move (U) ---")
cube.moveU()
cube_string2 = cube.getCubeAsString()
print(f"Cube string after U move: {cube_string2}")

try:
    solution = kociemba.solve(cube_string2)
    print(f"Solution: {solution}")
except Exception as e:
    print(f"Error: {e}")
