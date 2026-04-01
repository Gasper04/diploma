import pytest
from cube.cube import Cube
from cube.axis import Axis
from cube.move import Move, MoveType


@pytest.mark.parametrize("axis", list(Axis))
@pytest.mark.parametrize("size", [2, 3, 4, 5, 6])
def test_whole_rotation(axis, size):
    cube = Cube(size)
    move = Move(type=MoveType.ROTATION, turns=-1, axis=axis)
    cube.apply_move(move)
    assert not cube.is_solved()
    cube.apply_move(move)
    cube.apply_move(move)
    cube.apply_move(move)
    assert cube.is_solved()
    move = Move(type=MoveType.ROTATION, turns=1, axis=axis)
    cube.apply_move(move)
    cube.apply_move(move)
    cube.apply_move(move)
    cube.apply_move(move)
    assert cube.is_solved()


@pytest.mark.parametrize("size", [2, 3, 4, 5, 6])
def test_mixed_rotations1(size):
    cube = Cube(size)
    movex = Move(type=MoveType.ROTATION, turns=1, axis=Axis.X)
    movey = Move(type=MoveType.ROTATION, turns=1, axis=Axis.Y)
    movez = Move(type=MoveType.ROTATION, turns=1, axis=Axis.Z)
    cube.apply_move(movex)
    cube.apply_move(movey)
    cube.apply_move(movez)
    assert not cube.is_solved()
    for _ in range(3):
        cube.apply_move(movex)
        cube.apply_move(movey)
        cube.apply_move(movez)
    assert cube.is_solved()

@pytest.mark.parametrize("size", [2, 3, 4, 5, 6])
def test_mixed_rotations2(size):
    cube = Cube(size)
    move_y = Move(type=MoveType.ROTATION, turns=1, axis=Axis.Y)
    move_z = Move(type=MoveType.ROTATION, turns=1, axis=Axis.Z)
    cube.apply_move(move_y)
    cube.apply_move(move_z)
    cube.apply_move(move_z)
    cube.apply_move(move_y)
    cube.apply_move(move_z)
    cube.apply_move(move_z)
    assert cube.is_solved()

