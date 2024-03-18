import pygame
import sys
from pygame.locals import *
import math

# Constantes
WINDOW_SIZE = 800
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
CELL_SIZE = WINDOW_SIZE // 3

# Inicializar Pygame
pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Tic-Tac-Toe")

# Fontes
FONT = pygame.font.Font(None, 48)

# Variaveis do jogo
board = [[" " for _ in range(3)] for _ in range(3)]
game_over = False
player_piece = ""  # Quadrado do player
ai_piece = ""  # Quadrado da IA

# Tela do jogo
def draw_board():
    for i in range(1, 3):
        pygame.draw.line(WINDOW, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), 2)
        pygame.draw.line(WINDOW, LINE_COLOR, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), 2)

def draw_text(text, x, y):
    text_surface = FONT.render(text, True, LINE_COLOR)
    text_rect = text_surface.get_rect(center=(x, y))
    WINDOW.blit(text_surface, text_rect)

def check_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True

    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True

    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True

    return False

def is_board_full(board):
    return all([all([cell != " " for cell in row]) for row in board])

def get_free_positions(board):
    return [(row, col) for row in range(3) for col in range(3) if board[row][col] == " "]

def minimax(board, depth, is_maximizing):
    if check_winner(board, ai_piece):
        return 1
    elif check_winner(board, player_piece):
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row, col in get_free_positions(board):
            board[row][col] = ai_piece
            score = minimax(board, depth + 1, False)
            board[row][col] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row, col in get_free_positions(board):
            board[row][col] = player_piece
            score = minimax(board, depth + 1, True)
            board[row][col] = " "
            best_score = min(score, best_score)
        return best_score

def get_best_move(board):
    best_score = -math.inf
    best_move = None
    for row, col in get_free_positions(board):
        board[row][col] = ai_piece
        score = minimax(board, 0, False)
        board[row][col] = " "
        if score > best_score:
            best_score = score
            best_move = (row, col)
    return best_move

# Verificação do resultado do jogo
def draw_game_over(winner):
    if winner == "tie":
        draw_text("Empate!", WINDOW_SIZE // 2, WINDOW_SIZE // 2)
    elif winner == "Player":
        draw_text("Você Ganhou!", WINDOW_SIZE // 2, WINDOW_SIZE // 2)
    elif winner == "IA":
        draw_text("Você Perdeu!", WINDOW_SIZE // 2, WINDOW_SIZE // 2)

def reset_board():
    global board, game_over
    board = [[" " for _ in range(3)] for _ in range(3)]
    game_over = False

# Escolher o quadrado
def handle_click(row, col):
    global game_over
    if board[row][col] == " " and not game_over:
        board[row][col] = player_piece
        if check_winner(board, player_piece):
            game_over = True
        elif is_board_full(board):
            game_over = True
        else:
            ai_row, ai_col = get_best_move(board)
            board[ai_row][ai_col] = ai_piece
            if check_winner(board, ai_piece):
                game_over = True
            elif is_board_full(board):
                game_over = True
                
# Opção de escolha "X" ou "O"
def choose_piece():
    global player_piece, ai_piece
    chosen = False
    while not chosen:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_x:
                    player_piece = "X"
                    ai_piece = "O"
                    chosen = True
                elif event.key == K_o:
                    player_piece = "O"
                    ai_piece = "X"
                    chosen = True

        WINDOW.fill(BG_COLOR)
        draw_text("Escolha X ou O:", WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 50)
        draw_text("Pressione 'X' para X ou 'O' para O", WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 50)
        pygame.display.update()

choose_piece()  #Deixe o jogador escolher X ou O
reset_board()   # Reseta o Jogo
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            handle_click(row, col)
        if event.type == KEYDOWN and event.key == K_r: # Tecla "R" para resetar o jogo
            reset_board()

    WINDOW.fill(BG_COLOR)
    draw_board()

    for row in range(3):
        for col in range(3):
            if board[row][col] != " ":
                draw_text(board[row][col], col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
    
    #Verificação do resultado 
    if game_over:
        winner = "Player" if check_winner(board, player_piece) else "IA" if check_winner(board, ai_piece) else "tie"
        draw_game_over(winner)

    pygame.display.update()
