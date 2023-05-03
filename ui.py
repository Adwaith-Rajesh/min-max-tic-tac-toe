import flet as ft


class GameState:
    '''
    Store the current state of the game
    '''

    def __init__(self) -> None:
        self.board = [[8] * 3] * 3
        self.current_player = 1  # 1 - > X; 2 -> O

    def set_cell_val(self, row: int, col: int) -> None:
        self.board[row][col] = self.current_player
        self.current_player = 1 if self.current_player == 2 else 2

    def get_cell_val(self, row: int, col: int) -> int:
        return self.board[row][col]


def button_clicked(e: ft.ContainerTapEvent, state: GameState, row: int, col: int) -> None:
    state.set_cell_val(row, col)
    e.control.on_click = None
    e.control.content = ft.Icon(
        name='circle_outlined' if state.current_player == 1 else 'close_outlined',
        size=20,
        color=ft.colors.BLACK
    )
    e.page.update()


def main(page: ft.Page) -> None:
    page.title = 'Tic Tac Toe AI'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 550
    page.window_height = 550

    game = GameState()

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
                        on_click=lambda e, state=game, row=1, col=j: button_clicked(
                            e, state, row, col
                        )
                    ) for j in range(3)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )


if __name__ == '__main__':
    ft.app(target=main)
