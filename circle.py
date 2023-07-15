# This is a simple example of how the marching squares algorithm can be used.
# It displays a circle by passing a function which returns the distance from the origin; the
# marching_squares method then draws a curve for which this function attains the value 1.
import cv2 as cv
from main import *
from math import sqrt

blank = np.zeros((500, 1000, 3), dtype='uint8')

blank[:] = (40, 40, 40)

marching_squares(blank, lambda x, y: sqrt(x**2 + y**2), 10, 150, 1, (200, 35, 0), 3)

cv.imshow('Circle - marching squares example 1', blank)

cv.waitKey(0)