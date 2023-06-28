import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 900
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

class BreakthroughGame:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = random.choice([BLACK, GREEN])
        self.selected_piece = None
        self.players = {BLACK: ("Human", 16), GREEN: ("Human", 16)}

    def create_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if row < 2:
                    color = BLACK
                elif row > ROWS - 3:
                    color = GREEN
                else:
                    color = None
                if color:
                    self.board[row][col] = Piece(row, col, color)

    def draw_board(self, win):
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else RED
                pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = self.board[row][col]
                if piece:
                    pygame.draw.circle(win, piece.color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

        font = pygame.font.SysFont(None, 30)
        black_text = font.render(f"Black: {self.players[BLACK][1]}", True, BLACK)
        green_text = font.render(f"Green: {self.players[GREEN][1]}", True, GREEN)
        turn_text = font.render(f"Turn: {self.players[self.turn][0]}", True, self.turn)
        win.blit(black_text, (20, 800))
        win.blit(green_text, (WIDTH - green_text.get_width() - 20, 800))
        win.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, 850))

    def select_piece(self, row, col):
        piece = self.board[row][col]
        if piece and piece.color == self.turn:
            self.selected_piece = piece

    def move_piece(self, row, col):
        if self.selected_piece:
            if row < 0 or row >= ROWS or col < 0 or col >= COLS:
                return
            if self.board[row][col] is None or self.board[row][col].color != self.selected_piece.color:
                if self.selected_piece.color == BLACK and row < self.selected_piece.row:
                    return
                elif self.selected_piece.color == GREEN and row > self.selected_piece.row:
                    return

                if row == self.selected_piece.row:
                    return

                if col > self.selected_piece.col + 1 or col < self.selected_piece.col -1:
                    return
                
                if self.selected_piece.color == BLACK and row > self.selected_piece.row + 1:
                    return
                elif self.selected_piece.color == GREEN and row < self.selected_piece.row - 1:
                    return

                if self.board[row][col] is not None:
                    self.log_error_message(row, col)
                    other_color = self.board[row][col].color
                    self.players[other_color] = (self.players[other_color][0], self.players[other_color][1] - 1)

                    if self.players[other_color][1] < 1:
                        if self.turn == BLACK:
                            print("Black wins!")
                        elif self.turn == GREEN:
                            print("Green wins!")

                self.board[self.selected_piece.row][self.selected_piece.col] = None
                self.selected_piece.row = row
                self.selected_piece.col = col
                self.board[row][col] = self.selected_piece

                if self.turn == BLACK and row > 6:
                    print("Black wins!")

                elif self.turn == GREEN and row < 1:
                    print("Green wins!")
                
                self.selected_piece = None
                self.turn = GREEN if self.turn == BLACK else BLACK

    def log_error_message(self, row, col):
        player_color = self.turn
        player_name = self.players[player_color][0]
        piece_color = self.board[row][col].color
        piece_location = f"({self.board[row][col].row}, {self.board[row][col].col})"
        error_message = f"Error: {player_name} attempted to move onto {piece_color} piece at {piece_location}"
        print(error_message)

    def show_menu(self):
        pygame.init()
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Breakthrough Game")
        clock = pygame.time.Clock()

        font = pygame.font.SysFont(None, 40)
        title_text = font.render("Breakthrough Game Menu", True, WHITE)
        start_button = pygame.Rect(300, 400, 200, 50)
        start_text = font.render("Start Game", True, BLACK)
        exit_button = pygame.Rect(300, 500, 200, 50)
        exit_text = font.render("Exit", True, BLACK)
        ai_button = pygame.Rect(300, 300, 200, 50)
        ai_text = font.render("Toggle AI", True, BLACK)

        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(pos):
                        self.play()
                        running = False
                    elif exit_button.collidepoint(pos):
                        running = False
                    elif ai_button.collidepoint(pos):
                        self.toggle_ai()

            win.fill(BLACK)
            pygame.draw.rect(win, GREEN, start_button)
            pygame.draw.rect(win, RED, exit_button)
            pygame.draw.rect(win, BLACK, ai_button)
            win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 200))
            win.blit(start_text, (start_button.x + start_button.width // 2 - start_text.get_width() // 2, start_button.y + start_button.height // 2 - start_text.get_height() // 2))
            win.blit(exit_text, (exit_button.x + exit_button.width // 2 - exit_text.get_width() // 2, exit_button.y + exit_button.height // 2 - exit_text.get_height() // 2))
            ai_mode_text = "AI Mode: ON" if self.players[BLACK][0] == "AI" else "AI Mode: OFF"
            win.blit(ai_text, (ai_button.x + ai_button.width // 2 - ai_text.get_width() // 2, ai_button.y + ai_button.height // 2 - ai_text.get_height() // 2))
            win.blit(font.render(ai_mode_text, True, WHITE), (WIDTH // 2 - ai_text.get_width() // 2, 250))
            
            pygame.display.update()

        pygame.quit()

    def toggle_ai(self):
        self.players[BLACK] = ("AI", 16) if self.players[BLACK][0] == "Human" else ("Human", 16)

    def play(self):
        pygame.init()
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Breakthrough Game")
        clock = pygame.time.Clock()

        self.create_board()

        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.players[self.turn][0] == "Human":
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // SQUARE_SIZE
                        row = pos[1] // SQUARE_SIZE
                        if not self.selected_piece:
                            self.select_piece(row, col)
                        else:
                            self.move_piece(row, col)
            
            if self.players[self.turn][0] == "AI" and not self.selected_piece:
                self.ai_move()
                #pygame.time.wait(500)  # Delay between AI moves

            self.draw_board(win)
            pygame.display.update()

        pygame.quit()

    def ai_move(self):
        available_pieces = []
        for row in self.board:
            for piece in row:
                if piece and piece.color == self.turn:
                    available_pieces.append(piece)

        selected_piece = random.choice(available_pieces)
        valid_moves = []
        for row in range(selected_piece.row - 1, selected_piece.row + 2):
            for col in range(selected_piece.col - 1, selected_piece.col + 2):
                if row < 0 or row >= ROWS or col < 0 or col >= COLS:
                    continue
                if self.board[row][col] is None or self.board[row][col].color != selected_piece.color:
                    if selected_piece.color == BLACK and row < selected_piece.row:
                        continue
                    elif selected_piece.color == GREEN and row > selected_piece.row:
                        continue
                    if row == selected_piece.row or col > selected_piece.col + 1 or col < selected_piece.col - 1:
                        continue
                    if selected_piece.color == BLACK and row > selected_piece.row + 1:
                        continue
                    elif selected_piece.color == GREEN and row < selected_piece.row - 1:
                        continue
                    valid_moves.append((row, col))

        if valid_moves:
            selected_move = random.choice(valid_moves)
            self.move_piece(selected_move[0], selected_move[1])

if __name__ == "__main__":
    game = BreakthroughGame()
    game.show_menu()
