from enum import Enum
from cube.cube import Cube
from cube.face import Face

class Color(Enum):
    WHITE = 0
    GREEN = 1
    RED = 2
    BLUE = 3
    ORANGE = 4
    YELLOW = 5

class CenterPiece:
    def __init__(self, color: Color, face: Face, i: int, j: int):
        self.color = color
        self.face = face
        self.i = i
        self.j = j

    def __repr__(self):
        return f"CenterPiece(color={self.color.name}, face={self.face}, i={self.i}, j={self.j})"
    
    def __eq__(self, other):
        if not isinstance(other, CenterPiece):
            return False
        return self.color == other.color and self.face == other.face and self.i == other.i and self.j == other.j

def find_piece_locations(cube: Cube, center_piece: CenterPiece):
    found = []
    possible_locations = [(center_piece.i, center_piece.j)]
    n = cube.n
    i0 = center_piece.i
    j0 = center_piece.j
    for _ in range(3):
        i = j0
        j = n + 1 - i0
        possible_locations.append((i, j))
        i0, j0 = i, j

    for face in list(Face):
        for loc in possible_locations:
            if cube.get(face, loc[0], loc[1]) == center_piece.color.value:
                found.append(CenterPiece(color=center_piece.color, face=face, i=loc[0], j=loc[1]))
    return found
