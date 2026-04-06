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

class CornerPiece:
    def __init__(self, color1: Color, color2: Color, color3: Color, face1: Face = None, face2: Face = None, face3: Face = None):
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.face1 = face1
        self.face2 = face2
        self.face3 = face3

    def __eq__(self, value):
        if not isinstance(value, CornerPiece):
            return False
        return self.color1 == value.color1 and self.color2 == value.color2 and self.color3 == value.color3 and self.face1 == value.face1 and self.face2 == value.face2 and self.face3 == value.face3

color_combinations = [
    (Color.WHITE, Color.GREEN, Color.ORANGE),
    (Color.WHITE, Color.ORANGE, Color.BLUE),
    (Color.WHITE, Color.BLUE, Color.RED),
    (Color.WHITE, Color.RED, Color.GREEN),
    (Color.YELLOW, Color.GREEN, Color.RED),
    (Color.YELLOW, Color.RED, Color.BLUE),
    (Color.YELLOW, Color.BLUE, Color.ORANGE),
    (Color.YELLOW, Color.ORANGE, Color.GREEN),
]


def find_corner_piece(cube: Cube, corner_piece: CornerPiece):
    possible_locations = [(1, 1), (1, cube.n), (cube.n, 1), (cube.n, cube.n)]

    for face in list(Face):
        for loc in possible_locations:
            if cube.get(face, loc[0], loc[1]) == corner_piece.color1.value:
                touching_facelets = get_touching_facelets(Facelet(face=face, i=loc[0], j=loc[1]), cube.n)
                if len(touching_facelets) != 2:
                    raise Exception("Invalid cube state: corner does not have exactly 3 facelets")
                if set([cube.get(f.face, f.i, f.j) for f in touching_facelets]) == set([corner_piece.color2.value, corner_piece.color3.value]):
                    if cube.get(touching_facelets[0].face, touching_facelets[0].i, touching_facelets[0].j) == corner_piece.color2.value:
                        return CornerPiece(color1=corner_piece.color1, color2=corner_piece.color2, color3=corner_piece.color3, face1=face, face2=touching_facelets[0].face, face3=touching_facelets[1].face)
                    return CornerPiece(color1=corner_piece.color1, color2=corner_piece.color2, color3=corner_piece.color3, face1=face, face2=touching_facelets[1].face, face3=touching_facelets[0].face )
    raise Exception("Corner piece not found on the cube")
