import pygame
class Tileset:
    def __init__(self, img, size=(8, 8)) -> None:
        self.size = size
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.tiles = []
        self.load()
    def load(self):
        self.tiles = []
        width, height = self.rect.size
        ws, hs = width//self.size[0], height//self.size[1]
        for y in range(0, hs):
            for x in range(0, ws):
                tile = pygame.Surface(self.size)
                tile.blit(self.img, (0, 0), (x*self.size[0], y*self.size[1], *self.size))
                self.tiles.append(tile)
