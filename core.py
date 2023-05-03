from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui import GameState


class Utils:
    def __init__(self, state: GameState) -> None:
        self.state = state

    def check_empty_space_exists(self) -> bool:
        for i in range(3):
            for j in range(3):
                if self.state.board[i][j] == 0:
                    return True
        return False

    def check_winner(self) -> int:
        # 0 -> Draw; 1 -> X; 2 -> O
        board = [v for i in self.state.board for v in i]  # why not
        for i in range(1, 3):
            if ((board[0] == i and board[1] == i and board[2] == i) or
                    (board[3] == i and board[4] == i and board[5] == i) or
                    (board[6] == i and board[7] == i and board[8] == i) or
                    (board[0] == i and board[3] == i and board[6] == i) or
                    (board[1] == i and board[4] == i and board[7] == i) or
                    (board[2] == i and board[5] == i and board[8] == i) or
                    (board[0] == i and board[4] == i and board[8] == i) or
                    (board[2] == i and board[4] == i and board[6] == i)):
                return i
        else:
            return 0


class MinMax:
    pass
