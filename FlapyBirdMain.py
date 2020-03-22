import pygame
import neat
import time
import os
import random

# Window resolution
WIN_WIDTH = 500
WIN_HEIGHT = 800
# imported bird, pipe and ground images used to create animations
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


# Bird class holds information about velocity, rotation, animation duration and image
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    # constructor of Bird class
    # Creates default Bird object on x,y coordinates
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    # jump method sets velocity and assigns height depending on y coordinate
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        # add tick every frame
        self.tick_count += 1
        # how many pixels moving up/down this frame (displacement)
        frame_move = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        # terminal velocity  ( maximal speed moving down)
        if frame_move >= 16:
            frame_move = 16
        # add some speed moving upwards ( tunes movement)
        if frame_move < 0:
            frame_move -= 2
        # change y coordinate based on displacement
        self.y = self.y + frame_move
        # tilt the birds upwards
        if frame_move < 0 or self.y < self.height + 50:
            # check whether bird is tilted correctly ( prevent tilting wrong direction)
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        # tilt bird downwards
        else:
            # tilt bird 90 degrees downwards (nose-diving bird)
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    # animate bird on the window
    def draw(self, win):
        # save how many times one image was shown
        self.img_count += 1
        # display bird images according to img_count ( bird is flapping up and down :) )
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
            # after all images was displayed, show image 1 and then 0 to make animation smooth
            # without this statements bird looks like skipping frames
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        # when bird downwards prevent bird to flap wings
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
        # Rotate bird image around its center using pygame
        # (tilting bird image, this rotates image around top left hand corner)
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # move image to the center
        rectangle_position = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        # Blitting (drawing)  the image on the screen
        # Blitting - copy pixels belonging to said object onto the destination object
        win.blit(rotated_image, rectangle_position.topleft)

    # method for collision detection // TO DO collision
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


# draw window  method, creates window and bird
def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.update()


# main method starts game using pygame library and creates simple bird object
def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)

    pygame.quit()
    quit()


main()
