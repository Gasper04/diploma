from cube.cube import Cube
from cube.move import Move, MoveType
from cube.face import Face
from cube.axis import Axis
from cube.sequence import Sequence
from solvers.helpers.locator import find_piece_locations
from solvers.helpers.orient import orient
# poišči beli koščk (i, j)
# če je košček že na pravem mestu
#     continue
# sicer
#     izberi enega od koščkov na voljo po naslednji prioriteti glede strani
#     (R, F, B, L, U, D)
#     premakni ga na stran R
#     obrni ga da je na poziciji (i, j) na strani R
#     vstavi ga z {j}L {i}U {j}L'


def solve_white_center(cube: Cube) -> Sequence:
    _cube = cube.copy()
    moves = Sequence()
    moves.extend(orient(_cube))
    _cube.apply_sequence(moves)
    for j in range(2, _cube.n):
        for i in range(2, _cube.n):
            piece_solution = Sequence()
            best_piece = find_best_white_piece(_cube, i, j)
            if best_piece is None:
                continue
            piece_solution.extend(move_piece_to_face_R_white(best_piece, i, j, _cube.n))
            piece_solution.extend(insert_white_piece(i, j))
            _cube.apply_sequence(piece_solution)
            moves.extend(piece_solution)
    return moves


def find_best_white_piece(cube: Cube, i, j):
    pieces = find_piece_locations(cube, color=Face.U.value, i=i, j=j)
    best_piece = None
    if (Face.U, i, j) in pieces:
        return None
    for piece in pieces:
        if piece[0] == Face.R:
            best_piece = piece
            break
    if best_piece is None:
        for piece in pieces:
            if piece[0] == Face.F:
                best_piece = piece
            elif piece[0] == Face.B:
                best_piece = piece
            elif piece[0] == Face.L:
                best_piece = piece
    if best_piece is None:
        for piece in pieces:
            if piece[0] == Face.U:
                if piece[1] < i:
                    #pice in a solved column, skip
                    continue
                if piece[1] == i and piece[2] < j:
                    #piece in a row we are currently solving, skip
                    continue
                best_piece = piece
            elif piece[0] == Face.D:
                best_piece = piece
    return best_piece

def insert_white_piece(i, j):
    seq = Sequence()
    seq.append(Move(MoveType.SLICE, face=Face.L, layer=j, turns=1))
    seq.append(Move(MoveType.SLICE, face=Face.U, layer=i, turns=1))
    seq.append(Move(MoveType.SLICE, face=Face.L, layer=j, turns=3))
    return seq


def move_piece_to_face_R_white(piece, end_i, end_j, n):
    seq = Sequence()
    if piece[0] == Face.R:
        pass
    elif piece[0] == Face.F:
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=piece[1], turns=3))
    elif piece[0] == Face.B:
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=piece[1], turns=1))
    elif piece[0] == Face.L:
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=piece[1], turns=2))
    elif piece[0] == Face.U:
        seq.append(Move(MoveType.SLICE, face=Face.L, layer=piece[2], turns=1))
        seq.append(Move(MoveType.SLICE, face=Face.U, layer=piece[1], turns=3))
        seq.append(Move(MoveType.SLICE, face=Face.L, layer=piece[2], turns=3))
    elif piece[0] == Face.D:
        if n%2 == 1 and piece[2] == (n+1)//2:
            seq.append(Move(MoveType.SLICE, face=Face.L, layer=piece[2], turns=3))
            seq.append(Move(MoveType.FACE, face=Face.F, turns=1))
            seq.append(Move(MoveType.SLICE, face=Face.L, layer=piece[2], turns=1))
            seq.append(Move(MoveType.FACE, face=Face.F, turns=3))
            seq.append(Move(MoveType.SLICE, face=Face.U, layer=piece[1], turns=3))

        else:
            seq.append(Move(MoveType.SLICE, face=Face.L, layer=piece[2], turns=3))
            seq.append(Move(MoveType.FACE, face=Face.F, turns=2))
            seq.append(Move(MoveType.SLICE, face=Face.L, layer=piece[2], turns=1))
            seq.append(Move(MoveType.FACE, face=Face.F, turns=2))
            seq.append(Move(MoveType.SLICE, face=Face.U, layer=piece[1], turns=3))

    r = 0
    i0 = piece[1]
    j0 = piece[2]
    while not(i0 == end_i and j0 == end_j):
        r += 1
        i = j0
        j = n + 1 - i0
        i0, j0 = i, j
    if r != 0:
        seq.append(Move(MoveType.FACE, face=Face.R, turns=r))
    return seq


def solve_yellow_center(cube: Cube) -> Sequence:
    pass
