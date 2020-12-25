from concurrent.futures.process import ProcessPoolExecutor

import numpy as np
from copy import deepcopy
from Pieces import piecePoints, White, ChessPiece, Black


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


def findBestValue(pieceList, whitePieces, blackPieces, board, depth, alpha, beta):
    # copy white pieces and black pieces for concurrency
    bestValue = 1300
    bestMove = None
    for piece in pieceList:
        if piece.alive:
            for (x, y) in piece.showOptions(board, whitePieces, blackPieces, True):
                white_copy = deepcopy(whitePieces)
                black_copy = deepcopy(blackPieces)
                piece_copy = black_copy.find(piece)

                # threads work:
                removed = False
                temp_piece = None
                new_board = np.copy(board)
                oldX, oldY = piece_copy.getPosition()
                new_board[oldY][oldX] = None
                if new_board[y][x] is not None:
                    temp_piece = new_board[y][x]
                    white_copy.remove(new_board[y][x])
                    removed = True
                new_board[y][x] = piece_copy
                piece_copy.setPosition(x, y)
                v = miniMax(white_copy, black_copy, depth - 1, new_board, alpha, beta, True)
                value = v.value
                if removed:
                    new_board[y][x] = temp_piece
                    white_copy.add(temp_piece)
                new_board[oldY][oldX] = piece_copy
                piece_copy.setPosition(oldX, oldY)

                if bestValue > value:
                    bestValue = value
                    # beta = value
                    bestMove = ((oldX, oldY), (x, y))

    return bestValue, bestMove


def findNextMove(whitePieces, blackPieces, depth, board):
    bestMove = None
    bestValue = 1300
    alpha = -5000
    beta = 5000
    executor = ProcessPoolExecutor(max_workers=6)
    futureList = []

    white_copy = deepcopy(whitePieces)
    black_copy = deepcopy(blackPieces)
    board_copy = deepcopy(board)

    for pieceList in black_copy.getPieces():

        future = executor.submit(findBestValue, pieceList, white_copy, black_copy, board_copy, depth, alpha, beta)
        futureList.append(future)

    while True:
        if futureList[0].running():
            print("Task 1 running")
        if futureList[1].running():
            print("Task 2 running")
        if futureList[2].running():
            print("Task 3 running")
        if futureList[3].running():
            print("Task 4 running")
        if futureList[4].running():
            print("Task 5 running")
        if futureList[5].running():
            print("Task 6 running")

        if (futureList[0].done() and futureList[1].done() and futureList[2].done() and futureList[3].done()
                and futureList[4].done() and futureList[5].done()):
            print(futureList[0].result(), futureList[1].result(), futureList[2].result(), futureList[3].result(),
                  futureList[4].result(), futureList[5].result())
            break

    for future in futureList:
        value, move = future.result()

        if bestValue > value:
            bestValue = value
            bestMove = move

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

                        if depth == 3:
                            # for concurrency, every thread will have its own unique blackPieces and whitePieces to
                            # change so that there will be no race conditions
                            # we copy at 3 since we assume the initial depth is 4
                            black_copy = deepcopy(blackPieces)
                        else:
                            black_copy = blackPieces

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
                                black_copy.remove(temp_piece)
                                removed = True
                                new_board[y][x] = piece
                                piece.setPosition(x, y)
                        else:
                            new_board[y][x] = piece
                            piece.setPosition(x, y)

                        v = miniMax(whitePieces, black_copy, depth - 1, new_board, alpha, beta, False)
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
                            black_copy.add(temp_piece)
                        new_board[oldY][oldX] = piece
                        piece.setPosition(oldX, oldY)

                        if beta <= alpha:
                            return Value(alpha)

        result = Value(bestValue)
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

        result = Value(bestValue)
        return result


if __name__ == '__main__':
    board = np.empty([8, 8], dtype=ChessPiece)
    wp = White()
    bp = Black()
    # k = initialisePieces(wp, bp, board)
    b_copy = deepcopy(bp)
    print(b_copy)
