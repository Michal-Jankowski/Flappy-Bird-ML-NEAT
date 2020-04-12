from configes.Config import *
import pygame
import random


# Base class to draw bottom base image
class Base(object):
    VELOCITY = 5
    PIPE_WIDHT_SIZE = PIPEWIDTH

    def __init__(self, base_X):
        self.base_X_2 = 0
        self.base_X = base_X
        self.base_Y = self.PIPE_WIDHT_SIZE
        self.tickIter = 0
        self.baseShift = SHIFT[0]

    # method to move bottom image, depends on birds currently flying
    def move(self, birds):
        if (self.tickIter + 1) % 3 == 0:
            for bird in birds:
                bird.next()
        self.tickIter = (self.tickIter + 1) % 30
        self.base_X = 0

    def moveBase(self):

        self.base_X -= self.VELOCITY
        self.base_X_2 -= self.VELOCITY
        if self.base_X + self.PIPE_WIDHT_SIZE < 0:
            self.base_X = self.base_X_2 + self.PIPE_WIDHT_SIZE

        if self.base_X_2 + self.PIPE_WIDHT_SIZE < 0:
            self.base_X_2 = self.base_X + self.PIPE_WIDHT_SIZE

    # def draw(self, window):

    #   window.blit(self.PIPE[0], (self.base_X, self.base_Y))
    #   window.blit(self.PIPE[0], (self.base_X, self.base_Y))
