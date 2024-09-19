import math
import time

class Board:
    """Used to edit the board, get legal moves, and other associated proccessess.
    Terms:
    Notation: A string used to represent a square in chess
    Index: Typically used to represent the acutal location of a square's information"""
    import random, math
    def __init__(self):
        self.board = [["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"],
                 ["Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn"],
                 [None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None],
                 ["Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn"],
                 ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]]
        self.board_color = [["white", "white", "white", "white", "white", "white", "white", "white"],
                       ["white", "white", "white", "white", "white", "white", "white", "white"],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       ["black", "black", "black", "black", "black", "black", "black", "black"],
                       ["black", "black", "black", "black", "black", "black", "black", "black"]]
        self.board_notation = [["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"],
                          ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
                          ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
                          ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
                          ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
                          ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
                          ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
                          ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]]
        self.player_moves = []
        self.white_oo = True
        self.white_ooo = True
        self.black_oo = True
        self.black_ooo = True


    def set_position_via_fen(self, fen):
        pass
    
    
    def get_notation_via_index(self, index):
        """Returns the notation based off an index"""
        return self.board_notation[index[0]][index[1]]


    def if_contains(self, item, search):
        """Returns True if a list contains a value, otherwise returns False."""
        for i in range(len(search)):
            try:
                item.index(search[i])
                return True
            except:
                pass
        return False
    
    
    def get_index_via_notation(self, notation):
        """Returns the index based off a notation."""
        return (int(notation[1]) - 1, self.board_notation[int(notation[1]) - 1].index(notation))


    def get_square_value(self, notation):
        "Returns the value of a square based off a notation. The data will be returned in a tuple consisting of 1st: the piece on that square, and 2nd: the piece's color."
        return (self.board[self.get_index_via_notation(notation)[0]][self.get_index_via_notation(notation)[1]],
                self.board_color[self.get_index_via_notation(notation)[0]][self.get_index_via_notation(notation)[1]])


    def if_white_can_enpessant_this_move(self):
        """Returns True if there is a black pawn that has advanced two squares, otherwise returns False"""
        if len(self.player_moves) == 0:
            return None
        last_moved_piece = self.board[self.get_index_via_notation(self.player_moves[-1][2:4])[0]][self.get_index_via_notation(self.player_moves[-1][2:4])[1]]
        if last_moved_piece == "Pawn" and self.player_moves[-1][1] == "7" and self.player_moves[-1][3] == "5":
            return True
        else:
            return False


    def if_black_can_enpessant_this_move(self):
        """Returns True if there is a white pawn that has advanced two squares, otherwise returns False."""
        if len(self.player_moves) == 0:
            return None
        if self.board[self.get_index_via_notation(self.player_moves[-1][2:4])[0]][self.get_index_via_notation(self.player_moves[-1][2:4])[1]] == "Pawn" and self.player_moves[-1][1] == "2" and self.player_moves[-1][3] == "4":
            return True
        else:
            return False

    
    def clear_square(self, notation):
        """Removes all data from a square based off notation."""
        if type(notation) == str:
            notation = [notation]
        for i in range(len(notation)):
            index = self.get_index_via_notation(notation[i])
            self.board[index[0]][index[1]] = None
            self.board_color[index[0]][index[1]] = None


    def move(self, move):
        """Performs ANY move (Copys the contents of one square to another, and clears the first squares data), also updates castling rights if a rook or king has moved."""
        # Defining variables
        index1 = self.get_index_via_notation(move[0:2])
        index2 = self.get_index_via_notation(move[2:4])
        piece_values = self.get_square_value(move[0:2])
        # Checking if the piece is a Rook
        if piece_values[0] == "Rook":
            # Changing the castling values based off the rook (Checks if it's in a corner (Where rooks start off) and if so, changes if the color that side belongs to can castle on that side)
            if index1 == (0, 0):
                self.white_oo = False
            elif index1 == (7, 0):
                self.black_oo = False
            elif index1 == (7, 0):
                self.white_ooo = False
            elif index1 == (7, 7):
                self.black_ooo = False
        # Checking if the piece is a king
        if piece_values[0] == "King":
            # Changes one sides castling rights to all be false
            if piece_values[1] == "White":
                # Removes White's castling rights
                self.white_oo = False
                self.white_ooo = False
            else:
                # Removes Black's castling rights
                self.black_oo = False
                self.black_ooo = False
        # Changes the values of the board to align with the move
        self.board[index2[0]][index2[1]] = self.board[index1[0]][index1[1]]
        self.board_color[index2[0]][index2[1]] = self.board_color[index1[0]][index1[1]]
        self.clear_square(move[0:2])
        self.player_moves.append(move)
    
    
    def get_seeing_as_bishop_at(self, notation):
        """Returns all squares that a bishop would see (all squares it can move to, plus any that it protects) at the passed in square (notation)."""
        # Defining variables
        index = self.get_index_via_notation(notation)
        moves = []
        # checks the diagonals from the bishop to the edges in each direction until there is a piece:
        # negative, negative:
        spot = (index[0] - 1, index[1] - 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if self.board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] - 1, spot[1] - 1)
            else:
                moves.append(spot)
                break
        # negative, positive
        spot = (index[0] - 1, index[1] + 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if self.board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] - 1, spot[1] + 1)
            else:
                moves.append(spot)
                break
        # positive, positive
        spot = (index[0] + 1, index[1] + 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if self.board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] + 1, spot[1] + 1)
            else:
                moves.append(spot)
                break
        # positive, negative
        spot = (index[0] + 1, index[1] - 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if self.board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] + 1, spot[1] - 1)
            else:
                moves.append(spot)
                break
        # Checking if any squares are "illegal"
        i2 = 0
        for i in range(len(moves)):
            if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7:
                del moves[i2]
                i2 -= 1
            i2 += 1
        for i in range(len(moves)):
            moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def errorless_index(self, list_0, index_0):
        """Performs the same action as '.index', but instead of returning an error if an item is not found, it will instead return none."""
        try:
            return list_0.index(index_0)
        except:
            return None
    
    
    def get_seeing_as_pawn_at(self, notation):
        """Returns all squares a pawn can see (any square it protects)."""
        # Defining variables
        index = self.get_index_via_notation(notation)
        piece_color = self.get_square_value(notation)[1]
        moves = []
        if piece_color == "white":
            # Adding moves for taking
            moves.append((index[0] + 1, index[1] + 1))
            moves.append((index[0] + 1, index[1] - 1))
        else:
            # Adding moves for taking
            moves.append((index[0] - 1, index[1] + 1))
            moves.append((index[0] - 1, index[1] - 1))
        # Checking if any squares are "illegal"
        i2 = 0
        for i in range(len(moves)):
            if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7:
                del moves[i2]
                i2 -= 1
            i2 += 1
        for i in range(len(moves)):
            moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def get_legal_as_pawn_at(self, notation):
        """Returns all possible legal moves a pawn could make from a square (the passed in notation)."""
        # Defining variables
        index = self.get_index_via_notation(notation)
        piece_color = self.get_square_value(notation)[1]
        moves = []
        if piece_color == "white":
            # Checking moves if the pawn is white
            try:
                # Checking if the pawn can move one square forward
                if self.board[index[0] + 1][index[1]] == None:
                    moves.append((index[0] + 1, index[1]))
                    # Checking if the pawn can move two square forward (if it could move one forward first)
                    if index[0] == 1 and self.board[index[0] + 2][index[1]] == None:
                        moves.append((index[0] + 2, index[1]))
            except:
                pass
            try:
                # Checking for Enpessant
                if self.if_white_can_enpessant_this_move():
                    pawn_location = self.get_index_via_notation(self.player_moves[-1][2:4])
                    if index[1] - 1 == pawn_location[1] or index[1] + 1 == pawn_location[1]:
                        moves.append((pawn_location[0] + 1, pawn_location[1]))
            except IndexError:
                pass
            # Checking if the pawn can take
            if self.board_color[index[0] + 1][index[1] + 1] == "black":
                moves.append((index[0] + 1, index[1] + 1))
            if self.board_color[index[0] + 1][index[1] - 1] == "black":
                moves.append((index[0] + 1, index[1] - 1))
        else:
            # Checking moves if the pawn is black
            try:
                # Checking if the pawn can move one square forward
                if self.board[index[0] - 1][index[1]] == None:
                    moves.append((index[0] - 1, index[1]))
                    # Checking if the pawn can move two square forward (if it could move one forward first)
                    if index[0] == 6 and self.board[index[0] - 2][index[1]] == None:
                        moves.append((index[0] - 2, index[1]))
            except:
                pass
            # Checking for Enpessant
            if self.if_black_can_enpessant_this_move():
                pawn_location = self.get_index_via_notation(self.player_moves[-1][2:4])
                if index[1] - 1 == pawn_location[1] or index[1] + 1 == pawn_location[1]:
                    moves.append((pawn_location[0] - 1, pawn_location[1]))
            # Checking if the pawn can take
            if self.board_color[index[0] - 1][index[1] + 1] == "white":
                moves.append((index[0] - 1, index[1] + 1))
            if self.board_color[index[0] - 1][index[1] - 1] == "white":
                moves.append((index[0] - 1, index[1] - 1))
        # Checking if any squares are "illegal"
        i2 = 0
        for i in range(len(moves)):
            if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7:
                del moves[i2]
                i2 -= 1
            i2 += 1
        for i in range(len(moves)):
            moves[i] = self.get_notation_via_index(moves[i])
        return moves
    
    
    def get_seeing_as_knight_at(self, notation):
        """Returns all legal squares a knight could move to from a certain square (The passed in notation)."""
        # Defining variables
        index = self.get_index_via_notation(notation)
        moves = []
        moves.append((index[0] - 1, index[1] - 2))
        moves.append((index[0] - 1, index[1] + 2))
        moves.append((index[0] - 2, index[1] - 1))
        moves.append((index[0] + 2, index[1] - 1))
        moves.append((index[0] - 2, index[1] + 1))
        moves.append((index[0] + 2, index[1] + 1))
        moves.append((index[0] - 1, index[1] + 2))
        moves.append((index[0] + 1, index[1] + 2))
        # Checking if any squares are "illegal"
        i2 = 0
        for i in range(len(moves)):
            if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7:
                del moves[i2]
                i2 -= 1
            i2 += 1
        for i in range(len(moves)):
            moves[i] = self.get_notation_via_index(moves[i])
        return moves
    def get_seeing_as_king(self, notation):
        """Returns all squares a king protects from a certain square (the passed in notation)."""
        # Defining variables
        moves = []
        index = self.get_index_via_notation(notation)
        # Adds every possible direction of squares next to the king
        moves.append((index[0] - 1, index[1] - 1))
        moves.append((index[0] - 1, index[1] + 1))
        moves.append((index[0] + 1, index[1] + 1))
        moves.append((index[0] + 1, index[1] - 1))
        moves.append((index[0], index[1] + 1))
        moves.append((index[0], index[1] - 1))
        moves.append((index[0] - 1, index[1]))
        moves.append((index[0] + 1, index[1]))
        i2 = 0
        for i in range(len(moves)):
            if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7:
                del moves[i2]
                i2 -= 1
            i2 += 1
        for i in range(len(moves)):
            moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def get_legal_as_king(self, notation):
        """Returns all possible legal moves as a king from a certain square (the passed in notation)."""
        # Getting all "typical" (moving to all adjacent squares) king moves
        moves = [*self.get_seeing_as_king(notation)]
        # Castling
        # Checking the color of the king
        if self.get_square_value(notation)[1] == "white":
            # Castling for white
            if self.white_oo and self.get_pieces_seeing("f1") == [] and self.get_piece_seeing("g1") == []:
                moves.append("o-o")
            if self.white_oo and self.get_pieces_seeing("b1") == [] and self.get_piece_seeing("c1") == [] and self.get_piece_seeing("d1"):
                moves.append("o-o-o")
        else:
            # Castling for black
            if self.black_oo and self.get_pieces_seeing("f8") == [] and self.get_piece_seeing("g8") == []:
                moves.append("o-o")
            if self.black_oo and self.get_pieces_seeing("b8") == [] and self.get_piece_seeing("c8") == [] and self.get_piece_seeing("d8"):
                moves.append("o-o-o")
    
    
    def get_piece_seeing(self, notation):
        """Checks the value of square (gotten from notation), then gets what that piece sees (via checking the value of the square, then running that piece's respective function to get what it sees)."""
        index = self.get_index_via_notation(notation)
        piece = self.get_square_value(notation)[0]
        piece_color = self.board_color[index[0]][index[1]]
        moves = []
        if piece == "Knight":
            moves = [*moves, *self.get_seeing_as_knight_at(notation)]
        if piece == "King":
            moves = [*moves, *self.get_seeing_as_king_at(notation)]
        elif piece == "Rook":
            moves = [*moves, *self.get_seeing_as_rook_at(notation)]
        elif piece == "Bishop":
            moves = [*moves, *self.get_seeing_as_bishop_at(notation)]
        elif piece == "Queen":
            moves = [*moves, *self.get_seeing_as_bishop_at(notation)]
            moves = [*moves, *self.get_seeing_as_rook_at(notation)]
        elif piece == "Pawn":
            moves = [*moves, *self.get_seeing_as_pawn_at(notation)]
        # Checking if any squares are illegal
        for i in range(len(moves)):
            moves[i] = self.get_index_via_notation(moves[i])
        i2 = 0
        for i in range(len(moves)):
            if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7:
                del moves[i2]
                i2 -= 1
            i2 += 1
        return moves


    def get_pieces_seeing(self, notation):
        """Returns the squares off all pieces seeing a certain square (the square in question is gotten from notation)"""
        pieces_locations = []
        for i in range(64):
            if self.board[math.floor(i / 8)][i % 8] != None:
                try:
                    pieces_locations.append(self.get_piece_seeing(self.get_notation_via_index((math.floor(i / 8), i % 8))))
                except:
                    pass
        return pieces_locations


    def get_legal_moves(self, notation):
        """Returns all legal moves of a piece on a specific square (gotten via notation) (The moves are obtained by either getting what squares a piece sees, then vetting all the moves to remove the squares it cannot move to. Or uses the respective function to calculate that piece's legal moves)."""
        piece = self.get_square_value(notation)[0]
        if piece == "Pawn":
            moves = [*self.get_legal_as_pawn_at(notation)]
        elif piece == "King":
            moves = [*self.get_legal_as_king(notation)]
        else:
            moves = [*self.get_piece_seeing(notation)]
        # Changes all squares to indexs
        for i in range(len(moves)):
            moves[i] = self.get_index_via_notation(moves[i])
        # Checking if any squares are "illegal"
        i2 = 0
        for i in range(len(moves)):
            if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7 or self.get_square_value(notation)[1] == self.board_color[moves[i][0]][moves[i][1]]:
                del moves[i2]
                i2 -= 1
            i2 += 1
        for i in range(len(moves)):
            moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def who_to_move(self):
        """Returns a string containing either 'white' or 'black' based off which player's turn it is to move."""
        if len(self.player_moves) == 0:
            return "white"
        return self.get_square_value(self.player_moves[-1][2:4])


    def legal_move(self, move):
        """Checks if the move passed in is legal, if so then the move is performed and the function returns True, if it failed one of the checks, the function will return False."""
        if self.errorless_index(self.get_legal_moves(move[0:2]), move[2:4]) != None and self.get_square_value(move[0:2])[1] == self.who_to_move():
            self.move(move)
            return True
        return False
class Display:
    import pygame, math
    def __init__(self, square_one_color = (160, 82, 45), square_two_color = (255, 255, 255), screen_size = (700, 700), background = (0, 0, 0), if_view_from_whites_perspective = True):
        import pygame
        self.view_from_whites_perspective = if_view_from_whites_perspective
        self.square_one_color = square_one_color
        self.square_two_color = square_two_color
        self.screen_size = screen_size
        self.background = background
        self.frame = 0
        self.drawn_background_squares = []
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode(screen_size)
        if self.screen_size[0] == screen_size[1]:
            self.square_spacing_size = (screen_size[0] / 9) / 7
            self.board_offset_x = self.square_spacing_size
            self.board_offset_y = self.square_spacing_size
            self.square_edge_size = (screen_size[0] / 9) - ((self.square_spacing_size * 2)) / 8
        elif self.screen_size[0] > self.screen_size[1]:
            self.square_spacing_size = (screen_size[1] / 9) / 7
            self.board_offset_x = self.square_spacing_size - (self.screen_size[1] - self.screen_size[0]) / 2
            self.board_offset_y = self.square_spacing_size
            self.square_edge_size = (screen_size[1] / 9) - ((self.square_spacing_size * 2)) / 8
        else:
            self.square_spacing_size = (screen_size[0] / 9) / 7
            self.board_offset_x = self.square_spacing_size
            self.board_offset_y = self.square_spacing_size - (self.screen_size[0] - self.screen_size[1]) / 2
            self.square_edge_size = (screen_size[0] / 9) - ((self.square_spacing_size * 2)) / 8
        pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkPawn.png"), (self.square_edge_size, self.square_edge_size))
        self.piece_locations = {"black Pawn": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkPawn.png"), (self.square_edge_size, self.square_edge_size)),
                                "black Bishop": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkBishop.png"), (self.square_edge_size, self.square_edge_size)),
                                "black Knight": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkKnight.png"), (self.square_edge_size, self.square_edge_size)),
                                "black Rook": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkRook.png"), (self.square_edge_size, self.square_edge_size)),
                                "black King": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkKing.png"), (self.square_edge_size, self.square_edge_size)),
                                "black Queen": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkQueen.png"), (self.square_edge_size, self.square_edge_size)),
                                "white Pawn": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightPawn.png"), (self.square_edge_size, self.square_edge_size)),
                                "white Knight": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightKnight.png"), (self.square_edge_size, self.square_edge_size)),
                                "white Bishop": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightBishop.png"), (self.square_edge_size, self.square_edge_size)),
                                "white Rook": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightRook.png"), (self.square_edge_size, self.square_edge_size)),
                                "white King": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightKing.png"), (self.square_edge_size, self.square_edge_size)),
                                "white Queen": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightQueen.png"), (self.square_edge_size, self.square_edge_size))}
    def draw_background(self, background = "Nothing entered"):
        import pygame
        if background == "Nothing entered":
            background = self.background
        pygame.draw.rect(self.screen, background, pygame.Rect(0, 0, self.screen_size[0], self.screen_size[1]))
    def setup_background_squares(self):
        import pygame
        color_alternation = 0
        for i in range(64):
            if i % 8 == 0:
                color_alternation = (color_alternation + 1) % 2
            color_alternation = (color_alternation + 1) % 2
            if color_alternation == 0:
                self.drawn_background_squares.append(pygame.draw.rect(self.screen, self.square_one_color, pygame.Rect(((i % 8) * (self.square_spacing_size + self.square_edge_size)) + self.board_offset_x, (math.floor(i / 8) * (self.square_spacing_size + self.square_edge_size)) + self.board_offset_y, self.square_edge_size, self.square_edge_size)))
            else:
                self.drawn_background_squares.append(pygame.draw.rect(self.screen, self.square_two_color, pygame.Rect(((i % 8) * (self.square_spacing_size + self.square_edge_size)) + self.board_offset_x, (math.floor(i / 8) * (self.square_spacing_size + self.square_edge_size)) + self.board_offset_y, self.square_edge_size, self.square_edge_size)))
    def draw_pieces(self, board_class, whites_point_of_view = True):
        import pygame
        if whites_point_of_view:
            board_class.board_color.reverse()
            board_class.board.reverse()
        for i in range(8):
            for n in range(8):
                try:
                    self.screen.blit(self.piece_locations.get(board_class.board_color[i][n] + " " + board_class.board[i][n]), ((n * (self.square_edge_size + self.square_spacing_size)) + self.board_offset_x, (i * (self.square_edge_size + self.square_spacing_size)) + self.board_offset_y))
                except:
                    pass
        if whites_point_of_view:
            board_class.board_color.reverse()
            board_class.board.reverse()
    def update_screen(self, board):
        import pygame
        self.draw_background()
        self.setup_background_squares()
        self.draw_pieces(board, self.view_from_whites_perspective)
        pygame.display.flip()


