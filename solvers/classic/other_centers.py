from cube.cube import Cube
from cube.axis import Axis
from cube.face import Face
from cube.move import Move, MoveType
from cube.sequence import Sequence
from display.viewer import Viewer
from solvers.helpers.locator import find_piece_locations
from solvers.helpers.comutator import comutate_center_pieces
from solvers.helpers.orient import orient



def solve_other_centers(cube: Cube):

    _cube = cube.copy()
    moves = Sequence()
    orient_seq = orient(cube)
    _cube.apply_sequence(orient_seq)
    moves.extend(orient_seq)
    seq_F = solve_center(Face.F, _cube)
    seq_F.append(Move(MoveType.ROTATION, axis=Axis.Y, turns=1))
    _cube.apply_sequence(seq_F)
    seq_R = solve_center(Face.R, _cube)
    seq_R.append(Move(MoveType.ROTATION, axis=Axis.Y, turns=1))
    _cube.apply_sequence(seq_R)
    seq_B = solve_center(Face.B, _cube)
    seq_B.append(Move(MoveType.ROTATION, axis=Axis.Y, turns=1))
    _cube.apply_sequence(seq_B)
    seq_L = Sequence()
    seq_L.append(Move(MoveType.ROTATION, axis=Axis.Y, turns=1))
    _cube.apply_sequence(seq_L)
    moves.extend(seq_F)
    moves.extend(seq_R)
    moves.extend(seq_B)
    moves.extend(seq_L)
    return moves





def solve_center(face: Face, cube: Cube):
    _cube = cube.copy()
    moves = Sequence()
    _cube.apply_sequence(moves)
    for j in range(2, _cube.n):
        for i in range(2, _cube.n):
            piece_solution = Sequence()
            best_piece = find_best_piece(_cube, i, j, face)
            if best_piece is None:
                continue
            piece_solution.extend(rotate_piece(best_piece, i, j, _cube.n))
            piece_solution.extend(comutate_center_pieces(i, j, best_piece[0], _cube.n))
            _cube.apply_sequence(piece_solution)
            moves.extend(piece_solution)
    return moves

def find_best_piece(cube: Cube, i, j, face):
    pieces = find_piece_locations(cube, color=face.value, i=i, j=j)
    best_piece = None
    if (Face.F, i, j) in pieces:
        return None
    for piece in pieces:
        if piece[0] in [Face.R, Face.B, Face.L]:
            best_piece = piece
            break
    return best_piece

def rotate_piece(piece, end_i, end_j, n):
    seq = Sequence()
    r = 0
    i0 = piece[1]
    j0 = piece[2]
    while not(i0 == end_i and j0 == end_j):
        r += 1
        i = j0
        j = n + 1 - i0
        i0, j0 = i, j
    if r != 0:
        seq.append(Move(MoveType.FACE, face=piece[0], turns=r))
    return seq