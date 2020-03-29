import neat
from configes.Config import *


def pixelPerfectCollision(rect1, rect2, hitmask1, hitmask2):
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False


class Bird(object):
    def __init__(self, player_index_gen, genome, config):
        # select random player sprites
        self.playerIndexGen = player_index_gen['playerIndexGen']
        self.x, self.y = int(SCREENWIDTH * 0.2), player_index_gen['playery']

        self.genome = genome
        self.neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        self.crashInfo = None
        self.index = 0
        self.distance = 0
        self.start_ticks = pygame.time.get_ticks()
        self.y_velocity = -10  # player's velocity along Y, default same as playerFlapped
        self.max_y_velocity = 12  # max vel along Y, max descend speed
        self.gravity = 1  # players downward accleration
        self.flap_speed = -10  # players speed on flapping
        self.energy_used = 0

        self.can_flap = True
        self.ground_collision = False
        self.pipe_collision = False
        self.collision = False
        self.flapped = False

    def next(self):
        self.index = next(self.playerIndexGen)

    def move(self):
        if self.y_velocity < self.max_y_velocity and not self.flapped:
            self.y_velocity += self.gravity
        if self.flapped:
            self.flapped = False
        playerHeight = IMAGES['player'][self.index].get_height()
        self.y += min(self.y_velocity, BASEY - self.y - playerHeight)

    def checkCollision(self, pipes):
        player = {'w': IMAGES['player'][0].get_width(), 'h': IMAGES['player'][0].get_height()}
        # if player crashes into ground
        if self.y + player['h'] >= BASEY - 1:
            self.ground_collision = True
        else:
            playerRect = pygame.Rect(self.x, self.y,
                                     player['w'], player['h'])
            pipeW = IMAGES['pipe'][0].get_width()
            pipeH = IMAGES['pipe'][0].get_height()

            for uPipe, lPipe in zip(pipes.upper, pipes.lower):
                # upper and lower pipe rects
                uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
                lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

                # player and upper/lower pipe hitmasks
                pHitMask = HITMASKS['player'][self.index]
                uHitmask = HITMASKS['pipe'][0]
                lHitmask = HITMASKS['pipe'][1]

                # if bird collided with upipe or lpipe
                uCollide = pixelPerfectCollision(playerRect, uPipeRect, pHitMask, uHitmask)
                lCollide = pixelPerfectCollision(playerRect, lPipeRect, pHitMask, lHitmask)

                if uCollide or lCollide:
                    self.pipe_collision = True

        if self.ground_collision or self.pipe_collision:
            self.collision = True

    def flap_bird(self, pipes):

        inputNodes = (
            10000 * (pipes.upper[0]['x'] - self.x),
            10000 * (pipes.upper[0]['y'] - self.y),
            10000 * (pipes.lower[0]['y'] - self.y),
            10000 * (pipes.upper[1]['x'] - self.x),
            10000 * (pipes.upper[1]['y'] - self.y),
            10000 * (pipes.lower[1]['y'] - self.y),
        )

        outputNodes = self.neural_network.activate(inputNodes)

        if outputNodes[0] > 0.4:

            if self.y > -2 * IMAGES['player'][0].get_height():
                self.y_velocity = self.flap_speed
                self.flapped = True

    def crash_info(self, pipes, score):
        crashInfo = {
            'upperPipes': pipes.upper,
            'lowerPipes': pipes.lower,
            'score': score,
            'distance': self.distance * -1,
            'energy': self.energy_used,
            'network': self.neural_network,
            'genome': self.genome,
        }
        return crashInfo

    def check_crash(self, pipes, basex, score):
        self.checkCollision(pipes)

        if self.collision:
            # Values returned to species.py
            self.crashInfo = self.crash_info(pipes, score)
            return True
        else:
            return False

    def timerForBird(self):
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if not self.flapped:
            if seconds >= 0.017:
                self.can_flap = True
                self.start_ticks = pygame.time.get_ticks()
                return True
            else:
                #self.can_flap = False
                return False
        else:
            #self.can_flap = False
            return True

