class TicTacToe:
    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.winner = None
        self.round = 1
    
    
        
    def getBoard(self):
        return self.board
    
    def setBoard(self, newBoard):
        self.board = newBoard
        
    def isTaken(self, row, col):
        if (self.board[row][col] > 0):
            return True
        return False
    
    def setSquare(self, row, col, player_number):
        self.board[row][col] = player_number
        
    def isWinner(self):
        #row winner
        if (self.board[0][0] == self.board[0][1] and self.board[0][0] == self.board[0][2]): return self.board[0][0]
        if (self.board[1][0] == self.board[1][1] and self.board[1][0] == self.board[1][2]): return self.board[1][0]
        if (self.board[2][0] == self.board[2][1] and self.board[2][0] == self.board[2][2]): return self.board[2][0]
        
        #col winner
        if (self.board[0][0] == self.board[1][0] and self.board[0][0] == self.board[2][0]): return self.board[0][0]
        if (self.board[0][1] == self.board[1][1] and self.board[0][1] == self.board[2][1]): return self.board[0][1]
        if (self.board[0][2] == self.board[1][2] and self.board[0][2] == self.board[2][2]): return self.board[0][2]
        
        #diagonal winner
        if (self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2]): return self.board[0][0]
        if (self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0]): return self.board[2][0]
    
    
    '''mekel es taki def xuynyanem avelacrel bayc eli chi ashatum xuyevo incha'''
    def check_winner(self):
        if all(self.isWinner()=='X'):
            return "winner is player X"
        elif all(self.isWinner()== 'O'):
            return 'Winner is player O'
        else:
            return 'nobody wins guys)'
    
    def posToRow(self, pos):
        row = pos//3
        return row
    
    def posToCol(self, pos):
        col = pos%3
        return col
    
    def play(self, pos):
        row = self.posToRow(pos)
        col = self.posToCol(pos)
        if (self.isTaken(row, col) == False):
            self.setSquare(row, col, self.round % 2 + 1)
            self.round += 1 
            return [self.getBoard(), "empty", self.isWinner()]
        else:
            return [self.getBoard(), "taken", self.isWinner()]
        
    def toXO(self):
        boardXO = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    boardXO.append("")
                elif self.board[row][col] == 2:
                    boardXO.append("X")
                elif self.board[row][col] == 1:
                    boardXO.append("O")
                
        return boardXO