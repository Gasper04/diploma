
from cube.cube import Cube
from cube.move import Move, MoveType
from cube.face import Face
from cube.axis import Axis
from cube.sequence import Sequence
from display.viewer import Viewer
from solvers.helpers.reduction import reduce
from solvers.helpers.edge_piece import find_edge_piece, EdgePiece, Color



class SecondLayerSolver:

    def __init__(self, cube: Cube):
        self.cube = reduce(cube)
        self.moves = Sequence()

    def solve_second_layer(self) -> Sequence:
        color_combinations = [
            (Color.GREEN, Color.RED),
            (Color.GREEN, Color.ORANGE),
            (Color.RED, Color.BLUE),
            (Color.BLUE, Color.ORANGE),
        ]
        for (color1, color2) in color_combinations:
            edge_piece = EdgePiece(color1, color2, i = 2)
            self.move_edge_top(edge_piece)
            self.insert_edge(edge_piece)
        return self.moves







    def move_edge_top(self, no_face_edge_piece: EdgePiece) -> Sequence:
        edge_piece = find_edge_piece(self.cube, no_face_edge_piece)
        if edge_piece.face1 == Face.U or edge_piece.face2 == Face.U:
            pass
        else:
            faces = [edge_piece.face1, edge_piece.face2]
            if Face.R in faces:
                if Face.B in faces:
                    rotation = Move(MoveType.ROTATION, axis=Axis.Y, turns=1)
                    self.cube.apply_move(rotation)
                    self.moves.append(rotation)
                self.cube.apply_sequence(self.insert_right)
                self.moves.extend(self.insert_right)
            if Face.L in faces:
                if Face.B in faces:
                    rotation = Move(MoveType.ROTATION, axis=Axis.Y, turns=-1)
                    self.cube.apply_move(rotation)
                    self.moves.append(rotation)
                self.cube.apply_sequence(self.insert_left)
                self.moves.extend(self.insert_left)


    def insert_edge(self, no_face_edge_piece: EdgePiece):
        if not (find_edge_piece(self.cube, no_face_edge_piece).face1 == Face.U or find_edge_piece(self.cube, no_face_edge_piece).face2 == Face.U):
            raise Exception("Edge piece is not in the top layer")
        edge_piece = find_edge_piece(self.cube, no_face_edge_piece)
        if edge_piece.face1 == Face.U:
            front_color = edge_piece.color2
            top_color = edge_piece.color1
        else:
            front_color = edge_piece.color1
            top_color = edge_piece.color2

        rotation = Move(MoveType.ROTATION, axis=Axis.Y, turns=1)
        while self.cube.get(Face.F, 2, 2) != front_color.value:
            self.cube.apply_move(rotation)
            self.moves.append(rotation)

        edge_piece = find_edge_piece(self.cube, no_face_edge_piece)
        faces = (edge_piece.face1, edge_piece.face2)
        if Face.R in faces:
            move = Move(MoveType.FACE, face=Face.U, turns=1)
            self.cube.apply_move(move)
            self.moves.append(move)
        elif Face.B in faces:
            move = Move(MoveType.FACE, face=Face.U, turns=2)
            self.cube.apply_move(move)
            self.moves.append(move)
        elif Face.L in faces:
            move = Move(MoveType.FACE, face=Face.U, turns=-1)
            self.cube.apply_move(move)
            self.moves.append(move)

        if self.cube.get(Face.L, 2, 2) == top_color.value:
            self.cube.apply_sequence(self.insert_left)
            self.moves.extend(self.insert_left)
        else:
            self.cube.apply_sequence(self.insert_right)
            self.moves.extend(self.insert_right)

            

        


    insert_left = Sequence(
        [
            Move(MoveType.FACE, face=Face.U, turns=-1),
            Move(MoveType.FACE, face=Face.L, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=1),
            Move(MoveType.FACE, face=Face.L, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=1),
            Move(MoveType.FACE, face=Face.F, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=-1),
            Move(MoveType.FACE, face=Face.F, turns=-1),
        ]
    )

    insert_right = Sequence(
        [
            Move(MoveType.FACE, face=Face.U, turns=1),
            Move(MoveType.FACE, face=Face.R, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=-1),
            Move(MoveType.FACE, face=Face.R, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=-1),
            Move(MoveType.FACE, face=Face.F, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=1),
            Move(MoveType.FACE, face=Face.F, turns=1),
        ]
    )