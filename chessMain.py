import pygame as p


from chess_engine_code import chessEngine as cE , SmartMoveFinder

p.init()

WIDTH,HEIGHT = 512 ,512
DIMENSION = 8 #DIM OF CHESS 8X8
SQR_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}
'''
insitalizing global distionary for images

'''
def loadImages():

    pieces = ["bR", "bN","bB","bQ","bK","bp","wR", "wN", "wB", "wQ", "wK","wp"]
    for pice in pieces:
        IMAGES[pice] = p.transform.scale(p.image.load("images/" + pice + ".png") , (SQR_SIZE,SQR_SIZE))

'''

this is main driver , take user input and update graphics
'''

def main():


    screen = p.display.set_mode((WIDTH,HEIGHT))
    screen.fill((255,255,255))
    clock = p.time.Clock()
    gs = cE.Gamestate()
    print(gs.board)
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False # flag for animation
    loadImages()
    sqSelected = () #tuple # intially no squre selected # keep track of the last click of user (tuple:(row,col)), means it stores where user  want to place the pice or wich pice or square is selected
    playerClick = [] #keep track of user last move ( two tuple : [(6,4) ,(4,4)],intial and final square of pice
    gameOver = False
    playerOne = False # if human is playing with white then true, if ai is playing then false
    plyerTwo = False# same as above but for black






    run = True
    while run:
        humanTurn = (gs.whitetomove and playerOne) or (not gs.whitetomove and plyerTwo) # checking for weather human turn or AI , if AI it will block the mouse events , but key events are not affected
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
                #for finding that mouse is at wich position on the board (finding row and col)
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()#gives the coordinets of mouse
                    col = location[0]// SQR_SIZE
                    row = location[1] // SQR_SIZE
                    #print(row,col) #checking if correctly working or not
                    if sqSelected == (row,col): # user click on same sqare twice
                        sqSelected = () #deselect
                        playerClick = [] #clear  player click
                    else:
                        sqSelected = (row,col)
                        playerClick.append(sqSelected)
                    if len(playerClick) == 2: #after 2nd click
                        move = cE.Move(playerClick[0],playerClick[1],gs.board)
                        print(move)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])#we have optional parameter so we are making validmoves[i], not move , because of enpassant move.......
                                moveMade = True
                                animate = True
                                sqSelected = ()  # clear
                                playerClick = []  # clear player moves to store new moves
                        if not moveMade:
                            playerClick = [sqSelected]



            elif e.type == p.KEYDOWN: # undo button
                if e.key == p.K_z:
                    if playerOne and plyerTwo:
                        gs.undoMove()

                    else:
                        gs.undoMove()
                        gs.undoMove()

                    moveMade = True
                    animate = False
                    gameOver = False



                if e.key == p.K_r:  # reset the game whe press r
                    gs = cE.Gamestate()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClick = []
                    moveMade = False
                    animate = False
                    gameOver = False


        # Ai move finder
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMoveMinMax(gs, validMoves)
            if AIMove is None:
                 AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False


        drawGameState(screen,gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whitetomove:
                print("checkmate")
                drawText(screen, 'Black win by checkmate')
            else:
                drawText(screen, 'white win by checkmate')
        elif gs.staleMate:
            print("stalemate")
            drawText(screen, 'stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()



'''

highlighting square selected & moves for piece selected
'''
def highlightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whitetomove else 'b'):

            #Highlight sqSelected
            s = p.Surface((SQR_SIZE, SQR_SIZE))
            s.set_alpha(100) #transperency , value -> 0 transparent , 225 . opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQR_SIZE, r*SQR_SIZE))

            #HIGHLIGHT MOVES FROM THAT SQUARE
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*SQR_SIZE, move.endRow*SQR_SIZE) )








'''
display graphics of current state of game
'''
def drawGameState(screen,gs, validmoves, sqSelected):
    drawBoard(screen)#draw the square on board
    highlightSquare(screen, gs, validmoves, sqSelected)
    drawPices(screen,gs.board)#draw pices on the board/squares


def drawBoard(screen):
    #colors = [(255, 255, 255), (128, 128, 128)]  # white and gray
    global colors

    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen,color,p.Rect(c*SQR_SIZE,r*SQR_SIZE,SQR_SIZE,SQR_SIZE))


    #colors = [p.color("white"), p.color("gray")]

def drawPices(screen , board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pice = board[r][c]
            if pice != "__":
                screen.blit(IMAGES[pice], p.Rect(c*SQR_SIZE,r*SQR_SIZE,SQR_SIZE,SQR_SIZE))

'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPices(screen, board)
        #earase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQR_SIZE, move.endRow*SQR_SIZE, SQR_SIZE, SQR_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw picecaptured onto rectangle
        if move.piceCaptured != '__':
            screen.blit(IMAGES[move.piceCaptured], endSquare)
        # draw moving pices
        screen.blit(IMAGES[move.piceMoved], p.Rect(c*SQR_SIZE, r*SQR_SIZE, SQR_SIZE, SQR_SIZE))
        p.display.flip()
        clock.tick(60)



def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0 , p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))



if __name__=="__main__":
    main()



