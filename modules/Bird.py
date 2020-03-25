import neat
from configes.config import *


# Bird class creates players


class Bird(object):
    def __init__(self, player_index_gen, genome, config):
        # select random player sprites
        self.playerIndexGen = player_index_gen['playerIndexGen']
        self.x, self.y = int(SCREENWIDTH * 0.2), player_index_gen['playery']
        # set genome and neural network
        self.genome = genome
        self.neural_network = neat.nn.FeedForwardNetwork.create(genome, config)

        self.index = 0
        self.distance = 0
        # player's velocity along Y, default same as playerFlapped
        self.y_velocity = -9
        # max vel along Y, max descend speed
        self.max_y_velocity = 10
        # players downward accleration
        self.gravity = 1
        # players speed on flapping
        self.flap_speed = -6
        # how much energy each flap uses
        self.energy_used = 0
        # check if bird flapped for energy purposes
        self.flapped = False

    # set index of bird to index of genome
    def next(self):
        self.index = next(self.playerIndexGen)

    # move bird
    def move(self):
        if self.y_velocity < self.max_y_velocity and not self.flapped:
            self.y_velocity += self.gravity
        if self.flapped:
            self.flapped = False
        player_Height = IMAGES['player'][self.index].get_height()
        self.y += min(self.y_velocity, BASEY - self.y - player_Height)
