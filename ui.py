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


def show_popup_msg(page: ft.Page, msg: str, yes_callback: ClbkFnType, no_callback: ClbkFnType) -> None:

    def close_dlg(e: ft.ContainerTapEvent, clbk: ClbkFnType) -> None:
        dlg.open = False
        e.page.update()
        clbk()

    dlg = ft.AlertDialog(
        title=ft.Text('Tic Tac Toe'),
        content=ft.Text(msg),
        actions=[
            ft.TextButton(
                'Yes', on_click=lambda e: close_dlg(e, yes_callback)),
            ft.TextButton('No', on_click=lambda e: close_dlg(e, no_callback))
        ]
    )

    page.dialog = dlg
    dlg.open = True
    page.update()


def reset_board(page: ft.Page, state: GameState, click_reset_fn: ClkResetFnType) -> None:
    state.reset()

    for row in page.controls:  # gives the three rows that we initially set
        for col in row.controls:  # gives each ft.Container
            col.content = None
            col.no_click = click_reset_fn

    page.update()


def button_clicked(e: ft.ContainerTapEvent, state: GameState, row: int, col: int) -> None:
    state.set_cell_val(row, col)
    e.control.on_click = None
    e.control.content = ft.Icon(
        name='circle_outlined' if state.current_player == 1 else 'close_outlined',
        size=20,
        color=ft.colors.BLACK
    )
    if (w := state.check_winner()) in (win_msg := {
        1: 'X Won, would you like to continue?',
        2: '0 Won, would you like to continue?'
    }):
        show_popup_msg(e.page, win_msg[w], lambda: reset_board(
            e.page, state, button_clicked), e.page.window_close)

    if (w == 0 and state.check_empty_space_exists() is False):
        show_popup_msg(e.page, 'It\'s a Draw. Would you like to continue?',
                       lambda: reset_board(e.page, state, button_clicked), e.page.window_close)
    e.page.update()


def build_ui(page: ft.Page, game: GameState) -> None:
    for i in range(3):
        page.add(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(),
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.GREEN_200,
                        width=150,
                        height=150,
                        border_radius=10,
                        on_click=lambda e, state=game, row=i, col=j: button_clicked(
                            e, state, row, col
                        )
                    ) for j in range(3)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )


def main(page: ft.Page) -> None:
    page.title = 'Tic Tac Toe AI'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 550
    page.window_height = 550

    game = GameState()
    build_ui(page, game)
    page.update()


if __name__ == '__main__':
    ft.app(target=main)
