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
    sprite_list = ["base", "scores", "alive", "gen"]

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

    player_x = int(SCREENWIDTH * 0.2)
    player_y = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)
    PIPEWIDTH = int((IMAGES['base'].get_width()))
    base_x = 0
    # amount by which base can maximum shift to left
    base_shift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
    # player shm for up-down motion on welcome screen
    player_move = {'val': 0, 'dir': 1}

    # make first flap sound and return values for mainGame
    return {'playery': player_y + player_move['val'],
            'basex': base_x,
            'playerIndexGen': playerIndexGen, }


def oneScore(screen, digital_numbers, text):
    screen.blit(IMAGES['numbers'][digital_numbers[0]], (30, 470))
    screen.blit(IMAGES[text], (5, 430))


def twoScore(screen, digital_numbers, text):
    screen.blit(IMAGES['numbers'][digital_numbers[0]], (5, 470))
    screen.blit(IMAGES['numbers'][digital_numbers[1]], (30, 470))
    screen.blit(IMAGES[text], (5, 430))


def threeGeneration(screen, digital_numbers, text):
    screen.blit(IMAGES['numbers'][digital_numbers[0]], (0, 350))
    screen.blit(IMAGES['numbers'][digital_numbers[1]], (30, 350))
    screen.blit(IMAGES['numbers'][digital_numbers[2]], (50, 350))
    screen.blit(IMAGES[text], (5, 330))


def twoGeneration(screen, digital_numbers, text):
    screen.blit(IMAGES['numbers'][digital_numbers[0]], (0, 350))
    screen.blit(IMAGES['numbers'][digital_numbers[1]], (30, 350))
    screen.blit(IMAGES[text], (5, 330))


def oneGeneration(screen, digital_numbers, text):
    screen.blit(IMAGES['numbers'][digital_numbers[0]], (30, 350))
    screen.blit(IMAGES[text], (5, 330))


# method that draws score writing and number of passed pipes
def displayGameInformation(statistics, screen, text=None):

    digital_numbers = [int(x) for x in list(str(statistics))]

    if text == "scores":

        if len(digital_numbers) == 1:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (30, 470))
            screen.blit(IMAGES[text], (5, 430))
        else:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (5, 470))
            screen.blit(IMAGES['numbers'][digital_numbers[1]], (30, 470))
            screen.blit(IMAGES[text], (5, 430))
    elif text == "alive":

        if len(digital_numbers) == 1:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (30, 350))
            screen.blit(IMAGES[text], (5, 330))
        elif len(digital_numbers) == 2:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (0, 350))
            screen.blit(IMAGES['numbers'][digital_numbers[1]], (30, 350))
            screen.blit(IMAGES[text], (5, 330))
        else:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (5, 350))
            screen.blit(IMAGES['numbers'][digital_numbers[1]], (30, 350))
            screen.blit(IMAGES['numbers'][digital_numbers[2]], (50, 350))
            screen.blit(IMAGES[text], (5, 330))

    elif text == "gen":

        if len(digital_numbers) == 1:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (30, 150))
            screen.blit(IMAGES[text], (5, 130))
        elif len(digital_numbers) == 2:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (0, 150))
            screen.blit(IMAGES['numbers'][digital_numbers[1]], (30, 150))
            screen.blit(IMAGES[text], (5, 130))


def get_Hitmask(image):
    mask = []
    for i in range(image.get_width()):
        mask.append([])
        for j in range(image.get_height()):
            mask[i].append(bool(image.get_at((i, j))[3]))
    return mask


# initailize hitmask collision

def init_Hitmask():
    HITMASKS['player'] = (get_Hitmask(IMAGES['player'][0]),
                          get_Hitmask(IMAGES['player'][1]),
                          get_Hitmask(IMAGES['player'][2]),)

    HITMASKS['pipe'] = (get_Hitmask(IMAGES['pipe'][0]),
                        get_Hitmask(IMAGES['pipe'][1]),)


# run all methods from config to initialize resources

def load_all_resources():
    load_images()
    init_random_sprites()
    init_Hitmask()
    init_shift_info()

    return init_movement_info()
