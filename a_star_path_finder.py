from tkinter import *
from time import sleep
import heapq
import numpy as np

# FIRST WE CREATE THE VISUALIZATION OF THE GRID
root = Tk()
root.title("A* Path Visualization")
tdelta = 0.2

canvas = Canvas(root, bg='white', width='600', height='620')
canvas.pack()

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 12
HEIGHT = 12

# This sets the margin between each cell
MARGIN = 3

# creating the grid
grid = [[0 for x in range(40)] for y in range(40)]

# start and end nodes
start_pos = (0, 0)
end_pos = (39, 39)

blocks = [[0 for x in range(40)] for y in range(40)]


# drawing the grid
for row in range(len(grid)):
    for col in range(len(grid[row])):
        color = 'grey'
        if grid[row][col] == 1:
            color = 'black'
        elif (row, col) == start_pos:
            color = 'green'
        elif (row, col) == end_pos:
            color = 'red'
        blocks[row][col] = canvas.create_rectangle((MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN,
                                                   (MARGIN + WIDTH) * col + (MARGIN + WIDTH),
                                                   (MARGIN + HEIGHT) * row + (MARGIN + HEIGHT), fill=color)
# instructions
canvas.create_text(300, 612, text="Draw walls, then press space to start the simulation. Press c to clear the board.")


# ADDING MOUSE EVENTS TO THE GRID (find a way to make this more accurate)
def cell_clicked(event):
    col_val = event.x // (WIDTH + MARGIN)
    row_val = event.y // (HEIGHT + MARGIN)

    if (canvas.itemcget(blocks[row_val][col_val], 'fill')) == 'grey':
        canvas.itemconfig(blocks[row_val][col_val], fill='black')
        grid[row_val][col_val] = 1


# calling the a* function and colouring the path yellow
def start_sim(event):
    pathway = astar(grid, start_pos, end_pos)

    for node in pathway:
        if node == end_pos:
            canvas.itemconfig(blocks[node[0]][node[1]], fill='red')
            canvas.update()
        else:
            canvas.itemconfig(blocks[node[0]][node[1]], fill='yellow')
            canvas.update()


# clear the board
def clear_board(event):
    for i in range(len(grid)):
        for j in range(len(grid[row])):
            if (i, j) != start_pos and (i, j) != end_pos:
                grid[i][j] = 0
                canvas.itemconfig(blocks[i][j], fill='grey')

    canvas.update()


canvas.bind('<B1-Motion>', cell_clicked)
canvas.focus_set()
canvas.bind('<Key-space>', start_sim)
canvas.bind('<Key-c>', clear_board)


# NEXT WE IMPLEMENT AND VISUALIZE A*
def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def astar(array, start, goal):
    canvas.itemconfig(blocks[start[0]][start[1]], fill='green')
    canvas.update()
    canvas.itemconfig(blocks[goal[0]][goal[1]], fill='red')
    canvas.update()

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)

        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j

            # Make sure within range
            if neighbor[0] > (len(array) - 1) or neighbor[0] < 0 or neighbor[1] > (
                    len(array[len(array) - 1]) - 1) or neighbor[1] < 0:
                continue

            # filling the squares blue according to the neighbors
            if neighbor != start and grid[neighbor[0]][neighbor[1]] != 1:
                canvas.itemconfig(blocks[neighbor[0]][neighbor[1]], fill='blue')
                canvas.update()

            tentative_g_score = gscore[current] + heuristic(current, neighbor)

            if 0 <= neighbor[0] < len(array):
                if 0 <= neighbor[1] < len(array[0]):
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))


canvas.mainloop()
