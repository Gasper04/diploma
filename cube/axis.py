from enum import Enum
from cube.face import Face

class Axis(Enum):
    X = 0
    Y = 1
    Z = 2

    # axis:

    # X: L-R
    # Y: D-U
    # Z: B-F

face_to_axis = {
    Face.U: Axis.Y,
    Face.F: Axis.Z,
    Face.R: Axis.X,
    Face.B: Axis.Z,
    Face.L: Axis.X,
    Face.D: Axis.Y,
}

axis_to_char = {
    Axis.X: 'x',
    Axis.Y: 'y',
    Axis.Z: 'z'
}

char_to_axis = {
    'x': Axis.X,
    'y': Axis.Y,
    'z': Axis.Z
}