import tkinter as tk
import random


SIZE = 4
CELL_SIZE = 100
GAP = 10

BACKGROUND_COLOR = "#bbada0"
EMPTY_COLOR = "#cdc1b4"

COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}


class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048")

        self.score = 0
        self.board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

        self.frame = tk.Frame(
            self.window,
            bg=BACKGROUND_COLOR,
            width=SIZE * CELL_SIZE,
            height=SIZE * CELL_SIZE
        )
        self.frame.grid()

        self.cells = []
        self.create_grid()

        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()

        self.window.bind("<Left>", lambda event: self.move("left"))
        self.window.bind("<Right>", lambda event: self.move("right"))
        self.window.bind("<Up>", lambda event: self.move("up"))
        self.window.bind("<Down>", lambda event: self.move("down"))

        self.window.mainloop()

    def create_grid(self):
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                cell = tk.Label(
                    self.frame,
                    text="",
                    bg=EMPTY_COLOR,
                    width=4,
                    height=2,
                    font=("Arial", 32, "bold")
                )
                cell.grid(row=i, column=j, padx=GAP, pady=GAP)
                row.append(cell)
            self.cells.append(row)

    def update_grid(self):
        for i in range(SIZE):
            for j in range(SIZE):
                value = self.board[i][j]

                if value == 0:
                    self.cells[i][j].config(
                        text="",
                        bg=COLORS[0],
                        fg="#776e65"
                    )
                else:
                    color = COLORS.get(value, "#3c3a32")
                    text_color = "#776e65" if value <= 4 else "#f9f6f2"

                    self.cells[i][j].config(
                        text=str(value),
                        bg=color,
                        fg=text_color
                    )

    def add_new_tile(self):
        empty_cells = []

        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))

        if not empty_cells:
            return

        i, j = random.choice(empty_cells)

        if random.random() < 0.9:
            self.board[i][j] = 2
        else:
            self.board[i][j] = 4

    def compress_and_merge_row(self, row):
        # 1. 去掉所有 0
        numbers = [num for num in row if num != 0]

        # 2. 合并相邻且相同的数字
        result = []
        skip = False

        for i in range(len(numbers)):
            if skip:
                skip = False
                continue

            if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
                merged = numbers[i] * 2
                result.append(merged)
                self.score += merged
                skip = True
            else:
                result.append(numbers[i])

        # 3. 补 0 到长度为 4
        while len(result) < SIZE:
            result.append(0)

        return result

    def move_left(self):
        new_board = []

        for row in self.board:
            new_row = self.compress_and_merge_row(row)
            new_board.append(new_row)

        self.board = new_board

    def move_right(self):
        new_board = []

        for row in self.board:
            reversed_row = row[::-1]
            new_row = self.compress_and_merge_row(reversed_row)
            new_board.append(new_row[::-1])

        self.board = new_board

    def move_up(self):
        self.transpose()
        self.move_left()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.move_right()
        self.transpose()

    def transpose(self):
        new_board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

        for i in range(SIZE):
            for j in range(SIZE):
                new_board[j][i] = self.board[i][j]

        self.board = new_board

    def move(self, direction):
        old_board = [row[:] for row in self.board]

        if direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        elif direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()

        if self.board != old_board:
            self.add_new_tile()
            self.update_grid()

            if self.is_game_over():
                self.show_game_over()

    def is_game_over(self):
        # 还有空格，就没结束
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == 0:
                    return False

        # 横向还能合并，就没结束
        for i in range(SIZE):
            for j in range(SIZE - 1):
                if self.board[i][j] == self.board[i][j + 1]:
                    return False

        # 纵向还能合并，就没结束
        for i in range(SIZE - 1):
            for j in range(SIZE):
                if self.board[i][j] == self.board[i + 1][j]:
                    return False

        return True

    def show_game_over(self):
        game_over_window = tk.Toplevel(self.window)
        game_over_window.title("Game Over")

        label = tk.Label(
            game_over_window,
            text=f"Game Over!\nScore: {self.score}",
            font=("Arial", 24, "bold"),
            padx=30,
            pady=30
        )
        label.pack()


Game2048()