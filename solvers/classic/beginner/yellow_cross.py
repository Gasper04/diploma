
from cube.cube import Cube
from cube.move import Move, MoveType
from cube.face import Face
from cube.axis import Axis
from cube.sequence import Sequence
from display.viewer import Viewer
from solvers.helpers.reduction import reduce
from solvers.helpers.edge_piece import find_edge_piece, EdgePiece, Color



yellow_cross_alg = Sequence(
        [
            Move(MoveType.FACE, face=Face.F, turns=1),
            Move(MoveType.FACE, face=Face.R, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=1),
            Move(MoveType.FACE, face=Face.R, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=-1),
            Move(MoveType.FACE, face=Face.F, turns=-1)
        ]
    )

class YellowCrossSolver:

    def __init__(self, cube: Cube):
        self.original_cube = cube.copy()
        self.cube = reduce(cube)
        self.moves = Sequence()

        i = cube.n//2
        self.parity_alg = Sequence([
            Move(MoveType.WIDE, face=Face.R, layer=i, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=2),
            Move(MoveType.WIDE, face=Face.L, layer=i, turns=1),
            Move(MoveType.FACE, face=Face.F, turns=2),
            Move(MoveType.WIDE, face=Face.L, layer=i, turns=-1),
            Move(MoveType.FACE, face=Face.F, turns=2),
            Move(MoveType.WIDE, face=Face.R, layer=i, turns=2),
            Move(MoveType.FACE, face=Face.U, turns=2),
            Move(MoveType.WIDE, face=Face.R, layer=i, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=2),
            Move(MoveType.WIDE, face=Face.R, layer=i, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=2),
            Move(MoveType.FACE, face=Face.F, turns=2),
            Move(MoveType.WIDE, face=Face.R, layer=i, turns=2),
            Move(MoveType.FACE, face=Face.F, turns=2),
        ])

    def solve_yellow_cross(self) -> Sequence:
        count = 0
        for pos in [(1, 2), (2, 1), (3, 2), (2, 3)]:
            if self.cube.get(Face.U, pos[0], pos[1]) == Face.D.value:
                count += 1
        if count % 2 == 1:
            #we must do parity
            self.original_cube.apply_sequence(self.parity_alg)
            self.moves.extend(self.parity_alg)
            self.cube = reduce(self.original_cube)

        
        pattern = []
        for pos in [(1, 2), (2, 1), (3, 2), (2, 3)]:
            if self.cube.get(Face.U, pos[0], pos[1]) == Face.D.value:
                pattern.append(1)
            else:
                pattern.append(0)
        count = sum(pattern)

        if count == 4:
            pass
        if count == 0:
            self.cube.apply_sequence(yellow_cross_alg)
            self.moves.extend(yellow_cross_alg)
            self.cube.apply_move(Move(MoveType.FACE, face=Face.U, turns=2))
            self.moves.append((Move(MoveType.FACE, face=Face.U, turns=2)))

            self.cube.apply_sequence(yellow_cross_alg)
            self.moves.extend(yellow_cross_alg)
            self.cube.apply_sequence(yellow_cross_alg)
            self.moves.extend(yellow_cross_alg)
        if count == 2:
            if pattern == [0, 1, 0, 1] or pattern == [1, 0, 1, 0]:
                if pattern[0] == 1:
                    self.cube.apply_move(Move(MoveType.FACE, face=Face.U, turns=1))
                    self.moves.append((Move(MoveType.FACE, face=Face.U, turns=1)))

                self.cube.apply_sequence(yellow_cross_alg)
                self.moves.extend(yellow_cross_alg)
            
            else:
                if pattern[0] == 1 and pattern[1] == 1:
                    turns = 0
                if pattern[1] == 1 and pattern[2] == 1:
                    turns = 1
                if pattern[2] == 1 and pattern[3] == 1:
                    turns = 2
                if pattern[3] == 1 and pattern[0] == 1:
                    turns = 3
                self.cube.apply_move(Move(MoveType.FACE, face=Face.U, turns=turns))
                self.moves.append((Move(MoveType.FACE, face=Face.U, turns=turns)))

                self.cube.apply_sequence(yellow_cross_alg)
                self.moves.extend(yellow_cross_alg)
                self.cube.apply_sequence(yellow_cross_alg)
                self.moves.extend(yellow_cross_alg)
        return self.moves
    











