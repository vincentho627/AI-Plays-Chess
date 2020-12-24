import numpy as np

from Pieces import piecePoints

cache = dict()


class Value:
    def __init__(self, value):
        self.value = value
        self.used = True

    def setUsed(self):
        self.used = True


def getDifference(whitePieces, blackPieces):
    value = whitePieces.getPoints() - blackPieces.getPoints()
    return value


def getValue(e):
    if e is None:
        return 0
    else:
        index = 1
        if e.getColor() == 'b':
            index = -1
        return index * piecePoints[e.getName()]


vectorisedGetValue = np.vectorize(getValue)


def getCacheValue(board):
    mappedList = map(lambda x: tuple(vectorisedGetValue(x)), board)
    return tuple(mappedList)


def findNextMove(whitePieces, blackPieces, depth, board):
    bestMove = None
    bestValue = 1300
    alpha = -5000
    beta = 5000
    for pieceList in blackPieces.getPieces():
        for piece in pieceList:
            if piece.alive:
                for (x, y) in piece.showOptions(board, whitePieces, blackPieces, True):
                    removed = False
                    temp_piece = None
                    new_board = np.copy(board)
                    oldX, oldY = piece.getPosition()
                    new_board[oldY][oldX] = None
                    if new_board[y][x] is not None:
                        temp_piece = new_board[y][x]
                        whitePieces.remove(new_board[y][x])
                        removed = True
                    new_board[y][x] = piece
                    piece.setPosition(x, y)
                    cacheValue = getCacheValue(new_board)
                    if cacheValue in cache:
                        v = cache[cacheValue]
                        value = v.value
                        v.setUsed()
                    else:
                        v = miniMax(whitePieces, blackPieces, depth - 1, new_board, alpha, beta, True)
                        value = v.value
                    if bestValue > value:
                        bestValue = value
                        beta = value
                        bestMove = ((oldX, oldY), (x, y))
                    if removed:
                        new_board[y][x] = temp_piece
                        whitePieces.add(temp_piece)
                    new_board[oldY][oldX] = piece
                    piece.setPosition(oldX, oldY)

                    if beta <= alpha:
                        return beta

    # Clear up unnecessary cache items
    delete = []
    for key in cache.keys():
        value = cache[key]
        if value.used:
            value.used = False
        else:
            delete.append(key)

    for key in delete:
        del cache[key]

    return bestValue, bestMove


def miniMax(whitePieces, blackPieces, depth, board, alpha, beta, maxing):
    if depth == 0:
        # return points
        value = getDifference(whitePieces, blackPieces)
        return Value(value)

    if maxing:
        # want white to win
        bestValue = getDifference(whitePieces, blackPieces)

        for pieceList in whitePieces.getPieces():
            for piece in pieceList:
                if piece.alive:
                    for (x, y) in piece.showOptions(board, whitePieces, blackPieces, False):
                        removed = False
                        temp_piece = None
                        special_case = False
                        new_board = np.copy(board)

                        oldX, oldY = piece.getPosition()
                        new_board[oldY][oldX] = None
                        if new_board[y][x] is not None:
                            temp_piece = new_board[y][x]
                            if temp_piece.start and temp_piece.getName() == "Rook" and piece.getName() == "King" \
                                    and piece.start:
                                if x == 7:
                                    new_board[y][x - 1] = piece
                                    new_board[y][oldX + 1] = temp_piece
                                    temp_piece.setPosition(oldX + 1, y)
                                    piece.setPosition(x - 1, y)
                                    piece.started()
                                    temp_piece.started()
                                    special_case = True
                                elif x == 0:  # x == 0
                                    new_board[y][x + 2] = piece
                                    new_board[y][oldX - 1] = temp_piece
                                    temp_piece.setPosition(oldX - 1, y)
                                    piece.setPosition(x + 2, y)
                                    piece.started()
                                    temp_piece.started()
                                    special_case = True
                            elif temp_piece.start and temp_piece.getName() == "King" and piece.getName() == "Rook" \
                                    and piece.start:
                                if oldX == 7:
                                    new_board[y][oldX - 1] = temp_piece
                                    new_board[y][x + 1] = piece
                                    temp_piece.setPosition(oldX - 1, y)
                                    piece.setPosition(x + 1, y)
                                    piece.started()
                                    temp_piece.started()
                                    special_case = True
                                elif oldX == 0:  # oldX == 0
                                    new_board[y][oldX + 2] = temp_piece
                                    new_board[y][x - 1] = piece
                                    temp_piece.setPosition(oldX + 2, y)
                                    piece.setPosition(x - 1, y)
                                    piece.started()
                                    temp_piece.started()
                                    special_case = True
                            else:
                                blackPieces.remove(temp_piece)
                                removed = True
                                new_board[y][x] = piece
                                piece.setPosition(x, y)
                        else:
                            new_board[y][x] = piece
                            piece.setPosition(x, y)

                        cacheValue = getCacheValue(new_board)
                        if cacheValue in cache:
                            v = cache[cacheValue]
                            value = v.value
                            v.setUsed()
                        else:
                            v = miniMax(whitePieces, blackPieces, depth - 1, new_board, alpha, beta, False)
                            value = v.value

                        if special_case:
                            new_board[y][x] = temp_piece
                            temp_piece.setPosition(x, y)
                            temp_piece.start = True
                            piece.start = True
                            value += 10

                        bestValue = max(bestValue, value)
                        alpha = max(alpha, bestValue)

                        # resetting back to original states
                        if removed:
                            new_board[y][x] = temp_piece
                            blackPieces.add(temp_piece)
                        new_board[oldY][oldX] = piece
                        piece.setPosition(oldX, oldY)

                        if beta <= alpha:
                            return Value(alpha)

        cacheValue = getCacheValue(board)
        result = Value(bestValue)
        cache[cacheValue] = result
        return result

    else:
        # want black to win
        bestValue = getDifference(whitePieces, blackPieces)

        for pieceList in blackPieces.getPieces():
            for piece in pieceList:
                if piece.alive:
                    for (x, y) in piece.showOptions(board, whitePieces, blackPieces, True):
                        removed = False
                        temp_piece = None
                        new_board = np.copy(board)
                        special_case = False
                        oldX, oldY = piece.getPosition()
                        new_board[oldY][oldX] = None
                        if new_board[y][x] is not None:
                            temp_piece = new_board[y][x]
                            if temp_piece.start and temp_piece.getName() == "Rook" and piece.getName() == "King" \
                                    and piece.start:
                                if x == 7:
                                    new_board[y][x - 1] = piece
                                    new_board[y][oldX + 1] = temp_piece
                                    temp_piece.setPosition(oldX + 1, y)
                                    piece.setPosition(x - 1, y)
                                    piece.started()
                                    temp_piece.started()
                                    special_case = True
                                else:  # x == 0
                                    new_board[y][x + 2] = piece
                                    new_board[y][oldX - 1] = temp_piece
                                    temp_piece.setPosition(oldX - 1, y)
                                    piece.setPosition(x + 2, y)
                                    piece.started()
                                    temp_piece.started()
                                    special_case = True
                            elif temp_piece.start and temp_piece.getName() == "King" and piece.getName() == "Rook" \
                                    and piece.start:
                                if oldX == 7:
                                    new_board[y][oldX - 1] = temp_piece
                                    new_board[y][x + 1] = piece
                                    temp_piece.setPosition(oldX - 1, y)
                                    piece.setPosition(x + 1, y)
                                    piece.started()
                                    temp_piece.started()
                                    special_case = True
                                else:  # oldX == 0
                                    new_board[y][oldX + 2] = temp_piece
                                    new_board[y][x - 1] = piece
                                    temp_piece.setPosition(oldX + 2, y)
                                    piece.setPosition(x - 1, y)
                                    piece.started()
                                    temp_piece.started()
                                    special_case = True
                            else:
                                whitePieces.remove(new_board[y][x])
                                removed = True
                                new_board[y][x] = piece
                                piece.setPosition(x, y)
                        else:
                            new_board[y][x] = piece
                            piece.setPosition(x, y)

                        cacheValue = getCacheValue(new_board)
                        if cacheValue in cache:
                            v = cache[cacheValue]
                            value = v.value
                            v.setUsed()
                        else:
                            v = miniMax(whitePieces, blackPieces, depth - 1, new_board, alpha, beta, True)
                            value = v.value

                        if special_case:
                            new_board[y][x] = temp_piece
                            temp_piece.setPosition(x, y)
                            temp_piece.start = True
                            piece.start = True
                            value -= 10

                        bestValue = min(bestValue, value)
                        beta = min(beta, bestValue)

                        # resetting back to original states
                        if removed:
                            new_board[y][x] = temp_piece
                            whitePieces.add(temp_piece)
                        new_board[oldY][oldX] = piece
                        piece.setPosition(oldX, oldY)

                        if beta <= alpha:
                            return Value(beta)

        cacheValue = getCacheValue(board)
        result = Value(bestValue)
        cache[cacheValue] = result
        return result

# if __name__ == '__main__':
#     board = np.empty([8, 8], dtype=ChessPiece)
#     wp = White()
#     bp = Black()
#     k = initialisePieces(wp, bp, board)
#     print(getCacheValue(k))
