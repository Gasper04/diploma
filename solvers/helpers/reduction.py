from cube.cube import Cube

# cube that is alrerady reduced to a 3x3 will now be converted into a "same" cube but with size 3

def reduce(cube: Cube) -> Cube:

    size = cube.n
    if size <= 3:
        return cube.copy()
    reduced_cube = Cube(3)
    for face in range(6):
        reduced_cube.faces[face][0][0]= cube.faces[face][0][0]
        reduced_cube.faces[face][0][1]= cube.faces[face][0][1]
        reduced_cube.faces[face][0][2]= cube.faces[face][0][size-1]
        reduced_cube.faces[face][1][0]= cube.faces[face][1][0]
        reduced_cube.faces[face][1][1]= cube.faces[face][1][1]
        reduced_cube.faces[face][1][2]= cube.faces[face][1][size-1]
        reduced_cube.faces[face][2][0]= cube.faces[face][size-1][0]
        reduced_cube.faces[face][2][1]= cube.faces[face][size-1][1]
        reduced_cube.faces[face][2][2]= cube.faces[face][size-1][size-1]
    return reduced_cube