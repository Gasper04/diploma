from cube.cube import Cube
from cube.sequence import Sequence
from solvers.classic.white_center import solve_white_center
from solvers.classic.yellow_center import solve_yellow_center
from solvers.classic.other_centers import solve_other_centers


def solve_centers(cube: Cube):
    _cube = cube.copy()
    white = solve_white_center(_cube)
    _cube.apply_sequence(white)
    yellow = solve_yellow_center(_cube)
    _cube.apply_sequence(yellow)
    other_centers = solve_other_centers(_cube)
    _cube.apply_sequence(other_centers)
    sequence = Sequence()
    sequence.extend(white)
    sequence.extend(yellow)
    sequence.extend(other_centers)
    return sequence
