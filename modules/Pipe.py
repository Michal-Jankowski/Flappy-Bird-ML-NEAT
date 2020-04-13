import random
from configes.Config import *


# class for setting properties of pipe
class Pipe(object):

    def __init__(self):
        # random.seed() if (RANDOM_PIPES) else random.seed(5)

        # y of gap between upper and lower pipe
        gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
        gapY += int(BASEY * 0.2)
        pipeHeight = IMAGES['pipe'][0].get_height()
        pipeX = SCREENWIDTH + 10
        pipeY_upper = gapY - pipeHeight
        pipeY_lower = gapY + PIPEGAPSIZE

        self.x = pipeX
        self.y_upper = pipeY_upper
        self.y_lower = pipeY_lower

        # move pipe to left

    def move_left(self):
        self.x += self.x_velocity

        # getter for (x,y)  coordinates of upper  pipe

    def get_upper(self):
        return {'x': self.x, 'y': self.y_upper}

        # getter for (x,y)  coordinates of lower  pipe

    def get_lower(self):
        return {'x': self.x, 'y': self.y_lower}


