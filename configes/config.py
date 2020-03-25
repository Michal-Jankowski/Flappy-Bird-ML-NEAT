import pygame, random
from itertools import cycle

RANDOM_PIPES = True

FPS = 60
SCREENWIDTH = 512
SCREENHEIGHT = 512
SHIFT = [0]  # base shift of image

# amount by which base can maximum shift to left
PIPEGAPSIZE = 90  # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.79
# image dictionary
IMAGES = {}

# Player images
PLAYER = (
    (
        '../assets/sprites/yellowbird-upflap.png',
        '../assets/sprites/yellowbird-midflap.png',
        '../assets/sprites/yellowbird-downflap.png',
    ),
)

# Background image
BACKGROUND = (
    '../assets/sprites/background-day.png',
)

# Pipes image
PIPE = (
    '../assets/sprites/pipe-green.png',
)


def load_images():
    # load base image
    sprite_list = ["base"]

    for sprite in sprite_list:
        IMAGES[sprite] = pygame.image.load(
            '../assets/sprites/{}.png'.format(sprite)).convert_alpha()


def init_random_sprites():
    # Choose background image
    IMAGES['background'] = pygame.image.load(BACKGROUND[0]).convert()

    # Choose player images
    IMAGES['player'] = tuple([pygame.image.load(PLAYER[0][i]).convert_alpha() for i in range(3)])

    # Choose pipe sprite
    IMAGES['pipe'] = (
        pygame.transform.rotate(
            pygame.image.load(PIPE[0]).convert_alpha(), 180),
        pygame.image.load(PIPE[0]).convert_alpha(),
    )


def init_movement_info():
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    base_X = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player shm for up-down motion on welcome screen
    playerShmVals = {'val': 0, 'dir': 1}

    # make first flap sound and return values for mainGame
    return {'playery': playery + playerShmVals['val'],
            'basex': base_X,
            'playerIndexGen': playerIndexGen, }


# run all methods from config to initialize resources
def load_all_resources():
    load_images()
    init_random_sprites()
    #  how maximum can shift the base image to background
    SHIFT[0] = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    return init_movement_info()
