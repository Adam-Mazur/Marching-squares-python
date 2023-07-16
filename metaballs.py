# This is another example illustrating the marching squares algorithm.
# Metaballs are special curves of an explicit function animated by giving them position and velocity
# and implementing a simple physics collision simulation.
# The marching squares algorithm is used to render this animation from the given explicit function.
import cv2 as cv
from main import *
import random
from math import sqrt

width = 100
height = 50

unit_length = 10

delta_t = 0.2

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

class Metaball:
    def __init__(self, radius: float, velocity: Vector, position: Vector):
        self.radius = radius
        self.velocity = velocity
        self.position = position

metaballs = []

for i in range(10):
    radius = random.uniform(1, 3)
    metaballs.append(
        Metaball(
            radius = radius,
            position = Vector(
                random.uniform(-width/2 + radius, width/2 - radius),
                random.uniform(-height/2 + radius, height/2 - radius),
            ),
            velocity = Vector(
                random.uniform(-4, 4),
                random.uniform(-4, 4),
            ),
        )
    )

while True:
    def func(x, y):
        sum = 0
        for metaball in metaballs:
            sum += metaball.radius/sqrt((x - metaball.position.x)**2 + (y - metaball.position.y)**2)
        return sum

    blank = np.zeros((height * unit_length, width * unit_length, 3), dtype='uint8')

    blank[:] = (50, 50, 50)
    
    marching_squares(
        blank, 
        func, 
        5, unit_length, 1, (245, 66, 167), 2
    )

    blank = cv.GaussianBlur(blank, (3,3), cv.BORDER_DEFAULT)

    cv.imshow("Metaballs - marching squares example 3", blank)

    for metaball in metaballs:
        metaball.position += metaball.velocity * delta_t

        if metaball.position.x < - width / 2 + metaball.radius or metaball.position.x > width / 2 - metaball.radius:
            metaball.velocity.x = - metaball.velocity.x 

        if metaball.position.y < - height / 2 + metaball.radius or metaball.position.y > height / 2 - metaball.radius:
            metaball.velocity.y = - metaball.velocity.y 


    # If the key d is pressed, close the window
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

cv.destroyAllWindows() 
