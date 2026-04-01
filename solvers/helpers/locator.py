## the purpose of this helper is to find all 4 locations of the pices of the specified colourthat fit in the current spot
## the function is suposed to be used on the center pieces of the cube

from cube.cube import Cube
from cube.face import Face

def find_piece_locations(cube: Cube, color: int, i: int, j: int):
    found = []
    possible_locations = [(i, j)]
    n = cube.n
    i0 = i
    j0 = j
    for _ in range(3):
        i = j0
        j = n + 1 - i0
        possible_locations.append((i, j))
        i0, j0 = i, j

    for face in list(Face):
        for loc in possible_locations:
            if cube.get(face, loc[0], loc[1]) == color:
                found.append((face, loc[0], loc[1]))
    return found
