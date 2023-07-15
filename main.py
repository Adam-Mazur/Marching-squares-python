import numpy as np
import cv2 as cv

def marching_squares(canvas: np.ndarray, func, cell_width: int, unit_length: float, isovalue: float, color: tuple, thickness: int) -> None:
    """This is the simplest implementation of the marching squares algorithm for openCV. 
    It draws a contour of a given function on a canvas. The [canvas] parameter is a ndarray in the shape of (height, width, 3), 
    [func] is the function to be drawn that takes two floats and returns a float, [cell_width] is the size in pixels of a single cell, or square,
    [unit_length] is the length in pixels of a single unit on an axis, [isovalue] is a the value of the function where the line should be drawn, 
    [color] is a tuple in the form of (B, G, R), [thickness] is the thickness of the line."""
    cell_width_in_units = cell_width / unit_length

    width = canvas.shape[1]//cell_width
    height = canvas.shape[0]//cell_width

    grid = np.zeros((width, height))
    
    for w in range(width):
        for h in range(height):
            grid[w][h] = func(cell_width_in_units * (w - width//2), - cell_width_in_units * (h - height//2))

    def linear_interpolation(a: float, b: float) -> float:
        return abs((isovalue - a)/(a - b))

    def draw(p1: tuple, p2: tuple):
        cv.line(canvas, (int(p1[0] * cell_width), int(p1[1] * cell_width)), (int(p2[0] * cell_width), int(p2[1] * cell_width)), color, thickness)

    for w in range(width - 1):
        for h in range(height - 1):
            cell = [0, 0, 0, 0]
            
            c0 = grid[w][h]
            c1 = grid[w + 1][h]
            c2 = grid[w + 1][h + 1]
            c3 = grid[w][h + 1]

            if c0 > isovalue: cell[0] = 1
            if c1 > isovalue: cell[1] = 1
            if c2 > isovalue: cell[2] = 1
            if c3 > isovalue: cell[3] = 1

            match cell:
                case [0, 0, 0, 0]:
                    pass
                case [0, 0, 0, 1]:
                    d1 = linear_interpolation(c3, c2)
                    d2 = linear_interpolation(c0, c3)
                    draw((w + d1, h + 1), (w, h + d2))
                case [0, 0, 1, 0]:
                    d1 = linear_interpolation(c3, c2)
                    d2 = linear_interpolation(c1, c2)
                    draw((w + d1, h + 1), (w + 1, h + d2))
                case [0, 0, 1, 1]:
                    d1 = linear_interpolation(c0, c3)
                    d2 = linear_interpolation(c1, c2)
                    draw((w, h + d1), (w + 1, h + d2))
                case [0, 1, 0, 0]:
                    d1 = linear_interpolation(c0, c1)
                    d2 = linear_interpolation(c1, c2)
                    draw((w + d1, h), (w + 1, h + d2))
                case [0, 1, 0, 1]:
                    d1 = linear_interpolation(c0, c1)
                    d2 = linear_interpolation(c1, c2)
                    d3 = linear_interpolation(c3, c2)
                    d4 = linear_interpolation(c0, c3)
                    draw((w, h + d4), (w + d1, h))
                    draw((w + d3, h + 1), (w + 1, h + d2))
                case [0, 1, 1, 0]:
                    d1 = linear_interpolation(c0, c1)
                    d2 = linear_interpolation(c3, c2)
                    draw((w + d1, h), (w + d2, h + 1))
                case [0, 1, 1, 1]:
                    d1 = linear_interpolation(c0, c1)
                    d2 = linear_interpolation(c0, c3)
                    draw((w, h + d2), (w + d1, h))
                case [1, 0, 0, 0]:
                    d1 = linear_interpolation(c0, c1)
                    d2 = linear_interpolation(c0, c3)
                    draw((w, h + d2), (w + d1, h))
                case [1, 0, 0, 1]:
                    d1 = linear_interpolation(c0, c1)
                    d2 = linear_interpolation(c3, c2)
                    draw((w + d1, h), (w + d2, h + 1))
                case [1, 0, 1, 0]:
                    d1 = linear_interpolation(c0, c1)
                    d2 = linear_interpolation(c1, c2)
                    d3 = linear_interpolation(c3, c2)
                    d4 = linear_interpolation(c0, c3)
                    draw((w + d1, h), (w + 1, h + d2))
                    draw((w, h + d4), (w + d3, h + 1))
                case [1, 0, 1, 1]:
                    d1 = linear_interpolation(c0, c1)
                    d2 = linear_interpolation(c1, c2)
                    draw((w + d1, h), (w + 1, h + d2))
                case [1, 1, 0, 0]:
                    d1 = linear_interpolation(c0, c3)
                    d2 = linear_interpolation(c1, c2)
                    draw((w, h + d1), (w + 1, h + d2))
                case [1, 1, 0, 1]:
                    d1 = linear_interpolation(c1, c2)
                    d2 = linear_interpolation(c3, c2)
                    draw((w + d2, h + 1), (w + 1, h + d1))
                case [1, 1, 1, 0]:
                    d1 = linear_interpolation(c0, c3)
                    d2 = linear_interpolation(c3, c2)
                    draw((w, h + d1), (w + d2, h + 1))
                case [1, 1, 1, 1]:
                    pass
