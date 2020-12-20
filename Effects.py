import pygame


class Hover(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite = pygame.image.load("assets/hover.png")
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.image.blit(self.sprite, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 60, abs((480 - 60) - y * 60)


class PathDot(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite = pygame.image.load("assets/path.png")
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.image.blit(self.sprite, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 60, abs((480 - 60) - y * 60)


class CheckHover(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite = pygame.image.load("assets/check.png")
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.image.blit(self.sprite, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 60, abs((480 - 60) - y * 60)


class CheckMakeHover(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite = pygame.image.load("assets/checkMate.png")
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.image.blit(self.sprite, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 60, abs((480 - 60) - y * 60)