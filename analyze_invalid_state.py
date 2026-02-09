import sys
sys.path.insert(0, r'c:\Users\sean\Desktop\RubiksCubeProject\RubiksCube_project')

from collections import Counter

# The invalid cube string after M'
invalid = "UFUUFUUFURRRRRRRRRFDFFDFFDFDBDDBDDBDLLLLLLLLLBUBBUBBUB"

print("Analyzing why this cube state is invalid:")
print("=" * 70)
print(f"Cube string: {invalid}")
print(f"Length: {len(invalid)}")

# Count colors
counts = Counter(invalid)
print(f"\nColor counts: {dict(counts)}")
print(f"All colors appear 9 times: {all(c == 9 for c in counts.values())}")

# Break down by face
faces = ['U', 'R', 'F', 'D', 'L', 'B']
for i, face_name in enumerate(faces):
    start = i * 9
    face_str = invalid[start:start+9]
    print(f"\n{face_name} face: {face_str}")
    print(f"  Positions: {' '.join([f'{face_name}{j+1}' for j in range(9)])}")
    print(f"  Values:    {' '.join(list(face_str))}")

# The issue with kociemba validation:
# Kociemba checks if the cube is physically possible
# Key constraint: Edge pieces must maintain their orientation
# Edge pieces can only be in two orientations (flipped or not)

print("\n" + "=" * 70)
print("Checking edge orientations:")
print("\nIn Rubik's cube, edges have orientation constraints.")
print("After M', certain edges moved but may have wrong orientation.")

# Let's check which edges are affected by M'
print("\nM' should move these edges:")
print("  UF (U8) <-> UB (U2)")
print("  DF (D2) <-> DB (D8)")
print("  ... plus the middle layer edges")

print("\nLet's look at your M' result more carefully:")
print("\nU face after M': UFUUFUUFU")
print("  Position U2 (top-middle): F  <-- This should be what?")
print("  Position U5 (center): F      <-- Center, correct")
print("  Position U8 (bottom-middle): F  <-- This should be what?")

print("\nF face after M': FDFFDFFDF")
print("  Position F2: D  <-- Middle edge")
print("  Position F5: D  <-- Center, correct")
print("  Position F8: D  <-- Middle edge")

print("\nD face after M': DBDDBDDBD")
print("  Position D2: B  <-- Middle edge")
print("  Position D5: B  <-- Center, correct")
print("  Position D8: B  <-- Middle edge")

print("\nB face after M': BUBBUBBUB")
print("  Position B2: U  <-- Middle edge")
print("  Position B5: U  <-- Center, correct")
print("  Position B8: U  <-- Middle edge")

print("\n" + "=" * 70)
print("\nPOTENTIAL ISSUE:")
print("When pieces move from one face to another in the M slice,")
print("the ORIENTATION of how we read those pieces might need adjustment.")
print("\nFor example, when a piece from D[0][1] moves to F[0][1],")
print("we need to ensure it's oriented correctly in the cube string.")
print("\nThis is exactly what you mentioned - the 'plus' orientation issue!")
