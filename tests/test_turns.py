import pytest
from cube.cube import Cube
from cube.face import Face
from cube.move import Move, MoveType
from cube.scramble import generate_scramble


@pytest.mark.parametrize("size", [2, 3, 4, 5, 6])
@pytest.mark.parametrize("face", list(Face))
@pytest.mark.parametrize("turns", [1, 2, 3])
def test_360_turn(size, face, turns):
    cube = Cube(size)
    face_pre = Face.F if face not in [Face.F, Face.B] else Face.U
    move_pre = Move(type=MoveType.FACE, turns=turns, face=face_pre)
    move_post = Move(type=MoveType.FACE, turns=-turns, face=face_pre)
    for layers in range(1, size):
        move = Move(type=MoveType.WIDE, turns=turns, face=face, layer=layers)
        cube.apply_move(move_pre)
        cube.apply_move(move)
        assert not cube.is_solved()
        for _ in range(3):
            cube.apply_move(move)
        cube.apply_move(move_post)
        assert cube.is_solved()

@pytest.mark.parametrize("seed", list(range(100)))
@pytest.mark.parametrize("size", [2, 3, 4, 5, 6])
@pytest.mark.parametrize("faces", [(Face.R, Face.U), (Face.L, Face.F), (Face.B, Face.D)])
def test_mixed_turns(size, faces, seed):
    cube = Cube(size)
    scr = generate_scramble(size, relative_length=0.2, seed=seed)
    for layers in range(1, size//2 + 1):
        move1 = Move(type=MoveType.WIDE, turns=1, face=faces[0], layer=layers)
        move2 = Move(type=MoveType.WIDE, turns=1, face=faces[1], layer=layers)
        move3 = Move(type=MoveType.WIDE, turns=-1, face=faces[0], layer=layers)
        move4 = Move(type=MoveType.WIDE, turns=-1, face=faces[1], layer=layers)
        cube.apply_sequence(scr)
        cube.apply_move(move1)
        cube.apply_move(move2)
        cube.apply_move(move3)
        cube.apply_move(move4)
        for _ in range(5):
            assert not cube.is_solved()
            cube.apply_move(move1)
            cube.apply_move(move2)
            cube.apply_move(move3)
            cube.apply_move(move4)
        cube.apply_sequence(scr.inverted())
        assert cube.is_solved()

@pytest.mark.parametrize("size", [3, 4, 5, 6])
@pytest.mark.parametrize("face", list(Face))
@pytest.mark.parametrize("turns", [1, 2, 3])
def test_wide_slice_face(size, face, turns):
    cube = Cube(size)
    face_pre = Face.F if face not in [Face.F, Face.B] else Face.U
    move_pre = Move(type=MoveType.FACE, turns=1, face=face_pre)
    move_post = Move(type=MoveType.FACE, turns=-1, face=face_pre)
    move_wide = Move(type=MoveType.WIDE, turns=turns, face=face, layer=2)
    move_slice = Move(type=MoveType.SLICE, turns=4-turns, face=face, layer=2)
    move_face = Move(type=MoveType.FACE, turns=4-turns, face=face)
    cube.apply_move(move_pre)
    cube.apply_move(move_wide)
    cube.apply_move(move_slice)
    cube.apply_move(move_face)
    cube.apply_move(move_post)
    assert cube.is_solved()