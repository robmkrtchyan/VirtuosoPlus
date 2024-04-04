class Game:
    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.winner = None
        
    def getBoard(self):
        return self.board
        
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
        
    def play(row, col, round, game):
        if (game.isTaken(row, col) == False):
            game.setSquare(row, col, round % 2 + 1)
            return [game.getBoard(), "empty", game.isWinner()]
        else:
            return [game.getBoard(), "taken", game.isWinner()]       