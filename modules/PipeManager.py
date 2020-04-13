from configes.Config import *
from modules.Pipe import Pipe


class PipeManager(object):
    def __init__(self, pipeFirst, pipeSecond):
        self.upper_first_x = pipeFirst.x
        self.upper_second_x = pipeSecond.x
        self.movement_velocity = -4

        self.lower = [{'x': SCREENWIDTH + 200, 'y': pipeFirst.y_lower},
                      {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': pipeSecond.y_lower}]

        self.upper = [{'x': SCREENWIDTH + 200, 'y': pipeFirst.y_upper},
                      {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': pipeSecond.y_upper}]

    def move(self, birds):
        for upper_pipe, lower_pipe in zip(self.upper, self.lower):
            lower_pipe['x'] += self.movement_velocity
            upper_pipe['x'] += self.movement_velocity
            for bird in birds:
                bird.distance += self.movement_velocity

        self.update()

    def add(self, pipe):
        pipe = Pipe()
        self.lower.append(pipe.get_lower())
        self.upper.append(pipe.get_upper())

    def remove(self):
        self.lower.pop(0)
        self.upper.pop(0)

    def update(self):
        if 0 < self.upper[0]["x"] and 5 > self.upper[0]["x"]:
            self.add(Pipe())

        if -IMAGES["pipe"][0].get_width() > self.upper[0]["x"]:
            self.remove()

    def draw(self, SCREEN):
        for upper_pipe, lower_pipe in zip(self.lower, self.upper):
            SCREEN.blit(IMAGES["pipe"][0], (lower_pipe["x"], lower_pipe["y"]))
            SCREEN.blit(IMAGES["pipe"][1], (upper_pipe["x"], upper_pipe["y"]))
