import random
from configes.Config import *


# class for setting properties of pipe
class Pipe(object):

    def __init__(self):
        # random.seed() if (RANDOM_PIPES) else random.seed(5)

        # y of gap between upper and lower pipe
        self.x_velocity = None
        gap_y = random.randrange(0, int(BASEY * 0.8 - PIPEGAPSIZE))
        gap_y += int(BASEY * 0.1)
        pipe_height = IMAGES['pipe'][0].get_height()
        pipe_x = SCREENWIDTH + 10
        pipe_y_upper = gap_y - pipe_height
        pipe_y_lower = gap_y + PIPEGAPSIZE

        self.x = pipe_x
        self.y_upper = pipe_y_upper
        self.y_lower = pipe_y_lower

        # move pipe to left

    def move_left(self):
        self.x += self.x_velocity

        # getter for (x,y)  coordinates of upper  pipe

    def get_upper(self):
        return {'x': self.x, 'y': self.y_upper}

        # getter for (x,y)  coordinates of lower  pipe

    def get_lower(self):
        return {'x': self.x, 'y': self.y_lower}


