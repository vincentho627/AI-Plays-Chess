import pygame
import sys

from Effects import Hover, PathDot, CheckHover, CheckMakeHover
from Pieces import *

screen = pygame.display.set_mode((60 * 8, 60 * 8))
background_surface = pygame.image.load("assets/chessboard.png").convert()
board = [[None] * 8 for _ in range(8)]

all_sprites_list = pygame.sprite.Group()
sprites = []
hover = None
checkHover = None
current_Available_Paths = []
whitePieces = White()
blackPieces = Black()


def initialisePieces(whitePieces, blackPieces):
    placedWhiteBoard = whitePieces.put_On_Board(board)
    startingBoard = blackPieces.put_On_Board(placedWhiteBoard)
    return startingBoard


def getChessPiece():
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = abs((480 - y) // 60)
    return board[y][x]


def getChessPosition():
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = abs((480 - y) // 60)
    return x, y


def moveChessPiece(chessPiece, x, y):
    if chessPiece is None:
        return False, False
    if chessPiece.getPosition() == (x, y):
        return False, True
    options = chessPiece.showOptions(board)
    if (x, y) in options:
        oldX, oldY = chessPiece.getPosition()
        if chessPiece.getName() == 'King' and chessPiece.start:
            if x == 7 and board[oldY][5] is None and board[oldY][6] is None:
                rook = board[y][x]
                board[y][x - 1] = chessPiece
                board[y][x] = None
                board[y][oldX + 1] = rook
                board[oldY][oldX] = None
                chessPiece.setPosition(x - 1, y)
                rook.setPosition(oldX + 1, y)
                rook.started()
            elif x == 0 and board[oldY][2] is None and board[oldY][3] is None and board[oldY][1] is None:
                rook = board[y][x]
                board[y][x + 2] = chessPiece
                board[y][x] = None
                board[y][oldX - 1] = rook
                board[oldY][oldX] = None
                chessPiece.setPosition(x + 2, y)
                rook.setPosition(oldX - 1, y)
                rook.started()
        elif chessPiece.getName() == 'Rook' and chessPiece.start:
            if oldX == 7 and board[oldY][5] is None and board[oldY][6] is None:
                king = board[y][x]
                assert x == 4
                board[y][oldX - 1] = king
                board[y][x] = None
                board[y][x + 1] = chessPiece
                board[oldY][oldX] = None
                chessPiece.setPosition(x + 1, y)
                king.setPosition(oldX - 1, y)
                king.started()
            elif oldX == 0 and board[oldY][2] is None and board[oldY][3] is None and board[oldY][1] is None:
                king = board[y][x]
                assert x == 4
                board[y][oldX + 2] = king
                board[y][x] = None
                board[y][x - 1] = board[oldY][oldX]
                board[oldY][oldX] = None
                chessPiece.setPosition(x - 1, y)
                king.setPosition(oldX + 2, y)
                king.started()
            else:
                if board[y][x] is not None:
                    color = board[y][x].getColor()
                    if color == 'w':
                        whitePieces.remove(board[y][x])
                    else:
                        blackPieces.remove(board[y][x])
                    all_sprites_list.remove(board[y][x])
                board[y][x] = chessPiece
                board[oldY][oldX] = None
                chessPiece.setPosition(x, y)
        else:
            if board[y][x] is not None:
                color = board[y][x].getColor()
                if color == 'w':
                    whitePieces.remove(board[y][x])
                else:
                    blackPieces.remove(board[y][x])
                all_sprites_list.remove(board[y][x])
            board[y][x] = chessPiece
            board[oldY][oldX] = None
            chessPiece.setPosition(x, y)

        chessPiece.started()
        return True, False
    else:
        # alert error or something
        return False, False


def seeCheckMate(kingX, kingY, board, color):
    # ally king's x, y
    # input color is the one that just moved
    if color == 'b':
        for pieceType in whitePieces.pieces.values():
            for piece in pieceType:
                for (x, y) in piece.showOptions(board):
                    new_board = board.copy()
                    for i in range(len(board)):
                        new_board[i] = board[i].copy()
                    oldX, oldY = piece.getPosition()
                    new_board[oldY][oldX] = None
                    new_board[y][x] = piece
                    if piece.getName() == 'King':
                        if not blackPieces.seeCheck(x, y, new_board):
                            return False
                    else:
                        if not blackPieces.seeCheck(kingX, kingY, new_board):
                            return False
        return True
    else:
        for pieceType in blackPieces.pieces.values():
            for piece in pieceType:
                for (x, y) in piece.showOptions(board):
                    new_board = board.copy()
                    for i in range(len(board)):
                        new_board[i] = board[i].copy()
                    oldX, oldY = piece.getPosition()
                    new_board[oldY][oldX] = None
                    new_board[y][x] = piece
                    if not whitePieces.seeCheck(kingX, kingY, new_board):
                        return False
        return True


def setHover(x, y):
    global hover
    hover = Hover(x, y)
    all_sprites_list.add(hover)


def setPath(chessPiece):
    options = chessPiece.showOptions(board)
    for (x, y) in options:
        current_Available_Paths.append(PathDot(x, y))
    all_sprites_list.add(current_Available_Paths)


def setCheck(x, y):
    global checkHover
    checkHover = CheckHover(x, y)
    all_sprites_list.add(checkHover)


def setCheckMate(x, y):
    global checkHover
    checkHover = CheckMakeHover(x, y)
    all_sprites_list.add(checkHover)


def startGame():
    global board, all_sprites_list, sprites, whitePieces, blackPieces
    board = initialisePieces(whitePieces, blackPieces)
    sprites = [piece for row in board for piece in row if piece]
    all_sprites_list.add(sprites)


def runGame():
    global board, current_Available_Paths

    game_Over = False
    selected = False
    chessPiece = None
    removedCheck = False

    while not game_Over:
        screen.blit(background_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selected:
                    x, y = getChessPosition()
                    moved, unselect = moveChessPiece(chessPiece, x, y)
                    if unselect:
                        selected = False
                    else:
                        if moved:
                            selected = False
                        else:
                            pass
                    if not selected:
                        all_sprites_list.remove(hover)
                        all_sprites_list.remove(current_Available_Paths)
                        current_Available_Paths = []
                else:
                    chessPiece = getChessPiece()
                    if chessPiece is None:
                        pass
                    else:
                        selected = True
                        x, y = chessPiece.getPosition()
                        setHover(x, y)
                        setPath(chessPiece)

                wKing = whitePieces.getKing()
                wKingX, wKingY = wKing.getPosition()
                bKing = blackPieces.getKing()
                bKingX, bKingY = bKing.getPosition()

                if not removedCheck:
                    all_sprites_list.remove(checkHover)
                    removedCheck = True

                if whitePieces.seeCheck(bKingX, bKingY, board):
                    # hover effect on king
                    setCheck(bKingX, bKingY)
                    removedCheck = False

                    if seeCheckMate(bKingX, bKingY, board, 'w'):
                        all_sprites_list.remove(checkHover)
                        setCheckMate(bKingX, bKingY)

                if blackPieces.seeCheck(wKingX, wKingY, board):
                    # hover effect on king
                    setCheck(wKingX, wKingY)
                    removedCheck = False

                    if seeCheckMate(wKingX, wKingY, board, 'b'):
                        all_sprites_list.remove(checkHover)
                        setCheckMate(wKingX, wKingY)

        all_sprites_list.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    startGame()
    runGame()
