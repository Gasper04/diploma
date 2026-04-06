from cube.cube import Cube
from cube.move import Move, MoveType
from cube.face import Face
from cube.sequence import Sequence
from solvers.helpers.edge_piece import EdgePiece, Color, find_edge_piece, color_combinations
from display.viewer import Viewer

class EdgePieceSolver:
    def __init__(self, cube: Cube):
        self.cube = cube.copy()
        self.n = cube.n
        self.moves = Sequence()

    def solve_edges(self):
        for (color1, color2) in color_combinations[:-1]:
            self.solve_first_piece_of_edge(color1, color2)
            if color1 == Color.BLUE and color2 == Color.ORANGE:
                #this is the last edge piece, if the first piece of this edge is solved then the whole edge is solved
                pass
            for i in range(2, self.n):
                edge_piece_no_face = EdgePiece(color1=color1, color2=color2, face1=None, face2=None, i=i)
                edge_piece= find_edge_piece(self.cube, edge_piece_no_face)
                if edge_piece.face1 == Face.F and edge_piece.face2 == Face.L:
                    #piece is already solved, skip
                    continue
                #edge flipped
                if edge_piece.face2 == Face.F and edge_piece.face1 == Face.L:
                    #move buffer edge to top layer (i kow this one is unsolved since it is the last one)
                    #this edge gets messed up but thats ok this edge is not soved yet
                    buffer_edge_piece_no_face = EdgePiece(color1=color_combinations[-1][0], color2=color_combinations[-1][1], face1=None, face2=None, i=self.n//2 + 1 )
                    buffer_edge_piece = find_edge_piece(self.cube, buffer_edge_piece_no_face)
                    if buffer_edge_piece.face1 == Face.L and buffer_edge_piece.face2 == Face.F:
                        buffer_edge_piece_no_face = EdgePiece(color1=color_combinations[-1][0], color2=color_combinations[-1][1], face1=None, face2=None, i=self.n-(self.n//2))
                        buffer_edge_piece = find_edge_piece(self.cube, buffer_edge_piece_no_face)
                    sequence = self.move_edge_top(buffer_edge_piece, config="add")
                    self.cube.apply_sequence(sequence)
                    self.moves.extend(sequence)
                    #put the edge piece in the correct slot for the same place algorithm
                    buffer_edge_piece = find_edge_piece(self.cube, buffer_edge_piece_no_face)
                    setup_piece_sequence = self.setup_piece(buffer_edge_piece)
                    self.cube.apply_sequence(setup_piece_sequence)
                    self.moves.extend(setup_piece_sequence)
                    #apply same place algorithm to flip the edge piece in place
                    seq = self.same_place_alg(i)
                    self.cube.apply_sequence(seq)
                    self.moves.extend(seq)
                    continue

                #move adge to top layer
                sequence = self.move_edge_top(edge_piece, config="add")
                self.cube.apply_sequence(sequence)
                self.moves.extend(sequence)
                #put the edge containing the edge pice in the ceoret slot for the insert algorithm
                edge_piece = find_edge_piece(self.cube, edge_piece_no_face)
                setup_piece_sequence = self.setup_piece(edge_piece)
                self.cube.apply_sequence(setup_piece_sequence)
                self.moves.extend(setup_piece_sequence)
                #insert the edge piece in its place
                insert_sequence = self.insert_alg(i)
                self.cube.apply_sequence(insert_sequence)
                self.moves.extend(insert_sequence)
        self.last_edge_piece()
        return self.moves


        

    

    def solve_first_piece_of_edge(self, color1: Color, color2: Color):
        edge_piece_no_face = EdgePiece(color1=color1, color2=color2, face1=None, face2=None, i=self.n//2 + 1)
        edge_piece= find_edge_piece(self.cube, edge_piece_no_face)
        sequence = self.move_edge_top(edge_piece, config="base")
        self.cube.apply_sequence(sequence)
        self.moves.extend(sequence)
        edge_piece = find_edge_piece(self.cube, edge_piece_no_face)
        insert_base_piece_sequence = self.insert_base_piece(edge_piece)
        self.cube.apply_sequence(insert_base_piece_sequence)
        self.moves.extend(insert_base_piece_sequence)






    

    def move_edge_top(self, edge_piece: EdgePiece, config: str="add"):
        if edge_piece.face1 == Face.U or edge_piece.face2 == Face.U:
            return Sequence()
        if edge_piece.face1 == Face.D or edge_piece.face2 == Face.D:
            if edge_piece.face1 == Face.D:
                face = edge_piece.face2
            else:
                face = edge_piece.face1
            seq = Sequence()
            seq.append(Move(MoveType.FACE, face=face, turns=2))
            if (face == Face.F or face == Face.L) and config == "add":
                seq.append(Move(MoveType.FACE, face=Face.U, turns=1))
                seq.append(Move(MoveType.FACE, face=face, turns=2))
            return seq
            
        if edge_piece.face1 == Face.R or edge_piece.face2 == Face.R:
            seq = Sequence()
            if edge_piece.face1 == Face.R:
                face = edge_piece.face2
            else:
                face = edge_piece.face1
            if face == Face.F:
                seq.append(Move(MoveType.FACE, face=Face.R, turns=1))
            else:
                seq.append(Move(MoveType.FACE, face=Face.R, turns=3))
            return seq
        if edge_piece.face1 == Face.B or edge_piece.face2 == Face.B:
            seq = Sequence()
            if edge_piece.face1 == Face.B:
                face = edge_piece.face2
            else:
                face = edge_piece.face1
            if face == Face.R:
                seq.append(Move(MoveType.FACE, face=Face.B, turns=1))
            else:
                seq.append(Move(MoveType.FACE, face=Face.B, turns=3))
            return seq
        else:
            #pice must be on F-L edge
            if config == "add":
                raise Exception("Unexpected configuration for edge piece on F-L edge")
            seq = Sequence()
            seq.append(Move(MoveType.FACE, face=Face.L, turns=3))
            return seq
        
    def insert_base_piece(self, edge_piece: EdgePiece):
        if edge_piece.face1 == Face.U:
            seq = Sequence()
            if edge_piece.face2 == Face.F:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=1))
            elif edge_piece.face2 == Face.R:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=2))
            elif edge_piece.face2 == Face.B:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=3))
            seq.append(Move(MoveType.FACE, face=Face.L, turns=1))
        else:
            #here we want to rotate to F
            seq = Sequence()
            if edge_piece.face1 == Face.R:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=1))
            elif edge_piece.face1 == Face.B:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=2))
            elif edge_piece.face1 == Face.L:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=3))
            seq.append(Move(MoveType.FACE, face=Face.F, turns=-1))
        return seq

            
        
    def insert_alg(self, i: int):
        sequence = Sequence([
            Move(MoveType.SLICE, face=Face.U, layer=i, turns=-1),
            Move(MoveType.FACE, face=Face.R, turns=1),
            Move(MoveType.FACE, face=Face.F, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=1),
            Move(MoveType.FACE, face=Face.R, turns=-1),
            Move(MoveType.FACE, face=Face.F, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=1),
            Move(MoveType.SLICE, face=Face.U, layer=i, turns=1)
        ])
        return sequence

    def same_place_alg(self, i: int):
        sequence = Sequence([
            Move(MoveType.SLICE, face=Face.U, layer=self.n-i+1, turns=1),
            Move(MoveType.FACE, face=Face.L, turns=-1),
            Move(MoveType.FACE, face=Face.F, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=-1),
            Move(MoveType.FACE, face=Face.L, turns=1),
            Move(MoveType.FACE, face=Face.F, turns=-1),
            Move(MoveType.SLICE, face=Face.U, layer=self.n-i+1, turns=-1),
            Move(MoveType.FACE, face=Face.L, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=-1),
            Move(MoveType.FACE, face=Face.F, turns=-1),
        ])
        return sequence

    def setup_piece(self, edge_piece: EdgePiece):
        if edge_piece.face1 == Face.U:
            seq = Sequence()
            if edge_piece.face2 == Face.B:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=1))
            elif edge_piece.face2 == Face.L:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=2))
            elif edge_piece.face2 == Face.F:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=3))
            seq.append(Move(MoveType.FACE, face=Face.R, turns=-1))
            return seq
        else:
            seq = Sequence()
            if edge_piece.face1 == Face.B:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=1))
            elif edge_piece.face1 == Face.L:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=2))
            elif edge_piece.face1 == Face.F:
                seq.append(Move(MoveType.FACE, face=Face.U, turns=3))
            seq.append(Move(MoveType.FACE, face=Face.F, turns=-1))
            seq.append(Move(MoveType.FACE, face=Face.U, turns=1))
            seq.append(Move(MoveType.FACE, face=Face.F, turns=1))
            return seq
        

    def last_edge_piece(self):
        self.setup_last_piece(EdgePiece(color1=color_combinations[-1][0], color2=color_combinations[-1][1], face1=None, face2=None, i=self.n//2 + 1))
        top_color = self.cube.get(Face.U, self.n, (self.n+1)//2)
        for i in range(2, (self.n+1)//2):
            color = self.cube.get(Face.U, self.n, i)
            if color == top_color:
                continue
            else:
                alg = self.parity_alg(i)
                self.cube.apply_sequence(alg)
                self.moves.extend(alg)
        

    def setup_last_piece(self, no_face_edge_piece: EdgePiece):
        edge_piece = find_edge_piece(self.cube, no_face_edge_piece)
        move_top = self.move_edge_top(edge_piece, config="base")
        self.cube.apply_sequence(move_top)
        self.moves.extend(move_top)
        edge_piece = find_edge_piece(self.cube, no_face_edge_piece)
        turn_front = Sequence()
        if edge_piece.face1 == Face.R or edge_piece.face2 == Face.R:
            turn_front.append(Move(MoveType.FACE, face=Face.U, turns=1))
        elif edge_piece.face1 == Face.B or edge_piece.face2 == Face.B:
            turn_front.append(Move(MoveType.FACE, face=Face.U, turns=2))
        elif edge_piece.face1 == Face.L or edge_piece.face2 == Face.L:
            turn_front.append(Move(MoveType.FACE, face=Face.U, turns=3))
        self.cube.apply_sequence(turn_front)
        self.moves.extend(turn_front)

    

    def parity_alg(self, i):
        sequence = Sequence([
            Move(MoveType.SLICE, face=Face.R, layer=i, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=2),
            Move(MoveType.SLICE, face=Face.L, layer=i, turns=1),
            Move(MoveType.FACE, face=Face.F, turns=2),
            Move(MoveType.SLICE, face=Face.L, layer=i, turns=-1),
            Move(MoveType.FACE, face=Face.F, turns=2),
            Move(MoveType.SLICE, face=Face.R, layer=i, turns=2),
            Move(MoveType.FACE, face=Face.U, turns=2),
            Move(MoveType.SLICE, face=Face.R, layer=i, turns=1),
            Move(MoveType.FACE, face=Face.U, turns=2),
            Move(MoveType.SLICE, face=Face.R, layer=i, turns=-1),
            Move(MoveType.FACE, face=Face.U, turns=2),
            Move(MoveType.FACE, face=Face.F, turns=2),
            Move(MoveType.SLICE, face=Face.R, layer=i, turns=2),
            Move(MoveType.FACE, face=Face.F, turns=2),
        ])
        return sequence