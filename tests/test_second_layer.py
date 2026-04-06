import pytest
from cube.cube import Cube
from cube.face import Face
from cube.scramble import generate_scramble
from solvers.classic.white_center import solve_white_center
from solvers.classic.yellow_center import solve_yellow_center
from solvers.classic.beginner.white_cross import WhiteCrossSolver
from solvers.classic.beginner.white_corners import WhiteCornersSolver
from solvers.classic.beginner.second_layer import SecondLayerSolver
from solvers.helpers.orient import orient
from display.viewer import Viewer


N_SEEDS = 1000

@pytest.mark.parametrize("seed", list(range(N_SEEDS)))
def test_white_corners(seed):
    size = 3
    cube = Cube(size)
    scramble = generate_scramble(size, relative_length=1, seed=seed)
    cube.apply_sequence(scramble)
    cube.apply_sequence(orient(cube))
    wcs = WhiteCrossSolver(cube)
    moves = wcs.solve_white_cross()
    cube.apply_sequence(moves)
    wcrs = WhiteCornersSolver(cube)
    moves = wcrs.solve_white_corners()
    cube.apply_sequence(moves)

    second_layer_solver = SecondLayerSolver(cube)
    moves = second_layer_solver.solve_second_layer()
    cube.apply_sequence(moves)
    cube.apply_sequence(orient(cube))
    for x in range(3):
        for y in range(3):
            assert cube.get(Face.U, x, y) == Face.U.value
    
    for face in (Face.F, Face.R, Face.B, Face. L):
        assert cube.get(face, 2, 2) == face.value
        assert cube.get(face, 1, 1) == face.value
        assert cube.get(face, 1, 2) == face.value
        assert cube.get(face, 1, 3) == face.value
        assert cube.get(face, 2, 2) == face.value
        assert cube.get(face, 2, 3) == face.value
