# Example of displaying an ellipse from an explicit function.
import cv2 as cv
from main import *

blank = np.zeros((500, 1000, 3), dtype='uint8')

blank[:] = (40, 40, 40)

marching_squares(blank, lambda x, y: x**2/4 + y**2/0.9, 10, 150, 1, (50, 180, 24), 3)

cv.imshow('Ellipse - marching squares example 2', blank)

cv.waitKey(0)