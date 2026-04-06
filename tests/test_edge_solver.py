import pytest
from cube.cube import Cube
from cube.face import Face
from cube.scramble import generate_scramble
from solvers.classic.white_center import solve_white_center
from solvers.classic.yellow_center import solve_yellow_center
from solvers.classic.centers import solve_centers
from solvers.classic.edges import EdgePieceSolver

N_SEEDS = 100



@pytest.mark.parametrize("size", list(range(3, 15)))
@pytest.mark.parametrize("seed", list(range(N_SEEDS//6)))
def test_centers(size, seed):
    cube = Cube(size)
    scramble = generate_scramble(size, relative_length=1, seed=seed)
    cube.apply_sequence(scramble)
    center_sol = solve_centers(cube)
    cube.apply_sequence(center_sol)
    edge_sol = EdgePieceSolver(cube).solve_edges()
    cube.apply_sequence(edge_sol)
    for face in list(Face):
        #check if faces are solved
        for i in range(2, size):
            for j in range(2, size):
                assert cube.get(face, i, j) == face.value, f"Center not solved for face {face}, size {size}, seed {seed}"

        #check if edges are solved
        edge_colours = [
            cube.get(face, 1, 2),
            cube.get(face, size, 2),
            cube.get(face, 2, 1),
            cube.get(face, 2, size)
        ]
        for i in range(3, size):
            assert cube.get(face, 1, i) == edge_colours[0], f"Edge piece not solved for face {face}, size {size}, seed {seed}"
            assert cube.get(face, size, i) == edge_colours[1], f"Edge piece not solved for face {face}, size {size}, seed {seed}"
            assert cube.get(face, i, 1) == edge_colours[2], f"Edge piece not solved for face {face}, size {size}, seed {seed}"
            assert cube.get(face, i, size) == edge_colours[3], f"Edge piece not solved for face {face}, size {size}, seed {seed}"
