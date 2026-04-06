
from cube.axis import Axis
from cube.sequence import Sequence
from cube.face import Face
from cube.move import Move, MoveType
from cube.cube import Cube


def orient(cube: Cube):
    if cube.n % 2 == 0:
        return Sequence()
    moves = Sequence()
    i = (cube.n + 1) // 2
    _cube = cube.copy()


    #white top
    if cube.get(Face.F, i, i) == Face.U.value:
        moves.append(Move(MoveType.ROTATION, axis=Axis.X, turns=1))
    elif cube.get(Face.R, i, i) == Face.U.value:
        moves.append(Move(MoveType.ROTATION, axis=Axis.Z, turns=3))
    elif cube.get(Face.B, i, i) == Face.U.value:
        moves.append(Move(MoveType.ROTATION, axis=Axis.X, turns=3))
    elif cube.get(Face.L, i, i) == Face.U.value:
        moves.append(Move(MoveType.ROTATION, axis=Axis.Z, turns=1))
    elif cube.get(Face.D, i, i) == Face.U.value:
        moves.append(Move(MoveType.ROTATION, axis=Axis.X, turns=2))

    _cube.apply_sequence(moves)

    #green front
    if _cube.get(Face.R, i, i) == Face.F.value:
        moves.append(Move(MoveType.ROTATION, axis=Axis.Y, turns=1))
    elif _cube.get(Face.B, i, i) == Face.F.value:
        moves.append(Move(MoveType.ROTATION, axis=Axis.Y, turns=2))
    elif _cube.get(Face.L, i, i) == Face.F.value:
        moves.append(Move(MoveType.ROTATION, axis=Axis.Y, turns=3))
    
    return moves

    