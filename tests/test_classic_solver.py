import pytest
from cube.cube import Cube
from cube.scramble import generate_scramble
from solvers.classic.classic_solver import ClassicSolver


N_SEEDS = 100

@pytest.mark.parametrize("size", list(range(3, 15)))
@pytest.mark.parametrize("seed", list(range(N_SEEDS)))
def test_clasic_solver(size, seed):
    cube = Cube(size)
    scramble = generate_scramble(size, relative_length=1, seed=seed)
    cube.apply_sequence(scramble)
    solver = ClassicSolver(cube)
    solution = solver.solve()
    cube.apply_sequence(solution)
    assert cube.is_solved()