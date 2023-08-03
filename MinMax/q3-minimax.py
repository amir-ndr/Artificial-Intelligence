import numpy as np
import random
import pygame
import sys
import math

class Board:

    def __init__(self, row_number, col_number):
        
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.BLUE = (0,0,255)
        self.player_turn = 1
        self.ai_turn = 2
        self.PLAYER = 0
        self.AI = 1

        self.row_number = row_number
        self.col_number = col_number

        self.width = col_number * 70
        self.height = (row_number+1) * 70

        size = (self.width, self.height)

        self.RADIUS = int(70/2 - 5)
        pygame.init()

        self.screen = pygame.display.set_mode(size)

    def construct_the_board(self):
        board = np.zeros((self.row_number,self.col_number))
        return board

    def put(self, board, row, col, piece):
        board[row][col] = piece

    def validate_loc(self, board, col):
        return board[self.row_number-1][col] == 0

    def next_empty_loc(self, board, col):
        for r in range(self.col_number):
            if board[r][col] == 0:
                return r
    
    def show_the_board(self, board):
        print(np.flip(board, 0))

    def is_win(self, board, piece):

        for col in range(self.col_number-3):
            for row in range(self.row_number):
                if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                    return True

        for col in range(self.col_number):
            for row in range(self.row_number-3):
                if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                    return True

        for col in range(self.col_number-3):
            for row in range(self.row_number-3):
                if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                    return True

        for col in range(self.col_number-3):
            for row in range(3, self.row_number):
                if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                    return True

    def return_score(self, candidate, piece):
        opp_piece = self.ai_turn
        if piece == self.ai_turn:
            opp_piece = self.player_turn

        score = 0

        if candidate.count(piece) == 4:
            score += 100
        elif candidate.count(piece) == 3 and candidate.count(0) == 1:
            score += 70
        elif candidate.count(piece) == 2 and candidate.count(0) == 2:
            score += 20
        if candidate.count(opp_piece) == 3 and candidate.count(0) == 1:
            score -= 40

        return score

    def return_all_score_conditions(self, board, piece):
        score = 0

        center_array = [int(i) for i in list(board[:, self.col_number//2])]
        center_count = center_array.count(piece)
        score += center_count * 3


        for r in range(self.row_number-3):
            for c in range(self.col_number-3):
                candidate = [board[r+i][c+i] for i in range(4)]
                score += self.return_score(candidate, piece)

        for r in range(self.row_number-3):
            for c in range(self.col_number-3):
                candidate = [board[r+3-i][c+i] for i in range(4)]
                score += self.return_score(candidate, piece)

        for r in range(self.row_number):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(self.col_number-3):
                candidate = row_array[c:c+4]
                score += self.return_score(candidate, piece)

        for c in range(self.col_number):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(self.row_number-3):
                candidate = col_array[r:r+4]
                score += self.return_score(candidate, piece)

        return score
    
    def is_terminal_node(self, board):
        return self.is_win(board, self.player_turn) or self.is_win(board, self.ai_turn) or len(self.collect_best_cols(board)) == 0

    def minimax_algorithm(self, board, d, alpha, beta, maximizingPlayer):
        valid_locations = self.collect_best_cols(board)
        is_terminal = self.is_terminal_node(board)
        if d == 0 or is_terminal:
            if is_terminal:
                if self.is_win(board, self.ai_turn):
                    return (None, math.inf)
                elif self.is_win(board, self.player_turn):
                    return (None, -math.inf)
                else:
                    return (None, 0)
            else:
                return (None, self.return_all_score_conditions(board, self.ai_turn))

        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.next_empty_loc(board, col)
                b_copy = board.copy()
                self.put(b_copy, row, col, self.ai_turn)
                new_score = self.minimax_algorithm(b_copy, d-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.next_empty_loc(board, col)
                b_copy = board.copy()
                self.put(b_copy, row, col, self.player_turn)
                new_score = self.minimax_algorithm(b_copy, d-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def collect_best_cols(self, board):
        valid_locations = []
        for col in range(self.col_number):
            if self.validate_loc(board, col):
                valid_locations.append(col)
        return valid_locations

    def board_pygame(self, board):
        for c in range(self.col_number):
            for r in range(self.row_number):
                pygame.draw.rect(self.screen, self.BLACK, (c*70, (r+1)*70, 70, 70))
                pygame.draw.circle(self.screen, self.WHITE, (int(c*70+70/2), int((r+1)*70+70/2)), self.RADIUS)
        
        for c in range(self.col_number):
            for r in range(self.row_number):		
                if board[r][c] == self.player_turn:
                    pygame.draw.circle(self.screen, self.RED, (int(c*70+70/2), self.height-int(r*70+70/2)), self.RADIUS)
                elif board[r][c] == self.ai_turn: 
                    pygame.draw.circle(self.screen, self.BLUE, (int(c*70+70/2), self.height-int(r*70+70/2)), self.RADIUS)
        pygame.display.update()

    def game_ai_human(self):

        myfont = pygame.font.SysFont("monospace", 45)

        turn = random.randint(0, 1)
        game_over = False
        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.WHITE, (0,0, self.width, 70))

                    if turn == self.PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx/70))

                        if self.validate_loc(board, col):
                            row = self.next_empty_loc(board, col)
                            self.put(board, row, col, self.player_turn)

                            if self.is_win(board, self.player_turn):
                                label = myfont.render("Player 1 wins", 1, self.RED)
                                self.screen.blit(label, (40,10))
                                game_over = True

                            turn += 1
                            turn = turn % 2

                            self.show_the_board(board)
                            self.board_pygame(board)


            if turn == self.AI and not game_over:				

                col, _ = self.minimax_algorithm(board, 5, -math.inf, math.inf, True)

                if self.validate_loc(board, col):
                    row = self.next_empty_loc(board, col)
                    self.put(board, row, col, self.ai_turn)

                    if self.is_win(board, self.ai_turn):
                        label = myfont.render("Player 2 wins", 1, self.BLACK)
                        self.screen.blit(label, (20,10))
                        game_over = True

                    self.show_the_board(board)
                    self.board_pygame(board)

                    turn += 1
                    turn = turn % 2

            if game_over:
                pygame.time.wait(2000)

    def game_human_human(self):

        myfont = pygame.font.SysFont("monospace", 45)

        turn = random.randint(0, 1)
        game_over = False
        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.WHITE, (0,0, self.width, 70))

                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/70))

                        if self.validate_loc(board, col):
                            row = self.next_empty_loc(board, col)
                            self.put(board, row, col, 1)

                            if self.is_win(board, 1):
                                label = myfont.render("Player 1 wins", 1, self.RED)
                                self.screen.blit(label, (40,10))
                                game_over = True

                            turn += 1
                            turn = turn % 2

                            self.show_the_board(board)
                            self.board_pygame(board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.WHITE, (0,0, self.width, 70))
                    if turn == 1 and not game_over:				

                        posx = event.pos[0]
                        col = int(math.floor(posx/70))

                        if self.validate_loc(board, col):
                            row = self.next_empty_loc(board, col)
                            self.put(board, row, col, 2)

                            if self.is_win(board, 2):
                                label = myfont.render("Player 2 wins", 1, self.BLUE)
                                self.screen.blit(label, (40,10))
                                game_over = True

                            turn += 1
                            turn = turn % 2

                            self.show_the_board(board)
                            self.board_pygame(board)

            if game_over:
                pygame.time.wait(2000)

    def game_ai_ai(self):

        myfont = pygame.font.SysFont("monospace", 45)

        turn = random.randint(0, 1)
        game_over = False
        while not game_over:

            pygame.draw.rect(self.screen, self.WHITE, (0,0, self.width, 70))
            if turn == 0 and not game_over:				

                col, _ = self.minimax_algorithm(board, 5, -math.inf, math.inf, True)

                if self.validate_loc(board, col):
                    row = self.next_empty_loc(board, col)
                    self.put(board, row, col, 1)

                    if self.is_win(board, 1):
                        label = myfont.render("AI 1 wins", 1, self.BLACK)
                        self.screen.blit(label, (20,10))
                        game_over = True

                    self.show_the_board(board)
                    self.board_pygame(board)

                    turn += 1
                    turn = turn % 2
                    pygame.time.wait(1000)

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         sys.exit()
                pygame.draw.rect(self.screen, self.WHITE, (0,0, self.width, 70))
            if turn == 1 and not game_over:				

                col, _ = self.minimax_algorithm(board, 4, -math.inf, math.inf, True)

                if self.validate_loc(board, col):
                    row = self.next_empty_loc(board, col)
                    self.put(board, row, col, 2)

                    if self.is_win(board, 2):
                        label = myfont.render("AI 2 wins", 1, self.BLACK)
                        self.screen.blit(label, (20,10))
                        game_over = True

                    self.show_the_board(board)
                    self.board_pygame(board)

                    turn += 1
                    turn = turn % 2
                    pygame.time.wait(1000)

            if game_over:
                pygame.time.wait(5000)


row_number = int(input('input row number: '))
col_number = int(input('input col number: '))

obj = Board(row_number=row_number, col_number=col_number)
board = obj.construct_the_board()
obj.show_the_board(board)

obj.board_pygame(board)
pygame.display.update()

play_mode = int(input('choose play mode (1.player vs player), (2.player vs ai), (3. ai vs ai): '))
if play_mode == 1:
    obj.game_human_human()
elif play_mode == 2:
    obj.game_ai_human()
elif play_mode == 3:
    obj.game_human_human()