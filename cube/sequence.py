from cube.move import Move
from dataclasses import dataclass

@dataclass
class Sequence:
    def __init__(self, moves=None):
        if moves is None:
            moves = []
        self.moves = moves


    def __iter__(self):
        return iter(self.moves)

    def __len__(self):
        return len(self.moves)

    def __getitem__(self, item):
        return self.moves[item]

    def extend(self, seq2):
        self.moves.extend(seq2.moves)
    
    def append(self, move: Move):
        self.moves.append(move)
    
    def inverted(self):
        reversed_moves = []
        for move in reversed(self.moves):
            reversed_moves.append(Move(
                type=move.type,
                turns=4-(move.turns % 4),
                face=move.face,
                layer=move.layer,
                axis=move.axis
            ))
        return Sequence(reversed_moves)
    
