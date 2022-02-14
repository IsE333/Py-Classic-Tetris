import numpy
import pygame
class NextBlock:
    def __init__(self,type,level,tileset) -> None:
        self.type=type
        self.level=level
        self.tileset = tileset
        self.map = numpy.zeros((4, 4), dtype= int)
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.square = pygame.Surface((32, 32))
    def generateNext(self):
        temp = 1,1,1,1
        if (self.type==0): self.map[0][1],self.map[0][2],self.map[0][3],self.map[1][2]=temp #T
        elif (self.type==1): self.map[0][1],self.map[0][2],self.map[0][3],self.map[1][3]=temp #J
        elif (self.type==2): self.map[0][1],self.map[0][2],self.map[1][2],self.map[1][3]=temp #Z
        elif (self.type==3): self.map[0][1],self.map[0][2],self.map[1][1],self.map[1][2]=temp #O
        elif (self.type==4): self.map[0][2],self.map[0][3],self.map[1][1],self.map[1][2]=temp #S
        elif (self.type==5): self.map[0][1],self.map[0][2],self.map[0][3],self.map[1][1]=temp #L
        elif (self.type==6): self.map[0][0],self.map[0][1],self.map[0][2],self.map[0][3]=temp #I
        m, n = self.map.shape
        xmax,ymax = -1,-1
        xmin,ymin = 4,4
        for i in range(m):
            for j in range(n):
                if self.map[i][j]==1 and xmin>j: xmin = j
                if self.map[i][j]==1 and ymin>i: ymin = i
                if self.map[i][j]==1 and xmax<j: xmax = j
                if self.map[i][j]==1 and ymax<i: ymax = i
        cx,cy=(xmin-(3-xmax))/2,(ymin-(3-ymax))/2
        if self.level%2 == 0: tile = self.tileset.tiles[123+((self.type)%3)]
        elif self.level%2 == 1: tile = self.tileset.tiles[124+((self.type)%3)]
        for i in range(m):
            for j in range(n):
                if self.map[i][j]==1: self.image.blit(tile, ((j-cx)*8, (i-cy)*8))
        