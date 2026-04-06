


#can comutate pieces in the same place from the F, R, B and L faces to the face F

from cube.move import Move, MoveType
from cube.sequence import Sequence
from cube.face import Face


def comutate_center_pieces(i, j, face_from, n):
    if face_from == Face.F:
        raise ValueError("face_from must be R, B or L")
    seq = Sequence()
    if face_from == Face.R:
        turns = 3
    elif face_from == Face.B:
        turns = 2
    elif face_from == Face.L:
        turns = 1
    else:
        raise ValueError("face_from must be R, B or L")
    if i == j:
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=i, turns=4-turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=3))
        seq.append(Move(MoveType.SLICE, face=Face.D, layer=i, turns=turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=1))
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=i, turns=turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=3))
        seq.append(Move(MoveType.SLICE, face=Face.D, layer=i, turns=4-turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=1))

    elif i + j == n + 1:
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=i, turns=4-turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=1))
        seq.append(Move(MoveType.SLICE, face=Face.D, layer=i, turns=turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=3))
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=i, turns=turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=1))
        seq.append(Move(MoveType.SLICE, face=Face.D, layer=i, turns=4-turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=3))

    else:
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=i, turns=4-turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=1))
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=j, turns=4-turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=3))
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=i, turns=turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=1))
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=j, turns=turns))
        seq.append(Move(MoveType.FACE, face=Face.F, turns=3))

    return seq