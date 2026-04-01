import numpy as np

from cube.face import Face
from cube.axis import Axis
from cube.move import Move, MoveType
from cube.sequence import Sequence
from display.viewer import Viewer
import time

class Cube:
    def __init__(self, n: int):
        self.n = n

        self.faces = np.zeros((6, n, n), dtype=np.int8)

        for i in range(6):
            self.faces[i] = i

    # face orientation

    # the F, R, B and L faces are orianted so their "top" is at the contact with the U face

    # the U is orientet with B at its top

    # the D is oriented with F at its top
    
    def __str__(self):
        return self.faces.__str__()
    
    def copy(self):
        new_cube = Cube(self.n)
        new_cube.faces = np.copy(self.faces)
        return new_cube
    
    def is_solved(self) -> bool:
        for i in range(6):
            if not np.all(self.faces[i] == i):
                return False
        return True
    
    def get(self, face: Face, i: int, j: int) -> int:
        return self.faces[face.value, i-1, j-1]
    
    def apply_move(self, move: Move):
        if move.turns % 4 == 0:
            return
        if move.type == MoveType.FACE:
            self._slice(move.face, 0, 1, move.turns)
            self._rotate_face_(move.face, move.turns)
        elif move.type == MoveType.SLICE:
            self._slice(move.face, move.layer-1, move.layer, move.turns)
        elif move.type == MoveType.WIDE:
            self._slice(move.face, 0, move.layer, move.turns)
            self._rotate_face_(move.face, move.turns)
        elif move.type == MoveType.ROTATION:
            self._rotate_cube_(move.axis, move.turns)

    def apply_sequence(self, sequence: Sequence):
        for move in sequence:
            self.apply_move(move)

    def apply_sequence_display(self, sequence: Sequence, viewer: Viewer, delay=100):
        prev_time = time.time()
        for move in sequence:
            self.apply_move(move)
            if move.type == MoveType.ROTATION:
                pass
            viewer.update()

            elapsed = time.time() - prev_time
            frame_time = delay / 1000
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)

            prev_time = time.time()

    def reset(self):
        for i in range(6):
            self.faces[i] = i

    def _rotate_face_(self, face: Face, turns: int):
        self.faces[face.value] = np.rot90(self.faces[face.value], k=-turns)

    # axis:

    # X: L-R
    # Y: D-U
    # Z: B-F

    def _wide_slice_y(self, start=0, end=1, turns=1):
        _slice = slice(start, end)
        if turns == 1:
            temp = np.copy(self.faces[Face.F.value][_slice, :])
            self.faces[Face.F.value][_slice, :] = self.faces[Face.R.value][_slice, :]
            self.faces[Face.R.value][_slice, :] = self.faces[Face.B.value][_slice, :]
            self.faces[Face.B.value][_slice, :] = self.faces[Face.L.value][_slice, :]
            self.faces[Face.L.value][_slice, :] = temp
        elif turns == 2:
            temp = np.copy(self.faces[Face.F.value][_slice, :])
            self.faces[Face.F.value][_slice, :] = self.faces[Face.B.value][_slice, :]
            self.faces[Face.B.value][_slice, :] = temp
            temp = np.copy(self.faces[Face.R.value][_slice, :])
            self.faces[Face.R.value][_slice, :] = self.faces[Face.L.value][_slice, :]
            self.faces[Face.L.value][_slice, :] = temp
        elif turns == 3:
            temp = np.copy(self.faces[Face.F.value][_slice, :])
            self.faces[Face.F.value][_slice, :] = self.faces[Face.L.value][_slice, :]
            self.faces[Face.L.value][_slice, :] = self.faces[Face.B.value][_slice, :]
            self.faces[Face.B.value][_slice, :] = self.faces[Face.R.value][_slice, :]
            self.faces[Face.R.value][_slice, :] = temp

    def _wide_slice_x(self, start=0, end=1, turns=1):
        _slice = slice(start, end)
        _reverse = slice(self.n - end, self.n - start)
        for _ in range(turns):
            temp = np.copy(self.faces[Face.U.value][:, _reverse])
            self.faces[Face.U.value][:, _reverse] = self.faces[Face.F.value][:, _reverse]
            self.faces[Face.F.value][:, _reverse] = self.faces[Face.D.value][:, _reverse]
            self.faces[Face.D.value][:, _reverse] = np.flip(self.faces[Face.B.value][:, _slice], axis=(0, 1))
            self.faces[Face.B.value][:, _slice] = np.flip(temp, axis=(0, 1))

    def _wide_slice_z(self, start=0, end=1, turns=1):
        _slice = slice(start, end)
        _reverse = slice(self.n - end, self.n - start)
        for _ in range(turns):
            temp = np.copy(self.faces[Face.U.value][_reverse, :])
            self.faces[Face.U.value][_reverse, :] = np.flip(self.faces[Face.L.value][:, _reverse], axis=0).T
            self.faces[Face.L.value][:, _reverse] = np.flip(self.faces[Face.D.value][_slice, :], axis=0).T
            self.faces[Face.D.value][_slice, :] = np.flip(self.faces[Face.R.value][:, _slice], axis=0).T
            self.faces[Face.R.value][:, _slice] = np.flip(temp, axis=0).T
        

    def _slice(self, face: Face, start: int, end: int, turns: int):
        turns = turns % 4
        if face in [Face.B, Face.D, Face.L]:
            new_start = self.n - end
            end = self.n - start
            start = new_start
            turns = 4 - turns
        
        if face in [Face.U, Face.D]:
            self._wide_slice_y(start, end, turns)
        elif face in [Face.F, Face.B]:
            self._wide_slice_z(start, end, turns)
        elif face in [Face.R, Face.L]:
            self._wide_slice_x(start, end, turns)

    def _rotate_cube_(self, axis: int, turns: int):
        turns = turns % 4
        if axis == Axis.X:
            self._rotate_face_(Face.R, turns)
            self._rotate_face_(Face.L, 4 - turns)
            self._wide_slice_x(0, self.n, turns)
        elif axis == Axis.Y:
            self._rotate_face_(Face.U, turns)
            self._rotate_face_(Face.D, 4 - turns)
            self._wide_slice_y(0, self.n, turns)
        elif axis == Axis.Z:
            self._rotate_face_(Face.F, turns)
            self._rotate_face_(Face.B, 4 - turns)
            self._wide_slice_z(0, self.n, turns)


