import sys

from Effects import Hover, PathDot, CheckHover, CheckMakeHover
from Pieces import *
from MiniMax import findNextMove

screen = pygame.display.set_mode((60 * 8, 60 * 8))
background_surface = pygame.image.load("assets/chessboard.png").convert()
board = np.empty([8, 8], dtype=ChessPiece)

all_sprites_list = pygame.sprite.Group()
sprites = []
options = None
hover = None
checkHover = None
current_Available_Paths = []
whitePieces = White()
blackPieces = Black()


def initialisePieces(whitePieces, blackPieces, b):
    placedWhiteBoard = whitePieces.put_On_Board(b)
    startingBoard = blackPieces.put_On_Board(placedWhiteBoard)
    return startingBoard


def getChessPiece(whiteTurn):
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = abs((480 - y) // 60)
    if board[y][x] is not None:
        if whiteTurn:
            if board[y][x].getColor() == 'w':
                return board[y][x]
        else:
            if board[y][x].getColor() == 'b':
                return board[y][x]
    return None


def getChessPosition():
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = abs((480 - y) // 60)
    return x, y


def moveChessPiece(chessPiece, x, y):
    global options
    if chessPiece is None:
        return False, False
    if chessPiece.getPosition() == (x, y):
        return False, True
    # options = chessPiece.showOptions(board, whitePieces, blackPieces, True)
    if (x, y) in options:
        oldX, oldY = chessPiece.getPosition()
        if chessPiece.getName() == 'King' and chessPiece.start:
            if x == 7 and board[oldY][5] is None and board[oldY][6] is None and board[y][x] is not None \
                    and board[y][x].start:
                rook = board[y][x]
                board[y][x - 1] = chessPiece
                board[y][x] = None
                board[y][oldX + 1] = rook
                board[oldY][oldX] = None
                chessPiece.setPosition(x - 1, y)
                rook.setPosition(oldX + 1, y)
                rook.started()
            elif x == 0 and board[oldY][2] is None and board[oldY][3] is None and board[oldY][1] is None \
                    and board[y][x] is not None and board[y][x].start:
                rook = board[y][x]
                board[y][x + 2] = chessPiece
                board[y][x] = None
                board[y][oldX - 1] = rook
                board[oldY][oldX] = None
                chessPiece.setPosition(x + 2, y)
                rook.setPosition(oldX - 1, y)
                rook.started()
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
        elif chessPiece.getName() == 'Rook' and chessPiece.start and (oldX == 7 or oldX == 0) and y == oldY:
            if oldX == 7 and board[oldY][5] is None and board[oldY][6] is None and board[oldY][4] is not None \
                    and board[oldY][4].start:
                king = board[y][x]
                board[y][oldX - 1] = king
                board[y][x] = None
                board[y][x + 1] = chessPiece
                board[oldY][oldX] = None
                chessPiece.setPosition(x + 1, y)
                king.setPosition(oldX - 1, y)
                king.started()
            elif oldX == 0 and board[oldY][2] is None and board[oldY][3] is None and board[oldY][1] is None \
                    and board[oldY][4] is not None and board[oldY][4].start:
                king = board[y][x]
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
        elif chessPiece.getName() == 'Pawn' and y == 7:
            if board[y][x] is not None:
                temp_piece = board[y][x]
                if chessPiece.getColor() == 'w':
                    blackPieces.remove(temp_piece)
                    whitePieces.remove(chessPiece)
                else:
                    whitePieces.remove(temp_piece)
                    blackPieces.remove(chessPiece)
                board[y][x] = None
                all_sprites_list.remove(temp_piece)
            oldX, oldY = chessPiece.getPosition()
            board[oldY][oldX] = None
            all_sprites_list.remove(chessPiece)
            newQueen = Queen(x, y, chessPiece.getColor())
            newQueen.addSurfaces()
            newQueen.addImages()
            board[y][x] = newQueen
            newQueen.started()
            all_sprites_list.add(board[y][x])
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
                for (x, y) in piece.showOptions(board, None, None, False):
                    new_board = np.copy(board)
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
                for (x, y) in piece.showOptions(board, None, None, False):
                    new_board = np.copy(board)
                    oldX, oldY = piece.getPosition()
                    new_board[oldY][oldX] = None
                    new_board[y][x] = piece
                    if piece.getName() == 'King':
                        if not whitePieces.seeCheck(x, y, new_board):
                            return False
                    else:
                        if not whitePieces.seeCheck(kingX, kingY, new_board):
                            return False
        return True


def setHover(x, y):
    global hover
    hover = Hover(x, y)
    all_sprites_list.add(hover)


def setPath(chessPiece):
    global options
    options = chessPiece.showOptions(board, whitePieces, blackPieces, True)
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
    board = initialisePieces(whitePieces, blackPieces, board)
    sprites = [piece for row in board for piece in row if piece]
    all_sprites_list.add(sprites)


def runGame():
    global board, current_Available_Paths

    game_Over = False
    selected = False
    chessPiece = None
    removedCheck = False
    whiteTurn = True

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
                            _, move = findNextMove(whitePieces, blackPieces, 4, board)
                            if move is not None:
                                specialMove = False
                                queenChange = False
                                ((oldX, oldY), (newX, newY)) = move
                                blackPiece = board[oldY][oldX]
                                # transforming into queen
                                if blackPiece.getName() == 'Pawn' and newY == 0:
                                    if board[newY][newX] is not None:
                                        temp_piece = board[newY][newX]
                                        whitePieces.remove(temp_piece)
                                        blackPieces.remove(blackPiece)
                                        board[newY][newX] = None
                                        all_sprites_list.remove(temp_piece)
                                    board[oldY][oldX] = None
                                    all_sprites_list.remove(blackPiece)
                                    newQueen = Queen(newX, newY, 'b')
                                    newQueen.addSurfaces()
                                    newQueen.addImages()
                                    board[newY][newX] = newQueen
                                    newQueen.started()
                                    all_sprites_list.add(board[newY][newX])
                                    queenChange = True
                                elif board[newY][newX] is not None:
                                    curr_piece = board[oldY][oldX]
                                    temp_piece = board[newY][newX]

                                    if curr_piece.getColor() == temp_piece.getColor():
                                        if curr_piece.getName() == 'King':
                                            if temp_piece.getName() == 'Rook':
                                                if newY == oldY:
                                                    if newX == 7 and oldX == 4:
                                                        temp_piece.setPosition(5, oldY)
                                                        curr_piece.setPosition(6, oldY)
                                                        specialMove = True
                                                        temp_piece.started()
                                                        curr_piece.started()
                                                    elif newX == 0 and oldX == 4:
                                                        temp_piece.setPosition(3, oldY)
                                                        curr_piece.setPosition(2, oldY)
                                                        specialMove = True
                                                        temp_piece.started()
                                                        curr_piece.started()
                                                else:
                                                    print("Error move!")
                                        elif curr_piece.getName() == 'Rook':
                                            if temp_piece.getName() == 'King':
                                                if newY == oldY:
                                                    if oldX == 7 and newX == 4:
                                                        curr_piece.setPosition(5, oldY)
                                                        temp_piece.setPosition(6, oldY)
                                                        specialMove = True
                                                        temp_piece.started()
                                                        curr_piece.started()
                                                    elif newX == 0 and oldX == 4:
                                                        curr_piece.setPosition(3, oldY)
                                                        temp_piece.setPosition(2, oldY)
                                                        specialMove = True
                                                        temp_piece.started()
                                                        curr_piece.started()
                                                    else:
                                                        print("Error move!")
                                        else:
                                            print("Error move!")
                                    else:
                                        whitePieces.remove(board[newY][newX])
                                        all_sprites_list.remove(board[newY][newX])

                                if not specialMove and not queenChange:
                                    board[oldY][oldX] = None
                                    board[newY][newX] = blackPiece
                                    blackPiece.setPosition(newX, newY)
                                    blackPiece.started()

                            else:
                                print("Error no moves left!")
                                x, y = blackPieces.getKing().getPosition()
                                setCheckMate(x, y)
                        else:
                            pass
                    if not selected:
                        all_sprites_list.remove(hover)
                        all_sprites_list.remove(current_Available_Paths)
                        current_Available_Paths = []
                else:
                    chessPiece = getChessPiece(whiteTurn)
                    if chessPiece is None:
                        pass
                    else:
                        selected = True
                        x, y = chessPiece.getPosition()
                        setHover(x, y)
                        setPath(chessPiece)

                wKing = whitePieces.getKing()
                if wKing is not None:
                    wKingX, wKingY = wKing.getPosition()
                else:
                    setCheckMate(wKingX, wKingY)
                    # game_Over = True
                    pass
                bKing = blackPieces.getKing()
                if bKing is not None:
                    bKingX, bKingY = bKing.getPosition()
                else:
                    setCheckMate(bKingX, bKingY)
                    # game_Over = True
                    pass

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
