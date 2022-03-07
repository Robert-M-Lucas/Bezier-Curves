import pygame


class Handle:
    def __init__(self, color=(255, 255, 255), pos=(100, 100)):
        self.r = 10
        self.color = color
        self.pos = pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.r)


class LerpHandle:
    def __init__(self, h1, h2, color=(0, 255, 0)):
        self.h1, self.h2 = h1, h2
        self.color = color
        self.r = 5
        self.progress = 0
        self.pos = (0, 0)

    def draw(self, screen, draw=True):
        self.pos = (self.h1.pos[0] + ((self.h2.pos[0] - self.h1.pos[0]) * self.progress),
                            self.h1.pos[1] + ((self.h2.pos[1] - self.h1.pos[1]) * self.progress))

        if draw:
            pygame.draw.circle(screen, self.color, self.pos, self.r)