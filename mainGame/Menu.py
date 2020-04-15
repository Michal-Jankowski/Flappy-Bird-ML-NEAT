import pygame
from mainGame import Model as train
from mainGame import BestModel as best

pygame.init()
win = pygame.display.set_mode((500, 500))
win.fill((255, 255, 255))


class Logo(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Background(pygame.sprite.Sprite):
    def __init__(self, image_name, location):
        # call pygame Sprite initializer
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# Button class
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def redrawWindow():
    trainButton.draw(win, (0, 0, 0))
    bestButton.draw(win, (0, 0, 0))


def quitGame():
    global run
    run = False
    pygame.quit()
    quit()


run = True
trainButton = Button((0, 255, 0), 175, 150, 150, 50, "Train")
bestButton = Button((0, 255, 0), 175, 220, 150, 50, "Best")
background = Background("..//assets//sprites//background-blue.png", [0, 0])
logo = Logo("../assets/sprites/flappy_bird_logov1.png", [125, 50])
while run:
    win.fill([1, 1, 155])
    win.blit(background.image, background.rect)
    win.blit(logo.image, logo.rect)
    redrawWindow()
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
    if event.type == pygame.QUIT:
        quitGame()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if trainButton.isOver(pos):
            train.main()
            quitGame()
        if bestButton.isOver(pos):
            best.main()
            quitGame()

    if event.type == pygame.MOUSEMOTION:
        if trainButton.isOver(pos):
            trainButton.color = (255, 0, 0)
        else:
            trainButton.color = (0, 255, 0)

        if bestButton.isOver(pos):
            bestButton.color = (255, 0, 0)
        else:
            bestButton.color = (0, 255, 0)
