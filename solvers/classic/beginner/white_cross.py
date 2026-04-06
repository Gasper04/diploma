
from cube.cube import Cube
from cube.move import Move, MoveType
from cube.face import Face
from cube.axis import Axis
from cube.sequence import Sequence
from display.viewer import Viewer
from solvers.helpers.reduction import reduce
from solvers.helpers.edge_piece import find_edge_piece, EdgePiece, Color



class WhiteCrossSolver:

    def __init__(self, cube: Cube):
        self.cube = reduce(cube)
        self.moves = Sequence()

    def solve_white_cross(self, cube: Cube) -> Sequence:
        rotation = Move(MoveType.ROTATION, axis=Axis.Z, turns=2)
        self.cube.apply_move(rotation)
        self.moves.append(rotation)
        for colour in (Color.GREEN, Color.ORANGE, Color.BLUE, Color.RED):
            edge_piece = EdgePiece(Color.WHITE, colour, i = 2)
            self.move_edge_top(edge_piece)
            self.insert_edge(edge_piece)
            rotation = Move(MoveType.ROTATION, axis=Axis.Y, turns=1)
            self.cube.apply_move(rotation)
            self.moves.append(rotation)
        return self.moves







    def move_edge_top(self, no_face_edge_piece: EdgePiece) -> Sequence:
        edge_piece = find_edge_piece(self.cube, no_face_edge_piece)
        if edge_piece.face1 == Face.D or edge_piece.face2 == Face.D:
            face = edge_piece.face1 if edge_piece.face1 != Face.D else edge_piece.face2
            move = Move(MoveType.FACE, face=face, turns=2)
            self.cube.apply_move(move)
            self.moves.append(move)
        elif edge_piece.face1 == Face.U or edge_piece.face2 == Face.U:
            pass
        else:
            _cube = self.cube.copy()
            move = Move(MoveType.FACE, face=edge_piece.face1, turns=1)
            reverse = Move(MoveType.FACE, face=edge_piece.face1, turns=-1)
            _cube.apply_move(move)
            edge_piece_after_move = find_edge_piece(_cube, no_face_edge_piece)
            if edge_piece_after_move.face1 != Face.U and edge_piece_after_move.face2 != Face.U:
                move = Move(MoveType.FACE, face=edge_piece.face1, turns=-1)
                reverse = Move(MoveType.FACE, face=edge_piece.face1, turns=1)
            seq = Sequence([move, Move(MoveType.FACE, face=Face.U, turns=1), reverse])
            self.cube.apply_sequence(seq)
            self.moves.extend(seq)

    def insert_edge(self, no_face_edge_piece: EdgePiece):
        if not (find_edge_piece(self.cube, no_face_edge_piece).face1 == Face.U or find_edge_piece(self.cube, no_face_edge_piece).face2 == Face.U):
            raise Exception("Edge piece is not in the top layer")
        edge_piece = find_edge_piece(self.cube, no_face_edge_piece)
        if edge_piece.face1 == Face.U:
            if edge_piece.face2 == Face.R:
                move = Move(MoveType.FACE, face=Face.U, turns=1)
                self.cube.apply_move(move)
                self.moves.append(move)
            elif edge_piece.face2 == Face.B:
                move = Move(MoveType.FACE, face=Face.U, turns=2)
                self.cube.apply_move(move)
                self.moves.append(move)
            elif edge_piece.face2 == Face.L:
                move = Move(MoveType.FACE, face=Face.U, turns=-1)
                self.cube.apply_move(move)
                self.moves.append(move)
            move = Move(MoveType.FACE, face=Face.F, turns=2)
            self.cube.apply_move(move)
            self.moves.append(move)
        else:
            if edge_piece.face1 == Face.B:
                move = Move(MoveType.FACE, face=Face.U, turns=1)
                self.cube.apply_move(move)
                self.moves.append(move)
            elif edge_piece.face1 == Face.L:
                move = Move(MoveType.FACE, face=Face.U, turns=2)
                self.cube.apply_move(move)
                self.moves.append(move)
            elif edge_piece.face1 == Face.F:
                move = Move(MoveType.FACE, face=Face.U, turns=-1)
                self.cube.apply_move(move)
                self.moves.append(move)
            move = Move(MoveType.FACE, face=Face.R, turns=-1)
            reverse = Move(MoveType.FACE, face=Face.R, turns=1)
            seq = Sequence([move, Move(MoveType.FACE, face=Face.F, turns=1), reverse])
            self.cube.apply_sequence(seq)
            self.moves.extend(seq)