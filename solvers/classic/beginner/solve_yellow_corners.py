from cube.cube import Cube
from cube.move import Move, MoveType
from cube.face import Face
from cube.axis import Axis
from cube.sequence import Sequence
from display.viewer import Viewer
from solvers.helpers.reduction import reduce
from solvers.helpers.corner_piece import find_corner_piece, Color, CornerPiece, color_combinations


alg = Sequence(
            [
                Move(MoveType.FACE, face=Face.R, turns=1),
                Move(MoveType.FACE, face=Face.B, turns=-1),
                Move(MoveType.FACE, face=Face.R, turns=1),
                Move(MoveType.FACE, face=Face.F, turns=2),
                Move(MoveType.FACE, face=Face.R, turns=-1),
                Move(MoveType.FACE, face=Face.B, turns=1),
                Move(MoveType.FACE, face=Face.R, turns=1),
                Move(MoveType.FACE, face=Face.F, turns=2),
                Move(MoveType.FACE, face=Face.R, turns=2),
            ])

class YellowCornersSolver:

    def __init__(self, cube: Cube):
        self.cube = reduce(cube)
        self.moves = Sequence()

    def solve_yellow_corners(self):
        count = 0
        for _ in range(4):
            if self.cube.get(Face.F, 1, 1) == self.cube.get(Face.F, 1, 3):
                count += 1

            self.cube.apply_move(Move(MoveType.FACE, face=Face.U, turns=1))
            self.moves.append(Move(MoveType.FACE, face=Face.U, turns=1))
        if count == 4:
            for _ in range(4):
                if self.cube.get(Face.F, 1, 1) == self.cube.get(Face.F, 2, 2):
                    break
                self.cube.apply_move(Move(MoveType.FACE, face=Face.U, turns=1))
                self.moves.append(Move(MoveType.FACE, face=Face.U, turns=1))
            
            return self.moves
        found_pair = False
        for _ in range(4):
            if self.cube.get(Face.F, 1, 1) == self.cube.get(Face.F, 1, 3):
                found_pair = True
                break
            self.cube.apply_move(Move(MoveType.FACE, face=Face.U, turns=1))
            self.moves.append(Move(MoveType.FACE, face=Face.U, turns=1))
        
        if not found_pair:
            self.cube.apply_sequence(alg)
            self.moves.extend(alg)
            for _ in range(4):
                if self.cube.get(Face.F, 1, 1) == self.cube.get(Face.F, 1, 3):
                    found_pair = True
                    break
                self.cube.apply_move(Move(MoveType.FACE, face=Face.U, turns=1))
                self.moves.append(Move(MoveType.FACE, face=Face.U, turns=1))
        self.cube.apply_sequence(alg)
        self.moves.extend(alg)

        for _ in range(4):
            if self.cube.get(Face.F, 1, 1) == self.cube.get(Face.F, 2, 2):
                break
            self.cube.apply_move(Move(MoveType.FACE, face=Face.U, turns=1))
            self.moves.append(Move(MoveType.FACE, face=Face.U, turns=1))
            
        return self.moves
