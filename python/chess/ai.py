def evaluate_board(board):
    piece_values = {
        'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
        'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
    }
    
    score = 0
    for i in range(8):
        for j in range(8):
            piece = board.board[i][j]
            if piece != '.':
                score += piece_values[piece]
                
                # Бонус за позицию (центр доски ценнее)
                if piece.upper() in ['P', 'N', 'B']:
                    center_distance = abs(3.5 - i) + abs(3.5 - j)
                    score += (4 - center_distance) * (1 if piece.isupper() else -1)
    
    return score

def negamax(board, depth, alpha, beta, is_white):
    if depth == 0:
        return evaluate_board(board) * (1 if is_white else -1), None
        
    best_move = None
    best_value = float('-inf')
    
    moves = board.get_legal_moves(is_white)
    if not moves:
        if board.is_in_check(is_white):
            return float('-inf'), None
        return 0, None
        
    for move in moves:
        new_board = board.copy()
        new_board.make_move(move)
        
        value, _ = negamax(new_board, depth - 1, -beta, -alpha, not is_white)
        value = -value
        
        if value > best_value:
            best_value = value
            best_move = move
            
        alpha = max(alpha, value)
        if alpha >= beta:
            break
            
    return best_value, best_move 