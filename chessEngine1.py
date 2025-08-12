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
        self.enpassantPossible = ()
        self.currentCastlingRights = CastleRights(True,True, True, True)
        self.castelRightlog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                            self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]

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

        #pawn promotion

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.piceMoved[0] + 'Q'

        #enpassant move
        if move.isEnpassantmove:
            self.board[move.startRow][move.endCol] = '__'



        # updating the enpassantPossible variablr/tuple
        if move.piceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # only 2 sq pawn advance
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        # make castle move
        if move.isCastleMove:
            print("iam in castel make move function")
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]# move rook
                self.board[move.endRow][move.endCol + 1] = "__"# empty moove rook space
            else:# queen side castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # move rook
                self.board[move.endRow][move.endCol - 2] = '__'


        #update castel rights whenever king or rook moves
        self.updateCastleRights(move)
        self.castelRightlog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))








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

            #undo en passant
            if move.isEnpassantmove:
                self.board[move.endRow][move.endCol] = '__' #leaving landing squre blank
                self.board[move.startRow][move.endCol] = move.piceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            # undo 2 sq pawn advance
            if move.piceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            #undo castel rights
            self.castelRightlog.pop()#get out the latest casteling rights object
            self.currentCastlingRights = self.castelRightlog[-1]#set current castel rights to previous

            #undo castle moves
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]  # move rook
                    self.board[move.endRow][move.endCol - 1] = "__"  # empty moove rook space
                else:  # queen side castle
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]  # move rook
                    self.board[move.endRow][move.endCol + 1] = '__'







    '''
    update castel right on the given move
    '''

    def updateCastleRights(self, move):
        if move.piceMoved == 'wk':
            self.currentCastlingRights.wks= False
            self.currentCastlingRights.wqs = False
        elif move.piceMoved == 'bk':

            self.currentCastlingRights.wbs= False
            self.currentCastlingRights.bqs = False
        elif move.piceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.piceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.bks = False





    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempcastlerights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                            self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
        # 1) generate all possible moves
        moves = self.getAllPossibleMoves()
        if self.whitetomove:
            self.getCastelMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastelMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)




        # 2) for all possible moves make moves
        for i in range(len(moves)-1, -1, -1):
            #print(moves[i])
            self.makeMove(moves[i])
            # 3)generate opp all moves
            # 4)for each of your opp moves check , if they attack your king
            self.whitetomove = not self.whitetomove
            if self.inCheck():
                print("i am in check")
                moves.remove(moves[i])#5)if they attack your king remove it from move list
            self.whitetomove = not self.whitetomove
            self.undoMove()
        if len(moves) == 0:#for checkmate and stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRights = tempcastlerights
        return moves











    '''
    determine if player is in check
    '''
    def inCheck(self):
        if self.whitetomove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])





    '''
    determine if enemy can attack squaree r,c
    '''

    def squareUnderAttack(self , r ,c):
        self.whitetomove = not self.whitetomove #switching the move to opponent pov
        oppMoves = self.getAllPossibleMoves()
        self.whitetomove = not self.whitetomove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False














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
        if self.whitetomove:
            if self.board[r-1][c] == "__": # 1 square pawn advance
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "__": # 2 square pawn advance
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >=0:
                if self.board[r-1][c-1][0] == "b": #enemy pice to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c-1), self.board, isEnpassantMove=True))

                    # capture
            if c+1 <=7:
                if self.board[r-1][c+1][0] == "b": #enemy pice to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c+1), self.board, isEnpassantMove=True))

        else:#black pawn move
            if self.board[r+1][c] == "__":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r+2][c] == "__": # 1 square pawn advance
                    moves.append(Move((r,c),(r+2,c),self.board))
                    #capture
            if c-1 >=0:
                if self.board[r+1][c-1][0] == "w": #enemy pice to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c-1), self.board, isEnpassantMove=True))

            if c+1 <=7:
                if self.board[r+1][c+1][0] == "w": #enemy pice to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c+1), self.board, isEnpassantMove=True))

        #add pawn promotion


    '''
        get all possible move for rrrrook at row ,colum and add it into list
        '''

    def getRookMoves(self, r, c, moves):
        direction = ((-1,0), (0,-1), (1,0),(0,1))# up,left,down,right
        enemyColor = "b" if self.whitetomove else "w"
        for d in direction:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0<= endRow < 8 and 0 <= endCol < 8:
                    endPice = self.board[endRow][endCol]
                    if endPice == "__":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPice[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:#same color pice
                        break
                else:#off board
                    break

    '''
        get all possible move for Knight at row ,colum and add it into list
        '''


    def getKnightMoves(self, r, c, moves):
        knigntMoves =((-2,-1),(-2,1),(-1,-2),(1,-2),(-1,2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whitetomove else "b"
        for m in  knigntMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPice = self.board[endRow][endCol]
                if endPice[0] != allyColor:# not on same color pice
                    moves.append(Move((r, c), (endRow, endCol), self.board))





    '''
        get all possible move for Bishop at row ,colum and add it into list
        '''

    def getBishopMoves(self, r, c, moves):
        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # leftup,righup,leftdown,rightdown
        enemyColor = "b" if self.whitetomove else "w"
        for d in direction:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
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
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.whitetomove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPice = self.board[endRow][endCol]
                if endPice[0] != allyColor:  # not on same color pice
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    '''
    generate all castling moves
    '''
    def getCastelMoves(self, r, c,moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whitetomove and self.currentCastlingRights.wks) or (not self.whitetomove and self.currentCastlingRights.bks):
            self.getKingsideCastelMoves(r, c, moves)
        if (self.whitetomove and self.currentCastlingRights.wqs) or (not self.whitetomove and self.currentCastlingRights.bqs):
            self.getQueensideCastelMoves(r, c, moves)

    '''
        generate castel moves for king side at king at (r,c), this method only call when we have king side castel rights
        '''

    def getKingsideCastelMoves(self, r, c, moves):

        # check 2 square are empty or not between king and rookk and check the squares are under attack
        if self.board[r][c + 1] == '__' and self.board[r][c + 2] == '__':
               if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                    moves.append(Move((r, c), (r, c + 2), self.board, iscastleMove=True))
                    print("king side castle move appende")


    def getQueensideCastelMoves(self, r, c, moves):

        # check 2 square are empty or not between king and rookk and check the squares are under attack
        if self.board[r][c - 1] == '__' and self.board[r][c - 2] == '__' and self.board[r][c - 3] == '__':
                if not self.squareUnderAttack(r, c - 1, ) and not self.squareUnderAttack(r, c - 2,):
                    moves.append(Move((r, c), (r, c - 2), self.board, iscastleMove=True))
                    print("queen side castle move appende")


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs






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



    def __init__(self, startSq , endSQ , board, isEnpassantMove = False, iscastleMove=False): #taking parameters as tuple
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.piceMoved = board[startSq[0]][startSq[1]]
        self.piceCaptured = board[endSQ[0]][endSQ[1]]
        self.isCastleMove = iscastleMove

        #pawn promotion
        self.isPawnPromotion = False
        self.isPawnPromotion = (self.piceMoved == 'wp' and self.endRow == 0) or (self.piceMoved == 'bp' and self.endRow == 7)


        # en passant move

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


