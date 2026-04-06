from cube.cube import Cube
from cube.move import Move, MoveType
from cube.face import Face
from cube.axis import Axis
from cube.sequence import Sequence
from display.viewer import Viewer
from solvers.helpers.reduction import reduce
from solvers.helpers.corner_piece import find_corner_piece, Color, CornerPiece, color_combinations

class WhiteCornersSolver:

    def __init__(self, cube: Cube):
        self.cube = reduce(cube)
        self.moves = Sequence()


    def solve_white_corners(self):
        for (color1, color2, color3) in color_combinations[0:4]:
            corner = CornerPiece(color1=color1, color2=color2, color3=color3)
            self.move_top(corner)
            self.move_front_right(corner)
            self.insert_corner(corner)
            rotation = Move(MoveType.ROTATION, axis=Axis.Y, turns=1)
            self.cube.apply_move(rotation)
            self.moves.append(rotation)
        return self.moves
            


    def move_top(self, no_face_corner):
        corner = find_corner_piece(self.cube, no_face_corner)
        faces = (corner.face1, corner.face2, corner.face3)
        if Face.U in faces:
            return
        elif Face.F in faces and Face.R in faces:
            seq = Sequence([
                Move(MoveType.FACE, face=Face.R, turns=1),
                Move(MoveType.FACE, face=Face.U, turns=1),
                Move(MoveType.FACE, face=Face.R, turns=-1),
            ])
        elif Face.B in faces and Face.R in faces:
            seq = Sequence([
                Move(MoveType.FACE, face=Face.R, turns=-1),
                Move(MoveType.FACE, face=Face.U, turns=-1),
                Move(MoveType.FACE, face=Face.R, turns=1),
            ])
        elif Face.B in faces and Face.L in faces:
            seq = Sequence([
                Move(MoveType.FACE, face=Face.L, turns=1),
                Move(MoveType.FACE, face=Face.U, turns=1),
                Move(MoveType.FACE, face=Face.L, turns=-1),
            ])
        elif Face.F in faces and Face.L in faces:
            seq = Sequence([
                Move(MoveType.FACE, face=Face.L, turns=-1),
                Move(MoveType.FACE, face=Face.U, turns=-1),
                Move(MoveType.FACE, face=Face.L, turns=1),
            ])
        self.cube.apply_sequence(seq)
        self.moves.extend(seq)
        return
    
    def move_front_right(self, no_face_corner):
        corner = find_corner_piece(self.cube, no_face_corner)
        faces = (corner.face1, corner.face2, corner.face3)
        if Face.F in faces and Face.R in faces:
            return
        elif Face.B in faces and Face.R in faces:
            move = Move(MoveType.FACE, face=Face.U, turns=1)
            self.cube.apply_move(move)
            self.moves.append(move)
        elif Face.B in faces and Face.L in faces:
            move = Move(MoveType.FACE, face=Face.U, turns=2)
            self.cube.apply_move(move)
            self.moves.append(move)
        elif Face.F in faces and Face.L in faces:
            move = Move(MoveType.FACE, face=Face.U, turns=-1)
            self.cube.apply_move(move)
            self.moves.append(move)
        return
    

    def insert_corner(self, no_face_corner):
        corner = find_corner_piece(self.cube, no_face_corner)

        if corner.face1 == Face.R:
            self.cube.apply_sequence(self.sexi_move())
            self.moves.extend(self.sexi_move())

        elif corner.face1 == Face.U:
            for x in range(3):
                self.cube.apply_sequence(self.sexi_move())
                self.moves.extend(self.sexi_move())

        else:
            for x in range(5):
                self.cube.apply_sequence(self.sexi_move())
                self.moves.extend(self.sexi_move())


    def sexi_move(self):
        seq = Sequence([
                Move(MoveType.FACE, face=Face.R, turns=1),
                Move(MoveType.FACE, face=Face.U, turns=1),
                Move(MoveType.FACE, face=Face.R, turns=-1),
                Move(MoveType.FACE, face=Face.U, turns=-1),
        ]
        )
        return seq
