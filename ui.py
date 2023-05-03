from itertools import product
from typing import Callable

import flet as ft

from core import Utils


ClbkFnType = Callable[[], None]  # CallbackFunctionType
ClkResetFnType = Callable[[ft.Page, 'GameState', int, int], None]


class GameState(Utils):
    '''
    Store the current state of the game
    '''

    def __init__(self) -> None:
        super().__init__(self)
        self.board = [[0] * 3 for _ in range(3)]
        self.current_player = 1  # 1 - > X; 2 -> O

    def set_cell_val(self, row: int, col: int) -> None:
        self.board[row][col] = self.current_player
        self.current_player = 1 if self.current_player == 2 else 2

    def get_cell_val(self, row: int, col: int) -> int:
        return self.board[row][col]

    def reset(self) -> None:
        for i, j in product(range(0, 3), range(0, 3)):
            self.board[i][j] = 0
        self.current_player = 1


class TicTacToe(ft.UserControl):

    def __init__(self) -> None:
        super().__init__()
        self.g_state = GameState()

    def build(self):
        self.game_grid = ft.GridView(
            runs_count=3,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )

        for i in range(9):
            self.game_grid.controls.append(
                ft.Container(
                    content=ft.Icon(),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.GREEN_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    on_click=lambda e, row=i // 3, col=i % 3: self.on_cell_click(
                        e, row=row, col=col)
                )
            )
        return self.game_grid

    def on_cell_click(self, e: ft.ContainerTapEvent, row: int, col: int):
        self.g_state.set_cell_val(row, col)
        e.control.on_click = None
        e.control.content = ft.Icon(
            name='circle_outlined' if self.g_state.current_player == 1 else 'close_outlined',
            size=20,
            color=ft.colors.BLACK
        )
        if (w := self.g_state.check_winner()) != 0 and w in (win_msg := {
            1: 'X Won, would you like to continue?',
            2: '0 Won, would you like to continue?'
        }):
            self.show_popup_msg(
                win_msg[w], self.reset_board, e.page.window_close)

        if (w == 0 and self.g_state.check_empty_space_exists() is False):
            self.show_popup_msg(
                'It\'s a Draw. Would you like to continue?', self.reset_board, e.page.window_close)
        self.update()

    def show_popup_msg(self, msg: str, yes_callback: ClbkFnType, no_callback: ClbkFnType) -> None:
        def close_dlg(e: ft.ContainerTapEvent, clbk: ClbkFnType) -> None:
            dlg.open = False
            self.page.update()
            clbk()

        dlg = ft.AlertDialog(
            title=ft.Text('Tic Tac Toe'),
            content=ft.Text(msg),
            actions=[
                ft.TextButton(
                    'Yes', on_click=lambda e: close_dlg(e, yes_callback)),
                ft.TextButton(
                    'No', on_click=lambda e: close_dlg(e, no_callback))
            ]
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def reset_board(self) -> None:
        self.g_state.reset()

        self.page.controls.clear()
        self.page.controls.append(TicTacToe())

        self.page.update()
        self.update()


def main(page: ft.Page) -> None:
    page.title = 'Tic Tac Toe AI'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 550
    page.window_height = 550

    app = TicTacToe()
    page.add(app)


if __name__ == '__main__':
    ft.app(target=main)
