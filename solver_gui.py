from tkinter import *
from tkinter import messagebox


# CREATING THE CANVAS
root = Tk()
root.title("Sudoku")
root.iconbitmap('sudoku.png')
MARGIN = 10
WIDTH = 50
HEIGHT = 50

canvas = Canvas(root, bg='white', width='470', height='500')
canvas.pack()

board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

solved_board = [
        [7, 8, 5, 4, 3, 9, 1, 2, 6],
        [6, 1, 2, 8, 7, 5, 3, 4, 9],
        [4, 9, 3, 6, 2, 1, 5, 7, 8],
        [8, 5, 7, 9, 4, 3, 2, 6, 1],
        [2, 6, 1, 7, 5, 8, 9, 3, 4],
        [9, 3, 4, 1, 6, 2, 7, 8, 5],
        [5, 7, 8, 3, 9, 4, 6, 1, 2],
        [1, 2, 6, 5, 8, 7, 4, 9, 3],
        [3, 4, 9, 2, 1, 6, 8, 5, 7]
    ]


# GRID CLASS
class Grid:
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cubes = [[Cube(board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.green_square = None
        self.strikes = 0

    def draw(self):
        # drawing partition lines
        canvas.create_line(MARGIN + (self.width * 3), MARGIN, MARGIN + (self.width * 3), MARGIN + (self.height * 9),
                           width=4)
        canvas.create_line(MARGIN + (self.width * 6), MARGIN, MARGIN + (self.width * 6), MARGIN + (self.height * 9),
                           width=4)
        canvas.create_line(MARGIN, MARGIN + (self.height * 3), MARGIN + (self.width * 9), MARGIN + (self.height * 3),
                           width=4)
        canvas.create_line(MARGIN, MARGIN + (self.height * 6), MARGIN + (self.width * 9), MARGIN + (self.height * 6),
                           width=4)

        # drawing outer box lines
        canvas.create_line(MARGIN, MARGIN, MARGIN + (self.width * 9), MARGIN,
                           width=4)
        canvas.create_line(MARGIN, MARGIN + (self.height * 9), MARGIN + (self.width * 9), MARGIN + (self.height * 9),
                           width=4)
        canvas.create_line(MARGIN, MARGIN, MARGIN, MARGIN + (self.height * 9),
                           width=4)
        canvas.create_line(MARGIN + (self.width * 9), MARGIN, MARGIN + (self.width * 9), MARGIN + (self.height * 9),
                           width=4)

        # drawing cubes
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[i])):
                self.cubes[i][j].draw()

        # solve message
        canvas.create_text(MARGIN * 23, MARGIN + (self.height * 9) + MARGIN,
                           text='(press space to visualize solve using backtracking algorithm)')

    def select_cell(self, row_num, col_num):
        # make sure only one cell is selected by adding selected variable
        if self.green_square is not None:
            canvas.delete(self.green_square)
            self.selected = None
        if 0 <= row_num <= 8 and 0 <= col_num <= 8:
            self.green_square = canvas.create_rectangle(MARGIN + (self.width * col_num), MARGIN + (self.height * row_num),
                                                        MARGIN + (self.width * col_num) + self.width,
                                                        MARGIN + (self.height * row_num) + self.height, outline='green')
            self.selected = (row_num, col_num)
            # print(self.selected)


# CUBE CLASS
class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.penciled_value = None
        self.row = row
        self.col = col
        self.width = width
        self.height = height

    def draw(self):
        # drawing cube
        canvas.create_rectangle(MARGIN + (self.width * self.col), MARGIN + (self.height * self.row),
                                MARGIN + (self.width * self.col) + self.width,
                                MARGIN + (self.height * self.row) + self.height)

        # drawing value in cube
        if self.value != 0:
            canvas.create_text(MARGIN + (self.width * self.col) + self.width / 2,
                               MARGIN + (self.height * self.row) + self.height / 2, text=self.value)


def cell_clicked(event):
    col_val = (event.x - MARGIN) // WIDTH
    row_val = (event.y - MARGIN) // HEIGHT

    grid.select_cell(row_val, col_val)


# BINDING KEYS
def key_pressed(event):
    if event.char == ' ':
        solve(board)
    elif event.char == '1':
        if grid.selected is not None and grid.cubes[grid.selected[0]][grid.selected[1]].value == 0:
            if grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value is not None:
                canvas.delete(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value)
            grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value = canvas.create_text(
                MARGIN + (WIDTH * grid.selected[1]) + (WIDTH / 2) + MARGIN,
                MARGIN + (HEIGHT * grid.selected[0]) + (HEIGHT / 2) - MARGIN, text='1', fill='grey')
    elif event.char == '2':
        if grid.selected is not None and grid.cubes[grid.selected[0]][grid.selected[1]].value == 0:
            if grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value is not None:
                canvas.delete(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value)
            grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value = canvas.create_text(
                MARGIN + (WIDTH * grid.selected[1]) + (WIDTH / 2) + MARGIN,
                MARGIN + (HEIGHT * grid.selected[0]) + (HEIGHT / 2) - MARGIN, text='2', fill='grey')
    elif event.char == '3':
        if grid.selected is not None and grid.cubes[grid.selected[0]][grid.selected[1]].value == 0:
            if grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value is not None:
                canvas.delete(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value)
            grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value = canvas.create_text(
                MARGIN + (WIDTH * grid.selected[1]) + (WIDTH / 2) + MARGIN,
                MARGIN + (HEIGHT * grid.selected[0]) + (HEIGHT / 2) - MARGIN, text='3', fill='grey')
    elif event.char == '4':
        if grid.selected is not None and grid.cubes[grid.selected[0]][grid.selected[1]].value == 0:
            if grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value is not None:
                canvas.delete(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value)
            grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value = canvas.create_text(
                MARGIN + (WIDTH * grid.selected[1]) + (WIDTH / 2) + MARGIN,
                MARGIN + (HEIGHT * grid.selected[0]) + (HEIGHT / 2) - MARGIN, text='4', fill='grey')
    elif event.char == '5':
        if grid.selected is not None and grid.cubes[grid.selected[0]][grid.selected[1]].value == 0:
            if grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value is not None:
                canvas.delete(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value)
            grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value = canvas.create_text(
                MARGIN + (WIDTH * grid.selected[1]) + (WIDTH / 2) + MARGIN,
                MARGIN + (HEIGHT * grid.selected[0]) + (HEIGHT / 2) - MARGIN, text='5', fill='grey')
    elif event.char == '6':
        if grid.selected is not None and grid.cubes[grid.selected[0]][grid.selected[1]].value == 0:
            if grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value is not None:
                canvas.delete(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value)
            grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value = canvas.create_text(
                MARGIN + (WIDTH * grid.selected[1]) + (WIDTH / 2) + MARGIN,
                MARGIN + (HEIGHT * grid.selected[0]) + (HEIGHT / 2) - MARGIN, text='6', fill='grey')
    elif event.char == '7':
        if grid.selected is not None and grid.cubes[grid.selected[0]][grid.selected[1]].value == 0:
            if grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value is not None:
                canvas.delete(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value)
            grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value = canvas.create_text(
                MARGIN + (WIDTH * grid.selected[1]) + (WIDTH / 2) + MARGIN,
                MARGIN + (HEIGHT * grid.selected[0]) + (HEIGHT / 2) - MARGIN, text='7', fill='grey')
    elif event.char == '8':
        if grid.selected is not None and grid.cubes[grid.selected[0]][grid.selected[1]].value == 0:
            if grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value is not None:
                canvas.delete(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value)
            grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value = canvas.create_text(
                MARGIN + (WIDTH * grid.selected[1]) + (WIDTH / 2) + MARGIN,
                MARGIN + (HEIGHT * grid.selected[0]) + (HEIGHT / 2) - MARGIN, text='8', fill='grey')
    elif event.char == '9':
        if grid.selected is not None and grid.cubes[grid.selected[0]][grid.selected[1]].value == 0:
            if grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value is not None:
                canvas.delete(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value)
            grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value = canvas.create_text(
                MARGIN + (WIDTH * grid.selected[1]) + (WIDTH / 2) + MARGIN,
                MARGIN + (HEIGHT * grid.selected[0]) + (HEIGHT / 2) - MARGIN, text='9', fill='grey')
    elif event.char == '\r':
        if grid.selected is not None:
            if grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value is not None:
                if canvas.itemcget(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value, 'text') == str(solved_board[grid.selected[0]][grid.selected[1]]):
                    # penciled value is correct
                    canvas.delete(grid.cubes[grid.selected[0]][grid.selected[1]].penciled_value)
                    grid.cubes[grid.selected[0]][grid.selected[1]].value = solved_board[grid.selected[0]][grid.selected[1]]
                    board[grid.selected[0]][grid.selected[1]] = solved_board[grid.selected[0]][grid.selected[1]]
                    grid.draw()
                else:
                    # penciled value is incorrect
                    # draw a red x
                    grid.strikes += 1
                    canvas.create_text(MARGIN + (10 * grid.strikes), 490, text='X', fill='red')
                    if grid.strikes == 3:
                        messagebox.showinfo('', 'Strike three, you lose!')
                        root.destroy()


# MAIN METHOD
grid = Grid(9, 9, 50, 50)
grid.draw()
canvas.bind('<Button-1>', cell_clicked)
canvas.focus_set()
canvas.bind('<Key>', key_pressed)


# BACKTRACKING ALGORITHM
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        projected_value = canvas.create_text(
                         MARGIN + (WIDTH * col) + WIDTH / 2,
                         MARGIN + (HEIGHT * row) + HEIGHT / 2, text=i, fill='black')

        if valid(bo, i, (row, col)):
            bo[row][col] = i
            canvas.itemconfig(projected_value, fill='green')
            canvas.update()
            canvas.itemconfig(projected_value, fill='black')
            canvas.update()

            if solve(bo):
                return True

            canvas.delete(projected_value)
            canvas.update()
            bo[row][col] = 0
        else:
            # make number red then delete it from the board
            canvas.itemconfig(projected_value, fill='red')
            canvas.update()
            canvas.delete(projected_value)
            canvas.update()

    return False


def valid(bo, num, pos):
    # check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - -')

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(' | ', end='')

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + ' ', end='')


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j  # row, col

    return None


canvas.mainloop()
