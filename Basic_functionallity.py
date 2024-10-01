class IllegalMove(Exception):
    """Illegal move error"""
    pass

# TODO kings cannot move except castling, sometimes piece legal move previews will be completely off, add scaling to legal move preview circles (radius = 1/4 of square edge size


class Board:
    """Used to edit the board, get legal moves, and other associated proccessess.
    Terms:
    Notation: A string used to represent a square in chess
    Index: Typically used to represent the acutal location of a square's information"""
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


    def game_ended(self, side_lost):
        """A method to run any neccesary code at the end of the game"""
        # Current code is temporary
        print(f"Game over! {side_lost} lost!")
        import sys
        sys.exit()

    
    def get_notation_via_index(self, index):
        """Returns the notation based off an index"""
        return self.board_notation[index[0]][index[1]]
    
    
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
            return False
        last_moved_piece = self.board[self.get_index_via_notation(self.player_moves[-1][2:4])[0]][self.get_index_via_notation(self.player_moves[-1][2:4])[1]]
        if last_moved_piece == "Pawn" and self.player_moves[-1][1] == "7" and self.player_moves[-1][3] == "5":
            return True
        else:
            return False


    def if_black_can_enpessant_this_move(self):
        """Returns True if there is a white pawn that has advanced two squares, otherwise returns False."""
        if len(self.player_moves) == 0:
            return False
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
            self.game_ended(end_square_data[1])

    
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


    def set_square_value(self, notation, color = None, piece = None):
        index = self.get_index_via_notation(notation)
        if color != None:
            self.board_color[index[0]][index[1]] = color
        if piece != None:
            self.board[index[0]][index[1]] = piece
        if piece == None and color == None:
            raise TypeError("No square changed")

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
            if self.if_black_can_enpessant_this_move():
                pawn_location = self.get_index_via_notation(self.player_moves[-1][2:4])
                if index[1] - 1 == pawn_location[1] or index[1] + 1 == pawn_location[1]:
                    moves.append((pawn_location[0] - 1, pawn_location[1]))
            # Checking if the pawn can take
            if index[1] != 7 and self.board_color[index[0] - 1][index[1] + 1] == "white":
                moves.append((index[0] - 1, index[1] + 1))
            if index[1] != 0 and self.board_color[index[0] - 1][index[1] - 1] == "white":
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


    def get_seeing_as_rook_at(self, notation):
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


    def get_seeing_as_queen_at(self, notation):
        return [*self.get_seeing_as_rook_at(notation), *self.get_seeing_as_bishop_at(notation)]

    
    def get_seeing_as_knight_at(self, notation):
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


    def get_seeing_as_king(self, notation):
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


    def get_legal_as_king(self, notation):
        """Returns all possible legal moves as a king from a certain square (the passed in notation)."""
        # Getting all "typical" (moving to all adjacent squares) king moves
        moves = [*self.get_seeing_as_king(notation)]
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
    
    
    def get_piece_seeing(self, notation):
        import types
        """Checks the value of square (gotten from notation), then gets what that piece sees (via checking the value of the square, then running that piece's respective function to get what it sees)."""
        index = self.get_index_via_notation(notation)
        piece = self.get_square_value(notation)[0]
        piece_color = self.board_color[index[0]][index[1]]
        moves = []
        if piece == "Knight":
            moves = self.get_seeing_as_knight_at(notation)
        if piece == "King":
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
        for i in range(len(self.board)):
            for n in range(len(self.board[i])):
                self.board[i][n] = None


    def get_pieces_seeing(self, notation, color = None):
        """Returns the squares off all pieces seeing a certain square (the square in question is gotten from notation), color removes all pieces that are not of one color"""
        pieces_locations = []
        for i in range(8):
            for n in range(8):
                try:
                    if self.get_piece_seeing(self.get_notation_via_index((i, n))).index(notation) != None:
                        pieces_locations.append(self.get_notation_via_index((i, n)))
                except:
                    pass
        if color != None:
            i2 = 0
            for i in range(len(pieces_locations)):
                if self.get_square_value(pieces_locations[i2])[1] != color:
                    del pieces_locations[i2]
                    i2 -= 1
                i2 += 1
        return pieces_locations


    def get_legal_moves(self, notation):
        import types
        """Returns all legal moves of a piece on a specific square (gotten via notation) (The moves are obtained by either getting what squares a piece sees, then vetting all the moves to remove the squares it cannot move to. Or uses the respective function to calculate that piece's legal moves)."""
        if notation[0] == "o": # Checks if the move is castling. (otherwise you get an error)
            piece = "King"
        else:
            piece = self.get_square_value(notation)[0]
        if piece == "Pawn":
            moves = self.get_legal_as_pawn_at(notation)
        elif piece == "King":
            moves = self.get_legal_as_king(notation)
        else:
            moves = self.get_piece_seeing(notation)
        # Changes all squares to indexs
        if type(moves) != types.NoneType:
            for i in range(len(moves)):
                if moves[i] != "o-o" and moves[i] != "o-o-o":
                    moves[i] = self.get_index_via_notation(moves[i])
            # Checking if any squares are "illegal"
            i2 = 0
            for i in range(len(moves)):
                if moves[i2] != "o-o" and moves[i2] != "o-o-o":
                    if moves[i2][0] < 0 or moves[i2][0] > 7 or moves[i2][1] < 0 or moves[i2][1] > 7 or self.get_square_value(notation)[1] == self.board_color[moves[i2][0]][moves[i2][1]]:
                        del moves[i2]
                        i2 -= 1
                i2 += 1
            for i in range(len(moves)):
                if moves[i] != "o-o" and moves[i] != "o-o-o":
                    moves[i] = self.get_notation_via_index(moves[i])
        return moves


    def who_to_move(self):
        """Returns a string containing either 'white' or 'black' based off which player's turn it is to move."""
        if len(self.player_moves) == 0 or self.get_square_value(self.player_moves[-1][2:4])[1] == "black":
            return "white"
        else:
            return "black"


    def legal_move(self, move, raise_error_if_illegal = True):
        """Checks if the move passed in is legal, if so then the move is performed and the function returns True, if it failed one of the checks, the function will return False."""
        # Basic check for illegal moves
        if len(move) < 4 and move != "o-o":
            raise IllegalMove(f"move \"{move}\" is too short")
        if move != "o-o":
            if not int(move[1]) <= 8 or not int(move[1]) >= 1:
                raise IllegalMove(f"move \"{move}\" contains illegal square(s)")
            if not int(move[3]) <= 8 or not int(move[3]) >= 1:
                raise IllegalMove(f"move \"{move}\" contains illegal square(s)")
        if len(move) > 6:
            raise IllegalMove(f"move \"{move}\" is too long")
        # Checking if the move is castling, and if so skipping normal legal move check procedures (to prevent an error)
        if move[0] == "o":
            # Castling for white
            if self.who_to_move() == "white":
                if self.get_square_value("e1") == ("King", "white"):
                    # Checks if white can legally short castle, then, if so, performs it
                    if self.errorless_index(self.get_legal_as_king("e1"), "o-o") and move == "o-o":
                        # moving the Rook and King
                        self.move("e1g1")
                        self.move("h1f1")
                        # removing castling rights
                        self.white_oo = False
                        self.white_ooo = False
                        return True
                    # Checks if white can legally long castle, then, if so, performs it
                    if self.errorless_index(self.get_legal_as_king("e1"), "o-o-o") and move == "o-o-o":
                        # moving the Rook and King
                        self.move("e1c1")
                        self.move("a1d1")
                        # removing castling rights
                        self.white_oo = False
                        self.white_ooo = False
                        return True
            else:
                # Castling for black
                if self.get_square_value("e8") == ("King", "black"):
                    # Checks if black can legally short castle, then, if so, performs it
                    if self.errorless_index(self.get_legal_as_king("e8"), "o-o") and move == "o-o":
                        # moving the Rook and King
                        self.move("e8g8")
                        self.move("h8f8")
                        # removing castling rights
                        self.black_oo = False
                        self.black_ooo = False
                        return True
                    # Checks if black can legally long castle, then, if so, performs it
                    if self.errorless_index(self.get_legal_as_king("e8"), "o-o-o") and move == "o-o-o":
                        # moving the Rook and King
                        self.move("e8c8")
                        self.move("a8d8")
                        # removing castling rights
                        self.black_oo = False
                        self.black_ooo = False
                        return True
        # Checks for enpessant (en peasant)
        elif self.get_square_value(move[0:2])[0] == "Pawn" and self.get_square_value(move[2:4])[0] == None and move[0] != move[2] and self.who_to_move() == self.get_square_value(move[0:2])[1] and (self.if_white_can_enpessant_this_move() or self.if_black_can_enpessant_this_move()):
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
        elif self.get_square_value(move[0:2])[0] == "Pawn" and len(move) == 6 and move[4] == "=" and (move[3] == "8" or move[3] == "1"):
            # makes initial move
            self.move(move[0:4])
            # Changes the pawn to the piece its promoting to
            if move[5] == "B":
                self.set_square_value(move[2:4], piece="Bishop")
            elif move[5] == "N":
                self.set_square_value(move[2:4], piece="Knight")
            elif move[5] == "R":
                self.set_square_value(move[2:4], piece="Rook")
            elif move[5] == "Q":
                self.set_square_value(move[2:4], piece="Queen")
        else:
            if self.errorless_index(self.get_legal_moves(move[0:2]), move[2:4]) != None and self.get_square_value(move[0:2])[1] == self.who_to_move():
                self.move(move)
                return True
        if raise_error_if_illegal:
            raise IllegalMove(f"move \"{move}\" is illegal")
        else:
            return False


    def legal_moves(self, moves):
        """Performs multiple legal moves passed in as a list or tuple"""
        returning = []
        for i in range(len(moves)):
            returning.append(self.legal_move(moves[i]))
        return returning
class Display:
    import pygame, math
    def __init__(self, square_one_color = (125, 148, 93), square_two_color = (238, 238, 213), screen_size = (700, 700), background = (0, 0, 0), if_view_from_whites_perspective = True, grid_lines_size = 0, square_selection_color = (255, 255, 0), allow_moves_as_opposite_colored_player = False):
        import pygame
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
        self.board_notation = []
        if if_view_from_whites_perspective:
            self.board_notation = self.board_notation_white
        else:
            self.board_notation = self.board_notation_black
        # Defining variables - Math for scaling
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
        # Initializing pygame modules - defining the screen
        self.screen = pygame.display.set_mode(screen_size)
        pygame.transform.scale(pygame.image.load("Chess_Piece_Images/DarkPawn.png"), (self.square_edge_size, self.square_edge_size))
        pygame.display.set_caption("Sticky Chess")
    def flip_viewing_angle(self):
        self.view_from_whites_perspective = not self.view_from_whites_perspective
        if self.view_from_whites_perspective:
            self.board_notation = self.board_notation_white
        else:
            self.board_notation = self.board_notation_black
        if self.square_selected_one != None:
            self.square_selected_one = ((self.square_selected_one - 32) * -1) + 32
    def draw_background(self, background = "Nothing entered"):
        """Draws a single color background"""
        # importing modules
        import pygame
        # Checking if nothing entered (then draws a background based off the global background variable)
        if background == "Nothing entered":
            background = self.background
        # Draws a background based off the passed in background color
        else:
            pygame.draw.rect(self.screen, background, pygame.Rect(0, 0, self.screen_size[0], self.screen_size[1]))
    def move_via_click_check(self, board_class):
        """Checks for any squares being clicked, two have been, attempts that move"""
        var = self.allowed_moves_as_opposing_color or ((board_class.who_to_move() == "white" and self.view_from_whites_perspective) or (board_class.who_to_move() == "black" and not self.view_from_whites_perspective))
        if self.get_square_pressed() != None:
            if self.square_selected_one == None:
                self.square_selected_one = self.get_square_pressed()
            elif self.square_selected_one != self.get_square_pressed():
                move = self.board_notation[self.square_selected_one] + self.board_notation[self.get_square_pressed()]
                if move == "e1g1" or move == "e8g8":
                    move = "o-o"
                elif move == "e1c1" or move == "e8c8":
                    move = "o-o-o"
                if var:
                    board_class.legal_move(move, False)
                self.square_selected_one = None
    def get_legal_moves_preview(self, board_class, square_number):
        """Returns all legal moves of a square based of square number"""
        # getting all legal moves as notation
        notation_moves = board_class.get_legal_moves(self.board_notation[square_number])
        # changing all notation to square numbers
        for i in range(len(notation_moves)):
            if notation_moves[i] != "o-o" and notation_moves[i] != "o-o-o":
                notation_moves[i] = self.board_notation.index(notation_moves[i])
            elif notation_moves[i] == "o-o":
                if board_class.who_to_move() == "white":
                    notation_moves[i] = self.board_notation.index("g1")
                else:
                    notation_moves[i] = self.board_notation.index("g8")
            else:
                if board_class.who_to_move() == "white":
                    notation_moves[i] = self.board_notation.index("c1")
                else:
                    notation_moves[i] = self.board_notation.index("c8")
        return notation_moves
    def setup_background_squares(self, show_legal_moves_preview = False, board_class = None):
        """Draws all background squares"""
        # checking if anything needs to be passed in:
        if show_legal_moves_preview and board_class == None:
            raise Exception("If showing legal move previews, board_class needs to be passed in!")
        # importing modules
        import pygame, math
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
            # showing any previews of legal moves (if paramater to do so is true)
            if show_legal_moves_preview and self.square_selected_one != None:
                moves = self.get_legal_moves_preview(board_class, self.square_selected_one)
                # changing castling to show highlighted squares instead
                if board_class.who_to_move() == "white":
                    try:
                        moves[moves.index("o-o")] == "g1"
                    except:
                        try:
                            moves[moves.index("o-o-o")] == "c1"
                        except:
                            pass
                else:
                    try:
                        moves[moves.index("o-o")] == "g8"
                    except:
                        try:
                            moves[moves.index("o-o-o")] == "c8"
                        except:
                            pass
                # checking if the correct piece is moving, and is allowed to be moved by this player
                if (self.allowed_moves_as_opposing_color or ((board_class.who_to_move() == "white" and self.view_from_whites_perspective) or (board_class.who_to_move() == "black" and not self.view_from_whites_perspective))) and board_class.who_to_move() == board_class.get_square_value(self.board_notation[self.square_selected_one])[1]:
                    try:
                        if moves.index(i) != None:
                            # drawing the circle
                            pygame.draw.circle(self.screen, (128, 128, 128), (self.drawn_background_squares[-1][0] + (self.square_edge_size / 2), self.drawn_background_squares[-1][1] + (self.square_edge_size / 2)), 30)
                    except:
                        pass
    def draw_pieces(self, board_class, whites_point_of_view = True):
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
    def update_screen(self, board, show_legal_moves_from_selected_piece = False):
        """Updates the screen"""
        import pygame
        self.draw_background()
        self.setup_background_squares(show_legal_moves_from_selected_piece, board)
        self.draw_pieces(board, self.view_from_whites_perspective)
        self.move_via_click_check(board)
        pygame.display.flip()
    def get_square_pressed(self):
        """Returns an index of which square is being pressed, if none are, None is returned"""
        # importing modules
        import pygame, math
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