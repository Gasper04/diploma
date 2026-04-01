import pytest
from cube.cube import Cube
from cube.face import Face
from cube.scramble import generate_scramble
from solvers.classic.white_center import solve_white_center
from solvers.classic.yellow_center import solve_yellow_center
from solvers.classic.centers import solve_centers


N_SEEDS = 1000

@pytest.mark.parametrize("size", list(range(3, 15)))
@pytest.mark.parametrize("seed", list(range(N_SEEDS)))
def test_white_center(size, seed):
    cube = Cube(size)
    scramble = generate_scramble(size, relative_length=1, seed=seed)
    cube.apply_sequence(scramble)
    center_sol = solve_white_center(cube)
    cube.apply_sequence(center_sol)
    all_white = True
    for i in range(2, size):
        for j in range(2, size):
            if cube.get(Face.U, i, j) != Face.U.value:
                all_white = False
    assert all_white, f"White center not solved for size {size}, seed {seed}"


@pytest.mark.parametrize("size", list(range(3, 15)))
@pytest.mark.parametrize("seed", list(range(N_SEEDS//2)))
def test_white_and_yellow_center(size, seed):
    cube = Cube(size)
    scramble = generate_scramble(size, relative_length=1, seed=seed)
    cube.apply_sequence(scramble)
    center_sol = solve_white_center(cube)
    cube.apply_sequence(center_sol)
    yellow_center_sol = solve_yellow_center(cube)
    cube.apply_sequence(yellow_center_sol)
    all_white = True
    for i in range(2, size):
        for j in range(2, size):
            if cube.get(Face.U, i, j) != Face.U.value:
                all_white = False
    assert all_white, f"White center not solved for size {size}, seed {seed}"
    all_yellow = True
    for i in range(2, size):
        for j in range(2, size):
            if cube.get(Face.D, i, j) != Face.D.value:
                all_yellow = False
    assert all_yellow, f"Yellow center not solved for size {size}, seed {seed}"



@pytest.mark.parametrize("size", list(range(3, 15)))
@pytest.mark.parametrize("seed", list(range(N_SEEDS//6)))
def test_centers(size, seed):
    cube = Cube(size)
    scramble = generate_scramble(size, relative_length=1, seed=seed)
    cube.apply_sequence(scramble)
    center_sol = solve_centers(cube)
    cube.apply_sequence(center_sol)
    for face in list(Face):
        for i in range(2, size):
            for j in range(2, size):
                assert cube.get(face, i, j) == face.value, f"Center not solved for face {face}, size {size}, seed {seed}"

