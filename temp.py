from cube.cube import Cube
import numpy as np
from cube.move import Move, MoveType
from cube.face import Face
from cube.axis import Axis
from cube.scramble import generate_scramble
from display.viewer import Viewer
from cube.sequence import Sequence
from cube.notation.formater import format_sequence
from cube.notation.parser import parse_sequence
from solvers.helpers.locator import find_piece_locations
from solvers.classic.white_center import solve_white_center
from solvers.classic.yellow_center import solve_yellow_center
from solvers.helpers.orient import orient
from solvers.helpers.comutator import comutate_center_pieces
from solvers.classic.other_centers import solve_other_centers

size = 7
cube = Cube(size)
viewer = Viewer(cube)
viewer.show()

scramble = generate_scramble(size, relative_length=1, seed=10)

cube.apply_sequence(scramble)
viewer.update()
white = solve_white_center(cube)
cube.apply_sequence(white)
viewer.update()
yellow = solve_yellow_center(cube)
cube.apply_sequence(yellow)
viewer.update()
other_centers = solve_other_centers(cube)
cube.apply_sequence(other_centers)
viewer.update()
input("Press Enter to continue...")
