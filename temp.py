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
from solvers.classic.white_center import solve_white_center
from solvers.classic.yellow_center import solve_yellow_center
from solvers.helpers.orient import orient
from solvers.helpers.comutators import comutate_center_pieces
from solvers.classic.other_centers import solve_other_centers
from solvers.helpers.touching_facelets import get_touching_facelets, Facelet
from solvers.classic.edges import EdgePieceSolver
from solvers.helpers.edge_piece import Color, EdgePiece, find_edge_piece

seed = 1
size = 7



cube = Cube(size)
alg = EdgePieceSolver(cube).parity_alg(3)
viewer = Viewer(cube)
viewer.show()
viewer.update()

scramble = generate_scramble(size, relative_length=1, seed=seed)
cube.apply_sequence(scramble)
cube.apply_sequence(alg)

viewer.update()
input("Press Enter to continue...")
