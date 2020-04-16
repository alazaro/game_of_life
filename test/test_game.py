import pytest

from src.game import Board, Config


@pytest.fixture(scope='module', autouse=True)
def config_():
    Config.alive_cells_at_start = 0
    Config.board_size = 5, 5


def test_create_board():
    b = Board()
    assert len(b.cells) == Config.board_size[0]
    assert len(b.cells[0]) == Config.board_size[1]
    assert not any((any(c) for c in b.cells))


def test_get_neighbors():
    b = Board()
    assert set(b.get_neighbors(1, 1)) == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    }


def test_alive_neighbors():
    b = Board()
    b.cells[0][1] = True
    assert b.get_alive_neighbors(1, 1) == [(0, 1)]


def test_next_status_stay_alive_2():
    b = Board()
    b.cells[0][1] = True
    b.cells[1][2] = True
    b.cells[1][1] = True
    assert b.get_next_status(1, 1) is True


def test_next_status_stay_alive_3():
    b = Board()
    b.cells[0][1] = True
    b.cells[1][2] = True
    b.cells[0][0] = True
    b.cells[1][1] = True
    assert b.get_next_status(1, 1) is True


def test_next_status_relive():
    b = Board()
    b.cells[0][1] = True
    b.cells[1][2] = True
    b.cells[0][0] = True
    b.cells[1][1] = False
    assert b.get_next_status(1, 1) is True


def test_next_status_die_overpopulation():
    b = Board()
    b.cells[0][1] = True
    b.cells[1][2] = True
    b.cells[0][0] = True
    b.cells[1][0] = True
    b.cells[1][1] = True
    assert b.get_next_status(1, 1) is False


def test_next_status_die_underpopulation():
    b = Board()
    b.cells[0][1] = True
    b.cells[1][1] = True
    assert b.get_next_status(1, 1) is False


def test_blinker():
    b = Board()
    b.cells[2][1] = True
    b.cells[2][2] = True
    b.cells[2][3] = True
    b.next_step()
    assert all((
        b.cells[3][2],
        b.cells[2][2],
        b.cells[1][2],
    ))
