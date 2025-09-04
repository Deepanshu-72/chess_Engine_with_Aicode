




import  random


pieceScore = {"K" : 0, "Q" : 10, "R" :5, "B" : 3, "N" : 3, "p" : 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4


'''picks and return random move'''
def findRandomMove( validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

'''
find the best move based on the material alone
'''
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whitetomove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMinMaxScore = - CHECKMATE
        else:
            opponentsMoves = gs.getValidMoves()
            opponentMaxScore = - CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score =  CHECKMATE
                elif gs.staleMate:
                    score = 0
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score

                gs.undoMove()


        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove



'''helper method to make the first recursive call'''

def findBestMoveMinMax(gs, validMoves):
    # this is our helper method for calling our main mim max .. and other method
    global nextMove
    nextMove = None
    #findMoveMinMax(gs,validMoves,DEPTH, gs.whitetomove)
    #findMoveNegaMax(gs,validMoves,DEPTH,1 if gs.whitetomove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whitetomove else -1)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreBoard(gs)

    if whiteToMove:
        maxScore = -CHECKMATE
        random.shuffle(validMoves)
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore


    else:
        minScore = CHECKMATE
        random.shuffle(validMoves)
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs,validMoves,depth,turnMultiplier):
    global nextMove
    if depth ==0:
        return turnMultiplier*scoreBoard(gs)

    maxScore = -CHECKMATE
    random.shuffle(validMoves)
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1,-turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha , beta, turnMultiplier):
    global nextMove
    if depth ==0:
        return turnMultiplier*scoreBoard(gs)

    maxScore = -CHECKMATE
    random.shuffle(validMoves)
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore







def scoreBoard(gs):
    if gs.checkMate:
        if gs.whitetomove:
            return -CHECKMATE
        else:
            return CHECKMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score












'''
score the board based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score