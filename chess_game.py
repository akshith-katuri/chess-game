from typing import List, Tuple
import pygame


class ChessGame:
    def __init__(self):
        pygame.init()  # initialize pygame
        self.WIDTH = 1000  # chess screen width
        self.HEIGHT = 800  # chess screen height
        # Start point of board
        self.board_start = (50, 100)
        self.CAPTION = 'CHESS'
        self.SQUARE_SIZE = 65
        self.timer = pygame.time.Clock()
        self.fps = 60  # frames per second
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # chess screen width and height
        self.running = True

        # Initialize game variables and images
        self.initialize_game()
        self.initialize_piece_images()

    def initialize_game(self):
        self.player_turn = 'white'  # set first player turn
        self.valid_moves = []
        self.piece_list = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        self.black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                           'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                           'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        self.white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        self.captured_pieces_white = []
        self.captured_pieces_black = []

        self.click_pos = ()
        self.move_pos = ()
        # Boolean on the left is for en passant to the left, on the right for the right
        self.en_passant = [False, False]
        self.en_passant_move = ()
        self.en_passant_pieces = []
        self.is_moved = False
        # Boolean on the left is for short side castling, on the right for far side
        self.is_king_moved = [False, False]
        self.is_rook_moved = [[False, False], [False, False]]
        self.is_pawn_promotion = False
        self.is_game_over = False
        self.selection = 100
        self.counter = 0

    def initialize_piece_images(self):
        # Load game piece images
        self.black_queen = pygame.image.load('images/black_queen.png')
        self.black_queen = pygame.transform.scale(self.black_queen, (65, 65))
        self.black_queen_small = pygame.transform.scale(self.black_queen, (45, 45))
        self.black_king = pygame.image.load('images/black_king.png')
        self.black_king = pygame.transform.scale(self.black_king, (65, 65))
        self.black_king_small = pygame.transform.scale(self.black_king, (45, 45))
        self.black_rook = pygame.image.load('images/black_rook.png')
        self.black_rook = pygame.transform.scale(self.black_rook, (65, 65))
        self.black_rook_small = pygame.transform.scale(self.black_rook, (45, 45))
        self.black_bishop = pygame.image.load('images/black_bishop.png')
        self.black_bishop = pygame.transform.scale(self.black_bishop, (65, 65))
        self.black_bishop_small = pygame.transform.scale(self.black_bishop, (45, 45))
        self.black_knight = pygame.image.load('images/black_knight.png')
        self.black_knight = pygame.transform.scale(self.black_knight, (65, 65))
        self.black_knight_small = pygame.transform.scale(self.black_knight, (45, 45))
        self.black_pawn = pygame.image.load('images/black_pawn.png')
        self.black_pawn = pygame.transform.scale(self.black_pawn, (62, 62))
        self.black_pawn_small = pygame.transform.scale(self.black_pawn, (45, 45))
        self.white_queen = pygame.image.load('images/white_queen.png')
        self.white_queen = pygame.transform.scale(self.white_queen, (65, 65))
        self.white_queen_small = pygame.transform.scale(self.white_queen, (45, 45))
        self.white_king = pygame.image.load('images/white_king.png')
        self.white_king = pygame.transform.scale(self.white_king, (65, 65))
        self.white_king_small = pygame.transform.scale(self.white_king, (45, 45))
        self.white_rook = pygame.image.load('images/white_rook.png')
        self.white_rook = pygame.transform.scale(self.white_rook, (65, 65))
        self.white_rook_small = pygame.transform.scale(self.white_rook, (45, 45))
        self.white_bishop = pygame.image.load('images/white_bishop.png')
        self.white_bishop = pygame.transform.scale(self.white_bishop, (65, 65))
        self.white_bishop_small = pygame.transform.scale(self.white_bishop, (45, 45))
        self.white_knight = pygame.image.load('images/white_knight.png')
        self.white_knight = pygame.transform.scale(self.white_knight, (65, 65))
        self.white_knight_small = pygame.transform.scale(self.white_knight, (45, 45))
        self.white_pawn = pygame.image.load('images/white_pawn.png')
        self.white_pawn = pygame.transform.scale(self.white_pawn, (62, 62))
        self.white_pawn_small = pygame.transform.scale(self.white_pawn, (45, 45))

        self.white_images = [self.white_pawn, self.white_knight, self.white_bishop, self.white_rook, self.white_queen,
                             self.white_king]
        self.small_white_images = [self.white_pawn_small, self.white_knight_small, self.white_bishop_small,
                                   self.white_rook_small, self.white_queen_small, self.white_king_small]
        self.black_images = [self.black_pawn, self.black_knight, self.black_bishop, self.black_rook, self.black_queen,
                             self.black_king]
        self.small_black_images = [self.black_pawn_small, self.black_knight_small, self.black_bishop_small,
                                   self.black_rook_small, self.black_queen_small, self.black_king_small]

    def draw_board(self):
        """
        This function is responsible for drawing 8*8 chess board using pygame draw funciton at the correct psition
        """
        for i in range(64):
            column, row = i % 8, i // 8
            color = (200, 200, 200) if (row % 2 == 0 and i % 2 == 0) or (row % 2 != 0 and i % 2 == 1) else (0, 113, 0)
            
            pygame.draw.rect(self.screen, color,
                            pygame.Rect(self.board_start[0] + column * self.SQUARE_SIZE,
                                        self.board_start[1] + row * self.SQUARE_SIZE,
                                        self.SQUARE_SIZE, self.SQUARE_SIZE))
    
    def draw_pieces(self):
        """
        This function is responsible for drawing the pieces at their correct location after every move, displaying
        all the possible moves of any selected piece and the visual graphics for checkmate, stalemate, pawn promotion and new game
        """
        for i in range(len(self.white_pieces)):
            piece = self.white_pieces[i]
            index = self.piece_list.index(piece)
                
            if self.player_turn == 'white' and not self.is_game_over and not self.is_pawn_promotion:
                # Displays WHITE'S TURN
                font = pygame.font.Font('freesansbold.ttf', 30)
                text = font.render("WHITE'S TURN", True, (0,0,0), (255,255,255))
                textRect = text.get_rect()
                textRect.center = (315, 725)
                self.screen.blit(text, textRect)

                # Flash king square with red border when in check
                if self.is_king_in_check('white') and self.counter < 15:
                    pygame.draw.rect(self.screen, (240, 0, 0),
                                         pygame.Rect(
                                             self.white_locations[self.white_pieces.index('king')][0] * self.SQUARE_SIZE + self.board_start[0],
                                             self.white_locations[self.white_pieces.index('king')][1] * self.SQUARE_SIZE + self.board_start[1],
                                             self.SQUARE_SIZE,
                                             self.SQUARE_SIZE), 5)
                
                if self.selection == i:
                    if self.is_moved:
                        self.is_moved = False
                        self.player_turn = 'black'
                        self.selection = 100
                        
                        # Taking pieces
                        if self.move_pos in self.black_locations:
                            black_piece_index = self.black_locations.index(self.move_pos)
                            self.captured_pieces_black.append(self.black_pieces[black_piece_index])
                            # Removing piece
                            self.black_locations.remove(self.move_pos)
                            self.black_pieces.pop(black_piece_index)
                        
                        # Castling
                        elif piece == 'king':
                            if self.move_pos == (2, 7):
                                self.white_locations[0] = (3, 7)
                            elif self.move_pos == (6, 7):
                                self.white_locations[self.white_locations.index(((7, 7)))] = (5, 7)
                            self.is_king_moved[0] = True
                        
                        # En passant
                        elif piece == 'pawn':
                            self.en_passant_pieces = []
                            self.en_passant = [False, False]
                            if self.en_passant_move == self.move_pos:
                                self.en_passant = [False, False]
                                black_piece_index = self.black_locations.index((self.move_pos[0], self.move_pos[1] + 1))
                                self.captured_pieces_black.append(self.black_pieces[black_piece_index])
                                # Removing piece
                                self.black_locations.remove((self.move_pos[0], self.move_pos[1] + 1))
                                self.black_pieces.pop(black_piece_index)
                        
                        # Checks for pawn promotion
                        if self.move_pos[1] == 0 and piece == 'pawn':
                            self.is_pawn_promotion = True
                        
                        # Checks whether black pawns can en passant
                        if piece == 'pawn' and self.white_locations[i][1] - self.move_pos[1] == 2 and 'pawn' in self.black_pieces:
                            if (self.move_pos[0] + 1, self.move_pos[1]) in self.black_locations[
                                                                           self.black_pieces.index('pawn'):len(
                                                                               self.black_pieces)]:
                                self.en_passant[0] = True
                                self.en_passant_move = (self.move_pos[0], self.move_pos[1] + 1)
                                self.en_passant_pieces.append(self.black_locations.index((self.move_pos[0] + 1, self.move_pos[1])))
                            if (self.move_pos[0] - 1, self.move_pos[1]) in self.black_locations[
                                                                             self.black_pieces.index('pawn'):len(
                                                                                 self.black_pieces)]:
                                self.en_passant[1] = True
                                self.en_passant_move = (self.move_pos[0], self.move_pos[1] + 1)
                                self.en_passant_pieces.append(self.black_locations.index((self.move_pos[0] - 1, self.move_pos[1])))
                        
                        # Moves piece
                        self.white_locations[i] = self.move_pos
                        
                        # Game Over
                        if not any(self.possible_moves(self.black_pieces, self.black_locations, self.player_turn)):
                            self.game_over()
                    else:
                        # Highlights selected piece with yellow square
                        pygame.draw.rect(self.screen, (240, 230, 140),
                                         pygame.Rect(
                                             self.white_locations[i][0] * self.SQUARE_SIZE + self.board_start[0],
                                             self.white_locations[i][1] * self.SQUARE_SIZE + self.board_start[1],
                                             self.SQUARE_SIZE,
                                             self.SQUARE_SIZE))
                        
                        # Gets valid moves for the selected piece
                        moves_list = self.possible_moves(self.white_pieces, self.white_locations, self.player_turn)
                        self.valid_moves = moves_list[i]
                        
                        # Checks for castling and adds it to valid_moves
                        if piece == 'king':
                            is_castle = self.castle(self.player_turn)
                            if is_castle[0]:
                                self.valid_moves.append((2, 7))
                            if is_castle[1]:
                                self.valid_moves.append((6, 7))
            
            # Draws white pieces
            if piece == 'pawn':
                self.screen.blit(self.white_images[index],
                                      (self.white_locations[i][0] * self.SQUARE_SIZE + self.board_start[0] + 1,
                                       self.white_locations[i][1] * self.SQUARE_SIZE + self.board_start[1]))
            else:
                self.screen.blit(self.white_images[index],
                                      (self.white_locations[i][0] * self.SQUARE_SIZE + self.board_start[0] - 0.5,
                                       self.white_locations[i][1] * self.SQUARE_SIZE + self.board_start[1]))

        # Draws black pieces
        for i in range(len(self.black_pieces)):
            piece = self.black_pieces[i]
            index = self.piece_list.index(piece)
            
            if self.player_turn == 'black' and not self.is_game_over and not self.is_pawn_promotion:
                # Displays BLACK'S TURN
                font = pygame.font.Font('freesansbold.ttf', 30)
                text = font.render("BLACK'S TURN", True, (255,255,255), (0,0,0))
                textRect = text.get_rect()
                textRect.center = (315, 20)
                self.screen.blit(text, textRect)
                
                # Flash king square with red border when in check
                if self.is_king_in_check('black') and self.counter < 15:
                    pygame.draw.rect(self.screen, (240, 0, 0),
                                         pygame.Rect(
                                             self.black_locations[self.black_pieces.index('king')][0] * self.SQUARE_SIZE + self.board_start[0],
                                             self.black_locations[self.black_pieces.index('king')][1] * self.SQUARE_SIZE + self.board_start[1],
                                             self.SQUARE_SIZE,
                                             self.SQUARE_SIZE), 5)
                
                if self.selection == i:
                    if self.is_moved:
                        self.is_moved = False
                        self.player_turn = 'white'
                        self.selection = 100
                        
                        # Taking pieces
                        if self.move_pos in self.white_locations:
                            white_piece_index = self.white_locations.index(self.move_pos)
                            self.captured_pieces_white.append(self.white_pieces[white_piece_index])
                            # Removing piece
                            self.white_locations.remove(self.move_pos)
                            self.white_pieces.pop(white_piece_index)
                        
                        # Castling
                        elif piece == 'king':
                            if self.move_pos == (2, 0):
                                self.black_locations[0] = (3, 0)
                            elif self.move_pos == (6, 0):
                                self.black_locations[self.black_locations.index((7, 0))] = (5, 0)
                            self.is_king_moved[1] = True
                            
                        elif piece == 'pawn':
                            self.en_passant_pieces = []
                            self.en_passant = [False, False]
                            if self.en_passant_move == self.move_pos:
                                self.en_passant = [False, False]
                                white_piece_index = self.white_locations.index((self.move_pos[0], self.move_pos[1] - 1))
                                self.captured_pieces_white.append('pawn')
                                # Removing piece
                                self.white_locations.remove((self.move_pos[0], self.move_pos[1] - 1))
                                self.white_pieces.pop(white_piece_index)
                        
                        # Checks for pawn promotion
                        if self.move_pos[1] == 7 and piece == 'pawn':
                            self.is_pawn_promotion = True
                        
                        # Checks whether white pawns can en passant
                        if piece == 'pawn' and self.move_pos[1] - self.black_locations[i][1] == 2 and 'pawn' in self.white_pieces:
                            if (self.move_pos[0] + 1, self.move_pos[1]) in self.white_locations[
                                                                           self.white_pieces.index('pawn'):len(
                                                                               self.white_pieces)]:
                                self.en_passant[0] = True
                                self.en_passant_move = (self.move_pos[0], self.move_pos[1] - 1)
                                self.en_passant_pieces.append(self.white_locations.index((self.move_pos[0] + 1, self.move_pos[1])))
                            if (self.move_pos[0] - 1, self.move_pos[1]) in self.white_locations[
                                                                             self.white_pieces.index('pawn'):len(
                                                                                 self.white_pieces)]:
                                self.en_passant[1] = True
                                self.en_passant_move = (self.move_pos[0], self.move_pos[1] - 1)
                                self.en_passant_pieces.append(self.white_locations.index((self.move_pos[0] - 1, self.move_pos[1])))
                        self.black_locations[i] = self.move_pos
                        
                        # Game Over
                        if not any(self.possible_moves(self.white_pieces, self.white_locations, self.player_turn)):
                            self.game_over()
                    else:
                        # Highlights selected piece with yellow square
                        pygame.draw.rect(self.screen, (240, 230, 140),
                                         pygame.Rect(self.black_locations[i][0] * self.SQUARE_SIZE + self.board_start[0],
                                                     self.black_locations[i][1] * self.SQUARE_SIZE + self.board_start[1],
                                                     self.SQUARE_SIZE,
                                                     self.SQUARE_SIZE))

                        # Gets valid moves for the selected piece
                        moves_list = self.possible_moves(self.black_pieces, self.black_locations, self.player_turn)
                        self.valid_moves = moves_list[i]
                        
                        # Checks for castling and adds it to valid_moves
                        if piece == 'king':
                            is_castle = self.castle(self.player_turn)
                            if is_castle[0]:
                                self.valid_moves.append((2, 0))
                            if is_castle[1]:
                                self.valid_moves.append((6, 0))
            
            # Draws black pieces
            if piece == 'pawn':
                self.screen.blit(self.black_images[index],
                                      (self.black_locations[i][0] * self.SQUARE_SIZE + self.board_start[0] + 1,
                                       self.black_locations[i][1] * self.SQUARE_SIZE + self.board_start[1]))
            else:
                self.screen.blit(self.black_images[index],
                                      (self.black_locations[i][0] * self.SQUARE_SIZE + self.board_start[0] - 0.5,
                                       self.black_locations[i][1] * self.SQUARE_SIZE + self.board_start[1]))

        # Displays all possible moves for selected piece
        for move in self.valid_moves:
            pygame.draw.circle(self.screen, (120, 120, 120), (
                move[0] * self.SQUARE_SIZE + self.SQUARE_SIZE / 2 + self.board_start[0],
                move[1] * self.SQUARE_SIZE + self.SQUARE_SIZE / 2 + self.board_start[1]), 10)
            
        # Draws captured black pieces
        for i in range(len(self.captured_pieces_black)):
            index = self.piece_list.index(self.captured_pieces_black[i])
            self.screen.blit(self.small_black_images[index], (i * 50, 8 * self.SQUARE_SIZE + self.board_start[1] + 30))

        # Draws captured white pieces
        for i in range(len(self.captured_pieces_white)):
            index = self.piece_list.index(self.captured_pieces_white[i])
            self.screen.blit(self.small_white_images[index], (i * 50, 30))

    def pawn_moves(self, location: Tuple[int, int], turn: str) -> List[Tuple[int, int]]:
        """
        This function is responsible for finding all of a pawn's possible moves
        
        :param Tuple[int, int] location: the co-ordinates of the pawn, where (0, 0) is top left square
        :param str turn: white's or black's turn
        :return List[Tuple[int, int]]: return list of the pawn's possible move locations
        """
        pawn_moves_list = []
        if turn == 'white':
            # Checks whether there is a piece obstruction
            if (location[0], location[1] - 1) not in self.black_locations and (
            location[0], location[1] - 1) not in self.white_locations:
                # Prevents piece from leaving the board
                if location[1] != 0:
                    pawn_moves_list.append((location[0], location[1] - 1))
                # Validates for 2 squares move when it is the pawn's first move
                if location[1] == 6 and ((location[0], location[1] - 2) not in self.black_locations and (
                location[0], location[1] - 2) not in self.white_locations):
                    pawn_moves_list.append((location[0], location[1] - 2))
            # Taking pieces
            if location[0] != 0 and (location[0] - 1, location[1] - 1) in self.black_locations:
                pawn_moves_list.append((location[0] - 1, location[1] - 1))
            if location[0] != 7 and (location[0] + 1, location[1] - 1) in self.black_locations:
                pawn_moves_list.append((location[0] + 1, location[1] - 1))
            # En passant
            if self.white_locations.index(location) in self.en_passant_pieces:
                if self.en_passant[0] and (location[0] - 1, location[1] - 1) == self.en_passant_move:
                    pawn_moves_list.append((location[0] - 1, location[1] - 1))
                elif self.en_passant[1] and (location[0] + 1, location[1] - 1) == self.en_passant_move:
                    pawn_moves_list.append((location[0] + 1, location[1] - 1))
        else:
            # Checks whether there is a piece obstruction
            if ((location[0], location[1] + 1) not in self.white_locations and (
            location[0], location[1] + 1) not in self.black_locations):
                # Prevents piece from leaving the board
                if location[1] != 0:
                    pawn_moves_list.append((location[0], location[1] + 1))
                # Validates for 2 squares move when it is the pawn's first move
                if location[1] == 1 and ((location[0], location[1] + 2) not in self.black_locations and (
                location[0], location[1] + 2) not in self.white_locations):
                    pawn_moves_list.append((location[0], location[1] + 2))
            # Taking pieces
            if location[0] != 7 and (location[0] + 1, location[1] + 1) in self.white_locations:
                pawn_moves_list.append((location[0] + 1, location[1] + 1))
            if location[0] != 0 and (location[0] - 1, location[1] + 1) in self.white_locations:
                pawn_moves_list.append((location[0] - 1, location[1] + 1))
            # En passant
            if self.black_locations.index(location) in self.en_passant_pieces:
                if self.en_passant[0] and (location[0] - 1, location[1] + 1) == self.en_passant_move:
                    pawn_moves_list.append((location[0] - 1, location[1] + 1))
                elif self.en_passant[1] and (location[0] + 1, location[1] + 1) == self.en_passant_move:
                    pawn_moves_list.append((location[0] + 1, location[1] + 1))

        return pawn_moves_list

    def rook_moves(self, location: Tuple[int, int], turn: str) -> List[Tuple[int, int]]:    
        """
        This function is responsible for finding all of a rook's possible moves
        
        :param tuple(int, int) location: the co-ordinates of the rook, where (0, 0) is top left square
        :param str turn: white's or black's turn
        :return list[tuple(str, str)]: return list of the rook's possible move locations
        """
        rook_moves_list = []
        move_location = location
        
        # Finds possbile moves for rook moving towards the h file
        while (move_location == location or (
                move_location not in self.black_locations and move_location not in self.white_locations)) and move_location[
            0] < 7:
            move_location = (move_location[0] + 1, move_location[1])
            if move_location not in self.white_locations and turn == 'white':
                rook_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                rook_moves_list.append(move_location)

        # Finds possbile moves for rook moving towards the a file
        move_location = location
        while (move_location == location or (
                move_location not in self.black_locations and move_location not in self.white_locations)) and move_location[
            0] > 0:
            move_location = (move_location[0] - 1, move_location[1])
            if move_location not in self.white_locations and turn == 'white':
                rook_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                rook_moves_list.append(move_location)

        # Finds possbile moves for rook moving towards the 1st rank
        move_location = location
        while (move_location == location or (
                move_location not in self.black_locations and move_location not in self.white_locations)) and move_location[
            1] < 7:
            move_location = (move_location[0], move_location[1] + 1)
            if move_location not in self.white_locations and turn == 'white':
                rook_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                rook_moves_list.append(move_location)

        # Finds possbile moves for rook moving towards the 8th rank
        move_location = location
        while (move_location == location or (
                move_location not in self.black_locations and move_location not in self.white_locations)) and move_location[
            1] > 0:
            move_location = (move_location[0], move_location[1] - 1)
            if move_location not in self.white_locations and turn == 'white':
                rook_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                rook_moves_list.append(move_location)

        return rook_moves_list

    def bishop_moves(self, location: Tuple[int, int], turn: str) -> List[Tuple[int, int]]:
        """
        This function is responsible for finding all of a bishop's possible moves
        
        :param tuple(int, int) location: the co-ordinates of the bishop, where (0, 0) is top left square
        :param str turn: white's or black's turn
        :return list[tuple(str, str)]: return list of the bishop's possible move locations
        """
        bishop_moves_list = []
        move_location = location
        
        # Finds possbile moves for bishop moving towards the h file and the 1st rank
        while (move_location == location or (
                move_location not in self.black_locations and move_location not in self.white_locations)) and move_location[
            0] < 7 and move_location[1] < 7:
            move_location = (move_location[0] + 1, move_location[1] + 1)
            if move_location not in self.white_locations and turn == 'white':
                bishop_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                bishop_moves_list.append(move_location)

        # Finds possbile moves for bishop moving towards the a file and the 1st rank
        move_location = location
        while (move_location == location or (
                move_location not in self.black_locations and move_location not in self.white_locations)) and move_location[
            0] > 0 and move_location[1] < 7:
            move_location = (move_location[0] - 1, move_location[1] + 1)
            if move_location not in self.white_locations and turn == 'white':
                bishop_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                bishop_moves_list.append(move_location)

        # Finds possbile moves for bishop moving towards the h file and the 8th rank
        move_location = location
        while (move_location == location or (
                move_location not in self.black_locations and move_location not in self.white_locations)) and move_location[
            0] < 7 and move_location[1] > 0:
            move_location = (move_location[0] + 1, move_location[1] - 1)
            if move_location not in self.white_locations and turn == 'white':
                bishop_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                bishop_moves_list.append(move_location)

        # Finds possbile moves for bishop moving towards the a file and the 8th rank
        move_location = location
        while (move_location == location or (
                move_location not in self.black_locations and move_location not in self.white_locations)) and move_location[
            0] > 0 and move_location[1] > 0:
            move_location = (move_location[0] - 1, move_location[1] - 1)
            if move_location not in self.white_locations and turn == 'white':
                bishop_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                bishop_moves_list.append(move_location)

        return bishop_moves_list

    def queen_moves(self, location: Tuple[int, int], turn: str) -> List[Tuple[int, int]]:
        """
        This function is responsible for finding all of a queen's possible moves. As a queen can moves in the
        same way that both a rook and a bishop does, the function uses the rook_moves and bishop_moves functions
        
        :param tuple(int, int) location: the co-ordinates of the queen, where (0, 0) is top left square
        :param str turn: white's or black's turn
        :return list[tuple(str, str)]: return list of the queen's possible move locations
        """
        queen_moves_list = []
        if self.rook_moves(location, turn):
            queen_moves_list.extend(self.rook_moves(location, turn))
        if self.bishop_moves(location, turn):
            queen_moves_list.extend(self.bishop_moves(location, turn))
        return queen_moves_list

    def king_moves(self, location: Tuple[int, int], turn: str) -> List[Tuple[int, int]]:
        """
        This function is responsible for finding all of a king's possible moves
        
        :param tuple(int, int) location: the co-ordinates of the king, where (0, 0) is top left square
        :param str turn: white's or black's turn
        :return list[tuple(str, str)]: return list of the king's possible move locations
        """
        king_moves_list = []

        # Finds possbile moves for king moving towards the h file
        move_location = location
        if move_location[0] < 7:
            move_location = (move_location[0] + 1, move_location[1])
            if move_location not in self.white_locations and turn == 'white':
                king_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                king_moves_list.append(move_location)

        # Finds possbile moves for king moving towards the a file
        move_location = location
        if move_location[0] > 0:
            move_location = (move_location[0] - 1, move_location[1])
            if move_location not in self.white_locations and turn == 'white':
                king_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                king_moves_list.append(move_location)

        # Finds possbile moves for king moving towards the 1st rank
        move_location = location
        if move_location[1] < 7:
            move_location = (move_location[0], move_location[1] + 1)
            if move_location not in self.white_locations and turn == 'white':
                king_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                king_moves_list.append(move_location)

        # Finds possbile moves for king moving towards the 8th rank
        move_location = location
        if move_location[1] > 0:
            move_location = (move_location[0], move_location[1] - 1)
            if move_location not in self.white_locations and turn == 'white':
                king_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                king_moves_list.append(move_location)

        # Finds possbile moves for king moving towards the h file and the 1st rank
        move_location = location
        if move_location[0] < 7 and move_location[1] < 7:
            move_location = (move_location[0] + 1, move_location[1] + 1)
            if move_location not in self.white_locations and turn == 'white':
                king_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                king_moves_list.append(move_location)

        # Finds possbile moves for king moving towards the a file and the 1st rank
        move_location = location
        if move_location[0] > 0 and move_location[1] < 7:
            move_location = (move_location[0] - 1, move_location[1] + 1)
            if move_location not in self.white_locations and turn == 'white':
                king_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                king_moves_list.append(move_location)

        # Finds possbile moves for king moving towards the h file and the 8th rank
        move_location = location
        if move_location[0] < 7 and move_location[1] > 0:
            move_location = (move_location[0] + 1, move_location[1] - 1)
            if move_location not in self.white_locations and turn == 'white':
                king_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                king_moves_list.append(move_location)

        # Finds possbile moves for king moving towards the a file and the 8th rank
        move_location = location
        if move_location[0] > 0 and move_location[1] > 0:
            move_location = (move_location[0] - 1, move_location[1] - 1)
            if move_location not in self.white_locations and turn == 'white':
                king_moves_list.append(move_location)
            elif move_location not in self.black_locations and turn == 'black':
                king_moves_list.append(move_location)

        return king_moves_list

    def knight_moves(self, location: Tuple[int, int], turn: str) -> List[Tuple[int, int]]:
        """
        This function is responsible for finding all of a knight's possible moves
        
        :param tuple(int, int) location: The co-ordinates of the knight, where (0, 0) is top left square
        :param str turn: white's or black's turn
        :return list[tuple(str, str)]: return list of the knight's possible move locations
        """
        knight_moves_list = []
        move_location = location

        # Finds possbile moves for knight moving 1 square towards the h file
        if move_location[0] < 7:
            move_location = (move_location[0] + 1, move_location[1])
            if move_location[1] <= 5:
                if ((move_location[0], move_location[1] + 2) not in self.white_locations and turn == 'white') or ((move_location[0], move_location[1] + 2) not in self.black_locations and turn == 'black'):
                    knight_moves_list.append((move_location[0], move_location[1] + 2))
            if move_location[1] >= 2:
                if ((move_location[0], move_location[1] - 2) not in self.white_locations and turn == 'white') or ((move_location[0], move_location[1] - 2) not in self.black_locations and turn == 'black'):
                    knight_moves_list.append((move_location[0], move_location[1] - 2))

        # Finds possbile moves for knight moving 1 square towards the a file
        move_location = location
        if move_location[0] > 0:
            move_location = (move_location[0] - 1, move_location[1])
            if move_location[1] <= 5:
                if ((move_location[0], move_location[1] + 2) not in self.white_locations and turn == 'white') or ((move_location[0], move_location[1] + 2) not in self.black_locations and turn == 'black'):
                    knight_moves_list.append((move_location[0], move_location[1] + 2))
            if move_location[1] >= 2:
                if ((move_location[0], move_location[1] - 2) not in self.white_locations and turn == 'white') or ((move_location[0], move_location[1] - 2) not in self.black_locations and turn == 'black'):
                    knight_moves_list.append((move_location[0], move_location[1] - 2))

        # Finds possbile moves for knight moving 1 square towards the 1st rank
        move_location = location
        if move_location[1] < 7:
            move_location = (move_location[0], move_location[1] + 1)
            if move_location[0] <= 5:
                if ((move_location[0] + 2, move_location[1]) not in self.white_locations and turn == 'white') or ((move_location[0] + 2, move_location[1]) not in self.black_locations and turn == 'black'):
                    knight_moves_list.append((move_location[0] + 2, move_location[1]))
            if move_location[0] >= 2:
                if ((move_location[0] - 2, move_location[1]) not in self.white_locations and turn == 'white') or ((move_location[0] - 2, move_location[1]) not in self.black_locations and turn == 'black'):
                    knight_moves_list.append((move_location[0] - 2, move_location[1]))

        # Finds possbile moves for knight moving 1 square towards the 8th rank
        move_location = location
        if move_location[1] > 0:
            move_location = (move_location[0], move_location[1] - 1)
            if move_location[0] <= 5:
                if ((move_location[0] + 2, move_location[1]) not in self.white_locations and turn == 'white') or ((move_location[0] + 2, move_location[1]) not in self.black_locations and turn == 'black'):
                    knight_moves_list.append((move_location[0] + 2, move_location[1]))
            if move_location[0] >= 2:
                if ((move_location[0] - 2, move_location[1]) not in self.white_locations and turn == 'white') or ((move_location[0] - 2, move_location[1]) not in self.black_locations and turn == 'black'):
                    knight_moves_list.append((move_location[0] - 2, move_location[1]))

        return knight_moves_list

    def is_king_in_check(self, turn: str) -> bool:
        """
        This function is responsible for determining whether the player's king is in check
        
        :param str turn: white's or black's turn
        """
        if turn == 'black':
            all_moves_list = self.all_possible_moves(self.white_pieces, self.white_locations, 'white')
            king_pos = self.black_locations[self.black_pieces.index('king')]
        else:
            all_moves_list = self.all_possible_moves(self.black_pieces, self.black_locations, 'black')
            king_pos = self.white_locations[self.white_pieces.index('king')]

        return any(king_pos in piece_moves for piece_moves in all_moves_list)

    def castle(self, turn: str) -> List[bool]:
        """
        This function is responsible for finding all of a king's possible moves
        
        :param str turn: white's or black's turn
        :return List[bool]: Returns a list where index 0 is a boolean for whether short side castling is possible,
        and index 1 is for whether long side castling is possible
        """
        is_castle_list = [False, False]
        short_side_castle = True
        long_side_castle = True
        if turn == 'white':
            all_moves_list = self.all_possible_moves(self.black_pieces, self.black_locations, 'black')
            # Checks if opponent's pieces prevent castling
            for piece_moves in all_moves_list:
                if (5, 7) in piece_moves or (6, 7) in piece_moves:
                    short_side_castle = False
                if (2, 7) in piece_moves or (3, 7) in piece_moves:
                    long_side_castle = False
            # Checks if player's king and rooks have moved
            if not self.is_king_moved[0]:
                if not self.is_rook_moved[0][0] and (5, 7) not in self.white_locations and (6, 7) not in self.white_locations and (
                5, 7) not in self.black_locations and (6, 7) not in self.black_locations and short_side_castle:
                    is_castle_list[1] = True
                if not self.is_rook_moved[0][1] and (1, 7) not in self.white_locations and (2, 7) not in self.white_locations and (
                3, 7) not in self.white_locations and (1, 7) not in self.black_locations and (2, 7) not in self.black_locations and (
                3, 7) not in self.black_locations and long_side_castle:
                    is_castle_list[0] = True
        else:
            all_moves_list = self.all_possible_moves(self.white_pieces, self.white_locations, 'white')
            # Checks if opponent's pieces prevent castling
            for piece_moves in all_moves_list:
                if (5, 0) in piece_moves or (6, 0) in piece_moves:
                    short_side_castle = False
                if (2, 0) in piece_moves or (3, 0) in piece_moves:
                    long_side_castle = False
            # Checks if player's king and rooks have moved
            if not self.is_king_moved[1]:
                if not self.is_rook_moved[1][0] and (5, 0) not in self.black_locations and (6, 0) not in self.black_locations and (
                5, 0) not in self.white_locations and (6, 0) not in self.white_locations and short_side_castle:
                    is_castle_list[1] = True
                if not self.is_rook_moved[1][1] and (1, 0) not in self.black_locations and (2, 0) not in self.black_locations and (
                3, 0) not in self.black_locations and (1, 0) not in self.white_locations and (2, 0) not in self.white_locations and (
                3, 0) not in self.white_locations and long_side_castle:
                    is_castle_list[0] = True

        return is_castle_list

    def all_possible_moves(self, pieces: List[str], locations: List[Tuple[int, int]], turn: str) -> List[List[Tuple[int, int]]]:
        """
        This function is responsible for combining the lists of the possible moves of all the player's existing pieces
        
        :param List[str] pieces: a list of the player's existing pieces on the board
        :param List[Tuple[int, int]] locations: a list of the locations of the existing pieces
        :param str turn: white's or black's turn
        :return List[List[Tuple[int, int]]]: a list of the lists of each piece's possible moves
        """
        all_moves_list = []
        moves_list = []

        for i in range(len(pieces)):
            piece = pieces[i]
            location = locations[i]
            if piece == 'pawn':
                moves_list = self.pawn_moves(location, turn)
            elif piece == 'rook':
                moves_list = self.rook_moves(location, turn)
            elif piece == 'bishop':
                moves_list = self.bishop_moves(location, turn)
            elif piece == 'queen':
                moves_list = self.queen_moves(location, turn)
            elif piece == 'king':
                moves_list = self.king_moves(location, turn)
            elif piece == 'knight':
                moves_list = self.knight_moves(location, turn)

            all_moves_list.append(moves_list)

        return all_moves_list

    def possible_moves(self, pieces: List[str], locations: List[Tuple[int, int]], turn: str) -> List[List[Tuple[int, int]]]:
        """
        This function is responsible for removing moves from the list of valid moves that cause the player's king to be in check
        
        :param List[str] pieces: a list of the player's existing pieces on the board
        :param List[Tuple[int, int]] locations: a list of the locations of the existing pieces
        :param str turn: white's or black's turn
        :return List[List[Tuple[int, int]]]: a list of the lists of each piece's possible moves
        """
        old_pos = ()
        piece = ''
        index = 0
        take = False
        piece_moves_list = []
        moves_list = []
        move_lists = self.all_possible_moves(pieces, locations, turn)
        # Validates that the moves do not cause the king to be in check and removes moves that do so
        for i in range(len(move_lists)):
            piece_moves_list = []
            for move in move_lists[i]:
                if turn == 'white':
                    old_pos = self.white_locations[i]
                    self.white_locations[i] = move
                    if move in self.black_locations:
                        index = self.black_locations.index(move)
                        self.black_locations.pop(index)
                        piece = self.black_pieces[index]
                        self.black_pieces.pop(index)
                        take = True
                    if not self.is_king_in_check(turn):
                        piece_moves_list.append(move)
                    self.white_locations[i] = old_pos
                    if take:
                        self.black_locations.insert(index, move)
                        self.black_pieces.insert(index, piece)
                        take = False
                elif turn == 'black':
                    old_pos = self.black_locations[i]
                    self.black_locations[i] = move
                    if move in self.white_locations:
                        index = self.white_locations.index(move)
                        self.white_locations.pop(index)
                        piece = self.white_pieces[index]
                        self.white_pieces.pop(index)
                        take = True
                    if not self.is_king_in_check(turn):
                        piece_moves_list.append(move)
                    self.black_locations[i] = old_pos
                    if take:
                        self.white_locations.insert(index, move)
                        self.white_pieces.insert(index, piece)
                        take = False
            moves_list.append(piece_moves_list)

        return moves_list

    def pawn_promotion(self, click_pos: Tuple[int, int], turn: str):
        """
        This function is responsible for displaying the possible pieces to promote to and the functioning of the promotion
        
        :param Tuple[int, int] click_pos: position of where mouse clicked
        :param str turn: white's or black's turn
        """
        # Displays message
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render('Pick a piece for promotion', True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()

        # Displays options for promotion
        for i in range(len(self.piece_list)):
            if self.piece_list[i] not in ['king', 'pawn']:
                if turn == 'white':
                    textRect.center = (725, 400)
                    self.screen.blit(text, textRect)
                    rect = pygame.Rect(543 + i * 75, 415, 60, 60)
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)
                    self.screen.blit(self.black_images[i], (540 + i * 75, 410))
                    # Changes piece depending on player selection
                    if rect.collidepoint(click_pos):
                        self.black_pieces[self.black_locations.index(self.move_pos)] = self.piece_list[i]
                        self.is_pawn_promotion = False
                        break
                elif turn == 'black':
                    textRect.center = (725, 400)
                    self.screen.blit(text, textRect)
                    rect = pygame.Rect(543 + i * 75, 415, 60, 60)
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)
                    self.screen.blit(self.white_images[i], (540 + i * 75, 410))
                    # Changes piece depending on player selection
                    if rect.collidepoint(click_pos):
                        self.white_pieces[self.white_locations.index(self.move_pos)] = self.piece_list[i]
                        self.is_pawn_promotion = False
                        break

    def game_over(self):
        """
        This function is responsible for displaying the winner of the game or stalemate and the functioning of the New Game button
        """
        self.is_game_over = True
        rect = pygame.Rect(600, 200, 350, 200)
        pygame.draw.rect(self.screen, (220,220,220), rect, 0, 5)
        font = pygame.font.Font('freesansbold.ttf', 25)
        message = ''
        # Determines either stalemate or winner and checkmate
        if self.is_king_in_check(self.player_turn):
            if self.player_turn == 'black':
                winner = 'White'
            elif self.player_turn == 'white':
                winner = 'Black'
            message = f'{winner} has won the game!'
            checkmate = font.render('Checkmate!', True, (0,0,0), (220,220,220))    
            mateRect = checkmate.get_rect()
            mateRect.center = (775, 275)
            self.screen.blit(checkmate, mateRect)    
        else:
            message = 'Stalemate'
        # Displays message
        text = font.render(message, True, (0,0,0), (220,220,220))
        textRect = text.get_rect()
        textRect.center = (775, 225)
        self.screen.blit(text, textRect)
        # Displays New Game button
        buttonRect = pygame.Rect(0, 0, 150, 75)
        buttonRect.center = (775, 350)
        pygame.draw.rect(self.screen, (190,190,190), buttonRect, 0, 5)
        textButton = font.render('New game', True, (0,0,0), (190,190,190))
        Rect = textButton.get_rect()
        Rect.center = (775, 350)
        self.screen.blit(textButton, Rect)
        # Starts new game when New Game button clicked
        if buttonRect.collidepoint(self.click_pos):
            self.reset()

    def reset(self): 
        """
        This function is responsible for reseting every variable to their original value at the start of the game
        """
        self.initialize_game()

    def handle_events(self):
        """
        This function is responsible for tracking the events that occur on the pygame screen
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click_pos = event.pos
                x = (event.pos[0] - self.board_start[0]) // self.SQUARE_SIZE
                y = (event.pos[1] - self.board_start[1]) // self.SQUARE_SIZE
                click_co_ordinate = (x, y)
                # Checks whether the clicked place requires a reaction from the program
                if click_co_ordinate in self.valid_moves:
                    self.is_moved = True
                    self.move_pos = click_co_ordinate
                    self.valid_moves = []
                elif self.player_turn == 'white':
                    if click_co_ordinate in self.white_locations:
                        self.selection = self.white_locations.index(click_co_ordinate)
                elif self.player_turn == 'black':
                    if click_co_ordinate in self.black_locations:
                        self.selection = self.black_locations.index(click_co_ordinate)

    def play(self):
        """
        Runs the game on the pygame screen
        """
        while self.running:
            self.counter = (self.counter + 1) % 25
            self.timer.tick(self.fps)
            pygame.display.set_caption(self.CAPTION)
            self.screen.fill((50, 50, 50))

            # Check and does game over
            if self.is_game_over:
                self.game_over()
            # Check and does pawn promotion
            elif self.is_pawn_promotion:
                self.pawn_promotion(self.click_pos, self.player_turn)
            # Draws chess board
            self.draw_board()
            # Draws all pieces
            self.draw_pieces()
            # Handles the entire game
            self.handle_events()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.play()

