class Board:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        
    def copy(self):
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        return new_board
        
    def make_move(self, move):
        from_pos, to_pos = move
        self.board[to_pos[0]][to_pos[1]] = self.board[from_pos[0]][from_pos[1]]
        self.board[from_pos[0]][from_pos[1]] = '.'
        
    def get_all_moves(self, is_white):
        moves = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if self.is_piece_color(piece, is_white):
                    piece_moves = self.get_piece_moves((i, j))
                    moves.extend(((i, j), move) for move in piece_moves)
        return moves
        
    def is_piece_color(self, piece, is_white):
        return piece != '.' and piece.isupper() == is_white
        
    def get_piece_moves(self, pos):
        piece = self.board[pos[0]][pos[1]]
        moves = []
        
        if piece.upper() == 'P':
            moves.extend(self._get_pawn_moves(pos))
        elif piece.upper() == 'R':
            moves.extend(self._get_rook_moves(pos))
        elif piece.upper() == 'N':
            moves.extend(self._get_knight_moves(pos))
        elif piece.upper() == 'B':
            moves.extend(self._get_bishop_moves(pos))
        elif piece.upper() == 'Q':
            moves.extend(self._get_queen_moves(pos))
        elif piece.upper() == 'K':
            moves.extend(self._get_king_moves(pos))
            
        return moves
        
    def _get_pawn_moves(self, pos):
        moves = []
        direction = -1 if self.board[pos[0]][pos[1]].isupper() else 1
        start_row = 6 if direction == -1 else 1
        
        # Ход вперед на одну клетку
        if 0 <= pos[0] + direction < 8 and self.board[pos[0] + direction][pos[1]] == '.':
            moves.append((pos[0] + direction, pos[1]))
            
            # Ход вперед на две клетки с начальной позиции
            if pos[0] == start_row and self.board[pos[0] + 2*direction][pos[1]] == '.':
                moves.append((pos[0] + 2*direction, pos[1]))
        
        # Взятие по диагонали
        for j in [-1, 1]:
            if (0 <= pos[0] + direction < 8 and 0 <= pos[1] + j < 8 and
                self.board[pos[0] + direction][pos[1] + j] != '.' and
                self.is_piece_color(self.board[pos[0] + direction][pos[1] + j],
                                  not self.is_piece_color(self.board[pos[0]][pos[1]], True))):
                moves.append((pos[0] + direction, pos[1] + j))
                
        return moves
        
    def _get_rook_moves(self, pos):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for direction in directions:
            for i in range(1, 8):
                new_pos = (pos[0] + i*direction[0], pos[1] + i*direction[1])
                if not (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8):
                    break
                    
                target = self.board[new_pos[0]][new_pos[1]]
                if target == '.':
                    moves.append(new_pos)
                elif self.is_piece_color(target, not self.is_piece_color(self.board[pos[0]][pos[1]], True)):
                    moves.append(new_pos)
                    break
                else:
                    break
                    
        return moves
        
    def _get_knight_moves(self, pos):
        moves = []
        offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                   (1, 2), (1, -2), (-1, 2), (-1, -2)]
                   
        for offset in offsets:
            new_pos = (pos[0] + offset[0], pos[1] + offset[1])
            if (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8 and
                (self.board[new_pos[0]][new_pos[1]] == '.' or
                 self.is_piece_color(self.board[new_pos[0]][new_pos[1]],
                                   not self.is_piece_color(self.board[pos[0]][pos[1]], True)))):
                moves.append(new_pos)
                
        return moves
        
    def _get_bishop_moves(self, pos):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for direction in directions:
            for i in range(1, 8):
                new_pos = (pos[0] + i*direction[0], pos[1] + i*direction[1])
                if not (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8):
                    break
                    
                target = self.board[new_pos[0]][new_pos[1]]
                if target == '.':
                    moves.append(new_pos)
                elif self.is_piece_color(target, not self.is_piece_color(self.board[pos[0]][pos[1]], True)):
                    moves.append(new_pos)
                    break
                else:
                    break
                    
        return moves
        
    def _get_queen_moves(self, pos):
        return self._get_rook_moves(pos) + self._get_bishop_moves(pos)
        
    def _get_king_moves(self, pos):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
                     
        for direction in directions:
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8 and
                (self.board[new_pos[0]][new_pos[1]] == '.' or
                 self.is_piece_color(self.board[new_pos[0]][new_pos[1]],
                                   not self.is_piece_color(self.board[pos[0]][pos[1]], True)))):
                moves.append(new_pos)
                
        return moves
        
    def is_in_check(self, is_white):
        # Найдем позицию короля
        king_pos = None
        king = 'K' if is_white else 'k'
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == king:
                    king_pos = (i, j)
                    break
            if king_pos:
                break
                
        # Проверим, может ли какая-либо фигура противника атаковать короля
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != '.' and self.is_piece_color(piece, not is_white):
                    moves = self.get_piece_moves((i, j))
                    if king_pos in moves:
                        return True
        return False

    def is_move_legal(self, move, is_white):
        # Проверяем, не оставляет ли ход короля под шахом
        new_board = self.copy()
        new_board.make_move(move)
        return not new_board.is_in_check(is_white)

    def get_legal_moves(self, is_white):
        # Получаем все возможные ходы и фильтруем те, которые оставляют короля под шахом
        all_moves = self.get_all_moves(is_white)
        return [move for move in all_moves if self.is_move_legal(move, is_white)]

    def is_checkmate(self, is_white):
        # Мат - это когда король под шахом и нет легальных ходов
        return self.is_in_check(is_white) and len(self.get_legal_moves(is_white)) == 0

    def is_stalemate(self, is_white):
        # Пат - это когда король не под шахом, но нет легальных ходов
        return not self.is_in_check(is_white) and len(self.get_legal_moves(is_white)) == 0

    def is_valid_move(self, move, is_white):
        from_pos, to_pos = move
        if not (0 <= from_pos[0] < 8 and 0 <= from_pos[1] < 8 and
                0 <= to_pos[0] < 8 and 0 <= to_pos[1] < 8):
            return False
            
        piece = self.board[from_pos[0]][from_pos[1]]
        if piece == '.' or self.is_piece_color(piece, not is_white):
            return False
            
        valid_moves = self.get_piece_moves(from_pos)
        return to_pos in valid_moves and self.is_move_legal(move, is_white)