import random as rn
from cube.sequence import Sequence
from cube.move import Move, MoveType
from cube.face import Face

def generate_scramble(n, relative_length=1, seed=None):
    if seed is not None:
        rn.seed(seed)

    scramble = Sequence()

    length = int(round(relative_length * n * 20))

    for i in range(length):
        face = rn.choice(list(Face))
        turns = rn.randint(1, 3)
        layer = rn.randint(1, (n+1) // 2)
        move_type = MoveType.WIDE
        scramble.append(Move(type=move_type, turns=turns, face=face, layer=layer))

    return scramble