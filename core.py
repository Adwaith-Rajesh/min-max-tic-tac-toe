from __future__ import annotations

from itertools import product
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

    def get_empty_spaces(self) -> list[tuple[int, int]]:
        empty_spaces: list[tuple[int, int]] = []
        for pos in product(range(0, 3), range(0, 3)):
            if self.state.board[pos[0]][pos[1]] == 0:
                empty_spaces.append(pos)
        return empty_spaces

    def in_terminal_state(self) -> tuple[bool, int]:
        # for the mini max alg
        # returns -1 -> O wins, 1 -> X wins 0 -> draw

        if (w := self.check_winner()) in (1, 2):
            return True, 10 if w == 1 else -10

        if w == 0 and (not self.check_empty_space_exists()) is False:
            return True, 0

        return False, 0

# AI always plays X


def min_max(state: GameState) -> float:
    # return -> best score
    if (v := state.in_terminal_state())[0] is False:
        return v[1]

    print(f'{v=}::{state.board=}::{state.current_player=}')

    if state.current_player == 1:  # maximizing player
        max_best_score = float('-inf')

        for move in state.get_empty_spaces():
            state.set_cell_val(move[0], move[1])
            val = min_max(state)
            max_best_score = max(max_best_score, val)
            state.board[move[0]][move[1]] = 0

        return max_best_score
    else:  # minimizing player
        min_best_score = float('inf')

        for move in state.get_empty_spaces():
            state.set_cell_val(move[0], move[1])
            val = min_max(state)
            min_best_score = min(min_best_score, val)
            state.board[move[0]][move[1]] = 0

        return min_best_score


# assuming the current player is the maximizing player
def get_best_move(state: GameState) -> tuple[int, int]:
    print(f'{state.board=}')
    best_score = float('-inf')
    best_move = (-1, -1)

    for move in state.get_empty_spaces():
        state.board[move[0]][move[1]] = 1
        state.current_player = 2
        score = min_max(state)

        if score > best_score:
            best_move = move
            best_score = score
        state.board[move[0]][move[1]] = 0

    return best_move
