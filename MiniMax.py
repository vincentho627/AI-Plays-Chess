import numpy as np


def getDifference(whitePieces, blackPieces):
    return whitePieces.getPoints() - blackPieces.getPoints()


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
                    # for i in range(len(board)):
                    #     new_board[i] = board[i].copy()
                    oldX, oldY = piece.getPosition()
                    new_board[oldY][oldX] = None
                    if new_board[y][x] is not None:
                        temp_piece = new_board[y][x]
                        whitePieces.remove(new_board[y][x])
                        removed = True
                    new_board[y][x] = piece
                    piece.setPosition(x, y)
                    value = miniMax(whitePieces, blackPieces, depth - 1, new_board, alpha, beta, True)
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

    return bestValue, bestMove


def miniMax(whitePieces, blackPieces, depth, board, alpha, beta, maxing):
    if depth == 0:
        # return points
        return getDifference(whitePieces, blackPieces)

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
                                elif x == 0:   # x == 0
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

                        value = miniMax(whitePieces, blackPieces, depth - 1, new_board, alpha, beta, False)
                        bestValue = max(bestValue, value)
                        alpha = max(alpha, bestValue)

                        if special_case:
                            new_board[y][x] = temp_piece
                            temp_piece.setPosition(x, y)
                            temp_piece.start = True
                            piece.start = True

                        # resetting back to original states
                        if removed:
                            new_board[y][x] = temp_piece
                            blackPieces.add(temp_piece)
                        new_board[oldY][oldX] = piece
                        piece.setPosition(oldX, oldY)

                        if beta <= alpha:
                            return alpha

        return bestValue

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

                        value = miniMax(whitePieces, blackPieces, depth - 1, new_board, alpha, beta, True)
                        bestValue = min(bestValue, value)
                        beta = min(beta, bestValue)

                        if special_case:
                            new_board[y][x] = temp_piece
                            temp_piece.setPosition(x, y)
                            temp_piece.start = True
                            piece.start = True

                        # resetting back to original states
                        if removed:
                            new_board[y][x] = temp_piece
                            whitePieces.add(temp_piece)
                        new_board[oldY][oldX] = piece
                        piece.setPosition(oldX, oldY)

                        if beta <= alpha:
                            return beta

        return bestValue


# if __name__ == '__main__':
#     w = White()
#     b = Black()
#     bo = [[None] * 8 for _ in range(8)]
#     bo = initialisePieces(w, b, bo)
#     v, m = findNextMove(w, b, 2, bo, False)
#     print(v)
#     print(m)
#     print(bo)
