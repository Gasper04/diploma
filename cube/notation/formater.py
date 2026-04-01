from cube.move import Move, MoveType
from cube.axis import axis_to_char
from cube.face import face_to_char
from cube.sequence import Sequence



def format_move(move: Move) -> str:
    if move.turns % 4 == 0:
        direction_str = ''
    elif move.turns % 4 == 1:
        direction_str = ''
    elif move.turns % 4 == 2:
        direction_str = '2'
    elif move.turns % 4 == 3:
        direction_str = "'"
    
    if move.type == MoveType.ROTATION:
        return f"{axis_to_char[move.axis]}{direction_str}"
    face_str = face_to_char[move.face]
    if move.type == MoveType.FACE:
        return f"{face_str}{direction_str}"
    elif move.type == MoveType.WIDE:
        if move.layer == 1:
            return f"{face_str}{direction_str}"
        return f"{move.layer}{face_str}w{direction_str}"
    elif move.type == MoveType.SLICE:
        return f"{move.layer}{face_str}{direction_str}"
    
def format_sequence(sequence: Sequence) -> str:
    return ' '.join(format_move(move) for move in sequence)