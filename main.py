from cube.cube import Cube
import numpy as np
from cube.move import Move, MoveType
from cube.face import Face
from cube.axis import Axis
from cube.scramble import generate_scramble
from display import viewer
from display.viewer import Viewer
from cube.sequence import Sequence
from cube.notation.formater import format_sequence
from cube.notation.parser import parse_sequence
from solvers.classic.white_center import solve_white_center
from solvers.classic.yellow_center import solve_yellow_center
from solvers.helpers.center_piece import Color
from solvers.helpers.orient import orient
from solvers.helpers.comutators import comutate_center_pieces
from solvers.classic.other_centers import solve_other_centers
from solvers.classic.centers import solve_centers
from solvers.classic.edges import EdgePieceSolver
from solvers.helpers.reduction import reduce
from solvers.classic.beginner.white_cross import WhiteCrossSolver

size = 6
cube = Cube(size)
viewer = Viewer(cube)
viewer.show()

scramble = generate_scramble(size, relative_length=1, seed=None)

cube.apply_sequence(scramble)
viewer.update()
centers_solution = solve_centers(cube)
cube.apply_sequence(centers_solution)
viewer.update()
sq = EdgePieceSolver(cube).solve_edges()
cube.apply_sequence(sq)
viewer.update()
wcs = WhiteCrossSolver(cube)
wcs.solve_white_cross(cube)
cube.apply_sequence(wcs.moves)
viewer.update()



input("Press Enter to continue...")
