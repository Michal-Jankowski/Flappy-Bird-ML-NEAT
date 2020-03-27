import random, sys, os, pygame
import numpy as np

from pygame.locals import *
from configes.Config import *
from modules.Pipe import Pipe, Pipes
from modules.Bird import Bird
from modules.Base import Base


class GameAppManager(object):

    def __init__(self, genomes, config):
        global SCREEN, FPSCLOCK

        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption('BIAI FlappyGame')

        self.score = 0
        self.crash_info = []

        # Create player
        self.movementInfo = load_all_resources()
        self.birds = [Bird(self.movementInfo, genome, config) for genome in genomes]

        # Create pipes
        self.pipes = Pipes(Pipe(), Pipe())

        # Create base
        self.base = Base(self.movementInfo['basex'])

    def play(self):

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if self.on_loop():
                return
            else:
                self.on_render()

    def on_loop(self):
        # neural control of bird move, get value for move
        for bird in self.birds:
            bird.flap_bird(self.pipes)

        for index, bird in enumerate(self.birds):
            if bird.check_crash(self.pipes, self.base.base_X, self.score):
                self.crash_info.append((bird.crashInfo, bird.genome))
                del self.birds[index]
                if len(self.birds) == 0:
                    bird.specie_died = True
                    return True

        # move base image
        self.base.move(self.birds)
        # move bird (player)
        for bird in self.birds:
            bird.move()
        # move pipes
        self.pipes.move(self.birds)
        return False

    # render method
    def on_render(self):
        # draw background
        SCREEN.blit(IMAGES['background'], (0, 0))
        # draw pipes
        self.pipes.draw(SCREEN)
        # draw base image
        SCREEN.blit(IMAGES['base'], (self.base.base_X, BASEY))
        # draw birds
        for bird in self.birds:
            SCREEN.blit(IMAGES['player'][bird.index], (bird.x, bird.y))
        # update display
        pygame.display.update()
        # increase tick count
        FPSCLOCK.tick(FPS)


# main method of game
if __name__ == "__main__":
    game = GameAppManager()
    game.play()
