from random import randint
import sys
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
BALLOON_CHANGE = 4
BOW_CHANGE = 1
ARROW_CHANGE = BALLOON_CHANGE * 10
WHITE_RGB = (255, 255, 255)
BLACK_RGB = (0, 0, 0)

pygame.init()

class Balloon:
    def __init__(self) -> None:
        """ Balloon constructor. Randomly generates starting y-coordinate, always starts on the far left column."""
        self.x = 0
        self.y = randint(0, SCREEN_HEIGHT_END)
        self.image = pygame.image.load("images/balloon.png")

    def move(self) -> None:
        """ Randomly determines where the ballon goes and by how much """
        self.y += randint(-BALLOON_CHANGE, BALLOON_CHANGE)

class Bow:
    def __init__(self) -> None:
        """ Bow constructor. Always starts far right in the middle far right column."""
        self.x = SCREEN_LENGTH_END
        self.y = SCREEN_HEIGHT_END / 2
        self.image = pygame.image.load("images/bow.png")

    def moveUp(self) -> None:
        """ Moves the bow up and prints it in its new location. """
        self.y -= BOW_CHANGE
        if self.y < 0:
            self.y = 0

    def moveDown(self) -> None:
        """ Moves the bow down and prints it in its new location. """
        self.y += BOW_CHANGE
        if self.y > SCREEN_HEIGHT_END:
            self.y = SCREEN_HEIGHT_END

class Arrow:
    def __init__(self, bow: Bow) -> None:
        """ Arrow constructor."""
        self.x = -100
        self.y = -100
        self.state = "ready"
        self.image = pygame.image.load("images/arrow.png")

    def setStateFire(self) -> None:
        self.state = "fire"
        
    def printArrow(self, bow: Bow) -> None:
        """ Prints the balloon in front of the bow. """
        self.x = bow.x - IMAGE_SIDE_LENGTH
        self.y = bow.y

    def fireArrow(self) -> None:
        """ Arrow will move towards balloon. """
        self.x -= ARROW_CHANGE
        if self.x < 0:
            self.state = "ready"
            self.x = -100
            self.y = -100


class Game():
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.balloon = Balloon()
        self.bow = Bow()
        self.arrow = Arrow(self.bow)
        self.score_value = 0
        self.game_over = False
        pygame.display.set_caption("Balloon game")
        pygame.display.set_icon(self.balloon.image)

        while 1:
            self.loop()


    def loop(self):
        """ The main game loop."""
        self.eventLoop()
        self.draw()
        pygame.display.update()

    def eventLoop(self):
        """ The main event loop, detects keypresses and updates movements."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if not self.game_over:
            # Balloon Movement
            self.balloon.move()

            # Bow Movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.bow.moveUp()
            if keys[pygame.K_DOWN]:
                self.bow.moveDown()

            # Arrow Movement
            if keys[pygame.K_SPACE] and self.arrow.state == "ready":
                self.arrow.setStateFire()
                self.arrow.printArrow(self.bow)
                self.score_value += 1
            if self.arrow.state == "fire":
                self.arrow.fireArrow()
            
            if self.is_collision():
                self.game_over = True


    def draw(self):
        """ Calls all bilts for all objects needed. """
        self.screen.fill(WHITE_RGB)
        #Score
        score_font = pygame.font.Font("freesansbold.ttf", 32)
        score_text = score_font.render("Missed Shots: " + str(self.score_value), True, BLACK_RGB)
        self.screen.blit(score_text, (700, 0))
        if self.game_over:
            game_over_font = pygame.font.Font("freesansbold.ttf", 64)
            game_over_text = game_over_font.render("GAME OVER", True, BLACK_RGB)
            self.screen.blit(game_over_text, game_over_text.get_rect(center = self.screen.get_rect().center))
        else:
            self.screen.blit(self.balloon.image, (self.balloon.x, self.balloon.y))
            self.screen.blit(self.arrow.image, (self.arrow.x, self.arrow.y))
            self.screen.blit(self.bow.image, (self.bow.x, self.bow.y))
    
    def is_collision(self) -> bool:
        """ Returns true if arrow and balloon collides with each other. """
        a = self.arrow
        b = self.balloon
        if b.image.get_rect(x = b.x, y = b.y).colliderect(a.image.get_rect(x = a.x, y = a.y)):
            return True
        else:
            return False

if __name__ == "__main__":
    Game()