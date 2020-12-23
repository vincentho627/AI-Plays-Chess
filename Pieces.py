import pygame
import numpy as np

getEnemy = {'w': 'b', 'b': 'w'}
piecePoints = {"King": 900, "Queen": 90, "Bishop": 30, "Knight": 30,
                    "Rook": 50, "Pawn": 10}

pawnPoints = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0.5, 1, 1, -2, -2, 1, 1, 0.5],
    [0.5, -0.5, -1, 0, 0, -1, 0.5, 0.5],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

knightPoints = [
    [-5, -4, -3, -3, -3, -4, -5],
    [-4, -2, 0, 0, 0, 0, -2, -4],
    [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
    [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
    [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
    [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
    [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
    [-5, -4, -3, -3, -3, -3, -4, -5]
]

rookPoints = [
    [0, 0, 0, 0.5, 0.5, 0, 0, 0],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [0.5, 1, 1, 1, 1, 1, 1, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

bishopPoints = [
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
    [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
    [-1, 0, 1, 1, 1, 1, 0, -1],
    [-1, 1, 1, 1, 1, 1, 1, -1],
    [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]
]

queenPoints = [
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
    [-1, 0, 0.5, 0, 0, 0, 0, -1],
    [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
]

kingPoints = [
    [2, 3, 1, 0, 0, 1, 3, 2],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
]


class Player:

    def __init__(self):
        self.points = 0
        self.king = None
        self.queen = None
        self.bishop = None
        self.knight = None
        self.rook = None
        self.pawn = None
        self.pieceCount = 16
        self.pieces = None

    def getKing(self):
        if self.king:
            return self.king[0]
        return None

    def getPieces(self):
        if self.pieces is not None:
            return self.pieces.values()

    def getPoints(self):
        points = 0
        for pawn in self.pawn:
            if pawn.alive:
                x, y = pawn.getPosition()
                if pawn.getColor() == 'w':
                    points += piecePoints["Pawn"] + pawnPoints[y][x]
                else:
                    points += piecePoints["Pawn"] + pawnPoints[7 - y][x]
        for rook in self.rook:
            if rook.alive:
                x, y = rook.getPosition()
                if rook.getColor() == 'w':
                    points += piecePoints["Rook"] + rookPoints[y][x]
                else:
                    points += piecePoints["Rook"] + rookPoints[7 - y][x]
        for knight in self.knight:
            if knight.alive:
                x, y = knight.getPosition()
                if knight.getColor() == 'w':
                    points += piecePoints["Knight"] + knightPoints[y][x]
                else:
                    points += piecePoints["Knight"] + knightPoints[7 - y][x]
        for bishop in self.bishop:
            if bishop.alive:
                x, y = bishop.getPosition()
                if bishop.getColor() == 'w':
                    points += piecePoints["Bishop"] + bishopPoints[y][x]
                else:
                    points += piecePoints["Bishop"] + bishopPoints[7 - y][x]
        for queen in self.queen:
            if queen.alive:
                x, y = queen.getPosition()
                if queen.getColor() == 'w':
                    points += piecePoints["Queen"] + queenPoints[y][x]
                else:
                    points += piecePoints["Queen"] + queenPoints[7 - y][x]
        for king in self.king:
            if king.alive:
                x, y = king.getPosition()
                if king.getColor() == 'w':
                    points += piecePoints["King"] + kingPoints[y][x]
                else:
                    points += piecePoints["King"] + kingPoints[7 - y][x]
        return points

    def put_On_Board(self, board):
        for pawn in self.pawn:
            x, y = pawn.getPosition()
            board[y][x] = pawn
        for rook in self.rook:
            x, y = rook.getPosition()
            board[y][x] = rook
        for knight in self.knight:
            x, y = knight.getPosition()
            board[y][x] = knight
        for bishop in self.bishop:
            x, y = bishop.getPosition()
            board[y][x] = bishop
        for queen in self.queen:
            x, y = queen.getPosition()
            board[y][x] = queen
        for king in self.king:
            x, y = king.getPosition()
            board[y][x] = king

        return board

    def seeCheck(self, x, y, board):
        # takes in opponent's king position
        for pawn in self.pawn:
            if pawn.alive:
                if (x, y) in pawn.showOptions(board, None, None, False):
                    return True
        for rook in self.rook:
            if rook.alive:
                if (x, y) in rook.showOptions(board, None, None, False):
                    return True
        for knight in self.knight:
            if knight.alive:
                if (x, y) in knight.showOptions(board, None, None, False):
                    return True
        for bishop in self.bishop:
            if bishop.alive:
                if (x, y) in bishop.showOptions(board, None, None, False):
                    return True
        for queen in self.queen:
            if queen.alive:
                if (x, y) in queen.showOptions(board, None, None, False):
                    return True
        for king in self.king:
            if king.alive:
                if (x, y) in king.showOptions(board, None, None, False):
                    return True
        return False

    def add(self, chessPiece):
        chessPiece.setLive()
        self.pieceCount += 1

    def remove(self, chessPiece):
        chessPiece.setDied()
        self.pieceCount -= 1


class White(Player):
    def __init__(self):
        super().__init__()
        self.pawn = [Pawn(i, 1, 'w') for i in range(8)]
        self.rook = [Rook(0, 0, 'w'), Rook(7, 0, 'w')]
        self.knight = [Knight(1, 0, 'w'), Knight(6, 0, 'w')]
        self.bishop = [Bishop(2, 0, 'w'), Bishop(5, 0, 'w')]
        self.queen = [Queen(3, 0, 'w')]
        self.king = [King(4, 0, 'w')]
        self.pieceCount = 16
        self.pieces = {"King": self.king, "Queen": self.queen, "Bishop": self.bishop, "Knight": self.knight,
                       "Rook": self.rook, "Pawn": self.pawn}


class Black(Player):
    def __init__(self):
        super().__init__()
        self.pawn = [Pawn(i, 6, 'b') for i in range(8)]
        self.rook = [Rook(0, 7, 'b'), Rook(7, 7, 'b')]
        self.knight = [Knight(1, 7, 'b'), Knight(6, 7, 'b')]
        self.bishop = [Bishop(2, 7, 'b'), Bishop(5, 7, 'b')]
        self.queen = [Queen(3, 7, 'b')]
        self.king = [King(4, 7, 'b')]
        self.pieceCount = 16
        self.pieces = {"King": self.king, "Queen": self.queen, "Bishop": self.bishop, "Knight": self.knight,
                       "Rook": self.rook, "Pawn": self.pawn}


class ChessPiece(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.start = True
        self.name = ""
        self.alive = True
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 60, abs((480 - 60) - y * 60)

    def setDied(self):
        self.alive = False

    def setLive(self):
        self.alive = True

    def needChecks(self, x, y, arr, whitePieces, blackPieces):
            arr_copy = np.copy(arr)
            arr_copy[y][x] = self
            arr_copy[self.y][self.x] = None
            oldX, oldY = self.x, self.y
            self.setPosition(x, y)
            if self.color == 'w':
                if whitePieces.getKing() is not None:
                    x, y = whitePieces.getKing().getPosition()
                    if not blackPieces.seeCheck(x, y, arr_copy):
                        self.setPosition(oldX, oldY)
                        return True
            else:
                if blackPieces.getKing() is not None:
                    x, y = blackPieces.getKing().getPosition()
                    if not whitePieces.seeCheck(x, y, arr_copy):
                        self.setPosition(oldX, oldY)
                        return True
            self.setPosition(oldX, oldY)
            return False

    def needChecksNotNone(self, x, y, arr, whitePieces, blackPieces):
        arr_copy = np.copy(arr)
        temp_piece = arr_copy[y][x]
        arr_copy[y][x] = self
        arr_copy[self.y][self.x] = None
        oldX, oldY = self.x, self.y
        self.setPosition(x, y)
        if self.color == 'w':
            blackPieces.remove(temp_piece)
            if whitePieces.getKing() is not None:
                x, y = whitePieces.getKing().getPosition()
                if not blackPieces.seeCheck(x, y, arr_copy):
                    self.setPosition(oldX, oldY)
                    blackPieces.add(temp_piece)
                    return True
            blackPieces.add(temp_piece)
        else:
            whitePieces.remove(temp_piece)
            if blackPieces.getKing() is not None:
                x, y = blackPieces.getKing().getPosition()
                if not whitePieces.seeCheck(x, y, arr_copy):
                    self.setPosition(oldX, oldY)
                    whitePieces.add(temp_piece)
                    return True
            whitePieces.add(temp_piece)
        self.setPosition(oldX, oldY)
        return False

    def isEqual(self, other):
        return self.x == other.x and self.y == other.y and self.name == other.name

    def started(self):
        self.start = False

    def getName(self):
        return self.name

    def getPosition(self):
        return self.x, self.y

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.rect.x, self.rect.y = x * 60, abs((480 - 60) - y * 60)

    def getColor(self):
        return self.color

    def showOptions(self, arr, player1, player2, needCheck):
        pass


class Pawn(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.start = True
        self.name = "Pawn"
        self.sprite = pygame.image.load("assets/{}pawn.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr, whitePieces, blackPieces, needCheck):
        result = []
        if self.color == 'w':
            if 0 <= self.y + 1 < len(arr):
                if arr[self.y + 1][self.x] is None:
                    if needCheck:
                        arr_copy = np.copy(arr)
                        arr_copy[self.y + 1][self.x] = self
                        arr_copy[self.y][self.x] = None
                        oldX, oldY = self.x, self.y
                        self.setPosition(self.x, self.y + 1)
                        if whitePieces.getKing() is not None:
                            x, y = whitePieces.getKing().getPosition()
                            if not blackPieces.seeCheck(x, y, arr_copy):
                                result.append((oldX, oldY + 1))
                        self.setPosition(oldX, oldY)
                    else:
                        result.append((self.x, self.y + 1))
            if 0 <= self.y + 2 < len(arr):
                if self.start and arr[self.y + 2][self.x] is None and arr[self.y + 1][self.x] is None:
                    if needCheck:
                        arr_copy = np.copy(arr)
                        arr_copy[self.y + 2][self.x] = self
                        arr_copy[self.y][self.x] = None
                        oldX, oldY = self.x, self.y
                        self.setPosition(self.x, self.y + 2)
                        if whitePieces.getKing() is not None:
                            x, y = whitePieces.getKing().getPosition()
                            if not blackPieces.seeCheck(x, y, arr_copy):
                                result.append((oldX, oldY + 2))
                        self.setPosition(oldX, oldY)
                    else:
                        result.append((self.x, self.y + 2))
            if 0 <= self.y + 1 < len(arr) and 0 <= self.x + 1 < len(arr):
                if arr[self.y + 1][self.x + 1] is not None:
                    if arr[self.y + 1][self.x + 1].getColor() == 'b':
                        if needCheck:
                            arr_copy = np.copy(arr)
                            temp_piece = arr_copy[self.y + 1][self.x + 1]
                            arr_copy[self.y + 1][self.x + 1] = self
                            arr_copy[self.y][self.x] = None
                            oldX, oldY = self.x, self.y
                            self.setPosition(self.x + 1, self.y + 1)
                            blackPieces.remove(temp_piece)
                            if whitePieces.getKing() is not None:
                                x, y = whitePieces.getKing().getPosition()
                                if not blackPieces.seeCheck(x, y, arr_copy):
                                    result.append((oldX + 1, oldY + 1))
                            blackPieces.add(temp_piece)
                            self.setPosition(oldX, oldY)
                        else:
                            result.append((self.x + 1, self.y + 1))
            if 0 <= self.y + 1 < len(arr) and 0 <= self.x - 1 < len(arr):
                if arr[self.y + 1][self.x - 1] is not None:
                    if arr[self.y + 1][self.x - 1].getColor() == 'b':
                        if needCheck:
                            arr_copy = np.copy(arr)
                            temp_piece = arr_copy[self.y + 1][self.x - 1]
                            arr_copy[self.y + 1][self.x - 1] = self
                            arr_copy[self.y][self.x] = None
                            oldX, oldY = self.x, self.y
                            self.setPosition(self.x - 1, self.y + 1)
                            blackPieces.remove(temp_piece)
                            if whitePieces.getKing() is not None:
                                x, y = whitePieces.getKing().getPosition()
                                if not blackPieces.seeCheck(x, y, arr_copy):
                                    result.append((oldX - 1, oldY + 1))
                            blackPieces.add(temp_piece)
                            self.setPosition(oldX, oldY)
                        else:
                            result.append((self.x - 1, self.y + 1))

        else:
            if arr[self.y - 1][self.x] is None:
                if needCheck:
                    arr_copy = np.copy(arr)
                    arr_copy[self.y - 1][self.x] = self
                    arr_copy[self.y][self.x] = None
                    oldX, oldY = self.x, self.y
                    self.setPosition(self.x, self.y - 1)
                    if blackPieces.getKing() is not None:
                        x, y = blackPieces.getKing().getPosition()
                        if not whitePieces.seeCheck(x, y, arr_copy):
                            result.append((oldX, oldY - 1))
                    self.setPosition(oldX, oldY)
                else:
                    result.append((self.x, self.y - 1))
            if self.start and arr[self.y - 2][self.x] is None and arr[self.y - 1][self.x] is None:
                if needCheck:
                    arr_copy = np.copy(arr)
                    arr_copy[self.y - 2][self.x] = self
                    arr_copy[self.y][self.x] = None
                    oldX, oldY = self.x, self.y
                    self.setPosition(self.x, self.y - 2)
                    if blackPieces.getKing() is not None:
                        x, y = blackPieces.getKing().getPosition()
                        if not whitePieces.seeCheck(x, y, arr_copy):
                            result.append((oldX, oldY - 2))
                    self.setPosition(oldX, oldY)
                else:
                    result.append((self.x, self.y - 2))
            if 0 <= self.y - 1 < len(arr) and 0 <= self.x + 1 < len(arr):
                if arr[self.y - 1][self.x + 1] is not None:
                    if arr[self.y - 1][self.x + 1].getColor() == 'w':
                        if needCheck:
                            arr_copy = np.copy(arr)
                            temp_piece = arr_copy[self.y - 1][self.x + 1]
                            arr_copy[self.y - 1][self.x + 1] = self
                            arr_copy[self.y][self.x] = None
                            oldX, oldY = self.x, self.y
                            self.setPosition(self.x + 1, self.y - 1)
                            whitePieces.remove(temp_piece)
                            if blackPieces.getKing() is not None:
                                x, y = blackPieces.getKing().getPosition()
                                if not whitePieces.seeCheck(x, y, arr_copy):
                                    result.append((oldX + 1, oldY - 1))
                            whitePieces.add(temp_piece)
                            self.setPosition(oldX, oldY)
                        else:
                            result.append((self.x + 1, self.y - 1))
            if 0 <= self.y - 1 < len(arr) and 0 <= self.x - 1 < len(arr):
                if arr[self.y - 1][self.x - 1] is not None:
                    if arr[self.y - 1][self.x - 1].getColor() == 'w':
                        if needCheck:
                            arr_copy = np.copy(arr)
                            temp_piece = arr_copy[self.y - 1][self.x - 1]
                            arr_copy[self.y - 1][self.x - 1] = self
                            arr_copy[self.y][self.x] = None
                            oldX, oldY = self.x, self.y
                            self.setPosition(self.x - 1, self.y - 1)
                            whitePieces.remove(temp_piece)
                            if blackPieces.getKing() is not None:
                                x, y = blackPieces.getKing().getPosition()
                                if not whitePieces.seeCheck(x, y, arr_copy):
                                    result.append((oldX - 1, oldY - 1))
                            whitePieces.add(temp_piece)
                            self.setPosition(oldX, oldY)
                        else:
                            result.append((self.x - 1, self.y - 1))

        return result


class Rook(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.name = "Rook"
        self.sprite = pygame.image.load("assets/{}rook.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr, whitePieces, blackPieces, needCheck):
        result = []

        if self.start:
            # if self.y == 7:
            row = 0
            if self.color == 'b':
                row = 7
            if self.x == 7:
                if arr[row][5] is None and arr[row][6] is None:
                    if arr[row][4] is not None:
                        if arr[row][4].start and arr[row][4].getName() == 'King':
                            if needCheck:
                                temp_piece = arr[row][4]
                                arr[row][4] = None
                                temp_piece.setPosition(6, row)
                                if self.needChecks(5, row, arr, whitePieces, blackPieces):
                                    result.append((4, row))
                                arr[row][4] = temp_piece
                                temp_piece.setPosition(4, row)
                            else:
                                result.append((4, row))
            elif self.x == 0:
                hasNoObstacle = True
                for i in range(1, 4):
                    hasNoObstacle = hasNoObstacle and arr[row][i] is None
                if hasNoObstacle:
                    if arr[row][4] is not None:
                        if arr[row][4].start and arr[row][4].getName() == 'King':
                            if needCheck:
                                temp_piece = arr[row][4]
                                arr[row][4] = None
                                temp_piece.setPosition(2, row)
                                if self.needChecks(3, row, arr, whitePieces, blackPieces):
                                    result.append((4, row))
                                arr[row][4] = temp_piece
                                temp_piece.setPosition(4, row)
                            else:
                                result.append((4, row))

        # Move right
        for i in range(1, len(arr) - self.x):
            if 0 <= self.x + i < len(arr):
                if arr[self.y][self.x + i] is None:
                    if needCheck:
                        if self.needChecks(self.x + i, self.y, arr, whitePieces, blackPieces):
                            result.append((self.x + i, self.y))
                    else:
                        result.append((self.x + i, self.y))
                else:
                    if arr[self.y][self.x + i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x + i, self.y, arr, whitePieces, blackPieces):
                                result.append((self.x + i, self.y))
                        else:
                            result.append((self.x + i, self.y))
                    break

        # Move Left
        for i in range(1, self.x + 1):
            if 0 <= self.x - i < len(arr):
                if arr[self.y][self.x - i] is None:
                    if needCheck:
                        if self.needChecks(self.x - i, self.y, arr, whitePieces, blackPieces):
                            result.append((self.x - i, self.y))
                    else:
                        result.append((self.x - i, self.y))
                else:
                    if arr[self.y][self.x - i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x - i, self.y, arr, whitePieces, blackPieces):
                                result.append((self.x - i, self.y))
                        else:
                            result.append((self.x - i, self.y))
                    break

        # Move Up
        for j in range(1, len(arr) - self.y):
            if 0 <= self.y + j < len(arr):
                if arr[self.y + j][self.x] is None:
                    if needCheck:
                        if self.needChecks(self.x, self.y + j, arr, whitePieces, blackPieces):
                            result.append((self.x, self.y + j))
                    else:
                        result.append((self.x, self.y + j))
                else:
                    if arr[self.y + j][self.x].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x, self.y + j, arr, whitePieces, blackPieces):
                                result.append((self.x, self.y + j))
                        else:
                            result.append((self.x, self.y + j))
                    break

        # Move Down
        for j in range(1, self.y + 1):
            if 0 <= self.y - j < len(arr):
                if arr[self.y - j][self.x] is None:
                    if needCheck:
                        if self.needChecks(self.x, self.y - j, arr, whitePieces, blackPieces):
                            result.append((self.x, self.y - j))
                    else:
                        result.append((self.x, self.y - j))
                else:
                    if arr[self.y - j][self.x].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x, self.y - j, arr, whitePieces, blackPieces):
                                result.append((self.x, self.y - j))
                        else:
                            result.append((self.x, self.y - j))
                    break

        return result


class Knight(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.name = "Knight"
        self.sprite = pygame.image.load("assets/{}knight.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr, whitePieces, blackPieces, needCheck):
        result = []

        if 0 <= self.y + 2 < len(arr) and 0 <= self.x + 1 < len(arr):
            if arr[self.y + 2][self.x + 1] is None:
                if needCheck:
                    if self.needChecks(self.x + 1, self.y + 2, arr, whitePieces, blackPieces):
                        result.append((self.x + 1, self.y + 2))
                else:
                    result.append((self.x + 1, self.y + 2))
            else:
                if arr[self.y + 2][self.x + 1].getColor() == getEnemy[self.color]:
                    if needCheck:
                        if self.needChecksNotNone(self.x + 1, self.y + 2, arr, whitePieces, blackPieces):
                            result.append((self.x + 1, self.y + 2))
                    else:
                        result.append((self.x + 1, self.y + 2))

        if 0 <= self.y + 1 < len(arr) and 0 <= self.x + 2 < len(arr):
            if arr[self.y + 1][self.x + 2] is None:
                if needCheck:
                    if self.needChecks(self.x + 2, self.y + 1, arr, whitePieces, blackPieces):
                        result.append((self.x + 2, self.y + 1))
                else:
                    result.append((self.x + 2, self.y + 1))
            else:
                if arr[self.y + 1][self.x + 2].getColor() == getEnemy[self.color]:
                    if needCheck:
                        if self.needChecksNotNone(self.x + 2, self.y + 1, arr, whitePieces, blackPieces):
                            result.append((self.x + 2, self.y + 1))
                    else:
                        result.append((self.x + 2, self.y + 1))

        if 0 <= self.y - 1 < len(arr) and 0 <= self.x + 2 < len(arr):
            if arr[self.y - 1][self.x + 2] is None:
                if needCheck:
                    if self.needChecks(self.x + 2, self.y - 1, arr, whitePieces, blackPieces):
                        result.append((self.x + 2, self.y - 1))
                else:
                    result.append((self.x + 2, self.y - 1))
            else:
                if arr[self.y - 1][self.x + 2].getColor() == getEnemy[self.color]:
                    if needCheck:
                        if self.needChecksNotNone(self.x + 2, self.y - 1, arr, whitePieces, blackPieces):
                            result.append((self.x + 2, self.y - 1))
                    else:
                        result.append((self.x + 2, self.y - 1))

        if 0 <= self.y - 2 < len(arr) and 0 <= self.x + 1 < len(arr):
            if arr[self.y - 2][self.x + 1] is None:
                if needCheck:
                    if self.needChecks(self.x + 1, self.y - 2, arr, whitePieces, blackPieces):
                        result.append((self.x + 1, self.y - 2))
                else:
                    result.append((self.x + 1, self.y - 2))
            else:
                if arr[self.y - 2][self.x + 1].getColor() == getEnemy[self.color]:
                    if needCheck:
                        if self.needChecksNotNone(self.x + 1, self.y - 2, arr, whitePieces, blackPieces):
                            result.append((self.x + 1, self.y - 2))
                    else:
                        result.append((self.x + 1, self.y - 2))

        if 0 <= self.y + 2 < len(arr) and 0 <= self.x - 1 < len(arr):
            if arr[self.y + 2][self.x - 1] is None:
                if needCheck:
                    if self.needChecks(self.x - 1, self.y + 2, arr, whitePieces, blackPieces):
                        result.append((self.x - 1, self.y + 2))
                else:
                    result.append((self.x - 1, self.y + 2))
            else:
                if arr[self.y + 2][self.x - 1].getColor() == getEnemy[self.color]:
                    if needCheck:
                        if self.needChecksNotNone(self.x - 1, self.y + 2, arr, whitePieces, blackPieces):
                            result.append((self.x - 1, self.y + 2))
                    else:
                        result.append((self.x - 1, self.y + 2))

        if 0 <= self.y + 1 < len(arr) and 0 <= self.x - 2 < len(arr):
            if arr[self.y + 1][self.x - 2] is None:
                if needCheck:
                    if self.needChecks(self.x - 2, self.y + 1, arr, whitePieces, blackPieces):
                        result.append((self.x - 2, self.y + 1))
                else:
                    result.append((self.x - 2, self.y + 1))
            else:
                if arr[self.y + 1][self.x - 2].getColor() == getEnemy[self.color]:
                    if needCheck:
                        if self.needChecksNotNone(self.x - 2, self.y + 1, arr, whitePieces, blackPieces):
                            result.append((self.x - 2, self.y + 1))
                    else:
                        result.append((self.x - 2, self.y + 1))

        if 0 <= self.y - 1 < len(arr) and 0 <= self.x - 2 < len(arr):
            if arr[self.y - 1][self.x - 2] is None:
                if needCheck:
                    if self.needChecks(self.x - 2, self.y - 1, arr, whitePieces, blackPieces):
                        result.append((self.x - 2, self.y - 1))
                else:
                    result.append((self.x - 2, self.y - 1))
            else:
                if arr[self.y - 1][self.x - 2].getColor() == getEnemy[self.color]:
                    if needCheck:
                        if self.needChecksNotNone(self.x - 2, self.y - 1, arr, whitePieces, blackPieces):
                            result.append((self.x - 2, self.y - 1))
                    else:
                        result.append((self.x - 2, self.y - 1))

        if 0 <= self.y - 2 < len(arr) and 0 <= self.x - 1 < len(arr):
            if arr[self.y - 2][self.x - 1] is None:
                if needCheck:
                    if self.needChecks(self.x - 1, self.y - 2, arr, whitePieces, blackPieces):
                        result.append((self.x - 1, self.y - 2))
                else:
                    result.append((self.x - 1, self.y - 2))
            else:
                if arr[self.y - 2][self.x - 1].getColor() == getEnemy[self.color]:
                    if needCheck:
                        if self.needChecksNotNone(self.x - 1, self.y - 2, arr, whitePieces, blackPieces):
                            result.append((self.x - 1, self.y - 2))
                    else:
                        result.append((self.x - 1, self.y - 2))

        return result


class Bishop(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.name = "Bishop"
        self.sprite = pygame.image.load("assets/{}bishop.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr, whitePieces, blackPieces, needCheck):
        result = []
        minMove = min(self.x, self.y)
        maxMove = max(len(arr) - self.x, len(arr) - self.y)

        # Up left
        for i in range(1, abs(len(arr) - minMove)):
            if 0 <= self.y + i < len(arr) and 0 <= self.x - i < len(arr):
                if arr[self.y + i][self.x - i] is None:
                    if needCheck:
                        if self.needChecks(self.x - i, self.y + i, arr, whitePieces, blackPieces):
                            result.append((self.x - i, self.y + i))
                    else:
                        result.append((abs(self.x - i), abs(self.y + i)))
                else:
                    if arr[self.y + i][self.x - i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x - i, self.y + i, arr, whitePieces, blackPieces):
                                result.append((self.x - i, self.y + i))
                        else:
                            result.append((abs(self.x - i), self.y + i))
                    break

        # Down Left
        for i in range(1, minMove + 1):
            if 0 <= self.y - i < len(arr) and 0 <= self.x - i < len(arr):
                if arr[self.y - i][self.x - i] is None:
                    if needCheck:
                        if self.needChecks(self.x - i, self.y - i, arr, whitePieces, blackPieces):
                            result.append((self.x - i, self.y - i))
                    else:
                        result.append((abs(self.x - i), abs(self.y - i)))
                else:
                    if arr[self.y - i][self.x - i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x - i, self.y - i, arr, whitePieces, blackPieces):
                                result.append((self.x - i, self.y - i))
                        else:
                            result.append((abs(self.x - i), abs(self.y - i)))
                    break

        # Up Right
        for i in range(1, maxMove + 1):
            if 0 <= self.y + i < len(arr) and 0 <= self.x + i < len(arr):
                if arr[self.y + i][self.x + i] is None:
                    if needCheck:
                        if self.needChecks(self.x + i, self.y + i, arr, whitePieces, blackPieces):
                            result.append((self.x + i, self.y + i))
                    else:
                        result.append((self.x + i, self.y + i))
                else:
                    if arr[self.y + i][self.x + i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x + i, self.y + i, arr, whitePieces, blackPieces):
                                result.append((self.x + i, self.y + i))
                        else:
                            result.append((self.x + i, self.y + i))
                    break

        # Down right
        for i in range(1, maxMove + 1):
            if 0 <= self.y - i < len(arr) and 0 <= self.x + i < len(arr):
                if arr[self.y - i][self.x + i] is None:
                    if needCheck:
                        if self.needChecks(self.x + i, self.y - i, arr, whitePieces, blackPieces):
                            result.append((self.x + i, self.y - i))
                    else:
                        result.append((self.x + i, abs(self.y - i)))
                else:
                    if arr[self.y - i][self.x + i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x + i, self.y - i, arr, whitePieces, blackPieces):
                                result.append((self.x + i, self.y - i))
                        else:
                            result.append((self.x + i, abs(self.y - i)))
                    break

        return result


class Queen(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.name = "Queen"
        self.sprite = pygame.image.load("assets/{}queen.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr, whitePieces, blackPieces, needCheck):
        result = []

        minMove = min(self.x, self.y)
        maxMove = max(len(arr) - self.x, len(arr) - self.y)

        # Up left
        for i in range(1, abs(len(arr) - minMove)):
            if 0 <= self.y + i < len(arr) and 0 <= self.x - i < len(arr):
                if arr[self.y + i][self.x - i] is None:
                    if needCheck:
                        if self.needChecks(self.x - i, self.y + i, arr, whitePieces, blackPieces):
                            result.append((self.x - i, self.y + i))
                    else:
                        result.append((abs(self.x - i), abs(self.y + i)))
                else:
                    if arr[self.y + i][self.x - i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x - i, self.y + i, arr, whitePieces, blackPieces):
                                result.append((self.x - i, self.y + i))
                        else:
                            result.append((abs(self.x - i), self.y + i))
                    break

        # Down Left
        for i in range(1, minMove + 1):
            if 0 <= self.y - i < len(arr) and 0 <= self.x - i < len(arr):
                if arr[self.y - i][self.x - i] is None:
                    if needCheck:
                        if self.needChecks(self.x - i, self.y - i, arr, whitePieces, blackPieces):
                            result.append((self.x - i, self.y - i))
                    else:
                        result.append((abs(self.x - i), abs(self.y - i)))
                else:
                    if arr[self.y - i][self.x - i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x - i, self.y - i, arr, whitePieces, blackPieces):
                                result.append((self.x - i, self.y - i))
                        else:
                            result.append((abs(self.x - i), abs(self.y - i)))
                    break

        # Up Right
        for i in range(1, maxMove + 1):
            if 0 <= self.y + i < len(arr) and 0 <= self.x + i < len(arr):
                if arr[self.y + i][self.x + i] is None:
                    if needCheck:
                        if self.needChecks(self.x + i, self.y + i, arr, whitePieces, blackPieces):
                            result.append((self.x + i, self.y + i))
                    else:
                        result.append((self.x + i, self.y + i))
                else:
                    if arr[self.y + i][self.x + i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x + i, self.y + i, arr, whitePieces, blackPieces):
                                result.append((self.x + i, self.y + i))
                        else:
                            result.append((self.x + i, self.y + i))
                    break

        # Down right
        for i in range(1, maxMove + 1):
            if 0 <= self.y - i < len(arr) and 0 <= self.x + i < len(arr):
                if arr[self.y - i][self.x + i] is None:
                    if needCheck:
                        if self.needChecks(self.x + i, self.y - i, arr, whitePieces, blackPieces):
                            result.append((self.x + i, self.y - i))
                    else:
                        result.append((self.x + i, abs(self.y - i)))
                else:
                    if arr[self.y - i][self.x + i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x + i, self.y - i, arr, whitePieces, blackPieces):
                                result.append((self.x + i, self.y - i))
                        else:
                            result.append((self.x + i, abs(self.y - i)))
                    break

        # Move right
        for i in range(1, len(arr) - self.x):
            if 0 <= self.x + i < len(arr):
                if arr[self.y][self.x + i] is None:
                    if needCheck:
                        if self.needChecks(self.x + i, self.y, arr, whitePieces, blackPieces):
                            result.append((self.x + i, self.y))
                    else:
                        result.append((self.x + i, self.y))
                else:
                    if arr[self.y][self.x + i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x + i, self.y, arr, whitePieces, blackPieces):
                                result.append((self.x + i, self.y))
                        else:
                            result.append((self.x + i, self.y))
                    break

        # Move Left
        for i in range(1, self.x + 1):
            if 0 <= self.x - i < len(arr):
                if arr[self.y][self.x - i] is None:
                    if needCheck:
                        if self.needChecks(self.x - i, self.y, arr, whitePieces, blackPieces):
                            result.append((self.x - i, self.y))
                    else:
                        result.append((self.x - i, self.y))
                else:
                    if arr[self.y][self.x - i].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x - i, self.y, arr, whitePieces, blackPieces):
                                result.append((self.x - i, self.y))
                        else:
                            result.append((self.x - i, self.y))
                    break

        # Move Up
        for j in range(1, len(arr) - self.y):
            if 0 <= self.y + j < len(arr):
                if arr[self.y + j][self.x] is None:
                    if needCheck:
                        if self.needChecks(self.x, self.y + j, arr, whitePieces, blackPieces):
                            result.append((self.x, self.y + j))
                    else:
                        result.append((self.x, self.y + j))
                else:
                    if arr[self.y + j][self.x].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x, self.y + j, arr, whitePieces, blackPieces):
                                result.append((self.x, self.y + j))
                        else:
                            result.append((self.x, self.y + j))
                    break

        # Move Down
        for j in range(1, self.y + 1):
            if 0 <= self.y - j < len(arr):
                if arr[self.y - j][self.x] is None:
                    if needCheck:
                        if self.needChecks(self.x, self.y - j, arr, whitePieces, blackPieces):
                            result.append((self.x, self.y - j))
                    else:
                        result.append((self.x, self.y - j))
                else:
                    if arr[self.y - j][self.x].getColor() == getEnemy[self.color]:
                        if needCheck:
                            if self.needChecksNotNone(self.x, self.y - j, arr, whitePieces, blackPieces):
                                result.append((self.x, self.y - j))
                        else:
                            result.append((self.x, self.y - j))
                    break

        return result


class King(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.name = "King"
        self.sprite = pygame.image.load("assets/{}king.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr, whitePieces, blackPieces, needCheck):
        result = []
        if self.start:
            # if self.y == 7:
            row = 0
            if self.color == 'b':
                row = 7

            if arr[row][5] is None and arr[row][6] is None:
                if arr[row][7] is not None:
                    if arr[row][7].start and arr[row][7].getName() == 'Rook':
                        if needCheck:
                            temp_piece = arr[row][7]
                            arr[row][7] = None
                            temp_piece.setPosition(5, row)
                            if self.needChecks(6, row, arr, whitePieces, blackPieces):
                                result.append((7, row))
                            arr[row][7] = temp_piece
                            temp_piece.setPosition(7, row)
                        else:
                            result.append((7, row))
            hasNoObstacle = True
            for i in range(1, 4):
                hasNoObstacle = hasNoObstacle and arr[row][i] is None
            if hasNoObstacle:
                if arr[row][0] is not None:
                    if arr[row][0].start and arr[row][0].getName() == 'Rook':
                        if needCheck:
                            temp_piece = arr[row][0]
                            arr[row][0] = None
                            temp_piece.setPosition(3, row)
                            if self.needChecks(2, row, arr, whitePieces, blackPieces):
                                result.append((0, row))
                            arr[row][0] = temp_piece
                            temp_piece.setPosition(0, row)
                        else:
                            result.append((0, row))

        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if 0 <= self.y + j < len(arr) and 0 <= self.x + i < len(arr):
                    if arr[self.y + j][self.x + i] is None:
                        if needCheck:
                            if self.needChecks(self.x + i, self.y + j, arr, whitePieces, blackPieces):
                                result.append((self.x + i, self.y + j))
                        else:
                            result.append((self.x + i, self.y + j))
                    else:
                        if arr[self.y + j][self.x + i].getColor() == getEnemy[self.color]:
                            if needCheck:
                                if self.needChecksNotNone(self.x + i, self.y + j, arr, whitePieces, blackPieces):
                                    result.append((self.x + i, self.y + j))
                            else:
                                result.append((self.x + i, self.y + j))

        return result



