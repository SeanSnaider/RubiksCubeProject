import sys
sys.path.insert(0, r'c:\Users\sean\Desktop\RubiksCubeProject\RubiksCube_project')

from RubiksCube.RubiksCube import RubiksCube
import kociemba

print("Detailed M' move analysis:")
print("=" * 70)

# Test M' move
cube = RubiksCube()
print("\nBefore M' move:")
print(f"U: {cube.U}")
print(f"F: {cube.F}")
print(f"D: {cube.D}")
print(f"B: {cube.B}")
print(f"L: {cube.L}")
print(f"R: {cube.R}")

cube.moveMPrime()

print("\nAfter M' move:")
print(f"U: {cube.U}")
print(f"F: {cube.F}")
print(f"D: {cube.D}")
print(f"B: {cube.B}")
print(f"L: {cube.L}")
print(f"R: {cube.R}")

print("\nExpected changes for M':")
print("M' rotates the middle slice (column 1) in the same direction as L")
print("Should move: F[*][1] -> U[*][1] -> B[*][1] -> D[*][1] -> F[*][1]")
print("But B face pieces go in reverse order due to orientation")

cube_str = cube.getCubeAsString()
print(f"\nCube string: {cube_str}")

try:
    solution = kociemba.solve(cube_str)
    print(f"[OK] Solution: {solution}")
except Exception as e:
    print(f"[ERROR] {e}")
    print("\nThis cube state is invalid for kociemba!")
    print("The issue is likely in how pieces are being moved during M'")

# Let's manually check if the move logic is correct
print("\n" + "=" * 70)
print("Checking M' move logic from code...")
print("\nYour moveMPrime does:")
print("  self.F[0][1], self.U[0][1], self.B[2][1], self.D[0][1] = self.D[0][1], self.F[0][1], self.U[0][1], self.B[2][1]")
print("  self.F[1][1], self.U[1][1], self.B[1][1], self.D[1][1] = self.D[1][1], self.F[1][1], self.U[1][1], self.B[1][1]")
print("  self.F[2][1], self.U[2][1], self.B[0][1], self.D[2][1] = self.D[2][1], self.F[2][1], self.U[2][1], self.B[0][1]")

print("\nNotice: B face uses reversed indices (2, 1, 0) instead of (0, 1, 2)")
print("This is because B face is oriented opposite when looking at the cube")
