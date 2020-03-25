from configes.config import *
import pygame
import random


# Base class to draw bottom base image
class Base(object):
    def __init__(self, base_X):
        self.base_X = base_X
        self.tickIter = 0
        self.baseShift = SHIFT[0]

    # method to move bottom image, depends on birds currently flying
    def move(self, birds):
        if (self.tickIter + 1) % 2 == 5:
            for bird in birds:
                bird.next()
        self.tickIter = (self.tickIter + 1) % 20
        self.base_X = 0
