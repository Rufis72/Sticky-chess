import math
from operator import index


class Board:
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
    
    
    def get_notation_via_index(self, index):
        return self.board_notation[index[0]][index[1]]


    def if_contains(self, item, search):
        for i in range(len(search)):
            try:
                item.index(search[i])
                return True
            except:
                pass
        return False
    
    
    def get_index_via_notation(self, notation):
        return (int(notation[1]) - 1, self.board_notation[int(notation[1]) - 1].index(notation))


    def get_square_value(self, notation):
        return (self.board[self.get_index_via_notation(notation)[0]][self.get_index_via_notation(notation)[1]],
                self.board_color[self.get_index_via_notation(notation)[0]][self.get_index_via_notation(notation)[1]])


    def bundled_or(self, argument_a, argument_b):
        return argument_a or argument_b


    def if_white_can_enpessant_this_move(self):
        if len(self.player_moves) == 0:
            return None
        last_moved_piece = self.board[self.get_index_via_notation(self.player_moves[-1][2:4])[0]][self.get_index_via_notation(self.player_moves[-1][2:4])[1]]
        if last_moved_piece == "Pawn" and self.player_moves[-1][1] == "7" and self.player_moves[-1][3] == "5":
            return True
        else:
            return False


    def if_black_can_enpessant_this_move(self):
        if self.board[self.get_index_via_notation(self.player_moves[-1][2:4])[0]][self.get_index_via_notation(self.player_moves[-1][2:4])[1]] == "Pawn" and self.player_moves[-1][1] == "2" and self.player_moves[-1][3] == "4":
            return True
        else:
            return False


    def multi_append(self, list, items_to_be_appended):
        return (list, items_to_be_appended)

    
    def clear_square(self, notation):
        if type(notation) == str:
            notation = [notation]
        for i in range(len(notation)):
            index = self.get_index_via_notation(notation[i])
            self.board[index[0]][index[1]] = None
            self.board_color[index[0]][index[1]] = None


    def move(self, move):
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

    
    def square_empty(self, notation):
        if self.get_square_value(notation) == (None, None):
            return True
        else:
            return False
    
    
    def squares_empty(self, notations):
        true = True
        for i in range(len(self, notations)):
            if self.get_square_value(notations[i]) != (None, None) and true:
                true = False
        return true
    
    
    def get_seeing_as_bishop_at(self, notation):
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
        try:
            return list_0.index(index_0)
        except:
            return None
    
    
    def get_seeing_as_pawn_at(self, notation):
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


    def check_if_squares_legal(self, list_of_squares):
        moves = list_of_squares
        i2 = 0
        for i in range(len(moves)):
            if self.if_contains(moves[i], ("a", "b", "c", "d", "e", "f", "g", "h")):
                moves[i] = self.get_index_via_notation(moves[i])
        for i in range(len(moves)):
            if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7:
                del moves[i2]
                i2 -= 1
            i2 += 1
        for i in range(len(moves)):
            moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def get_legal_as_pawn_at(self, notation):
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
        pieces_locations = []
        for i in range(64):
            if self.board[math.floor(i / 8)][i % 8] != None:
                try:
                    pieces_locations.append(self.get_piece_seeing(self.get_notation_via_index((math.floor(i / 8), i % 8))))
                except:
                    pass
        return pieces_locations


    def get_legal_moves(self, notation):
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
        if len(self.player_moves) == 0:
            return "white"
        return self.get_square_value(self.player_moves[-1][2:4])
    
    
    def get_square_seen_by(self, notation):
        seeing = []
        index = self.get_index_via_notation(self.notation)
        for a in range(len(self.board)):
            for b in range(len(self.board[a])):
                try:
                    if self.board[a][b] is not None:
                        if self.get_piece_seeing(self.get_notation_via_index((a, b))).index(notation) is not None:
                            seeing.append(self.board_notation[a][b])
                except:
                    pass
        return seeing
    def legal_move(self, move):
        if self.errorless_index(self.get_legal_moves(move[0:2]), move[2:4]) != None and self.get_square_value(move[0:2]) != self.who_to_move():
            self.move(move)
            return True
        return False
