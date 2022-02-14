from gettext import dpgettext
import numpy
import pygame
from pygame.key import start_text_input
from tileSet import Tileset
from tileMap import TileMap
from blocks import Blocks
from nextBlock import NextBlock
from score import Score
class GameLoop:
    def __init__(self,startLevel) -> None:
        pygame.init()
        self.cw, self.ch = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.w, self.h = self.cw,self.ch
        if self.cw/self.ch > 32/30: self.w,self.h= self.ch*32/30,self.ch
        if self.cw/self.ch < 32/30: self.w,self.h= self.cw*30/32,self.cw
        self.screen = pygame.display.set_mode((self.cw, self.ch), pygame.FULLSCREEN)
        self.background_colour = (0, 0, 32)
        self.startLevel = int(startLevel)
    def loop(self):
        sLevelSelect = pygame.mixer.Sound("sounds/levelSelect.wav")
        pygame.mixer.Sound.play(sLevelSelect)
        pygame.display.set_caption("Tetris")
        FPS = 60
        fpsClock = pygame.time.Clock()

        sRotate = pygame.mixer.Sound("sounds/rotate.wav")
        sBlockDown = pygame.mixer.Sound("sounds/blockDown.wav")
        s1line = pygame.mixer.Sound("sounds/1line.wav")
        s4lines = pygame.mixer.Sound("sounds/4lines.wav")
        sPause = pygame.mixer.Sound("sounds/pause.wav")
        sMovement = pygame.mixer.Sound("sounds/movement.wav")
        sTopout = pygame.mixer.Sound("sounds/topout.wav")
        sLevelUp = pygame.mixer.Sound("sounds/levelUp.wav")
        tileset = Tileset('t.png')
        tileset.load()
        tMLineC = TileMap(tileset,4,1)
        tMTopSC = TileMap(tileset,6,1)
        tMScoreC = TileMap(tileset,6,1)
        tMLevel = TileMap(tileset,2,1)
        tMStats = TileMap(tileset,3,14)
        tMBlockMap = TileMap(tileset,10,20)
        tMBlockMap.set_zero()
        level = numpy.array([self.startLevel//10,self.startLevel%10])
        bg = pygame.image.load('b.png')
        block = Blocks(tMBlockMap.map, numpy.random.randint(0,7),int(str(level[0])+str(level[1])))
        nextBlock = NextBlock(block.nextBlockType,block.level,tileset)
        score = Score(block.level)
        nextBlock.generateNext()
        score.statUpdate(block.type)
        frameCounter = 0
        continuity = True
        dasCharge=0
        lastDirection=0
        oldLineCount=0
        dPressTime=0
        pause=False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_LEFT and not pause:
                        pygame.mixer.Sound.play(sMovement)
                        dasCharge=4
                        lastDirection=0
                        block.button(0)
                    if event.key == pygame.K_RIGHT and not pause:
                        pygame.mixer.Sound.play(sMovement)
                        dasCharge=4
                        lastDirection=1
                        block.button(1)
                    if event.key == pygame.K_DOWN and not pause:
                        continuity = True
                    if event.key == pygame.K_s and not pause: #rotate clockwise
                        pygame.mixer.Sound.play(sRotate)
                        block.button(2)
                    if event.key == pygame.K_a and not pause: #rotate reverse clockwise
                        pygame.mixer.Sound.play(sRotate)
                        block.button(3)
                    if event.key == pygame.K_w: #pause
                        if not pause: pygame.mixer.Sound.play(sPause)
                        pause=not pause
                    if event.key == pygame.K_r: #restart
                        tMBlockMap.set_zero()
                        block = Blocks(tMBlockMap.map, block.nextBlockType,int(str(level[0])+str(level[1])))
                        score.reset(block.level,0)
                        level = numpy.array([0,9])
                        score.lineC = numpy.array([0,0,0,0])
                        score.stats = numpy.array([ [255*(a%2),255*(a%2),255*(a%2)] for a in range(14)])
            keys = pygame.key.get_pressed()
            if not block.isMoving: continuity = False
            if continuity: 
                dPressTime+=1
                frameCounter+=keys[pygame.K_DOWN]*100*block.speed
            else: 
                score.pressDown(dPressTime)
                dPressTime=0
            dasCharge+=(keys[pygame.K_LEFT] and not pause or keys[pygame.K_RIGHT] and not pause)*1
            if dasCharge == 16:
                block.button(lastDirection)
                dasCharge=12
            if (block.nextBlockType!=nextBlock.type):
                nextBlock = NextBlock(block.nextBlockType,block.level,tileset)
                nextBlock.generateNext()
            if frameCounter >= block.speed*60:
                if not block.isStuck:
                    if not block.isMoving:
                        lastCheck=block.lastCheck()
                        if not lastCheck:
                            lineSound,lineCount,tMBlockMap.map=block.check()
                            score.statUpdate(block.type)
                            levelCheck,level = score.lineCountUpdate(lineCount)
                            score.lineClear(lineCount-oldLineCount)
                            if levelCheck: pygame.mixer.Sound.play(sLevelUp)#for not playing two or more sounds at once
                            elif lineSound==0: pygame.mixer.Sound.play(s4lines)
                            elif lineSound==1: pygame.mixer.Sound.play(s1line)
                            else: pygame.mixer.Sound.play(sBlockDown)
                            oldLineCount=lineCount
                            block = Blocks(tMBlockMap.map, block.nextBlockType,int(str(level[0])+str(level[1])))
                    else:
                        tMBlockMap.map=block.tick()
                    frameCounter = 0
                else:
                    if frameCounter<100:
                        pygame.mixer.Sound.play(sTopout)
                        score.reset(block.level,1)
                        frameCounter=100
            if not pause: frameCounter+=1
            tMLevel.map[0] = level
            tMStats.map = score.stats
            tMLineC.map[0] = score.lineC
            tMScoreC.map[0] = score.map
            tMTopSC.map[0] = score.maxScoreMap
            tMBlockMap.render()
            tMLineC.render()
            tMLevel.render()
            tMScoreC.render()
            tMTopSC.render()
            tMStats.render()
            self.screen.blit(pygame.transform.scale(bg, (self.w,self.h)), ((self.cw-self.w)/2, (self.ch-self.h)/2))
            self.screen.blit(pygame.transform.scale(tMBlockMap.image, (self.w*10/32,self.h*20/30)), (((self.cw-self.w)/2)+12*self.w/32, ((self.ch-self.h)/2)+6*self.h/30))
            self.screen.blit(pygame.transform.scale(tMStats.image, (self.w*3/32,self.h*14/30)), (((self.cw-self.w)/2)+6*self.w/32, ((self.ch-self.h)/2)+12*self.h/30))
            self.screen.blit(pygame.transform.scale(tMLevel.image, (self.w*2/32,self.h*1/30)), (((self.cw-self.w)/2)+26*self.w/32, ((self.ch-self.h)/2)+21*self.h/30))
            self.screen.blit(pygame.transform.scale(tMScoreC.image, (self.w*6/32,self.h*1/30)), (((self.cw-self.w)/2)+24*self.w/32, ((self.ch-self.h)/2)+8*self.h/30))
            self.screen.blit(pygame.transform.scale(tMTopSC.image, (self.w*6/32,self.h*1/30)), (((self.cw-self.w)/2)+24*self.w/32, ((self.ch-self.h)/2)+5*self.h/30))
            self.screen.blit(pygame.transform.scale(tMLineC.image, (self.w*4/32,self.h*1/30)), (((self.cw-self.w)/2)+18*self.w/32, ((self.ch-self.h)/2)+3*self.h/30))
            self.screen.blit(pygame.transform.scale(nextBlock.image, (self.w*4/32,self.h*4/30)), (((self.cw-self.w)/2)+24*self.w/32, ((self.ch-self.h)/2)+14*self.h/30))
            pygame.display.update()
            fpsClock.tick(FPS)
    