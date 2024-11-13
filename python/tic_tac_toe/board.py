class Board:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        
    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def is_valid_move(self, row, col):
        if 0 <= row < 3 and 0 <= col < 3:
            return self.board[row][col] == ' '
        return False
        
    def get_empty_cells(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
        
    def is_winner(self, player):
        # Проверка строк и столбцов
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
                
        # Проверка диагоналей
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2-i] == player for i in range(3)):
            return True
            
        return False
        
    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or not self.get_empty_cells()
        
    def undo_move(self, row, col):
        self.board[row][col] = ' '
        self.current_player = 'O' if self.current_player == 'X' else 'X' 