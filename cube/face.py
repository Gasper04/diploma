from enum import Enum

class Face(Enum):
    U = 0
    F = 1
    R = 2
    B = 3
    L = 4
    D = 5

face_to_char = {
    Face.U: 'U',
    Face.F: 'F',
    Face.R: 'R',
    Face.B: 'B',
    Face.L: 'L',
    Face.D: 'D'
}

char_to_face = {
    'U': Face.U,
    'F': Face.F,
    'R': Face.R,
    'B': Face.B,
    'L': Face.L,
    'D': Face.D
}