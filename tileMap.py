import pygame
import numpy
class TileMap:
    def __init__(self, tileset,x,y) -> None:
        self.x=x
        self.y=y
        self.tileset = tileset
        self.image = pygame.Surface((8*self.x, 8*self.y))
        self.rect = self.image.get_rect()
        self.map = numpy.zeros((self.y, self.x), dtype= int)
    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*8, i*8))
    def set_zero(self):
        a = 0x16
        self.map = numpy.zeros((self.y, self.x), dtype= int)
        self.map = numpy.array([[255 for _ in range(self.x)] for _ in range(self.y)])
        self.render()
    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = numpy.random.randint(n, size=(self.y, self.x))
        self.render()