from time import sleep
from math import inf
from random import randint
class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        if (isMax):
            if (self.checkWinner() == 1):
                return self.winnerMaxUtility
        else:
            if (self.checkWinner() == -1):
                return self.winnerMinUtility

        score = 0
        if (isMax):
            currentPlayer = self.maxPlayer
            opponent = self.minPlayer
        else:
            currentPlayer = self.minPlayer
            opponent = self.maxPlayer
        # check each local board
        for startX, startY in self.globalIdx:
            # check two in a row 

            for i in range (3):
                # Check horizontally
                if self.board[startX + i][startY] == self.board[startX + i][startY + 1] == currentPlayer and self.board[startX + i][startY + 2] == '_':
                    score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
                if self.board[startX + i][startY] == self.board[startX + i][startY + 2] == currentPlayer and self.board[startX + i][startY + 1] == '_':
                    score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
                if self.board[startX + i][startY + 1] == self.board[startX + i][startY + 2] == currentPlayer and self.board[startX + i][startY] == '_':
                    score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
                # Check vertically
                if self.board[startX][startY + i] == self.board[startX + 1][startY + i] == currentPlayer and self.board[startX + 2][startY + i] == '_':
                    score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
                if self.board[startX][startY + i] == self.board[startX + 2][startY + i] == currentPlayer and self.board[startX + 1][startY + i] == '_':
                    score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
                if self.board[startX + 1][startY + i] == self.board[startX + 2][startY + i] == currentPlayer and self.board[startX][startY + i] == '_':
                    score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
            # Check diagonally
            if self.board[startX][startY] == self.board[startX + 1][startY + 1] == currentPlayer and self.board[startX + 2][startY + 2] == '_':
                score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
            if self.board[startX][startY] == self.board[startX + 2][startY + 2] == currentPlayer and self.board[startX + 1][startY + 1] == '_':
                score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
            if self.board[startX + 1][startY + 1] == self.board[startX + 2][startY + 2] == currentPlayer and self.board[startX][startY] == '_':
                score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
            if self.board[startX + 2][startY] == self.board[startX + 1][startY + 1] == currentPlayer and self.board[startX][startY + 2] == '_':
                score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
            if self.board[startX + 2][startY] == self.board[startX][startY + 2] == currentPlayer and self.board[startX + 1][startY + 1] == '_':
                score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
            if self.board[startX][startY + 2] == self.board[startX + 1][startY + 1] == currentPlayer and self.board[startX + 2][startY] == '_':
                score += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
            
            # check prevent three in a row
            for i in range (3):
                # Check horizontally
                if (self.board[startX + i][startY] == self.board[startX + i][startY + 1] == opponent and self.board[startX + i][startY + 2] == currentPlayer):
                    score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
                if (self.board[startX + i][startY] == self.board[startX + i][startY + 2] == opponent and self.board[startX + i][startY + 1] == currentPlayer):
                    score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
                if (self.board[startX + i][startY + 1] == self.board[startX + i][startY + 2] == opponent and self.board[startX + i][startY] == currentPlayer):
                    score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
                # Check vertically
                if (self.board[startX][startY + i] == self.board[startX + 1][startY + i] == opponent and self.board[startX + 2][startY + i] == currentPlayer):
                    score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
                if (self.board[startX][startY + i] == self.board[startX + 2][startY + i] == opponent and self.board[startX + 1][startY + i] == currentPlayer):
                    score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
                if (self.board[startX + 1][startY + i] == self.board[startX + 2][startY + i] == opponent and self.board[startX][startY + i] == currentPlayer):
                    score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
            # Check diagonally
            if (self.board[startX][startY] == self.board[startX + 1][startY + 1] == opponent and self.board[startX + 2][startY + 2] == currentPlayer):
                score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
            if (self.board[startX][startY] == self.board[startX + 2][startY + 2] == opponent and self.board[startX + 1][startY + 1] == currentPlayer):
                score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
            if (self.board[startX + 1][startY + 1] == self.board[startX + 2][startY + 2] == opponent and self.board[startX][startY] == currentPlayer):
                score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
            if (self.board[startX + 2][startY] == self.board[startX + 1][startY + 1] == opponent and self.board[startX][startY + 2] == currentPlayer):
                score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
            if (self.board[startX + 2][startY] == self.board[startX + 2][startY + 2] == opponent and self.board[startX][startY + 1] == currentPlayer):
                score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
            if (self.board[startX][startY + 2] == self.board[startX + 1][startY + 1] == opponent and self.board[startX + 2][startY] == currentPlayer):
                score += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
        if score > 0 or score < 0:
            return score
        # check corners
        for startX, startY in self.globalIdx:
            if self.board[startX][startY] == currentPlayer:
                score += self.cornerMaxUtility if isMax else self.cornerMinUtility
            if self.board[startX][startY + 2] == currentPlayer:
                score += self.cornerMaxUtility if isMax else self.cornerMinUtility
            if self.board[startX + 2][startY] == currentPlayer:
                score += self.cornerMaxUtility if isMax else self.cornerMinUtility
            if self.board[startX + 2][startY + 2] == currentPlayer:
                score += self.cornerMaxUtility if isMax else self.cornerMinUtility 
        return score


    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for row in self.board:
            if '_' in row:
                return True  # Found an empty spot, so moves are left
        return False  # No empty spots found, no moves left

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        for boardStart in self.globalIdx:
            startX, startY = boardStart
            for dx in range(3):
                for dy in range(3):
                    if self.board[startX + dx][startY + dy] != '_':
                        player = self.board[startX + dx][startY + dy]
                        # Check horizontally
                        if dy == 0 and self.board[startX + dx][startY + dy] == self.board[startX + dx][startY + dy + 1] == self.board[startX + dx][startY + dy + 2]:
                            return 1 if player == self.maxPlayer else -1
                        # Check vertically
                        if dx == 0 and self.board[startX + dx][startY + dy] == self.board[startX + dx + 1][startY + dy] == self.board[startX + dx + 2][startY + dy]:
                            return 1 if player == self.maxPlayer else -1
                        # Check diagonal (top-left to bottom-right)
                        if dx == 0 and dy == 0 and self.board[startX + dx][startY + dy] == self.board[startX + dx + 1][startY + dy + 1] == self.board[startX + dx + 2][startY + dy + 2]:
                            return 1 if player == self.maxPlayer else -1
                        # Check diagonal (bottom-left to top-right)
                        if dx == 2 and dy == 0 and self.board[startX + dx][startY + dy] == self.board[startX + dx - 1][startY + dy + 1] == self.board[startX + dx - 2][startY + dy + 2]:
                            return 1 if player == self.maxPlayer else -1
        return 0

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        if depth == self.maxDepth or self.checkWinner() != 0 or not self.checkMovesLeft():
            return self.evaluatePredifined(self.currPlayer)
        bestValue = -inf if isMax else inf

        startX, startY = self.globalIdx[currBoardIdx]
        for dx in range(3):
            for dy in range(3):
                if self.board[startX + dx][startY + dy] == '_':
                    self.board[startX + dx][startY + dy] = self.maxPlayer if isMax else self.minPlayer
                    value = self.alphabeta(depth + 1, (startX + dx) % 3 * 3 + (startY + dy) % 3, alpha, beta, not isMax)
                    self.board[startX + dx][startY + dy] = '_'
                    if isMax:
                        bestValue = max(bestValue, value)
                        alpha = max(alpha, bestValue)
                    else:
                        bestValue = min(bestValue, value)
                        beta = min(beta, bestValue)
                    if beta <= alpha:
                        return bestValue
        return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        if depth == self.maxDepth or self.checkWinner() != 0 or not self.checkMovesLeft():
            value = self.evaluatePredifined(self.currPlayers)
            return value
        bestValue = -inf if isMax else inf

        startX, startY = self.globalIdx[currBoardIdx]
        for dx in range(3):
            for dy in range(3):
                if self.board[startX + dx][startY + dy] == '_':
                    self.board[startX + dx][startY + dy] = self.maxPlayer if isMax else self.minPlayer
                    value = self.minimax(depth + 1, (startX + dx) % 3 * 3 + (startY + dy) % 3, not isMax)

                    self.board[startX + dx][startY + dy] = '_'
                    bestValue = max(bestValue, value) if isMax else min(bestValue, value)
        return bestValue
    
    def my_minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        if depth == self.maxDepth or self.checkWinner() != 0 or not self.checkMovesLeft():
            if (self.checkWinner() == 1 and self.currPlayers == False) or (self.checkWinner() == -1 and self.currPlayers == True):
                # this choice make the other side win
                return self.winnerMinUtility if self.currPlayers else self.winnerMaxUtility
            value = self.evaluatePredifined(self.currPlayers)
            return value
        bestValue = -inf if isMax else inf

        startX, startY = self.globalIdx[currBoardIdx]
        for dx in range(3):
            for dy in range(3):
                if self.board[startX + dx][startY + dy] == '_':
                    self.board[startX + dx][startY + dy] = self.maxPlayer if isMax else self.minPlayer
                    value = self.my_minimax(depth + 1, (startX + dx) % 3 * 3 + (startY + dy) % 3, not isMax)
                    self.board[startX + dx][startY + dy] = '_'
                    # if (value == self.winnerMinUtility and self.currPlayers == True) or (value == self.winnerMaxUtility and self.currPlayers == False):
                    #     return value
                    bestValue = max(bestValue, value) if isMax else min(bestValue, value)
        return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0

        alpha = -inf
        beta = inf
        current_board = self.startBoardIdx
        self.currPlayers = maxFirst
        expandedNodes = []
        node = 0
        while self.checkWinner() == 0 and self.checkMovesLeft():
            startX, startY = self.globalIdx[current_board]
            best_value = -inf if self.currPlayers else inf
            for i in range(3):
                for j in range(3):
                    if self.board[startX + i][startY + j] == '_':
                        self.board[startX + i][startY + j] = self.maxPlayer if self.currPlayers else self.minPlayer
                        if self.currPlayers:
                            if isMinimaxOffensive:
                                value = self.my_minimax(1, (startX + i) % 3 * 3 + (startY + j) % 3, not self.currPlayers)
                            else:
                                value = self.alphabeta(1, (startX + i) % 3 * 3 + (startY + j) % 3, alpha, beta, not self.currPlayers)
                        else:
                            if isMinimaxDefensive:
                                value = self.my_minimax(1, (startX + i) % 3 * 3 + (startY + j) % 3, not self.currPlayers)
                            else:
                                value = self.alphabeta(1, (startX + i) % 3 * 3 + (startY + j) % 3, alpha, beta, not self.currPlayers)
                        self.board[startX + i][startY + j] = '_'
                        if self.currPlayers:
                            if value > best_value:
                                best_value = value
                                best_move = (startX + i, startY + j)
                        else:
                            if value < best_value:
                                best_value = value
                                best_move = (startX + i, startY + j)
            bestMove.append(best_move)
            node += 1
            expandedNodes.append(node)
            bestValue.append(best_value)
            self.board[best_move[0]][best_move[1]] = self.maxPlayer if self.currPlayers else self.minPlayer
            gameBoards.append([row.copy() for row in self.board])
            current_board = (best_move[0] % 3) * 3 + (best_move[1] % 3)
            self.currPlayers = not self.currPlayers
            self.printGameBoard()
            print("best value", best_value)
            print()
        
        if self.checkWinner() == 1:
            winner = 1
        elif self.checkWinner() == -1:
            winner = -1
        return gameBoards, bestMove, expandedNodes, bestValue, winner    

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    # feel free to write your own test code
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,True,True)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")