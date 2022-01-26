from random import randint
import pygame
# Coded in pygame version 2.1.2

#### Constants ####
# All units of length are in pixels.
# All images are 64x64 pixels.
SCREEN_LENGTH = 1000
SCREEN_HEIGHT = 500
IMAGE_SIDE_LENGTH = 64
SCREEN_LENGTH_END = SCREEN_LENGTH - IMAGE_SIDE_LENGTH
SCREEN_HEIGHT_END = SCREEN_HEIGHT - IMAGE_SIDE_LENGTH
BALLOON_CHANGE = 0.5
BOW_CHANGE = 1
ARROW_CHANGE = BALLOON_CHANGE * 10
WHITE_RGB = (255, 255, 255)
BLACK_RGB = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))


pygame.display.set_caption("Balloon game")
balloonImage = pygame.image.load("images/balloon.png")
pygame.display.set_icon(balloonImage)


class Balloon:
    def __init__(self) -> None:
        """ Balloon constructor. Randomly generates starting y-coordinate, always starts on the far left column."""
        self.x = 0
        self.y = randint(0, SCREEN_HEIGHT_END)
        self.image = balloonImage
        
    def printBalloon(self) -> None:
        """ Prints the balloon at its current location. """
        screen.blit(self.image, (self.x, self.y))

    def moveUp(self) -> None:
        """ Moves the balloon up and prints it in its new location. """
        self.y -= BALLOON_CHANGE
        if self.y < 0:
            self.y = 0
        screen.blit(self.image, (self.x, self.y))

    def moveDown(self) -> None:
        """ Moves the balloon down and prints it in its new location. """
        self.y += BALLOON_CHANGE
        if self.y > SCREEN_HEIGHT_END:
            self.y = SCREEN_HEIGHT_END
        screen.blit(self.image, (self.x, self.y))

class Bow:
    def __init__(self) -> None:
        """ Bow constructor. Always starts far right in the middle far right column."""
        self.x = SCREEN_LENGTH_END
        self.y = SCREEN_HEIGHT_END / 2
        self.image = pygame.image.load("images/bow.png")

    def printBow(self) -> None:
        """ Prints the bow at its current location. """
        screen.blit(self.image, (self.x, self.y))

    def moveUp(self) -> None:
        """ Moves the bow up and prints it in its new location. """
        self.y -= BOW_CHANGE
        if self.y < 0:
            self.y = 0
        screen.blit(self.image, (self.x, self.y))

    def moveDown(self) -> None:
        """ Moves the bow down and prints it in its new location. """
        self.y += BOW_CHANGE
        if self.y > SCREEN_HEIGHT_END:
            self.y = SCREEN_HEIGHT_END
        screen.blit(self.image, (self.x, self.y))

class Arrow:
    def __init__(self, bow: Bow) -> None:
        """ Arrow constructor."""
        self.x = bow.x - IMAGE_SIDE_LENGTH
        self.y = bow.y
        self.state = "ready"
        self.image = pygame.image.load("images/arrow.png")

    def setStateFire(self) -> None:
        self.state = "fire"
        
    def printArrow(self, bow: Bow) -> None:
        """ Prints the balloon in front of the bow. """
        self.x = bow.x - IMAGE_SIDE_LENGTH
        self.y = bow.y
        screen.blit(self.image, (self.x, self.y))

    def fireArrow(self) -> None:
        """ Arrow will move towards balloon. """
        self.x -= ARROW_CHANGE
        if self.x < 0:
            self.state = "ready"
        screen.blit(self.image, (self.x, self.y))

#### Driver Loop ####
balloon = Balloon()
bow = Bow()
arrow = Arrow(bow)
score_value = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)
running = True
while running:
    screen.fill(WHITE_RGB)
    #Score
    score = score_font.render("Missed Shots: " + str(score_value), True, BLACK_RGB)
    screen.blit(score, (740, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Balloon Movement
    rand_num = randint(0, 2)
    if rand_num == 0:
        balloon.moveDown()
    elif rand_num == 1:
        balloon.moveUp()
    else:
        balloon.printBalloon()

    # Bow Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        bow.moveUp()
    if keys[pygame.K_DOWN]:
        bow.moveDown()
    bow.printBow()

    # Arrow Movement
    if keys[pygame.K_SPACE] and arrow.state == "ready":
        arrow.setStateFire()
        arrow.printArrow(bow)
        score_value += 1
    if arrow.state == "fire":
        arrow.fireArrow()

    # Collision
    if balloon.image.get_rect(x = balloon.x, y = balloon.y).colliderect(arrow.image.get_rect(x = arrow.x, y = arrow.y)):
        game_over_font = pygame.font.Font("freesansbold.ttf", 64)
        game_over = game_over_font.render("GAME OVER", True, BLACK_RGB)
        screen.blit(game_over, game_over.get_rect(center = screen.get_rect().center))

    pygame.display.update()
