import pygame


WIDTH: int = 500
HEIGHT: int = 500
ROWS: int = 10
COLS: int = 10
SQUARE_SIZE: int = WIDTH // COLS


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe 2: Electric Boogaloo")


FONT = pygame.font.Font(None, 50)


def make_board():
    board_layout = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    return board_layout


def draw_board(board_layout):
    screen.fill(BLACK)

    for row_element in range(ROWS):
        for col_element in range(COLS):
            pygame.draw.rect(screen, WHITE, (
                col_element * SQUARE_SIZE,
                row_element * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            ))
            pygame.draw.rect(screen, BLACK, (
                col_element * SQUARE_SIZE + 2,
                row_element * SQUARE_SIZE + 2,
                SQUARE_SIZE - 4,
                SQUARE_SIZE - 4
            ))

            if board_layout[row_element][col_element] != ' ':
                symbol = FONT.render(
                    board_layout[row_element][col_element],
                    True, WHITE
                )

                symbol_rect = symbol.get_rect(center=(
                    col_element * SQUARE_SIZE + SQUARE_SIZE // 2,
                    row_element * SQUARE_SIZE + SQUARE_SIZE // 2
                ))

                screen.blit(symbol, symbol_rect)

    pygame.display.flip()


def check_winner(board_layout, player):
    # rows
    for row_element in board_layout:
        for start_col in range(COLS - 4):
            sequence = row_element[start_col:start_col + 5]
            if all(symbol == player for symbol in sequence):
                return True

    # columns
    for col_element in range(COLS):
        for start_row in range(ROWS - 4):
            sequence = [board_layout[start_row + i][col_element] for i in range(5)]
            if all(symbol == player for symbol in sequence):
                return True

    # diagonals from top left to bottom right
    for start_row in range(ROWS - 4):
        for start_col in range(COLS - 4):
            sequence = [board_layout[start_row + i][start_col + i] for i in range(5)]
            if all(symbol == player for symbol in sequence):
                return True

    # diagonals from bottom left to top right
    for start_row in range(ROWS - 4):
        for start_col in range(COLS - 1, 3, -1):
            sequence = [board_layout[start_row + i][start_col - i] for i in range(5)]
            if all(symbol == player for symbol in sequence):
                return True

    return False


board = make_board()
current_player = 'X'
end_game = False


def get_row_col_from_mouse(positon):
    x, y = positon
    row_element = y // SQUARE_SIZE
    col_element = x // SQUARE_SIZE
    return row_element, col_element


def print_winner(player):
    print("{}{}{}".format("WYGRYWA GRACZ ", player, "!"))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not end_game:
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_mouse(pos)

            if board[row][col] == ' ':
                board[row][col] = current_player
                if check_winner(board, current_player):
                    print_winner(current_player)
                    end_game = True
                elif all(board[i][j] != ' ' for i in range(ROWS) for j in range(COLS)):
                    print("REMIS")
                    end_game = True
                else:
                    current_player = 'O' if current_player == 'X' else 'X'

    draw_board(board)

pygame.quit()
