import random
board = [["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"],
         ["Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn"],
         [None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None],
         ["Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn"],
         ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]]
board_color = [["white", "white", "white", "white", "white", "white", "white", "white"],
               ["white", "white", "white", "white", "white", "white", "white", "white"],
               [None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None],
               ["black", "black", "black", "black", "black", "black", "black", "black"],
               ["black", "black", "black", "black", "black", "black", "black", "black"]]
sticky = [[0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0]]
board_notation = [["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"],
                  ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
                  ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
                  ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
                  ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
                  ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
                  ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
                  ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]]
white_oo = True
white_ooo = True
black_oo = True
black_ooo = True
def getnotationviaindex(index):
    return board_notation[index[0]][index[1]]
def getindexvianotation(notation):
    return((("a", "b", "c", "d", "e", "f", "g", "h").index(notation[0]), int(notation[1]) - 1))


def getsquarevalue(notation):
    return (board[getindexvianotation(notation)[0]][getindexvianotation(notation)[1]], board_color[getindexvianotation(notation)[0]][getindexvianotation(notation)[1]])


def delsquare(notation):
    if type(notation) == str:
        notation = [notation]
    for i in range(len(notation)):
        index = getindexvianotation(notation[i])
        board[index[0]][index[1]] = None
        board_color[index[0]][index[1]] = None


def squareempty(notation):
    if getsquarevalue(notation) == (None, None):
        return True
    else:
        return False


def squaresempty(notations):
    true = True
    for i in range(len(notations)):
        if getsquarevalue(notations[i]) != (None, None) and true:
            true = False
    return true


def getlegalmoves(notation):
    index = getindexvianotation(notation)
    piece = board[index[0]][index[1]]
    piece_color = board_color[index[0]][index[1]]
    moves = []
    if piece == "Knight":
        moves.append((index[0] - 1, index[1] - 2))
        moves.append((index[0] - 1, index[1] + 2))
        moves.append((index[0] - 2, index[1] - 1))
        moves.append((index[0] + 2, index[1] - 1))
        moves.append((index[0] - 2, index[1] + 1))
        moves.append((index[0] + 2, index[1] + 1))
        moves.append((index[0] - 1, index[1] + 2))
        moves.append((index[0] + 1, index[1] + 2))
    if piece == "King":
        moves.append((index[0] - 1, index[1] - 1))
        moves.append((index[0] - 1, index[1] + 1))
        moves.append((index[0] + 1, index[1] + 1))
        moves.append((index[0] + 1, index[1] - 1))
        moves.append((index[0], index[1] + 1))
        moves.append((index[0], index[1] - 1))
        moves.append((index[0] - 1, index[1]))
        moves.append((index[0] + 1, index[1]))
        if piece_color == "white":
            if white_oo and squaresempty(("f1", "g1")):
                moves.append("o-o")
            if white_ooo and squaresempty(("b1", "c1", "d1")):
                moves.append("o-o-o")
        else:
            if black_oo and squaresempty(("f8", "g8")):
                moves.append("o-o")
            if black_ooo and squaresempty(("b8", "c8", "d8")):
                moves.append("o-o-o")


    elif piece == "Rook":
        # check the row for pieces in the way of moving:
        # starts at piece, goes until it reaches -1:
        for i in range(index[0] -1, -1, -1):
            if board[i][index[1]] == None:
                moves.append((i, index[1]))
            else:
                break
        # starts at piece, go until it reaches 8:
        for i in range(index[0] + 1, 7, + 1):
            if board[i][index[1]] == None:
                moves.append((i, index[1]))
            else:
                break
        # checks the column for pieces in way of moving
        # starts at piece, goes until it reaches -1
        for i in range(index[1] -1, -1, -1):
            if board[index[0]][i] == None:
                moves.append((index[0], i))
            else:
                break
        # starts at piece, go until it reaches 8:
        for i in range(index[1] + 1, 7, + 1):
            if board[index[0]][i] == None:
                moves.append((index[1], i))
            else:
                break
    elif piece == "Bishop":
        # checks the diagonals from the bishop to the edges in each direction until there is a piece:
        # negative, negative:
        spot = (index[0] - 1, index[1] - 1)
        while(spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] - 1, spot[1] - 1)
            else:
                break
        # negative, positive
        spot = (index[0] - 1, index[1] + 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] - 1, spot[1] + 1)
            else:
                break
        # positive, positive
        spot = (index[0] + 1, index[1] + 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] + 1, spot[1] + 1)
            else:
                break
        # positive, negative
        spot = (index[0] + 1, index[1] - 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] + 1, spot[1] - 1)
            else:
                break
    elif piece == "Queen":
        # Copied from rook
        # check the row for pieces in the way of moving:
        # starts at piece, goes until it reaches -1:
        for i in range(index[0] - 1, -1, -1):
            if board[i][index[1]] == None:
                moves.append((i, index[1]))
            else:
                break
        # starts at piece, go until it reaches 8:
        for i in range(index[0] + 1, 7, + 1):
            if board[i][index[1]] == None:
                moves.append((i, index[1]))
            else:
                break
        # checks the column for pieces in way of moving:
        # starts at piece, goes until it reaches -1:
        for i in range(index[1] - 1, -1, -1):
            if board[index[0]][i] == None:
                moves.append((index[0], i))
            else:
                break
        # starts at piece, go until it reaches 8:
        for i in range(index[1] + 1, 7, + 1):
            if board[index[0]][i] == None:
                moves.append((index[1], i))
            else:
                break
        # Copied from bishop
        # checks the diagnols from the bishop to the edges in each direction until there is a piece:
        # negative, negative:
        spot = (index[0] - 1, index[1] - 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] - 1, spot[1] - 1)
            else:
                break
        # negative, positive
        spot = (index[0] - 1, index[1] + 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] - 1, spot[1] + 1)
            else:
                break
        # positive, positive
        spot = (index[0] + 1, index[1] + 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] + 1, spot[1] + 1)
            else:
                break
        # positive, negative
        spot = (index[0] + 1, index[1] - 1)
        while (spot[0] != -1 and spot[1] != -1 and spot[0] != 8 and spot[1] != 8):
            if board[spot[0]][spot[1]] == None:
                moves.append(spot)
                spot = (spot[0] + 1, spot[1] - 1)
            else:
                break
    elif piece == "Pawn":
        if board_color[index[0]][index[1]] == "white":
            if index[1] == 2 and board[index[0]][index[1] + 1] == None:
                moves.append((index[0], index[1] + 1))
                moves.append((index[0], index[1] + 2))
            else:
                moves.append((index[0], index[1] + 1))
            try:
                if board_color[index[0] - 1][index[1] + 1] == "black":
                    moves.append((index[0] - 1, index[1] + 1))
            except:
                pass
            try:
                if board_color[index[0] + 1][index[1] + 1] == "back":
                    moves.append((index[0] + 1, index[1] + 1))
            except:
                pass
        else:
            if index[1] == 8 and board[index[0]][index[1] - 1] == None:
                moves.append((index[0], index[1] - 1))
                moves.append((index[0], index[1] - 2))
            else:
                moves.append((index[0], index[1] - 1))
            try:
                if board_color[index[0] - 1][index[1] - 1] == "white":
                    moves.append((index[0] - 1, index[1] - 1))
            except:
                pass
            try:
                if board_color[index[0] + 1][index[1] - 1] == "white":
                    moves.append((index[0] + 1, index[1] - 1))
            except:
                pass
    for i in range(len(moves) - 1, -1, -1):
        if moves[i][0] < 0 or moves[i][0] > 7 or moves[i][1] < 0 or moves[i][1] > 7 or board_color[moves[i][0]][moves[i][1]] == piece_color:
            del moves[i]
    for i in range(len(moves)):
        moves[i] = getnotationviaindex(moves[i])
    return moves


def getpiecesseeing(notation):
    seeing = []
    index = getindexvianotation(notation)
    for a in range(len(board)):
        for b in range(len(board[a])):
            try:
                if board[a][b] != None and getlegalmoves(board_notation[a][b].index(notation)):
                    seeing.append(board_notation[a][b])
            except:
                pass
    return seeing
print(("a", "b").index("a"))
print(getpiecesseeing("a2"))
delsquare(("d2", "c2", "e2"))
print(getlegalmoves("g1"))





