class Gamestate():
    def __init__(self):
        self.board = [
            ["bR", "bN","bB","bQ","bK","bB","bN","bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["__","__","__","__","__","__","__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunction = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves,
                             'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves,}
        self.whitetomove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = ()
        #castel rights
        self.whitecastleKingSide = True
        self.blackcastleKingSide = True
        self.whitecastleQueenSide = True
        self.blackcastleQueenSide = True
        self.castelRightsLog = [CastleRights(self.whitecastleKingSide, self.blackcastleKingSide,
                                             self.whitecastleQueenSide,self.blackcastleQueenSide)]


        '''
        take a Move as parameter and exectues it (this will not work for castaling , pawn promoton,)
        '''

    def makeMove(self ,move):
        self.board[move.startRow][move.startCol] = "__"
        self.board[move.endRow][move.endCol] = move.piceMoved
        self.moveLog.append(move)#log / store move so that we can undo it later
        self.whitetomove = not self.whitetomove #swap the player
        #update king location if moved
        if move.piceMoved == "wK":
            self.whiteKingLocation = (move.endRow , move.endCol)
        elif move.piceMoved == "bK":
            self.blackKingLocation = (move.endRow , move.endCol)

        # if pawn move 2 next move can be capture
        if move.piceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # only 2 sq pawn advance
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        # en passant move
        if move.isEnpassantmove:
            self.board[move.startRow][move.endCol] = '__'

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.piceMoved[0] + 'Q'
            print('pawn promotiom')

        ##castle Move
        if move.castel:
            print("iam in castel")
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]# move rook
                self.board[move.endRow][move.endCol + 1] = '__'# empty moove rook space
            else:# queen side castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # move rook
                self.board[move.endRow][move.endCol - 2] = '__'




        # update castle Rights
        self.updateCastleRight(move)
        self.castelRightsLog.append(CastleRights(self.whitecastleKingSide, self.blackcastleKingSide,
                                             self.whitecastleQueenSide,self.blackcastleQueenSide))







        '''
        undo of move
        '''
    def undoMove(self):
        if len(self.moveLog) !=0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.piceMoved
            self.board[move.endRow][move.endCol] = move.piceCaptured
            self.whitetomove = not self.whitetomove
            # update king location if undo
            if move.piceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.piceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            # undo en passant
            if move.isEnpassantmove:
                self.board[move.endRow][move.endCol] = '__' #leaving landing squre blank
                self.board[move.startRow][move.endCol] = move.piceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            # undo 2 sq pawn advance
            if move.piceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            # undo
            #give back castle rights to king if move is undo
            self.castelRightsLog.pop() # remove last update
            castleRights = self.castelRightsLog[-1]
            self.whitecastleKingSide = castleRights.whitecastleKingSide
            self.blackcastleKingSide = castleRights.blackcastleKingSide
            self.whitecastleQueenSide = castleRights.whitecastleQueenSide
            self.blackcastleQueenSide = castleRights.blackcastleQueenSide


            #undo castle
            if move.castel:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]  # move rook
                    self.board[move.endRow][move.endCol - 1] = "__"  # empty moove rook space
                else:  # queen side castle
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]  # move rook
                    self.board[move.endRow][move.endCol + 1] = '__'


            # add this because if we undo move we also have to undo the stalemate and checkmate valriables
            self.checkMate = False
            self.staleMate = False







    def getValidMoves(self):
        moves = []
        self.incheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whitetomove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.incheck:
            print("i am in check")
            if len(self.checks) == 1:# only 1 checks , block check or move king
                moves = self.getAllPossibleMoves()
                # to block check put pice between sq of king and the enemy pice
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                piceChecking = self.board[checkRow][checkCol] # any pice
                validSquares = [] #squares that pices can move

                # if piceChecking is knight , must capture knight or move king , we can't block it

                if piceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in  range(1,8):
                        validSquare = (kingRow + check[2] * i , kingCol + check[3] * i) #check[2] ,[3]  are check direction
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol :
                            break
                #get rid on any move that block or move king
                for i in range(len(moves) -1, -1, -1):
                    if moves[i].piceMoved[1] !='K': #skkiping the kings moves to remove
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])

            else: # double check so move king
                self.getKingMoves(kingRow, kingCol, moves)
        else:# not in check
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:#for checkmate and stalemate
            if self.incheck:
                print("true11")
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False














        return moves




























    '''All posssible move without considering checks'''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whitetomove) or (turn == 'b' and not self.whitetomove):
                    pice = self.board[r][c][1]
                    self.moveFunction[pice](r,c,moves)

        return moves

    '''
    get all possible move for pawn at row ,colum and add it into list
    '''
    def getPawnMoves(self, r, c, moves):
        picePined = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                picePined = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break



        if self.whitetomove:
            if self.board[r-1][c] == "__": # 1 square pawn advance
                if not picePined or pinDirection == (-1,0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "__":  # 2 square pawn advance
                        moves.append(Move((r, c), (r - 2, c), self.board))

            if c-1 >=0:
                if self.board[r-1][c-1][0] == "b": #enemy pice to capture
                    if not picePined or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c-1), self.board, isEnpassantMove=True))


                    # capture
            if c+1 <=7:
                if self.board[r-1][c+1][0] == "b": #enemy pice to capture
                    if not picePined or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif(r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c+1), self.board, isEnpassantMove=True))



        else:#black pawn move
            if self.board[r+1][c] == "__":
                if not picePined or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "__":  # 1 square pawn advance
                        moves.append(Move((r, c), (r + 2, c), self.board))

                    #capture
            if c-1 >=0:
                if self.board[r+1][c-1][0] == "w": #enemy pice to capture
                    if not picePined or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c-1), self.board, isEnpassantMove=True))


            if c+1 <=7:
                if self.board[r+1][c+1][0] == "w": #enemy pice to capture
                    if not picePined or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c+1), self.board, isEnpassantMove=True))


        #add pawn promotion


    '''
        get all possible move for rrrrook at row ,colum and add it into list
        '''

    def getRookMoves(self, r, c, moves):
        picePined = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                picePined = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])

                break

        direction = ((-1,0), (0,-1), (1,0),(0,1))# up,left,down,right
        enemyColor = "b" if self.whitetomove else "w"
        for d in direction:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0<= endRow < 8 and 0 <= endCol < 8:
                    if not picePined or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPice = self.board[endRow][endCol]
                        if endPice == "__":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPice[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # same color pice
                            break
                else:#off board
                    break




    '''
        get all possible move for Knight at row ,colum and add it into list
        '''


    def getKnightMoves(self, r, c, moves):
        picePined = False

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                picePined = True
                self.pins.remove(self.pins[i])
                break
        knigntMoves =((-2,-1),(-2,1),(-1,-2),(1,-2),(-1,2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whitetomove else "b"
        for m in  knigntMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not picePined :
                    endPice = self.board[endRow][endCol]
                    if endPice[0] != allyColor:  # not on same color pice
                        moves.append(Move((r, c), (endRow, endCol), self.board))






    '''
        get all possible move for Bishop at row ,colum and add it into list
        '''

    def getBishopMoves(self, r, c, moves):
        picePined = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                picePined = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # leftup,righup,leftdown,rightdown
        enemyColor = "b" if self.whitetomove else "w"
        for d in direction:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not picePined or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPice = self.board[endRow][endCol]
                        if endPice == "__":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPice[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # same color pice
                            break

                else:  # off board
                    break

    '''
        get all possible move for Queen at row ,colum and add it into list
        '''


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves( r, c, moves)
        self.getBishopMoves( r, c, moves)

    '''
        get all possible move for king at row ,colum and add it into list
        '''


    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whitetomove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPice = self.board[endRow][endCol]
                if endPice[0] != allyColor:  # not on same color pice
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow,endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # place king on original square
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        self.getCastelMoves(r,c,moves, allyColor)

    '''
    generate castel moves for the king at (r,c) and then in list of moves
    '''
    def getCastelMoves(self,r, c, moves, allyColor):
        print("get castel move method called")
        incheck = self.squareUnderAttack(r, c, allyColor)
        print(incheck)

        if incheck:
            print("ofk")
            return
        if (self.whitetomove and self.whitecastleKingSide) or (not self.whitetomove and self.blackcastleKingSide):
            self.getKingsideCastelMoves(r, c, moves, allyColor)
        if (self.whitetomove and self.whitecastleQueenSide) or (not self.whitetomove and self.blackcastleQueenSide):
            self.getQueensideCastelMoves(r, c, moves, allyColor)


    '''
    generate castel moves for king side at king at (r,c), this method only call when we have king side castel rights
    '''
    def getKingsideCastelMoves(self, r, c, moves, allyColor):

        # check 2 square are empty or not between king and rookk and check the squares are under attack
        if self.board[r][c+1] == '__' and self.board[r][c+2] == '__' and \
            not self.squareUnderAttack(r, c+1, allyColor) and not self.squareUnderAttack(r, c+2, allyColor):
            moves.append(Move((r, c), (r, c+2), self.board, castel=True))
            print("king side castle move appende")

    '''
    generate castel moves for queen side at king at (r,c), this method only call when we have queen side castel rights
    '''

    def getQueensideCastelMoves(self, r, c, moves, allyColor):

        # check 2 square are empty or not between king and rookk and check the squares are under attack
        if self.board[r][c - 1] == '__' and self.board[r][c - 2] == '__' and self.board[r][c - 3] == '__' and \
                not self.squareUnderAttack(r, c - 1, allyColor) and not self.squareUnderAttack(r, c - 2, allyColor):
            moves.append(Move((r, c), (r, c - 2), self.board, castel=True))
            print("queen side castle move appende")




    '''
    check sq is under attack
    '''
    def squareUnderAttack(self, r, c, allyColor):
        #check outward from square
        enemyColor = 'w' if allyColor == 'b' else 'b'
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0<=endRow < 8 and 0<= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor: # not have attack
                        print("wea re break because sam color pice")
                        break
                    if endPiece[0] == enemyColor:
                        print("we are in enemy color")
                        type = endPiece[1]
                        if (0<= j <=3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5)) ) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            print("we are enter in if condition")
                            return True
                        else:
                            break
                    else:
                        break
                else:
                    break # off board

                # for knight
                knigntMoves = ((-2, -1), (-2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2), (2, -1), (2, 1))
                for m in knigntMoves:
                    endRow = r + m[0]
                    endCol = c + m[1]
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece[0] == enemyColor and endPiece[1] == 'N':  # enemy kinight attackinf king
                            return True
        return False


    def updateCastleRight(self,move):
        if move.piceMoved == 'wK':
            self.whitecastleKingSide = False
            self.whitecastleQueenSide = False
        elif move.piceMoved == 'bK':
            self.blackcastleKingSide= False
            self.blackcastleQueenSide = False
        elif move.piceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 7:
                    self.whitecastleKingSide = False
                elif move.startCol == 0:
                    self.whitecastleQueenSide = False
        elif move.piceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 7:
                    self.blackcastleKingSide = False
                elif move.startCol == 0:
                    self.blackcastleQueenSide = False
















    '''
    return if player king in check , list of pins , list of checks
    
    '''
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whitetomove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # check outward from king for pins and checks, keep track of pins
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () #reset possible pins
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0<=endRow < 8 and 0<= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # 2 ally pices , so no pin and check in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        #print("entet where enmy colr ")
                        type = endPiece[1]
                        # there are 5 possiblites in this complex condition
                        '''
                        1) orthogonally away from king & pice is rook
                        2) diagonally away from king & pice is bishop
                        3) 1 square awazy diagonally from king & pice is pawn 
                        4) Any direction from king & pice is queen
                        5) Any direction and 1 sq away and pice is king (this is necessary to prevent king 
                          move to square control by another king)
                          
                        '''
                        if (0<= j <=3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5)) ) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():# no pice blocking so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: # pice is blocking so pin
                                #print("in pin fun")
                                pins.append(possiblePin)
                                break
                        else:#enemy is not applying any check or pin
                            break
                else:
                    break #off the board


        '''check of knight checks'''
        knigntMoves = ((-2, -1), (-2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2), (2, -1), (2, 1))
        for m in knigntMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': #enemy kinight attackinf king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks




class CastleRights():
    def __init__(self,wks, bks, wqs, bqs):
        self.whitecastleKingSide = wks
        self.blackcastleKingSide = bks
        self.whitecastleQueenSide = wqs
        self.blackcastleQueenSide = bqs

















class Move():

    # map keys to values
    #key : value
    # so chess follow or describ emoves in rank and files like d4,a8,e5..etc so the conversin . rank = row && file == col
    ranksToRows ={"1": 7,"2": 6,"3": 5,"4": 4,"5": 3,"6": 2,
                  "7": 1,"8": 0, }
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesTocols = {"a" : 0, "b" : 1, "c" : 2,"d" : 3,"e" : 4,
                   "f" : 5, "g" : 6, "h" : 7,}
    colsToFiles ={v:k for k,v in filesTocols.items()}



    def __init__(self, startSq , endSQ , board, isEnpassantMove = False, castel = False): #taking parameters as tuple
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.piceMoved = board[startSq[0]][startSq[1]]
        self.piceCaptured = board[endSQ[0]][endSQ[1]]
        self.castel = castel

        # pawn promotion
        self.isPawnPromotion = False
        self.isPawnPromotion = (self.piceMoved == 'wp' and self.endRow == 0) or (self.piceMoved == 'bp' and self.endRow == 7)

        self.isEnpassantmove = isEnpassantMove
        if self.isEnpassantmove:
            self.piceCaptured = 'wp' if self.piceMoved == 'bp' else 'bp'

        self.moveId = self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol
        #print(self.moveId)

    '''
    overridding the equal method to compare 2 obj betwe valid and move by user
    '''
    def __eq__(self,other):
        if isinstance(other , Move):
            return self.moveId == other.moveId
        else:
            return False

    def getChessNotation(self):
        # get start and end position
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r , c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


