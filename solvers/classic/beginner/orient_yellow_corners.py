from cube.cube import Cube
from cube.move import Move, MoveType
from cube.face import Face
from cube.axis import Axis
from cube.sequence import Sequence
from display.viewer import Viewer
from solvers.helpers.reduction import reduce
from solvers.helpers.corner_piece import find_corner_piece, Color, CornerPiece, color_combinations


sexi_move = Sequence(
            [
                Move(MoveType.FACE, face=Face.R, turns=-1),
                Move(MoveType.FACE, face=Face.D, turns=-1),
                Move(MoveType.FACE, face=Face.R, turns=1),
                Move(MoveType.FACE, face=Face.D, turns=1),
            ])

class YellowCornersOrient:

    def __init__(self, cube: Cube):
        self.cube = reduce(cube)
        self.moves = Sequence()


    def orient_yellow_corners(self):
        for _ in range(4):
            if self.cube.get(Face.R, 1, 1) == Color.YELLOW.value:
                reps = 2
            elif self.cube.get(Face.F, 1, 3) == Color.YELLOW.value:
                reps = 4
            else:
                reps = 0

            for x in range(reps):
                self.cube.apply_sequence(sexi_move)
                self.moves.extend(sexi_move)
            
            self.cube.apply_move(Move(MoveType.FACE, face=Face.U, turns=1))
            self.moves.append(Move(MoveType.FACE, face=Face.U, turns=1))
        return self.moves
