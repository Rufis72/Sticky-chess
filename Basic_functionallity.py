# importing modules
from tabnanny import check

import pygame, sys, types, math, typing, copy, pyperclip, time

# todo add pawn promotion window, add eval for doubled pawn, add changability to bot.evaluate_position(), add fen capability to board, train values with stockfish as source of truth, changed eval values to be more like stockfish?, add different eval functions, add eval option to minimax


class IllegalMove(Exception):
    """Illegal move error"""
    pass


class Board:
    """Used to edit the board, get legal moves, and other associated proccessess.
    Terms:
    Notation: A string used to represent a square in chess
    Index: Typically used to represent the acutal location of a square's information"""
    def __init__(self, allow_king_blunders: bool = False, copy_moves_when_game_over: bool = False):
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
        self.is_copy = False
        self.player_moves = []
        self.white_oo = True
        self.white_ooo = True
        self.black_oo = True
        self.black_ooo = True
        self.copy_moves_when_over = copy_moves_when_game_over
        self.allow_king_blunders = allow_king_blunders


    def game_ended(self, side_won: str):
        """A method to run any neccesary code at the end of the game"""
        # Current code is temporary
        if self.copy_moves_when_over:
            pyperclip.copy(self.player_moves)
        if not self.is_copy:
            print(f"Game over, {side_won} won!")
            sys.exit()


    def create_instance_copy(self):
        """A method to create a instance copy of self"""
        # creating the copy
        c_copy = copy.deepcopy(self)
        # changing its values (to prevent deletion of main board)
        c_copy.is_copy = True
        return c_copy


    def del_instance_copy(self):
        """Deletes an (ONLY) instance copy (the one its being ran in)"""
        # checking if the instance is a copy
        if self.is_copy:
            # deleting the copy
            del self
        else:
            # raising an error if it is the main board
            raise Exception("Cannot (should not) delete any non instance (main) boards")


    def find_piece(self, piece: str = "all", color: str = "any"):
        """Returns all squares that have pieces that fulfill the entered criteria"""
        # defining variables
        output = []
        # looping through every square
        for i in range(8):
            for n in range(8):
                # checking if that squares data fits the criteria
                if (piece == "all" or self.board[i][n] == piece) and (color == "any" or self.board_color[i][n] == color):
                    # appending the square to the output list
                    output.append(self.get_notation_via_index((i, n)))
        # returning a list of all squares that meet the criteria
        return output

    
    def get_notation_via_index(self, index: typing.Tuple):
        """Returns the notation based off an index"""
        return self.board_notation[index[0]][index[1]]
    
    
    def get_index_via_notation(self, notation: str):
        """Returns the index based off a notation."""
        return (int(notation[1]) - 1, self.board_notation[int(notation[1]) - 1].index(notation))


    def get_square_value(self, notation: str):
        "Returns the value of a square based off a notation. The data will be returned in a tuple consisting of 1st: the piece on that square, and 2nd: the piece's color."
        return (self.board[self.get_index_via_notation(notation)[0]][self.get_index_via_notation(notation)[1]],
                self.board_color[self.get_index_via_notation(notation)[0]][self.get_index_via_notation(notation)[1]])


    def if_white_could_enpessant_this_move(self):
        """Returns True if there is a black pawn that has advanced two squares, otherwise returns False"""
        if len(self.player_moves) == 0:
            return False
        if self.player_moves[-1][0] != "o" and self.get_square_value(self.player_moves[-1][0:2]) == ("Pawn", "black") and self.get_square_value(self.player_moves[-1][1]) == "7" and self.get_square_value(self.player_moves[-1][3]) == "5":
            return True
        else:
            return False


    def if_black_could_enpessant_this_move(self):
        """Returns True if there is a white pawn that has advanced two squares, otherwise returns False."""
        if len(self.player_moves) == 0:
            return False
        if self.player_moves[-1][0] != "o" and self.get_square_value(self.player_moves[-1][0:2]) == ("Pawn", "white") and self.get_square_value(self.player_moves[-1][1]) == "2" and self.get_square_value(self.player_moves[-1][3]) == "4":
            return True
        else:
            return False

    
    def clear_square(self, notation: str):
        """Removes all data from a square based off notation."""
        if type(notation) == str:
            notation = [notation]
        for i in range(len(notation)):
            index = self.get_index_via_notation(notation[i])
            self.board[index[0]][index[1]] = None
            self.board_color[index[0]][index[1]] = None


    def move(self, move: str):
        """Performs ANY move (Copys the contents of one square to another, and clears the first squares data), also updates castling rights if a rook or king has moved."""
        # Defining variables
        index1 = self.get_index_via_notation(move[0:2])
        index2 = self.get_index_via_notation(move[2:4])
        piece_values = self.get_square_value(move[0:2])
        # Checking if the piece is a Rook
        if piece_values[0] == "Rook":
            # Changing the castling values based off the rook (Checks if it's in a corner (Where rooks start off) and if so, changes if the color that side belongs to can castle on that side)
            # short castling
            if index1 == (0, 7):
                self.white_oo = False
            elif index1 == (7, 7):
                self.black_oo = False
            # long castling
            elif index1 == (7, 0):
                self.white_ooo = False
            elif index1 == (7, 0):
                self.black_ooo = False
        # Checking if the piece is a king
        if piece_values[0] == "King":
            # Changes one sides castling rights to all be false
            if piece_values[1] == "white":
                # Removes White's castling rights
                self.white_oo = False
                self.white_ooo = False
            else:
                # Removes Black's castling rights
                self.black_oo = False
                self.black_ooo = False
        # Changes the values of the board to align with the move
        end_square_data = self.get_square_value(move[2:4])
        self.board[index2[0]][index2[1]] = self.board[index1[0]][index1[1]]
        self.board_color[index2[0]][index2[1]] = self.board_color[index1[0]][index1[1]]
        self.clear_square(move[0:2])
        self.player_moves.append(move)
        if end_square_data[0] == "King":
            self.game_ended(piece_values[1])

    
    def get_seeing_as_bishop_at(self, notation: str):
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


    def errorless_index(self, list: list, index_0):
        """Performs the same action as '.index', but instead of returning an error if an item is not found, it will instead return none."""
        # attempting to index the item
        try:
            # returning the index
            return list.index(index_0)
        except:
            # returning None since the index returned an error
            return None
    

    def get_seeing_as_pawn_at(self, notation: str):
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


    def set_square_value(self, notation: str, color: str = None, piece: str = None):
        index = self.get_index_via_notation(notation)
        if color != None:
            self.board_color[index[0]][index[1]] = color
        if piece != None:
            self.board[index[0]][index[1]] = piece
        if self.errorless_index(self.get_square_value(notation), None) != None:
            raise Exception(f"A board square must be either None, None or Piece, Color. Not {self.get_square_value(notation)}")

    def get_legal_as_pawn_at(self, notation: str):
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
                if self.if_white_could_enpessant_this_move():
                    pawn_location = self.get_index_via_notation(self.player_moves[-1][2:4])
                    if (index[1] - 1 == pawn_location[1] or index[1] + 1 == pawn_location[1]) and index[0] == pawn_location[0]:
                        moves.append((pawn_location[0] + 1, pawn_location[1]))
            except IndexError:
                pass
            # Checking if the pawn can take
            if index[1] != 7 and self.board_color[index[0] + 1][index[1] + 1] == "black":
                moves.append((index[0] + 1, index[1] + 1))
            if index[1] != 0 and self.board_color[index[0] + 1][index[1] - 1] == "black":
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
            if self.if_black_could_enpessant_this_move():
                pawn_location = self.get_index_via_notation(self.player_moves[-1][2:4])
                if (index[1] - 1 == pawn_location[1] or index[1] + 1 == pawn_location[1]) and index[0] == pawn_location[0]:
                    moves.append((pawn_location[0] - 1, pawn_location[1]))
            # Checking if the pawn can take
            if index[1] != 7 and self.board_color[index[0] - 1][index[1] + 1] == "white":
                moves.append((index[0] - 1, index[1] + 1))
            if index[1] != 0 and self.board_color[index[0] - 1][index[1] - 1] == "white":
                moves.append((index[0] - 1, index[1] - 1))
        # checking for pawn promotion
        for i in range(len(moves) -1, -1, -1):
            if moves[i][0] == 7 or moves[i][0] == 0:
                # adding all version of the move with promotion
                moves[i] = self.get_notation_via_index(moves[i])
                moves.append(moves[i] + "=Q")
                moves.append(moves[i] + "=R")
                moves.append(moves[i] + "=B")
                moves.append(moves[i] + "=N")
                # deleting the original (illegal) move
                del moves[i]
        # Checking if any squares are "illegal"
        for i in range(len(moves) - 1, -1, -1):
            if type(moves[i]) != str and (moves[i][0] < 0 or moves[i][0] > 7 or moves[i][1] < 0 or moves[i][1] > 7):
                del moves[i]
        # converting indexs to notation
        for i in range(len(moves)):
            # checking if the square isn't already notation (because of pawn promotion)
            if type(moves[i]) != str:
                moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def get_seeing_as_rook_at(self, notation: str):
        """Returns all squares a rook at notation could see"""
        # Defining variables
        index = self.get_index_via_notation(notation)
        moves = []
        # Columns
        for i in range(index[0] - 1, -1, -1):
            moves.append((i, index[1]))
            if self.board[i][index[1]] != None:
                break
        for i in range(index[0] + 1, 8):
            moves.append((i, index[1]))
            if self.board[i][index[1]] != None:
                break
        # Rows
        for i in range(index[1] - 1, -1, -1):
            moves.append((index[0], i))
            if self.board[index[0]][i] != None:
                break
        for i in range(index[1] + 1, 8):
            moves.append((index[0], i))
            if self.board[index[0]][i] != None:
                break
        # Checking if any squares are illegal
        for i in range(len(moves) - 1, -1, -1):
            if moves[i][0] < 0 or moves[i][0] > 7 or moves[i][1] < 0 or moves[i][1] > 7:
                del moves[i]
        # Converting all indexs to notations
        for i in range(len(moves)):
            moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def get_seeing_as_queen_at(self, notation: str):
        return [*self.get_seeing_as_rook_at(notation), *self.get_seeing_as_bishop_at(notation)]

    
    def get_seeing_as_knight_at(self, notation: str):
        """Returns all legal squares a knight could move to from a certain square (The passed in notation)."""
        # Defining variables
        index = self.get_index_via_notation(notation)
        moves = []
        moves.append((index[0] - 1, index[1] - 2))
        moves.append((index[0] - 1, index[1] + 2))
        moves.append((index[0] + 1, index[1] - 2))
        moves.append((index[0] + 1, index[1] + 2))
        moves.append((index[0] - 2, index[1] - 1))
        moves.append((index[0] - 2, index[1] + 1))
        moves.append((index[0] + 2, index[1] - 1))
        moves.append((index[0] + 2, index[1] + 1))
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


    def get_seeing_as_king(self, notation: str):
        """Returns all squares a king protects from a certain square (the passed in notation)."""
        # Defining variables
        moves = []
        index = self.get_index_via_notation(notation)
        # Adds every possible direction of squares next to the king
        moves.append((index[0] + 1, index[1] + 1))
        moves.append((index[0] + 1, index[1] - 1))
        moves.append((index[0] - 1, index[1] - 1))
        moves.append((index[0] - 1, index[1] + 1))
        moves.append((index[0] + 1, index[1]))
        moves.append((index[0] - 1, index[1]))
        moves.append((index[0], index[1] + 1))
        moves.append((index[0], index[1] - 1))
        i2 = 0
        for i in range(len(moves)):
            if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7:
                del moves[i2]
                i2 -= 1
            i2 += 1
        for i in range(len(moves)):
            moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def get_legal_as_king_at(self, notation: str):
        """Returns all possible legal moves as a king from a certain square (the passed in notation)."""
        # Getting all "typical" (moving to all adjacent squares) king moves
        moves = [*self.get_seeing_as_king(notation)]
        if self.get_square_value(notation)[1] == "white":
            opposite_color = "black"
        else:
            opposite_color = "white"
        if notation == "b8":
            print(1)
        # if king blunders aren't allowed, checks if any move would blunder the king
        if not self.allow_king_blunders:
            for i in range(len(moves) - 1, -1, -1):
                if self.get_pieces_seeing(notation, opposite_color, True) != []:
                    del moves[i]
        # Castling
        # Checking the color of the king
        if self.get_square_value(notation)[1] == "white":
            # Castling for white
            if self.white_oo and self.get_pieces_seeing("f1", "black") == [] and self.get_pieces_seeing("g1", "black") == [] and self.get_square_value("f1") == (None, None) and self.get_square_value("g1") == (None, None) and self.white_oo:
                moves.append("o-o")
            if self.white_oo and self.get_pieces_seeing("b1", "black") == [] and self.get_pieces_seeing("c1", "black") == [] and self.get_pieces_seeing("d1", "black") == [] and self.get_square_value("b1") == (None, None) and self.get_square_value("c1") == (None, None) and self.get_square_value("d1") == (None, None) and self.white_ooo:
                moves.append("o-o-o")
        else:
            # Castling for black
            if self.black_oo and self.get_pieces_seeing("f8", "white") == [] and self.get_pieces_seeing("g8", "white") == [] and self.get_square_value("f8") == (None, None) and self.get_square_value("g8") == (None, None):
                moves.append("o-o")
            if self.black_oo and self.get_pieces_seeing("b8", "white") == [] and self.get_pieces_seeing("c8", "white") == [] and self.get_pieces_seeing("d8", "white") == [] and self.get_square_value("b8") == (None, None) and self.get_square_value("c8") == (None, None) and self.get_square_value("d8") == (None, None):
                moves.append("o-o-o")
        # Checking if any squares have friendly pieces on them
        for i in range(len(moves) - 1, -1, -1):
            if moves[i] != "o-o" and moves[i] != "o-o-o":
                if self.get_square_value(moves[i])[1] == self.get_square_value(notation)[1]:
                    del moves[i]
        return moves
    
    
    def get_piece_seeing(self, notation: str):
        """Checks the value of square (gotten from notation), then gets what that piece sees (via checking the value of the square, then running that piece's respective function to get what it sees)."""
        index = self.get_index_via_notation(notation)
        piece = self.get_square_value(notation)[0]
        moves = []
        if piece == "Knight":
            moves = self.get_seeing_as_knight_at(notation)
        elif piece == "King":
            moves = self.get_seeing_as_king_at(notation)
        elif piece == "Rook":
            moves = self.get_seeing_as_rook_at(notation)
        elif piece == "Bishop":
            moves = self.get_seeing_as_bishop_at(notation)
        elif piece == "Queen":
            moves = self.get_seeing_as_queen_at(notation)
        elif piece == "Pawn":
            moves = self.get_seeing_as_pawn_at(notation)
        # Checking if any squares are illegal (excluding castling)
        if type(moves) != types.NoneType:
            for i in range(len(moves)):
                moves[i] = self.get_index_via_notation(moves[i])
            i2 = 0
            for i in range(len(moves)):
                if moves[i] != "o-o" and moves[i] != "o-o-o":
                    if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7:
                        del moves[i2]
                        i2 -= 1
                    i2 += 1
            for i in range(len(moves)):
                moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def clear_board(self):
        """Removes the data of all squares on the board"""
        for i in range(len(self.board)):
            for n in range(len(self.board[i])):
                self.board[i][n] = None
                self.board_color[i][n] = None


    def get_pieces_seeing(self, notation: str, color: typing.Tuple = None, check_legal_for_pawn: bool = False):
        """Returns the squares off all pieces seeing a certain square (the square in question is gotten from notation), color removes all pieces that are not of one color"""
        pieces_locations = []
        for i in range(8):
            for n in range(8):
                try:
                    if check_legal_for_pawn and self.board[i][n] == "Pawn":
                        self.get_legal_moves(self.get_notation_via_index((i, n)))
                    elif self.get_piece_seeing(self.get_notation_via_index((i, n))).index(notation) != None:
                        pieces_locations.append(self.get_notation_via_index((i, n)))
                except:
                    pass
        if color != None:
            for i in range(len(pieces_locations) - 1, -1, -1):
                if self.get_square_value(pieces_locations[i])[1] != color:
                    del pieces_locations[i]
        return pieces_locations



    def get_legal_moves(self, notation: str) -> list:
        """Returns all legal moves of a piece on a specific square (gotten via notation) (The moves are obtained by either getting what squares a piece sees, then vetting all the moves to remove the squares it cannot move to. Or uses the respective function to calculate that piece's legal moves)."""
        piece = self.get_square_value(notation)[0]
        if piece == "Pawn":
            moves = self.get_legal_as_pawn_at(notation)
        elif piece == "King":
            moves = self.get_legal_as_king_at(notation)
        else:
            moves = self.get_piece_seeing(notation)
        # checking if "[]" was returned
        if type(moves) != types.NoneType:
            # changing all squares to indexs
            for i in range(len(moves)):
                # checking if the move is nether castling nor pawn promotion
                if len(moves[i]) < 3:
                    moves[i] = self.get_index_via_notation(moves[i])
            # checking if any squares are "illegal"
            for i in range(len(moves) - 1, -1, -1):
                # checking if that move is either castling or pawn promotion (then they were not converted to indexs)
                if type(moves[i]) != str:
                    if moves[i][0] < 0 or moves[i][0] > 7 or moves[i][1] < 0 or moves[i][1] > 7 or self.get_square_value(notation)[1] == self.get_square_value(self.get_notation_via_index(moves[i]))[1]:
                        del moves[i]
            # changing all squares back to notation (except castling and pawn promotion)
            for i in range(len(moves)):
                # checking if the move is neither pawn promotion, nor castling
                if type(moves[i]) != str:
                    moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def who_to_move(self):
        """Returns a string containing either 'white' or 'black' based off which player's turn it is to move."""
        if len(self.player_moves) % 2 == 0:
            return "white"
        else:
            return "black"


    def legal_move(self, move: str, raise_error_if_illegal: typing.Tuple = True, show_debug_data: bool = False) -> True or False:
        """Checks if the move passed in is legal, if so then the move is performed and the function returns True, if it failed one of the checks, the function will return False."""
        # Basic check for illegal moves
        if raise_error_if_illegal:
            if len(move) < 4 and move != "o-o":
                raise IllegalMove(f"move \"{move}\" is too short")
            if move != "o-o" and move != "o-o-o":
                if not int(move[1]) <= 8 or not int(move[1]) >= 1:
                    raise IllegalMove(f"move \"{move}\" contains illegal square(s)")
                if not int(move[3]) <= 8 or not int(move[3]) >= 1:
                    raise IllegalMove(f"move \"{move}\" contains illegal square(s)")
                if self.get_square_value(move[0:2]) == (None, None):
                    raise IllegalMove(f"move \"{move}\" is illegal, the square {move[0:2]} is empty")
                if self.get_square_value(move[0:2])[1] != self.who_to_move():
                    raise IllegalMove(f"move \"{move}\" is illegal, it is not {self.get_square_value(move[0:2])[1]}'s turn to move")
                if self.get_square_value(move[0:2])[1] == self.get_square_value(move[2:4])[1]:
                    raise IllegalMove(f"move \"{move}\" is illegal, you cannot capture your own pieces")
            if len(move) > 6:
                raise IllegalMove(f"move \"{move}\" is too long")
            if len(move) == 6 and self.get_square_value(move[0:2])[0] == "Pawn" and (move[2] == "0" or move[2] == "7"):
                raise IllegalMove(f"move \"{move}\" is illegal, pawns must promote when reaching their back rank")

        # Checking if the move is castling, and if so skipping normal legal move check procedures (to prevent an error)
        if move[0] == "o":
            # Castling for white
            if self.who_to_move() == "white":
                if self.get_square_value("e1") == ("King", "white"):
                    # Checks if white can legally short castle, then, if so, performs it
                    if self.errorless_index(self.get_legal_as_king_at("e1"), "o-o") and move == "o-o":
                        # "moving" the Rook and King
                        self.clear_square("e1")
                        self.clear_square("h1")
                        # adding the King and Rook to their new positions
                        self.set_square_value("f1", "white", "Rook")
                        self.set_square_value("g1", "white", "King")
                        # adding the move to self.player_moves
                        self.player_moves.append("o-o")
                        # removing castling rights
                        self.white_oo = False
                        self.white_ooo = False
                        return True
                    # Checks if white can legally long castle, then, if so, performs it
                    if self.errorless_index(self.get_legal_as_king_at("e1"), "o-o-o") and move == "o-o-o":
                        # "moving" the Rook and King
                        self.clear_square("e1")
                        self.clear_square("a1")
                        # adding the King and Rook to their new positions
                        self.set_square_value("d1", "white", "Rook")
                        self.set_square_value("c1", "white", "King")
                        # adding the move to self.player_moves
                        self.player_moves.append("o-o-o")
                        # removing castling rights
                        self.white_oo = False
                        self.white_ooo = False
                        return True
            else:
                # Castling for black
                if self.get_square_value("e8") == ("King", "black"):
                    # Checks if black can legally short castle, then, if so, performs it
                    if self.errorless_index(self.get_legal_as_king_at("e8"), "o-o") and move == "o-o":
                        # "moving" the Rook and King
                        # removing the old King and Rook
                        self.clear_square("e8")
                        self.clear_square("h8")
                        # adding the King and Rook to their new positions
                        self.set_square_value("f8", "black", "Rook")
                        self.set_square_value("g8", "black", "King")
                        # adding the move to self.player_moves
                        self.player_moves.append("o-o")
                        # removing castling rights
                        self.black_oo = False
                        self.black_ooo = False
                        return True
                    # Checks if black can legally long castle, then, if so, performs it
                    if self.errorless_index(self.get_legal_as_king_at("e8"), "o-o-o") and move == "o-o-o":
                        # "moving" the Rook and King
                        self.clear_square("e8")
                        self.clear_square("a8")
                        # adding the King and Rook to their new positions
                        self.set_square_value("d8", "black", "Rook")
                        self.set_square_value("c8", "black", "King")
                        # adding the move to self.player_moves
                        self.player_moves.append("o-o-o")
                        # removing castling rights
                        self.black_oo = False
                        self.black_ooo = False
                        return True
        # Checks for enpessant (en peasant)
        elif self.get_square_value(move[0:2])[0] == "Pawn" and self.get_square_value(move[2:4])[0] == None and move[0] != move[2] and self.who_to_move() == self.get_square_value(move[0:2])[1] and (self.if_white_could_enpessant_this_move() or self.if_black_could_enpessant_this_move()):
            # defining variables
            index_FL = self.get_index_via_notation(move[2:4])
            # Checking enpessant for white
            if self.get_square_value(move[0:2])[1] == "white" and self.board[index_FL[0] - 1][index_FL[1]] == "Pawn":
                self.move(move)
                self.clear_square(self.get_notation_via_index((index_FL[0] - 1, index_FL[1])))
                return True
            # Checking enpessant for black
            if self.get_square_value(move[0:2])[1] == "black" and self.board[index_FL[0] + 1][index_FL[1]] == "Pawn":
                self.move(move)
                self.clear_square(self.get_notation_via_index((index_FL[0] - 1, index_FL[1])))
                return True
        # Checks for pawn promotion
        elif self.get_square_value(move[0:2])[0] == "Pawn" and len(move) == 6 and (move[3] == "8" or move[3] == "1"):
            # makes initial move
            self.move(move[0:4])
            self.player_moves[-1] = move
            # Changes the pawn to the piece its promoting to
            if move[5] == "B":
                self.set_square_value(move[2:4], piece="Bishop")
                return  True
            elif move[5] == "N":
                self.set_square_value(move[2:4], piece="Knight")
                return True
            elif move[5] == "R":
                self.set_square_value(move[2:4], piece="Rook")
                return True
            elif move[5] == "Q":
                self.set_square_value(move[2:4], piece="Queen")
                return True
            elif raise_error_if_illegal:
                raise IllegalMove(f"move \"{move}\" is illegal, pawns must promote to either a Bishop, Knight, Rook, or Queen (B, N, R, Q), not to \"{move[5]}\"")
        else:
            if self.errorless_index(self.get_legal_moves(move[0:2]), move[2:4]) != None and self.get_square_value(move[0:2])[1] == self.who_to_move():
                self.move(move)
                return True
        # printing debug data (if enabled)
        if show_debug_data:
            print((self.get_square_value(move[0:2]), self.get_square_value(move[2:4]), move))
        # raising an error, or if disabled, returning False
        if raise_error_if_illegal:
            raise IllegalMove(f"move \"{move}\" is illegal")
        else:
            return False


    def legal_moves(self, moves: list or typing.Tuple, wait: float or int = 0) -> list:
        """Performs multiple legal moves passed in as a list or tuple"""
        # defining variables
        returning = []
        for i in range(len(moves)):
            returning.append(self.legal_move(moves[i]))
            time.sleep(wait)
        return returning


    def get_all_legal_moves(self, return_non_color_to_play_moves: bool = False) -> list:
        """Gets all legal moves of every piece. Returns in this format: [starting_square + ending_square, starting_square + ending_square, etc]"""
        # defining variables
        moves = []
        who_moving = self.who_to_move()
        non_start_moves = []
        # cycling through every square
        for y in range(8):
            for x in range(8):
                # checking if that square should be evaluated
                if self.board[y][x] != None and (return_non_color_to_play_moves or self.board_color[y][x] == who_moving):
                    # getting all the legal moves for that square
                    non_start_moves = self.get_legal_moves(self.get_notation_via_index((y, x)))
                    for i in range(len(non_start_moves)):
                        # adding the starting square to all the moves (if the move is not castling
                        if non_start_moves[i][0] != "o": # checking if the move is castling
                            non_start_moves[i] = self.get_notation_via_index((y, x)) + non_start_moves[i]
                    # adding the new moves the list of moves
                    moves = moves + non_start_moves
        return moves



class Display:
    def __init__(self, square_one_color: typing.Tuple = (125, 148, 93), square_two_color: typing.Tuple = (238, 238, 213), screen_size: typing.Tuple = (700, 700), background: typing.Tuple = (0, 0, 0), if_view_from_whites_perspective: bool = True, grid_lines_size: int = 0, square_selection_color: typing.Tuple = (255, 255, 0), allow_moves_as_opposite_colored_player: bool = False, legal_move_circle_indicator_size: float = 0.7, show_legal_moves_preview: bool = True, promotion_window_scale: float or int = 1):
        # Defining variables
        self.square_selection_color = square_selection_color
        self.view_from_whites_perspective = if_view_from_whites_perspective
        self.square_one_color = square_one_color
        self.square_two_color = square_two_color
        self.screen_size = screen_size
        self.background = background
        self.frame = 0
        self.drawn_background_squares = []
        self.allowed_moves_as_opposing_color = allow_moves_as_opposite_colored_player
        self.square_selected_one = None
        self.show_legal_moves_preview = show_legal_moves_preview
        self.board_notation_white = ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
                          "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
                          "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
                          "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
                          "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
                          "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
                          "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
                          "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]
        self.board_notation_black = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
                          "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
                          "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
                          "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
                          "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
                          "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
                          "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
                          "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]
        self.move_preview_circle_percentage = legal_move_circle_indicator_size
        self.board_notation = []
        if if_view_from_whites_perspective:
            self.board_notation = self.board_notation_white
        else:
            self.board_notation = self.board_notation_black
        # Defining variables - Math for scaling everything
        if grid_lines_size == 0:
            self.square_spacing_size = 0
        if self.screen_size[0] == screen_size[1]:
            if grid_lines_size == 0:
                self.square_spacing_size = -1
            else:
                self.square_spacing_size = (screen_size[0] / grid_lines_size) / 9
            self.board_offset_x = self.square_spacing_size
            self.board_offset_y = self.square_spacing_size
            self.square_edge_size = (screen_size[0] - (self.square_spacing_size * 9)) / 8
        elif self.screen_size[0] > self.screen_size[1]:
            if grid_lines_size == 0:
                self.square_spacing_size = -1
            else:
                self.square_spacing_size = (screen_size[1] / grid_lines_size) / 9
            self.board_offset_x = self.square_spacing_size - (self.screen_size[1] - self.screen_size[0]) / 2
            self.board_offset_y = self.square_spacing_size
            self.square_edge_size = (screen_size[1] - (self.square_spacing_size * 9)) / 8
        else:
            if grid_lines_size == 0:
                self.square_spacing_size = -1
            else:
                self.square_spacing_size = (screen_size[0] / grid_lines_size) / 9
            self.board_offset_x = self.square_spacing_size
            self.board_offset_y = self.square_spacing_size - (self.screen_size[0] - self.screen_size[1]) / 2
            self.square_edge_size = (screen_size[0] - (self.square_spacing_size * 9)) / 8
        # Defining variables - creating a hashmap linking to loaded chess piece images
        self.piece_locations = {
            "black Pawn": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkPawn.png"),
                                                 (self.square_edge_size, self.square_edge_size)),
            "black Bishop": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkBishop.png"),
                                                   (self.square_edge_size, self.square_edge_size)),
            "black Knight": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkKnight.png"),
                                                   (self.square_edge_size, self.square_edge_size)),
            "black Rook": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkRook.png"),
                                                 (self.square_edge_size, self.square_edge_size)),
            "black King": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkKing.png"),
                                                 (self.square_edge_size, self.square_edge_size)),
            "black Queen": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkQueen.png"),
                                                  (self.square_edge_size, self.square_edge_size)),
            "white Pawn": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightPawn.png"),
                                                 (self.square_edge_size, self.square_edge_size)),
            "white Knight": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightKnight.png"),
                                                   (self.square_edge_size, self.square_edge_size)),
            "white Bishop": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightBishop.png"),
                                                   (self.square_edge_size, self.square_edge_size)),
            "white Rook": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightRook.png"),
                                                 (self.square_edge_size, self.square_edge_size)),
            "white King": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightKing.png"),
                                                 (self.square_edge_size, self.square_edge_size)),
            "white Queen": pygame.transform.scale(pygame.image.load("Chess_Piece_Images/LightQueen.png"),
                                                  (self.square_edge_size, self.square_edge_size))}
        # Initializing pygame modules
        pygame.init()
        pygame.display.init()
        # Initializing pygame modules - defining the screen surface
        self.screen = pygame.display.set_mode(screen_size)
        pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkPawn.png"), (self.square_edge_size, self.square_edge_size))
        pygame.display.set_caption("Sticky Chess")


    def flip_viewing_angle(self):
        """Flips the viewing angle to the opposing color"""
        self.view_from_whites_perspective = not self.view_from_whites_perspective
        if self.view_from_whites_perspective:
            self.board_notation = self.board_notation_white
        else:
            self.board_notation = self.board_notation_black
        if self.square_selected_one != None:
            self.square_selected_one = ((self.square_selected_one - 32) * -1) + 32


    def draw_background(self, background: typing.Tuple = "Nothing entered"):
        """Draws a single color background"""
        # Checking if nothing entered (then draws a background based off the global background variable)
        if background == "Nothing entered":
            self.screen.fill(self.background)
        # Draws a background based off the passed in background color
        else:
            self.screen.fill(background)


    def move_via_click_check(self, board_class):
        """Checks for any squares being clicked, two have been, attempts that move"""
        var = self.allowed_moves_as_opposing_color or ((board_class.who_to_move() == "white" and self.view_from_whites_perspective) or (board_class.who_to_move() == "black" and not self.view_from_whites_perspective))
        if self.get_square_pressed() != None:
            if self.square_selected_one == None:
                self.square_selected_one = self.get_square_pressed()
            elif self.square_selected_one != self.get_square_pressed():

                move = self.board_notation[self.square_selected_one] + self.board_notation[self.get_square_pressed()]
                # checking if the piece is a king
                if board_class.get_square_value(self.board_notation[self.square_selected_one])[0] == "King":
                    if move == "e1g1" or move == "e8g8":
                        move = "o-o"
                    elif move == "e1c1" or move == "e8c8":
                        move = "o-o-o"
                if var:
                    board_class.legal_move(move, False)
                self.square_selected_one = None


    def get_legal_moves_preview(self, board_class, square_number: int) -> list:
        """Returns all legal moves of a square based of square number"""
        # getting all legal moves as notation
        notation_moves = board_class.get_legal_moves(self.board_notation[square_number])
        # changing all notation to square numbers
        for i in range(len(notation_moves) - 1, -1, -1):
            if notation_moves[i] != "o-o" and notation_moves[i] != "o-o-o" and len(notation_moves[i]) != 4:
                notation_moves[i] = self.board_notation.index(notation_moves[i])
            elif len(notation_moves[i]) == 4 and notation_moves[i][3] == "Q":
                notation_moves[i] = self.board_notation.index(notation_moves[i][0:2])
            elif notation_moves[i] == "o-o":
                if board_class.who_to_move() == "white":
                    notation_moves[i] = self.board_notation.index("g1")
                else:
                    notation_moves[i] = self.board_notation.index("g8")
            elif notation_moves[i] == "o-o-o":
                if board_class.who_to_move() == "white":
                    notation_moves[i] = self.board_notation.index("c1")
                else:
                    notation_moves[i] = self.board_notation.index("c8")
            else:
                del notation_moves[i]
        return notation_moves


    def setup_background_squares(self, show_legal_moves_preview: bool = False, board_class = None):
        """Draws all background squares"""
        # checking if anything needs to be passed in:
        if show_legal_moves_preview and board_class == None:
            raise Exception("If showing legal move previews, board_class needs to be passed in!")
        # changing the checkerboard pattern's colors to make each square the same color for all players
        if self.view_from_whites_perspective:
            color_alternation = 1
        else:
            color_alternation = 0
        # drawing all 64 squares
        for i in range(64):
            # simulating a snaking pattern
            if i % 8 == 0:
                color_alternation = (color_alternation + 1) % 2
            color_alternation = (color_alternation + 1) % 2
            # drawing a square with the first color if the color_alternation variable is 0
            if color_alternation == 0:
                self.drawn_background_squares.append(pygame.draw.rect(self.screen, self.square_one_color, pygame.Rect(((i % 8) * (self.square_spacing_size + self.square_edge_size)) + self.board_offset_x, (math.floor(i / 8) * (self.square_spacing_size + self.square_edge_size)) + self.board_offset_y, self.square_edge_size, self.square_edge_size)))
            # drawing a square with the second color if the color_alternation variable is 1
            else:
                self.drawn_background_squares.append(pygame.draw.rect(self.screen, self.square_two_color, pygame.Rect(((i % 8) * (self.square_spacing_size + self.square_edge_size)) + self.board_offset_x, (math.floor(i / 8) * (self.square_spacing_size + self.square_edge_size)) + self.board_offset_y, self.square_edge_size, self.square_edge_size)))
            # drawing an outline (if the square is selected)
            if i == self.square_selected_one:
                pygame.draw.rect(self.screen, self.square_selection_color, pygame.Rect(((i % 8) * (self.square_spacing_size + self.square_edge_size)) + self.board_offset_x, (math.floor(i / 8) * (self.square_spacing_size + self.square_edge_size)) + self.board_offset_y, self.square_edge_size, self.square_edge_size), int(self.square_edge_size / 10))
            # showing any previews of legal moves (if parameter to do so is true)
            if show_legal_moves_preview and self.square_selected_one != None:
                moves = self.get_legal_moves_preview(board_class, self.square_selected_one)
                # checking if the correct piece is moving, and is allowed to be moved by this player
                if (self.allowed_moves_as_opposing_color or ((board_class.who_to_move() == "white" and self.view_from_whites_perspective) or (board_class.who_to_move() == "black" and not self.view_from_whites_perspective))) and board_class.who_to_move() == board_class.get_square_value(self.board_notation[self.square_selected_one])[1]:
                    try:
                        if moves.index(i) != None:
                            # drawing the circle
                            pygame.draw.circle(self.screen, (128, 128, 128, 128), (self.drawn_background_squares[-1][0] + (self.square_edge_size / 2), self.drawn_background_squares[-1][1] + (self.square_edge_size / 2)), (self.square_edge_size / 2) * self.move_preview_circle_percentage)
                    except:
                        pass


    def draw_pieces(self, board_class, whites_point_of_view: bool = True):
        """Draws pieces based off the class variables passed in"""
        # reversing the board if viewing from whites perspective
        if whites_point_of_view:
            board_class.board_color.reverse()
            board_class.board.reverse()
        # Drawing all pieces
        for i in range(8):
            for n in range(8):
                # bliting a chess piece image based off self.piece_locations and the data from the board_class parameter (the try is there incase the space is None, in which case, normally a IndexError would be returned)
                try:
                    self.screen.blit(self.piece_locations.get(board_class.board_color[i][n] + " " + board_class.board[i][n]), ((n * (self.square_edge_size + self.square_spacing_size)) + self.board_offset_x, (i * (self.square_edge_size + self.square_spacing_size)) + self.board_offset_y))
                except:
                    pass
        # re-reversing the board to prevent constant switching between perspectives
        if whites_point_of_view:
            board_class.board_color.reverse()
            board_class.board.reverse()


    def update_screen(self, board_class, show_legal_moves_from_selected_piece: bool = False):
        """Updates the screen"""
        self.draw_background()
        self.setup_background_squares(show_legal_moves_from_selected_piece, board_class)
        self.draw_pieces(board_class, self.view_from_whites_perspective)
        self.move_via_click_check(board_class)
        pygame.display.flip()


    def get_square_pressed(self) -> int or None:
        """Returns an index of which square is being pressed, if none are, None is returned"""
        # iterating through all squares and checking if it is pressed
        for i in range(64):
            # defining variables (to improve readability of the if statement)
            square = self.drawn_background_squares[i]
            square_end = (square[0] + square[2], square[1] + square[3])
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            # checking if the mouse is within the dimension of the square, and if left click is being pressed
            if (pygame.mouse.get_pressed(3)[0]
                    and square[0] <= mouse_x
                    and square[1] <= mouse_y
                    and square_end[0] >= mouse_x
                    and square_end[1] >= mouse_y):
                return i
        return None


class Bot:
    def __init__(self, depth: int):
        self.depth = depth
        self.searched_positions = {}


    def get_white_material_advantage(self, board_class) -> int:
        """Returns the material advantage of white"""
        # defining variables
        white_material_advantage = 0
        # calculating the advantage
        # cycling through every square
        for i in range(8):
            for n in range(8):
                # checking if the piece is white
                if board_class.board_color[i][n] == "white":
                    # adding the material value to the score
                    if board_class.board[i][n] == "Pawn":
                        white_material_advantage += 1
                    elif board_class.board[i][n] == "Knight":
                        white_material_advantage += 3
                    elif board_class.board[i][n] == "Bishop":
                        white_material_advantage += 3
                    elif board_class.board[i][n] == "Rook":
                        white_material_advantage += 5
                    elif board_class.board[i][n] == "Queen":
                        white_material_advantage += 9
                # removing blacks material points from the score
                elif board_class.board_color[i][n] != None:
                    # subtracting the material value from the score
                    if board_class.board[i][n] == "Pawn":
                        white_material_advantage -= 1
                    elif board_class.board[i][n] == "Knight":
                        white_material_advantage -= 3
                    elif board_class.board[i][n] == "Bishop":
                        white_material_advantage -= 3
                    elif board_class.board[i][n] == "Rook":
                        white_material_advantage -= 5
                    elif board_class.board[i][n] == "Queen":
                        white_material_advantage -= 9
        return white_material_advantage


    def get_king_safety(self, board_class, color: str) -> float:
        """Returns a score based off the immediate safety of the white king"""
        # defining variables
        # defining variables - getting enemy color
        if color == "white":
            enemy = "black"
        else:
            enemy = "white"
        # defining variables - getting castling values
        if color == "white":
            oo = board_class.white_oo
            ooo = board_class.white_ooo
        else:
            oo = board_class.black_oo
            ooo = board_class.black_ooo
        location = board_class.find_piece(color=color, piece="King")
        # checking if there is no king (then returning a negative infinite score)
        if location == []:
            return float("-inf")
        king_index = board_class.get_index_via_notation(location[0])
        neighbor_squares = board_class.get_seeing_as_king(location[0])
        safety_score = float(0)
        # checking for friendly pieces above the king
        for i in range(len(neighbor_squares)):
            # checking if the piece is a pawn
            if board_class.get_square_value(neighbor_squares[i]) == ("Pawn", color):
                safety_score += 1
            # removing points for non-pawn pieces
            elif board_class.get_square_value(neighbor_squares[i])[1] == color:
                safety_score -= 0.1
        # checking for free (no enemy pieces seeing) squares around the king
        for i in range(len(neighbor_squares)):
            # getting all squares seeing the square
            squares = board_class.get_pieces_seeing(neighbor_squares, enemy)
            # removing score based off the amount of pieces seeing
            if len(squares) != 0:
                safety_score -= len(squares)
        # checking for castling options
        # checking if just one of the castling options has been removed
        if oo != ooo:
            safety_score -= 0.7
        # checking if both castling options do not exist
        elif not (oo and ooo):
            safety_score -= 2.3
        # checking for the position of the king
        # removing score based off how close the king is to the center
        Eking_indexz = king_index[0]
        Eking_indexo = king_index[1]
        if king_index[0] > 3:
            Eking_indexz -= 1
        if king_index[1] > 3:
            Eking_indexo -= 1
        safety_score -= (abs((Eking_indexz + 1) - 4)) * 0.4
        safety_score -= (abs((Eking_indexo + 1) - 4)) * 0.4
        return safety_score


    def get_white_advanced_pawn_value(self, board_class) -> int:
        """Returns a score based off how advanced white's pawns are on the board"""
        score = 0
        # cycling through every square
        for i in range(8):
            for n in range(8):
                # checking if the square is a white pawn
                if board_class.get_square_value(board_class.get_notation_via_index((i, n))) == ("Pawn", "white"):
                    # adding how far the pawn is down the board (all the "complicated" math is too flip the value since the data is represented from black's point of view)
                    score += i
        return score - 8


    def get_black_advanced_pawn_value(self, board_class) -> int:
        """Returns a score based off how advanced pawns are on the board"""
        score = 0
        # cycling through every square
        for i in range(8):
            for n in range(8):
                # checking if the square is a white pawn
                if board_class.get_square_value(board_class.get_notation_via_index((i, n))) == ("Pawn", "black"):
                    # adding how far the pawn is down the board
                    score += ((i + 1) * -1) + 8
        return score - 8


    def get_black_central_space_value(self, board_class, pawn_center_value: int or float = 2, general_central_value: int or float = 0.3) -> float:
        """Returns a score based off how many of blacks pieces are near the center / on "optimal" squares"""
        # defining variables
        score = float(0)
        # checking the important squares for pawns
        if board_class.board_color[4][2] == "black" and board_class.board[4][2] == "Pawn": # checking c5
            score += 2 * pawn_center_value
        if board_class.board_color[4][3] == "black" and board_class.board[4][3] == "Pawn": # checking d5
            score += 1.5 * pawn_center_value
        if board_class.board_color[4][4] == "black" and board_class.board[4][4] == "Pawn": # checking e5
            score += 2 * pawn_center_value
        # checking the central squares generally
        if board_class.board_color[4][4] == "black" and board_class.board[4][2] != "Pawn": # checking e5
            score += 1 * general_central_value
        if board_class.board_color[4][3] == "black" and board_class.board[4][2] != "Pawn": # checking d5
            score += 1 * general_central_value
        if board_class.board_color[3][4] == "black": # checking e4
            score += 0.8 * general_central_value
        if board_class.board_color[3][3] == "black": # checking d4
            score += 0.8 * general_central_value
        # checking the semi-central squares generally
        if board_class.board_color[2][2] == "black": # checking c3
            score += 1
        if board_class.board_color[2][3] == "black": # checking d3
            score += 1
        if board_class.board_color[2][4] == "black": # checking e3
            score += 0.8
        if board_class.board_color[2][5] == "black": # checking f3
            score += 0.8
        if board_class.board_color[3][2] == "black" and board_class.board[4][2] != "Pawn": # checking c4
            score += 1
        if board_class.board_color[3][5] == "black": # checking f4
            score += 1
        if board_class.board_color[4][2] == "black": # checking c5
            score += 0.8
        if board_class.board_color[4][5] == "black": # checking f5
            score += 0.8
        if board_class.board_color[5][2] == "black": # checking c6
            score += 1
        if board_class.board_color[5][3] == "black": # checking d6
            score += 1
        if board_class.board_color[5][4] == "black": # checking e6
            score += 0.8
        if board_class.board_color[5][5] == "black": # checking f6
            score += 0.8
        return score


    def get_white_central_space_value(self, board_class, pawn_center_values: float or int = 2, general_central_value: int or float = 0.3) -> float:
        """Returns a score based off how many of blacks pieces are near the center / on "optimal" squares"""
        # defining variables
        score = float(0)
        # checking the important squares for pawns
        if board_class.board_color[3][2] == "white" and board_class.board[4][2] == "Pawn": # checking c4
            score += 2 * pawn_center_values
        if board_class.board_color[3][3] == "white" and board_class.board[4][3] == "Pawn": # checking d4
            score += 1.5 * pawn_center_values
        if board_class.board_color[3][4] == "white" and board_class.board[4][4] == "Pawn": # checking e4
            score += 1.8 * pawn_center_values
        # checking the central squares generally
        if board_class.board_color[4][4] == "white": # checking e5
            score += 0.8 * general_central_value
        if board_class.board_color[4][3] == "white": # checking d5
            score += 0.8 * general_central_value
        if board_class.board_color[3][4] == "white" and board_class.board[4][2] != "Pawn": # checking e4
            score += 1 * general_central_value
        if board_class.board_color[3][3] == "white" and board_class.board[4][2] != "Pawn": # checking d4
            score += 1 * general_central_value
        # checking the semi-central squares generally
        if board_class.board_color[2][2] == "white": # checking c3
            score += 1
        if board_class.board_color[2][3] == "white": # checking d3
            score += 1
        if board_class.board_color[2][4] == "white": # checking e3
            score += 0.8
        if board_class.board_color[2][5] == "white": # checking f3
            score += 0.8
        if board_class.board_color[3][2] == "white" and board_class.board[4][2] != "Pawn": # checking c4
            score += 1
        if board_class.board_color[3][5] == "white": # checking f4
            score += 1
        if board_class.board_color[4][2] == "white": # checking c5
            score += 0.8
        if board_class.board_color[4][5] == "white": # checking f5
            score += 0.8
        if board_class.board_color[5][2] == "white": # checking c6
            score += 1
        if board_class.board_color[5][3] == "white": # checking d6
            score += 1
        if board_class.board_color[5][4] == "white": # checking e6
            score += 0.8
        if board_class.board_color[5][5] == "white": # checking f6
            score += 0.8
        return score


    def get_black_undeveloped_piece_score(self, board_class) -> float:
        """Returns a score based off how many pieces are on Black's back rank (ignoring the king)"""
        # defining variables
        score = float(0)
        # doing the actual checks
        for x in range(8):
            piece = board_class.board[7][x]
            if board_class.board_color[7][x] == "black" and piece != "King":
                if piece == "Knight" or piece == "Bishop":
                    score -= 2
                if piece == "Queen":
                    score -= 1.5
                if piece == "Rook":
                    score -= 0.3
        return score


    def get_white_undeveloped_piece_score(self, board_class) -> float:
        """Returns a score based off how many pieces are on White's back rank (ignoring the king)"""
        # defining variables
        score = float(0)
        # doing the actual checks
        for x in range(8):
            piece = board_class.board[0][x]
            if board_class.board_color[0][x] == "white" and piece != "King":
                if piece == "Knight" or piece == "Bishop":
                    score -= 2
                if piece == "Queen":
                    score -= 1.5
                if piece == "Rook":
                    score -= 0.3
        return score




    def evaluate_position(self, board_class, player) -> float:
        # defining variables
        white_eval = 0
        black_eval = 0
        # evaluating white's position
        # changing points based off material advantage
        # adding an extra amount to create an insentive for trading when up, and not to when down
        white_eval += (self.get_white_material_advantage(board_class) * 1.6)
        # adding eval for advanced pawns
        white_eval += self.get_white_advanced_pawn_value(board_class) * 0.3
        # adding eval for king safety
        white_eval += self.get_king_safety(board_class, "white") * 1.3
        # removing eval for undeveloped pieces
        white_eval += self.get_white_undeveloped_piece_score(board_class) * 0.7
        # adding eval for central pieces
        white_eval += self.get_white_central_space_value(board_class) * 1.1

        # evaluating black's position
        # changing points based off material advantage
        # adding an extra amount to create an insentive for trading when up, and not to when down
        black_eval -= (self.get_white_material_advantage(board_class) * 1.6)
        # adding eval for advanced pawns
        black_eval += self.get_black_advanced_pawn_value(board_class) * 0.3
        # adding eval for king safety
        black_eval += self.get_king_safety(board_class, "black") * 1.3
        # removing eval for undeveloped pieces
        black_eval += self.get_black_undeveloped_piece_score(board_class) * 0.7
        # adding eval for central pieces
        black_eval += self.get_black_central_space_value(board_class) * 1.1

        # returning the score
        if player == "white":
            return (white_eval - black_eval) # positive = you're winning, negative = opposing player is winning
        elif player == "black":
            return (black_eval - white_eval)  # positive = you're winning, negative = opposing player is winning
        else:
            raise Exception(f"player must be either 'white' or 'black', not {player}!")

    def minimax(self,
                depth: int,
                board_class_instance: object,
                player: str,
                is_maxing_player: bool = None,
                alpha: float = float('-inf'),
                beta: float = float('inf'),
                moves: list = [],
                newmove: str = None) -> tuple:
        """Searches every option of moves and returns the best move"""

        # defining variables
        current_instance = board_class_instance.create_instance_copy()  # creating a copy of the class instance
        if newmove != None: # checking if there is any new move
            moves.append(newmove) # adding the new move to the moves list
            current_instance.legal_move(newmove)  # performing the new move so we have a instance with our updated board
        else:
            self.searched_positions = {}
        if self.searched_positions.get(str(current_instance.board)) == None:
            if is_maxing_player == None: # getting the is_maxing_player paramater if nothing was entered
                if player == board_class_instance.who_to_move():
                    is_maxing_player = True
                else:
                    is_maxing_player = False

            returning_move = None

            # checking if you have reached max depth
            if depth <= 0:
                evaluation = self.evaluate_position(current_instance, player)
                self.searched_positions.update({str(current_instance.board): (evaluation, [])})
                return((evaluation, []))

            # beginning / continuing the search down the possibility tree
            # checking if it should try and get the best moves for the current player
            if is_maxing_player:
                max_eval = float('-inf')
                for move in current_instance.get_all_legal_moves():
                    board_eval = self.minimax(depth - 1, current_instance, player, False, alpha, beta, moves, move)
                    max_eval = max(max_eval, board_eval[0])
                    alpha = max(alpha, board_eval[0])
                    if max_eval == board_eval[0]:
                        returning_move = [move]
                    try:
                        if beta <= alpha:
                            break
                    except:
                        pyperclip.copy(board_class_instance.player_moves)
                        raise Exception("error ran into, moves copied to clipboard")
                self.searched_positions.update({str(current_instance.board): (max_eval, returning_move + board_eval[1])})
                return((max_eval, returning_move + board_eval[1]))

            # getting the best move for the opponent, to see the position we can force.
            else:
                min_eval = float('inf')
                for move in current_instance.get_all_legal_moves():
                    board_eval = self.minimax(depth - 1, current_instance, player, True, alpha, beta, moves, move)
                    min_eval = min(min_eval, board_eval[0])
                    beta = min(beta, board_eval[0])
                    if min_eval == board_eval[0]:
                        returning_move = [move]
                    if beta <= alpha:
                        break
                self.searched_positions.update({str(current_instance.board): (min_eval, returning_move + board_eval[1])})
                return((min_eval, returning_move + board_eval[1]))
        else:
            return list(self.searched_positions.get(str(current_instance.board)))


