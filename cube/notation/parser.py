from cube.move import Move, MoveType
from cube.axis import char_to_axis
from cube.face import char_to_face
from cube.sequence import Sequence


def parse_move(move_str: str) -> Move:
    move_str = move_str.strip()
    if move_str[-1] == '2':
        turns = 2
        move_str = move_str[:-1]
    elif move_str[-1] == "'":
        turns = 3
        move_str = move_str[:-1]
    else:
        turns = 1
    
    if move_str[0].lower() in char_to_axis:
        axis = char_to_axis[move_str[0].lower()]
        return Move(type=MoveType.ROTATION, turns=turns, axis=axis)

    if len(move_str) == 1:
        face_char = move_str[0]
        face = char_to_face[face_char.upper()]
        return Move(type=MoveType.FACE, turns=turns, face=face)
    
    if move_str[-1].lower() == 'w':
        if len(move_str) == 2:
            layer = 2
        else:
            layer = int(move_str[:-2])
        face_char = move_str[-2]
        face = char_to_face[face_char.upper()]
        return Move(type=MoveType.WIDE, turns=turns, face=face, layer=layer)
    
    layer = int(move_str[:-1])
    face_char = move_str[-1]
    face = char_to_face[face_char.upper()]
    return Move(type=MoveType.SLICE, turns=turns, face=face, layer=layer)

def parse_sequence(sequence_str: str) -> Sequence:
    move_strs = sequence_str.split()
    moves = [parse_move(move_str) for move_str in move_strs]
    return Sequence(moves)
