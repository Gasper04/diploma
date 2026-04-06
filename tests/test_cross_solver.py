import pytest
from cube.cube import Cube
from cube.face import Face
from cube.scramble import generate_scramble
from solvers.classic.white_center import solve_white_center
from solvers.classic.yellow_center import solve_yellow_center
from solvers.classic.beginner.white_cross import WhiteCrossSolver
from solvers.helpers.orient import orient
from display.viewer import Viewer



N_SEEDS = 1000

@pytest.mark.parametrize("seed", list(range(N_SEEDS)))
def test_white_cross(seed):
    size = 3
    cube = Cube(size)
    scramble = generate_scramble(size, relative_length=1, seed=seed)
    cube.apply_sequence(scramble)
    cube.apply_sequence(orient(cube))
    wcs = WhiteCrossSolver(cube)
    moves = wcs.solve_white_cross(cube)
    cube.apply_sequence(moves)
    cube.apply_sequence(orient(cube))
    assert cube.get(Face.F, 2, 2) == Face.F.value
    assert cube.get(Face.F, 1, 2) == Face.F.value

    assert cube.get(Face.R, 2, 2) == Face.R.value
    assert cube.get(Face.R, 1, 2) == Face.R.value

    assert cube.get(Face.B, 2, 2) == Face.B.value
    assert cube.get(Face.B, 1, 2) == Face.B.value

    assert cube.get(Face.L, 2, 2) == Face.L.value
    assert cube.get(Face.L, 1, 2) == Face.L.value

    assert cube.get(Face.U, 2, 2) == Face.U.value
    assert cube.get(Face.U, 1, 2) == Face.U.value
    assert cube.get(Face.U, 2, 1) == Face.U.value
    assert cube.get(Face.U, 2, 3) == Face.U.value
    assert cube.get(Face.U, 3, 2) == Face.U.value
