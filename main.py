from random import randrange
from time import sleep
from tkinter import *

root = Tk()
root.title("Bubble Sort Visualization")
canvas = Canvas(root, bg='white', width='800', height='500')
canvas.pack()


ndigits = 20
digits = [randrange(10) for i in range(ndigits)]
tdelta = .2
xstart = 110
xdelta = 30
ydigit = 80
ybar = 100


def color(i, swap):
    # temporarily color digits and bars i and i+i according to swap needed
    dcolor = 'Red' if swap else 'green'
    canvas.itemconfigure(items[i], fill=dcolor)
    canvas.itemconfigure(items[i+1], fill=dcolor)

    canvas.itemconfigure(bars[i], fill=dcolor)
    canvas.itemconfigure(bars[i + 1], fill=dcolor)

    canvas.update()
    sleep(tdelta)
    canvas.itemconfigure(items[i], fill='Black')
    canvas.itemconfigure(items[i+1], fill='Black')

    canvas.itemconfigure(bars[i], fill='grey')
    canvas.itemconfigure(bars[i + 1], fill='grey')

    canvas.update()
    sleep(tdelta)


def swap(i):
    digits[i], digits[i+1] = digits[i+1], digits[i]
    canvas.move(items[i], xdelta, 0)
    canvas.move(items[i+1], -xdelta, 0)
    items[i], items[i+1] = items[i+1], items[i]

    canvas.move(bars[i], 30, 0)
    canvas.move(bars[i + 1], -30, 0)
    bars[i], bars[i + 1] = bars[i + 1], bars[i]


def bubble_sort():
    # sort bars and digits and animate
    for stop in reversed(range(1, ndigits)):
        # stop = index of position whose entry will be determined.
        for i in range(stop):
            swap_needed = digits[i] > digits[i+1]
            color(i, swap_needed)
            if swap_needed:
                swap(i)
                color(i, False)


# Create display items and pause.
items = [canvas.create_text(xstart + xdelta*i, ydigit, text=str(digit))
         for i, digit in enumerate(digits)]

bars = [canvas.create_rectangle(120 + (30 * i), ybar + (20*digit), ybar + (30 * i), ybar, fill='grey') for i, digit in enumerate(digits)]

canvas.update()
sleep(tdelta)

bubble_sort()
canvas.mainloop()
