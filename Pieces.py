import pygame

getEnemy = {'w': 'b', 'b': 'w'}
piecePoints = {"King": 900, "Queen": 90, "Bishop": 32, "Knight": 30,
                    "Rook": 50, "Pawn": 10}


class Player:

    def __init__(self):
        self.points = 1294
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
        return self.points

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
            if (x, y) in pawn.showOptions(board):
                return True
        for rook in self.rook:
            if (x, y) in rook.showOptions(board):
                return True
        for knight in self.knight:
            if (x, y) in knight.showOptions(board):
                return True
        for bishop in self.bishop:
            if (x, y) in bishop.showOptions(board):
                return True
        for queen in self.queen:
            if (x, y) in queen.showOptions(board):
                return True
        for king in self.king:
            if (x, y) in king.showOptions(board):
                return True

    def add(self, chessPiece):
        name = chessPiece.getName()
        chessPiecesList = self.pieces[name]
        isIn = False

        if chessPiecesList is not None:
            for cp in chessPiecesList:
                if chessPiece.isEqual(cp):
                    isIn = True
                    break

        if not isIn:
            chessPiecesList.append(chessPiece)
            self.points += piecePoints[chessPiece.getName()]
            self.pieceCount += 1

    def remove(self, chessPiece):
        name = chessPiece.getName()
        chessPiecesList = self.pieces[name]

        if chessPiecesList is not None:
            for cp in chessPiecesList:
                if chessPiece.isEqual(cp):
                    chessPiecesList.remove(cp)
                    self.pieceCount -= 1
                    self.points -= piecePoints[chessPiece.getName()]


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
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 60, abs((480 - 60) - y * 60)

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

    def showOptions(self, arr):
        pass


class Pawn(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.start = True
        self.name = "Pawn"
        self.sprite = pygame.image.load("assets/{}pawn.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr):
        result = []
        if self.color == 'w':
            if arr[self.y + 1][self.x] is None:
                result.append((self.x, self.y + 1))
            if self.start and arr[self.y + 2][self.x] is None and arr[self.y + 1][self.x] is None:
                result.append((self.x, self.y + 2))
            if 0 <= self.y + 1 < len(arr) and 0 <= self.x + 1 < len(arr):
                if arr[self.y + 1][self.x + 1] is not None:
                    if arr[self.y + 1][self.x + 1].getColor() == 'b':
                        result.append((self.x + 1, self.y + 1))
            if 0 <= self.y + 1 < len(arr) and 0 <= self.x - 1 < len(arr):
                if arr[self.y + 1][self.x - 1] is not None:
                    if arr[self.y + 1][self.x - 1].getColor() == 'b':
                        result.append((self.x - 1, self.y + 1))

        else:
            if arr[self.y - 1][self.x] is None:
                result.append((self.x, self.y - 1))
            if self.start and arr[self.y - 2][self.x] is None:
                result.append((self.x, self.y - 2))
            if 0 <= self.y - 1 < len(arr) and 0 <= self.x + 1 < len(arr):
                if arr[self.y - 1][self.x + 1] is not None:
                    if arr[self.y - 1][self.x + 1].getColor() == 'w':
                        result.append((self.x + 1, self.y - 1))
            if 0 <= self.y - 1 < len(arr) and 0 <= self.x - 1 < len(arr):
                if arr[self.y - 1][self.x - 1] is not None:
                    if arr[self.y - 1][self.x - 1].getColor() == 'w':
                        result.append((self.x - 1, self.y - 1))

        return result


class Rook(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.name = "Rook"
        self.sprite = pygame.image.load("assets/{}rook.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr):
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
                            result.append((4, row))
            elif self.x == 0:
                hasNoObstacle = True
                for i in range(1, 4):
                    hasNoObstacle = hasNoObstacle and arr[row][i] is None
                if hasNoObstacle:
                    if arr[row][4] is not None:
                        if arr[row][4].start and arr[row][4].getName() == 'King':
                            result.append((4, row))

        # Move right
        for i in range(1, len(arr) - self.x):
            if 0 <= self.x + i < len(arr):
                if arr[self.y][self.x + i] is None:
                    result.append((self.x + i, self.y))
                else:
                    if arr[self.y][self.x + i].getColor() == getEnemy[self.color]:
                        result.append((self.x + i, self.y))
                    break

        # Move Left
        for i in range(1, self.x + 1):
            if 0 <= self.x - i < len(arr):
                if arr[self.y][self.x - i] is None:
                    result.append((self.x - i, self.y))
                else:
                    if arr[self.y][self.x - i].getColor() == getEnemy[self.color]:
                        result.append((self.x - i, self.y))
                    break

        # Move Up
        for j in range(1, len(arr) - self.y):
            if 0 <= self.y + j < len(arr):
                if arr[self.y + j][self.x] is None:
                    result.append((self.x, self.y + j))
                else:
                    if arr[self.y + j][self.x].getColor() == getEnemy[self.color]:
                        result.append((self.x, self.y + j))
                    break

        # Move Down
        for j in range(1, self.y + 1):
            if 0 <= self.y - j < len(arr):
                if arr[self.y - j][self.x] is None:
                    result.append((self.x, self.y - j))
                else:
                    if arr[self.y - j][self.x].getColor() == getEnemy[self.color]:
                        result.append((self.x, self.y - j))
                    break

        return result


class Knight(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.name = "Knight"
        self.sprite = pygame.image.load("assets/{}knight.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr):
        result = []

        if 0 <= self.y + 2 < len(arr) and 0 <= self.x + 1 < len(arr):
            if arr[self.y + 2][self.x + 1] is None:
                result.append((self.x + 1, self.y + 2))
            else:
                if arr[self.y + 2][self.x + 1].getColor() == getEnemy[self.color]:
                    result.append((self.x + 1, self.y + 2))

        if 0 <= self.y + 1 < len(arr) and 0 <= self.x + 2 < len(arr):
            if arr[self.y + 1][self.x + 2] is None:
                result.append((self.x + 2, self.y + 1))
            else:
                if arr[self.y + 1][self.x + 2].getColor() == getEnemy[self.color]:
                    result.append((self.x + 2, self.y + 1))

        if 0 <= self.y - 1 < len(arr) and 0 <= self.x + 2 < len(arr):
            if arr[self.y - 1][self.x + 2] is None:
                result.append((self.x + 2, self.y - 1))
            else:
                if arr[self.y - 1][self.x + 2].getColor() == getEnemy[self.color]:
                    result.append((self.x + 2, self.y - 1))

        if 0 <= self.y - 2 < len(arr) and 0 <= self.x + 1 < len(arr):
            if arr[self.y - 2][self.x + 1] is None:
                result.append((self.x + 1, self.y - 2))
            else:
                if arr[self.y - 2][self.x + 1].getColor() == getEnemy[self.color]:
                    result.append((self.x + 1, self.y - 2))

        if 0 <= self.y + 2 < len(arr) and 0 <= self.x - 1 < len(arr):
            if arr[self.y + 2][self.x - 1] is None:
                result.append((self.x - 1, self.y + 2))
            else:
                if arr[self.y + 2][self.x - 1].getColor() == getEnemy[self.color]:
                    result.append((self.x - 1, self.y + 2))

        if 0 <= self.y + 1 < len(arr) and 0 <= self.x - 2 < len(arr):
            if arr[self.y + 1][self.x - 2] is None:
                result.append((self.x - 2, self.y + 1))
            else:
                if arr[self.y + 1][self.x - 2].getColor() == getEnemy[self.color]:
                    result.append((self.x - 2, self.y + 1))

        if 0 <= self.y - 1 < len(arr) and 0 <= self.x - 2 < len(arr):
            if arr[self.y - 1][self.x - 2] is None:
                result.append((self.x - 2, self.y - 1))
            else:
                if arr[self.y - 1][self.x - 2].getColor() == getEnemy[self.color]:
                    result.append((self.x - 2, self.y - 1))

        if 0 <= self.y - 2 < len(arr) and 0 <= self.x - 1 < len(arr):
            if arr[self.y - 2][self.x - 1] is None:
                result.append((self.x - 1, self.y - 2))
            else:
                if arr[self.y - 2][self.x - 1].getColor() == getEnemy[self.color]:
                    result.append((self.x - 1, self.y - 2))

        return result


class Bishop(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.name = "Bishop"
        self.sprite = pygame.image.load("assets/{}bishop.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr):
        result = []
        minMove = min(self.x, self.y)
        maxMove = max(len(arr) - self.x, len(arr) - self.y)

        # Up left
        for i in range(1, abs(len(arr) - minMove)):
            if 0 <= self.y + i < len(arr) and 0 <= self.x - i < len(arr):
                if arr[self.y + i][self.x - i] is None:
                    result.append((abs(self.x - i), abs(self.y + i)))
                else:
                    if arr[self.y + i][self.x - i].getColor() == getEnemy[self.color]:
                        result.append((abs(self.x - i), self.y + i))
                    break

        # Down Left
        for i in range(1, minMove + 1):
            if 0 <= self.y - i < len(arr) and 0 <= self.x - i < len(arr):
                if arr[self.y - i][self.x - i] is None:
                    result.append((abs(self.x - i), abs(self.y - i)))
                else:
                    if arr[self.y - i][self.x - i].getColor() == getEnemy[self.color]:
                        result.append((abs(self.x - i), abs(self.y - i)))
                    break

        # Up Right
        for i in range(1, maxMove + 1):
            if 0 <= self.y + i < len(arr) and 0 <= self.x + i < len(arr):
                if arr[self.y + i][self.x + i] is None:
                    result.append((self.x + i, self.y + i))
                else:
                    if arr[self.y + i][self.x + i].getColor() == getEnemy[self.color]:
                        result.append((self.x + i, self.y + i))
                    break

        # Down right
        for i in range(1, maxMove + 1):
            if 0 <= self.y - i < len(arr) and 0 <= self.x + i < len(arr):
                if arr[self.y - i][self.x + i] is None:
                    result.append((self.x + i, abs(self.y - i)))
                else:
                    if arr[self.y - i][self.x + i].getColor() == getEnemy[self.color]:
                        result.append((self.x + i, abs(self.y - i)))
                    break

        return result


class Queen(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.name = "Queen"
        self.sprite = pygame.image.load("assets/{}queen.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr):
        result = []

        minMove = min(self.x, self.y)
        maxMove = max(len(arr) - self.x, len(arr) - self.y)

        # Up left
        for i in range(1, abs(len(arr) - minMove)):
            if 0 <= self.y + i < len(arr) and 0 <= self.x - i < len(arr):
                if arr[self.y + i][self.x - i] is None:
                    result.append((abs(self.x - i), abs(self.y + i)))
                else:
                    if arr[self.y + i][self.x - i].getColor() == getEnemy[self.color]:
                        result.append((abs(self.x - i), self.y + i))
                    break

        # Down Left
        for i in range(1, minMove + 1):
            if 0 <= self.y - i < len(arr) and 0 <= self.x - i < len(arr):
                if arr[self.y - i][self.x - i] is None:
                    result.append((abs(self.x - i), abs(self.y - i)))
                else:
                    if arr[self.y - i][self.x - i].getColor() == getEnemy[self.color]:
                        result.append((abs(self.x - i), abs(self.y - i)))
                    break

        # Up Right
        for i in range(1, maxMove + 1):
            if 0 <= self.y + i < len(arr) and 0 <= self.x + i < len(arr):
                if arr[self.y + i][self.x + i] is None:
                    result.append((self.x + i, self.y + i))
                else:
                    if arr[self.y + i][self.x + i].getColor() == getEnemy[self.color]:
                        result.append((self.x + i, self.y + i))
                    break

        # Down right
        for i in range(1, maxMove + 1):
            if 0 <= self.y - i < len(arr) and 0 <= self.x + i < len(arr):
                if arr[self.y - i][self.x + i] is None:
                    result.append((self.x + i, abs(self.y - i)))
                else:
                    if arr[self.y - i][self.x + i].getColor() == getEnemy[self.color]:
                        result.append((self.x + i, abs(self.y - i)))
                    break

        # Move right
        for i in range(1, len(arr) - self.x):
            if 0 <= self.x + i < len(arr):
                if arr[self.y][self.x + i] is None:
                    result.append((self.x + i, self.y))
                else:
                    if arr[self.y][self.x + i].getColor() == getEnemy[self.color]:
                        result.append((self.x + i, self.y))
                    break

        # Move Left
        for i in range(1, self.x + 1):
            if 0 <= self.x - i < len(arr):
                if arr[self.y][self.x - i] is None:
                    result.append((self.x - i, self.y))
                else:
                    if arr[self.y][self.x - i].getColor() == getEnemy[self.color]:
                        result.append((self.x - i, self.y))
                    break

        # Move Up
        for j in range(1, len(arr) - self.y):
            if 0 <= self.y + j < len(arr):
                if arr[self.y + j][self.x] is None:
                    result.append((self.x, self.y + j))
                else:
                    if arr[self.y + j][self.x].getColor() == getEnemy[self.color]:
                        result.append((self.x, self.y + j))
                    break

        # Move Down
        for j in range(1, self.y + 1):
            if 0 <= self.y - j < len(arr):
                if arr[self.y - j][self.x] is None:
                    result.append((self.x, self.y - j))
                else:
                    if arr[self.y - j][self.x].getColor() == getEnemy[self.color]:
                        result.append((self.x, self.y - j))
                    break

        return result


class King(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.name = "King"
        self.sprite = pygame.image.load("assets/{}king.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def showOptions(self, arr):
        result = []
        if self.start:
            # if self.y == 7:
            row = 0
            if self.color == 'b':
                row = 7

            if arr[row][5] is None and arr[row][6] is None:
                if arr[row][7] is not None:
                    if arr[row][7].start and arr[row][7].getName() == 'Rook':
                        result.append((7, row))
            hasNoObstacle = True
            for i in range(1, 4):
                hasNoObstacle = hasNoObstacle and arr[row][i] is None
            if hasNoObstacle:
                if arr[row][0] is not None:
                    if arr[row][0].start and arr[row][0].getName() == 'Rook':
                        result.append((0, row))

        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if 0 <= self.y + j < len(arr) and 0 <= self.x + i < len(arr):
                    if arr[self.y + j][self.x + i] is None:
                        result.append((self.x + i, self.y + j))
                    else:
                        if arr[self.y + j][self.x + i].getColor() == getEnemy[self.color]:
                            result.append((self.x + i, self.y + j))

        return result



