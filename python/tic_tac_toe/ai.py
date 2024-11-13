class AI:
    def __init__(self, player='O'):
        self.player = player
        self.opponent = 'X' if player == 'O' else 'O'
        
    def get_best_move(self, board):
        # Первый ход - в центр или угол
        if len(board.get_empty_cells()) == 9:
            if board.is_valid_move(1, 1):
                return (1, 1)
            return (0, 0)
            
        # Проверяем выигрышный ход
        winning_move = self.find_winning_move(board, self.player)
        if winning_move:
            return winning_move
            
        # Блокируем выигрышный ход противника
        blocking_move = self.find_winning_move(board, self.opponent)
        if blocking_move:
            return blocking_move
            
        # Полный перебор оставшихся ходов с помощью Negamax
        best_score = float('-inf')
        best_move = None
        
        for row, col in board.get_empty_cells():
            board.make_move(row, col)
            score = -self.negamax(board, 0)  # Минус, потому что следующий ход противника
            board.undo_move(row, col)
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
                
        return best_move
        
    def find_winning_move(self, board, player):
        for row, col in board.get_empty_cells():
            board.make_move(row, col)
            if board.is_winner(player):
                board.undo_move(row, col)
                return (row, col)
            board.undo_move(row, col)
        return None
        
    def negamax(self, board, depth):
        # Проверяем терминальные состояния
        if board.is_winner(board.current_player):
            return 100 - depth  # Выигрыш текущего игрока
        if board.is_winner('X' if board.current_player == 'O' else 'O'):
            return -(100 - depth)  # Выигрыш противника
        if not board.get_empty_cells():
            return 0  # Ничья
            
        best_score = float('-inf')
        for row, col in board.get_empty_cells():
            board.make_move(row, col)
            score = -self.negamax(board, depth + 1)  # Рекурсивный вызов с инверсией счета
            board.undo_move(row, col)
            best_score = max(best_score, score)
            
        return best_score