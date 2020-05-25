import neat
from configes.Config import *


# check collision form evert bir with pipes and ground
def checkCollision(rectangle_1, rectangle_2, hitmask_1, hitmask_2):
    rect = rectangle_1.clip(rectangle_2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rectangle_1.x, rect.y - rectangle_1.y
    x2, y2 = rect.x - rectangle_2.x, rect.y - rectangle_2.y

    for i in range(rect.width):
        for j in range(rect.height):
            if hitmask_1[x1 + i][y1 + j] and hitmask_2[x2 + i][y2 + j]:
                return True
    return False


class Bird(object):
    def __init__(self, player_index_gen, genome, config):
        # select bird sprite from config
        self.playerIndexGen = player_index_gen['playerIndexGen']
        self.x, self.y = int(SCREENWIDTH * 0.2), player_index_gen['playery']

        self.genome = genome
        self.neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        self.crashInfo = None
        self.index = 0
        self.start_ticks = pygame.time.get_ticks()
        self.y_velocity = -10  # bird's velocity along Y
        self.max_y_velocity = 12  # max Y velocity,  maximum descend speed
        self.gravity = 1  # players downoard accleration
        self.flap_speed = -10  # player's speed on flapping
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
        # if bird crashes into ground
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
                uCollide = checkCollision(playerRect, uPipeRect, pHitMask, uHitmask)
                lCollide = checkCollision(playerRect, lPipeRect, pHitMask, lHitmask)

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

    def crash_info(self, pipes, score, generation):
        crash_info = {
            'upperPipes': pipes.upper,
            'lowerPipes': pipes.lower,
            'generation': generation,
            'score': score,
            'network': self.neural_network,
            'genome': self.genome,
        }
        return crash_info

    def check_crash(self, pipes, score, generation):
        self.checkCollision(pipes)

        if self.collision:
            # Values returned to NEAT algorithm
            self.crashInfo = self.crash_info(pipes, score, generation)
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
                # can_flap = False
                return False
        else:
            # can_flap = True
            return True
