from configes.Config import *


# Base class to draw bottom base image
class Base(object):
    velocity = 5
    pipe_width_size = pipe_width

    def __init__(self, base_x):
        self.base_X_2 = 0
        self.base_x = base_x
        self.base_y = self.pipe_width_size
        self.tick_iteration = 0
        self.baseShift = SHIFT[0]

    # method to move bottom image, depends on birds currently flying
    def move(self, birds):
        if (self.tick_iteration + 1) % 3 == 0:
            for bird in birds:
                bird.next()
        self.tick_iteration = (self.tick_iteration + 1) % 30
        self.base_x = -((-self.base_x + 5) % self.baseShift)

    def moveBase(self):

        self.base_x -= self.velocity
        self.base_X_2 -= self.velocity
        if self.base_x + self.pipe_width_size < 0:
            self.base_x = self.base_X_2 + self.pipe_width_size

        if self.base_X_2 + self.pipe_width_size < 0:
            self.base_X_2 = self.base_x + self.pipe_width_size

    # def draw(self, window):

    #   window.blit(self.PIPE[0], (self.base_X, self.base_Y))
    #   window.blit(self.PIPE[0], (self.base_X, self.base_Y))
