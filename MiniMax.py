# from Chess import initialisePieces
from Pieces import White, Black
import numpy as np


def getDifference(whitePieces, blackPieces):
    return whitePieces.getPoints() - blackPieces.getPoints()


def findNextMove(whitePieces, blackPieces, depth, board):
    bestMove = None
    bestValue = 1300
    for pieceList in blackPieces.getPieces():
        for piece in pieceList:
            for (x, y) in piece.showOptions(board):
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
                value = miniMax(whitePieces, blackPieces, depth - 1, new_board, True)
                if bestValue >= value:
                    bestValue = value
                    bestMove = ((oldX, oldY), (x, y))
                if removed:
                    new_board[y][x] = temp_piece
                    whitePieces.add(temp_piece)
                new_board[oldY][oldX] = piece
                piece.setPosition(oldX, oldY)

    return bestValue, bestMove


def miniMax(whitePieces, blackPieces, depth, board, maxing):
    if depth == 0:
        # return points
        return getDifference(whitePieces, blackPieces)

    if maxing:
        # want white to win
        bestValue = getDifference(whitePieces, blackPieces)

        for pieceList in whitePieces.getPieces():
            for piece in pieceList:
                for (x, y) in piece.showOptions(board):
                    removed = False
                    temp_piece = None
                    special_case = False
                    new_board = np.copy(board)

                    oldX, oldY = piece.getPosition()
                    new_board[oldY][oldX] = None
                    if new_board[y][x] is not None:
                        temp_piece = new_board[y][x]
                        if temp_piece.start and temp_piece.getName() == "Rook" and piece.getName() == "King":
                            if x == 7:
                                board[y][x - 1] = piece
                                board[y][oldX + 1] = temp_piece
                                special_case = True
                            else:   # x == 0
                                board[y][x + 2] = piece
                                board[y][oldX - 1] = temp_piece
                                special_case = True
                        elif temp_piece.start and temp_piece.getName() == "King" and piece.getName() == "Rook":
                            if oldX == 7:
                                board[y][oldX - 1] = temp_piece
                                board[y][x + 1] = piece
                                special_case = True
                            else:  # oldX == 0
                                board[y][oldX + 2] = temp_piece
                                board[y][x - 1] = piece
                                special_case = True
                        else:
                            blackPieces.remove(new_board[y][x])
                            removed = True
                            new_board[y][x] = piece
                            piece.setPosition(x, y)
                    else:
                        new_board[y][x] = piece
                        piece.setPosition(x, y)

                    value = miniMax(whitePieces, blackPieces, depth - 1, new_board, False)
                    bestValue = max(bestValue, value)

                    if special_case:
                        board[y][x] = temp_piece
                        board[y][oldX] = piece

                    # resetting back to original states
                    if removed:
                        new_board[y][x] = temp_piece
                        blackPieces.add(temp_piece)
                    new_board[oldY][oldX] = piece
                    piece.setPosition(oldX, oldY)

        return bestValue

    else:
        # want black to win
        bestValue = getDifference(whitePieces, blackPieces)

        for pieceList in blackPieces.getPieces():
            for piece in pieceList:
                for (x, y) in piece.showOptions(board):
                    removed = False
                    temp_piece = None
                    new_board = np.copy(board)
                    special_case = False

                    oldX, oldY = piece.getPosition()
                    new_board[oldY][oldX] = None
                    if new_board[y][x] is not None:
                        temp_piece = new_board[y][x]
                        if temp_piece.start and temp_piece.getName() == "Rook" and piece.getName() == "King":
                            if x == 7:
                                board[y][x - 1] = piece
                                board[y][oldX + 1] = temp_piece
                                special_case = True
                            else:  # x == 0
                                board[y][x + 2] = piece
                                board[y][oldX - 1] = temp_piece
                                special_case = True
                        elif temp_piece.start and temp_piece.getName() == "King" and piece.getName() == "Rook":
                            if oldX == 7:
                                board[y][oldX - 1] = temp_piece
                                board[y][x + 1] = piece
                                special_case = True
                            else:  # oldX == 0
                                board[y][oldX + 2] = temp_piece
                                board[y][x - 1] = piece
                                special_case = True
                        else:
                            blackPieces.remove(new_board[y][x])
                            removed = True
                            new_board[y][x] = piece
                            piece.setPosition(x, y)
                    else:
                        new_board[y][x] = piece
                        piece.setPosition(x, y)

                    value = miniMax(whitePieces, blackPieces, depth - 1, new_board, True)
                    bestValue = min(bestValue, value)

                    if special_case:
                        board[y][x] = temp_piece
                        board[y][oldX] = piece

                    # resetting back to original states
                    if removed:
                        new_board[y][x] = temp_piece
                        whitePieces.add(temp_piece)
                    new_board[oldY][oldX] = piece
                    piece.setPosition(oldX, oldY)

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
