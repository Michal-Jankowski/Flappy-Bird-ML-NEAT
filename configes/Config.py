from itertools import cycle

import pygame

RANDOM_PIPES = True

FPS = 5000
SCREENWIDTH = 512
SCREENHEIGHT = 512
SHIFT = [0]  # base shift of image
# amount by which base can maximum shift to left
PIPEGAPSIZE = 110  # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.79  # Base image shift value based on screenheight
# image dictionary
IMAGES = {}
HITMASKS = {}
pipe_width = [0]
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
    val1 = IMAGES['base'].get_width()
    val2 = IMAGES['background'].get_width()
    SHIFT[0] = val1 - val2


def load_images():
    # numbers sprites for score display
    IMAGES['numbers'] = tuple(
        [pygame.image.load('../assets/sprites/{}.png'.format(x)).convert_alpha() for x in range(10)])
    # load base image
    sprite_list = ["base", "score", "alive", "generation"]

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
    player_index_gen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    player_y = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)
    base_x = 50
    # player shm for up-down motion on welcome screen
    player_move = {'val': 0, 'dir': 1}

    # make first flap sound and return values for mainGame
    return {'playery': player_y + player_move['val'],
            'basex': base_x,
            'playerIndexGen': player_index_gen, }


# method that draws score writing and number of passed pipes
def display_game_information(statistics, screen, text=None):
    digital_numbers = [int(x) for x in list(str(statistics))]

    if text == "score":

        if len(digital_numbers) == 1:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (30, 470))
            screen.blit(IMAGES[text], (5, 435))
        elif len(digital_numbers) == 2:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (5, 470))
            screen.blit(IMAGES['numbers'][digital_numbers[1]], (30, 470))
            screen.blit(IMAGES[text], (5, 435))
        else:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (5, 470))
            screen.blit(IMAGES['numbers'][digital_numbers[1]], (30, 470))
            screen.blit(IMAGES['numbers'][digital_numbers[2]], (55, 470))
            screen.blit(IMAGES[text], (5, 430))

    elif text == "alive":

        if len(digital_numbers) == 1:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (120, 470))
            screen.blit(IMAGES[text], (105, 430))
        elif len(digital_numbers) == 2:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (120, 470))
            screen.blit(IMAGES['numbers'][digital_numbers[1]], (145, 470))
            screen.blit(IMAGES[text], (105, 430))
        else:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (95, 470))
            screen.blit(IMAGES['numbers'][digital_numbers[1]], (120, 470))
            screen.blit(IMAGES['numbers'][digital_numbers[2]], (145, 470))
            screen.blit(IMAGES[text], (105, 430))

    elif text == "generation":

        if len(digital_numbers) == 1:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (250, 470))
            screen.blit(IMAGES[text], (195, 430))
        elif len(digital_numbers) == 2:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (250, 470))
            screen.blit(IMAGES['numbers'][digital_numbers[1]], (275, 470))
            screen.blit(IMAGES[text], (195, 430))
        else:
            screen.blit(IMAGES['numbers'][digital_numbers[0]], (225, 470))
            screen.blit(IMAGES['numbers'][digital_numbers[1]], (250, 470))
            screen.blit(IMAGES['numbers'][digital_numbers[2]], (275, 470))
            screen.blit(IMAGES[text], (195, 430))


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
