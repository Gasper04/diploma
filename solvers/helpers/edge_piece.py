from enum import Enum
from cube.cube import Cube
from cube.face import Face
from solvers.helpers.touching_facelets import Facelet, get_touching_facelets

class Color(Enum):
    WHITE = 0
    GREEN = 1
    RED = 2
    BLUE = 3
    ORANGE = 4
    YELLOW = 5

class EdgePiece:
    def __init__(self, color1: Color, color2: Color, face1: Face = None, face2: Face = None, i: int = 1):
        self.color1 = color1
        self.color2 = color2
        self.face1 = face1
        self.face2 = face2
        self.i = i

    def __eq__(self, value):
        if not isinstance(value, EdgePiece):
            return False
        return self.color1 == value.color1 and self.color2 == value.color2 and self.face1 == value.face1 and self.face2 == value.face2 and self.i == value.i
    

color_combinations = [
    (Color.WHITE, Color.GREEN),
    (Color.WHITE, Color.RED),
    (Color.WHITE, Color.BLUE),
    (Color.WHITE, Color.ORANGE),
    (Color.GREEN, Color.RED),
    (Color.GREEN, Color.ORANGE),
    (Color.GREEN, Color.YELLOW),
    (Color.RED, Color.BLUE),
    (Color.RED, Color.YELLOW),
    (Color.BLUE, Color.ORANGE),
    (Color.BLUE, Color.YELLOW),
    (Color.ORANGE, Color.YELLOW)
]


def find_edge_piece(cube: Cube, edge_piece: EdgePiece):
    possible_locations = [(edge_piece.i, 1)]
    n = cube.n
    i0 = edge_piece.i
    j0 = 1
    for _ in range(3):
        i = j0
        j = n + 1 - i0
        possible_locations.append((i, j))
        i0, j0 = i, j

    for face in list(Face):
        for loc in possible_locations:
            if cube.get(face, loc[0], loc[1]) == edge_piece.color1.value:
                touching_facelets = get_touching_facelets(Facelet(face=face, i=loc[0], j=loc[1]), cube.n)
                if len(touching_facelets) != 1:
                    raise Exception("Invalid cube state, edge piece has more than 2 facelets")
                facelet = touching_facelets[0]
                if cube.get(facelet.face, facelet.i, facelet.j) == edge_piece.color2.value: 
                    return EdgePiece(color1=edge_piece.color1, color2=edge_piece.color2, face1=face, face2=touching_facelets[0].face, i=edge_piece.i)
    raise Exception("Edge piece not found on the cube")
