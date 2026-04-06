import pytest
from cube.cube import Cube
from cube.face import Face
from cube.scramble import generate_scramble
from solvers.helpers.touching_facelets import Facelet, get_touching_facelets
import random as rn


N_SEEDS = 100

@pytest.mark.parametrize("size", list(range(3, 15)))
@pytest.mark.parametrize("seed", list(range(N_SEEDS)))
def test_touching_facelets(size, seed):
    cube = Cube(size)
    cube.faces[:, :, :] = 0
    rn.seed(seed)
    for x in range(10):
        face = rn.choice(list(Face))
        edge_choice = rn.randint(0, 3)
        if edge_choice == 0:
            facelet = Facelet(face, 1, rn.randint(1, size))
        elif edge_choice == 1:
            facelet = Facelet(face, size, rn.randint(1, size))
        elif edge_choice == 2:
            facelet = Facelet(face, rn.randint(1, size), 1)
        else:
            facelet = Facelet(face, rn.randint(1, size), size)

        cube.faces[facelet.face.value, facelet.i-1, facelet.j-1] = x+1
        touching_facelets = get_touching_facelets(facelet=facelet, n=size)
        for touching_facelet in touching_facelets:
            cube.faces[touching_facelet.face.value, touching_facelet.i-1, touching_facelet.j-1] = x+1
    
    scramble = generate_scramble(size, relative_length=1, seed=seed)
    cube.apply_sequence(scramble)

    for face in list(Face):
        for i in range(1, size+1):
            for j in range(1, size+1):
                color = cube.faces[face.value, i-1, j-1]
                touching_facelets = get_touching_facelets(Facelet(face, i, j), size)
                for touching_facelet in touching_facelets:
                    assert cube.faces[touching_facelet.face.value, touching_facelet.i-1, touching_facelet.j-1] == color, f"Touching facelet {touching_facelet} does not have the same color as {face}({i}, {j})"
