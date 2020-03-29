from itertools import cycle

import pygame

RANDOM_PIPES = True

FPS = 60
SCREENWIDTH = 512
SCREENHEIGHT = 512
SHIFT = [0]  # base shift of image
# amount by which base can maximum shift to left
PIPEGAPSIZE = 110  # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.79  # Base image shift value based on screenheight
# image dictionary
IMAGES = {}
HITMASKS = {}
PIPEWIDTH = [0]
# Player images
PLAYER = (
    (
        '../assets/sprites/yellowbird-upflap.png',
        '../assets/sprites/yellowbird-midflap.png',
        '../assets/sprites/yellowbird-downflap.png',
    ),
)

# Background image
BACKGROUND = ('../assets/sprites/background-day.png',)

# Pipes image
PIPE = ('../assets/sprites/pipe-green.png',)


# how maximum can shift the base image to background

def init_shift_info():
    SHIFT[0] = IMAGES['base'].get_width() - IMAGES['background'].get_width()


def load_images():
    # numbers sprites for score display
    IMAGES['numbers'] = tuple(
        [pygame.image.load('../assets/sprites/{}.png'.format(x)).convert_alpha() for x in range(10)])
    # load base image
    sprite_list = ["base", "scores"]

    for sprite in sprite_list:
        IMAGES[sprite] = pygame.image.load('../assets/sprites/{}.png'.format(sprite)).convert_alpha()


def init_random_sprites():
    # Choose background image
    IMAGES['background'] = pygame.image.load(BACKGROUND[0]).convert()

    # Choose player images
    IMAGES['player'] = tuple([pygame.image.load(PLAYER[0][i]).convert_alpha() for i in range(3)])

    # Choose pipe sprite
    IMAGES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE[0]).convert_alpha(), 180),
                      pygame.image.load(PIPE[0]).convert_alpha(),)


def init_movement_info():
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)
    PIPEWIDTH = int((IMAGES['base'].get_width()))
    base_X = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
    # player shm for up-down motion on welcome screen
    playerShmVals = {'val': 0, 'dir': 1}

    # make first flap sound and return values for mainGame
    return {'playery': playery + playerShmVals['val'],
            'basex': base_X,
            'playerIndexGen': playerIndexGen, }


# method that draws score writing and number of passed pipes
def displayScore(statistics, screen, text=None):
    try:
        DigitsNumbers = [int(x) for x in list(str(statistics))]
        total_Width = 0

        for number in DigitsNumbers:
            total_Width += IMAGES['numbers'][number].get_width()

        X_offset = (SCREENWIDTH - total_Width) / 2

    except:  # Should catch specific exception this is bad
        pass
        print("Info about error")

    if text == "scores":

        for digit in DigitsNumbers:
            screen.blit(IMAGES['numbers'][digit], (30, 470))

        screen.blit(IMAGES[text], (5, 430))


def get_Hitmask(image):
    mask = []
    for i in range(image.get_width()):
        mask.append([])
        for j in range(image.get_height()):
            mask[i].append(bool(image.get_at((i, j))[3]))
    return mask


# initailize hitmask collision

def ini_Hitmask():
    HITMASKS['player'] = (get_Hitmask(IMAGES['player'][0]),
                          get_Hitmask(IMAGES['player'][1]),
                          get_Hitmask(IMAGES['player'][2]),)

    HITMASKS['pipe'] = (get_Hitmask(IMAGES['pipe'][0]),
                        get_Hitmask(IMAGES['pipe'][1]),)


# run all methods from config to initialize resources

def load_all_resources():
    load_images()
    init_random_sprites()
    ini_Hitmask()
    init_shift_info()

    return init_movement_info()
