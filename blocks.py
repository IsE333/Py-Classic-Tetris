import numpy
import pygame
class Blocks:
    def __init__(self,gameMap,type,level) -> None:
        self.gameMap = gameMap
        self.type=type #0 to 6 integer
        self.nextBlockType = numpy.random.randint(0,7)
        self.rotation = 0 #0 to 3 integer
        self.map = numpy.zeros((4, 4), dtype= int)
        self.level = level
        speeds=48,43,38,33,28,23,18,13,8,6,5,5,5,4,4,4,3,3,3,2,2,2,2,2,2,2,2,2,2 #frames
        self.speed = 1/60
        if level<29: self.speed = speeds[level]/60 #seconds
        self.isMoving = True
        self.isStuck = False
        self.position = [0,3] #y,x
        self.lastPosition = [[0 for _ in range(2)] for _ in range(4)] #relative to gameMap
        self.map = numpy.zeros((4, 4), dtype= int)
        temp = 1,1,1,1 
        if (self.type==0): self.map[0][1],self.map[0][2],self.map[0][3],self.map[1][2]=temp #T
        elif (self.type==1): self.map[0][1],self.map[0][2],self.map[0][3],self.map[1][3]=temp #J
        elif (self.type==2): self.map[0][1],self.map[0][2],self.map[1][2],self.map[1][3]=temp #Z
        elif (self.type==3): self.map[0][1],self.map[0][2],self.map[1][1],self.map[1][2]=temp #O
        elif (self.type==4): self.map[0][2],self.map[0][3],self.map[1][1],self.map[1][2]=temp #S
        elif (self.type==5): self.map[0][1],self.map[0][2],self.map[0][3],self.map[1][1]=temp #L
        elif (self.type==6): self.map[0][0],self.map[0][1],self.map[0][2],self.map[0][3]=temp #I
        self.printBlock()
    def button(self,button):
        if button == 0:
            temp=[-1,-1,-1,-1]
            canMove=True
            for y1 in range(0,4):
                for x1 in range(0,4):
                    if self.map[3-y1][x1] != 0 and temp[3-y1] == -1:
                        y = self.position[0] + 3-y1
                        x = self.position[1] + x1
                        temp[3-y1]=x1
                        if x-1<0 or self.gameMap[y][x-1] != 255: # cheks if the blok is on the edge of the map or a block
                            canMove=False 
                            break
            if canMove: 
                self.position[1] -= 1
                self.printBlock()
        if button == 1:
            temp=[-1,-1,-1,-1]
            canMove=True
            for y1 in range(0,4):
                for x1 in range(0,4):
                    if self.map[3-y1][3-x1] != 0 and temp[3-y1] == -1:
                        y = self.position[0] + 3-y1
                        x = self.position[1] + 3-x1
                        temp[3-y1]=3-x1
                        if x+1>9 or self.gameMap[y][x+1] != 255: # cheks if the blok is on the edge of the map or a block
                            canMove=False 
                            break
            if canMove: 
                self.position[1] += 1
                self.printBlock()
        if button ==2:
            self.rotate(1)
        if button ==3:
            self.rotate(-1)
    def setLast(self):
        counter=0
        for y in range(0,4):
            for x in range(0,4):
                if self.map[y][x]==1:
                    self.lastPosition[counter]=[y+self.position[0],x+self.position[1]]
                    counter+=1
    def rotate(self,direction):
        self.rotation = (self.rotation+direction)%4
        self.map = numpy.zeros((4, 4), dtype= int)
        temp = 1,1,1,1
        if (self.type==0 and self.rotation==0): self.map[0][1],self.map[0][2],self.map[0][3],self.map[1][2]=temp #T
        elif (self.type==0 and self.rotation==1): self.map[0][2],self.map[1][1],self.map[1][2],self.map[2][2]=temp #T
        elif (self.type==0 and self.rotation==2): self.map[0][2],self.map[1][1],self.map[1][2],self.map[1][3]=temp #T
        elif (self.type==0 and self.rotation==3): self.map[0][2],self.map[1][2],self.map[1][3],self.map[2][2]=temp #T
        elif (self.type==1 and self.rotation==0): self.map[0][1],self.map[0][2],self.map[0][3],self.map[1][3]=temp #J
        elif (self.type==1 and self.rotation==1): self.map[0][2],self.map[1][2],self.map[2][1],self.map[2][2]=temp #J
        elif (self.type==1 and self.rotation==2): self.map[0][1],self.map[1][1],self.map[1][2],self.map[1][3]=temp #J
        elif (self.type==1 and self.rotation==3): self.map[0][2],self.map[0][3],self.map[1][2],self.map[2][2]=temp #J
        elif (self.type==2 and self.rotation%2==0): self.map[0][1],self.map[0][2],self.map[1][2],self.map[1][3]=temp #Z
        elif (self.type==2 and self.rotation%2==1): self.map[0][3],self.map[1][2],self.map[1][3],self.map[2][2]=temp #Z
        elif (self.type==3): self.map[0][1],self.map[0][2],self.map[1][1],self.map[1][2]=temp #O
        elif (self.type==4 and self.rotation%2==0): self.map[0][2],self.map[0][3],self.map[1][1],self.map[1][2]=temp #S
        elif (self.type==4 and self.rotation%2==1): self.map[0][2],self.map[1][2],self.map[1][3],self.map[2][3]=temp #S
        elif (self.type==5 and self.rotation==0): self.map[0][1],self.map[0][2],self.map[0][3],self.map[1][1]=temp #L
        elif (self.type==5 and self.rotation==1): self.map[0][2],self.map[0][3],self.map[1][3],self.map[2][3]=temp #L
        elif (self.type==5 and self.rotation==2): self.map[0][3],self.map[1][1],self.map[1][2],self.map[1][3]=temp #L
        elif (self.type==5 and self.rotation==3): self.map[0][2],self.map[1][2],self.map[2][2],self.map[2][3]=temp #L
        elif (self.type==6 and self.rotation%2==0): self.map[0][0],self.map[0][1],self.map[0][2],self.map[0][3]=temp #I
        elif (self.type==6 and self.rotation%2==1): self.map[0][2],self.map[1][2],self.map[2][2],self.map[3][2]=temp #I
        canMove=True
        for y1 in range(0,4):
            for x1 in range(0,4):
                y = self.position[0] + 3-y1
                x = self.position[1] + 3-x1
                if self.map[3-y1][3-x1] != 0 and [y,x] not in self.lastPosition:
                    if x<0 or x>9 or 0>y or y>19 or self.gameMap[y][x] != 255: # cheks if the blok is on the edge of the map or a block
                        canMove=False 
                        break
        if canMove: 
            self.printBlock()
        else: #turn back
            self.rotation = (self.rotation+2)%4
            self.rotate(1)
    def printBlock(self):
        for c in range(0,4):
            self.gameMap[self.lastPosition[c][0],self.lastPosition[c][1]] = 255 #remove the last block
        for y1 in range(0,4):
                for x1 in range(0,4):
                    if self.map[3-y1][3-x1] != 0:
                        y = self.position[0] + 3-y1
                        x = self.position[1] + 3-x1
                        if y>=0:
                            if self.level%2 == 0: self.gameMap[y][x] = 123+((self.type)%3) #add
                            elif self.level%2 == 1: self.gameMap[y][x] = 124+((self.type)%3)
        self.setLast()
    def tick(self):
        self.isMoving=True
        basePoints = [-1,-1,-1,-1]
        for y1 in range(0,4):
            for x1 in range(0,4):
                if self.map[3-y1][3-x1] != 0 and basePoints[3-x1] == -1:
                    basePoints[3-x1] = 3-y1
        for a in range(0,4):
            if basePoints[a] != -1:
                y2 = self.position[0] + basePoints[a] + 1
                x2 = self.position[1] + a
                if y2 > 19:
                    self.isMoving = False
                    break
                if self.gameMap[y2][x2] !=255: #check if any basepoint is colliding gamemap
                    self.isMoving = False
                    if self.position[0] == 0:
                        self.isStuck = True
                    break
        if self.isMoving:
            self.position[0]+=1
        self.printBlock()
        return self.gameMap
    def check(self): #for clearing lines and clear
        filledLines=[] # full lines
        sound=-1
        for y1 in range(0,20):
            temp = True
            for x1 in range(0,10):
                if self.gameMap[y1][x1] == 255:
                    temp = False
                    break
            if temp: filledLines.append(y1)
        if(len(filledLines) != 0):
            if len(filledLines)==4: sound = 0
            else: sound = 1
            oldGameMap = numpy.copy(self.gameMap)
            oldGameMap = numpy.delete(oldGameMap,filledLines,axis=0)
            for _ in range(0,len(filledLines)):
                oldGameMap = numpy.insert(oldGameMap,0,[255 for _ in range(0,10)],axis=0)
            self.gameMap= oldGameMap
        return sound,len(filledLines),self.gameMap
    def lastCheck(self): #for movement
        self.tick()
        if not self.isMoving: 
            return False
        else: return True
        

