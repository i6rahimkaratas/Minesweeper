import random

class Minesweeper:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.true_board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.mines_uncovered = 0
        self.setup_board()

    def setup_board(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.true_board[r][c] != 'M':
                self.true_board[r][c] = 'M'
                mines_placed += 1
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.true_board[r][c] == 'M':
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols and self.true_board[nr][nc] == 'M':
                            count += 1
                self.true_board[r][c] = str(count)

    def print_board(self, reveal=False):
        print("  " + " ".join(str(i) for i in range(self.cols)))
        print(" --" + "--" * self.cols)
        for r in range(self.rows):
            print(f"{r}|", end="")
            for c in range(self.cols):
                if reveal:
                    print(f"{self.true_board[r][c]} ", end="")
                else:
                    print(f"{self.board[r][c]} ", end="")
            print()

    def uncover(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols) or self.board[r][c] != ' ':
            return

        if self.true_board[r][c] == 'M':
            self.game_over = True
            print("Mayına bastınız! Oyun bitti.")
            self.print_board(reveal=True)
            return

        self.board[r][c] = self.true_board[r][c]
        self.mines_uncovered += 1

        if self.true_board[r][c] == '0':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    self.uncover(r + dr, c + dc)
    
    def check_win(self):
        total_non_mines = (self.rows * self.cols) - self.num_mines
        return self.mines_uncovered == total_non_mines

    def play(self):
        while not self.game_over:
            self.print_board()
            try:
                choice = input("Hücre açmak için 'a satir sutun', bayrak koymak için 'f satir sutun' girin (örn: a 0 0): ").split()
                action = choice[0]
                r = int(choice[1])
                c = int(choice[2])

                if action == 'a':
                    if self.board[r][c] == 'F':
                        print("Bayraklı bir hücreyi açamazsınız. Önce bayrağı kaldırın.")
                        continue
                    self.uncover(r, c)
                elif action == 'f':
                    if self.board[r][c] == ' ':
                        self.board[r][c] = 'F'
                    elif self.board[r][c] == 'F':
                        self.board[r][c] = ' '
                else:
                    print("Geçersiz işlem. Tekrar deneyin.")
            except (IndexError, ValueError):
                print("Geçersiz giriş. Lütfen doğru formatta girin.")
            
            if self.check_win():
                self.game_over = True
                self.print_board(reveal=True)
                print("Tebrikler! Oyunu kazandınız!")
        
if __name__ == "__main__":
    game = Minesweeper(8, 8, 10)
    game.play()
