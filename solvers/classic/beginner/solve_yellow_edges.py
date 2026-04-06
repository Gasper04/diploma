
from cube.cube import Cube
from cube.move import Move, MoveType
from cube.face import Face
from cube.axis import Axis
from cube.sequence import Sequence
from display.viewer import Viewer
from solvers.helpers.reduction import reduce
from solvers.helpers.edge_piece import find_edge_piece, EdgePiece, Color



edges_rotator = Sequence(
        [
            Move(MoveType.FACE, face=Face.R, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=-1),

            Move(MoveType.FACE, face=Face.R, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=1),

            Move(MoveType.FACE, face=Face.R, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=1),

            Move(MoveType.FACE, face=Face.R, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=-1),

            Move(MoveType.FACE, face=Face.R, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=-1),

            Move(MoveType.FACE, face=Face.R, turns=2),
        ]
    )

class YellowEdgesSolver:

    def __init__(self, cube: Cube):
        self.original_cube = cube.copy()
        self.cube = reduce(cube)
        self.moves = Sequence()

        i = cube.n//2
        self.parity_alg = Sequence([
            Move(MoveType.WIDE, face=Face.U, layer=i, turns=2),
            Move(MoveType.WIDE, face=Face.R, layer=i, turns=2),
            Move(MoveType.FACE, face=Face.U, turns=2),
            Move(MoveType.WIDE, face=Face.R, layer=i, turns=2),
            Move(MoveType.FACE, face=Face.R, turns=2),
            Move(MoveType.FACE, face=Face.U, turns=2),
            Move(MoveType.WIDE, face=Face.R, layer=i, turns=2),
            Move(MoveType.WIDE, face=Face.U, layer=i, turns=2),
        ])

    def solve_yellow_edges(self) -> Sequence:
        while not self.check_for_solved_edge():
            self.cube.apply_sequence(edges_rotator)
            self.moves.extend(edges_rotator)
        n_solved = self.count_solved()

        if n_solved != 4:

            if n_solved == 2:
                self.original_cube.apply_sequence(self.moves)
                self.original_cube.apply_sequence(self.parity_alg)
                self.moves.extend(self.parity_alg)
                self.cube = reduce(self.original_cube)


            self.cube.apply_move(Move(MoveType.ROTATION, axis=Axis.Y, turns=1))
            self.moves.append(Move(MoveType.ROTATION, axis=Axis.Y, turns=1))

            while self.count_solved() != 4:
                self.cube.apply_sequence(edges_rotator)
                self.moves.extend(edges_rotator)



        return self.moves


    def check_for_solved_edge(self):
        found_solved = False
        for _ in range(4):
            if self.cube.get(Face.L, 1, 2) == self.cube.get(Face.L, 2, 2):
                found_solved = True
                break
            self.cube.apply_move(Move(MoveType.ROTATION, axis=Axis.Y, turns=1))
            self.moves.append(Move(MoveType.ROTATION, axis=Axis.Y, turns=1))
        return found_solved


    def count_solved(self):
        n_solved = 0
        for face in [Face.R, Face.F, Face.L, Face.B]:
            if self.cube.get(face, 1, 2) == self.cube.get(face, 2, 2):
                n_solved += 1

        return n_solved












