from board import Board
from ai import negamax
import time
import sys

def print_board(board):
    pieces = {
        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
        '.': '·'
    }
    print('  a b c d e f g h')
    for i in range(8):
        print(f"{8-i}", end=' ')
        for j in range(8):
            piece = board.board[i][j]
            print(pieces.get(piece, piece), end=' ')
        print(f"{8-i}")
    print('  a b c d e f g h')

def get_user_move():
    while True:
        try:
            move = input("Ваш ход (например, e2e4): ").strip().lower()
            if move in ['quit', 'exit', 'q']:
                raise KeyboardInterrupt
            if len(move) == 4:
                from_pos = (8 - int(move[1]), ord(move[0]) - ord('a'))
                to_pos = (8 - int(move[3]), ord(move[2]) - ord('a'))
                return (from_pos, to_pos)
        except KeyboardInterrupt:
            raise
        except:
            pass
        print("Неверный формат хода. Используйте формат 'e2e4' или 'quit' для выхода")

def get_difficulty():
    while True:
        print("\nВыберите уровень сложности:")
        print("1. Легкий (глубина 2)")
        print("2. Средний (глубина 3)")
        print("3. Сложный (глубина 4)")
        print("4. Очень сложный (глубина 5)")
        
        try:
            choice = input("Введите номер (1-4) или 'q' для выхода: ").lower()
            if choice in ['quit', 'exit', 'q']:
                raise KeyboardInterrupt
            choice = int(choice)
            if 1 <= choice <= 4:
                depths = {1: 2, 2: 3, 3: 4, 4: 5}
                return depths[choice]
        except KeyboardInterrupt:
            raise
        except ValueError:
            pass
        print("Пожалуйста, введите число от 1 до 4")

def play_game():
    print("Добро пожаловать в шахматы!")
    print("Для выхода в любой момент нажмите Ctrl+C или введите 'quit'")
    
    try:
        depth = get_difficulty()
        board = Board()
        
        while True:
            print_board(board)
            
            if board.is_in_check(True):
                print("Шах белому королю!")
            
            # Ход игрока
            while True:
                try:
                    move = get_user_move()
                    if board.is_valid_move(move, is_white=True):
                        board.make_move(move)
                        break
                    print("Недопустимый ход! Возможно, король останется под шахом.")
                except KeyboardInterrupt:
                    print("\nИгра прервана")
                    return
            
            if board.is_checkmate(False):
                print_board(board)
                print("Шах и мат! Вы победили!")
                break
            elif board.is_stalemate(False):
                print_board(board)
                print("Пат! Ничья!")
                break
                
            print("\nХод компьютера...")
            start_time = time.time()
            
            # Ход компьютера
            score, best_move = negamax(board, depth, float('-inf'), float('inf'), False)
            if best_move is None:
                print("Компьютер сдается!")
                break
                
            board.make_move(best_move)
            elapsed = time.time() - start_time
            print(f"Компьютер сделал ход за {elapsed:.1f} секунд")
            
            if depth >= 4:
                print(f"Оценка позиции: {score/100:.2f}")
            
            if board.is_in_check(True):
                print("Шах!")
            
            if board.is_checkmate(True):
                print_board(board)
                print("Шах и мат! Компьютер победил!")
                break
            elif board.is_stalemate(True):
                print_board(board)
                print("Пат! Ничья!")
                break

    except KeyboardInterrupt:
        print("\nИгра прервана")
        return

def main():
    while True:
        try:
            play_game()
            
            while True:
                try:
                    choice = input("\nХотите сыграть еще раз? (да/нет): ").lower()
                    if choice in ['н', 'нет', 'no', 'n', 'q', 'quit', 'exit']:
                        print("Спасибо за игру!")
                        return
                    if choice in ['д', 'да', 'yes', 'y']:
                        print("\n" + "="*50 + "\n")
                        break
                except KeyboardInterrupt:
                    print("\nСпасибо за игру!")
                    return
                
        except KeyboardInterrupt:
            print("\nСпасибо за игру!")
            return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nИгра завершена")
    sys.exit(0) 