from dataclasses import dataclass
from enum import Enum
from cube.face import Face

class MoveType(Enum):
    ROTATION = "rotation"
    FACE = "face"
    WIDE = "wide"
    SLICE = "slice"

@dataclass(frozen=True)
class Move:
    type: MoveType
    turns: int
    face: Face | None = None
    layer: int | None = None
    axis: Face | None = None